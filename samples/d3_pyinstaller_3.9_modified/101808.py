# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: unittest\runner.py
"""Running tests"""
import sys, time, warnings
from . import result
from .signals import registerResult
__unittest = True

class _WritelnDecorator(object):
    __doc__ = "Used to decorate file-like objects with a handy 'writeln' method"

    def __init__(self, stream):
        self.stream = stream

    def __getattr__--- This code section failed: ---

 L.  19         0  LOAD_FAST                'attr'
                2  LOAD_CONST               ('stream', '__getstate__')
                4  <118>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.  20         8  LOAD_GLOBAL              AttributeError
               10  LOAD_FAST                'attr'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L.  21        16  LOAD_GLOBAL              getattr
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                stream
               22  LOAD_FAST                'attr'
               24  CALL_FUNCTION_2       2  ''
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def writeln(self, arg=None):
        if arg:
            self.write(arg)
        self.write('\n')


class TextTestResult(result.TestResult):
    __doc__ = 'A test result class that can print formatted text results to a stream.\n\n    Used by TextTestRunner.\n    '
    separator1 = '======================================================================'
    separator2 = '----------------------------------------------------------------------'

    def __init__(self, stream, descriptions, verbosity):
        superTextTestResultself.__init__(stream, descriptions, verbosity)
        self.stream = stream
        self.showAll = verbosity > 1
        self.dots = verbosity == 1
        self.descriptions = descriptions

    def getDescription(self, test):
        doc_first_line = test.shortDescription()
        if self.descriptions:
            if doc_first_line:
                return '\n'.join((str(test), doc_first_line))
        return str(test)

    def startTest(self, test):
        superTextTestResultself.startTest(test)
        if self.showAll:
            self.stream.write(self.getDescription(test))
            self.stream.write(' ... ')
            self.stream.flush()

    def addSuccess(self, test):
        superTextTestResultself.addSuccess(test)
        if self.showAll:
            self.stream.writeln('ok')
        elif self.dots:
            self.stream.write('.')
            self.stream.flush()

    def addError(self, test, err):
        superTextTestResultself.addError(test, err)
        if self.showAll:
            self.stream.writeln('ERROR')
        elif self.dots:
            self.stream.write('E')
            self.stream.flush()

    def addFailure(self, test, err):
        superTextTestResultself.addFailure(test, err)
        if self.showAll:
            self.stream.writeln('FAIL')
        elif self.dots:
            self.stream.write('F')
            self.stream.flush()

    def addSkip(self, test, reason):
        superTextTestResultself.addSkip(test, reason)
        if self.showAll:
            self.stream.writeln('skipped {0!r}'.format(reason))
        elif self.dots:
            self.stream.write('s')
            self.stream.flush()

    def addExpectedFailure(self, test, err):
        superTextTestResultself.addExpectedFailure(test, err)
        if self.showAll:
            self.stream.writeln('expected failure')
        elif self.dots:
            self.stream.write('x')
            self.stream.flush()

    def addUnexpectedSuccess(self, test):
        superTextTestResultself.addUnexpectedSuccess(test)
        if self.showAll:
            self.stream.writeln('unexpected success')
        elif self.dots:
            self.stream.write('u')
            self.stream.flush()

    def printErrors(self):
        if self.dots or (self.showAll):
            self.stream.writeln()
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)

    def printErrorList(self, flavour, errors):
        for test, err in errors:
            self.stream.writeln(self.separator1)
            self.stream.writeln('%s: %s' % (flavour, self.getDescription(test)))
            self.stream.writeln(self.separator2)
            self.stream.writeln('%s' % err)


class TextTestRunner(object):
    __doc__ = 'A test runner class that displays results in textual form.\n\n    It prints out the names of tests as they are run, errors as they\n    occur, and a summary of the results at the end of the test run.\n    '
    resultclass = TextTestResult

    def __init__--- This code section failed: ---

 L. 136         0  LOAD_FAST                'stream'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 137         8  LOAD_GLOBAL              sys
               10  LOAD_ATTR                stderr
               12  STORE_FAST               'stream'
             14_0  COME_FROM             6  '6'

 L. 138        14  LOAD_GLOBAL              _WritelnDecorator
               16  LOAD_FAST                'stream'
               18  CALL_FUNCTION_1       1  ''
               20  LOAD_FAST                'self'
               22  STORE_ATTR               stream

 L. 139        24  LOAD_FAST                'descriptions'
               26  LOAD_FAST                'self'
               28  STORE_ATTR               descriptions

 L. 140        30  LOAD_FAST                'verbosity'
               32  LOAD_FAST                'self'
               34  STORE_ATTR               verbosity

 L. 141        36  LOAD_FAST                'failfast'
               38  LOAD_FAST                'self'
               40  STORE_ATTR               failfast

 L. 142        42  LOAD_FAST                'buffer'
               44  LOAD_FAST                'self'
               46  STORE_ATTR               buffer

 L. 143        48  LOAD_FAST                'tb_locals'
               50  LOAD_FAST                'self'
               52  STORE_ATTR               tb_locals

 L. 144        54  LOAD_FAST                'warnings'
               56  LOAD_FAST                'self'
               58  STORE_ATTR               warnings

 L. 145        60  LOAD_FAST                'resultclass'
               62  LOAD_CONST               None
               64  <117>                 1  ''
               66  POP_JUMP_IF_FALSE    74  'to 74'

 L. 146        68  LOAD_FAST                'resultclass'
               70  LOAD_FAST                'self'
               72  STORE_ATTR               resultclass
             74_0  COME_FROM            66  '66'

Parse error at or near `None' instruction at offset -1

    def _makeResult(self):
        return self.resultclass(self.stream, self.descriptions, self.verbosity)

    def run--- This code section failed: ---

 L. 153         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _makeResult
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'result'

 L. 154         8  LOAD_GLOBAL              registerResult
               10  LOAD_FAST                'result'
               12  CALL_FUNCTION_1       1  ''
               14  POP_TOP          

 L. 155        16  LOAD_FAST                'self'
               18  LOAD_ATTR                failfast
               20  LOAD_FAST                'result'
               22  STORE_ATTR               failfast

 L. 156        24  LOAD_FAST                'self'
               26  LOAD_ATTR                buffer
               28  LOAD_FAST                'result'
               30  STORE_ATTR               buffer

 L. 157        32  LOAD_FAST                'self'
               34  LOAD_ATTR                tb_locals
               36  LOAD_FAST                'result'
               38  STORE_ATTR               tb_locals

 L. 158        40  LOAD_GLOBAL              warnings
               42  LOAD_METHOD              catch_warnings
               44  CALL_METHOD_0         0  ''
               46  SETUP_WITH          218  'to 218'
               48  POP_TOP          

 L. 159        50  LOAD_FAST                'self'
               52  LOAD_ATTR                warnings
               54  POP_JUMP_IF_FALSE    94  'to 94'

 L. 161        56  LOAD_GLOBAL              warnings
               58  LOAD_METHOD              simplefilter
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                warnings
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          

 L. 167        68  LOAD_FAST                'self'
               70  LOAD_ATTR                warnings
               72  LOAD_CONST               ('default', 'always')
               74  <118>                 0  ''
               76  POP_JUMP_IF_FALSE    94  'to 94'

 L. 168        78  LOAD_GLOBAL              warnings
               80  LOAD_ATTR                filterwarnings
               82  LOAD_STR                 'module'

 L. 169        84  LOAD_GLOBAL              DeprecationWarning

 L. 170        86  LOAD_STR                 'Please use assert\\w+ instead.'

 L. 168        88  LOAD_CONST               ('category', 'message')
               90  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               92  POP_TOP          
             94_0  COME_FROM            76  '76'
             94_1  COME_FROM            54  '54'

 L. 171        94  LOAD_GLOBAL              time
               96  LOAD_METHOD              perf_counter
               98  CALL_METHOD_0         0  ''
              100  STORE_FAST               'startTime'

 L. 172       102  LOAD_GLOBAL              getattr
              104  LOAD_FAST                'result'
              106  LOAD_STR                 'startTestRun'
              108  LOAD_CONST               None
              110  CALL_FUNCTION_3       3  ''
              112  STORE_FAST               'startTestRun'

 L. 173       114  LOAD_FAST                'startTestRun'
              116  LOAD_CONST               None
              118  <117>                 1  ''
              120  POP_JUMP_IF_FALSE   128  'to 128'

 L. 174       122  LOAD_FAST                'startTestRun'
              124  CALL_FUNCTION_0       0  ''
              126  POP_TOP          
            128_0  COME_FROM           120  '120'

 L. 175       128  SETUP_FINALLY       168  'to 168'

 L. 176       130  LOAD_FAST                'test'
              132  LOAD_FAST                'result'
              134  CALL_FUNCTION_1       1  ''
              136  POP_TOP          
              138  POP_BLOCK        

 L. 178       140  LOAD_GLOBAL              getattr
              142  LOAD_FAST                'result'
              144  LOAD_STR                 'stopTestRun'
              146  LOAD_CONST               None
              148  CALL_FUNCTION_3       3  ''
              150  STORE_FAST               'stopTestRun'

 L. 179       152  LOAD_FAST                'stopTestRun'
              154  LOAD_CONST               None
              156  <117>                 1  ''
              158  POP_JUMP_IF_FALSE   196  'to 196'

 L. 180       160  LOAD_FAST                'stopTestRun'
              162  CALL_FUNCTION_0       0  ''
              164  POP_TOP          
              166  JUMP_FORWARD        196  'to 196'
            168_0  COME_FROM_FINALLY   128  '128'

 L. 178       168  LOAD_GLOBAL              getattr
              170  LOAD_FAST                'result'
              172  LOAD_STR                 'stopTestRun'
              174  LOAD_CONST               None
              176  CALL_FUNCTION_3       3  ''
              178  STORE_FAST               'stopTestRun'

 L. 179       180  LOAD_FAST                'stopTestRun'
              182  LOAD_CONST               None
              184  <117>                 1  ''
              186  POP_JUMP_IF_FALSE   194  'to 194'

 L. 180       188  LOAD_FAST                'stopTestRun'
              190  CALL_FUNCTION_0       0  ''
              192  POP_TOP          
            194_0  COME_FROM           186  '186'
              194  <48>             
            196_0  COME_FROM           166  '166'
            196_1  COME_FROM           158  '158'

 L. 181       196  LOAD_GLOBAL              time
              198  LOAD_METHOD              perf_counter
              200  CALL_METHOD_0         0  ''
              202  STORE_FAST               'stopTime'
              204  POP_BLOCK        
              206  LOAD_CONST               None
              208  DUP_TOP          
              210  DUP_TOP          
              212  CALL_FUNCTION_3       3  ''
              214  POP_TOP          
              216  JUMP_FORWARD        234  'to 234'
            218_0  COME_FROM_WITH       46  '46'
              218  <49>             
              220  POP_JUMP_IF_TRUE    224  'to 224'
              222  <48>             
            224_0  COME_FROM           220  '220'
              224  POP_TOP          
              226  POP_TOP          
              228  POP_TOP          
              230  POP_EXCEPT       
              232  POP_TOP          
            234_0  COME_FROM           216  '216'

 L. 182       234  LOAD_FAST                'stopTime'
              236  LOAD_FAST                'startTime'
              238  BINARY_SUBTRACT  
              240  STORE_FAST               'timeTaken'

 L. 183       242  LOAD_FAST                'result'
              244  LOAD_METHOD              printErrors
              246  CALL_METHOD_0         0  ''
              248  POP_TOP          

 L. 184       250  LOAD_GLOBAL              hasattr
              252  LOAD_FAST                'result'
              254  LOAD_STR                 'separator2'
              256  CALL_FUNCTION_2       2  ''
          258_260  POP_JUMP_IF_FALSE   276  'to 276'

 L. 185       262  LOAD_FAST                'self'
              264  LOAD_ATTR                stream
              266  LOAD_METHOD              writeln
              268  LOAD_FAST                'result'
              270  LOAD_ATTR                separator2
              272  CALL_METHOD_1         1  ''
              274  POP_TOP          
            276_0  COME_FROM           258  '258'

 L. 186       276  LOAD_FAST                'result'
              278  LOAD_ATTR                testsRun
              280  STORE_FAST               'run'

 L. 187       282  LOAD_FAST                'self'
              284  LOAD_ATTR                stream
              286  LOAD_METHOD              writeln
              288  LOAD_STR                 'Ran %d test%s in %.3fs'

 L. 188       290  LOAD_FAST                'run'
              292  LOAD_FAST                'run'
              294  LOAD_CONST               1
              296  COMPARE_OP               !=
          298_300  POP_JUMP_IF_FALSE   308  'to 308'
              302  LOAD_STR                 's'
          304_306  JUMP_IF_TRUE_OR_POP   310  'to 310'
            308_0  COME_FROM           298  '298'
              308  LOAD_STR                 ''
            310_0  COME_FROM           304  '304'
              310  LOAD_FAST                'timeTaken'
              312  BUILD_TUPLE_3         3 

 L. 187       314  BINARY_MODULO    
              316  CALL_METHOD_1         1  ''
              318  POP_TOP          

 L. 189       320  LOAD_FAST                'self'
              322  LOAD_ATTR                stream
              324  LOAD_METHOD              writeln
              326  CALL_METHOD_0         0  ''
              328  POP_TOP          

 L. 191       330  LOAD_CONST               0
              332  DUP_TOP          
              334  STORE_FAST               'expectedFails'
              336  DUP_TOP          
              338  STORE_FAST               'unexpectedSuccesses'
              340  STORE_FAST               'skipped'

 L. 192       342  SETUP_FINALLY       370  'to 370'

 L. 193       344  LOAD_GLOBAL              map
              346  LOAD_GLOBAL              len
              348  LOAD_FAST                'result'
              350  LOAD_ATTR                expectedFailures

 L. 194       352  LOAD_FAST                'result'
              354  LOAD_ATTR                unexpectedSuccesses

 L. 195       356  LOAD_FAST                'result'
              358  LOAD_ATTR                skipped

 L. 193       360  BUILD_TUPLE_3         3 
              362  CALL_FUNCTION_2       2  ''
              364  STORE_FAST               'results'
              366  POP_BLOCK        
              368  JUMP_FORWARD        390  'to 390'
            370_0  COME_FROM_FINALLY   342  '342'

 L. 196       370  DUP_TOP          
              372  LOAD_GLOBAL              AttributeError
          374_376  <121>               388  ''
              378  POP_TOP          
              380  POP_TOP          
              382  POP_TOP          

 L. 197       384  POP_EXCEPT       
              386  JUMP_FORWARD        400  'to 400'
              388  <48>             
            390_0  COME_FROM           368  '368'

 L. 199       390  LOAD_FAST                'results'
              392  UNPACK_SEQUENCE_3     3 
              394  STORE_FAST               'expectedFails'
              396  STORE_FAST               'unexpectedSuccesses'
              398  STORE_FAST               'skipped'
            400_0  COME_FROM           386  '386'

 L. 201       400  BUILD_LIST_0          0 
              402  STORE_FAST               'infos'

 L. 202       404  LOAD_FAST                'result'
              406  LOAD_METHOD              wasSuccessful
              408  CALL_METHOD_0         0  ''
          410_412  POP_JUMP_IF_TRUE    490  'to 490'

 L. 203       414  LOAD_FAST                'self'
              416  LOAD_ATTR                stream
              418  LOAD_METHOD              write
              420  LOAD_STR                 'FAILED'
              422  CALL_METHOD_1         1  ''
              424  POP_TOP          

 L. 204       426  LOAD_GLOBAL              len
              428  LOAD_FAST                'result'
              430  LOAD_ATTR                failures
              432  CALL_FUNCTION_1       1  ''
              434  LOAD_GLOBAL              len
              436  LOAD_FAST                'result'
              438  LOAD_ATTR                errors
              440  CALL_FUNCTION_1       1  ''
              442  ROT_TWO          
              444  STORE_FAST               'failed'
              446  STORE_FAST               'errored'

 L. 205       448  LOAD_FAST                'failed'
          450_452  POP_JUMP_IF_FALSE   468  'to 468'

 L. 206       454  LOAD_FAST                'infos'
              456  LOAD_METHOD              append
              458  LOAD_STR                 'failures=%d'
              460  LOAD_FAST                'failed'
              462  BINARY_MODULO    
              464  CALL_METHOD_1         1  ''
              466  POP_TOP          
            468_0  COME_FROM           450  '450'

 L. 207       468  LOAD_FAST                'errored'
          470_472  POP_JUMP_IF_FALSE   502  'to 502'

 L. 208       474  LOAD_FAST                'infos'
              476  LOAD_METHOD              append
              478  LOAD_STR                 'errors=%d'
              480  LOAD_FAST                'errored'
              482  BINARY_MODULO    
              484  CALL_METHOD_1         1  ''
              486  POP_TOP          
              488  JUMP_FORWARD        502  'to 502'
            490_0  COME_FROM           410  '410'

 L. 210       490  LOAD_FAST                'self'
              492  LOAD_ATTR                stream
              494  LOAD_METHOD              write
              496  LOAD_STR                 'OK'
              498  CALL_METHOD_1         1  ''
              500  POP_TOP          
            502_0  COME_FROM           488  '488'
            502_1  COME_FROM           470  '470'

 L. 211       502  LOAD_FAST                'skipped'
          504_506  POP_JUMP_IF_FALSE   522  'to 522'

 L. 212       508  LOAD_FAST                'infos'
              510  LOAD_METHOD              append
              512  LOAD_STR                 'skipped=%d'
              514  LOAD_FAST                'skipped'
              516  BINARY_MODULO    
              518  CALL_METHOD_1         1  ''
              520  POP_TOP          
            522_0  COME_FROM           504  '504'

 L. 213       522  LOAD_FAST                'expectedFails'
          524_526  POP_JUMP_IF_FALSE   542  'to 542'

 L. 214       528  LOAD_FAST                'infos'
              530  LOAD_METHOD              append
              532  LOAD_STR                 'expected failures=%d'
              534  LOAD_FAST                'expectedFails'
              536  BINARY_MODULO    
              538  CALL_METHOD_1         1  ''
              540  POP_TOP          
            542_0  COME_FROM           524  '524'

 L. 215       542  LOAD_FAST                'unexpectedSuccesses'
          544_546  POP_JUMP_IF_FALSE   562  'to 562'

 L. 216       548  LOAD_FAST                'infos'
              550  LOAD_METHOD              append
              552  LOAD_STR                 'unexpected successes=%d'
              554  LOAD_FAST                'unexpectedSuccesses'
              556  BINARY_MODULO    
              558  CALL_METHOD_1         1  ''
              560  POP_TOP          
            562_0  COME_FROM           544  '544'

 L. 217       562  LOAD_FAST                'infos'
          564_566  POP_JUMP_IF_FALSE   594  'to 594'

 L. 218       568  LOAD_FAST                'self'
              570  LOAD_ATTR                stream
              572  LOAD_METHOD              writeln
              574  LOAD_STR                 ' (%s)'
              576  LOAD_STR                 ', '
              578  LOAD_METHOD              join
              580  LOAD_FAST                'infos'
              582  CALL_METHOD_1         1  ''
              584  BUILD_TUPLE_1         1 
              586  BINARY_MODULO    
              588  CALL_METHOD_1         1  ''
              590  POP_TOP          
              592  JUMP_FORWARD        606  'to 606'
            594_0  COME_FROM           564  '564'

 L. 220       594  LOAD_FAST                'self'
              596  LOAD_ATTR                stream
              598  LOAD_METHOD              write
              600  LOAD_STR                 '\n'
              602  CALL_METHOD_1         1  ''
              604  POP_TOP          
            606_0  COME_FROM           592  '592'

 L. 221       606  LOAD_FAST                'result'
              608  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 74