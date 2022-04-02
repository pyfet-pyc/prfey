# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: numpy\_pytesttester.py
"""
Pytest test running.

This module implements the ``test()`` function for NumPy modules. The usual
boiler plate for doing that is to put the following in the module
``__init__.py`` file::

    from numpy._pytesttester import PytestTester
    test = PytestTester(__name__).test
    del PytestTester

Warnings filtering and other runtime settings should be dealt with in the
``pytest.ini`` file in the numpy repo root. The behavior of the test depends on
whether or not that file is found as follows:

* ``pytest.ini`` is present (develop mode)
    All warnings except those explicitly filtered out are raised as error.
* ``pytest.ini`` is absent (release mode)
    DeprecationWarnings and PendingDeprecationWarnings are ignored, other
    warnings are passed through.

In practice, tests run from the numpy repo are run in develop mode. That
includes the standard ``python runtests.py`` invocation.

This module is imported by every numpy subpackage, so lies at the top level to
simplify circular import issues. For the same reason, it contains no numpy
imports at module scope, instead importing numpy within function calls.
"""
import sys, os
__all__ = [
 'PytestTester']

def _show_numpy_info():
    import numpy as np
    print('NumPy version %s' % np.__version__)
    relaxed_strides = np.ones((10, 1), order='C').flags.f_contiguous
    print('NumPy relaxed strides checking option:', relaxed_strides)


class PytestTester:
    __doc__ = "\n    Pytest test runner.\n\n    A test function is typically added to a package's __init__.py like so::\n\n      from numpy._pytesttester import PytestTester\n      test = PytestTester(__name__).test\n      del PytestTester\n\n    Calling this test function finds and runs all tests associated with the\n    module and all its sub-modules.\n\n    Attributes\n    ----------\n    module_name : str\n        Full path to the package to test.\n\n    Parameters\n    ----------\n    module_name : module name\n        The name of the module to test.\n\n    Notes\n    -----\n    Unlike the previous ``nose``-based implementation, this class is not\n    publicly exposed as it performs some ``numpy``-specific warning\n    suppression.\n\n    "

    def __init__(self, module_name):
        self.module_name = module_name

    def __call__--- This code section failed: ---

 L. 125         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              pytest
                6  STORE_FAST               'pytest'

 L. 126         8  LOAD_CONST               0
               10  LOAD_CONST               None
               12  IMPORT_NAME              warnings
               14  STORE_FAST               'warnings'

 L. 129        16  LOAD_CONST               0
               18  LOAD_CONST               None
               20  IMPORT_NAME              hypothesis
               22  STORE_FAST               'hypothesis'

 L. 131        24  LOAD_GLOBAL              sys
               26  LOAD_ATTR                modules
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                module_name
               32  BINARY_SUBSCR    
               34  STORE_FAST               'module'

 L. 132        36  LOAD_GLOBAL              os
               38  LOAD_ATTR                path
               40  LOAD_METHOD              abspath
               42  LOAD_FAST                'module'
               44  LOAD_ATTR                __path__
               46  LOAD_CONST               0
               48  BINARY_SUBSCR    
               50  CALL_METHOD_1         1  ''
               52  STORE_FAST               'module_path'

 L. 135        54  LOAD_STR                 '-l'
               56  BUILD_LIST_1          1 
               58  STORE_FAST               'pytest_args'

 L. 138        60  LOAD_FAST                'pytest_args'
               62  LOAD_STR                 '-q'
               64  BUILD_LIST_1          1 
               66  INPLACE_ADD      
               68  STORE_FAST               'pytest_args'

 L. 143        70  LOAD_FAST                'warnings'
               72  LOAD_METHOD              catch_warnings
               74  CALL_METHOD_0         0  ''
               76  SETUP_WITH          116  'to 116'
               78  POP_TOP          

 L. 144        80  LOAD_FAST                'warnings'
               82  LOAD_METHOD              simplefilter
               84  LOAD_STR                 'always'
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          

 L. 145        90  LOAD_CONST               0
               92  LOAD_CONST               ('cpuinfo',)
               94  IMPORT_NAME_ATTR         numpy.distutils
               96  IMPORT_FROM              cpuinfo
               98  STORE_FAST               'cpuinfo'
              100  POP_TOP          
              102  POP_BLOCK        
              104  LOAD_CONST               None
              106  DUP_TOP          
              108  DUP_TOP          
              110  CALL_FUNCTION_3       3  ''
              112  POP_TOP          
              114  JUMP_FORWARD        132  'to 132'
            116_0  COME_FROM_WITH       76  '76'
              116  <49>             
              118  POP_JUMP_IF_TRUE    122  'to 122'
              120  <48>             
            122_0  COME_FROM           118  '118'
              122  POP_TOP          
              124  POP_TOP          
              126  POP_TOP          
              128  POP_EXCEPT       
              130  POP_TOP          
            132_0  COME_FROM           114  '114'

 L. 149       132  LOAD_FAST                'pytest_args'
              134  BUILD_LIST_0          0 
              136  LOAD_CONST               ('-W ignore:Not importing directory', '-W ignore:numpy.dtype size changed', '-W ignore:numpy.ufunc size changed', '-W ignore::UserWarning:cpuinfo')
              138  CALL_FINALLY        141  'to 141'
              140  INPLACE_ADD      
              142  STORE_FAST               'pytest_args'

 L. 157       144  LOAD_FAST                'pytest_args'

 L. 158       146  LOAD_STR                 '-W ignore:the matrix subclass is not'

 L. 159       148  LOAD_STR                 '-W ignore:Importing from numpy.matlib is'

 L. 157       150  BUILD_LIST_2          2 
              152  INPLACE_ADD      
              154  STORE_FAST               'pytest_args'

 L. 162       156  LOAD_FAST                'doctests'
              158  POP_JUMP_IF_FALSE   168  'to 168'

 L. 163       160  LOAD_GLOBAL              ValueError
              162  LOAD_STR                 'Doctests not supported'
              164  CALL_FUNCTION_1       1  ''
              166  RAISE_VARARGS_1       1  'exception instance'
            168_0  COME_FROM           158  '158'

 L. 165       168  LOAD_FAST                'extra_argv'
              170  POP_JUMP_IF_FALSE   184  'to 184'

 L. 166       172  LOAD_FAST                'pytest_args'
              174  LOAD_GLOBAL              list
              176  LOAD_FAST                'extra_argv'
              178  CALL_FUNCTION_1       1  ''
              180  INPLACE_ADD      
              182  STORE_FAST               'pytest_args'
            184_0  COME_FROM           170  '170'

 L. 168       184  LOAD_FAST                'verbose'
              186  LOAD_CONST               1
              188  COMPARE_OP               >
              190  POP_JUMP_IF_FALSE   214  'to 214'

 L. 169       192  LOAD_FAST                'pytest_args'
              194  LOAD_STR                 '-'
              196  LOAD_STR                 'v'
              198  LOAD_FAST                'verbose'
              200  LOAD_CONST               1
              202  BINARY_SUBTRACT  
              204  BINARY_MULTIPLY  
              206  BINARY_ADD       
              208  BUILD_LIST_1          1 
              210  INPLACE_ADD      
              212  STORE_FAST               'pytest_args'
            214_0  COME_FROM           190  '190'

 L. 171       214  LOAD_FAST                'coverage'
              216  POP_JUMP_IF_FALSE   232  'to 232'

 L. 172       218  LOAD_FAST                'pytest_args'
              220  LOAD_STR                 '--cov='
              222  LOAD_FAST                'module_path'
              224  BINARY_ADD       
              226  BUILD_LIST_1          1 
              228  INPLACE_ADD      
              230  STORE_FAST               'pytest_args'
            232_0  COME_FROM           216  '216'

 L. 174       232  LOAD_FAST                'label'
              234  LOAD_STR                 'fast'
              236  COMPARE_OP               ==
          238_240  POP_JUMP_IF_FALSE   288  'to 288'

 L. 176       242  LOAD_CONST               0
              244  LOAD_CONST               ('IS_PYPY',)
              246  IMPORT_NAME_ATTR         numpy.testing
              248  IMPORT_FROM              IS_PYPY
              250  STORE_FAST               'IS_PYPY'
              252  POP_TOP          

 L. 177       254  LOAD_FAST                'IS_PYPY'
          256_258  POP_JUMP_IF_FALSE   274  'to 274'

 L. 178       260  LOAD_FAST                'pytest_args'
              262  LOAD_STR                 '-m'
              264  LOAD_STR                 'not slow and not slow_pypy'
              266  BUILD_LIST_2          2 
              268  INPLACE_ADD      
              270  STORE_FAST               'pytest_args'
              272  JUMP_FORWARD        286  'to 286'
            274_0  COME_FROM           256  '256'

 L. 180       274  LOAD_FAST                'pytest_args'
              276  LOAD_STR                 '-m'
              278  LOAD_STR                 'not slow'
              280  BUILD_LIST_2          2 
              282  INPLACE_ADD      
              284  STORE_FAST               'pytest_args'
            286_0  COME_FROM           272  '272'
              286  JUMP_FORWARD        310  'to 310'
            288_0  COME_FROM           238  '238'

 L. 182       288  LOAD_FAST                'label'
              290  LOAD_STR                 'full'
              292  COMPARE_OP               !=
          294_296  POP_JUMP_IF_FALSE   310  'to 310'

 L. 183       298  LOAD_FAST                'pytest_args'
              300  LOAD_STR                 '-m'
              302  LOAD_FAST                'label'
              304  BUILD_LIST_2          2 
              306  INPLACE_ADD      
              308  STORE_FAST               'pytest_args'
            310_0  COME_FROM           294  '294'
            310_1  COME_FROM           286  '286'

 L. 185       310  LOAD_FAST                'durations'
              312  LOAD_CONST               0
              314  COMPARE_OP               >=
          316_318  POP_JUMP_IF_FALSE   334  'to 334'

 L. 186       320  LOAD_FAST                'pytest_args'
              322  LOAD_STR                 '--durations=%s'
              324  LOAD_FAST                'durations'
              326  BINARY_MODULO    
              328  BUILD_LIST_1          1 
              330  INPLACE_ADD      
              332  STORE_FAST               'pytest_args'
            334_0  COME_FROM           316  '316'

 L. 188       334  LOAD_FAST                'tests'
              336  LOAD_CONST               None
              338  <117>                 0  ''
          340_342  POP_JUMP_IF_FALSE   352  'to 352'

 L. 189       344  LOAD_FAST                'self'
              346  LOAD_ATTR                module_name
              348  BUILD_LIST_1          1 
              350  STORE_FAST               'tests'
            352_0  COME_FROM           340  '340'

 L. 191       352  LOAD_FAST                'pytest_args'
              354  LOAD_STR                 '--pyargs'
              356  BUILD_LIST_1          1 
              358  LOAD_GLOBAL              list
              360  LOAD_FAST                'tests'
              362  CALL_FUNCTION_1       1  ''
              364  BINARY_ADD       
              366  INPLACE_ADD      
              368  STORE_FAST               'pytest_args'

 L. 196       370  LOAD_FAST                'hypothesis'
              372  LOAD_ATTR                settings
              374  LOAD_ATTR                register_profile

 L. 197       376  LOAD_STR                 'np.test() profile'

 L. 198       378  LOAD_CONST               None
              380  LOAD_CONST               True
              382  LOAD_CONST               None
              384  LOAD_CONST               True

 L. 199       386  LOAD_FAST                'hypothesis'
              388  LOAD_ATTR                HealthCheck
              390  LOAD_METHOD              all
              392  CALL_METHOD_0         0  ''

 L. 196       394  LOAD_CONST               ('name', 'deadline', 'print_blob', 'database', 'derandomize', 'suppress_health_check')
              396  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              398  POP_TOP          

 L. 203       400  LOAD_GLOBAL              _show_numpy_info
              402  CALL_FUNCTION_0       0  ''
              404  POP_TOP          

 L. 205       406  SETUP_FINALLY       422  'to 422'

 L. 206       408  LOAD_FAST                'pytest'
              410  LOAD_METHOD              main
              412  LOAD_FAST                'pytest_args'
              414  CALL_METHOD_1         1  ''
              416  STORE_FAST               'code'
              418  POP_BLOCK        
              420  JUMP_FORWARD        466  'to 466'
            422_0  COME_FROM_FINALLY   406  '406'

 L. 207       422  DUP_TOP          
              424  LOAD_GLOBAL              SystemExit
          426_428  <121>               464  ''
              430  POP_TOP          
              432  STORE_FAST               'exc'
              434  POP_TOP          
              436  SETUP_FINALLY       456  'to 456'

 L. 208       438  LOAD_FAST                'exc'
              440  LOAD_ATTR                code
              442  STORE_FAST               'code'
              444  POP_BLOCK        
              446  POP_EXCEPT       
              448  LOAD_CONST               None
              450  STORE_FAST               'exc'
              452  DELETE_FAST              'exc'
              454  JUMP_FORWARD        466  'to 466'
            456_0  COME_FROM_FINALLY   436  '436'
              456  LOAD_CONST               None
              458  STORE_FAST               'exc'
              460  DELETE_FAST              'exc'
              462  <48>             
              464  <48>             
            466_0  COME_FROM           454  '454'
            466_1  COME_FROM           420  '420'

 L. 210       466  LOAD_FAST                'code'
              468  LOAD_CONST               0
              470  COMPARE_OP               ==
              472  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 106