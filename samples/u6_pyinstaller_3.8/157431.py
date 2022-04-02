# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
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
               10  JUMP_FORWARD         40  'to 40'
             12_0  COME_FROM_FINALLY     0  '0'

 L.  35        12  DUP_TOP          
               14  LOAD_GLOBAL              AttributeError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    38  'to 38'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L.  36        26  LOAD_GLOBAL              str
               28  LOAD_FAST                'test'
               30  CALL_FUNCTION_1       1  ''
               32  ROT_FOUR         
               34  POP_EXCEPT       
               36  RETURN_VALUE     
             38_0  COME_FROM            18  '18'
               38  END_FINALLY      
             40_0  COME_FROM            10  '10'

 L.  37        40  SETUP_FINALLY        50  'to 50'

 L.  38        42  LOAD_FAST                'test_id'
               44  CALL_FUNCTION_0       0  ''
               46  POP_BLOCK        
               48  RETURN_VALUE     
             50_0  COME_FROM_FINALLY    40  '40'

 L.  39        50  DUP_TOP          
               52  LOAD_GLOBAL              TypeError
               54  COMPARE_OP               exception-match
               56  POP_JUMP_IF_FALSE    76  'to 76'
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L.  40        64  LOAD_GLOBAL              str
               66  LOAD_FAST                'test_id'
               68  CALL_FUNCTION_1       1  ''
               70  ROT_FOUR         
               72  POP_EXCEPT       
               74  RETURN_VALUE     
             76_0  COME_FROM            56  '56'
               76  END_FINALLY      

 L.  41        78  LOAD_GLOBAL              repr
               80  LOAD_FAST                'test'
               82  CALL_FUNCTION_1       1  ''
               84  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 60

    def startTest(self, test):
        super().startTest(test)
        self._RegressionTestResult__e = e = ET.SubElement(self._RegressionTestResult__suite, 'testcase')
        self._RegressionTestResult__start_time = time.perf_counter()
        if self._RegressionTestResult__verbose:
            self.stream.write(f"{self.getDescription(test)} ... ")
            self.stream.flush()

    def _add_result(self, test, capture=False, **args):
        e = self._RegressionTestResult__e
        self._RegressionTestResult__e = None
        if e is None:
            return
        e.set('name', args.pop('name', self._RegressionTestResult__getId(test)))
        e.set('status', args.pop('status', 'run'))
        e.set('result', args.pop('result', 'completed'))
        if self._RegressionTestResult__start_time:
            e.set('time', f"{time.perf_counter() - self._RegressionTestResult__start_time:0.6f}")
        if capture:
            if self._stdout_buffer is not None:
                stdout = self._stdout_buffer.getvalue().rstrip()
                ET.SubElement(e, 'system-out').text = stdout
            if self._stderr_buffer is not None:
                stderr = self._stderr_buffer.getvalue().rstrip()
                ET.SubElement(e, 'system-err').text = stderr
        for k, v in args.items():
            if k:
                if not v:
                    pass
                else:
                    e2 = ET.SubElement(e, k)
                    if hasattr(v, 'items'):
                        for k2, v2 in v.items():
                            if k2:
                                e2.set(k2, str(v2))
                            else:
                                e2.text = str(v2)

                    else:
                        e2.text = str(v)

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