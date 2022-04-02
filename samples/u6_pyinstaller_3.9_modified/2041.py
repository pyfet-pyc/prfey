# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: numpy\testing\_private\noseclasses.py
import os, sys, doctest, inspect, numpy, nose
import nose.plugins as npd
from nose.plugins.errorclass import ErrorClass, ErrorClassPlugin
from nose.plugins.base import Plugin
from nose.util import src
from .nosetester import get_package_name
from .utils import KnownFailureException, KnownFailureTest

class NumpyDocTestFinder(doctest.DocTestFinder):

    def _from_module--- This code section failed: ---

 L.  35         0  LOAD_FAST                'module'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.  36         8  LOAD_CONST               True
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L.  37        12  LOAD_GLOBAL              inspect
               14  LOAD_METHOD              isfunction
               16  LOAD_FAST                'object'
               18  CALL_METHOD_1         1  ''
               20  POP_JUMP_IF_FALSE    34  'to 34'

 L.  38        22  LOAD_FAST                'module'
               24  LOAD_ATTR                __dict__
               26  LOAD_FAST                'object'
               28  LOAD_ATTR                __globals__
               30  <117>                 0  ''
               32  RETURN_VALUE     
             34_0  COME_FROM            20  '20'

 L.  39        34  LOAD_GLOBAL              inspect
               36  LOAD_METHOD              isbuiltin
               38  LOAD_FAST                'object'
               40  CALL_METHOD_1         1  ''
               42  POP_JUMP_IF_FALSE    56  'to 56'

 L.  40        44  LOAD_FAST                'module'
               46  LOAD_ATTR                __name__
               48  LOAD_FAST                'object'
               50  LOAD_ATTR                __module__
               52  COMPARE_OP               ==
               54  RETURN_VALUE     
             56_0  COME_FROM            42  '42'

 L.  41        56  LOAD_GLOBAL              inspect
               58  LOAD_METHOD              isclass
               60  LOAD_FAST                'object'
               62  CALL_METHOD_1         1  ''
               64  POP_JUMP_IF_FALSE    78  'to 78'

 L.  42        66  LOAD_FAST                'module'
               68  LOAD_ATTR                __name__
               70  LOAD_FAST                'object'
               72  LOAD_ATTR                __module__
               74  COMPARE_OP               ==
               76  RETURN_VALUE     
             78_0  COME_FROM            64  '64'

 L.  43        78  LOAD_GLOBAL              inspect
               80  LOAD_METHOD              ismethod
               82  LOAD_FAST                'object'
               84  CALL_METHOD_1         1  ''
               86  POP_JUMP_IF_FALSE   104  'to 104'

 L.  48        88  LOAD_FAST                'module'
               90  LOAD_ATTR                __name__
               92  LOAD_FAST                'object'
               94  LOAD_ATTR                __self__
               96  LOAD_ATTR                __class__
               98  LOAD_ATTR                __module__
              100  COMPARE_OP               ==
              102  RETURN_VALUE     
            104_0  COME_FROM            86  '86'

 L.  49       104  LOAD_GLOBAL              inspect
              106  LOAD_METHOD              getmodule
              108  LOAD_FAST                'object'
              110  CALL_METHOD_1         1  ''
              112  LOAD_CONST               None
              114  <117>                 1  ''
              116  POP_JUMP_IF_FALSE   132  'to 132'

 L.  50       118  LOAD_FAST                'module'
              120  LOAD_GLOBAL              inspect
              122  LOAD_METHOD              getmodule
              124  LOAD_FAST                'object'
              126  CALL_METHOD_1         1  ''
              128  <117>                 0  ''
              130  RETURN_VALUE     
            132_0  COME_FROM           116  '116'

 L.  51       132  LOAD_GLOBAL              hasattr
              134  LOAD_FAST                'object'
              136  LOAD_STR                 '__module__'
              138  CALL_FUNCTION_2       2  ''
              140  POP_JUMP_IF_FALSE   154  'to 154'

 L.  52       142  LOAD_FAST                'module'
              144  LOAD_ATTR                __name__
              146  LOAD_FAST                'object'
              148  LOAD_ATTR                __module__
              150  COMPARE_OP               ==
              152  RETURN_VALUE     
            154_0  COME_FROM           140  '140'

 L.  53       154  LOAD_GLOBAL              isinstance
              156  LOAD_FAST                'object'
              158  LOAD_GLOBAL              property
              160  CALL_FUNCTION_2       2  ''
              162  POP_JUMP_IF_FALSE   168  'to 168'

 L.  54       164  LOAD_CONST               True
              166  RETURN_VALUE     
            168_0  COME_FROM           162  '162'

 L.  56       168  LOAD_GLOBAL              ValueError
              170  LOAD_STR                 'object must be a class or function'
              172  CALL_FUNCTION_1       1  ''
              174  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `None' instruction at offset -1

    def _find--- This code section failed: ---

 L.  64         0  LOAD_GLOBAL              doctest
                2  LOAD_ATTR                DocTestFinder
                4  LOAD_METHOD              _find
                6  LOAD_FAST                'self'
                8  LOAD_FAST                'tests'
               10  LOAD_FAST                'obj'
               12  LOAD_FAST                'name'
               14  LOAD_FAST                'module'

 L.  65        16  LOAD_FAST                'source_lines'
               18  LOAD_FAST                'globs'
               20  LOAD_FAST                'seen'

 L.  64        22  CALL_METHOD_8         8  ''
               24  POP_TOP          

 L.  72        26  LOAD_CONST               0
               28  LOAD_CONST               ('isroutine', 'isclass', 'ismodule', 'isfunction', 'ismethod')
               30  IMPORT_NAME              inspect
               32  IMPORT_FROM              isroutine
               34  STORE_FAST               'isroutine'
               36  IMPORT_FROM              isclass
               38  STORE_FAST               'isclass'
               40  IMPORT_FROM              ismodule
               42  STORE_FAST               'ismodule'
               44  IMPORT_FROM              isfunction
               46  STORE_FAST               'isfunction'
               48  IMPORT_FROM              ismethod
               50  STORE_FAST               'ismethod'
               52  POP_TOP          

 L.  77        54  LOAD_FAST                'ismodule'
               56  LOAD_FAST                'obj'
               58  CALL_FUNCTION_1       1  ''
               60  POP_JUMP_IF_FALSE   150  'to 150'
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                _recurse
               66  POP_JUMP_IF_FALSE   150  'to 150'

 L.  78        68  LOAD_FAST                'obj'
               70  LOAD_ATTR                __dict__
               72  LOAD_METHOD              items
               74  CALL_METHOD_0         0  ''
               76  GET_ITER         
             78_0  COME_FROM           124  '124'
             78_1  COME_FROM           112  '112'
               78  FOR_ITER            150  'to 150'
               80  UNPACK_SEQUENCE_2     2 
               82  STORE_FAST               'valname'
               84  STORE_FAST               'val'

 L.  79        86  LOAD_STR                 '%s.%s'
               88  LOAD_FAST                'name'
               90  LOAD_FAST                'valname'
               92  BUILD_TUPLE_2         2 
               94  BINARY_MODULO    
               96  STORE_FAST               'valname1'

 L.  80        98  LOAD_FAST                'isroutine'
              100  LOAD_FAST                'val'
              102  CALL_FUNCTION_1       1  ''
              104  POP_JUMP_IF_TRUE    114  'to 114'
              106  LOAD_FAST                'isclass'
              108  LOAD_FAST                'val'
              110  CALL_FUNCTION_1       1  ''
              112  POP_JUMP_IF_FALSE    78  'to 78'
            114_0  COME_FROM           104  '104'

 L.  81       114  LOAD_FAST                'self'
              116  LOAD_METHOD              _from_module
              118  LOAD_FAST                'module'
              120  LOAD_FAST                'val'
              122  CALL_METHOD_2         2  ''

 L.  80       124  POP_JUMP_IF_FALSE    78  'to 78'

 L.  83       126  LOAD_FAST                'self'
              128  LOAD_METHOD              _find
              130  LOAD_FAST                'tests'
              132  LOAD_FAST                'val'
              134  LOAD_FAST                'valname1'
              136  LOAD_FAST                'module'
              138  LOAD_FAST                'source_lines'

 L.  84       140  LOAD_FAST                'globs'
              142  LOAD_FAST                'seen'

 L.  83       144  CALL_METHOD_7         7  ''
              146  POP_TOP          
              148  JUMP_BACK            78  'to 78'
            150_0  COME_FROM            66  '66'
            150_1  COME_FROM            60  '60'

 L.  87       150  LOAD_FAST                'isclass'
              152  LOAD_FAST                'obj'
              154  CALL_FUNCTION_1       1  ''
          156_158  POP_JUMP_IF_FALSE   316  'to 316'
              160  LOAD_FAST                'self'
              162  LOAD_ATTR                _recurse
          164_166  POP_JUMP_IF_FALSE   316  'to 316'

 L.  88       168  LOAD_FAST                'obj'
              170  LOAD_ATTR                __dict__
              172  LOAD_METHOD              items
              174  CALL_METHOD_0         0  ''
              176  GET_ITER         
            178_0  COME_FROM           278  '278'
            178_1  COME_FROM           266  '266'
              178  FOR_ITER            316  'to 316'
              180  UNPACK_SEQUENCE_2     2 
              182  STORE_FAST               'valname'
              184  STORE_FAST               'val'

 L.  90       186  LOAD_GLOBAL              isinstance
              188  LOAD_FAST                'val'
              190  LOAD_GLOBAL              staticmethod
              192  CALL_FUNCTION_2       2  ''
              194  POP_JUMP_IF_FALSE   206  'to 206'

 L.  91       196  LOAD_GLOBAL              getattr
              198  LOAD_FAST                'obj'
              200  LOAD_FAST                'valname'
              202  CALL_FUNCTION_2       2  ''
              204  STORE_FAST               'val'
            206_0  COME_FROM           194  '194'

 L.  92       206  LOAD_GLOBAL              isinstance
              208  LOAD_FAST                'val'
              210  LOAD_GLOBAL              classmethod
              212  CALL_FUNCTION_2       2  ''
              214  POP_JUMP_IF_FALSE   228  'to 228'

 L.  93       216  LOAD_GLOBAL              getattr
              218  LOAD_FAST                'obj'
              220  LOAD_FAST                'valname'
              222  CALL_FUNCTION_2       2  ''
              224  LOAD_ATTR                __func__
              226  STORE_FAST               'val'
            228_0  COME_FROM           214  '214'

 L.  96       228  LOAD_FAST                'isfunction'
              230  LOAD_FAST                'val'
              232  CALL_FUNCTION_1       1  ''
          234_236  POP_JUMP_IF_TRUE    268  'to 268'
              238  LOAD_FAST                'isclass'
              240  LOAD_FAST                'val'
              242  CALL_FUNCTION_1       1  ''
          244_246  POP_JUMP_IF_TRUE    268  'to 268'

 L.  97       248  LOAD_FAST                'ismethod'
              250  LOAD_FAST                'val'
              252  CALL_FUNCTION_1       1  ''

 L.  96   254_256  POP_JUMP_IF_TRUE    268  'to 268'

 L.  97       258  LOAD_GLOBAL              isinstance
              260  LOAD_FAST                'val'
              262  LOAD_GLOBAL              property
              264  CALL_FUNCTION_2       2  ''

 L.  96       266  POP_JUMP_IF_FALSE   178  'to 178'
            268_0  COME_FROM           254  '254'
            268_1  COME_FROM           244  '244'
            268_2  COME_FROM           234  '234'

 L.  98       268  LOAD_FAST                'self'
              270  LOAD_METHOD              _from_module
              272  LOAD_FAST                'module'
              274  LOAD_FAST                'val'
              276  CALL_METHOD_2         2  ''

 L.  96       278  POP_JUMP_IF_FALSE   178  'to 178'

 L.  99       280  LOAD_STR                 '%s.%s'
              282  LOAD_FAST                'name'
              284  LOAD_FAST                'valname'
              286  BUILD_TUPLE_2         2 
              288  BINARY_MODULO    
              290  STORE_FAST               'valname'

 L. 100       292  LOAD_FAST                'self'
              294  LOAD_METHOD              _find
              296  LOAD_FAST                'tests'
              298  LOAD_FAST                'val'
              300  LOAD_FAST                'valname'
              302  LOAD_FAST                'module'
              304  LOAD_FAST                'source_lines'

 L. 101       306  LOAD_FAST                'globs'
              308  LOAD_FAST                'seen'

 L. 100       310  CALL_METHOD_7         7  ''
              312  POP_TOP          
              314  JUMP_BACK           178  'to 178'
            316_0  COME_FROM           164  '164'
            316_1  COME_FROM           156  '156'

Parse error at or near `COME_FROM' instruction at offset 316_0


class NumpyOutputChecker(doctest.OutputChecker):

    def check_output--- This code section failed: ---

 L. 109         0  LOAD_GLOBAL              doctest
                2  LOAD_ATTR                OutputChecker
                4  LOAD_METHOD              check_output
                6  LOAD_FAST                'self'
                8  LOAD_FAST                'want'
               10  LOAD_FAST                'got'

 L. 110        12  LOAD_FAST                'optionflags'

 L. 109        14  CALL_METHOD_4         4  ''
               16  STORE_FAST               'ret'

 L. 111        18  LOAD_FAST                'ret'
               20  POP_JUMP_IF_TRUE    118  'to 118'

 L. 112        22  LOAD_STR                 '#random'
               24  LOAD_FAST                'want'
               26  <118>                 0  ''
               28  POP_JUMP_IF_FALSE    34  'to 34'

 L. 113        30  LOAD_CONST               True
               32  RETURN_VALUE     
             34_0  COME_FROM            28  '28'

 L. 119        34  LOAD_FAST                'got'
               36  LOAD_METHOD              replace
               38  LOAD_STR                 "'>"
               40  LOAD_STR                 "'<"
               42  CALL_METHOD_2         2  ''
               44  STORE_FAST               'got'

 L. 120        46  LOAD_FAST                'want'
               48  LOAD_METHOD              replace
               50  LOAD_STR                 "'>"
               52  LOAD_STR                 "'<"
               54  CALL_METHOD_2         2  ''
               56  STORE_FAST               'want'

 L. 123        58  LOAD_CONST               (4, 8)
               60  GET_ITER         
               62  FOR_ITER            100  'to 100'
               64  STORE_FAST               'sz'

 L. 124        66  LOAD_FAST                'got'
               68  LOAD_METHOD              replace
               70  LOAD_STR                 "'<i%d'"
               72  LOAD_FAST                'sz'
               74  BINARY_MODULO    
               76  LOAD_STR                 'int'
               78  CALL_METHOD_2         2  ''
               80  STORE_FAST               'got'

 L. 125        82  LOAD_FAST                'want'
               84  LOAD_METHOD              replace
               86  LOAD_STR                 "'<i%d'"
               88  LOAD_FAST                'sz'
               90  BINARY_MODULO    
               92  LOAD_STR                 'int'
               94  CALL_METHOD_2         2  ''
               96  STORE_FAST               'want'
               98  JUMP_BACK            62  'to 62'

 L. 127       100  LOAD_GLOBAL              doctest
              102  LOAD_ATTR                OutputChecker
              104  LOAD_METHOD              check_output
              106  LOAD_FAST                'self'
              108  LOAD_FAST                'want'

 L. 128       110  LOAD_FAST                'got'
              112  LOAD_FAST                'optionflags'

 L. 127       114  CALL_METHOD_4         4  ''
              116  STORE_FAST               'ret'
            118_0  COME_FROM            20  '20'

 L. 130       118  LOAD_FAST                'ret'
              120  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 26


class NumpyDocTestCase(npd.DocTestCase):

    def __init__(self, test, optionflags=0, setUp=None, tearDown=None, checker=None, obj=None, result_var='_'):
        self._result_var = result_var
        self._nose_obj = obj
        doctest.DocTestCase.__init__(self, test, optionflags=optionflags,
          setUp=setUp,
          tearDown=tearDown,
          checker=checker)


print_state = numpy.get_printoptions()

class NumpyDoctest(npd.Doctest):
    name = 'numpydoctest'
    score = 1000
    doctest_optflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest_ignore = [
     'generate_numpy_api.py',
     'setup.py']
    doctest_case_class = NumpyDocTestCase
    out_check_class = NumpyOutputChecker
    test_finder_class = NumpyDocTestFinder

    def options(self, parser, env=os.environ):
        Plugin.options(self, parser, env)
        self.doctest_tests = True
        self.doctest_result_var = None

    def configure(self, options, config):
        Plugin.configure(self, options, config)
        self.finder = self.test_finder_class()
        self.parser = doctest.DocTestParser()
        if self.enabled:
            config.plugins.plugins = [p for p in config.plugins.plugins if p.name != 'doctest']

    def set_test_context--- This code section failed: ---

 L. 207         0  LOAD_GLOBAL              get_package_name
                2  LOAD_GLOBAL              os
                4  LOAD_ATTR                path
                6  LOAD_METHOD              dirname
                8  LOAD_FAST                'test'
               10  LOAD_ATTR                filename
               12  CALL_METHOD_1         1  ''
               14  CALL_FUNCTION_1       1  ''
               16  STORE_FAST               'pkg_name'

 L. 217        18  LOAD_GLOBAL              __builtins__

 L. 218        20  LOAD_STR                 '__main__'

 L. 219        22  LOAD_STR                 '__main__'

 L. 220        24  LOAD_GLOBAL              numpy

 L. 217        26  LOAD_CONST               ('__builtins__', '__file__', '__name__', 'np')
               28  BUILD_CONST_KEY_MAP_4     4 
               30  LOAD_FAST                'test'
               32  STORE_ATTR               globs

 L. 222        34  LOAD_STR                 'scipy'
               36  LOAD_FAST                'pkg_name'
               38  <118>                 0  ''
               40  POP_JUMP_IF_FALSE    84  'to 84'

 L. 223        42  LOAD_FAST                'pkg_name'
               44  LOAD_METHOD              split
               46  LOAD_STR                 '.'
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'p'

 L. 224        52  LOAD_FAST                'p'
               54  LOAD_CONST               -1
               56  BINARY_SUBSCR    
               58  STORE_FAST               'p2'

 L. 225        60  LOAD_GLOBAL              __import__
               62  LOAD_FAST                'pkg_name'
               64  LOAD_FAST                'test'
               66  LOAD_ATTR                globs
               68  BUILD_MAP_0           0 
               70  LOAD_FAST                'p2'
               72  BUILD_LIST_1          1 
               74  CALL_FUNCTION_4       4  ''
               76  LOAD_FAST                'test'
               78  LOAD_ATTR                globs
               80  LOAD_FAST                'p2'
               82  STORE_SUBSCR     
             84_0  COME_FROM            40  '40'

Parse error at or near `<118>' instruction at offset 38

    def loadTestsFromModule--- This code section failed: ---

 L. 231         0  LOAD_FAST                'self'
                2  LOAD_METHOD              matches
                4  LOAD_FAST                'module'
                6  LOAD_ATTR                __name__
                8  CALL_METHOD_1         1  ''
               10  POP_JUMP_IF_TRUE     30  'to 30'

 L. 232        12  LOAD_GLOBAL              npd
               14  LOAD_ATTR                log
               16  LOAD_METHOD              debug
               18  LOAD_STR                 "Doctest doesn't want module %s"
               20  LOAD_FAST                'module'
               22  CALL_METHOD_2         2  ''
               24  POP_TOP          

 L. 233        26  LOAD_CONST               None
               28  RETURN_VALUE     
             30_0  COME_FROM            10  '10'

 L. 234        30  SETUP_FINALLY        48  'to 48'

 L. 235        32  LOAD_FAST                'self'
               34  LOAD_ATTR                finder
               36  LOAD_METHOD              find
               38  LOAD_FAST                'module'
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'tests'
               44  POP_BLOCK        
               46  JUMP_FORWARD         68  'to 68'
             48_0  COME_FROM_FINALLY    30  '30'

 L. 236        48  DUP_TOP          
               50  LOAD_GLOBAL              AttributeError
               52  <121>                66  ''
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L. 239        60  POP_EXCEPT       
               62  LOAD_CONST               None
               64  RETURN_VALUE     
               66  <48>             
             68_0  COME_FROM            46  '46'

 L. 240        68  LOAD_FAST                'tests'
               70  POP_JUMP_IF_TRUE     76  'to 76'

 L. 241        72  LOAD_CONST               None
               74  RETURN_VALUE     
             76_0  COME_FROM            70  '70'

 L. 242        76  LOAD_FAST                'tests'
               78  LOAD_METHOD              sort
               80  CALL_METHOD_0         0  ''
               82  POP_TOP          

 L. 243        84  LOAD_GLOBAL              src
               86  LOAD_FAST                'module'
               88  LOAD_ATTR                __file__
               90  CALL_FUNCTION_1       1  ''
               92  STORE_FAST               'module_file'

 L. 244        94  LOAD_FAST                'tests'
               96  GET_ITER         
               98  FOR_ITER            162  'to 162'
              100  STORE_FAST               'test'

 L. 245       102  LOAD_FAST                'test'
              104  LOAD_ATTR                examples
              106  POP_JUMP_IF_TRUE    110  'to 110'

 L. 246       108  JUMP_BACK            98  'to 98'
            110_0  COME_FROM           106  '106'

 L. 247       110  LOAD_FAST                'test'
              112  LOAD_ATTR                filename
              114  POP_JUMP_IF_TRUE    122  'to 122'

 L. 248       116  LOAD_FAST                'module_file'
              118  LOAD_FAST                'test'
              120  STORE_ATTR               filename
            122_0  COME_FROM           114  '114'

 L. 250       122  LOAD_FAST                'self'
              124  LOAD_METHOD              set_test_context
              126  LOAD_FAST                'test'
              128  CALL_METHOD_1         1  ''
              130  POP_TOP          

 L. 251       132  LOAD_FAST                'self'
              134  LOAD_ATTR                doctest_case_class
              136  LOAD_FAST                'test'

 L. 252       138  LOAD_FAST                'self'
              140  LOAD_ATTR                doctest_optflags

 L. 253       142  LOAD_FAST                'self'
              144  LOAD_METHOD              out_check_class
              146  CALL_METHOD_0         0  ''

 L. 254       148  LOAD_FAST                'self'
              150  LOAD_ATTR                doctest_result_var

 L. 251       152  LOAD_CONST               ('optionflags', 'checker', 'result_var')
              154  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              156  YIELD_VALUE      
              158  POP_TOP          
              160  JUMP_BACK            98  'to 98'

Parse error at or near `<121>' instruction at offset 52

    def afterContext--- This code section failed: ---

 L. 259         0  LOAD_GLOBAL              numpy
                2  LOAD_ATTR                set_printoptions
                4  BUILD_TUPLE_0         0 
                6  BUILD_MAP_0           0 
                8  LOAD_GLOBAL              print_state
               10  <164>                 1  ''
               12  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               14  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def wantFile--- This code section failed: ---

 L. 263         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              basename
                6  LOAD_FAST                'file'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'bn'

 L. 264        12  LOAD_FAST                'bn'
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                doctest_ignore
               18  <118>                 0  ''
               20  POP_JUMP_IF_FALSE    26  'to 26'

 L. 265        22  LOAD_CONST               False
               24  RETURN_VALUE     
             26_0  COME_FROM            20  '20'

 L. 266        26  LOAD_GLOBAL              npd
               28  LOAD_ATTR                Doctest
               30  LOAD_METHOD              wantFile
               32  LOAD_FAST                'self'
               34  LOAD_FAST                'file'
               36  CALL_METHOD_2         2  ''
               38  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 18


class Unplugger:
    __doc__ = ' Nose plugin to remove named plugin late in loading\n\n    By default it removes the "doctest" plugin.\n    '
    name = 'unplugger'
    enabled = True
    score = 4000

    def __init__(self, to_unplug='doctest'):
        self.to_unplug = to_unplug

    def options(self, parser, env):
        pass

    def configure(self, options, config):
        config.plugins.plugins = [p for p in config.plugins.plugins if p.name != self.to_unplug]


class KnownFailurePlugin(ErrorClassPlugin):
    __doc__ = "Plugin that installs a KNOWNFAIL error class for the\n    KnownFailureClass exception.  When KnownFailure is raised,\n    the exception will be logged in the knownfail attribute of the\n    result, 'K' or 'KNOWNFAIL' (verbose) will be output, and the\n    exception will not be counted as an error or failure."
    enabled = True
    knownfail = ErrorClass(KnownFailureException, label='KNOWNFAIL',
      isfailure=False)

    def options(self, parser, env=os.environ):
        env_opt = 'NOSE_WITHOUT_KNOWNFAIL'
        parser.add_option('--no-knownfail', action='store_true', dest='noKnownFail',
          default=(env.getenv_optFalse),
          help='Disable special handling of KnownFailure exceptions')

    def configure(self, options, conf):
        if not self.can_configure:
            return
        self.conf = conf
        disable = getattr(options, 'noKnownFail', False)
        if disable:
            self.enabled = False


KnownFailure = KnownFailurePlugin

class FPUModeCheckPlugin(Plugin):
    __doc__ = '\n    Plugin that checks the FPU mode before and after each test,\n    raising failures if the test changed the mode.\n    '

    def prepareTestCase(self, test):
        from numpy.core._multiarray_tests import get_fpu_mode

        def run--- This code section failed: ---

 L. 329         0  LOAD_DEREF               'get_fpu_mode'
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'old_mode'

 L. 330         6  LOAD_DEREF               'test'
                8  LOAD_METHOD              test
               10  LOAD_FAST                'result'
               12  CALL_METHOD_1         1  ''
               14  POP_TOP          

 L. 331        16  LOAD_DEREF               'get_fpu_mode'
               18  CALL_FUNCTION_0       0  ''
               20  STORE_FAST               'new_mode'

 L. 333        22  LOAD_FAST                'old_mode'
               24  LOAD_FAST                'new_mode'
               26  COMPARE_OP               !=
               28  POP_JUMP_IF_FALSE    86  'to 86'

 L. 334        30  SETUP_FINALLY        52  'to 52'

 L. 335        32  LOAD_GLOBAL              AssertionError

 L. 336        34  LOAD_STR                 'FPU mode changed from {0:#x} to {1:#x} during the test'
               36  LOAD_METHOD              format

 L. 337        38  LOAD_FAST                'old_mode'
               40  LOAD_FAST                'new_mode'

 L. 336        42  CALL_METHOD_2         2  ''

 L. 335        44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
               48  POP_BLOCK        
               50  JUMP_FORWARD         86  'to 86'
             52_0  COME_FROM_FINALLY    30  '30'

 L. 338        52  DUP_TOP          
               54  LOAD_GLOBAL              AssertionError
               56  <121>                84  ''
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L. 339        64  LOAD_FAST                'result'
               66  LOAD_METHOD              addFailure
               68  LOAD_DEREF               'test'
               70  LOAD_GLOBAL              sys
               72  LOAD_METHOD              exc_info
               74  CALL_METHOD_0         0  ''
               76  CALL_METHOD_2         2  ''
               78  POP_TOP          
               80  POP_EXCEPT       
               82  JUMP_FORWARD         86  'to 86'
               84  <48>             
             86_0  COME_FROM            82  '82'
             86_1  COME_FROM            50  '50'
             86_2  COME_FROM            28  '28'

Parse error at or near `<121>' instruction at offset 56

        return run


class NumpyTestProgram(nose.core.TestProgram):

    def runTests--- This code section failed: ---

 L. 355         0  LOAD_FAST                'self'
                2  LOAD_ATTR                testRunner
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    40  'to 40'

 L. 356        10  LOAD_GLOBAL              nose
               12  LOAD_ATTR                core
               14  LOAD_ATTR                TextTestRunner
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                config
               20  LOAD_ATTR                stream

 L. 357        22  LOAD_FAST                'self'
               24  LOAD_ATTR                config
               26  LOAD_ATTR                verbosity

 L. 358        28  LOAD_FAST                'self'
               30  LOAD_ATTR                config

 L. 356        32  LOAD_CONST               ('stream', 'verbosity', 'config')
               34  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               36  LOAD_FAST                'self'
               38  STORE_ATTR               testRunner
             40_0  COME_FROM             8  '8'

 L. 359        40  LOAD_FAST                'self'
               42  LOAD_ATTR                config
               44  LOAD_ATTR                plugins
               46  LOAD_METHOD              prepareTestRunner
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                testRunner
               52  CALL_METHOD_1         1  ''
               54  STORE_FAST               'plug_runner'

 L. 360        56  LOAD_FAST                'plug_runner'
               58  LOAD_CONST               None
               60  <117>                 1  ''
               62  POP_JUMP_IF_FALSE    70  'to 70'

 L. 361        64  LOAD_FAST                'plug_runner'
               66  LOAD_FAST                'self'
               68  STORE_ATTR               testRunner
             70_0  COME_FROM            62  '62'

 L. 362        70  LOAD_FAST                'self'
               72  LOAD_ATTR                testRunner
               74  LOAD_METHOD              run
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                test
               80  CALL_METHOD_1         1  ''
               82  LOAD_FAST                'self'
               84  STORE_ATTR               result

 L. 363        86  LOAD_FAST                'self'
               88  LOAD_ATTR                result
               90  LOAD_METHOD              wasSuccessful
               92  CALL_METHOD_0         0  ''
               94  LOAD_FAST                'self'
               96  STORE_ATTR               success

 L. 364        98  LOAD_FAST                'self'
              100  LOAD_ATTR                success
              102  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1