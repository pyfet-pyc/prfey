# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
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
    return (suiteClass((test,)), message)


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

    def loadTestsFromModule--- This code section failed: ---

 L. 104         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'args'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_CONST               0
                8  COMPARE_OP               >
               10  POP_JUMP_IF_TRUE     20  'to 20'
               12  LOAD_STR                 'use_load_tests'
               14  LOAD_FAST                'kws'
               16  <118>                 0  ''
               18  POP_JUMP_IF_FALSE    44  'to 44'
             20_0  COME_FROM            10  '10'

 L. 105        20  LOAD_GLOBAL              warnings
               22  LOAD_METHOD              warn
               24  LOAD_STR                 'use_load_tests is deprecated and ignored'

 L. 106        26  LOAD_GLOBAL              DeprecationWarning

 L. 105        28  CALL_METHOD_2         2  ''
               30  POP_TOP          

 L. 107        32  LOAD_FAST                'kws'
               34  LOAD_METHOD              pop
               36  LOAD_STR                 'use_load_tests'
               38  LOAD_CONST               None
               40  CALL_METHOD_2         2  ''
               42  POP_TOP          
             44_0  COME_FROM            18  '18'

 L. 108        44  LOAD_GLOBAL              len
               46  LOAD_FAST                'args'
               48  CALL_FUNCTION_1       1  ''
               50  LOAD_CONST               1
               52  COMPARE_OP               >
               54  POP_JUMP_IF_FALSE    82  'to 82'

 L. 111        56  LOAD_GLOBAL              len
               58  LOAD_FAST                'args'
               60  CALL_FUNCTION_1       1  ''
               62  LOAD_CONST               1
               64  BINARY_ADD       
               66  STORE_FAST               'complaint'

 L. 112        68  LOAD_GLOBAL              TypeError
               70  LOAD_STR                 'loadTestsFromModule() takes 1 positional argument but {} were given'
               72  LOAD_METHOD              format
               74  LOAD_FAST                'complaint'
               76  CALL_METHOD_1         1  ''
               78  CALL_FUNCTION_1       1  ''
               80  RAISE_VARARGS_1       1  'exception instance'
             82_0  COME_FROM            54  '54'

 L. 113        82  LOAD_GLOBAL              len
               84  LOAD_FAST                'kws'
               86  CALL_FUNCTION_1       1  ''
               88  LOAD_CONST               0
               90  COMPARE_OP               !=
               92  POP_JUMP_IF_FALSE   120  'to 120'

 L. 118        94  LOAD_GLOBAL              sorted
               96  LOAD_FAST                'kws'
               98  CALL_FUNCTION_1       1  ''
              100  LOAD_CONST               0
              102  BINARY_SUBSCR    
              104  STORE_FAST               'complaint'

 L. 119       106  LOAD_GLOBAL              TypeError
              108  LOAD_STR                 "loadTestsFromModule() got an unexpected keyword argument '{}'"
              110  LOAD_METHOD              format
              112  LOAD_FAST                'complaint'
              114  CALL_METHOD_1         1  ''
              116  CALL_FUNCTION_1       1  ''
              118  RAISE_VARARGS_1       1  'exception instance'
            120_0  COME_FROM            92  '92'

 L. 120       120  BUILD_LIST_0          0 
              122  STORE_FAST               'tests'

 L. 121       124  LOAD_GLOBAL              dir
              126  LOAD_FAST                'module'
              128  CALL_FUNCTION_1       1  ''
              130  GET_ITER         
            132_0  COME_FROM           166  '166'
            132_1  COME_FROM           154  '154'
              132  FOR_ITER            186  'to 186'
              134  STORE_FAST               'name'

 L. 122       136  LOAD_GLOBAL              getattr
              138  LOAD_FAST                'module'
              140  LOAD_FAST                'name'
              142  CALL_FUNCTION_2       2  ''
              144  STORE_FAST               'obj'

 L. 123       146  LOAD_GLOBAL              isinstance
              148  LOAD_FAST                'obj'
              150  LOAD_GLOBAL              type
              152  CALL_FUNCTION_2       2  ''
              154  POP_JUMP_IF_FALSE   132  'to 132'
              156  LOAD_GLOBAL              issubclass
              158  LOAD_FAST                'obj'
              160  LOAD_GLOBAL              case
              162  LOAD_ATTR                TestCase
              164  CALL_FUNCTION_2       2  ''
              166  POP_JUMP_IF_FALSE   132  'to 132'

 L. 124       168  LOAD_FAST                'tests'
              170  LOAD_METHOD              append
              172  LOAD_FAST                'self'
              174  LOAD_METHOD              loadTestsFromTestCase
              176  LOAD_FAST                'obj'
              178  CALL_METHOD_1         1  ''
              180  CALL_METHOD_1         1  ''
              182  POP_TOP          
              184  JUMP_BACK           132  'to 132'

 L. 126       186  LOAD_GLOBAL              getattr
              188  LOAD_FAST                'module'
              190  LOAD_STR                 'load_tests'
              192  LOAD_CONST               None
              194  CALL_FUNCTION_3       3  ''
              196  STORE_FAST               'load_tests'

 L. 127       198  LOAD_FAST                'self'
              200  LOAD_METHOD              suiteClass
              202  LOAD_FAST                'tests'
              204  CALL_METHOD_1         1  ''
              206  STORE_FAST               'tests'

 L. 128       208  LOAD_FAST                'load_tests'
              210  LOAD_CONST               None
              212  <117>                 1  ''
          214_216  POP_JUMP_IF_FALSE   308  'to 308'

 L. 129       218  SETUP_FINALLY       234  'to 234'

 L. 130       220  LOAD_FAST                'load_tests'
              222  LOAD_FAST                'self'
              224  LOAD_FAST                'tests'
              226  LOAD_FAST                'pattern'
              228  CALL_FUNCTION_3       3  ''
              230  POP_BLOCK        
              232  RETURN_VALUE     
            234_0  COME_FROM_FINALLY   218  '218'

 L. 131       234  DUP_TOP          
              236  LOAD_GLOBAL              Exception
          238_240  <121>               306  ''
              242  POP_TOP          
              244  STORE_FAST               'e'
              246  POP_TOP          
              248  SETUP_FINALLY       298  'to 298'

 L. 132       250  LOAD_GLOBAL              _make_failed_load_tests

 L. 133       252  LOAD_FAST                'module'
              254  LOAD_ATTR                __name__
              256  LOAD_FAST                'e'
              258  LOAD_FAST                'self'
              260  LOAD_ATTR                suiteClass

 L. 132       262  CALL_FUNCTION_3       3  ''
              264  UNPACK_SEQUENCE_2     2 
              266  STORE_FAST               'error_case'
              268  STORE_FAST               'error_message'

 L. 134       270  LOAD_FAST                'self'
              272  LOAD_ATTR                errors
              274  LOAD_METHOD              append
              276  LOAD_FAST                'error_message'
              278  CALL_METHOD_1         1  ''
              280  POP_TOP          

 L. 135       282  LOAD_FAST                'error_case'
              284  POP_BLOCK        
              286  ROT_FOUR         
              288  POP_EXCEPT       
              290  LOAD_CONST               None
              292  STORE_FAST               'e'
              294  DELETE_FAST              'e'
              296  RETURN_VALUE     
            298_0  COME_FROM_FINALLY   248  '248'
              298  LOAD_CONST               None
              300  STORE_FAST               'e'
              302  DELETE_FAST              'e'
              304  <48>             
              306  <48>             
            308_0  COME_FROM           214  '214'

 L. 136       308  LOAD_FAST                'tests'
              310  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def loadTestsFromName--- This code section failed: ---

 L. 147         0  LOAD_FAST                'name'
                2  LOAD_METHOD              split
                4  LOAD_STR                 '.'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'parts'

 L. 148        10  LOAD_CONST               (None, None)
               12  UNPACK_SEQUENCE_2     2 
               14  STORE_FAST               'error_case'
               16  STORE_FAST               'error_message'

 L. 149        18  LOAD_FAST                'module'
               20  LOAD_CONST               None
               22  <117>                 0  ''
               24  POP_JUMP_IF_FALSE   150  'to 150'

 L. 150        26  LOAD_FAST                'parts'
               28  LOAD_CONST               None
               30  LOAD_CONST               None
               32  BUILD_SLICE_2         2 
               34  BINARY_SUBSCR    
               36  STORE_FAST               'parts_copy'

 L. 151        38  LOAD_FAST                'parts_copy'
               40  POP_JUMP_IF_FALSE   138  'to 138'

 L. 152        42  SETUP_FINALLY        70  'to 70'

 L. 153        44  LOAD_STR                 '.'
               46  LOAD_METHOD              join
               48  LOAD_FAST                'parts_copy'
               50  CALL_METHOD_1         1  ''
               52  STORE_FAST               'module_name'

 L. 154        54  LOAD_GLOBAL              __import__
               56  LOAD_FAST                'module_name'
               58  CALL_FUNCTION_1       1  ''
               60  STORE_FAST               'module'

 L. 155        62  POP_BLOCK        
               64  JUMP_ABSOLUTE       138  'to 138'
               66  POP_BLOCK        
               68  JUMP_BACK            38  'to 38'
             70_0  COME_FROM_FINALLY    42  '42'

 L. 156        70  DUP_TOP          
               72  LOAD_GLOBAL              ImportError
               74  <121>               134  ''
               76  POP_TOP          
               78  POP_TOP          
               80  POP_TOP          

 L. 157        82  LOAD_FAST                'parts_copy'
               84  LOAD_METHOD              pop
               86  CALL_METHOD_0         0  ''
               88  STORE_FAST               'next_attribute'

 L. 159        90  LOAD_GLOBAL              _make_failed_import_test

 L. 160        92  LOAD_FAST                'next_attribute'
               94  LOAD_FAST                'self'
               96  LOAD_ATTR                suiteClass

 L. 159        98  CALL_FUNCTION_2       2  ''
              100  UNPACK_SEQUENCE_2     2 
              102  STORE_FAST               'error_case'
              104  STORE_FAST               'error_message'

 L. 161       106  LOAD_FAST                'parts_copy'
              108  POP_JUMP_IF_TRUE    130  'to 130'

 L. 163       110  LOAD_FAST                'self'
              112  LOAD_ATTR                errors
              114  LOAD_METHOD              append
              116  LOAD_FAST                'error_message'
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          

 L. 164       122  LOAD_FAST                'error_case'
              124  ROT_FOUR         
              126  POP_EXCEPT       
              128  RETURN_VALUE     
            130_0  COME_FROM           108  '108'
              130  POP_EXCEPT       
              132  JUMP_BACK            38  'to 38'
              134  <48>             
              136  JUMP_BACK            38  'to 38'
            138_0  COME_FROM            40  '40'

 L. 165       138  LOAD_FAST                'parts'
              140  LOAD_CONST               1
              142  LOAD_CONST               None
              144  BUILD_SLICE_2         2 
              146  BINARY_SUBSCR    
              148  STORE_FAST               'parts'
            150_0  COME_FROM            24  '24'

 L. 166       150  LOAD_FAST                'module'
              152  STORE_FAST               'obj'

 L. 167       154  LOAD_FAST                'parts'
              156  GET_ITER         
              158  FOR_ITER            346  'to 346'
              160  STORE_FAST               'part'

 L. 168       162  SETUP_FINALLY       184  'to 184'

 L. 169       164  LOAD_FAST                'obj'
              166  LOAD_GLOBAL              getattr
              168  LOAD_FAST                'obj'
              170  LOAD_FAST                'part'
              172  CALL_FUNCTION_2       2  ''
              174  ROT_TWO          
              176  STORE_FAST               'parent'
              178  STORE_FAST               'obj'
              180  POP_BLOCK        
              182  JUMP_BACK           158  'to 158'
            184_0  COME_FROM_FINALLY   162  '162'

 L. 170       184  DUP_TOP          
              186  LOAD_GLOBAL              AttributeError
          188_190  <121>               342  ''
              192  POP_TOP          
              194  STORE_FAST               'e'
              196  POP_TOP          
              198  SETUP_FINALLY       334  'to 334'

 L. 172       200  LOAD_GLOBAL              getattr
              202  LOAD_FAST                'obj'
              204  LOAD_STR                 '__path__'
              206  LOAD_CONST               None
              208  CALL_FUNCTION_3       3  ''
              210  LOAD_CONST               None
              212  <117>                 1  ''
          214_216  POP_JUMP_IF_FALSE   260  'to 260'

 L. 173       218  LOAD_FAST                'error_case'
              220  LOAD_CONST               None
              222  <117>                 1  ''

 L. 172   224_226  POP_JUMP_IF_FALSE   260  'to 260'

 L. 179       228  LOAD_FAST                'self'
              230  LOAD_ATTR                errors
              232  LOAD_METHOD              append
              234  LOAD_FAST                'error_message'
              236  CALL_METHOD_1         1  ''
              238  POP_TOP          

 L. 180       240  LOAD_FAST                'error_case'
              242  POP_BLOCK        
              244  ROT_FOUR         
              246  POP_EXCEPT       
              248  LOAD_CONST               None
              250  STORE_FAST               'e'
              252  DELETE_FAST              'e'
              254  ROT_TWO          
              256  POP_TOP          
              258  RETURN_VALUE     
            260_0  COME_FROM           224  '224'
            260_1  COME_FROM           214  '214'

 L. 183       260  LOAD_GLOBAL              _make_failed_test

 L. 184       262  LOAD_FAST                'part'
              264  LOAD_FAST                'e'
              266  LOAD_FAST                'self'
              268  LOAD_ATTR                suiteClass

 L. 185       270  LOAD_STR                 'Failed to access attribute:\n%s'

 L. 186       272  LOAD_GLOBAL              traceback
              274  LOAD_METHOD              format_exc
              276  CALL_METHOD_0         0  ''

 L. 185       278  BUILD_TUPLE_1         1 
              280  BINARY_MODULO    

 L. 183       282  CALL_FUNCTION_4       4  ''
              284  UNPACK_SEQUENCE_2     2 
              286  STORE_FAST               'error_case'
              288  STORE_FAST               'error_message'

 L. 187       290  LOAD_FAST                'self'
              292  LOAD_ATTR                errors
              294  LOAD_METHOD              append
              296  LOAD_FAST                'error_message'
              298  CALL_METHOD_1         1  ''
              300  POP_TOP          

 L. 188       302  LOAD_FAST                'error_case'
              304  POP_BLOCK        
              306  ROT_FOUR         
              308  POP_EXCEPT       
              310  LOAD_CONST               None
              312  STORE_FAST               'e'
              314  DELETE_FAST              'e'
              316  ROT_TWO          
              318  POP_TOP          
              320  RETURN_VALUE     
              322  POP_BLOCK        
              324  POP_EXCEPT       
              326  LOAD_CONST               None
              328  STORE_FAST               'e'
              330  DELETE_FAST              'e'
              332  JUMP_BACK           158  'to 158'
            334_0  COME_FROM_FINALLY   198  '198'
              334  LOAD_CONST               None
              336  STORE_FAST               'e'
              338  DELETE_FAST              'e'
              340  <48>             
              342  <48>             
              344  JUMP_BACK           158  'to 158'

 L. 190       346  LOAD_GLOBAL              isinstance
              348  LOAD_FAST                'obj'
              350  LOAD_GLOBAL              types
              352  LOAD_ATTR                ModuleType
              354  CALL_FUNCTION_2       2  ''
          356_358  POP_JUMP_IF_FALSE   370  'to 370'

 L. 191       360  LOAD_FAST                'self'
              362  LOAD_METHOD              loadTestsFromModule
              364  LOAD_FAST                'obj'
              366  CALL_METHOD_1         1  ''
              368  RETURN_VALUE     
            370_0  COME_FROM           356  '356'

 L. 192       370  LOAD_GLOBAL              isinstance
              372  LOAD_FAST                'obj'
              374  LOAD_GLOBAL              type
              376  CALL_FUNCTION_2       2  ''
          378_380  POP_JUMP_IF_FALSE   406  'to 406'
              382  LOAD_GLOBAL              issubclass
              384  LOAD_FAST                'obj'
              386  LOAD_GLOBAL              case
              388  LOAD_ATTR                TestCase
              390  CALL_FUNCTION_2       2  ''
          392_394  POP_JUMP_IF_FALSE   406  'to 406'

 L. 193       396  LOAD_FAST                'self'
              398  LOAD_METHOD              loadTestsFromTestCase
              400  LOAD_FAST                'obj'
              402  CALL_METHOD_1         1  ''
              404  RETURN_VALUE     
            406_0  COME_FROM           392  '392'
            406_1  COME_FROM           378  '378'

 L. 194       406  LOAD_GLOBAL              isinstance
              408  LOAD_FAST                'obj'
              410  LOAD_GLOBAL              types
              412  LOAD_ATTR                FunctionType
              414  CALL_FUNCTION_2       2  ''
          416_418  POP_JUMP_IF_FALSE   496  'to 496'

 L. 195       420  LOAD_GLOBAL              isinstance
              422  LOAD_FAST                'parent'
              424  LOAD_GLOBAL              type
              426  CALL_FUNCTION_2       2  ''

 L. 194   428_430  POP_JUMP_IF_FALSE   496  'to 496'

 L. 196       432  LOAD_GLOBAL              issubclass
              434  LOAD_FAST                'parent'
              436  LOAD_GLOBAL              case
              438  LOAD_ATTR                TestCase
              440  CALL_FUNCTION_2       2  ''

 L. 194   442_444  POP_JUMP_IF_FALSE   496  'to 496'

 L. 197       446  LOAD_FAST                'parts'
              448  LOAD_CONST               -1
              450  BINARY_SUBSCR    
              452  STORE_FAST               'name'

 L. 198       454  LOAD_FAST                'parent'
              456  LOAD_FAST                'name'
              458  CALL_FUNCTION_1       1  ''
              460  STORE_FAST               'inst'

 L. 200       462  LOAD_GLOBAL              isinstance
              464  LOAD_GLOBAL              getattr
              466  LOAD_FAST                'inst'
              468  LOAD_FAST                'name'
              470  CALL_FUNCTION_2       2  ''
              472  LOAD_GLOBAL              types
              474  LOAD_ATTR                FunctionType
              476  CALL_FUNCTION_2       2  ''
          478_480  POP_JUMP_IF_TRUE    514  'to 514'

 L. 201       482  LOAD_FAST                'self'
              484  LOAD_METHOD              suiteClass
              486  LOAD_FAST                'inst'
              488  BUILD_LIST_1          1 
              490  CALL_METHOD_1         1  ''
              492  RETURN_VALUE     
              494  JUMP_FORWARD        514  'to 514'
            496_0  COME_FROM           442  '442'
            496_1  COME_FROM           428  '428'
            496_2  COME_FROM           416  '416'

 L. 202       496  LOAD_GLOBAL              isinstance
              498  LOAD_FAST                'obj'
              500  LOAD_GLOBAL              suite
              502  LOAD_ATTR                TestSuite
              504  CALL_FUNCTION_2       2  ''
          506_508  POP_JUMP_IF_FALSE   514  'to 514'

 L. 203       510  LOAD_FAST                'obj'
              512  RETURN_VALUE     
            514_0  COME_FROM           506  '506'
            514_1  COME_FROM           494  '494'
            514_2  COME_FROM           478  '478'

 L. 204       514  LOAD_GLOBAL              callable
              516  LOAD_FAST                'obj'
              518  CALL_FUNCTION_1       1  ''
          520_522  POP_JUMP_IF_FALSE   592  'to 592'

 L. 205       524  LOAD_FAST                'obj'
              526  CALL_FUNCTION_0       0  ''
              528  STORE_FAST               'test'

 L. 206       530  LOAD_GLOBAL              isinstance
              532  LOAD_FAST                'test'
              534  LOAD_GLOBAL              suite
              536  LOAD_ATTR                TestSuite
              538  CALL_FUNCTION_2       2  ''
          540_542  POP_JUMP_IF_FALSE   548  'to 548'

 L. 207       544  LOAD_FAST                'test'
              546  RETURN_VALUE     
            548_0  COME_FROM           540  '540'

 L. 208       548  LOAD_GLOBAL              isinstance
              550  LOAD_FAST                'test'
              552  LOAD_GLOBAL              case
              554  LOAD_ATTR                TestCase
              556  CALL_FUNCTION_2       2  ''
          558_560  POP_JUMP_IF_FALSE   574  'to 574'

 L. 209       562  LOAD_FAST                'self'
              564  LOAD_METHOD              suiteClass
              566  LOAD_FAST                'test'
              568  BUILD_LIST_1          1 
              570  CALL_METHOD_1         1  ''
              572  RETURN_VALUE     
            574_0  COME_FROM           558  '558'

 L. 211       574  LOAD_GLOBAL              TypeError
              576  LOAD_STR                 'calling %s returned %s, not a test'

 L. 212       578  LOAD_FAST                'obj'
              580  LOAD_FAST                'test'
              582  BUILD_TUPLE_2         2 

 L. 211       584  BINARY_MODULO    
              586  CALL_FUNCTION_1       1  ''
              588  RAISE_VARARGS_1       1  'exception instance'
              590  JUMP_FORWARD        604  'to 604'
            592_0  COME_FROM           520  '520'

 L. 214       592  LOAD_GLOBAL              TypeError
              594  LOAD_STR                 "don't know how to make test from: %s"
              596  LOAD_FAST                'obj'
              598  BINARY_MODULO    
              600  CALL_FUNCTION_1       1  ''
              602  RAISE_VARARGS_1       1  'exception instance'
            604_0  COME_FROM           590  '590'

Parse error at or near `<117>' instruction at offset 22

    def loadTestsFromNames(self, names, module=None):
        """Return a suite of all test cases found using the given sequence
        of string specifiers. See 'loadTestsFromName()'.
        """
        suites = [self.loadTestsFromName(name, module) for name in names]
        return self.suiteClass(suites)

    def getTestCaseNames(self, testCaseClass):
        """Return a sorted sequence of method names found within testCaseClass
        """

        def shouldIncludeMethod--- This code section failed: ---

 L. 227         0  LOAD_FAST                'attrname'
                2  LOAD_METHOD              startswith
                4  LOAD_DEREF               'self'
                6  LOAD_ATTR                testMethodPrefix
                8  CALL_METHOD_1         1  ''
               10  POP_JUMP_IF_TRUE     16  'to 16'

 L. 228        12  LOAD_CONST               False
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L. 229        16  LOAD_GLOBAL              getattr
               18  LOAD_DEREF               'testCaseClass'
               20  LOAD_FAST                'attrname'
               22  CALL_FUNCTION_2       2  ''
               24  STORE_FAST               'testFunc'

 L. 230        26  LOAD_GLOBAL              callable
               28  LOAD_FAST                'testFunc'
               30  CALL_FUNCTION_1       1  ''
               32  POP_JUMP_IF_TRUE     38  'to 38'

 L. 231        34  LOAD_CONST               False
               36  RETURN_VALUE     
             38_0  COME_FROM            32  '32'

 L. 232        38  LOAD_STR                 '%s.%s.%s'

 L. 233        40  LOAD_DEREF               'testCaseClass'
               42  LOAD_ATTR                __module__
               44  LOAD_DEREF               'testCaseClass'
               46  LOAD_ATTR                __qualname__
               48  LOAD_FAST                'attrname'

 L. 232        50  BUILD_TUPLE_3         3 
               52  BINARY_MODULO    
               54  STORE_DEREF              'fullName'

 L. 235        56  LOAD_DEREF               'self'
               58  LOAD_ATTR                testNamePatterns
               60  LOAD_CONST               None
               62  <117>                 0  ''
               64  JUMP_IF_TRUE_OR_POP    88  'to 88'

 L. 236        66  LOAD_GLOBAL              any
               68  LOAD_CLOSURE             'fullName'
               70  BUILD_TUPLE_1         1 
               72  LOAD_GENEXPR             '<code_object <genexpr>>'
               74  LOAD_STR                 'TestLoader.getTestCaseNames.<locals>.shouldIncludeMethod.<locals>.<genexpr>'
               76  MAKE_FUNCTION_8          'closure'
               78  LOAD_DEREF               'self'
               80  LOAD_ATTR                testNamePatterns
               82  GET_ITER         
               84  CALL_FUNCTION_1       1  ''
               86  CALL_FUNCTION_1       1  ''
             88_0  COME_FROM            64  '64'

 L. 235        88  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 62

        testFnNames = list(filter(shouldIncludeMethod, dir(testCaseClass)))
        if self.sortTestMethodsUsing:
            testFnNames.sort(key=(functools.cmp_to_key(self.sortTestMethodsUsing)))
        return testFnNames

    def discover--- This code section failed: ---

 L. 270         0  LOAD_CONST               False
                2  STORE_FAST               'set_implicit_top'

 L. 271         4  LOAD_FAST                'top_level_dir'
                6  LOAD_CONST               None
                8  <117>                 0  ''
               10  POP_JUMP_IF_FALSE    30  'to 30'
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                _top_level_dir
               16  LOAD_CONST               None
               18  <117>                 1  ''
               20  POP_JUMP_IF_FALSE    30  'to 30'

 L. 273        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _top_level_dir
               26  STORE_FAST               'top_level_dir'
               28  JUMP_FORWARD         46  'to 46'
             30_0  COME_FROM            20  '20'
             30_1  COME_FROM            10  '10'

 L. 274        30  LOAD_FAST                'top_level_dir'
               32  LOAD_CONST               None
               34  <117>                 0  ''
               36  POP_JUMP_IF_FALSE    46  'to 46'

 L. 275        38  LOAD_CONST               True
               40  STORE_FAST               'set_implicit_top'

 L. 276        42  LOAD_FAST                'start_dir'
               44  STORE_FAST               'top_level_dir'
             46_0  COME_FROM            36  '36'
             46_1  COME_FROM            28  '28'

 L. 278        46  LOAD_GLOBAL              os
               48  LOAD_ATTR                path
               50  LOAD_METHOD              abspath
               52  LOAD_FAST                'top_level_dir'
               54  CALL_METHOD_1         1  ''
               56  STORE_FAST               'top_level_dir'

 L. 280        58  LOAD_FAST                'top_level_dir'
               60  LOAD_GLOBAL              sys
               62  LOAD_ATTR                path
               64  <118>                 1  ''
               66  POP_JUMP_IF_FALSE    82  'to 82'

 L. 285        68  LOAD_GLOBAL              sys
               70  LOAD_ATTR                path
               72  LOAD_METHOD              insert
               74  LOAD_CONST               0
               76  LOAD_FAST                'top_level_dir'
               78  CALL_METHOD_2         2  ''
               80  POP_TOP          
             82_0  COME_FROM            66  '66'

 L. 286        82  LOAD_FAST                'top_level_dir'
               84  LOAD_FAST                'self'
               86  STORE_ATTR               _top_level_dir

 L. 288        88  LOAD_CONST               False
               90  STORE_FAST               'is_not_importable'

 L. 289        92  LOAD_CONST               False
               94  STORE_FAST               'is_namespace'

 L. 290        96  BUILD_LIST_0          0 
               98  STORE_FAST               'tests'

 L. 291       100  LOAD_GLOBAL              os
              102  LOAD_ATTR                path
              104  LOAD_METHOD              isdir
              106  LOAD_GLOBAL              os
              108  LOAD_ATTR                path
              110  LOAD_METHOD              abspath
              112  LOAD_FAST                'start_dir'
              114  CALL_METHOD_1         1  ''
              116  CALL_METHOD_1         1  ''
              118  POP_JUMP_IF_FALSE   168  'to 168'

 L. 292       120  LOAD_GLOBAL              os
              122  LOAD_ATTR                path
              124  LOAD_METHOD              abspath
              126  LOAD_FAST                'start_dir'
              128  CALL_METHOD_1         1  ''
              130  STORE_FAST               'start_dir'

 L. 293       132  LOAD_FAST                'start_dir'
              134  LOAD_FAST                'top_level_dir'
              136  COMPARE_OP               !=
              138  POP_JUMP_IF_FALSE   164  'to 164'

 L. 294       140  LOAD_GLOBAL              os
              142  LOAD_ATTR                path
              144  LOAD_METHOD              isfile
              146  LOAD_GLOBAL              os
              148  LOAD_ATTR                path
              150  LOAD_METHOD              join
              152  LOAD_FAST                'start_dir'
              154  LOAD_STR                 '__init__.py'
              156  CALL_METHOD_2         2  ''
              158  CALL_METHOD_1         1  ''
              160  UNARY_NOT        
              162  STORE_FAST               'is_not_importable'
            164_0  COME_FROM           138  '138'
          164_166  JUMP_FORWARD        530  'to 530'
            168_0  COME_FROM           118  '118'

 L. 297       168  SETUP_FINALLY       182  'to 182'

 L. 298       170  LOAD_GLOBAL              __import__
              172  LOAD_FAST                'start_dir'
              174  CALL_FUNCTION_1       1  ''
              176  POP_TOP          
              178  POP_BLOCK        
              180  JUMP_FORWARD        206  'to 206'
            182_0  COME_FROM_FINALLY   168  '168'

 L. 299       182  DUP_TOP          
              184  LOAD_GLOBAL              ImportError
              186  <121>               204  ''
              188  POP_TOP          
              190  POP_TOP          
              192  POP_TOP          

 L. 300       194  LOAD_CONST               True
              196  STORE_FAST               'is_not_importable'
              198  POP_EXCEPT       
          200_202  JUMP_FORWARD        530  'to 530'
              204  <48>             
            206_0  COME_FROM           180  '180'

 L. 302       206  LOAD_GLOBAL              sys
              208  LOAD_ATTR                modules
              210  LOAD_FAST                'start_dir'
              212  BINARY_SUBSCR    
              214  STORE_FAST               'the_module'

 L. 303       216  LOAD_FAST                'start_dir'
              218  LOAD_METHOD              split
              220  LOAD_STR                 '.'
              222  CALL_METHOD_1         1  ''
              224  LOAD_CONST               0
              226  BINARY_SUBSCR    
              228  STORE_FAST               'top_part'

 L. 304       230  SETUP_FINALLY       258  'to 258'

 L. 305       232  LOAD_GLOBAL              os
              234  LOAD_ATTR                path
              236  LOAD_METHOD              abspath

 L. 306       238  LOAD_GLOBAL              os
              240  LOAD_ATTR                path
              242  LOAD_METHOD              dirname
              244  LOAD_FAST                'the_module'
              246  LOAD_ATTR                __file__
              248  CALL_METHOD_1         1  ''

 L. 305       250  CALL_METHOD_1         1  ''
              252  STORE_FAST               'start_dir'
              254  POP_BLOCK        
              256  JUMP_FORWARD        480  'to 480'
            258_0  COME_FROM_FINALLY   230  '230'

 L. 307       258  DUP_TOP          
              260  LOAD_GLOBAL              AttributeError
          262_264  <121>               478  ''
              266  POP_TOP          
              268  POP_TOP          
              270  POP_TOP          

 L. 309       272  SETUP_FINALLY       284  'to 284'

 L. 310       274  LOAD_FAST                'the_module'
              276  LOAD_ATTR                __spec__
              278  STORE_FAST               'spec'
              280  POP_BLOCK        
              282  JUMP_FORWARD        308  'to 308'
            284_0  COME_FROM_FINALLY   272  '272'

 L. 311       284  DUP_TOP          
              286  LOAD_GLOBAL              AttributeError
          288_290  <121>               306  ''
              292  POP_TOP          
              294  POP_TOP          
              296  POP_TOP          

 L. 312       298  LOAD_CONST               None
              300  STORE_FAST               'spec'
              302  POP_EXCEPT       
              304  JUMP_FORWARD        308  'to 308'
              306  <48>             
            308_0  COME_FROM           304  '304'
            308_1  COME_FROM           282  '282'

 L. 314       308  LOAD_FAST                'spec'
          310_312  POP_JUMP_IF_FALSE   432  'to 432'
              314  LOAD_FAST                'spec'
              316  LOAD_ATTR                loader
              318  LOAD_CONST               None
              320  <117>                 0  ''
          322_324  POP_JUMP_IF_FALSE   432  'to 432'

 L. 315       326  LOAD_FAST                'spec'
              328  LOAD_ATTR                submodule_search_locations
              330  LOAD_CONST               None
              332  <117>                 1  ''
          334_336  POP_JUMP_IF_FALSE   474  'to 474'

 L. 316       338  LOAD_CONST               True
              340  STORE_FAST               'is_namespace'

 L. 318       342  LOAD_FAST                'the_module'
              344  LOAD_ATTR                __path__
              346  GET_ITER         
              348  FOR_ITER            430  'to 430'
              350  STORE_FAST               'path'

 L. 319       352  LOAD_FAST                'set_implicit_top'
          354_356  POP_JUMP_IF_TRUE    374  'to 374'

 L. 320       358  LOAD_FAST                'path'
              360  LOAD_METHOD              startswith
              362  LOAD_FAST                'top_level_dir'
              364  CALL_METHOD_1         1  ''

 L. 319   366_368  POP_JUMP_IF_TRUE    374  'to 374'

 L. 321   370_372  JUMP_BACK           348  'to 348'
            374_0  COME_FROM           366  '366'
            374_1  COME_FROM           354  '354'

 L. 323       374  LOAD_FAST                'path'
              376  LOAD_METHOD              split
              378  LOAD_FAST                'the_module'
              380  LOAD_ATTR                __name__
              382  LOAD_METHOD              replace

 L. 324       384  LOAD_STR                 '.'
              386  LOAD_GLOBAL              os
              388  LOAD_ATTR                path
              390  LOAD_ATTR                sep

 L. 323       392  CALL_METHOD_2         2  ''
              394  CALL_METHOD_1         1  ''

 L. 324       396  LOAD_CONST               0

 L. 323       398  BINARY_SUBSCR    

 L. 322       400  LOAD_FAST                'self'
              402  STORE_ATTR               _top_level_dir

 L. 325       404  LOAD_FAST                'tests'
              406  LOAD_METHOD              extend
              408  LOAD_FAST                'self'
              410  LOAD_ATTR                _find_tests
              412  LOAD_FAST                'path'

 L. 326       414  LOAD_FAST                'pattern'

 L. 327       416  LOAD_CONST               True

 L. 325       418  LOAD_CONST               ('namespace',)
              420  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              422  CALL_METHOD_1         1  ''
              424  POP_TOP          
          426_428  JUMP_BACK           348  'to 348'
              430  JUMP_FORWARD        474  'to 474'
            432_0  COME_FROM           322  '322'
            432_1  COME_FROM           310  '310'

 L. 328       432  LOAD_FAST                'the_module'
              434  LOAD_ATTR                __name__
              436  LOAD_GLOBAL              sys
              438  LOAD_ATTR                builtin_module_names
              440  <118>                 0  ''
          442_444  POP_JUMP_IF_FALSE   458  'to 458'

 L. 330       446  LOAD_GLOBAL              TypeError
              448  LOAD_STR                 'Can not use builtin modules as dotted module names'
              450  CALL_FUNCTION_1       1  ''

 L. 331       452  LOAD_CONST               None

 L. 330       454  RAISE_VARARGS_2       2  'exception instance with __cause__'
              456  JUMP_FORWARD        474  'to 474'
            458_0  COME_FROM           442  '442'

 L. 333       458  LOAD_GLOBAL              TypeError

 L. 334       460  LOAD_STR                 "don't know how to discover from {!r}"
              462  LOAD_METHOD              format

 L. 335       464  LOAD_FAST                'the_module'

 L. 334       466  CALL_METHOD_1         1  ''

 L. 333       468  CALL_FUNCTION_1       1  ''

 L. 335       470  LOAD_CONST               None

 L. 333       472  RAISE_VARARGS_2       2  'exception instance with __cause__'
            474_0  COME_FROM           456  '456'
            474_1  COME_FROM           430  '430'
            474_2  COME_FROM           334  '334'
              474  POP_EXCEPT       
              476  JUMP_FORWARD        480  'to 480'
              478  <48>             
            480_0  COME_FROM           476  '476'
            480_1  COME_FROM           256  '256'

 L. 337       480  LOAD_FAST                'set_implicit_top'
          482_484  POP_JUMP_IF_FALSE   530  'to 530'

 L. 338       486  LOAD_FAST                'is_namespace'
          488_490  POP_JUMP_IF_TRUE    518  'to 518'

 L. 340       492  LOAD_FAST                'self'
              494  LOAD_METHOD              _get_directory_containing_module
              496  LOAD_FAST                'top_part'
              498  CALL_METHOD_1         1  ''

 L. 339       500  LOAD_FAST                'self'
              502  STORE_ATTR               _top_level_dir

 L. 341       504  LOAD_GLOBAL              sys
              506  LOAD_ATTR                path
              508  LOAD_METHOD              remove
              510  LOAD_FAST                'top_level_dir'
              512  CALL_METHOD_1         1  ''
              514  POP_TOP          
              516  JUMP_FORWARD        530  'to 530'
            518_0  COME_FROM           488  '488'

 L. 343       518  LOAD_GLOBAL              sys
              520  LOAD_ATTR                path
              522  LOAD_METHOD              remove
              524  LOAD_FAST                'top_level_dir'
              526  CALL_METHOD_1         1  ''
              528  POP_TOP          
            530_0  COME_FROM           516  '516'
            530_1  COME_FROM           482  '482'
            530_2  COME_FROM           200  '200'
            530_3  COME_FROM           164  '164'

 L. 345       530  LOAD_FAST                'is_not_importable'
          532_534  POP_JUMP_IF_FALSE   548  'to 548'

 L. 346       536  LOAD_GLOBAL              ImportError
              538  LOAD_STR                 'Start directory is not importable: %r'
              540  LOAD_FAST                'start_dir'
              542  BINARY_MODULO    
              544  CALL_FUNCTION_1       1  ''
              546  RAISE_VARARGS_1       1  'exception instance'
            548_0  COME_FROM           532  '532'

 L. 348       548  LOAD_FAST                'is_namespace'
          550_552  POP_JUMP_IF_TRUE    570  'to 570'

 L. 349       554  LOAD_GLOBAL              list
              556  LOAD_FAST                'self'
              558  LOAD_METHOD              _find_tests
              560  LOAD_FAST                'start_dir'
              562  LOAD_FAST                'pattern'
              564  CALL_METHOD_2         2  ''
              566  CALL_FUNCTION_1       1  ''
              568  STORE_FAST               'tests'
            570_0  COME_FROM           550  '550'

 L. 350       570  LOAD_FAST                'self'
              572  LOAD_METHOD              suiteClass
              574  LOAD_FAST                'tests'
              576  CALL_METHOD_1         1  ''
              578  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 8

    def _get_directory_containing_module(self, module_name):
        module = sys.modules[module_name]
        full_path = os.path.abspath(module.__file__)
        if os.path.basename(full_path).lower().startswith('__init__.py'):
            return os.path.dirname(os.path.dirname(full_path))
        return os.path.dirname(full_path)

    def _get_name_from_path--- This code section failed: ---

 L. 365         0  LOAD_FAST                'path'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _top_level_dir
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 366        10  LOAD_STR                 '.'
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 367        14  LOAD_GLOBAL              _jython_aware_splitext
               16  LOAD_GLOBAL              os
               18  LOAD_ATTR                path
               20  LOAD_METHOD              normpath
               22  LOAD_FAST                'path'
               24  CALL_METHOD_1         1  ''
               26  CALL_FUNCTION_1       1  ''
               28  STORE_FAST               'path'

 L. 369        30  LOAD_GLOBAL              os
               32  LOAD_ATTR                path
               34  LOAD_METHOD              relpath
               36  LOAD_FAST                'path'
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                _top_level_dir
               42  CALL_METHOD_2         2  ''
               44  STORE_FAST               '_relpath'

 L. 370        46  LOAD_GLOBAL              os
               48  LOAD_ATTR                path
               50  LOAD_METHOD              isabs
               52  LOAD_FAST                '_relpath'
               54  CALL_METHOD_1         1  ''
               56  POP_JUMP_IF_FALSE    66  'to 66'
               58  <74>             
               60  LOAD_STR                 'Path must be within the project'
               62  CALL_FUNCTION_1       1  ''
               64  RAISE_VARARGS_1       1  'exception instance'
             66_0  COME_FROM            56  '56'

 L. 371        66  LOAD_FAST                '_relpath'
               68  LOAD_METHOD              startswith
               70  LOAD_STR                 '..'
               72  CALL_METHOD_1         1  ''
               74  POP_JUMP_IF_FALSE    84  'to 84'
               76  <74>             
               78  LOAD_STR                 'Path must be within the project'
               80  CALL_FUNCTION_1       1  ''
               82  RAISE_VARARGS_1       1  'exception instance'
             84_0  COME_FROM            74  '74'

 L. 373        84  LOAD_FAST                '_relpath'
               86  LOAD_METHOD              replace
               88  LOAD_GLOBAL              os
               90  LOAD_ATTR                path
               92  LOAD_ATTR                sep
               94  LOAD_STR                 '.'
               96  CALL_METHOD_2         2  ''
               98  STORE_FAST               'name'

 L. 374       100  LOAD_FAST                'name'
              102  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 58

    def _get_module_from_name(self, name):
        __import__(name)
        return sys.modules[name]

    def _match_path(self, path, full_path, pattern):
        return fnmatch(path, pattern)

    def _find_tests--- This code section failed: ---

 L. 387         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _get_name_from_path
                4  LOAD_FAST                'start_dir'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'name'

 L. 390        10  LOAD_FAST                'name'
               12  LOAD_STR                 '.'
               14  COMPARE_OP               !=
               16  POP_JUMP_IF_FALSE    68  'to 68'
               18  LOAD_FAST                'name'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                _loading_packages
               24  <118>                 1  ''
               26  POP_JUMP_IF_FALSE    68  'to 68'

 L. 393        28  LOAD_FAST                'self'
               30  LOAD_METHOD              _find_test_path

 L. 394        32  LOAD_FAST                'start_dir'
               34  LOAD_FAST                'pattern'
               36  LOAD_FAST                'namespace'

 L. 393        38  CALL_METHOD_3         3  ''
               40  UNPACK_SEQUENCE_2     2 
               42  STORE_FAST               'tests'
               44  STORE_FAST               'should_recurse'

 L. 395        46  LOAD_FAST                'tests'
               48  LOAD_CONST               None
               50  <117>                 1  ''
               52  POP_JUMP_IF_FALSE    60  'to 60'

 L. 396        54  LOAD_FAST                'tests'
               56  YIELD_VALUE      
               58  POP_TOP          
             60_0  COME_FROM            52  '52'

 L. 397        60  LOAD_FAST                'should_recurse'
               62  POP_JUMP_IF_TRUE     68  'to 68'

 L. 400        64  LOAD_CONST               None
               66  RETURN_VALUE     
             68_0  COME_FROM            62  '62'
             68_1  COME_FROM            26  '26'
             68_2  COME_FROM            16  '16'

 L. 402        68  LOAD_GLOBAL              sorted
               70  LOAD_GLOBAL              os
               72  LOAD_METHOD              listdir
               74  LOAD_FAST                'start_dir'
               76  CALL_METHOD_1         1  ''
               78  CALL_FUNCTION_1       1  ''
               80  STORE_FAST               'paths'

 L. 403        82  LOAD_FAST                'paths'
               84  GET_ITER         
             86_0  COME_FROM           138  '138'
               86  FOR_ITER            216  'to 216'
               88  STORE_FAST               'path'

 L. 404        90  LOAD_GLOBAL              os
               92  LOAD_ATTR                path
               94  LOAD_METHOD              join
               96  LOAD_FAST                'start_dir'
               98  LOAD_FAST                'path'
              100  CALL_METHOD_2         2  ''
              102  STORE_FAST               'full_path'

 L. 405       104  LOAD_FAST                'self'
              106  LOAD_METHOD              _find_test_path

 L. 406       108  LOAD_FAST                'full_path'
              110  LOAD_FAST                'pattern'
              112  LOAD_FAST                'namespace'

 L. 405       114  CALL_METHOD_3         3  ''
              116  UNPACK_SEQUENCE_2     2 
              118  STORE_FAST               'tests'
              120  STORE_FAST               'should_recurse'

 L. 407       122  LOAD_FAST                'tests'
              124  LOAD_CONST               None
              126  <117>                 1  ''
              128  POP_JUMP_IF_FALSE   136  'to 136'

 L. 408       130  LOAD_FAST                'tests'
              132  YIELD_VALUE      
              134  POP_TOP          
            136_0  COME_FROM           128  '128'

 L. 409       136  LOAD_FAST                'should_recurse'
              138  POP_JUMP_IF_FALSE    86  'to 86'

 L. 411       140  LOAD_FAST                'self'
              142  LOAD_METHOD              _get_name_from_path
              144  LOAD_FAST                'full_path'
              146  CALL_METHOD_1         1  ''
              148  STORE_FAST               'name'

 L. 412       150  LOAD_FAST                'self'
              152  LOAD_ATTR                _loading_packages
              154  LOAD_METHOD              add
              156  LOAD_FAST                'name'
              158  CALL_METHOD_1         1  ''
              160  POP_TOP          

 L. 413       162  SETUP_FINALLY       200  'to 200'

 L. 414       164  LOAD_FAST                'self'
              166  LOAD_METHOD              _find_tests
              168  LOAD_FAST                'full_path'
              170  LOAD_FAST                'pattern'
              172  LOAD_FAST                'namespace'
              174  CALL_METHOD_3         3  ''
              176  GET_YIELD_FROM_ITER
              178  LOAD_CONST               None
              180  YIELD_FROM       
              182  POP_TOP          
              184  POP_BLOCK        

 L. 416       186  LOAD_FAST                'self'
              188  LOAD_ATTR                _loading_packages
              190  LOAD_METHOD              discard
              192  LOAD_FAST                'name'
              194  CALL_METHOD_1         1  ''
              196  POP_TOP          
              198  JUMP_BACK            86  'to 86'
            200_0  COME_FROM_FINALLY   162  '162'
              200  LOAD_FAST                'self'
              202  LOAD_ATTR                _loading_packages
              204  LOAD_METHOD              discard
              206  LOAD_FAST                'name'
              208  CALL_METHOD_1         1  ''
              210  POP_TOP          
              212  <48>             
              214  JUMP_BACK            86  'to 86'

Parse error at or near `<118>' instruction at offset 24

    def _find_test_path--- This code section failed: ---

 L. 426         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              basename
                6  LOAD_FAST                'full_path'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'basename'

 L. 427        12  LOAD_GLOBAL              os
               14  LOAD_ATTR                path
               16  LOAD_METHOD              isfile
               18  LOAD_FAST                'full_path'
               20  CALL_METHOD_1         1  ''
            22_24  POP_JUMP_IF_FALSE   340  'to 340'

 L. 428        26  LOAD_GLOBAL              VALID_MODULE_NAME
               28  LOAD_METHOD              match
               30  LOAD_FAST                'basename'
               32  CALL_METHOD_1         1  ''
               34  POP_JUMP_IF_TRUE     40  'to 40'

 L. 430        36  LOAD_CONST               (None, False)
               38  RETURN_VALUE     
             40_0  COME_FROM            34  '34'

 L. 431        40  LOAD_FAST                'self'
               42  LOAD_METHOD              _match_path
               44  LOAD_FAST                'basename'
               46  LOAD_FAST                'full_path'
               48  LOAD_FAST                'pattern'
               50  CALL_METHOD_3         3  ''
               52  POP_JUMP_IF_TRUE     58  'to 58'

 L. 432        54  LOAD_CONST               (None, False)
               56  RETURN_VALUE     
             58_0  COME_FROM            52  '52'

 L. 434        58  LOAD_FAST                'self'
               60  LOAD_METHOD              _get_name_from_path
               62  LOAD_FAST                'full_path'
               64  CALL_METHOD_1         1  ''
               66  STORE_FAST               'name'

 L. 435        68  SETUP_FINALLY        84  'to 84'

 L. 436        70  LOAD_FAST                'self'
               72  LOAD_METHOD              _get_module_from_name
               74  LOAD_FAST                'name'
               76  CALL_METHOD_1         1  ''
               78  STORE_FAST               'module'
               80  POP_BLOCK        
               82  JUMP_FORWARD        186  'to 186'
             84_0  COME_FROM_FINALLY    68  '68'

 L. 437        84  DUP_TOP          
               86  LOAD_GLOBAL              case
               88  LOAD_ATTR                SkipTest
               90  <121>               138  ''
               92  POP_TOP          
               94  STORE_FAST               'e'
               96  POP_TOP          
               98  SETUP_FINALLY       130  'to 130'

 L. 438       100  LOAD_GLOBAL              _make_skipped_test
              102  LOAD_FAST                'name'
              104  LOAD_FAST                'e'
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                suiteClass
              110  CALL_FUNCTION_3       3  ''
              112  LOAD_CONST               False
              114  BUILD_TUPLE_2         2 
              116  POP_BLOCK        
              118  ROT_FOUR         
              120  POP_EXCEPT       
              122  LOAD_CONST               None
              124  STORE_FAST               'e'
              126  DELETE_FAST              'e'
              128  RETURN_VALUE     
            130_0  COME_FROM_FINALLY    98  '98'
              130  LOAD_CONST               None
              132  STORE_FAST               'e'
              134  DELETE_FAST              'e'
              136  <48>             

 L. 439       138  POP_TOP          
              140  POP_TOP          
              142  POP_TOP          

 L. 441       144  LOAD_GLOBAL              _make_failed_import_test
              146  LOAD_FAST                'name'
              148  LOAD_FAST                'self'
              150  LOAD_ATTR                suiteClass
              152  CALL_FUNCTION_2       2  ''

 L. 440       154  UNPACK_SEQUENCE_2     2 
              156  STORE_FAST               'error_case'
              158  STORE_FAST               'error_message'

 L. 442       160  LOAD_FAST                'self'
              162  LOAD_ATTR                errors
              164  LOAD_METHOD              append
              166  LOAD_FAST                'error_message'
              168  CALL_METHOD_1         1  ''
              170  POP_TOP          

 L. 443       172  LOAD_FAST                'error_case'
              174  LOAD_CONST               False
              176  BUILD_TUPLE_2         2 
              178  ROT_FOUR         
              180  POP_EXCEPT       
              182  RETURN_VALUE     
              184  <48>             
            186_0  COME_FROM            82  '82'

 L. 445       186  LOAD_GLOBAL              os
              188  LOAD_ATTR                path
              190  LOAD_METHOD              abspath

 L. 446       192  LOAD_GLOBAL              getattr
              194  LOAD_FAST                'module'
              196  LOAD_STR                 '__file__'
              198  LOAD_FAST                'full_path'
              200  CALL_FUNCTION_3       3  ''

 L. 445       202  CALL_METHOD_1         1  ''
              204  STORE_FAST               'mod_file'

 L. 447       206  LOAD_GLOBAL              _jython_aware_splitext

 L. 448       208  LOAD_GLOBAL              os
              210  LOAD_ATTR                path
              212  LOAD_METHOD              realpath
              214  LOAD_FAST                'mod_file'
              216  CALL_METHOD_1         1  ''

 L. 447       218  CALL_FUNCTION_1       1  ''
              220  STORE_FAST               'realpath'

 L. 449       222  LOAD_GLOBAL              _jython_aware_splitext

 L. 450       224  LOAD_GLOBAL              os
              226  LOAD_ATTR                path
              228  LOAD_METHOD              realpath
              230  LOAD_FAST                'full_path'
              232  CALL_METHOD_1         1  ''

 L. 449       234  CALL_FUNCTION_1       1  ''
              236  STORE_FAST               'fullpath_noext'

 L. 451       238  LOAD_FAST                'realpath'
              240  LOAD_METHOD              lower
              242  CALL_METHOD_0         0  ''
              244  LOAD_FAST                'fullpath_noext'
              246  LOAD_METHOD              lower
              248  CALL_METHOD_0         0  ''
              250  COMPARE_OP               !=
          252_254  POP_JUMP_IF_FALSE   318  'to 318'

 L. 452       256  LOAD_GLOBAL              os
              258  LOAD_ATTR                path
              260  LOAD_METHOD              dirname
              262  LOAD_FAST                'realpath'
              264  CALL_METHOD_1         1  ''
              266  STORE_FAST               'module_dir'

 L. 453       268  LOAD_GLOBAL              _jython_aware_splitext

 L. 454       270  LOAD_GLOBAL              os
              272  LOAD_ATTR                path
              274  LOAD_METHOD              basename
              276  LOAD_FAST                'full_path'
              278  CALL_METHOD_1         1  ''

 L. 453       280  CALL_FUNCTION_1       1  ''
              282  STORE_FAST               'mod_name'

 L. 455       284  LOAD_GLOBAL              os
              286  LOAD_ATTR                path
              288  LOAD_METHOD              dirname
              290  LOAD_FAST                'full_path'
              292  CALL_METHOD_1         1  ''
              294  STORE_FAST               'expected_dir'

 L. 456       296  LOAD_STR                 '%r module incorrectly imported from %r. Expected %r. Is this module globally installed?'
              298  STORE_FAST               'msg'

 L. 458       300  LOAD_GLOBAL              ImportError

 L. 459       302  LOAD_FAST                'msg'
              304  LOAD_FAST                'mod_name'
              306  LOAD_FAST                'module_dir'
              308  LOAD_FAST                'expected_dir'
              310  BUILD_TUPLE_3         3 
              312  BINARY_MODULO    

 L. 458       314  CALL_FUNCTION_1       1  ''
              316  RAISE_VARARGS_1       1  'exception instance'
            318_0  COME_FROM           252  '252'

 L. 460       318  LOAD_FAST                'self'
              320  LOAD_ATTR                loadTestsFromModule
              322  LOAD_FAST                'module'
              324  LOAD_FAST                'pattern'
              326  LOAD_CONST               ('pattern',)
              328  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              330  LOAD_CONST               False
              332  BUILD_TUPLE_2         2 
              334  RETURN_VALUE     
          336_338  JUMP_FORWARD        640  'to 640'
            340_0  COME_FROM            22  '22'

 L. 461       340  LOAD_GLOBAL              os
              342  LOAD_ATTR                path
              344  LOAD_METHOD              isdir
              346  LOAD_FAST                'full_path'
              348  CALL_METHOD_1         1  ''
          350_352  POP_JUMP_IF_FALSE   636  'to 636'

 L. 462       354  LOAD_FAST                'namespace'
          356_358  POP_JUMP_IF_TRUE    388  'to 388'

 L. 463       360  LOAD_GLOBAL              os
              362  LOAD_ATTR                path
              364  LOAD_METHOD              isfile
              366  LOAD_GLOBAL              os
              368  LOAD_ATTR                path
              370  LOAD_METHOD              join
              372  LOAD_FAST                'full_path'
              374  LOAD_STR                 '__init__.py'
              376  CALL_METHOD_2         2  ''
              378  CALL_METHOD_1         1  ''

 L. 462   380_382  POP_JUMP_IF_TRUE    388  'to 388'

 L. 464       384  LOAD_CONST               (None, False)
              386  RETURN_VALUE     
            388_0  COME_FROM           380  '380'
            388_1  COME_FROM           356  '356'

 L. 466       388  LOAD_CONST               None
              390  STORE_FAST               'load_tests'

 L. 467       392  LOAD_CONST               None
              394  STORE_FAST               'tests'

 L. 468       396  LOAD_FAST                'self'
              398  LOAD_METHOD              _get_name_from_path
              400  LOAD_FAST                'full_path'
              402  CALL_METHOD_1         1  ''
              404  STORE_FAST               'name'

 L. 469       406  SETUP_FINALLY       422  'to 422'

 L. 470       408  LOAD_FAST                'self'
              410  LOAD_METHOD              _get_module_from_name
              412  LOAD_FAST                'name'
              414  CALL_METHOD_1         1  ''
              416  STORE_FAST               'package'
              418  POP_BLOCK        
              420  JUMP_FORWARD        526  'to 526'
            422_0  COME_FROM_FINALLY   406  '406'

 L. 471       422  DUP_TOP          
              424  LOAD_GLOBAL              case
              426  LOAD_ATTR                SkipTest
          428_430  <121>               478  ''
              432  POP_TOP          
              434  STORE_FAST               'e'
              436  POP_TOP          
              438  SETUP_FINALLY       470  'to 470'

 L. 472       440  LOAD_GLOBAL              _make_skipped_test
              442  LOAD_FAST                'name'
              444  LOAD_FAST                'e'
              446  LOAD_FAST                'self'
              448  LOAD_ATTR                suiteClass
              450  CALL_FUNCTION_3       3  ''
              452  LOAD_CONST               False
              454  BUILD_TUPLE_2         2 
              456  POP_BLOCK        
              458  ROT_FOUR         
              460  POP_EXCEPT       
              462  LOAD_CONST               None
              464  STORE_FAST               'e'
              466  DELETE_FAST              'e'
              468  RETURN_VALUE     
            470_0  COME_FROM_FINALLY   438  '438'
              470  LOAD_CONST               None
              472  STORE_FAST               'e'
              474  DELETE_FAST              'e'
              476  <48>             

 L. 473       478  POP_TOP          
              480  POP_TOP          
              482  POP_TOP          

 L. 475       484  LOAD_GLOBAL              _make_failed_import_test
              486  LOAD_FAST                'name'
              488  LOAD_FAST                'self'
              490  LOAD_ATTR                suiteClass
              492  CALL_FUNCTION_2       2  ''

 L. 474       494  UNPACK_SEQUENCE_2     2 
              496  STORE_FAST               'error_case'
              498  STORE_FAST               'error_message'

 L. 476       500  LOAD_FAST                'self'
              502  LOAD_ATTR                errors
              504  LOAD_METHOD              append
              506  LOAD_FAST                'error_message'
              508  CALL_METHOD_1         1  ''
              510  POP_TOP          

 L. 477       512  LOAD_FAST                'error_case'
              514  LOAD_CONST               False
              516  BUILD_TUPLE_2         2 
              518  ROT_FOUR         
              520  POP_EXCEPT       
              522  RETURN_VALUE     
              524  <48>             
            526_0  COME_FROM           420  '420'

 L. 479       526  LOAD_GLOBAL              getattr
              528  LOAD_FAST                'package'
              530  LOAD_STR                 'load_tests'
              532  LOAD_CONST               None
              534  CALL_FUNCTION_3       3  ''
              536  STORE_FAST               'load_tests'

 L. 481       538  LOAD_FAST                'self'
              540  LOAD_ATTR                _loading_packages
              542  LOAD_METHOD              add
              544  LOAD_FAST                'name'
              546  CALL_METHOD_1         1  ''
              548  POP_TOP          

 L. 482       550  SETUP_FINALLY       620  'to 620'

 L. 483       552  LOAD_FAST                'self'
              554  LOAD_ATTR                loadTestsFromModule
              556  LOAD_FAST                'package'
              558  LOAD_FAST                'pattern'
              560  LOAD_CONST               ('pattern',)
              562  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              564  STORE_FAST               'tests'

 L. 484       566  LOAD_FAST                'load_tests'
              568  LOAD_CONST               None
              570  <117>                 1  ''
          572_574  POP_JUMP_IF_FALSE   598  'to 598'

 L. 486       576  LOAD_FAST                'tests'
              578  LOAD_CONST               False
              580  BUILD_TUPLE_2         2 
              582  POP_BLOCK        

 L. 489       584  LOAD_FAST                'self'
              586  LOAD_ATTR                _loading_packages
              588  LOAD_METHOD              discard
              590  LOAD_FAST                'name'
              592  CALL_METHOD_1         1  ''
              594  POP_TOP          

 L. 486       596  RETURN_VALUE     
            598_0  COME_FROM           572  '572'

 L. 487       598  LOAD_FAST                'tests'
              600  LOAD_CONST               True
              602  BUILD_TUPLE_2         2 
              604  POP_BLOCK        

 L. 489       606  LOAD_FAST                'self'
              608  LOAD_ATTR                _loading_packages
              610  LOAD_METHOD              discard
              612  LOAD_FAST                'name'
              614  CALL_METHOD_1         1  ''
              616  POP_TOP          

 L. 487       618  RETURN_VALUE     
            620_0  COME_FROM_FINALLY   550  '550'

 L. 489       620  LOAD_FAST                'self'
              622  LOAD_ATTR                _loading_packages
              624  LOAD_METHOD              discard
              626  LOAD_FAST                'name'
              628  CALL_METHOD_1         1  ''
              630  POP_TOP          
              632  <48>             
              634  JUMP_FORWARD        640  'to 640'
            636_0  COME_FROM           350  '350'

 L. 491       636  LOAD_CONST               (None, False)
              638  RETURN_VALUE     
            640_0  COME_FROM           634  '634'
            640_1  COME_FROM           336  '336'

Parse error at or near `<121>' instruction at offset 90


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