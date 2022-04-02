# uncompyle6 version 3.7.4
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
    test = PytestTester(__name__)
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
    from numpy.core._multiarray_umath import __cpu_features__, __cpu_baseline__, __cpu_dispatch__
    import numpy as np
    print('NumPy version %s' % np.__version__)
    relaxed_strides = np.ones((10, 1), order='C').flags.f_contiguous
    print('NumPy relaxed strides checking option:', relaxed_strides)
    if len(__cpu_baseline__) == 0 and len(__cpu_dispatch__) == 0:
        enabled_features = 'nothing enabled'
    else:
        enabled_features = ' '.join(__cpu_baseline__)
        for feature in __cpu_dispatch__:
            if __cpu_features__[feature]:
                enabled_features += ' %s*' % feature
            else:
                enabled_features += ' %s?' % feature
        else:
            print('NumPy CPU features:', enabled_features)


class PytestTester:
    __doc__ = "\n    Pytest test runner.\n\n    A test function is typically added to a package's __init__.py like so::\n\n      from numpy._pytesttester import PytestTester\n      test = PytestTester(__name__).test\n      del PytestTester\n\n    Calling this test function finds and runs all tests associated with the\n    module and all its sub-modules.\n\n    Attributes\n    ----------\n    module_name : str\n        Full path to the package to test.\n\n    Parameters\n    ----------\n    module_name : module name\n        The name of the module to test.\n\n    Notes\n    -----\n    Unlike the previous ``nose``-based implementation, this class is not\n    publicly exposed as it performs some ``numpy``-specific warning\n    suppression.\n\n    "

    def __init__(self, module_name):
        self.module_name = module_name

    def __call__--- This code section failed: ---

 L. 140         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              pytest
                6  STORE_FAST               'pytest'

 L. 141         8  LOAD_CONST               0
               10  LOAD_CONST               None
               12  IMPORT_NAME              warnings
               14  STORE_FAST               'warnings'

 L. 143        16  LOAD_GLOBAL              sys
               18  LOAD_ATTR                modules
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                module_name
               24  BINARY_SUBSCR    
               26  STORE_FAST               'module'

 L. 144        28  LOAD_GLOBAL              os
               30  LOAD_ATTR                path
               32  LOAD_METHOD              abspath
               34  LOAD_FAST                'module'
               36  LOAD_ATTR                __path__
               38  LOAD_CONST               0
               40  BINARY_SUBSCR    
               42  CALL_METHOD_1         1  ''
               44  STORE_FAST               'module_path'

 L. 147        46  LOAD_STR                 '-l'
               48  BUILD_LIST_1          1 
               50  STORE_FAST               'pytest_args'

 L. 150        52  LOAD_FAST                'pytest_args'
               54  LOAD_STR                 '-q'
               56  BUILD_LIST_1          1 
               58  INPLACE_ADD      
               60  STORE_FAST               'pytest_args'

 L. 155        62  LOAD_FAST                'warnings'
               64  LOAD_METHOD              catch_warnings
               66  CALL_METHOD_0         0  ''
               68  SETUP_WITH          108  'to 108'
               70  POP_TOP          

 L. 156        72  LOAD_FAST                'warnings'
               74  LOAD_METHOD              simplefilter
               76  LOAD_STR                 'always'
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          

 L. 157        82  LOAD_CONST               0
               84  LOAD_CONST               ('cpuinfo',)
               86  IMPORT_NAME_ATTR         numpy.distutils
               88  IMPORT_FROM              cpuinfo
               90  STORE_FAST               'cpuinfo'
               92  POP_TOP          
               94  POP_BLOCK        
               96  LOAD_CONST               None
               98  DUP_TOP          
              100  DUP_TOP          
              102  CALL_FUNCTION_3       3  ''
              104  POP_TOP          
              106  JUMP_FORWARD        124  'to 124'
            108_0  COME_FROM_WITH       68  '68'
              108  <49>             
              110  POP_JUMP_IF_TRUE    114  'to 114'
              112  <48>             
            114_0  COME_FROM           110  '110'
              114  POP_TOP          
              116  POP_TOP          
              118  POP_TOP          
              120  POP_EXCEPT       
              122  POP_TOP          
            124_0  COME_FROM           106  '106'

 L. 161       124  LOAD_FAST                'pytest_args'
              126  BUILD_LIST_0          0 
              128  LOAD_CONST               ('-W ignore:Not importing directory', '-W ignore:numpy.dtype size changed', '-W ignore:numpy.ufunc size changed', '-W ignore::UserWarning:cpuinfo')
              130  CALL_FINALLY        133  'to 133'
              132  INPLACE_ADD      
              134  STORE_FAST               'pytest_args'

 L. 169       136  LOAD_FAST                'pytest_args'

 L. 170       138  LOAD_STR                 '-W ignore:the matrix subclass is not'

 L. 171       140  LOAD_STR                 '-W ignore:Importing from numpy.matlib is'

 L. 169       142  BUILD_LIST_2          2 
              144  INPLACE_ADD      
              146  STORE_FAST               'pytest_args'

 L. 174       148  LOAD_FAST                'doctests'
              150  POP_JUMP_IF_FALSE   160  'to 160'

 L. 175       152  LOAD_GLOBAL              ValueError
              154  LOAD_STR                 'Doctests not supported'
              156  CALL_FUNCTION_1       1  ''
              158  RAISE_VARARGS_1       1  'exception instance'
            160_0  COME_FROM           150  '150'

 L. 177       160  LOAD_FAST                'extra_argv'
              162  POP_JUMP_IF_FALSE   176  'to 176'

 L. 178       164  LOAD_FAST                'pytest_args'
              166  LOAD_GLOBAL              list
              168  LOAD_FAST                'extra_argv'
              170  CALL_FUNCTION_1       1  ''
              172  INPLACE_ADD      
              174  STORE_FAST               'pytest_args'
            176_0  COME_FROM           162  '162'

 L. 180       176  LOAD_FAST                'verbose'
              178  LOAD_CONST               1
              180  COMPARE_OP               >
              182  POP_JUMP_IF_FALSE   206  'to 206'

 L. 181       184  LOAD_FAST                'pytest_args'
              186  LOAD_STR                 '-'
              188  LOAD_STR                 'v'
              190  LOAD_FAST                'verbose'
              192  LOAD_CONST               1
              194  BINARY_SUBTRACT  
              196  BINARY_MULTIPLY  
              198  BINARY_ADD       
              200  BUILD_LIST_1          1 
              202  INPLACE_ADD      
              204  STORE_FAST               'pytest_args'
            206_0  COME_FROM           182  '182'

 L. 183       206  LOAD_FAST                'coverage'
              208  POP_JUMP_IF_FALSE   224  'to 224'

 L. 184       210  LOAD_FAST                'pytest_args'
              212  LOAD_STR                 '--cov='
              214  LOAD_FAST                'module_path'
              216  BINARY_ADD       
              218  BUILD_LIST_1          1 
              220  INPLACE_ADD      
              222  STORE_FAST               'pytest_args'
            224_0  COME_FROM           208  '208'

 L. 186       224  LOAD_FAST                'label'
              226  LOAD_STR                 'fast'
              228  COMPARE_OP               ==
          230_232  POP_JUMP_IF_FALSE   280  'to 280'

 L. 188       234  LOAD_CONST               0
              236  LOAD_CONST               ('IS_PYPY',)
              238  IMPORT_NAME_ATTR         numpy.testing
              240  IMPORT_FROM              IS_PYPY
              242  STORE_FAST               'IS_PYPY'
              244  POP_TOP          

 L. 189       246  LOAD_FAST                'IS_PYPY'
          248_250  POP_JUMP_IF_FALSE   266  'to 266'

 L. 190       252  LOAD_FAST                'pytest_args'
              254  LOAD_STR                 '-m'
              256  LOAD_STR                 'not slow and not slow_pypy'
              258  BUILD_LIST_2          2 
              260  INPLACE_ADD      
              262  STORE_FAST               'pytest_args'
              264  JUMP_FORWARD        278  'to 278'
            266_0  COME_FROM           248  '248'

 L. 192       266  LOAD_FAST                'pytest_args'
              268  LOAD_STR                 '-m'
              270  LOAD_STR                 'not slow'
              272  BUILD_LIST_2          2 
              274  INPLACE_ADD      
              276  STORE_FAST               'pytest_args'
            278_0  COME_FROM           264  '264'
              278  JUMP_FORWARD        302  'to 302'
            280_0  COME_FROM           230  '230'

 L. 194       280  LOAD_FAST                'label'
              282  LOAD_STR                 'full'
              284  COMPARE_OP               !=
          286_288  POP_JUMP_IF_FALSE   302  'to 302'

 L. 195       290  LOAD_FAST                'pytest_args'
              292  LOAD_STR                 '-m'
              294  LOAD_FAST                'label'
              296  BUILD_LIST_2          2 
              298  INPLACE_ADD      
              300  STORE_FAST               'pytest_args'
            302_0  COME_FROM           286  '286'
            302_1  COME_FROM           278  '278'

 L. 197       302  LOAD_FAST                'durations'
              304  LOAD_CONST               0
              306  COMPARE_OP               >=
          308_310  POP_JUMP_IF_FALSE   326  'to 326'

 L. 198       312  LOAD_FAST                'pytest_args'
              314  LOAD_STR                 '--durations=%s'
              316  LOAD_FAST                'durations'
              318  BINARY_MODULO    
              320  BUILD_LIST_1          1 
              322  INPLACE_ADD      
              324  STORE_FAST               'pytest_args'
            326_0  COME_FROM           308  '308'

 L. 200       326  LOAD_FAST                'tests'
              328  LOAD_CONST               None
              330  <117>                 0  ''
          332_334  POP_JUMP_IF_FALSE   344  'to 344'

 L. 201       336  LOAD_FAST                'self'
              338  LOAD_ATTR                module_name
              340  BUILD_LIST_1          1 
              342  STORE_FAST               'tests'
            344_0  COME_FROM           332  '332'

 L. 203       344  LOAD_FAST                'pytest_args'
              346  LOAD_STR                 '--pyargs'
              348  BUILD_LIST_1          1 
              350  LOAD_GLOBAL              list
              352  LOAD_FAST                'tests'
              354  CALL_FUNCTION_1       1  ''
              356  BINARY_ADD       
              358  INPLACE_ADD      
              360  STORE_FAST               'pytest_args'

 L. 206       362  LOAD_GLOBAL              _show_numpy_info
              364  CALL_FUNCTION_0       0  ''
              366  POP_TOP          

 L. 208       368  SETUP_FINALLY       384  'to 384'

 L. 209       370  LOAD_FAST                'pytest'
              372  LOAD_METHOD              main
              374  LOAD_FAST                'pytest_args'
              376  CALL_METHOD_1         1  ''
              378  STORE_FAST               'code'
              380  POP_BLOCK        
              382  JUMP_FORWARD        428  'to 428'
            384_0  COME_FROM_FINALLY   368  '368'

 L. 210       384  DUP_TOP          
              386  LOAD_GLOBAL              SystemExit
          388_390  <121>               426  ''
              392  POP_TOP          
              394  STORE_FAST               'exc'
              396  POP_TOP          
              398  SETUP_FINALLY       418  'to 418'

 L. 211       400  LOAD_FAST                'exc'
              402  LOAD_ATTR                code
              404  STORE_FAST               'code'
              406  POP_BLOCK        
              408  POP_EXCEPT       
              410  LOAD_CONST               None
              412  STORE_FAST               'exc'
              414  DELETE_FAST              'exc'
              416  JUMP_FORWARD        428  'to 428'
            418_0  COME_FROM_FINALLY   398  '398'
              418  LOAD_CONST               None
              420  STORE_FAST               'exc'
              422  DELETE_FAST              'exc'
              424  <48>             
              426  <48>             
            428_0  COME_FROM           416  '416'
            428_1  COME_FROM           382  '382'

 L. 213       428  LOAD_FAST                'code'
              430  LOAD_CONST               0
              432  COMPARE_OP               ==
              434  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 98