# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: unittest\main.py
"""Unittest main program"""
import sys, argparse, os
from . import loader, runner
from .signals import installHandler
__unittest = True
MAIN_EXAMPLES = 'Examples:\n  %(prog)s test_module               - run tests from test_module\n  %(prog)s module.TestClass          - run tests from module.TestClass\n  %(prog)s module.Class.test_method  - run specified test method\n  %(prog)s path/to/test_file.py      - run tests from test_file.py\n'
MODULE_EXAMPLES = "Examples:\n  %(prog)s                           - run default set of tests\n  %(prog)s MyTestSuite               - run suite 'MyTestSuite'\n  %(prog)s MyTestCase.testSomething  - run MyTestCase.testSomething\n  %(prog)s MyTestCase                - run all 'test*' test methods\n                                       in MyTestCase\n"

def _convert_name(name):
    if os.path.isfile(name):
        if name.lower().endswith('.py'):
            if os.path.isabs(name):
                rel_path = os.path.relpath(name, os.getcwd())
                if os.path.isabs(rel_path) or rel_path.startswith(os.pardir):
                    return name
                name = rel_path
            return name[:-3].replace('\\', '.').replace('/', '.')
    return name


def _convert_names(names):
    return [_convert_name(name) for name in names]


def _convert_select_pattern--- This code section failed: ---

 L.  50         0  LOAD_STR                 '*'
                2  LOAD_FAST                'pattern'
                4  <118>                 1  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.  51         8  LOAD_STR                 '*%s*'
               10  LOAD_FAST                'pattern'
               12  BINARY_MODULO    
               14  STORE_FAST               'pattern'
             16_0  COME_FROM             6  '6'

 L.  52        16  LOAD_FAST                'pattern'
               18  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class TestProgram(object):
    __doc__ = 'A command-line program that runs a set of tests; this is primarily\n       for making test modules conveniently executable.\n    '
    module = None
    verbosity = 1
    failfast = catchbreak = buffer = progName = warnings = testNamePatterns = None
    _discovery_parser = None

    def __init__--- This code section failed: ---

 L.  69         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'module'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    60  'to 60'

 L.  70        10  LOAD_GLOBAL              __import__
               12  LOAD_FAST                'module'
               14  CALL_FUNCTION_1       1  ''
               16  LOAD_FAST                'self'
               18  STORE_ATTR               module

 L.  71        20  LOAD_FAST                'module'
               22  LOAD_METHOD              split
               24  LOAD_STR                 '.'
               26  CALL_METHOD_1         1  ''
               28  LOAD_CONST               1
               30  LOAD_CONST               None
               32  BUILD_SLICE_2         2 
               34  BINARY_SUBSCR    
               36  GET_ITER         
               38  FOR_ITER             58  'to 58'
               40  STORE_FAST               'part'

 L.  72        42  LOAD_GLOBAL              getattr
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                module
               48  LOAD_FAST                'part'
               50  CALL_FUNCTION_2       2  ''
               52  LOAD_FAST                'self'
               54  STORE_ATTR               module
               56  JUMP_BACK            38  'to 38'
               58  JUMP_FORWARD         66  'to 66'
             60_0  COME_FROM             8  '8'

 L.  74        60  LOAD_FAST                'module'
               62  LOAD_FAST                'self'
               64  STORE_ATTR               module
             66_0  COME_FROM            58  '58'

 L.  75        66  LOAD_FAST                'argv'
               68  LOAD_CONST               None
               70  <117>                 0  ''
               72  POP_JUMP_IF_FALSE    80  'to 80'

 L.  76        74  LOAD_GLOBAL              sys
               76  LOAD_ATTR                argv
               78  STORE_FAST               'argv'
             80_0  COME_FROM            72  '72'

 L.  78        80  LOAD_FAST                'exit'
               82  LOAD_FAST                'self'
               84  STORE_ATTR               exit

 L.  79        86  LOAD_FAST                'failfast'
               88  LOAD_FAST                'self'
               90  STORE_ATTR               failfast

 L.  80        92  LOAD_FAST                'catchbreak'
               94  LOAD_FAST                'self'
               96  STORE_ATTR               catchbreak

 L.  81        98  LOAD_FAST                'verbosity'
              100  LOAD_FAST                'self'
              102  STORE_ATTR               verbosity

 L.  82       104  LOAD_FAST                'buffer'
              106  LOAD_FAST                'self'
              108  STORE_ATTR               buffer

 L.  83       110  LOAD_FAST                'tb_locals'
              112  LOAD_FAST                'self'
              114  STORE_ATTR               tb_locals

 L.  84       116  LOAD_FAST                'warnings'
              118  LOAD_CONST               None
              120  <117>                 0  ''
              122  POP_JUMP_IF_FALSE   138  'to 138'
              124  LOAD_GLOBAL              sys
              126  LOAD_ATTR                warnoptions
              128  POP_JUMP_IF_TRUE    138  'to 138'

 L.  88       130  LOAD_STR                 'default'
              132  LOAD_FAST                'self'
              134  STORE_ATTR               warnings
              136  JUMP_FORWARD        144  'to 144'
            138_0  COME_FROM           128  '128'
            138_1  COME_FROM           122  '122'

 L.  95       138  LOAD_FAST                'warnings'
              140  LOAD_FAST                'self'
              142  STORE_ATTR               warnings
            144_0  COME_FROM           136  '136'

 L.  96       144  LOAD_FAST                'defaultTest'
              146  LOAD_FAST                'self'
              148  STORE_ATTR               defaultTest

 L.  97       150  LOAD_FAST                'testRunner'
              152  LOAD_FAST                'self'
              154  STORE_ATTR               testRunner

 L.  98       156  LOAD_FAST                'testLoader'
              158  LOAD_FAST                'self'
              160  STORE_ATTR               testLoader

 L.  99       162  LOAD_GLOBAL              os
              164  LOAD_ATTR                path
              166  LOAD_METHOD              basename
              168  LOAD_FAST                'argv'
              170  LOAD_CONST               0
              172  BINARY_SUBSCR    
              174  CALL_METHOD_1         1  ''
              176  LOAD_FAST                'self'
              178  STORE_ATTR               progName

 L. 100       180  LOAD_FAST                'self'
              182  LOAD_METHOD              parseArgs
              184  LOAD_FAST                'argv'
              186  CALL_METHOD_1         1  ''
              188  POP_TOP          

 L. 101       190  LOAD_FAST                'self'
              192  LOAD_METHOD              runTests
              194  CALL_METHOD_0         0  ''
              196  POP_TOP          

Parse error at or near `<117>' instruction at offset 70

    def usageExit--- This code section failed: ---

 L. 104         0  LOAD_FAST                'msg'
                2  POP_JUMP_IF_FALSE    12  'to 12'

 L. 105         4  LOAD_GLOBAL              print
                6  LOAD_FAST                'msg'
                8  CALL_FUNCTION_1       1  ''
               10  POP_TOP          
             12_0  COME_FROM             2  '2'

 L. 106        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _discovery_parser
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    30  'to 30'

 L. 107        22  LOAD_FAST                'self'
               24  LOAD_METHOD              _initArgParsers
               26  CALL_METHOD_0         0  ''
               28  POP_TOP          
             30_0  COME_FROM            20  '20'

 L. 108        30  LOAD_FAST                'self'
               32  LOAD_METHOD              _print_help
               34  CALL_METHOD_0         0  ''
               36  POP_TOP          

 L. 109        38  LOAD_GLOBAL              sys
               40  LOAD_METHOD              exit
               42  LOAD_CONST               2
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          

Parse error at or near `<117>' instruction at offset 18

    def _print_help--- This code section failed: ---

 L. 112         0  LOAD_FAST                'self'
                2  LOAD_ATTR                module
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    54  'to 54'

 L. 113        10  LOAD_GLOBAL              print
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                _main_parser
               16  LOAD_METHOD              format_help
               18  CALL_METHOD_0         0  ''
               20  CALL_FUNCTION_1       1  ''
               22  POP_TOP          

 L. 114        24  LOAD_GLOBAL              print
               26  LOAD_GLOBAL              MAIN_EXAMPLES
               28  LOAD_STR                 'prog'
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                progName
               34  BUILD_MAP_1           1 
               36  BINARY_MODULO    
               38  CALL_FUNCTION_1       1  ''
               40  POP_TOP          

 L. 115        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _discovery_parser
               46  LOAD_METHOD              print_help
               48  CALL_METHOD_0         0  ''
               50  POP_TOP          
               52  JUMP_FORWARD         86  'to 86'
             54_0  COME_FROM             8  '8'

 L. 117        54  LOAD_GLOBAL              print
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                _main_parser
               60  LOAD_METHOD              format_help
               62  CALL_METHOD_0         0  ''
               64  CALL_FUNCTION_1       1  ''
               66  POP_TOP          

 L. 118        68  LOAD_GLOBAL              print
               70  LOAD_GLOBAL              MODULE_EXAMPLES
               72  LOAD_STR                 'prog'
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                progName
               78  BUILD_MAP_1           1 
               80  BINARY_MODULO    
               82  CALL_FUNCTION_1       1  ''
               84  POP_TOP          
             86_0  COME_FROM            52  '52'

Parse error at or near `None' instruction at offset -1

    def parseArgs--- This code section failed: ---

 L. 121         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _initArgParsers
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 122         8  LOAD_FAST                'self'
               10  LOAD_ATTR                module
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE   112  'to 112'

 L. 123        18  LOAD_GLOBAL              len
               20  LOAD_FAST                'argv'
               22  CALL_FUNCTION_1       1  ''
               24  LOAD_CONST               1
               26  COMPARE_OP               >
               28  POP_JUMP_IF_FALSE    68  'to 68'
               30  LOAD_FAST                'argv'
               32  LOAD_CONST               1
               34  BINARY_SUBSCR    
               36  LOAD_METHOD              lower
               38  CALL_METHOD_0         0  ''
               40  LOAD_STR                 'discover'
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_FALSE    68  'to 68'

 L. 124        46  LOAD_FAST                'self'
               48  LOAD_METHOD              _do_discovery
               50  LOAD_FAST                'argv'
               52  LOAD_CONST               2
               54  LOAD_CONST               None
               56  BUILD_SLICE_2         2 
               58  BINARY_SUBSCR    
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          

 L. 125        64  LOAD_CONST               None
               66  RETURN_VALUE     
             68_0  COME_FROM            44  '44'
             68_1  COME_FROM            28  '28'

 L. 126        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _main_parser
               72  LOAD_METHOD              parse_args
               74  LOAD_FAST                'argv'
               76  LOAD_CONST               1
               78  LOAD_CONST               None
               80  BUILD_SLICE_2         2 
               82  BINARY_SUBSCR    
               84  LOAD_FAST                'self'
               86  CALL_METHOD_2         2  ''
               88  POP_TOP          

 L. 127        90  LOAD_FAST                'self'
               92  LOAD_ATTR                tests
               94  POP_JUMP_IF_TRUE    134  'to 134'

 L. 130        96  LOAD_FAST                'self'
               98  LOAD_METHOD              _do_discovery
              100  BUILD_LIST_0          0 
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          

 L. 131       106  LOAD_CONST               None
              108  RETURN_VALUE     
              110  JUMP_FORWARD        134  'to 134'
            112_0  COME_FROM            16  '16'

 L. 133       112  LOAD_FAST                'self'
              114  LOAD_ATTR                _main_parser
              116  LOAD_METHOD              parse_args
              118  LOAD_FAST                'argv'
              120  LOAD_CONST               1
              122  LOAD_CONST               None
              124  BUILD_SLICE_2         2 
              126  BINARY_SUBSCR    
              128  LOAD_FAST                'self'
              130  CALL_METHOD_2         2  ''
              132  POP_TOP          
            134_0  COME_FROM           110  '110'
            134_1  COME_FROM            94  '94'

 L. 135       134  LOAD_FAST                'self'
              136  LOAD_ATTR                tests
              138  POP_JUMP_IF_FALSE   168  'to 168'

 L. 136       140  LOAD_GLOBAL              _convert_names
              142  LOAD_FAST                'self'
              144  LOAD_ATTR                tests
              146  CALL_FUNCTION_1       1  ''
              148  LOAD_FAST                'self'
              150  STORE_ATTR               testNames

 L. 137       152  LOAD_GLOBAL              __name__
              154  LOAD_STR                 '__main__'
              156  COMPARE_OP               ==
              158  POP_JUMP_IF_FALSE   222  'to 222'

 L. 139       160  LOAD_CONST               None
              162  LOAD_FAST                'self'
              164  STORE_ATTR               module
              166  JUMP_FORWARD        222  'to 222'
            168_0  COME_FROM           138  '138'

 L. 140       168  LOAD_FAST                'self'
              170  LOAD_ATTR                defaultTest
              172  LOAD_CONST               None
              174  <117>                 0  ''
              176  POP_JUMP_IF_FALSE   186  'to 186'

 L. 142       178  LOAD_CONST               None
              180  LOAD_FAST                'self'
              182  STORE_ATTR               testNames
              184  JUMP_FORWARD        222  'to 222'
            186_0  COME_FROM           176  '176'

 L. 143       186  LOAD_GLOBAL              isinstance
              188  LOAD_FAST                'self'
              190  LOAD_ATTR                defaultTest
              192  LOAD_GLOBAL              str
              194  CALL_FUNCTION_2       2  ''
              196  POP_JUMP_IF_FALSE   210  'to 210'

 L. 144       198  LOAD_FAST                'self'
              200  LOAD_ATTR                defaultTest
              202  BUILD_TUPLE_1         1 
              204  LOAD_FAST                'self'
              206  STORE_ATTR               testNames
              208  JUMP_FORWARD        222  'to 222'
            210_0  COME_FROM           196  '196'

 L. 146       210  LOAD_GLOBAL              list
              212  LOAD_FAST                'self'
              214  LOAD_ATTR                defaultTest
              216  CALL_FUNCTION_1       1  ''
              218  LOAD_FAST                'self'
              220  STORE_ATTR               testNames
            222_0  COME_FROM           208  '208'
            222_1  COME_FROM           184  '184'
            222_2  COME_FROM           166  '166'
            222_3  COME_FROM           158  '158'

 L. 147       222  LOAD_FAST                'self'
              224  LOAD_METHOD              createTests
              226  CALL_METHOD_0         0  ''
              228  POP_TOP          

Parse error at or near `<117>' instruction at offset 14

    def createTests--- This code section failed: ---

 L. 150         0  LOAD_FAST                'self'
                2  LOAD_ATTR                testNamePatterns
                4  POP_JUMP_IF_FALSE    16  'to 16'

 L. 151         6  LOAD_FAST                'self'
                8  LOAD_ATTR                testNamePatterns
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                testLoader
               14  STORE_ATTR               testNamePatterns
             16_0  COME_FROM             4  '4'

 L. 152        16  LOAD_FAST                'from_discovery'
               18  POP_JUMP_IF_FALSE    64  'to 64'

 L. 153        20  LOAD_FAST                'Loader'
               22  LOAD_CONST               None
               24  <117>                 0  ''
               26  POP_JUMP_IF_FALSE    34  'to 34'
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                testLoader
               32  JUMP_FORWARD         38  'to 38'
             34_0  COME_FROM            26  '26'
               34  LOAD_FAST                'Loader'
               36  CALL_FUNCTION_0       0  ''
             38_0  COME_FROM            32  '32'
               38  STORE_FAST               'loader'

 L. 154        40  LOAD_FAST                'loader'
               42  LOAD_METHOD              discover
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                start
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                pattern
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                top
               56  CALL_METHOD_3         3  ''
               58  LOAD_FAST                'self'
               60  STORE_ATTR               test
               62  JUMP_FORWARD        112  'to 112'
             64_0  COME_FROM            18  '18'

 L. 155        64  LOAD_FAST                'self'
               66  LOAD_ATTR                testNames
               68  LOAD_CONST               None
               70  <117>                 0  ''
               72  POP_JUMP_IF_FALSE    92  'to 92'

 L. 156        74  LOAD_FAST                'self'
               76  LOAD_ATTR                testLoader
               78  LOAD_METHOD              loadTestsFromModule
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                module
               84  CALL_METHOD_1         1  ''
               86  LOAD_FAST                'self'
               88  STORE_ATTR               test
               90  JUMP_FORWARD        112  'to 112'
             92_0  COME_FROM            72  '72'

 L. 158        92  LOAD_FAST                'self'
               94  LOAD_ATTR                testLoader
               96  LOAD_METHOD              loadTestsFromNames
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                testNames

 L. 159       102  LOAD_FAST                'self'
              104  LOAD_ATTR                module

 L. 158       106  CALL_METHOD_2         2  ''
              108  LOAD_FAST                'self'
              110  STORE_ATTR               test
            112_0  COME_FROM            90  '90'
            112_1  COME_FROM            62  '62'

Parse error at or near `<117>' instruction at offset 24

    def _initArgParsers(self):
        parent_parser = self._getParentArgParser()
        self._main_parser = self._getMainArgParser(parent_parser)
        self._discovery_parser = self._getDiscoveryArgParser(parent_parser)

    def _getParentArgParser--- This code section failed: ---

 L. 167         0  LOAD_GLOBAL              argparse
                2  LOAD_ATTR                ArgumentParser
                4  LOAD_CONST               False
                6  LOAD_CONST               ('add_help',)
                8  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               10  STORE_FAST               'parser'

 L. 169        12  LOAD_FAST                'parser'
               14  LOAD_ATTR                add_argument
               16  LOAD_STR                 '-v'
               18  LOAD_STR                 '--verbose'
               20  LOAD_STR                 'verbosity'

 L. 170        22  LOAD_STR                 'store_const'
               24  LOAD_CONST               2

 L. 171        26  LOAD_STR                 'Verbose output'

 L. 169        28  LOAD_CONST               ('dest', 'action', 'const', 'help')
               30  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
               32  POP_TOP          

 L. 172        34  LOAD_FAST                'parser'
               36  LOAD_ATTR                add_argument
               38  LOAD_STR                 '-q'
               40  LOAD_STR                 '--quiet'
               42  LOAD_STR                 'verbosity'

 L. 173        44  LOAD_STR                 'store_const'
               46  LOAD_CONST               0

 L. 174        48  LOAD_STR                 'Quiet output'

 L. 172        50  LOAD_CONST               ('dest', 'action', 'const', 'help')
               52  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
               54  POP_TOP          

 L. 175        56  LOAD_FAST                'parser'
               58  LOAD_ATTR                add_argument
               60  LOAD_STR                 '--locals'
               62  LOAD_STR                 'tb_locals'

 L. 176        64  LOAD_STR                 'store_true'

 L. 177        66  LOAD_STR                 'Show local variables in tracebacks'

 L. 175        68  LOAD_CONST               ('dest', 'action', 'help')
               70  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               72  POP_TOP          

 L. 178        74  LOAD_FAST                'self'
               76  LOAD_ATTR                failfast
               78  LOAD_CONST               None
               80  <117>                 0  ''
               82  POP_JUMP_IF_FALSE   110  'to 110'

 L. 179        84  LOAD_FAST                'parser'
               86  LOAD_ATTR                add_argument
               88  LOAD_STR                 '-f'
               90  LOAD_STR                 '--failfast'
               92  LOAD_STR                 'failfast'

 L. 180        94  LOAD_STR                 'store_true'

 L. 181        96  LOAD_STR                 'Stop on first fail or error'

 L. 179        98  LOAD_CONST               ('dest', 'action', 'help')
              100  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              102  POP_TOP          

 L. 182       104  LOAD_CONST               False
              106  LOAD_FAST                'self'
              108  STORE_ATTR               failfast
            110_0  COME_FROM            82  '82'

 L. 183       110  LOAD_FAST                'self'
              112  LOAD_ATTR                catchbreak
              114  LOAD_CONST               None
              116  <117>                 0  ''
              118  POP_JUMP_IF_FALSE   146  'to 146'

 L. 184       120  LOAD_FAST                'parser'
              122  LOAD_ATTR                add_argument
              124  LOAD_STR                 '-c'
              126  LOAD_STR                 '--catch'
              128  LOAD_STR                 'catchbreak'

 L. 185       130  LOAD_STR                 'store_true'

 L. 186       132  LOAD_STR                 'Catch Ctrl-C and display results so far'

 L. 184       134  LOAD_CONST               ('dest', 'action', 'help')
              136  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              138  POP_TOP          

 L. 187       140  LOAD_CONST               False
              142  LOAD_FAST                'self'
              144  STORE_ATTR               catchbreak
            146_0  COME_FROM           118  '118'

 L. 188       146  LOAD_FAST                'self'
              148  LOAD_ATTR                buffer
              150  LOAD_CONST               None
              152  <117>                 0  ''
              154  POP_JUMP_IF_FALSE   182  'to 182'

 L. 189       156  LOAD_FAST                'parser'
              158  LOAD_ATTR                add_argument
              160  LOAD_STR                 '-b'
              162  LOAD_STR                 '--buffer'
              164  LOAD_STR                 'buffer'

 L. 190       166  LOAD_STR                 'store_true'

 L. 191       168  LOAD_STR                 'Buffer stdout and stderr during tests'

 L. 189       170  LOAD_CONST               ('dest', 'action', 'help')
              172  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              174  POP_TOP          

 L. 192       176  LOAD_CONST               False
              178  LOAD_FAST                'self'
              180  STORE_ATTR               buffer
            182_0  COME_FROM           154  '154'

 L. 193       182  LOAD_FAST                'self'
              184  LOAD_ATTR                testNamePatterns
              186  LOAD_CONST               None
              188  <117>                 0  ''
              190  POP_JUMP_IF_FALSE   218  'to 218'

 L. 194       192  LOAD_FAST                'parser'
              194  LOAD_ATTR                add_argument
              196  LOAD_STR                 '-k'
              198  LOAD_STR                 'testNamePatterns'

 L. 195       200  LOAD_STR                 'append'
              202  LOAD_GLOBAL              _convert_select_pattern

 L. 196       204  LOAD_STR                 'Only run tests which match the given substring'

 L. 194       206  LOAD_CONST               ('dest', 'action', 'type', 'help')
              208  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              210  POP_TOP          

 L. 197       212  BUILD_LIST_0          0 
              214  LOAD_FAST                'self'
              216  STORE_ATTR               testNamePatterns
            218_0  COME_FROM           190  '190'

 L. 199       218  LOAD_FAST                'parser'
              220  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 80

    def _getMainArgParser(self, parent):
        parser = argparse.ArgumentParser(parents=[parent])
        parser.prog = self.progName
        parser.print_help = self._print_help
        parser.add_argument('tests', nargs='*', help='a list of any number of test modules, classes and test methods.')
        return parser

    def _getDiscoveryArgParser(self, parent):
        parser = argparse.ArgumentParser(parents=[parent])
        parser.prog = '%s discover' % self.progName
        parser.epilog = 'For test discovery all test modules must be importable from the top level directory of the project.'
        parser.add_argument('-s', '--start-directory', dest='start', help="Directory to start discovery ('.' default)")
        parser.add_argument('-p', '--pattern', dest='pattern', help="Pattern to match tests ('test*.py' default)")
        parser.add_argument('-t', '--top-level-directory', dest='top', help='Top level directory of project (defaults to start directory)')
        for arg in ('start', 'pattern', 'top'):
            parser.add_argument(arg, nargs='?', default=(argparse.SUPPRESS),
              help=(argparse.SUPPRESS))
        else:
            return parser

    def _do_discovery--- This code section failed: ---

 L. 234         0  LOAD_STR                 '.'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               start

 L. 235         6  LOAD_STR                 'test*.py'
                8  LOAD_FAST                'self'
               10  STORE_ATTR               pattern

 L. 236        12  LOAD_CONST               None
               14  LOAD_FAST                'self'
               16  STORE_ATTR               top

 L. 237        18  LOAD_FAST                'argv'
               20  LOAD_CONST               None
               22  <117>                 1  ''
               24  POP_JUMP_IF_FALSE    58  'to 58'

 L. 239        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _discovery_parser
               30  LOAD_CONST               None
               32  <117>                 0  ''
               34  POP_JUMP_IF_FALSE    44  'to 44'

 L. 241        36  LOAD_FAST                'self'
               38  LOAD_METHOD              _initArgParsers
               40  CALL_METHOD_0         0  ''
               42  POP_TOP          
             44_0  COME_FROM            34  '34'

 L. 242        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _discovery_parser
               48  LOAD_METHOD              parse_args
               50  LOAD_FAST                'argv'
               52  LOAD_FAST                'self'
               54  CALL_METHOD_2         2  ''
               56  POP_TOP          
             58_0  COME_FROM            24  '24'

 L. 244        58  LOAD_FAST                'self'
               60  LOAD_ATTR                createTests
               62  LOAD_CONST               True
               64  LOAD_FAST                'Loader'
               66  LOAD_CONST               ('from_discovery', 'Loader')
               68  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               70  POP_TOP          

Parse error at or near `<117>' instruction at offset 22

    def runTests--- This code section failed: ---

 L. 247         0  LOAD_FAST                'self'
                2  LOAD_ATTR                catchbreak
                4  POP_JUMP_IF_FALSE    12  'to 12'

 L. 248         6  LOAD_GLOBAL              installHandler
                8  CALL_FUNCTION_0       0  ''
               10  POP_TOP          
             12_0  COME_FROM             4  '4'

 L. 249        12  LOAD_FAST                'self'
               14  LOAD_ATTR                testRunner
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    30  'to 30'

 L. 250        22  LOAD_GLOBAL              runner
               24  LOAD_ATTR                TextTestRunner
               26  LOAD_FAST                'self'
               28  STORE_ATTR               testRunner
             30_0  COME_FROM            20  '20'

 L. 251        30  LOAD_GLOBAL              isinstance
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                testRunner
               36  LOAD_GLOBAL              type
               38  CALL_FUNCTION_2       2  ''
               40  POP_JUMP_IF_FALSE   156  'to 156'

 L. 252        42  SETUP_FINALLY       128  'to 128'

 L. 253        44  SETUP_FINALLY        80  'to 80'

 L. 254        46  LOAD_FAST                'self'
               48  LOAD_ATTR                testRunner
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                verbosity

 L. 255        54  LOAD_FAST                'self'
               56  LOAD_ATTR                failfast

 L. 256        58  LOAD_FAST                'self'
               60  LOAD_ATTR                buffer

 L. 257        62  LOAD_FAST                'self'
               64  LOAD_ATTR                warnings

 L. 258        66  LOAD_FAST                'self'
               68  LOAD_ATTR                tb_locals

 L. 254        70  LOAD_CONST               ('verbosity', 'failfast', 'buffer', 'warnings', 'tb_locals')
               72  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               74  STORE_FAST               'testRunner'
               76  POP_BLOCK        
               78  JUMP_FORWARD        124  'to 124'
             80_0  COME_FROM_FINALLY    44  '44'

 L. 259        80  DUP_TOP          
               82  LOAD_GLOBAL              TypeError
               84  <121>               122  ''
               86  POP_TOP          
               88  POP_TOP          
               90  POP_TOP          

 L. 261        92  LOAD_FAST                'self'
               94  LOAD_ATTR                testRunner
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                verbosity

 L. 262       100  LOAD_FAST                'self'
              102  LOAD_ATTR                failfast

 L. 263       104  LOAD_FAST                'self'
              106  LOAD_ATTR                buffer

 L. 264       108  LOAD_FAST                'self'
              110  LOAD_ATTR                warnings

 L. 261       112  LOAD_CONST               ('verbosity', 'failfast', 'buffer', 'warnings')
              114  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              116  STORE_FAST               'testRunner'
              118  POP_EXCEPT       
              120  JUMP_FORWARD        124  'to 124'
              122  <48>             
            124_0  COME_FROM           120  '120'
            124_1  COME_FROM            78  '78'
              124  POP_BLOCK        
              126  JUMP_ABSOLUTE       162  'to 162'
            128_0  COME_FROM_FINALLY    42  '42'

 L. 265       128  DUP_TOP          
              130  LOAD_GLOBAL              TypeError
              132  <121>               152  ''
              134  POP_TOP          
              136  POP_TOP          
              138  POP_TOP          

 L. 267       140  LOAD_FAST                'self'
              142  LOAD_METHOD              testRunner
              144  CALL_METHOD_0         0  ''
              146  STORE_FAST               'testRunner'
              148  POP_EXCEPT       
              150  JUMP_ABSOLUTE       162  'to 162'
              152  <48>             
              154  JUMP_FORWARD        162  'to 162'
            156_0  COME_FROM            40  '40'

 L. 270       156  LOAD_FAST                'self'
              158  LOAD_ATTR                testRunner
              160  STORE_FAST               'testRunner'
            162_0  COME_FROM_EXCEPT_CLAUSE   154  '154'
            162_1  COME_FROM_EXCEPT_CLAUSE   150  '150'

 L. 271       162  LOAD_FAST                'testRunner'
              164  LOAD_METHOD              run
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                test
              170  CALL_METHOD_1         1  ''
              172  LOAD_FAST                'self'
              174  STORE_ATTR               result

 L. 272       176  LOAD_FAST                'self'
              178  LOAD_ATTR                exit
              180  POP_JUMP_IF_FALSE   200  'to 200'

 L. 273       182  LOAD_GLOBAL              sys
              184  LOAD_METHOD              exit
              186  LOAD_FAST                'self'
              188  LOAD_ATTR                result
              190  LOAD_METHOD              wasSuccessful
              192  CALL_METHOD_0         0  ''
              194  UNARY_NOT        
              196  CALL_METHOD_1         1  ''
              198  POP_TOP          
            200_0  COME_FROM           180  '180'

Parse error at or near `<117>' instruction at offset 18


main = TestProgram