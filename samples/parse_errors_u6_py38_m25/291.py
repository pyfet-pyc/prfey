# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
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
               16  COMPARE_OP               in
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
              212  COMPARE_OP               is-not
          214_216  POP_JUMP_IF_FALSE   310  'to 310'

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
              238  COMPARE_OP               exception-match
          240_242  POP_JUMP_IF_FALSE   308  'to 308'
              244  POP_TOP          
              246  STORE_FAST               'e'
              248  POP_TOP          
              250  SETUP_FINALLY       296  'to 296'

 L. 132       252  LOAD_GLOBAL              _make_failed_load_tests

 L. 133       254  LOAD_FAST                'module'
              256  LOAD_ATTR                __name__

 L. 133       258  LOAD_FAST                'e'

 L. 133       260  LOAD_FAST                'self'
              262  LOAD_ATTR                suiteClass

 L. 132       264  CALL_FUNCTION_3       3  ''
              266  UNPACK_SEQUENCE_2     2 
              268  STORE_FAST               'error_case'
              270  STORE_FAST               'error_message'

 L. 134       272  LOAD_FAST                'self'
              274  LOAD_ATTR                errors
              276  LOAD_METHOD              append
              278  LOAD_FAST                'error_message'
              280  CALL_METHOD_1         1  ''
              282  POP_TOP          

 L. 135       284  LOAD_FAST                'error_case'
              286  ROT_FOUR         
              288  POP_BLOCK        
              290  POP_EXCEPT       
              292  CALL_FINALLY        296  'to 296'
              294  RETURN_VALUE     
            296_0  COME_FROM           292  '292'
            296_1  COME_FROM_FINALLY   250  '250'
              296  LOAD_CONST               None
              298  STORE_FAST               'e'
              300  DELETE_FAST              'e'
              302  END_FINALLY      
              304  POP_EXCEPT       
              306  JUMP_FORWARD        310  'to 310'
            308_0  COME_FROM           240  '240'
              308  END_FINALLY      
            310_0  COME_FROM           306  '306'
            310_1  COME_FROM           214  '214'

 L. 136       310  LOAD_FAST                'tests'
              312  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 288

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
               22  COMPARE_OP               is
               24  POP_JUMP_IF_FALSE   152  'to 152'

 L. 150        26  LOAD_FAST                'parts'
               28  LOAD_CONST               None
               30  LOAD_CONST               None
               32  BUILD_SLICE_2         2 
               34  BINARY_SUBSCR    
               36  STORE_FAST               'parts_copy'

 L. 151        38  LOAD_FAST                'parts_copy'
               40  POP_JUMP_IF_FALSE   140  'to 140'

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
               64  JUMP_ABSOLUTE       140  'to 140'
               66  POP_BLOCK        
               68  JUMP_BACK            38  'to 38'
             70_0  COME_FROM_FINALLY    42  '42'

 L. 156        70  DUP_TOP          
               72  LOAD_GLOBAL              ImportError
               74  COMPARE_OP               exception-match
               76  POP_JUMP_IF_FALSE   136  'to 136'
               78  POP_TOP          
               80  POP_TOP          
               82  POP_TOP          

 L. 157        84  LOAD_FAST                'parts_copy'
               86  LOAD_METHOD              pop
               88  CALL_METHOD_0         0  ''
               90  STORE_FAST               'next_attribute'

 L. 159        92  LOAD_GLOBAL              _make_failed_import_test

 L. 160        94  LOAD_FAST                'next_attribute'

 L. 160        96  LOAD_FAST                'self'
               98  LOAD_ATTR                suiteClass

 L. 159       100  CALL_FUNCTION_2       2  ''
              102  UNPACK_SEQUENCE_2     2 
              104  STORE_FAST               'error_case'
              106  STORE_FAST               'error_message'

 L. 161       108  LOAD_FAST                'parts_copy'
              110  POP_JUMP_IF_TRUE    132  'to 132'

 L. 163       112  LOAD_FAST                'self'
              114  LOAD_ATTR                errors
              116  LOAD_METHOD              append
              118  LOAD_FAST                'error_message'
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          

 L. 164       124  LOAD_FAST                'error_case'
              126  ROT_FOUR         
              128  POP_EXCEPT       
              130  RETURN_VALUE     
            132_0  COME_FROM           110  '110'
              132  POP_EXCEPT       
              134  JUMP_BACK            38  'to 38'
            136_0  COME_FROM            76  '76'
              136  END_FINALLY      
              138  JUMP_BACK            38  'to 38'
            140_0  COME_FROM            40  '40'

 L. 165       140  LOAD_FAST                'parts'
              142  LOAD_CONST               1
              144  LOAD_CONST               None
              146  BUILD_SLICE_2         2 
              148  BINARY_SUBSCR    
              150  STORE_FAST               'parts'
            152_0  COME_FROM            24  '24'

 L. 166       152  LOAD_FAST                'module'
              154  STORE_FAST               'obj'

 L. 167       156  LOAD_FAST                'parts'
              158  GET_ITER         
              160  FOR_ITER            338  'to 338'
              162  STORE_FAST               'part'

 L. 168       164  SETUP_FINALLY       186  'to 186'

 L. 169       166  LOAD_FAST                'obj'
              168  LOAD_GLOBAL              getattr
              170  LOAD_FAST                'obj'
              172  LOAD_FAST                'part'
              174  CALL_FUNCTION_2       2  ''
              176  ROT_TWO          
              178  STORE_FAST               'parent'
              180  STORE_FAST               'obj'
              182  POP_BLOCK        
              184  JUMP_BACK           160  'to 160'
            186_0  COME_FROM_FINALLY   164  '164'

 L. 170       186  DUP_TOP          
              188  LOAD_GLOBAL              AttributeError
              190  COMPARE_OP               exception-match
          192_194  POP_JUMP_IF_FALSE   334  'to 334'
              196  POP_TOP          
              198  STORE_FAST               'e'
              200  POP_TOP          
              202  SETUP_FINALLY       322  'to 322'

 L. 172       204  LOAD_GLOBAL              getattr
              206  LOAD_FAST                'obj'
              208  LOAD_STR                 '__path__'
              210  LOAD_CONST               None
              212  CALL_FUNCTION_3       3  ''
              214  LOAD_CONST               None
              216  COMPARE_OP               is-not
          218_220  POP_JUMP_IF_FALSE   260  'to 260'

 L. 173       222  LOAD_FAST                'error_case'
              224  LOAD_CONST               None
              226  COMPARE_OP               is-not

 L. 172   228_230  POP_JUMP_IF_FALSE   260  'to 260'

 L. 179       232  LOAD_FAST                'self'
              234  LOAD_ATTR                errors
              236  LOAD_METHOD              append
              238  LOAD_FAST                'error_message'
              240  CALL_METHOD_1         1  ''
              242  POP_TOP          

 L. 180       244  LOAD_FAST                'error_case'
              246  ROT_FOUR         
              248  POP_BLOCK        
              250  POP_EXCEPT       
              252  CALL_FINALLY        322  'to 322'
              254  ROT_TWO          
              256  POP_TOP          
              258  RETURN_VALUE     
            260_0  COME_FROM           228  '228'
            260_1  COME_FROM           218  '218'

 L. 183       260  LOAD_GLOBAL              _make_failed_test

 L. 184       262  LOAD_FAST                'part'

 L. 184       264  LOAD_FAST                'e'

 L. 184       266  LOAD_FAST                'self'
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
              304  ROT_FOUR         
              306  POP_BLOCK        
              308  POP_EXCEPT       
              310  CALL_FINALLY        322  'to 322'
              312  ROT_TWO          
              314  POP_TOP          
              316  RETURN_VALUE     
              318  POP_BLOCK        
              320  BEGIN_FINALLY    
            322_0  COME_FROM           310  '310'
            322_1  COME_FROM           252  '252'
            322_2  COME_FROM_FINALLY   202  '202'
              322  LOAD_CONST               None
              324  STORE_FAST               'e'
              326  DELETE_FAST              'e'
              328  END_FINALLY      
              330  POP_EXCEPT       
              332  JUMP_BACK           160  'to 160'
            334_0  COME_FROM           192  '192'
              334  END_FINALLY      
              336  JUMP_BACK           160  'to 160'

 L. 190       338  LOAD_GLOBAL              isinstance
              340  LOAD_FAST                'obj'
              342  LOAD_GLOBAL              types
              344  LOAD_ATTR                ModuleType
              346  CALL_FUNCTION_2       2  ''
          348_350  POP_JUMP_IF_FALSE   362  'to 362'

 L. 191       352  LOAD_FAST                'self'
              354  LOAD_METHOD              loadTestsFromModule
              356  LOAD_FAST                'obj'
              358  CALL_METHOD_1         1  ''
              360  RETURN_VALUE     
            362_0  COME_FROM           348  '348'

 L. 192       362  LOAD_GLOBAL              isinstance
              364  LOAD_FAST                'obj'
              366  LOAD_GLOBAL              type
              368  CALL_FUNCTION_2       2  ''
          370_372  POP_JUMP_IF_FALSE   398  'to 398'
              374  LOAD_GLOBAL              issubclass
              376  LOAD_FAST                'obj'
              378  LOAD_GLOBAL              case
              380  LOAD_ATTR                TestCase
              382  CALL_FUNCTION_2       2  ''
          384_386  POP_JUMP_IF_FALSE   398  'to 398'

 L. 193       388  LOAD_FAST                'self'
              390  LOAD_METHOD              loadTestsFromTestCase
              392  LOAD_FAST                'obj'
              394  CALL_METHOD_1         1  ''
              396  RETURN_VALUE     
            398_0  COME_FROM           384  '384'
            398_1  COME_FROM           370  '370'

 L. 194       398  LOAD_GLOBAL              isinstance
              400  LOAD_FAST                'obj'
              402  LOAD_GLOBAL              types
              404  LOAD_ATTR                FunctionType
              406  CALL_FUNCTION_2       2  ''
          408_410  POP_JUMP_IF_FALSE   488  'to 488'

 L. 195       412  LOAD_GLOBAL              isinstance
              414  LOAD_FAST                'parent'
              416  LOAD_GLOBAL              type
              418  CALL_FUNCTION_2       2  ''

 L. 194   420_422  POP_JUMP_IF_FALSE   488  'to 488'

 L. 196       424  LOAD_GLOBAL              issubclass
              426  LOAD_FAST                'parent'
              428  LOAD_GLOBAL              case
              430  LOAD_ATTR                TestCase
              432  CALL_FUNCTION_2       2  ''

 L. 194   434_436  POP_JUMP_IF_FALSE   488  'to 488'

 L. 197       438  LOAD_FAST                'parts'
              440  LOAD_CONST               -1
              442  BINARY_SUBSCR    
              444  STORE_FAST               'name'

 L. 198       446  LOAD_FAST                'parent'
              448  LOAD_FAST                'name'
              450  CALL_FUNCTION_1       1  ''
              452  STORE_FAST               'inst'

 L. 200       454  LOAD_GLOBAL              isinstance
              456  LOAD_GLOBAL              getattr
              458  LOAD_FAST                'inst'
              460  LOAD_FAST                'name'
              462  CALL_FUNCTION_2       2  ''
              464  LOAD_GLOBAL              types
              466  LOAD_ATTR                FunctionType
              468  CALL_FUNCTION_2       2  ''
          470_472  POP_JUMP_IF_TRUE    506  'to 506'

 L. 201       474  LOAD_FAST                'self'
              476  LOAD_METHOD              suiteClass
              478  LOAD_FAST                'inst'
              480  BUILD_LIST_1          1 
              482  CALL_METHOD_1         1  ''
              484  RETURN_VALUE     
              486  JUMP_FORWARD        506  'to 506'
            488_0  COME_FROM           434  '434'
            488_1  COME_FROM           420  '420'
            488_2  COME_FROM           408  '408'

 L. 202       488  LOAD_GLOBAL              isinstance
              490  LOAD_FAST                'obj'
              492  LOAD_GLOBAL              suite
              494  LOAD_ATTR                TestSuite
              496  CALL_FUNCTION_2       2  ''
          498_500  POP_JUMP_IF_FALSE   506  'to 506'

 L. 203       502  LOAD_FAST                'obj'
              504  RETURN_VALUE     
            506_0  COME_FROM           498  '498'
            506_1  COME_FROM           486  '486'
            506_2  COME_FROM           470  '470'

 L. 204       506  LOAD_GLOBAL              callable
              508  LOAD_FAST                'obj'
              510  CALL_FUNCTION_1       1  ''
          512_514  POP_JUMP_IF_FALSE   584  'to 584'

 L. 205       516  LOAD_FAST                'obj'
              518  CALL_FUNCTION_0       0  ''
              520  STORE_FAST               'test'

 L. 206       522  LOAD_GLOBAL              isinstance
              524  LOAD_FAST                'test'
              526  LOAD_GLOBAL              suite
              528  LOAD_ATTR                TestSuite
              530  CALL_FUNCTION_2       2  ''
          532_534  POP_JUMP_IF_FALSE   540  'to 540'

 L. 207       536  LOAD_FAST                'test'
              538  RETURN_VALUE     
            540_0  COME_FROM           532  '532'

 L. 208       540  LOAD_GLOBAL              isinstance
              542  LOAD_FAST                'test'
              544  LOAD_GLOBAL              case
              546  LOAD_ATTR                TestCase
              548  CALL_FUNCTION_2       2  ''
          550_552  POP_JUMP_IF_FALSE   566  'to 566'

 L. 209       554  LOAD_FAST                'self'
              556  LOAD_METHOD              suiteClass
              558  LOAD_FAST                'test'
              560  BUILD_LIST_1          1 
              562  CALL_METHOD_1         1  ''
              564  RETURN_VALUE     
            566_0  COME_FROM           550  '550'

 L. 211       566  LOAD_GLOBAL              TypeError
              568  LOAD_STR                 'calling %s returned %s, not a test'

 L. 212       570  LOAD_FAST                'obj'
              572  LOAD_FAST                'test'
              574  BUILD_TUPLE_2         2 

 L. 211       576  BINARY_MODULO    
              578  CALL_FUNCTION_1       1  ''
              580  RAISE_VARARGS_1       1  'exception instance'
              582  JUMP_FORWARD        596  'to 596'
            584_0  COME_FROM           512  '512'

 L. 214       584  LOAD_GLOBAL              TypeError
              586  LOAD_STR                 "don't know how to make test from: %s"
              588  LOAD_FAST                'obj'
              590  BINARY_MODULO    
              592  CALL_FUNCTION_1       1  ''
              594  RAISE_VARARGS_1       1  'exception instance'
            596_0  COME_FROM           582  '582'

Parse error at or near `POP_BLOCK' instruction at offset 66

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
            else:
                testFunc = getattr(testCaseClass, attrname)
                return callable(testFunc) or False
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
        else:
            if top_level_dir is None:
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
                    else:
                        if spec and spec.loader is None:
                            if spec.submodule_search_locations is not None:
                                is_namespace = True
                                for path in the_module.__path__:
                                    if not (set_implicit_top or path.startswith(top_level_dir)):
                                        pass
                                    else:
                                        self._top_level_dir = path.split(the_module.__name__.replace('.', os.path.sep))[0]
                                        tests.extend(self._find_tests(path, pattern,
                                          namespace=True))

                        else:
                            if the_module.__name__ in sys.builtin_module_names:
                                raise TypeError('Can not use builtin modules as dotted module names') from None
                            else:
                                raise TypeError("don't know how to discover from {!r}".format(the_module)) from None
                else:
                    if set_implicit_top:
                        if not is_namespace:
                            self._top_level_dir = self._get_directory_containing_module(top_part)
                            sys.path.remove(top_level_dir)
                        else:
                            sys.path.remove(top_level_dir)
                    else:
                        if is_not_importable:
                            raise ImportError('Start directory is not importable: %r' % start_dir)
                        tests = is_namespace or list(self._find_tests(start_dir, pattern))
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
                    (yield tests)
                if not should_recurse:
                    return
        paths = sorted(os.listdir(start_dir))
        for path in paths:
            full_path = os.path.join(start_dir, path)
            tests, should_recurse = self._find_test_path(full_path, pattern, namespace)
            if tests is not None:
                (yield tests)
            if should_recurse:
                name = self._get_name_from_path(full_path)
                self._loading_packages.add(name)
                try:
                    (yield from self._find_tests(full_path, pattern, namespace))
                finally:
                    self._loading_packages.discard(name)

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
            22_24  POP_JUMP_IF_FALSE   342  'to 342'

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
               82  JUMP_FORWARD        188  'to 188'
             84_0  COME_FROM_FINALLY    68  '68'

 L. 437        84  DUP_TOP          
               86  LOAD_GLOBAL              case
               88  LOAD_ATTR                SkipTest
               90  COMPARE_OP               exception-match
               92  POP_JUMP_IF_FALSE   140  'to 140'
               94  POP_TOP          
               96  STORE_FAST               'e'
               98  POP_TOP          
              100  SETUP_FINALLY       128  'to 128'

 L. 438       102  LOAD_GLOBAL              _make_skipped_test
              104  LOAD_FAST                'name'
              106  LOAD_FAST                'e'
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                suiteClass
              112  CALL_FUNCTION_3       3  ''
              114  LOAD_CONST               False
              116  BUILD_TUPLE_2         2 
              118  ROT_FOUR         
              120  POP_BLOCK        
              122  POP_EXCEPT       
              124  CALL_FINALLY        128  'to 128'
              126  RETURN_VALUE     
            128_0  COME_FROM           124  '124'
            128_1  COME_FROM_FINALLY   100  '100'
              128  LOAD_CONST               None
              130  STORE_FAST               'e'
              132  DELETE_FAST              'e'
              134  END_FINALLY      
              136  POP_EXCEPT       
              138  JUMP_FORWARD        624  'to 624'
            140_0  COME_FROM            92  '92'

 L. 439       140  POP_TOP          
              142  POP_TOP          
              144  POP_TOP          

 L. 441       146  LOAD_GLOBAL              _make_failed_import_test
              148  LOAD_FAST                'name'
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                suiteClass
              154  CALL_FUNCTION_2       2  ''

 L. 440       156  UNPACK_SEQUENCE_2     2 
              158  STORE_FAST               'error_case'
              160  STORE_FAST               'error_message'

 L. 442       162  LOAD_FAST                'self'
              164  LOAD_ATTR                errors
              166  LOAD_METHOD              append
              168  LOAD_FAST                'error_message'
              170  CALL_METHOD_1         1  ''
              172  POP_TOP          

 L. 443       174  LOAD_FAST                'error_case'
              176  LOAD_CONST               False
              178  BUILD_TUPLE_2         2 
              180  ROT_FOUR         
              182  POP_EXCEPT       
              184  RETURN_VALUE     
              186  END_FINALLY      
            188_0  COME_FROM            82  '82'

 L. 445       188  LOAD_GLOBAL              os
              190  LOAD_ATTR                path
              192  LOAD_METHOD              abspath

 L. 446       194  LOAD_GLOBAL              getattr
              196  LOAD_FAST                'module'
              198  LOAD_STR                 '__file__'
              200  LOAD_FAST                'full_path'
              202  CALL_FUNCTION_3       3  ''

 L. 445       204  CALL_METHOD_1         1  ''
              206  STORE_FAST               'mod_file'

 L. 447       208  LOAD_GLOBAL              _jython_aware_splitext

 L. 448       210  LOAD_GLOBAL              os
              212  LOAD_ATTR                path
              214  LOAD_METHOD              realpath
              216  LOAD_FAST                'mod_file'
              218  CALL_METHOD_1         1  ''

 L. 447       220  CALL_FUNCTION_1       1  ''
              222  STORE_FAST               'realpath'

 L. 449       224  LOAD_GLOBAL              _jython_aware_splitext

 L. 450       226  LOAD_GLOBAL              os
              228  LOAD_ATTR                path
              230  LOAD_METHOD              realpath
              232  LOAD_FAST                'full_path'
              234  CALL_METHOD_1         1  ''

 L. 449       236  CALL_FUNCTION_1       1  ''
              238  STORE_FAST               'fullpath_noext'

 L. 451       240  LOAD_FAST                'realpath'
              242  LOAD_METHOD              lower
              244  CALL_METHOD_0         0  ''
              246  LOAD_FAST                'fullpath_noext'
              248  LOAD_METHOD              lower
              250  CALL_METHOD_0         0  ''
              252  COMPARE_OP               !=
          254_256  POP_JUMP_IF_FALSE   320  'to 320'

 L. 452       258  LOAD_GLOBAL              os
              260  LOAD_ATTR                path
              262  LOAD_METHOD              dirname
              264  LOAD_FAST                'realpath'
              266  CALL_METHOD_1         1  ''
              268  STORE_FAST               'module_dir'

 L. 453       270  LOAD_GLOBAL              _jython_aware_splitext

 L. 454       272  LOAD_GLOBAL              os
              274  LOAD_ATTR                path
              276  LOAD_METHOD              basename
              278  LOAD_FAST                'full_path'
              280  CALL_METHOD_1         1  ''

 L. 453       282  CALL_FUNCTION_1       1  ''
              284  STORE_FAST               'mod_name'

 L. 455       286  LOAD_GLOBAL              os
              288  LOAD_ATTR                path
              290  LOAD_METHOD              dirname
              292  LOAD_FAST                'full_path'
              294  CALL_METHOD_1         1  ''
              296  STORE_FAST               'expected_dir'

 L. 456       298  LOAD_STR                 '%r module incorrectly imported from %r. Expected %r. Is this module globally installed?'
              300  STORE_FAST               'msg'

 L. 458       302  LOAD_GLOBAL              ImportError

 L. 459       304  LOAD_FAST                'msg'
              306  LOAD_FAST                'mod_name'
              308  LOAD_FAST                'module_dir'
              310  LOAD_FAST                'expected_dir'
              312  BUILD_TUPLE_3         3 
              314  BINARY_MODULO    

 L. 458       316  CALL_FUNCTION_1       1  ''
              318  RAISE_VARARGS_1       1  'exception instance'
            320_0  COME_FROM           254  '254'

 L. 460       320  LOAD_FAST                'self'
              322  LOAD_ATTR                loadTestsFromModule
              324  LOAD_FAST                'module'
              326  LOAD_FAST                'pattern'
              328  LOAD_CONST               ('pattern',)
              330  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              332  LOAD_CONST               False
              334  BUILD_TUPLE_2         2 
              336  RETURN_VALUE     
          338_340  JUMP_FORWARD        624  'to 624'
            342_0  COME_FROM            22  '22'

 L. 461       342  LOAD_GLOBAL              os
              344  LOAD_ATTR                path
              346  LOAD_METHOD              isdir
              348  LOAD_FAST                'full_path'
              350  CALL_METHOD_1         1  ''
          352_354  POP_JUMP_IF_FALSE   620  'to 620'

 L. 462       356  LOAD_FAST                'namespace'
          358_360  POP_JUMP_IF_TRUE    390  'to 390'

 L. 463       362  LOAD_GLOBAL              os
              364  LOAD_ATTR                path
              366  LOAD_METHOD              isfile
              368  LOAD_GLOBAL              os
              370  LOAD_ATTR                path
              372  LOAD_METHOD              join
              374  LOAD_FAST                'full_path'
              376  LOAD_STR                 '__init__.py'
              378  CALL_METHOD_2         2  ''
              380  CALL_METHOD_1         1  ''

 L. 462   382_384  POP_JUMP_IF_TRUE    390  'to 390'

 L. 464       386  LOAD_CONST               (None, False)
              388  RETURN_VALUE     
            390_0  COME_FROM           382  '382'
            390_1  COME_FROM           358  '358'

 L. 466       390  LOAD_CONST               None
              392  STORE_FAST               'load_tests'

 L. 467       394  LOAD_CONST               None
              396  STORE_FAST               'tests'

 L. 468       398  LOAD_FAST                'self'
              400  LOAD_METHOD              _get_name_from_path
              402  LOAD_FAST                'full_path'
              404  CALL_METHOD_1         1  ''
              406  STORE_FAST               'name'

 L. 469       408  SETUP_FINALLY       424  'to 424'

 L. 470       410  LOAD_FAST                'self'
              412  LOAD_METHOD              _get_module_from_name
              414  LOAD_FAST                'name'
              416  CALL_METHOD_1         1  ''
              418  STORE_FAST               'package'
              420  POP_BLOCK        
            422_0  COME_FROM           138  '138'
              422  JUMP_FORWARD        530  'to 530'
            424_0  COME_FROM_FINALLY   408  '408'

 L. 471       424  DUP_TOP          
              426  LOAD_GLOBAL              case
              428  LOAD_ATTR                SkipTest
              430  COMPARE_OP               exception-match
          432_434  POP_JUMP_IF_FALSE   482  'to 482'
              436  POP_TOP          
              438  STORE_FAST               'e'
              440  POP_TOP          
              442  SETUP_FINALLY       470  'to 470'

 L. 472       444  LOAD_GLOBAL              _make_skipped_test
              446  LOAD_FAST                'name'
              448  LOAD_FAST                'e'
              450  LOAD_FAST                'self'
              452  LOAD_ATTR                suiteClass
              454  CALL_FUNCTION_3       3  ''
              456  LOAD_CONST               False
              458  BUILD_TUPLE_2         2 
              460  ROT_FOUR         
              462  POP_BLOCK        
              464  POP_EXCEPT       
              466  CALL_FINALLY        470  'to 470'
              468  RETURN_VALUE     
            470_0  COME_FROM           466  '466'
            470_1  COME_FROM_FINALLY   442  '442'
              470  LOAD_CONST               None
              472  STORE_FAST               'e'
              474  DELETE_FAST              'e'
              476  END_FINALLY      
              478  POP_EXCEPT       
              480  JUMP_FORWARD        618  'to 618'
            482_0  COME_FROM           432  '432'

 L. 473       482  POP_TOP          
              484  POP_TOP          
              486  POP_TOP          

 L. 475       488  LOAD_GLOBAL              _make_failed_import_test
              490  LOAD_FAST                'name'
              492  LOAD_FAST                'self'
              494  LOAD_ATTR                suiteClass
              496  CALL_FUNCTION_2       2  ''

 L. 474       498  UNPACK_SEQUENCE_2     2 
              500  STORE_FAST               'error_case'
              502  STORE_FAST               'error_message'

 L. 476       504  LOAD_FAST                'self'
              506  LOAD_ATTR                errors
              508  LOAD_METHOD              append
              510  LOAD_FAST                'error_message'
              512  CALL_METHOD_1         1  ''
              514  POP_TOP          

 L. 477       516  LOAD_FAST                'error_case'
              518  LOAD_CONST               False
              520  BUILD_TUPLE_2         2 
              522  ROT_FOUR         
              524  POP_EXCEPT       
              526  RETURN_VALUE     
              528  END_FINALLY      
            530_0  COME_FROM           422  '422'

 L. 479       530  LOAD_GLOBAL              getattr
              532  LOAD_FAST                'package'
              534  LOAD_STR                 'load_tests'
              536  LOAD_CONST               None
              538  CALL_FUNCTION_3       3  ''
              540  STORE_FAST               'load_tests'

 L. 481       542  LOAD_FAST                'self'
              544  LOAD_ATTR                _loading_packages
              546  LOAD_METHOD              add
              548  LOAD_FAST                'name'
              550  CALL_METHOD_1         1  ''
              552  POP_TOP          

 L. 482       554  SETUP_FINALLY       604  'to 604'

 L. 483       556  LOAD_FAST                'self'
              558  LOAD_ATTR                loadTestsFromModule
              560  LOAD_FAST                'package'
              562  LOAD_FAST                'pattern'
              564  LOAD_CONST               ('pattern',)
              566  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              568  STORE_FAST               'tests'

 L. 484       570  LOAD_FAST                'load_tests'
              572  LOAD_CONST               None
              574  COMPARE_OP               is-not
          576_578  POP_JUMP_IF_FALSE   592  'to 592'

 L. 486       580  LOAD_FAST                'tests'
              582  LOAD_CONST               False
              584  BUILD_TUPLE_2         2 
              586  POP_BLOCK        
              588  CALL_FINALLY        604  'to 604'
              590  RETURN_VALUE     
            592_0  COME_FROM           576  '576'

 L. 487       592  LOAD_FAST                'tests'
              594  LOAD_CONST               True
              596  BUILD_TUPLE_2         2 
              598  POP_BLOCK        
              600  CALL_FINALLY        604  'to 604'
              602  RETURN_VALUE     
            604_0  COME_FROM           600  '600'
            604_1  COME_FROM           588  '588'
            604_2  COME_FROM_FINALLY   554  '554'

 L. 489       604  LOAD_FAST                'self'
              606  LOAD_ATTR                _loading_packages
              608  LOAD_METHOD              discard
              610  LOAD_FAST                'name'
              612  CALL_METHOD_1         1  ''
              614  POP_TOP          
              616  END_FINALLY      
            618_0  COME_FROM           480  '480'
              618  JUMP_FORWARD        624  'to 624'
            620_0  COME_FROM           352  '352'

 L. 491       620  LOAD_CONST               (None, False)
              622  RETURN_VALUE     
            624_0  COME_FROM           618  '618'
            624_1  COME_FROM           338  '338'

Parse error at or near `COME_FROM' instruction at offset 422_0


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