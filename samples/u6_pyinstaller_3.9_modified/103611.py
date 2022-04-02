# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: test\support\testresult.py
"""Test runner and result class for the regression test suite.

"""
import functools, io, sys, time, traceback, unittest
import xml.etree.ElementTree as ET
from datetime import datetime

class RegressionTestResult(unittest.TextTestResult):
    separator1 = '======================================================================\n'
    separator2 = '----------------------------------------------------------------------\n'

    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream=stream, descriptions=descriptions, verbosity=0)
        self.buffer = True
        self._RegressionTestResult__suite = ET.Element('testsuite')
        self._RegressionTestResult__suite.set('start', datetime.utcnow().isoformat(' '))
        self._RegressionTestResult__e = None
        self._RegressionTestResult__start_time = None
        self._RegressionTestResult__results = []
        self._RegressionTestResult__verbose = bool(verbosity)

    @classmethod
    def __getId--- This code section failed: ---

 L.  33         0  SETUP_FINALLY        12  'to 12'

 L.  34         2  LOAD_FAST                'test'
                4  LOAD_ATTR                id
                6  STORE_FAST               'test_id'
                8  POP_BLOCK        
               10  JUMP_FORWARD         38  'to 38'
             12_0  COME_FROM_FINALLY     0  '0'

 L.  35        12  DUP_TOP          
               14  LOAD_GLOBAL              AttributeError
               16  <121>                36  ''
               18  POP_TOP          
               20  POP_TOP          
               22  POP_TOP          

 L.  36        24  LOAD_GLOBAL              str
               26  LOAD_FAST                'test'
               28  CALL_FUNCTION_1       1  ''
               30  ROT_FOUR         
               32  POP_EXCEPT       
               34  RETURN_VALUE     
               36  <48>             
             38_0  COME_FROM            10  '10'

 L.  37        38  SETUP_FINALLY        48  'to 48'

 L.  38        40  LOAD_FAST                'test_id'
               42  CALL_FUNCTION_0       0  ''
               44  POP_BLOCK        
               46  RETURN_VALUE     
             48_0  COME_FROM_FINALLY    38  '38'

 L.  39        48  DUP_TOP          
               50  LOAD_GLOBAL              TypeError
               52  <121>                72  ''
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L.  40        60  LOAD_GLOBAL              str
               62  LOAD_FAST                'test_id'
               64  CALL_FUNCTION_1       1  ''
               66  ROT_FOUR         
               68  POP_EXCEPT       
               70  RETURN_VALUE     
               72  <48>             

 L.  41        74  LOAD_GLOBAL              repr
               76  LOAD_FAST                'test'
               78  CALL_FUNCTION_1       1  ''
               80  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 16

    def startTest(self, test):
        super().startTest(test)
        self._RegressionTestResult__e = e = ET.SubElement(self._RegressionTestResult__suite, 'testcase')
        self._RegressionTestResult__start_time = time.perf_counter()
        if self._RegressionTestResult__verbose:
            self.stream.write(f"{self.getDescription(test)} ... ")
            self.stream.flush()

    def _add_result--- This code section failed: ---

 L.  52         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _RegressionTestResult__e
                4  STORE_FAST               'e'

 L.  53         6  LOAD_CONST               None
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _RegressionTestResult__e

 L.  54        12  LOAD_FAST                'e'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L.  55        20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L.  56        24  LOAD_FAST                'e'
               26  LOAD_METHOD              set
               28  LOAD_STR                 'name'
               30  LOAD_FAST                'args'
               32  LOAD_METHOD              pop
               34  LOAD_STR                 'name'
               36  LOAD_FAST                'self'
               38  LOAD_METHOD              _RegressionTestResult__getId
               40  LOAD_FAST                'test'
               42  CALL_METHOD_1         1  ''
               44  CALL_METHOD_2         2  ''
               46  CALL_METHOD_2         2  ''
               48  POP_TOP          

 L.  57        50  LOAD_FAST                'e'
               52  LOAD_METHOD              set
               54  LOAD_STR                 'status'
               56  LOAD_FAST                'args'
               58  LOAD_METHOD              pop
               60  LOAD_STR                 'status'
               62  LOAD_STR                 'run'
               64  CALL_METHOD_2         2  ''
               66  CALL_METHOD_2         2  ''
               68  POP_TOP          

 L.  58        70  LOAD_FAST                'e'
               72  LOAD_METHOD              set
               74  LOAD_STR                 'result'
               76  LOAD_FAST                'args'
               78  LOAD_METHOD              pop
               80  LOAD_STR                 'result'
               82  LOAD_STR                 'completed'
               84  CALL_METHOD_2         2  ''
               86  CALL_METHOD_2         2  ''
               88  POP_TOP          

 L.  59        90  LOAD_FAST                'self'
               92  LOAD_ATTR                _RegressionTestResult__start_time
               94  POP_JUMP_IF_FALSE   122  'to 122'

 L.  60        96  LOAD_FAST                'e'
               98  LOAD_METHOD              set
              100  LOAD_STR                 'time'
              102  LOAD_GLOBAL              time
              104  LOAD_METHOD              perf_counter
              106  CALL_METHOD_0         0  ''
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                _RegressionTestResult__start_time
              112  BINARY_SUBTRACT  
              114  LOAD_STR                 '0.6f'
              116  FORMAT_VALUE_ATTR     4  ''
              118  CALL_METHOD_2         2  ''
              120  POP_TOP          
            122_0  COME_FROM            94  '94'

 L.  62       122  LOAD_FAST                'capture'
              124  POP_JUMP_IF_FALSE   202  'to 202'

 L.  63       126  LOAD_FAST                'self'
              128  LOAD_ATTR                _stdout_buffer
              130  LOAD_CONST               None
              132  <117>                 1  ''
              134  POP_JUMP_IF_FALSE   164  'to 164'

 L.  64       136  LOAD_FAST                'self'
              138  LOAD_ATTR                _stdout_buffer
              140  LOAD_METHOD              getvalue
              142  CALL_METHOD_0         0  ''
              144  LOAD_METHOD              rstrip
              146  CALL_METHOD_0         0  ''
              148  STORE_FAST               'stdout'

 L.  65       150  LOAD_FAST                'stdout'
              152  LOAD_GLOBAL              ET
              154  LOAD_METHOD              SubElement
              156  LOAD_FAST                'e'
              158  LOAD_STR                 'system-out'
              160  CALL_METHOD_2         2  ''
              162  STORE_ATTR               text
            164_0  COME_FROM           134  '134'

 L.  66       164  LOAD_FAST                'self'
              166  LOAD_ATTR                _stderr_buffer
              168  LOAD_CONST               None
              170  <117>                 1  ''
              172  POP_JUMP_IF_FALSE   202  'to 202'

 L.  67       174  LOAD_FAST                'self'
              176  LOAD_ATTR                _stderr_buffer
              178  LOAD_METHOD              getvalue
              180  CALL_METHOD_0         0  ''
              182  LOAD_METHOD              rstrip
              184  CALL_METHOD_0         0  ''
              186  STORE_FAST               'stderr'

 L.  68       188  LOAD_FAST                'stderr'
              190  LOAD_GLOBAL              ET
              192  LOAD_METHOD              SubElement
              194  LOAD_FAST                'e'
              196  LOAD_STR                 'system-err'
              198  CALL_METHOD_2         2  ''
              200  STORE_ATTR               text
            202_0  COME_FROM           172  '172'
            202_1  COME_FROM           124  '124'

 L.  70       202  LOAD_FAST                'args'
              204  LOAD_METHOD              items
              206  CALL_METHOD_0         0  ''
              208  GET_ITER         
            210_0  COME_FROM           220  '220'
              210  FOR_ITER            320  'to 320'
              212  UNPACK_SEQUENCE_2     2 
              214  STORE_FAST               'k'
              216  STORE_FAST               'v'

 L.  71       218  LOAD_FAST                'k'
              220  POP_JUMP_IF_FALSE   210  'to 210'
              222  LOAD_FAST                'v'
              224  POP_JUMP_IF_TRUE    228  'to 228'

 L.  72       226  JUMP_BACK           210  'to 210'
            228_0  COME_FROM           224  '224'

 L.  73       228  LOAD_GLOBAL              ET
              230  LOAD_METHOD              SubElement
              232  LOAD_FAST                'e'
              234  LOAD_FAST                'k'
              236  CALL_METHOD_2         2  ''
              238  STORE_FAST               'e2'

 L.  74       240  LOAD_GLOBAL              hasattr
              242  LOAD_FAST                'v'
              244  LOAD_STR                 'items'
              246  CALL_FUNCTION_2       2  ''
          248_250  POP_JUMP_IF_FALSE   308  'to 308'

 L.  75       252  LOAD_FAST                'v'
              254  LOAD_METHOD              items
              256  CALL_METHOD_0         0  ''
              258  GET_ITER         
              260  FOR_ITER            306  'to 306'
              262  UNPACK_SEQUENCE_2     2 
              264  STORE_FAST               'k2'
              266  STORE_FAST               'v2'

 L.  76       268  LOAD_FAST                'k2'
          270_272  POP_JUMP_IF_FALSE   292  'to 292'

 L.  77       274  LOAD_FAST                'e2'
              276  LOAD_METHOD              set
              278  LOAD_FAST                'k2'
              280  LOAD_GLOBAL              str
              282  LOAD_FAST                'v2'
              284  CALL_FUNCTION_1       1  ''
              286  CALL_METHOD_2         2  ''
              288  POP_TOP          
              290  JUMP_BACK           260  'to 260'
            292_0  COME_FROM           270  '270'

 L.  79       292  LOAD_GLOBAL              str
              294  LOAD_FAST                'v2'
              296  CALL_FUNCTION_1       1  ''
              298  LOAD_FAST                'e2'
              300  STORE_ATTR               text
          302_304  JUMP_BACK           260  'to 260'
              306  JUMP_BACK           210  'to 210'
            308_0  COME_FROM           248  '248'

 L.  81       308  LOAD_GLOBAL              str
              310  LOAD_FAST                'v'
              312  CALL_FUNCTION_1       1  ''
              314  LOAD_FAST                'e2'
              316  STORE_ATTR               text
              318  JUMP_BACK           210  'to 210'

Parse error at or near `<117>' instruction at offset 16

    def __write(self, c, word):
        if self._RegressionTestResult__verbose:
            self.stream.write(f"{word}\n")

    @classmethod
    def __makeErrorDict(cls, err_type, err_value, err_tb):
        if isinstance(err_type, type):
            if err_type.__module__ == 'builtins':
                typename = err_type.__name__
            else:
                typename = f"{err_type.__module__}.{err_type.__name__}"
        else:
            typename = repr(err_type)
        msg = traceback.format_exception(err_type, err_value, None)
        tb = traceback.format_exception(err_type, err_value, err_tb)
        return {'type':typename, 
         'message':''.join(msg), 
         '':''.join(tb)}

    def addError(self, test, err):
        self._add_result(test, True, error=(self._RegressionTestResult__makeErrorDict)(*err))
        super().addError(test, err)
        self._RegressionTestResult__write('E', 'ERROR')

    def addExpectedFailure(self, test, err):
        self._add_result(test, True, output=(self._RegressionTestResult__makeErrorDict)(*err))
        super().addExpectedFailure(test, err)
        self._RegressionTestResult__write('x', 'expected failure')

    def addFailure(self, test, err):
        self._add_result(test, True, failure=(self._RegressionTestResult__makeErrorDict)(*err))
        super().addFailure(test, err)
        self._RegressionTestResult__write('F', 'FAIL')

    def addSkip(self, test, reason):
        self._add_result(test, skipped=reason)
        super().addSkip(test, reason)
        self._RegressionTestResult__write('S', f"skipped {reason!r}")

    def addSuccess(self, test):
        self._add_result(test)
        super().addSuccess(test)
        self._RegressionTestResult__write('.', 'ok')

    def addUnexpectedSuccess(self, test):
        self._add_result(test, outcome='UNEXPECTED_SUCCESS')
        super().addUnexpectedSuccess(test)
        self._RegressionTestResult__write('u', 'unexpected success')

    def printErrors(self):
        if self._RegressionTestResult__verbose:
            self.stream.write('\n')
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)

    def printErrorList(self, flavor, errors):
        for test, err in errors:
            self.stream.write(self.separator1)
            self.stream.write(f"{flavor}: {self.getDescription(test)}\n")
            self.stream.write(self.separator2)
            self.stream.write('%s\n' % err)

    def get_xml_element(self):
        e = self._RegressionTestResult__suite
        e.set('tests', str(self.testsRun))
        e.set('errors', str(len(self.errors)))
        e.set('failures', str(len(self.failures)))
        return e


class QuietRegressionTestRunner:

    def __init__(self, stream, buffer=False):
        self.result = RegressionTestResult(stream, None, 0)
        self.result.buffer = buffer

    def run(self, test):
        test(self.result)
        return self.result


def get_test_runner_class(verbosity, buffer=False):
    if verbosity:
        return functools.partial((unittest.TextTestRunner), resultclass=RegressionTestResult,
          buffer=buffer,
          verbosity=verbosity)
    return functools.partial(QuietRegressionTestRunner, buffer=buffer)


def get_test_runner(stream, verbosity, capture_output=False):
    return get_test_runner_class(verbosity, capture_output)(stream)


if __name__ == '__main__':

    class TestTests(unittest.TestCase):

        def test_pass(self):
            pass

        def test_pass_slow(self):
            time.sleep(1.0)

        def test_fail(self):
            print('stdout', file=(sys.stdout))
            print('stderr', file=(sys.stderr))
            self.fail('failure message')

        def test_error(self):
            print('stdout', file=(sys.stdout))
            print('stderr', file=(sys.stderr))
            raise RuntimeError('error message')


    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestTests))
    stream = io.StringIO()
    runner_cls = get_test_runner_class(sum((a == '-v' for a in sys.argv)))
    runner = runner_cls(sys.stdout)
    result = runner.run(suite)
    print('Output:', stream.getvalue())
    print('XML: ', end='')
    for s in ET.tostringlist(result.get_xml_element()):
        print((s.decode()), end='')
    else:
        print()