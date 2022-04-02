# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: numpy\testing\_private\utils.py
"""
Utility function to facilitate testing.

"""
import os, sys, platform, re, gc, operator, warnings
from functools import partial, wraps
import shutil, contextlib
from tempfile import mkdtemp, mkstemp
from unittest.case import SkipTest
from warnings import WarningMessage
import pprint
from numpy.core import intp, float32, empty, arange, array_repr, ndarray, isnat, array
import numpy.linalg.lapack_lite
from io import StringIO
__all__ = [
 'assert_equal', 'assert_almost_equal', 'assert_approx_equal',
 'assert_array_equal', 'assert_array_less', 'assert_string_equal',
 'assert_array_almost_equal', 'assert_raises', 'build_err_msg',
 'decorate_methods', 'jiffies', 'memusage', 'print_assert_equal',
 'raises', 'rundocs', 'runstring', 'verbose', 'measure',
 'assert_', 'assert_array_almost_equal_nulp', 'assert_raises_regex',
 'assert_array_max_ulp', 'assert_warns', 'assert_no_warnings',
 'assert_allclose', 'IgnoreException', 'clear_and_catch_warnings',
 'SkipTest', 'KnownFailureException', 'temppath', 'tempdir', 'IS_PYPY',
 'HAS_REFCOUNT', 'suppress_warnings', 'assert_array_compare',
 '_assert_valid_refcount', '_gen_alignment_data', 'assert_no_gc_cycles',
 'break_cycles', 'HAS_LAPACK64']

class KnownFailureException(Exception):
    __doc__ = 'Raise this exception to mark a test as a known failing test.'


KnownFailureTest = KnownFailureException
verbose = 0
IS_PYPY = platform.python_implementation() == 'PyPy'
HAS_REFCOUNT = getattr(sys, 'getrefcount', None) is not None
HAS_LAPACK64 = numpy.linalg.lapack_lite._ilp64

def import_nose():
    """ Import nose only when needed.
    """
    nose_is_good = True
    minimum_nose_version = (1, 0, 0)
    try:
        import nose
    except ImportError:
        nose_is_good = False
    else:
        if nose.__versioninfo__ < minimum_nose_version:
            nose_is_good = False
    if not nose_is_good:
        msg = 'Need nose >= %d.%d.%d for tests - see https://nose.readthedocs.io' % minimum_nose_version
        raise ImportError(msg)
    return nose


def assert_(val, msg=''):
    """
    Assert that works in release mode.
    Accepts callable msg to allow deferring evaluation until failure.

    The Python built-in ``assert`` does not work when executing code in
    optimized mode (the ``-O`` flag) - no byte-code is generated for it.

    For documentation on usage, refer to the Python documentation.

    """
    __tracebackhide__ = True
    if not val:
        try:
            smsg = msg()
        except TypeError:
            smsg = msg
        else:
            raise AssertionError(smsg)


def gisnan(x):
    """like isnan, but always raise an error if type not supported instead of
    returning a TypeError object.

    Notes
    -----
    isnan and other ufunc sometimes return a NotImplementedType object instead
    of raising any exception. This function is a wrapper to make sure an
    exception is always raised.

    This should be removed once this problem is solved at the Ufunc level."""
    from numpy.core import isnan
    st = isnan(x)
    if isinstance(st, type(NotImplemented)):
        raise TypeError('isnan not supported for this type')
    return st


def gisfinite(x):
    """like isfinite, but always raise an error if type not supported instead of
    returning a TypeError object.

    Notes
    -----
    isfinite and other ufunc sometimes return a NotImplementedType object instead
    of raising any exception. This function is a wrapper to make sure an
    exception is always raised.

    This should be removed once this problem is solved at the Ufunc level."""
    from numpy.core import isfinite, errstate
    with errstate(invalid='ignore'):
        st = isfinite(x)
        if isinstance(st, type(NotImplemented)):
            raise TypeError('isfinite not supported for this type')
    return st


def gisinf(x):
    """like isinf, but always raise an error if type not supported instead of
    returning a TypeError object.

    Notes
    -----
    isinf and other ufunc sometimes return a NotImplementedType object instead
    of raising any exception. This function is a wrapper to make sure an
    exception is always raised.

    This should be removed once this problem is solved at the Ufunc level."""
    from numpy.core import isinf, errstate
    with errstate(invalid='ignore'):
        st = isinf(x)
        if isinstance(st, type(NotImplemented)):
            raise TypeError('isinf not supported for this type')
    return st


if os.name == 'nt':

    def GetPerformanceAttributes--- This code section failed: ---

 L. 165         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              win32pdh
                6  STORE_FAST               'win32pdh'

 L. 166         8  LOAD_FAST                'format'
               10  LOAD_CONST               None
               12  COMPARE_OP               is
               14  POP_JUMP_IF_FALSE    22  'to 22'

 L. 167        16  LOAD_FAST                'win32pdh'
               18  LOAD_ATTR                PDH_FMT_LONG
               20  STORE_FAST               'format'
             22_0  COME_FROM            14  '14'

 L. 168        22  LOAD_FAST                'win32pdh'
               24  LOAD_METHOD              MakeCounterPath
               26  LOAD_FAST                'machine'
               28  LOAD_FAST                'object'
               30  LOAD_FAST                'instance'
               32  LOAD_CONST               None
               34  LOAD_FAST                'inum'
               36  LOAD_FAST                'counter'
               38  BUILD_TUPLE_6         6 
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'path'

 L. 169        44  LOAD_FAST                'win32pdh'
               46  LOAD_METHOD              OpenQuery
               48  CALL_METHOD_0         0  ''
               50  STORE_FAST               'hq'

 L. 170        52  SETUP_FINALLY       122  'to 122'

 L. 171        54  LOAD_FAST                'win32pdh'
               56  LOAD_METHOD              AddCounter
               58  LOAD_FAST                'hq'
               60  LOAD_FAST                'path'
               62  CALL_METHOD_2         2  ''
               64  STORE_FAST               'hc'

 L. 172        66  SETUP_FINALLY       106  'to 106'

 L. 173        68  LOAD_FAST                'win32pdh'
               70  LOAD_METHOD              CollectQueryData
               72  LOAD_FAST                'hq'
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          

 L. 174        78  LOAD_FAST                'win32pdh'
               80  LOAD_METHOD              GetFormattedCounterValue
               82  LOAD_FAST                'hc'
               84  LOAD_FAST                'format'
               86  CALL_METHOD_2         2  ''
               88  UNPACK_SEQUENCE_2     2 
               90  STORE_FAST               'type'
               92  STORE_FAST               'val'

 L. 175        94  LOAD_FAST                'val'
               96  POP_BLOCK        
               98  CALL_FINALLY        106  'to 106'
              100  POP_BLOCK        
              102  CALL_FINALLY        122  'to 122'
              104  RETURN_VALUE     
            106_0  COME_FROM            98  '98'
            106_1  COME_FROM_FINALLY    66  '66'

 L. 177       106  LOAD_FAST                'win32pdh'
              108  LOAD_METHOD              RemoveCounter
              110  LOAD_FAST                'hc'
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          
              116  END_FINALLY      
              118  POP_BLOCK        
              120  BEGIN_FINALLY    
            122_0  COME_FROM           102  '102'
            122_1  COME_FROM_FINALLY    52  '52'

 L. 179       122  LOAD_FAST                'win32pdh'
              124  LOAD_METHOD              CloseQuery
              126  LOAD_FAST                'hq'
              128  CALL_METHOD_1         1  ''
              130  POP_TOP          
              132  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 98


    def memusage(processName='python', instance=0):
        import win32pdh
        return GetPerformanceAttributes('Process', 'Virtual Bytes', processName, instance, win32pdh.PDH_FMT_LONG, None)


elif sys.platform[:5] == 'linux':

    def memusage--- This code section failed: ---

 L. 194         0  SETUP_FINALLY        52  'to 52'

 L. 195         2  LOAD_GLOBAL              open
                4  LOAD_FAST                '_proc_pid_stat'
                6  LOAD_STR                 'r'
                8  CALL_FUNCTION_2       2  ''
               10  SETUP_WITH           32  'to 32'
               12  STORE_FAST               'f'

 L. 196        14  LOAD_FAST                'f'
               16  LOAD_METHOD              readline
               18  CALL_METHOD_0         0  ''
               20  LOAD_METHOD              split
               22  LOAD_STR                 ' '
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'l'
               28  POP_BLOCK        
               30  BEGIN_FINALLY    
             32_0  COME_FROM_WITH       10  '10'
               32  WITH_CLEANUP_START
               34  WITH_CLEANUP_FINISH
               36  END_FINALLY      

 L. 197        38  LOAD_GLOBAL              int
               40  LOAD_FAST                'l'
               42  LOAD_CONST               22
               44  BINARY_SUBSCR    
               46  CALL_FUNCTION_1       1  ''
               48  POP_BLOCK        
               50  RETURN_VALUE     
             52_0  COME_FROM_FINALLY     0  '0'

 L. 198        52  DUP_TOP          
               54  LOAD_GLOBAL              Exception
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    72  'to 72'
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L. 199        66  POP_EXCEPT       
               68  LOAD_CONST               None
               70  RETURN_VALUE     
             72_0  COME_FROM            58  '58'
               72  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 68


else:

    def memusage():
        """
        Return memory usage of running python. [Not implemented]

        """
        raise NotImplementedError


if sys.platform[:5] == 'linux':

    def jiffies(_proc_pid_stat='/proc/%s/stat' % os.getpid(), _load_time=[]):
        """
        Return number of jiffies elapsed.

        Return number of jiffies (1/100ths of a second) that this
        process has been scheduled in user mode. See man 5 proc.

        """
        import time
        if not _load_time:
            _load_time.appendtime.time()
        try:
            with open(_proc_pid_stat, 'r') as f:
                l = f.readline().split' '
            return int(l[13])
        except Exception:
            return int(100 * (time.time() - _load_time[0]))


else:

    def jiffies(_load_time=[]):
        """
        Return number of jiffies elapsed.

        Return number of jiffies (1/100ths of a second) that this
        process has been scheduled in user mode. See man 5 proc.

        """
        import time
        if not _load_time:
            _load_time.appendtime.time()
        return int(100 * (time.time() - _load_time[0]))


def build_err_msg(arrays, err_msg, header='Items are not equal:', verbose=True, names=('ACTUAL', 'DESIRED'), precision=8):
    msg = [
     '\n' + header]
    if err_msg:
        if err_msg.find'\n' == -1 and len(err_msg) < 79 - len(header):
            msg = [
             msg[0] + ' ' + err_msg]
        else:
            msg.appenderr_msg
    if verbose:
        for i, a in enumerate(arrays):
            if isinstance(a, ndarray):
                r_func = partial(array_repr, precision=precision)
            else:
                r_func = repr
            try:
                r = r_func(a)
            except Exception as exc:
                try:
                    r = '[repr failed for <{}>: {}]'.formattype(a).__name__exc
                finally:
                    exc = None
                    del exc

            if r.count'\n' > 3:
                r = '\n'.joinr.splitlines()[:3]
                r += '...'
            else:
                msg.append(' %s: %s' % (names[i], r))

        return '\n'.joinmsg


def assert_equal--- This code section failed: ---

 L. 324         0  LOAD_CONST               True
                2  STORE_FAST               '__tracebackhide__'

 L. 325         4  LOAD_GLOBAL              isinstance
                6  LOAD_FAST                'desired'
                8  LOAD_GLOBAL              dict
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_FALSE   134  'to 134'

 L. 326        14  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'actual'
               18  LOAD_GLOBAL              dict
               20  CALL_FUNCTION_2       2  ''
               22  POP_JUMP_IF_TRUE     40  'to 40'

 L. 327        24  LOAD_ASSERT              AssertionError
               26  LOAD_GLOBAL              repr
               28  LOAD_GLOBAL              type
               30  LOAD_FAST                'actual'
               32  CALL_FUNCTION_1       1  ''
               34  CALL_FUNCTION_1       1  ''
               36  CALL_FUNCTION_1       1  ''
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            22  '22'

 L. 328        40  LOAD_GLOBAL              assert_equal
               42  LOAD_GLOBAL              len
               44  LOAD_FAST                'actual'
               46  CALL_FUNCTION_1       1  ''
               48  LOAD_GLOBAL              len
               50  LOAD_FAST                'desired'
               52  CALL_FUNCTION_1       1  ''
               54  LOAD_FAST                'err_msg'
               56  LOAD_FAST                'verbose'
               58  CALL_FUNCTION_4       4  ''
               60  POP_TOP          

 L. 329        62  LOAD_FAST                'desired'
               64  LOAD_METHOD              items
               66  CALL_METHOD_0         0  ''
               68  GET_ITER         
             70_0  COME_FROM           128  '128'
               70  FOR_ITER            130  'to 130'
               72  UNPACK_SEQUENCE_2     2 
               74  STORE_FAST               'k'
               76  STORE_FAST               'i'

 L. 330        78  LOAD_FAST                'k'
               80  LOAD_FAST                'actual'
               82  COMPARE_OP               not-in
               84  POP_JUMP_IF_FALSE    98  'to 98'

 L. 331        86  LOAD_GLOBAL              AssertionError
               88  LOAD_GLOBAL              repr
               90  LOAD_FAST                'k'
               92  CALL_FUNCTION_1       1  ''
               94  CALL_FUNCTION_1       1  ''
               96  RAISE_VARARGS_1       1  'exception instance'
             98_0  COME_FROM            84  '84'

 L. 332        98  LOAD_GLOBAL              assert_equal
              100  LOAD_FAST                'actual'
              102  LOAD_FAST                'k'
              104  BINARY_SUBSCR    
              106  LOAD_FAST                'desired'
              108  LOAD_FAST                'k'
              110  BINARY_SUBSCR    
              112  LOAD_STR                 'key=%r\n%s'
              114  LOAD_FAST                'k'
              116  LOAD_FAST                'err_msg'
              118  BUILD_TUPLE_2         2 
              120  BINARY_MODULO    
              122  LOAD_FAST                'verbose'
              124  CALL_FUNCTION_4       4  ''
              126  POP_TOP          
              128  JUMP_BACK            70  'to 70'
            130_0  COME_FROM            70  '70'

 L. 333       130  LOAD_CONST               None
              132  RETURN_VALUE     
            134_0  COME_FROM            12  '12'

 L. 334       134  LOAD_GLOBAL              isinstance
              136  LOAD_FAST                'desired'
              138  LOAD_GLOBAL              list
              140  LOAD_GLOBAL              tuple
              142  BUILD_TUPLE_2         2 
              144  CALL_FUNCTION_2       2  ''
              146  POP_JUMP_IF_FALSE   236  'to 236'
              148  LOAD_GLOBAL              isinstance
              150  LOAD_FAST                'actual'
              152  LOAD_GLOBAL              list
              154  LOAD_GLOBAL              tuple
              156  BUILD_TUPLE_2         2 
              158  CALL_FUNCTION_2       2  ''
              160  POP_JUMP_IF_FALSE   236  'to 236'

 L. 335       162  LOAD_GLOBAL              assert_equal
              164  LOAD_GLOBAL              len
              166  LOAD_FAST                'actual'
              168  CALL_FUNCTION_1       1  ''
              170  LOAD_GLOBAL              len
              172  LOAD_FAST                'desired'
              174  CALL_FUNCTION_1       1  ''
              176  LOAD_FAST                'err_msg'
              178  LOAD_FAST                'verbose'
              180  CALL_FUNCTION_4       4  ''
              182  POP_TOP          

 L. 336       184  LOAD_GLOBAL              range
              186  LOAD_GLOBAL              len
              188  LOAD_FAST                'desired'
              190  CALL_FUNCTION_1       1  ''
              192  CALL_FUNCTION_1       1  ''
              194  GET_ITER         
            196_0  COME_FROM           230  '230'
              196  FOR_ITER            232  'to 232'
              198  STORE_FAST               'k'

 L. 337       200  LOAD_GLOBAL              assert_equal
              202  LOAD_FAST                'actual'
              204  LOAD_FAST                'k'
              206  BINARY_SUBSCR    
              208  LOAD_FAST                'desired'
              210  LOAD_FAST                'k'
              212  BINARY_SUBSCR    
              214  LOAD_STR                 'item=%r\n%s'
              216  LOAD_FAST                'k'
              218  LOAD_FAST                'err_msg'
              220  BUILD_TUPLE_2         2 
              222  BINARY_MODULO    
              224  LOAD_FAST                'verbose'
              226  CALL_FUNCTION_4       4  ''
              228  POP_TOP          
              230  JUMP_BACK           196  'to 196'
            232_0  COME_FROM           196  '196'

 L. 338       232  LOAD_CONST               None
              234  RETURN_VALUE     
            236_0  COME_FROM           160  '160'
            236_1  COME_FROM           146  '146'

 L. 339       236  LOAD_CONST               0
              238  LOAD_CONST               ('ndarray', 'isscalar', 'signbit')
              240  IMPORT_NAME_ATTR         numpy.core
              242  IMPORT_FROM              ndarray
              244  STORE_FAST               'ndarray'
              246  IMPORT_FROM              isscalar
              248  STORE_FAST               'isscalar'
              250  IMPORT_FROM              signbit
              252  STORE_FAST               'signbit'
              254  POP_TOP          

 L. 340       256  LOAD_CONST               0
              258  LOAD_CONST               ('iscomplexobj', 'real', 'imag')
              260  IMPORT_NAME_ATTR         numpy.lib
              262  IMPORT_FROM              iscomplexobj
              264  STORE_FAST               'iscomplexobj'
              266  IMPORT_FROM              real
              268  STORE_FAST               'real'
              270  IMPORT_FROM              imag
              272  STORE_FAST               'imag'
              274  POP_TOP          

 L. 341       276  LOAD_GLOBAL              isinstance
              278  LOAD_FAST                'actual'
              280  LOAD_FAST                'ndarray'
              282  CALL_FUNCTION_2       2  ''
          284_286  POP_JUMP_IF_TRUE    300  'to 300'
              288  LOAD_GLOBAL              isinstance
              290  LOAD_FAST                'desired'
              292  LOAD_FAST                'ndarray'
              294  CALL_FUNCTION_2       2  ''
          296_298  POP_JUMP_IF_FALSE   314  'to 314'
            300_0  COME_FROM           284  '284'

 L. 342       300  LOAD_GLOBAL              assert_array_equal
              302  LOAD_FAST                'actual'
              304  LOAD_FAST                'desired'
              306  LOAD_FAST                'err_msg'
              308  LOAD_FAST                'verbose'
              310  CALL_FUNCTION_4       4  ''
              312  RETURN_VALUE     
            314_0  COME_FROM           296  '296'

 L. 343       314  LOAD_GLOBAL              build_err_msg
              316  LOAD_FAST                'actual'
              318  LOAD_FAST                'desired'
              320  BUILD_LIST_2          2 
              322  LOAD_FAST                'err_msg'
              324  LOAD_FAST                'verbose'
              326  LOAD_CONST               ('verbose',)
              328  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              330  STORE_FAST               'msg'

 L. 348       332  SETUP_FINALLY       356  'to 356'

 L. 349       334  LOAD_FAST                'iscomplexobj'
              336  LOAD_FAST                'actual'
              338  CALL_FUNCTION_1       1  ''
          340_342  JUMP_IF_TRUE_OR_POP   350  'to 350'
              344  LOAD_FAST                'iscomplexobj'
              346  LOAD_FAST                'desired'
              348  CALL_FUNCTION_1       1  ''
            350_0  COME_FROM           340  '340'
              350  STORE_FAST               'usecomplex'
              352  POP_BLOCK        
              354  JUMP_FORWARD        386  'to 386'
            356_0  COME_FROM_FINALLY   332  '332'

 L. 350       356  DUP_TOP          
              358  LOAD_GLOBAL              ValueError
              360  LOAD_GLOBAL              TypeError
              362  BUILD_TUPLE_2         2 
              364  COMPARE_OP               exception-match
          366_368  POP_JUMP_IF_FALSE   384  'to 384'
              370  POP_TOP          
              372  POP_TOP          
              374  POP_TOP          

 L. 351       376  LOAD_CONST               False
              378  STORE_FAST               'usecomplex'
              380  POP_EXCEPT       
              382  JUMP_FORWARD        386  'to 386'
            384_0  COME_FROM           366  '366'
              384  END_FINALLY      
            386_0  COME_FROM           382  '382'
            386_1  COME_FROM           354  '354'

 L. 353       386  LOAD_FAST                'usecomplex'
          388_390  POP_JUMP_IF_FALSE   520  'to 520'

 L. 354       392  LOAD_FAST                'iscomplexobj'
              394  LOAD_FAST                'actual'
              396  CALL_FUNCTION_1       1  ''
          398_400  POP_JUMP_IF_FALSE   420  'to 420'

 L. 355       402  LOAD_FAST                'real'
              404  LOAD_FAST                'actual'
              406  CALL_FUNCTION_1       1  ''
              408  STORE_FAST               'actualr'

 L. 356       410  LOAD_FAST                'imag'
              412  LOAD_FAST                'actual'
              414  CALL_FUNCTION_1       1  ''
              416  STORE_FAST               'actuali'
              418  JUMP_FORWARD        428  'to 428'
            420_0  COME_FROM           398  '398'

 L. 358       420  LOAD_FAST                'actual'
              422  STORE_FAST               'actualr'

 L. 359       424  LOAD_CONST               0
              426  STORE_FAST               'actuali'
            428_0  COME_FROM           418  '418'

 L. 360       428  LOAD_FAST                'iscomplexobj'
              430  LOAD_FAST                'desired'
              432  CALL_FUNCTION_1       1  ''
          434_436  POP_JUMP_IF_FALSE   456  'to 456'

 L. 361       438  LOAD_FAST                'real'
              440  LOAD_FAST                'desired'
              442  CALL_FUNCTION_1       1  ''
              444  STORE_FAST               'desiredr'

 L. 362       446  LOAD_FAST                'imag'
              448  LOAD_FAST                'desired'
              450  CALL_FUNCTION_1       1  ''
              452  STORE_FAST               'desiredi'
              454  JUMP_FORWARD        464  'to 464'
            456_0  COME_FROM           434  '434'

 L. 364       456  LOAD_FAST                'desired'
              458  STORE_FAST               'desiredr'

 L. 365       460  LOAD_CONST               0
              462  STORE_FAST               'desiredi'
            464_0  COME_FROM           454  '454'

 L. 366       464  SETUP_FINALLY       490  'to 490'

 L. 367       466  LOAD_GLOBAL              assert_equal
              468  LOAD_FAST                'actualr'
              470  LOAD_FAST                'desiredr'
              472  CALL_FUNCTION_2       2  ''
              474  POP_TOP          

 L. 368       476  LOAD_GLOBAL              assert_equal
              478  LOAD_FAST                'actuali'
              480  LOAD_FAST                'desiredi'
              482  CALL_FUNCTION_2       2  ''
              484  POP_TOP          
              486  POP_BLOCK        
              488  JUMP_FORWARD        520  'to 520'
            490_0  COME_FROM_FINALLY   464  '464'

 L. 369       490  DUP_TOP          
              492  LOAD_GLOBAL              AssertionError
              494  COMPARE_OP               exception-match
          496_498  POP_JUMP_IF_FALSE   518  'to 518'
              500  POP_TOP          
              502  POP_TOP          
              504  POP_TOP          

 L. 370       506  LOAD_GLOBAL              AssertionError
              508  LOAD_FAST                'msg'
              510  CALL_FUNCTION_1       1  ''
              512  RAISE_VARARGS_1       1  'exception instance'
              514  POP_EXCEPT       
              516  JUMP_FORWARD        520  'to 520'
            518_0  COME_FROM           496  '496'
              518  END_FINALLY      
            520_0  COME_FROM           516  '516'
            520_1  COME_FROM           488  '488'
            520_2  COME_FROM           388  '388'

 L. 373       520  LOAD_FAST                'isscalar'
              522  LOAD_FAST                'desired'
              524  CALL_FUNCTION_1       1  ''
              526  LOAD_FAST                'isscalar'
              528  LOAD_FAST                'actual'
              530  CALL_FUNCTION_1       1  ''
              532  COMPARE_OP               !=
          534_536  POP_JUMP_IF_FALSE   546  'to 546'

 L. 374       538  LOAD_GLOBAL              AssertionError
              540  LOAD_FAST                'msg'
              542  CALL_FUNCTION_1       1  ''
              544  RAISE_VARARGS_1       1  'exception instance'
            546_0  COME_FROM           534  '534'

 L. 376       546  SETUP_FINALLY       624  'to 624'

 L. 377       548  LOAD_GLOBAL              isnat
              550  LOAD_FAST                'desired'
              552  CALL_FUNCTION_1       1  ''
              554  STORE_FAST               'isdesnat'

 L. 378       556  LOAD_GLOBAL              isnat
              558  LOAD_FAST                'actual'
              560  CALL_FUNCTION_1       1  ''
              562  STORE_FAST               'isactnat'

 L. 379       564  LOAD_GLOBAL              array
              566  LOAD_FAST                'desired'
              568  CALL_FUNCTION_1       1  ''
              570  LOAD_ATTR                dtype
              572  LOAD_ATTR                type
              574  LOAD_GLOBAL              array
              576  LOAD_FAST                'actual'
              578  CALL_FUNCTION_1       1  ''
              580  LOAD_ATTR                dtype
              582  LOAD_ATTR                type
              584  COMPARE_OP               ==
              586  STORE_FAST               'dtypes_match'

 L. 380       588  LOAD_FAST                'isdesnat'
          590_592  POP_JUMP_IF_FALSE   620  'to 620'
              594  LOAD_FAST                'isactnat'
          596_598  POP_JUMP_IF_FALSE   620  'to 620'

 L. 383       600  LOAD_FAST                'dtypes_match'
          602_604  POP_JUMP_IF_FALSE   612  'to 612'

 L. 384       606  POP_BLOCK        
              608  LOAD_CONST               None
              610  RETURN_VALUE     
            612_0  COME_FROM           602  '602'

 L. 386       612  LOAD_GLOBAL              AssertionError
              614  LOAD_FAST                'msg'
              616  CALL_FUNCTION_1       1  ''
              618  RAISE_VARARGS_1       1  'exception instance'
            620_0  COME_FROM           596  '596'
            620_1  COME_FROM           590  '590'
              620  POP_BLOCK        
              622  JUMP_FORWARD        652  'to 652'
            624_0  COME_FROM_FINALLY   546  '546'

 L. 388       624  DUP_TOP          
              626  LOAD_GLOBAL              TypeError
              628  LOAD_GLOBAL              ValueError
              630  LOAD_GLOBAL              NotImplementedError
              632  BUILD_TUPLE_3         3 
              634  COMPARE_OP               exception-match
          636_638  POP_JUMP_IF_FALSE   650  'to 650'
              640  POP_TOP          
              642  POP_TOP          
              644  POP_TOP          

 L. 389       646  POP_EXCEPT       
              648  JUMP_FORWARD        652  'to 652'
            650_0  COME_FROM           636  '636'
              650  END_FINALLY      
            652_0  COME_FROM           648  '648'
            652_1  COME_FROM           622  '622'

 L. 392       652  SETUP_FINALLY       790  'to 790'

 L. 393       654  LOAD_GLOBAL              gisnan
              656  LOAD_FAST                'desired'
              658  CALL_FUNCTION_1       1  ''
              660  STORE_FAST               'isdesnan'

 L. 394       662  LOAD_GLOBAL              gisnan
              664  LOAD_FAST                'actual'
              666  CALL_FUNCTION_1       1  ''
              668  STORE_FAST               'isactnan'

 L. 395       670  LOAD_FAST                'isdesnan'
          672_674  POP_JUMP_IF_FALSE   688  'to 688'
              676  LOAD_FAST                'isactnan'
          678_680  POP_JUMP_IF_FALSE   688  'to 688'

 L. 396       682  POP_BLOCK        
              684  LOAD_CONST               None
              686  RETURN_VALUE     
            688_0  COME_FROM           678  '678'
            688_1  COME_FROM           672  '672'

 L. 399       688  LOAD_GLOBAL              array
              690  LOAD_FAST                'actual'
              692  CALL_FUNCTION_1       1  ''
              694  STORE_FAST               'array_actual'

 L. 400       696  LOAD_GLOBAL              array
              698  LOAD_FAST                'desired'
              700  CALL_FUNCTION_1       1  ''
              702  STORE_FAST               'array_desired'

 L. 401       704  LOAD_FAST                'array_actual'
              706  LOAD_ATTR                dtype
              708  LOAD_ATTR                char
              710  LOAD_STR                 'Mm'
              712  COMPARE_OP               in
          714_716  POP_JUMP_IF_TRUE    732  'to 732'

 L. 402       718  LOAD_FAST                'array_desired'
              720  LOAD_ATTR                dtype
              722  LOAD_ATTR                char
              724  LOAD_STR                 'Mm'
              726  COMPARE_OP               in

 L. 401   728_730  POP_JUMP_IF_FALSE   740  'to 740'
            732_0  COME_FROM           714  '714'

 L. 408       732  LOAD_GLOBAL              NotImplementedError
              734  LOAD_STR                 'cannot compare to a scalar with a different type'
              736  CALL_FUNCTION_1       1  ''
              738  RAISE_VARARGS_1       1  'exception instance'
            740_0  COME_FROM           728  '728'

 L. 411       740  LOAD_FAST                'desired'
              742  LOAD_CONST               0
              744  COMPARE_OP               ==
          746_748  POP_JUMP_IF_FALSE   786  'to 786'
              750  LOAD_FAST                'actual'
              752  LOAD_CONST               0
              754  COMPARE_OP               ==
          756_758  POP_JUMP_IF_FALSE   786  'to 786'

 L. 412       760  LOAD_FAST                'signbit'
              762  LOAD_FAST                'desired'
              764  CALL_FUNCTION_1       1  ''
              766  LOAD_FAST                'signbit'
              768  LOAD_FAST                'actual'
              770  CALL_FUNCTION_1       1  ''
              772  COMPARE_OP               ==
          774_776  POP_JUMP_IF_TRUE    786  'to 786'

 L. 413       778  LOAD_ASSERT              AssertionError
              780  LOAD_FAST                'msg'
              782  CALL_FUNCTION_1       1  ''
              784  RAISE_VARARGS_1       1  'exception instance'
            786_0  COME_FROM           774  '774'
            786_1  COME_FROM           756  '756'
            786_2  COME_FROM           746  '746'
              786  POP_BLOCK        
              788  JUMP_FORWARD        818  'to 818'
            790_0  COME_FROM_FINALLY   652  '652'

 L. 415       790  DUP_TOP          
              792  LOAD_GLOBAL              TypeError
              794  LOAD_GLOBAL              ValueError
              796  LOAD_GLOBAL              NotImplementedError
              798  BUILD_TUPLE_3         3 
              800  COMPARE_OP               exception-match
          802_804  POP_JUMP_IF_FALSE   816  'to 816'
              806  POP_TOP          
              808  POP_TOP          
              810  POP_TOP          

 L. 416       812  POP_EXCEPT       
              814  JUMP_FORWARD        818  'to 818'
            816_0  COME_FROM           802  '802'
              816  END_FINALLY      
            818_0  COME_FROM           814  '814'
            818_1  COME_FROM           788  '788'

 L. 418       818  SETUP_FINALLY       842  'to 842'

 L. 420       820  LOAD_FAST                'desired'
              822  LOAD_FAST                'actual'
              824  COMPARE_OP               ==
          826_828  POP_JUMP_IF_TRUE    838  'to 838'

 L. 421       830  LOAD_ASSERT              AssertionError
              832  LOAD_FAST                'msg'
              834  CALL_FUNCTION_1       1  ''
              836  RAISE_VARARGS_1       1  'exception instance'
            838_0  COME_FROM           826  '826'
              838  POP_BLOCK        
              840  JUMP_FORWARD        910  'to 910'
            842_0  COME_FROM_FINALLY   818  '818'

 L. 423       842  DUP_TOP          
              844  LOAD_GLOBAL              DeprecationWarning
              846  LOAD_GLOBAL              FutureWarning
              848  BUILD_TUPLE_2         2 
              850  COMPARE_OP               exception-match
          852_854  POP_JUMP_IF_FALSE   908  'to 908'
              856  POP_TOP          
              858  STORE_FAST               'e'
              860  POP_TOP          
              862  SETUP_FINALLY       896  'to 896'

 L. 425       864  LOAD_STR                 'elementwise == comparison'
              866  LOAD_FAST                'e'
              868  LOAD_ATTR                args
              870  LOAD_CONST               0
              872  BINARY_SUBSCR    
              874  COMPARE_OP               in
          876_878  POP_JUMP_IF_FALSE   890  'to 890'

 L. 426       880  LOAD_GLOBAL              AssertionError
              882  LOAD_FAST                'msg'
              884  CALL_FUNCTION_1       1  ''
              886  RAISE_VARARGS_1       1  'exception instance'
              888  JUMP_FORWARD        892  'to 892'
            890_0  COME_FROM           876  '876'

 L. 428       890  RAISE_VARARGS_0       0  'reraise'
            892_0  COME_FROM           888  '888'
              892  POP_BLOCK        
              894  BEGIN_FINALLY    
            896_0  COME_FROM_FINALLY   862  '862'
              896  LOAD_CONST               None
              898  STORE_FAST               'e'
              900  DELETE_FAST              'e'
              902  END_FINALLY      
              904  POP_EXCEPT       
              906  JUMP_FORWARD        910  'to 910'
            908_0  COME_FROM           852  '852'
              908  END_FINALLY      
            910_0  COME_FROM           906  '906'
            910_1  COME_FROM           840  '840'

Parse error at or near `LOAD_CONST' instruction at offset 608


def print_assert_equal(test_string, actual, desired):
    """
    Test if two objects are equal, and print an error message if test fails.

    The test is performed with ``actual == desired``.

    Parameters
    ----------
    test_string : str
        The message supplied to AssertionError.
    actual : object
        The object to test for equality against `desired`.
    desired : object
        The expected result.

    Examples
    --------
    >>> np.testing.print_assert_equal('Test XYZ of func xyz', [0, 1], [0, 1])
    >>> np.testing.print_assert_equal('Test XYZ of func xyz', [0, 1], [0, 2])
    Traceback (most recent call last):
    ...
    AssertionError: Test XYZ of func xyz failed
    ACTUAL:
    [0, 1]
    DESIRED:
    [0, 2]

    """
    __tracebackhide__ = True
    import pprint
    if not actual == desired:
        msg = StringIO()
        msg.writetest_string
        msg.write' failed\nACTUAL: \n'
        pprint.pprintactualmsg
        msg.write'DESIRED: \n'
        pprint.pprintdesiredmsg
        raise AssertionError(msg.getvalue())


def assert_almost_equal--- This code section failed: ---

 L. 541         0  LOAD_CONST               True
                2  STORE_FAST               '__tracebackhide__'

 L. 542         4  LOAD_CONST               0
                6  LOAD_CONST               ('ndarray',)
                8  IMPORT_NAME_ATTR         numpy.core
               10  IMPORT_FROM              ndarray
               12  STORE_FAST               'ndarray'
               14  POP_TOP          

 L. 543        16  LOAD_CONST               0
               18  LOAD_CONST               ('iscomplexobj', 'real', 'imag')
               20  IMPORT_NAME_ATTR         numpy.lib
               22  IMPORT_FROM              iscomplexobj
               24  STORE_FAST               'iscomplexobj'
               26  IMPORT_FROM              real
               28  STORE_FAST               'real'
               30  IMPORT_FROM              imag
               32  STORE_FAST               'imag'
               34  POP_TOP          

 L. 548        36  SETUP_FINALLY        58  'to 58'

 L. 549        38  LOAD_FAST                'iscomplexobj'
               40  LOAD_DEREF               'actual'
               42  CALL_FUNCTION_1       1  ''
               44  JUMP_IF_TRUE_OR_POP    52  'to 52'
               46  LOAD_FAST                'iscomplexobj'
               48  LOAD_DEREF               'desired'
               50  CALL_FUNCTION_1       1  ''
             52_0  COME_FROM            44  '44'
               52  STORE_FAST               'usecomplex'
               54  POP_BLOCK        
               56  JUMP_FORWARD         82  'to 82'
             58_0  COME_FROM_FINALLY    36  '36'

 L. 550        58  DUP_TOP          
               60  LOAD_GLOBAL              ValueError
               62  COMPARE_OP               exception-match
               64  POP_JUMP_IF_FALSE    80  'to 80'
               66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          

 L. 551        72  LOAD_CONST               False
               74  STORE_FAST               'usecomplex'
               76  POP_EXCEPT       
               78  JUMP_FORWARD         82  'to 82'
             80_0  COME_FROM            64  '64'
               80  END_FINALLY      
             82_0  COME_FROM            78  '78'
             82_1  COME_FROM            56  '56'

 L. 553        82  LOAD_CLOSURE             'actual'
               84  LOAD_CLOSURE             'decimal'
               86  LOAD_CLOSURE             'desired'
               88  LOAD_CLOSURE             'err_msg'
               90  LOAD_CLOSURE             'verbose'
               92  BUILD_TUPLE_5         5 
               94  LOAD_CODE                <code_object _build_err_msg>
               96  LOAD_STR                 'assert_almost_equal.<locals>._build_err_msg'
               98  MAKE_FUNCTION_8          'closure'
              100  STORE_FAST               '_build_err_msg'

 L. 558       102  LOAD_FAST                'usecomplex'
              104  POP_JUMP_IF_FALSE   238  'to 238'

 L. 559       106  LOAD_FAST                'iscomplexobj'
              108  LOAD_DEREF               'actual'
              110  CALL_FUNCTION_1       1  ''
              112  POP_JUMP_IF_FALSE   132  'to 132'

 L. 560       114  LOAD_FAST                'real'
              116  LOAD_DEREF               'actual'
              118  CALL_FUNCTION_1       1  ''
              120  STORE_FAST               'actualr'

 L. 561       122  LOAD_FAST                'imag'
              124  LOAD_DEREF               'actual'
              126  CALL_FUNCTION_1       1  ''
              128  STORE_FAST               'actuali'
              130  JUMP_FORWARD        140  'to 140'
            132_0  COME_FROM           112  '112'

 L. 563       132  LOAD_DEREF               'actual'
              134  STORE_FAST               'actualr'

 L. 564       136  LOAD_CONST               0
              138  STORE_FAST               'actuali'
            140_0  COME_FROM           130  '130'

 L. 565       140  LOAD_FAST                'iscomplexobj'
              142  LOAD_DEREF               'desired'
              144  CALL_FUNCTION_1       1  ''
              146  POP_JUMP_IF_FALSE   166  'to 166'

 L. 566       148  LOAD_FAST                'real'
              150  LOAD_DEREF               'desired'
              152  CALL_FUNCTION_1       1  ''
              154  STORE_FAST               'desiredr'

 L. 567       156  LOAD_FAST                'imag'
              158  LOAD_DEREF               'desired'
              160  CALL_FUNCTION_1       1  ''
              162  STORE_FAST               'desiredi'
              164  JUMP_FORWARD        174  'to 174'
            166_0  COME_FROM           146  '146'

 L. 569       166  LOAD_DEREF               'desired'
              168  STORE_FAST               'desiredr'

 L. 570       170  LOAD_CONST               0
              172  STORE_FAST               'desiredi'
            174_0  COME_FROM           164  '164'

 L. 571       174  SETUP_FINALLY       208  'to 208'

 L. 572       176  LOAD_GLOBAL              assert_almost_equal
              178  LOAD_FAST                'actualr'
              180  LOAD_FAST                'desiredr'
              182  LOAD_DEREF               'decimal'
              184  LOAD_CONST               ('decimal',)
              186  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              188  POP_TOP          

 L. 573       190  LOAD_GLOBAL              assert_almost_equal
              192  LOAD_FAST                'actuali'
              194  LOAD_FAST                'desiredi'
              196  LOAD_DEREF               'decimal'
              198  LOAD_CONST               ('decimal',)
              200  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              202  POP_TOP          
              204  POP_BLOCK        
              206  JUMP_FORWARD        238  'to 238'
            208_0  COME_FROM_FINALLY   174  '174'

 L. 574       208  DUP_TOP          
              210  LOAD_GLOBAL              AssertionError
              212  COMPARE_OP               exception-match
              214  POP_JUMP_IF_FALSE   236  'to 236'
              216  POP_TOP          
              218  POP_TOP          
              220  POP_TOP          

 L. 575       222  LOAD_GLOBAL              AssertionError
              224  LOAD_FAST                '_build_err_msg'
              226  CALL_FUNCTION_0       0  ''
              228  CALL_FUNCTION_1       1  ''
              230  RAISE_VARARGS_1       1  'exception instance'
              232  POP_EXCEPT       
              234  JUMP_FORWARD        238  'to 238'
            236_0  COME_FROM           214  '214'
              236  END_FINALLY      
            238_0  COME_FROM           234  '234'
            238_1  COME_FROM           206  '206'
            238_2  COME_FROM           104  '104'

 L. 577       238  LOAD_GLOBAL              isinstance
              240  LOAD_DEREF               'actual'
              242  LOAD_FAST                'ndarray'
              244  LOAD_GLOBAL              tuple
              246  LOAD_GLOBAL              list
              248  BUILD_TUPLE_3         3 
              250  CALL_FUNCTION_2       2  ''
          252_254  POP_JUMP_IF_TRUE    274  'to 274'

 L. 578       256  LOAD_GLOBAL              isinstance
              258  LOAD_DEREF               'desired'
              260  LOAD_FAST                'ndarray'
              262  LOAD_GLOBAL              tuple
              264  LOAD_GLOBAL              list
              266  BUILD_TUPLE_3         3 
              268  CALL_FUNCTION_2       2  ''

 L. 577   270_272  POP_JUMP_IF_FALSE   288  'to 288'
            274_0  COME_FROM           252  '252'

 L. 579       274  LOAD_GLOBAL              assert_array_almost_equal
              276  LOAD_DEREF               'actual'
              278  LOAD_DEREF               'desired'
              280  LOAD_DEREF               'decimal'
              282  LOAD_DEREF               'err_msg'
              284  CALL_FUNCTION_4       4  ''
              286  RETURN_VALUE     
            288_0  COME_FROM           270  '270'

 L. 580       288  SETUP_FINALLY       392  'to 392'

 L. 584       290  LOAD_GLOBAL              gisfinite
              292  LOAD_DEREF               'desired'
              294  CALL_FUNCTION_1       1  ''
          296_298  POP_JUMP_IF_FALSE   310  'to 310'
              300  LOAD_GLOBAL              gisfinite
              302  LOAD_DEREF               'actual'
              304  CALL_FUNCTION_1       1  ''
          306_308  POP_JUMP_IF_TRUE    388  'to 388'
            310_0  COME_FROM           296  '296'

 L. 585       310  LOAD_GLOBAL              gisnan
              312  LOAD_DEREF               'desired'
              314  CALL_FUNCTION_1       1  ''
          316_318  POP_JUMP_IF_TRUE    330  'to 330'
              320  LOAD_GLOBAL              gisnan
              322  LOAD_DEREF               'actual'
              324  CALL_FUNCTION_1       1  ''
          326_328  POP_JUMP_IF_FALSE   362  'to 362'
            330_0  COME_FROM           316  '316'

 L. 586       330  LOAD_GLOBAL              gisnan
              332  LOAD_DEREF               'desired'
              334  CALL_FUNCTION_1       1  ''
          336_338  POP_JUMP_IF_FALSE   350  'to 350'
              340  LOAD_GLOBAL              gisnan
              342  LOAD_DEREF               'actual'
              344  CALL_FUNCTION_1       1  ''
          346_348  POP_JUMP_IF_TRUE    382  'to 382'
            350_0  COME_FROM           336  '336'

 L. 587       350  LOAD_ASSERT              AssertionError
              352  LOAD_FAST                '_build_err_msg'
              354  CALL_FUNCTION_0       0  ''
              356  CALL_FUNCTION_1       1  ''
              358  RAISE_VARARGS_1       1  'exception instance'
              360  JUMP_FORWARD        382  'to 382'
            362_0  COME_FROM           326  '326'

 L. 589       362  LOAD_DEREF               'desired'
              364  LOAD_DEREF               'actual'
              366  COMPARE_OP               ==
          368_370  POP_JUMP_IF_TRUE    382  'to 382'

 L. 590       372  LOAD_ASSERT              AssertionError
              374  LOAD_FAST                '_build_err_msg'
              376  CALL_FUNCTION_0       0  ''
              378  CALL_FUNCTION_1       1  ''
              380  RAISE_VARARGS_1       1  'exception instance'
            382_0  COME_FROM           368  '368'
            382_1  COME_FROM           360  '360'
            382_2  COME_FROM           346  '346'

 L. 591       382  POP_BLOCK        
              384  LOAD_CONST               None
              386  RETURN_VALUE     
            388_0  COME_FROM           306  '306'
              388  POP_BLOCK        
              390  JUMP_FORWARD        418  'to 418'
            392_0  COME_FROM_FINALLY   288  '288'

 L. 592       392  DUP_TOP          
              394  LOAD_GLOBAL              NotImplementedError
              396  LOAD_GLOBAL              TypeError
              398  BUILD_TUPLE_2         2 
              400  COMPARE_OP               exception-match
          402_404  POP_JUMP_IF_FALSE   416  'to 416'
              406  POP_TOP          
              408  POP_TOP          
              410  POP_TOP          

 L. 593       412  POP_EXCEPT       
              414  JUMP_FORWARD        418  'to 418'
            416_0  COME_FROM           402  '402'
              416  END_FINALLY      
            418_0  COME_FROM           414  '414'
            418_1  COME_FROM           390  '390'

 L. 594       418  LOAD_GLOBAL              abs
              420  LOAD_DEREF               'desired'
              422  LOAD_DEREF               'actual'
              424  BINARY_SUBTRACT  
              426  CALL_FUNCTION_1       1  ''
              428  LOAD_CONST               1.5
              430  LOAD_CONST               10.0
              432  LOAD_DEREF               'decimal'
              434  UNARY_NEGATIVE   
              436  BINARY_POWER     
              438  BINARY_MULTIPLY  
              440  COMPARE_OP               >=
          442_444  POP_JUMP_IF_FALSE   456  'to 456'

 L. 595       446  LOAD_GLOBAL              AssertionError
              448  LOAD_FAST                '_build_err_msg'
              450  CALL_FUNCTION_0       0  ''
              452  CALL_FUNCTION_1       1  ''
              454  RAISE_VARARGS_1       1  'exception instance'
            456_0  COME_FROM           442  '442'

Parse error at or near `COME_FROM' instruction at offset 388_0


def assert_approx_equal--- This code section failed: ---

 L. 656         0  LOAD_CONST               True
                2  STORE_FAST               '__tracebackhide__'

 L. 657         4  LOAD_CONST               0
                6  LOAD_CONST               None
                8  IMPORT_NAME              numpy
               10  STORE_FAST               'np'

 L. 659        12  LOAD_GLOBAL              map
               14  LOAD_GLOBAL              float
               16  LOAD_FAST                'actual'
               18  LOAD_FAST                'desired'
               20  BUILD_TUPLE_2         2 
               22  CALL_FUNCTION_2       2  ''
               24  UNPACK_SEQUENCE_2     2 
               26  STORE_FAST               'actual'
               28  STORE_FAST               'desired'

 L. 660        30  LOAD_FAST                'desired'
               32  LOAD_FAST                'actual'
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE    42  'to 42'

 L. 661        38  LOAD_CONST               None
               40  RETURN_VALUE     
             42_0  COME_FROM            36  '36'

 L. 664        42  LOAD_FAST                'np'
               44  LOAD_ATTR                errstate
               46  LOAD_STR                 'ignore'
               48  LOAD_CONST               ('invalid',)
               50  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               52  SETUP_WITH          108  'to 108'
               54  POP_TOP          

 L. 665        56  LOAD_CONST               0.5
               58  LOAD_FAST                'np'
               60  LOAD_METHOD              abs
               62  LOAD_FAST                'desired'
               64  CALL_METHOD_1         1  ''
               66  LOAD_FAST                'np'
               68  LOAD_METHOD              abs
               70  LOAD_FAST                'actual'
               72  CALL_METHOD_1         1  ''
               74  BINARY_ADD       
               76  BINARY_MULTIPLY  
               78  STORE_FAST               'scale'

 L. 666        80  LOAD_FAST                'np'
               82  LOAD_METHOD              power
               84  LOAD_CONST               10
               86  LOAD_FAST                'np'
               88  LOAD_METHOD              floor
               90  LOAD_FAST                'np'
               92  LOAD_METHOD              log10
               94  LOAD_FAST                'scale'
               96  CALL_METHOD_1         1  ''
               98  CALL_METHOD_1         1  ''
              100  CALL_METHOD_2         2  ''
              102  STORE_FAST               'scale'
              104  POP_BLOCK        
              106  BEGIN_FINALLY    
            108_0  COME_FROM_WITH       52  '52'
              108  WITH_CLEANUP_START
              110  WITH_CLEANUP_FINISH
              112  END_FINALLY      

 L. 667       114  SETUP_FINALLY       128  'to 128'

 L. 668       116  LOAD_FAST                'desired'
              118  LOAD_FAST                'scale'
              120  BINARY_TRUE_DIVIDE
              122  STORE_FAST               'sc_desired'
              124  POP_BLOCK        
              126  JUMP_FORWARD        152  'to 152'
            128_0  COME_FROM_FINALLY   114  '114'

 L. 669       128  DUP_TOP          
              130  LOAD_GLOBAL              ZeroDivisionError
              132  COMPARE_OP               exception-match
              134  POP_JUMP_IF_FALSE   150  'to 150'
              136  POP_TOP          
              138  POP_TOP          
              140  POP_TOP          

 L. 670       142  LOAD_CONST               0.0
              144  STORE_FAST               'sc_desired'
              146  POP_EXCEPT       
              148  JUMP_FORWARD        152  'to 152'
            150_0  COME_FROM           134  '134'
              150  END_FINALLY      
            152_0  COME_FROM           148  '148'
            152_1  COME_FROM           126  '126'

 L. 671       152  SETUP_FINALLY       166  'to 166'

 L. 672       154  LOAD_FAST                'actual'
              156  LOAD_FAST                'scale'
              158  BINARY_TRUE_DIVIDE
              160  STORE_FAST               'sc_actual'
              162  POP_BLOCK        
              164  JUMP_FORWARD        190  'to 190'
            166_0  COME_FROM_FINALLY   152  '152'

 L. 673       166  DUP_TOP          
              168  LOAD_GLOBAL              ZeroDivisionError
              170  COMPARE_OP               exception-match
              172  POP_JUMP_IF_FALSE   188  'to 188'
              174  POP_TOP          
              176  POP_TOP          
              178  POP_TOP          

 L. 674       180  LOAD_CONST               0.0
              182  STORE_FAST               'sc_actual'
              184  POP_EXCEPT       
              186  JUMP_FORWARD        190  'to 190'
            188_0  COME_FROM           172  '172'
              188  END_FINALLY      
            190_0  COME_FROM           186  '186'
            190_1  COME_FROM           164  '164'

 L. 675       190  LOAD_GLOBAL              build_err_msg

 L. 676       192  LOAD_FAST                'actual'
              194  LOAD_FAST                'desired'
              196  BUILD_LIST_2          2 

 L. 676       198  LOAD_FAST                'err_msg'

 L. 677       200  LOAD_STR                 'Items are not equal to %d significant digits:'
              202  LOAD_FAST                'significant'
              204  BINARY_MODULO    

 L. 678       206  LOAD_FAST                'verbose'

 L. 675       208  LOAD_CONST               ('header', 'verbose')
              210  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              212  STORE_FAST               'msg'

 L. 679       214  SETUP_FINALLY       310  'to 310'

 L. 683       216  LOAD_GLOBAL              gisfinite
              218  LOAD_FAST                'desired'
              220  CALL_FUNCTION_1       1  ''
              222  POP_JUMP_IF_FALSE   234  'to 234'
              224  LOAD_GLOBAL              gisfinite
              226  LOAD_FAST                'actual'
              228  CALL_FUNCTION_1       1  ''
          230_232  POP_JUMP_IF_TRUE    306  'to 306'
            234_0  COME_FROM           222  '222'

 L. 684       234  LOAD_GLOBAL              gisnan
              236  LOAD_FAST                'desired'
              238  CALL_FUNCTION_1       1  ''
              240  POP_JUMP_IF_TRUE    252  'to 252'
              242  LOAD_GLOBAL              gisnan
              244  LOAD_FAST                'actual'
              246  CALL_FUNCTION_1       1  ''
          248_250  POP_JUMP_IF_FALSE   282  'to 282'
            252_0  COME_FROM           240  '240'

 L. 685       252  LOAD_GLOBAL              gisnan
              254  LOAD_FAST                'desired'
              256  CALL_FUNCTION_1       1  ''
          258_260  POP_JUMP_IF_FALSE   272  'to 272'
              262  LOAD_GLOBAL              gisnan
              264  LOAD_FAST                'actual'
              266  CALL_FUNCTION_1       1  ''
          268_270  POP_JUMP_IF_TRUE    300  'to 300'
            272_0  COME_FROM           258  '258'

 L. 686       272  LOAD_ASSERT              AssertionError
              274  LOAD_FAST                'msg'
              276  CALL_FUNCTION_1       1  ''
              278  RAISE_VARARGS_1       1  'exception instance'
              280  JUMP_FORWARD        300  'to 300'
            282_0  COME_FROM           248  '248'

 L. 688       282  LOAD_FAST                'desired'
              284  LOAD_FAST                'actual'
              286  COMPARE_OP               ==
          288_290  POP_JUMP_IF_TRUE    300  'to 300'

 L. 689       292  LOAD_ASSERT              AssertionError
              294  LOAD_FAST                'msg'
              296  CALL_FUNCTION_1       1  ''
              298  RAISE_VARARGS_1       1  'exception instance'
            300_0  COME_FROM           288  '288'
            300_1  COME_FROM           280  '280'
            300_2  COME_FROM           268  '268'

 L. 690       300  POP_BLOCK        
              302  LOAD_CONST               None
              304  RETURN_VALUE     
            306_0  COME_FROM           230  '230'
              306  POP_BLOCK        
              308  JUMP_FORWARD        336  'to 336'
            310_0  COME_FROM_FINALLY   214  '214'

 L. 691       310  DUP_TOP          
              312  LOAD_GLOBAL              TypeError
              314  LOAD_GLOBAL              NotImplementedError
              316  BUILD_TUPLE_2         2 
              318  COMPARE_OP               exception-match
          320_322  POP_JUMP_IF_FALSE   334  'to 334'
              324  POP_TOP          
              326  POP_TOP          
              328  POP_TOP          

 L. 692       330  POP_EXCEPT       
              332  JUMP_FORWARD        336  'to 336'
            334_0  COME_FROM           320  '320'
              334  END_FINALLY      
            336_0  COME_FROM           332  '332'
            336_1  COME_FROM           308  '308'

 L. 693       336  LOAD_FAST                'np'
              338  LOAD_METHOD              abs
              340  LOAD_FAST                'sc_desired'
              342  LOAD_FAST                'sc_actual'
              344  BINARY_SUBTRACT  
              346  CALL_METHOD_1         1  ''
              348  LOAD_FAST                'np'
              350  LOAD_METHOD              power
              352  LOAD_CONST               10.0
              354  LOAD_FAST                'significant'
              356  LOAD_CONST               1
              358  BINARY_SUBTRACT  
              360  UNARY_NEGATIVE   
              362  CALL_METHOD_2         2  ''
              364  COMPARE_OP               >=
          366_368  POP_JUMP_IF_FALSE   378  'to 378'

 L. 694       370  LOAD_GLOBAL              AssertionError
              372  LOAD_FAST                'msg'
              374  CALL_FUNCTION_1       1  ''
              376  RAISE_VARARGS_1       1  'exception instance'
            378_0  COME_FROM           366  '366'

Parse error at or near `COME_FROM' instruction at offset 306_0


def assert_array_compare--- This code section failed: ---

 L. 700         0  LOAD_CONST               True
                2  STORE_FAST               '__tracebackhide__'

 L. 701         4  LOAD_CONST               0
                6  LOAD_CONST               ('array', 'array2string', 'isnan', 'inf', 'bool_', 'errstate', 'all', 'max', 'object_')
                8  IMPORT_NAME_ATTR         numpy.core
               10  IMPORT_FROM              array
               12  STORE_FAST               'array'
               14  IMPORT_FROM              array2string
               16  STORE_FAST               'array2string'
               18  IMPORT_FROM              isnan
               20  STORE_FAST               'isnan'
               22  IMPORT_FROM              inf
               24  STORE_DEREF              'inf'
               26  IMPORT_FROM              bool_
               28  STORE_DEREF              'bool_'
               30  IMPORT_FROM              errstate
               32  STORE_FAST               'errstate'
               34  IMPORT_FROM              all
               36  STORE_FAST               'all'
               38  IMPORT_FROM              max
               40  STORE_FAST               'max'
               42  IMPORT_FROM              object_
               44  STORE_FAST               'object_'
               46  POP_TOP          

 L. 703        48  LOAD_FAST                'array'
               50  LOAD_FAST                'x'
               52  LOAD_CONST               False
               54  LOAD_CONST               True
               56  LOAD_CONST               ('copy', 'subok')
               58  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               60  STORE_FAST               'x'

 L. 704        62  LOAD_FAST                'array'
               64  LOAD_FAST                'y'
               66  LOAD_CONST               False
               68  LOAD_CONST               True
               70  LOAD_CONST               ('copy', 'subok')
               72  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               74  STORE_FAST               'y'

 L. 707        76  LOAD_FAST                'x'
               78  LOAD_FAST                'y'
               80  ROT_TWO          
               82  STORE_FAST               'ox'
               84  STORE_FAST               'oy'

 L. 709        86  LOAD_CODE                <code_object isnumber>
               88  LOAD_STR                 'assert_array_compare.<locals>.isnumber'
               90  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               92  STORE_FAST               'isnumber'

 L. 712        94  LOAD_CODE                <code_object istime>
               96  LOAD_STR                 'assert_array_compare.<locals>.istime'
               98  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              100  STORE_FAST               'istime'

 L. 715       102  LOAD_FAST                'isnan'
              104  LOAD_STR                 'nan'
              106  BUILD_TUPLE_2         2 
              108  LOAD_CLOSURE             'bool_'
              110  LOAD_CLOSURE             'err_msg'
              112  LOAD_CLOSURE             'header'
              114  LOAD_CLOSURE             'precision'
              116  LOAD_CLOSURE             'verbose'
              118  BUILD_TUPLE_5         5 
              120  LOAD_CODE                <code_object func_assert_same_pos>
              122  LOAD_STR                 'assert_array_compare.<locals>.func_assert_same_pos'
              124  MAKE_FUNCTION_9          'default, closure'
              126  STORE_FAST               'func_assert_same_pos'

 L. 750   128_130  SETUP_FINALLY       880  'to 880'

 L. 751       132  LOAD_FAST                'x'
              134  LOAD_ATTR                shape
              136  LOAD_CONST               ()
              138  COMPARE_OP               ==
              140  JUMP_IF_TRUE_OR_POP   162  'to 162'
              142  LOAD_FAST                'y'
              144  LOAD_ATTR                shape
              146  LOAD_CONST               ()
              148  COMPARE_OP               ==
              150  JUMP_IF_TRUE_OR_POP   162  'to 162'
              152  LOAD_FAST                'x'
              154  LOAD_ATTR                shape
              156  LOAD_FAST                'y'
              158  LOAD_ATTR                shape
              160  COMPARE_OP               ==
            162_0  COME_FROM           150  '150'
            162_1  COME_FROM           140  '140'
              162  STORE_FAST               'cond'

 L. 752       164  LOAD_FAST                'cond'
              166  POP_JUMP_IF_TRUE    216  'to 216'

 L. 753       168  LOAD_GLOBAL              build_err_msg
              170  LOAD_FAST                'x'
              172  LOAD_FAST                'y'
              174  BUILD_LIST_2          2 

 L. 754       176  LOAD_DEREF               'err_msg'

 L. 755       178  LOAD_STR                 '\n(shapes %s, %s mismatch)'
              180  LOAD_FAST                'x'
              182  LOAD_ATTR                shape

 L. 756       184  LOAD_FAST                'y'
              186  LOAD_ATTR                shape

 L. 755       188  BUILD_TUPLE_2         2 
              190  BINARY_MODULO    

 L. 754       192  BINARY_ADD       

 L. 757       194  LOAD_DEREF               'verbose'

 L. 757       196  LOAD_DEREF               'header'

 L. 758       198  LOAD_CONST               ('x', 'y')

 L. 758       200  LOAD_DEREF               'precision'

 L. 753       202  LOAD_CONST               ('verbose', 'header', 'names', 'precision')
              204  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              206  STORE_FAST               'msg'

 L. 759       208  LOAD_GLOBAL              AssertionError
              210  LOAD_FAST                'msg'
              212  CALL_FUNCTION_1       1  ''
              214  RAISE_VARARGS_1       1  'exception instance'
            216_0  COME_FROM           166  '166'

 L. 761       216  LOAD_DEREF               'bool_'
              218  LOAD_CONST               False
              220  CALL_FUNCTION_1       1  ''
              222  STORE_FAST               'flagged'

 L. 762       224  LOAD_FAST                'isnumber'
              226  LOAD_FAST                'x'
              228  CALL_FUNCTION_1       1  ''
          230_232  POP_JUMP_IF_FALSE   330  'to 330'
              234  LOAD_FAST                'isnumber'
              236  LOAD_FAST                'y'
              238  CALL_FUNCTION_1       1  ''
          240_242  POP_JUMP_IF_FALSE   330  'to 330'

 L. 763       244  LOAD_FAST                'equal_nan'
          246_248  POP_JUMP_IF_FALSE   266  'to 266'

 L. 764       250  LOAD_FAST                'func_assert_same_pos'
              252  LOAD_FAST                'x'
              254  LOAD_FAST                'y'
              256  LOAD_FAST                'isnan'
              258  LOAD_STR                 'nan'
              260  LOAD_CONST               ('func', 'hasval')
              262  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              264  STORE_FAST               'flagged'
            266_0  COME_FROM           246  '246'

 L. 766       266  LOAD_FAST                'equal_inf'
          268_270  POP_JUMP_IF_FALSE   390  'to 390'

 L. 767       272  LOAD_FAST                'flagged'
              274  LOAD_FAST                'func_assert_same_pos'
              276  LOAD_FAST                'x'
              278  LOAD_FAST                'y'

 L. 768       280  LOAD_CLOSURE             'inf'
              282  BUILD_TUPLE_1         1 
              284  LOAD_LAMBDA              '<code_object <lambda>>'
              286  LOAD_STR                 'assert_array_compare.<locals>.<lambda>'
              288  MAKE_FUNCTION_8          'closure'

 L. 769       290  LOAD_STR                 '+inf'

 L. 767       292  LOAD_CONST               ('func', 'hasval')
              294  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              296  INPLACE_OR       
              298  STORE_FAST               'flagged'

 L. 770       300  LOAD_FAST                'flagged'
              302  LOAD_FAST                'func_assert_same_pos'
              304  LOAD_FAST                'x'
              306  LOAD_FAST                'y'

 L. 771       308  LOAD_CLOSURE             'inf'
              310  BUILD_TUPLE_1         1 
              312  LOAD_LAMBDA              '<code_object <lambda>>'
              314  LOAD_STR                 'assert_array_compare.<locals>.<lambda>'
              316  MAKE_FUNCTION_8          'closure'

 L. 772       318  LOAD_STR                 '-inf'

 L. 770       320  LOAD_CONST               ('func', 'hasval')
              322  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              324  INPLACE_OR       
              326  STORE_FAST               'flagged'
              328  JUMP_FORWARD        390  'to 390'
            330_0  COME_FROM           240  '240'
            330_1  COME_FROM           230  '230'

 L. 774       330  LOAD_FAST                'istime'
              332  LOAD_FAST                'x'
              334  CALL_FUNCTION_1       1  ''
          336_338  POP_JUMP_IF_FALSE   390  'to 390'
              340  LOAD_FAST                'istime'
              342  LOAD_FAST                'y'
              344  CALL_FUNCTION_1       1  ''
          346_348  POP_JUMP_IF_FALSE   390  'to 390'

 L. 776       350  LOAD_FAST                'equal_nan'
          352_354  POP_JUMP_IF_FALSE   390  'to 390'
              356  LOAD_FAST                'x'
              358  LOAD_ATTR                dtype
              360  LOAD_ATTR                type
              362  LOAD_FAST                'y'
              364  LOAD_ATTR                dtype
              366  LOAD_ATTR                type
              368  COMPARE_OP               ==
          370_372  POP_JUMP_IF_FALSE   390  'to 390'

 L. 777       374  LOAD_FAST                'func_assert_same_pos'
              376  LOAD_FAST                'x'
              378  LOAD_FAST                'y'
              380  LOAD_GLOBAL              isnat
              382  LOAD_STR                 'NaT'
              384  LOAD_CONST               ('func', 'hasval')
              386  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              388  STORE_FAST               'flagged'
            390_0  COME_FROM           370  '370'
            390_1  COME_FROM           352  '352'
            390_2  COME_FROM           346  '346'
            390_3  COME_FROM           336  '336'
            390_4  COME_FROM           328  '328'
            390_5  COME_FROM           268  '268'

 L. 779       390  LOAD_FAST                'flagged'
              392  LOAD_ATTR                ndim
              394  LOAD_CONST               0
              396  COMPARE_OP               >
          398_400  POP_JUMP_IF_FALSE   444  'to 444'

 L. 780       402  LOAD_FAST                'x'
              404  LOAD_FAST                'flagged'
              406  UNARY_INVERT     
              408  BINARY_SUBSCR    
              410  LOAD_FAST                'y'
              412  LOAD_FAST                'flagged'
              414  UNARY_INVERT     
              416  BINARY_SUBSCR    
              418  ROT_TWO          
              420  STORE_FAST               'x'
              422  STORE_FAST               'y'

 L. 782       424  LOAD_FAST                'x'
              426  LOAD_ATTR                size
              428  LOAD_CONST               0
              430  COMPARE_OP               ==
          432_434  POP_JUMP_IF_FALSE   456  'to 456'

 L. 783       436  POP_BLOCK        
              438  LOAD_CONST               None
              440  RETURN_VALUE     
              442  JUMP_FORWARD        456  'to 456'
            444_0  COME_FROM           398  '398'

 L. 784       444  LOAD_FAST                'flagged'
          446_448  POP_JUMP_IF_FALSE   456  'to 456'

 L. 786       450  POP_BLOCK        
              452  LOAD_CONST               None
              454  RETURN_VALUE     
            456_0  COME_FROM           446  '446'
            456_1  COME_FROM           442  '442'
            456_2  COME_FROM           432  '432'

 L. 788       456  LOAD_FAST                'comparison'
              458  LOAD_FAST                'x'
              460  LOAD_FAST                'y'
              462  CALL_FUNCTION_2       2  ''
              464  STORE_FAST               'val'

 L. 790       466  LOAD_GLOBAL              isinstance
              468  LOAD_FAST                'val'
              470  LOAD_GLOBAL              bool
              472  CALL_FUNCTION_2       2  ''
          474_476  POP_JUMP_IF_FALSE   494  'to 494'

 L. 791       478  LOAD_FAST                'val'
              480  STORE_FAST               'cond'

 L. 792       482  LOAD_FAST                'array'
              484  LOAD_FAST                'val'
              486  BUILD_LIST_1          1 
              488  CALL_FUNCTION_1       1  ''
              490  STORE_FAST               'reduced'
              492  JUMP_FORWARD        510  'to 510'
            494_0  COME_FROM           474  '474'

 L. 794       494  LOAD_FAST                'val'
              496  LOAD_METHOD              ravel
              498  CALL_METHOD_0         0  ''
              500  STORE_FAST               'reduced'

 L. 795       502  LOAD_FAST                'reduced'
              504  LOAD_METHOD              all
              506  CALL_METHOD_0         0  ''
              508  STORE_FAST               'cond'
            510_0  COME_FROM           492  '492'

 L. 801       510  LOAD_FAST                'cond'
              512  LOAD_CONST               True
              514  COMPARE_OP               !=
          516_518  POP_JUMP_IF_FALSE   876  'to 876'

 L. 802       520  LOAD_FAST                'reduced'
              522  LOAD_ATTR                size
              524  LOAD_FAST                'reduced'
              526  LOAD_ATTR                sum
              528  LOAD_GLOBAL              intp
              530  LOAD_CONST               ('dtype',)
              532  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              534  BINARY_SUBTRACT  
              536  STORE_FAST               'n_mismatch'

 L. 803       538  LOAD_FAST                'flagged'
              540  LOAD_ATTR                ndim
              542  LOAD_CONST               0
              544  COMPARE_OP               !=
          546_548  POP_JUMP_IF_FALSE   556  'to 556'
              550  LOAD_FAST                'flagged'
              552  LOAD_ATTR                size
              554  JUMP_FORWARD        560  'to 560'
            556_0  COME_FROM           546  '546'
              556  LOAD_FAST                'reduced'
              558  LOAD_ATTR                size
            560_0  COME_FROM           554  '554'
              560  STORE_FAST               'n_elements'

 L. 804       562  LOAD_CONST               100
              564  LOAD_FAST                'n_mismatch'
              566  BINARY_MULTIPLY  
              568  LOAD_FAST                'n_elements'
              570  BINARY_TRUE_DIVIDE
              572  STORE_FAST               'percent_mismatch'

 L. 806       574  LOAD_STR                 'Mismatched elements: {} / {} ({:.3g}%)'
              576  LOAD_METHOD              format

 L. 807       578  LOAD_FAST                'n_mismatch'

 L. 807       580  LOAD_FAST                'n_elements'

 L. 807       582  LOAD_FAST                'percent_mismatch'

 L. 806       584  CALL_METHOD_3         3  ''

 L. 805       586  BUILD_LIST_1          1 
              588  STORE_FAST               'remarks'

 L. 809       590  LOAD_FAST                'errstate'
              592  LOAD_STR                 'ignore'
              594  LOAD_STR                 'ignore'
              596  LOAD_CONST               ('invalid', 'divide')
              598  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              600  SETUP_WITH          820  'to 820'
              602  POP_TOP          

 L. 811       604  LOAD_GLOBAL              contextlib
              606  LOAD_METHOD              suppress
              608  LOAD_GLOBAL              TypeError
              610  CALL_METHOD_1         1  ''
              612  SETUP_WITH          810  'to 810'
              614  POP_TOP          

 L. 812       616  LOAD_GLOBAL              abs
              618  LOAD_FAST                'x'
              620  LOAD_FAST                'y'
              622  BINARY_SUBTRACT  
              624  CALL_FUNCTION_1       1  ''
              626  STORE_FAST               'error'

 L. 813       628  LOAD_FAST                'max'
              630  LOAD_FAST                'error'
              632  CALL_FUNCTION_1       1  ''
              634  STORE_FAST               'max_abs_error'

 L. 814       636  LOAD_GLOBAL              getattr
              638  LOAD_FAST                'error'
              640  LOAD_STR                 'dtype'
              642  LOAD_FAST                'object_'
              644  CALL_FUNCTION_3       3  ''
              646  LOAD_FAST                'object_'
              648  COMPARE_OP               ==
          650_652  POP_JUMP_IF_FALSE   674  'to 674'

 L. 815       654  LOAD_FAST                'remarks'
              656  LOAD_METHOD              append
              658  LOAD_STR                 'Max absolute difference: '

 L. 816       660  LOAD_GLOBAL              str
              662  LOAD_FAST                'max_abs_error'
              664  CALL_FUNCTION_1       1  ''

 L. 815       666  BINARY_ADD       
              668  CALL_METHOD_1         1  ''
              670  POP_TOP          
              672  JUMP_FORWARD        692  'to 692'
            674_0  COME_FROM           650  '650'

 L. 818       674  LOAD_FAST                'remarks'
              676  LOAD_METHOD              append
              678  LOAD_STR                 'Max absolute difference: '

 L. 819       680  LOAD_FAST                'array2string'
              682  LOAD_FAST                'max_abs_error'
              684  CALL_FUNCTION_1       1  ''

 L. 818       686  BINARY_ADD       
              688  CALL_METHOD_1         1  ''
              690  POP_TOP          
            692_0  COME_FROM           672  '672'

 L. 824       692  LOAD_DEREF               'bool_'
              694  LOAD_FAST                'y'
              696  LOAD_CONST               0
              698  COMPARE_OP               !=
              700  CALL_FUNCTION_1       1  ''
              702  STORE_FAST               'nonzero'

 L. 825       704  LOAD_FAST                'all'
              706  LOAD_FAST                'nonzero'
              708  UNARY_INVERT     
              710  CALL_FUNCTION_1       1  ''
          712_714  POP_JUMP_IF_FALSE   726  'to 726'

 L. 826       716  LOAD_FAST                'array'
              718  LOAD_DEREF               'inf'
              720  CALL_FUNCTION_1       1  ''
              722  STORE_FAST               'max_rel_error'
              724  JUMP_FORWARD        750  'to 750'
            726_0  COME_FROM           712  '712'

 L. 828       726  LOAD_FAST                'max'
              728  LOAD_FAST                'error'
              730  LOAD_FAST                'nonzero'
              732  BINARY_SUBSCR    
              734  LOAD_GLOBAL              abs
              736  LOAD_FAST                'y'
              738  LOAD_FAST                'nonzero'
              740  BINARY_SUBSCR    
              742  CALL_FUNCTION_1       1  ''
              744  BINARY_TRUE_DIVIDE
              746  CALL_FUNCTION_1       1  ''
              748  STORE_FAST               'max_rel_error'
            750_0  COME_FROM           724  '724'

 L. 829       750  LOAD_GLOBAL              getattr
              752  LOAD_FAST                'error'
              754  LOAD_STR                 'dtype'
              756  LOAD_FAST                'object_'
              758  CALL_FUNCTION_3       3  ''
              760  LOAD_FAST                'object_'
              762  COMPARE_OP               ==
          764_766  POP_JUMP_IF_FALSE   788  'to 788'

 L. 830       768  LOAD_FAST                'remarks'
              770  LOAD_METHOD              append
              772  LOAD_STR                 'Max relative difference: '

 L. 831       774  LOAD_GLOBAL              str
              776  LOAD_FAST                'max_rel_error'
              778  CALL_FUNCTION_1       1  ''

 L. 830       780  BINARY_ADD       
              782  CALL_METHOD_1         1  ''
              784  POP_TOP          
              786  JUMP_FORWARD        806  'to 806'
            788_0  COME_FROM           764  '764'

 L. 833       788  LOAD_FAST                'remarks'
              790  LOAD_METHOD              append
              792  LOAD_STR                 'Max relative difference: '

 L. 834       794  LOAD_FAST                'array2string'
              796  LOAD_FAST                'max_rel_error'
              798  CALL_FUNCTION_1       1  ''

 L. 833       800  BINARY_ADD       
              802  CALL_METHOD_1         1  ''
              804  POP_TOP          
            806_0  COME_FROM           786  '786'
              806  POP_BLOCK        
              808  BEGIN_FINALLY    
            810_0  COME_FROM_WITH      612  '612'
              810  WITH_CLEANUP_START
              812  WITH_CLEANUP_FINISH
              814  END_FINALLY      
              816  POP_BLOCK        
              818  BEGIN_FINALLY    
            820_0  COME_FROM_WITH      600  '600'
              820  WITH_CLEANUP_START
              822  WITH_CLEANUP_FINISH
              824  END_FINALLY      

 L. 836       826  LOAD_DEREF               'err_msg'
              828  LOAD_STR                 '\n'
              830  LOAD_STR                 '\n'
              832  LOAD_METHOD              join
              834  LOAD_FAST                'remarks'
              836  CALL_METHOD_1         1  ''
              838  BINARY_ADD       
              840  INPLACE_ADD      
              842  STORE_DEREF              'err_msg'

 L. 837       844  LOAD_GLOBAL              build_err_msg
              846  LOAD_FAST                'ox'
              848  LOAD_FAST                'oy'
              850  BUILD_LIST_2          2 
              852  LOAD_DEREF               'err_msg'

 L. 838       854  LOAD_DEREF               'verbose'

 L. 838       856  LOAD_DEREF               'header'

 L. 839       858  LOAD_CONST               ('x', 'y')

 L. 839       860  LOAD_DEREF               'precision'

 L. 837       862  LOAD_CONST               ('verbose', 'header', 'names', 'precision')
              864  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              866  STORE_FAST               'msg'

 L. 840       868  LOAD_GLOBAL              AssertionError
              870  LOAD_FAST                'msg'
              872  CALL_FUNCTION_1       1  ''
              874  RAISE_VARARGS_1       1  'exception instance'
            876_0  COME_FROM           516  '516'
              876  POP_BLOCK        
              878  JUMP_FORWARD        962  'to 962'
            880_0  COME_FROM_FINALLY   128  '128'

 L. 841       880  DUP_TOP          
              882  LOAD_GLOBAL              ValueError
              884  COMPARE_OP               exception-match
          886_888  POP_JUMP_IF_FALSE   960  'to 960'
              890  POP_TOP          
              892  POP_TOP          
              894  POP_TOP          

 L. 842       896  LOAD_CONST               0
              898  LOAD_CONST               None
              900  IMPORT_NAME              traceback
              902  STORE_FAST               'traceback'

 L. 843       904  LOAD_FAST                'traceback'
              906  LOAD_METHOD              format_exc
              908  CALL_METHOD_0         0  ''
              910  STORE_FAST               'efmt'

 L. 844       912  LOAD_STR                 'error during assertion:\n\n%s\n\n%s'
              914  LOAD_FAST                'efmt'
              916  LOAD_DEREF               'header'
              918  BUILD_TUPLE_2         2 
              920  BINARY_MODULO    
              922  STORE_DEREF              'header'

 L. 846       924  LOAD_GLOBAL              build_err_msg
              926  LOAD_FAST                'x'
              928  LOAD_FAST                'y'
              930  BUILD_LIST_2          2 
              932  LOAD_DEREF               'err_msg'
              934  LOAD_DEREF               'verbose'
              936  LOAD_DEREF               'header'

 L. 847       938  LOAD_CONST               ('x', 'y')

 L. 847       940  LOAD_DEREF               'precision'

 L. 846       942  LOAD_CONST               ('verbose', 'header', 'names', 'precision')
              944  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              946  STORE_FAST               'msg'

 L. 848       948  LOAD_GLOBAL              ValueError
              950  LOAD_FAST                'msg'
              952  CALL_FUNCTION_1       1  ''
              954  RAISE_VARARGS_1       1  'exception instance'
              956  POP_EXCEPT       
              958  JUMP_FORWARD        962  'to 962'
            960_0  COME_FROM           886  '886'
              960  END_FINALLY      
            962_0  COME_FROM           958  '958'
            962_1  COME_FROM           878  '878'

Parse error at or near `LOAD_CONST' instruction at offset 438


def assert_array_equal(x, y, err_msg='', verbose=True):
    """
    Raises an AssertionError if two array_like objects are not equal.

    Given two array_like objects, check that the shape is equal and all
    elements of these objects are equal (but see the Notes for the special
    handling of a scalar). An exception is raised at shape mismatch or
    conflicting values. In contrast to the standard usage in numpy, NaNs
    are compared like numbers, no assertion is raised if both objects have
    NaNs in the same positions.

    The usual caution for verifying equality with floating point numbers is
    advised.

    Parameters
    ----------
    x : array_like
        The actual object to check.
    y : array_like
        The desired, expected object.
    err_msg : str, optional
        The error message to be printed in case of failure.
    verbose : bool, optional
        If True, the conflicting values are appended to the error message.

    Raises
    ------
    AssertionError
        If actual and desired objects are not equal.

    See Also
    --------
    assert_allclose: Compare two array_like objects for equality with desired
                     relative and/or absolute precision.
    assert_array_almost_equal_nulp, assert_array_max_ulp, assert_equal

    Notes
    -----
    When one of `x` and `y` is a scalar and the other is array_like, the
    function checks that each element of the array_like object is equal to
    the scalar.

    Examples
    --------
    The first assert does not raise an exception:

    >>> np.testing.assert_array_equal([1.0,2.33333,np.nan],
    ...                               [np.exp(0),2.33333, np.nan])

    Assert fails with numerical imprecision with floats:

    >>> np.testing.assert_array_equal([1.0,np.pi,np.nan],
    ...                               [1, np.sqrt(np.pi)**2, np.nan])
    Traceback (most recent call last):
        ...
    AssertionError:
    Arrays are not equal
    <BLANKLINE>
    Mismatched elements: 1 / 3 (33.3%)
    Max absolute difference: 4.4408921e-16
    Max relative difference: 1.41357986e-16
     x: array([1.      , 3.141593,      nan])
     y: array([1.      , 3.141593,      nan])

    Use `assert_allclose` or one of the nulp (number of floating point values)
    functions for these cases instead:

    >>> np.testing.assert_allclose([1.0,np.pi,np.nan],
    ...                            [1, np.sqrt(np.pi)**2, np.nan],
    ...                            rtol=1e-10, atol=0)

    As mentioned in the Notes section, `assert_array_equal` has special
    handling for scalars. Here the test checks that each value in `x` is 3:

    >>> x = np.full((2, 5), fill_value=3)
    >>> np.testing.assert_array_equal(x, 3)

    """
    __tracebackhide__ = True
    assert_array_compare((operator.__eq__), x, y, err_msg=err_msg, verbose=verbose,
      header='Arrays are not equal')


def assert_array_almost_equal(x, y, decimal=6, err_msg='', verbose=True):
    """
    Raises an AssertionError if two objects are not equal up to desired
    precision.

    .. note:: It is recommended to use one of `assert_allclose`,
              `assert_array_almost_equal_nulp` or `assert_array_max_ulp`
              instead of this function for more consistent floating point
              comparisons.

    The test verifies identical shapes and that the elements of ``actual`` and
    ``desired`` satisfy.

        ``abs(desired-actual) < 1.5 * 10**(-decimal)``

    That is a looser test than originally documented, but agrees with what the
    actual implementation did up to rounding vagaries. An exception is raised
    at shape mismatch or conflicting values. In contrast to the standard usage
    in numpy, NaNs are compared like numbers, no assertion is raised if both
    objects have NaNs in the same positions.

    Parameters
    ----------
    x : array_like
        The actual object to check.
    y : array_like
        The desired, expected object.
    decimal : int, optional
        Desired precision, default is 6.
    err_msg : str, optional
      The error message to be printed in case of failure.
    verbose : bool, optional
        If True, the conflicting values are appended to the error message.

    Raises
    ------
    AssertionError
        If actual and desired are not equal up to specified precision.

    See Also
    --------
    assert_allclose: Compare two array_like objects for equality with desired
                     relative and/or absolute precision.
    assert_array_almost_equal_nulp, assert_array_max_ulp, assert_equal

    Examples
    --------
    the first assert does not raise an exception

    >>> np.testing.assert_array_almost_equal([1.0,2.333,np.nan],
    ...                                      [1.0,2.333,np.nan])

    >>> np.testing.assert_array_almost_equal([1.0,2.33333,np.nan],
    ...                                      [1.0,2.33339,np.nan], decimal=5)
    Traceback (most recent call last):
        ...
    AssertionError:
    Arrays are not almost equal to 5 decimals
    <BLANKLINE>
    Mismatched elements: 1 / 3 (33.3%)
    Max absolute difference: 6.e-05
    Max relative difference: 2.57136612e-05
     x: array([1.     , 2.33333,     nan])
     y: array([1.     , 2.33339,     nan])

    >>> np.testing.assert_array_almost_equal([1.0,2.33333,np.nan],
    ...                                      [1.0,2.33333, 5], decimal=5)
    Traceback (most recent call last):
        ...
    AssertionError:
    Arrays are not almost equal to 5 decimals
    <BLANKLINE>
    x and y nan location mismatch:
     x: array([1.     , 2.33333,     nan])
     y: array([1.     , 2.33333, 5.     ])

    """
    __tracebackhide__ = True
    from numpy.core import number, float_, result_type, array
    from numpy.core.numerictypes import issubdtype
    import numpy.core.fromnumeric as npany

    def compare--- This code section failed: ---

 L.1017         0  SETUP_FINALLY       122  'to 122'

 L.1018         2  LOAD_DEREF               'npany'
                4  LOAD_GLOBAL              gisinf
                6  LOAD_FAST                'x'
                8  CALL_FUNCTION_1       1  ''
               10  CALL_FUNCTION_1       1  ''
               12  POP_JUMP_IF_TRUE     26  'to 26'
               14  LOAD_DEREF               'npany'
               16  LOAD_GLOBAL              gisinf
               18  LOAD_FAST                'y'
               20  CALL_FUNCTION_1       1  ''
               22  CALL_FUNCTION_1       1  ''
               24  POP_JUMP_IF_FALSE   118  'to 118'
             26_0  COME_FROM            12  '12'

 L.1019        26  LOAD_GLOBAL              gisinf
               28  LOAD_FAST                'x'
               30  CALL_FUNCTION_1       1  ''
               32  STORE_FAST               'xinfid'

 L.1020        34  LOAD_GLOBAL              gisinf
               36  LOAD_FAST                'y'
               38  CALL_FUNCTION_1       1  ''
               40  STORE_FAST               'yinfid'

 L.1021        42  LOAD_FAST                'xinfid'
               44  LOAD_FAST                'yinfid'
               46  COMPARE_OP               ==
               48  LOAD_METHOD              all
               50  CALL_METHOD_0         0  ''
               52  POP_JUMP_IF_TRUE     60  'to 60'

 L.1022        54  POP_BLOCK        
               56  LOAD_CONST               False
               58  RETURN_VALUE     
             60_0  COME_FROM            52  '52'

 L.1024        60  LOAD_FAST                'x'
               62  LOAD_ATTR                size
               64  LOAD_FAST                'y'
               66  LOAD_ATTR                size
               68  DUP_TOP          
               70  ROT_THREE        
               72  COMPARE_OP               ==
               74  POP_JUMP_IF_FALSE    84  'to 84'
               76  LOAD_CONST               1
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE    98  'to 98'
               82  JUMP_FORWARD         88  'to 88'
             84_0  COME_FROM            74  '74'
               84  POP_TOP          
               86  JUMP_FORWARD         98  'to 98'
             88_0  COME_FROM            82  '82'

 L.1025        88  LOAD_FAST                'x'
               90  LOAD_FAST                'y'
               92  COMPARE_OP               ==
               94  POP_BLOCK        
               96  RETURN_VALUE     
             98_0  COME_FROM            86  '86'
             98_1  COME_FROM            80  '80'

 L.1026        98  LOAD_FAST                'x'
              100  LOAD_FAST                'xinfid'
              102  UNARY_INVERT     
              104  BINARY_SUBSCR    
              106  STORE_FAST               'x'

 L.1027       108  LOAD_FAST                'y'
              110  LOAD_FAST                'yinfid'
              112  UNARY_INVERT     
              114  BINARY_SUBSCR    
              116  STORE_FAST               'y'
            118_0  COME_FROM            24  '24'
              118  POP_BLOCK        
              120  JUMP_FORWARD        146  'to 146'
            122_0  COME_FROM_FINALLY     0  '0'

 L.1028       122  DUP_TOP          
              124  LOAD_GLOBAL              TypeError
              126  LOAD_GLOBAL              NotImplementedError
              128  BUILD_TUPLE_2         2 
              130  COMPARE_OP               exception-match
              132  POP_JUMP_IF_FALSE   144  'to 144'
              134  POP_TOP          
              136  POP_TOP          
              138  POP_TOP          

 L.1029       140  POP_EXCEPT       
              142  JUMP_FORWARD        146  'to 146'
            144_0  COME_FROM           132  '132'
              144  END_FINALLY      
            146_0  COME_FROM           142  '142'
            146_1  COME_FROM           120  '120'

 L.1033       146  LOAD_DEREF               'result_type'
              148  LOAD_FAST                'y'
              150  LOAD_CONST               1.0
              152  CALL_FUNCTION_2       2  ''
              154  STORE_FAST               'dtype'

 L.1034       156  LOAD_DEREF               'array'
              158  LOAD_FAST                'y'
              160  LOAD_FAST                'dtype'
              162  LOAD_CONST               False
              164  LOAD_CONST               True
              166  LOAD_CONST               ('dtype', 'copy', 'subok')
              168  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              170  STORE_FAST               'y'

 L.1035       172  LOAD_GLOBAL              abs
              174  LOAD_FAST                'x'
              176  LOAD_FAST                'y'
              178  BINARY_SUBTRACT  
              180  CALL_FUNCTION_1       1  ''
              182  STORE_FAST               'z'

 L.1037       184  LOAD_DEREF               'issubdtype'
              186  LOAD_FAST                'z'
              188  LOAD_ATTR                dtype
              190  LOAD_DEREF               'number'
              192  CALL_FUNCTION_2       2  ''
              194  POP_JUMP_IF_TRUE    206  'to 206'

 L.1038       196  LOAD_FAST                'z'
              198  LOAD_METHOD              astype
              200  LOAD_DEREF               'float_'
              202  CALL_METHOD_1         1  ''
              204  STORE_FAST               'z'
            206_0  COME_FROM           194  '194'

 L.1040       206  LOAD_FAST                'z'
              208  LOAD_CONST               1.5
              210  LOAD_CONST               10.0
              212  LOAD_DEREF               'decimal'
              214  UNARY_NEGATIVE   
              216  BINARY_POWER     
              218  BINARY_MULTIPLY  
              220  COMPARE_OP               <
              222  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 56

    assert_array_compare(compare, x, y, err_msg=err_msg, verbose=verbose, header=('Arrays are not almost equal to %d decimals' % decimal),
      precision=decimal)


def assert_array_less(x, y, err_msg='', verbose=True):
    """
    Raises an AssertionError if two array_like objects are not ordered by less
    than.

    Given two array_like objects, check that the shape is equal and all
    elements of the first object are strictly smaller than those of the
    second object. An exception is raised at shape mismatch or incorrectly
    ordered values. Shape mismatch does not raise if an object has zero
    dimension. In contrast to the standard usage in numpy, NaNs are
    compared, no assertion is raised if both objects have NaNs in the same
    positions.

    Parameters
    ----------
    x : array_like
      The smaller object to check.
    y : array_like
      The larger object to compare.
    err_msg : string
      The error message to be printed in case of failure.
    verbose : bool
        If True, the conflicting values are appended to the error message.

    Raises
    ------
    AssertionError
      If actual and desired objects are not equal.

    See Also
    --------
    assert_array_equal: tests objects for equality
    assert_array_almost_equal: test objects for equality up to precision

    Examples
    --------
    >>> np.testing.assert_array_less([1.0, 1.0, np.nan], [1.1, 2.0, np.nan])
    >>> np.testing.assert_array_less([1.0, 1.0, np.nan], [1, 2.0, np.nan])
    Traceback (most recent call last):
        ...
    AssertionError:
    Arrays are not less-ordered
    <BLANKLINE>
    Mismatched elements: 1 / 3 (33.3%)
    Max absolute difference: 1.
    Max relative difference: 0.5
     x: array([ 1.,  1., nan])
     y: array([ 1.,  2., nan])

    >>> np.testing.assert_array_less([1.0, 4.0], 3)
    Traceback (most recent call last):
        ...
    AssertionError:
    Arrays are not less-ordered
    <BLANKLINE>
    Mismatched elements: 1 / 2 (50%)
    Max absolute difference: 2.
    Max relative difference: 0.66666667
     x: array([1., 4.])
     y: array(3)

    >>> np.testing.assert_array_less([1.0, 2.0, 3.0], [4])
    Traceback (most recent call last):
        ...
    AssertionError:
    Arrays are not less-ordered
    <BLANKLINE>
    (shapes (3,), (1,) mismatch)
     x: array([1., 2., 3.])
     y: array([4])

    """
    __tracebackhide__ = True
    assert_array_compare((operator.__lt__), x, y, err_msg=err_msg, verbose=verbose,
      header='Arrays are not less-ordered',
      equal_inf=False)


def runstring(astr, dict):
    exec(astr, dict)


def assert_string_equal(actual, desired):
    """
    Test if two strings are equal.

    If the given strings are equal, `assert_string_equal` does nothing.
    If they are not equal, an AssertionError is raised, and the diff
    between the strings is shown.

    Parameters
    ----------
    actual : str
        The string to test for equality against the expected string.
    desired : str
        The expected string.

    Examples
    --------
    >>> np.testing.assert_string_equal('abc', 'abc')
    >>> np.testing.assert_string_equal('abc', 'abcd')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ...
    AssertionError: Differences in strings:
    - abc+ abcd?    +

    """
    __tracebackhide__ = True
    import difflib
    assert isinstance(actual, str), repr(type(actual))
    assert isinstance(desired, str), repr(type(desired))
    if desired == actual:
        return
    diff = list(difflib.Differ().compareactual.splitlinesTruedesired.splitlinesTrue)
    diff_list = []
    while True:
        if diff:
            d1 = diff.pop0
            if d1.startswith'  ':
                pass
            else:
                if d1.startswith'- ':
                    l = [
                     d1]
                    d2 = diff.pop0
                    if d2.startswith'? ':
                        l.appendd2
                        d2 = diff.pop0
                    assert d2.startswith'+ ', repr(d2)
                    l.appendd2
                    if diff:
                        d3 = diff.pop0
                        if d3.startswith'? ':
                            l.appendd3
                        else:
                            diff.insert0d3
                    if d2[2:] == d1[2:]:
                        pass
                    else:
                        diff_list.extendl
                    raise AssertionError(repr(d1))

    if not diff_list:
        return
    msg = 'Differences in strings:\n%s' % ''.joindiff_list.rstrip()
    if actual != desired:
        raise AssertionError(msg)


def rundocs(filename=None, raise_on_error=True):
    """
    Run doctests found in the given file.

    By default `rundocs` raises an AssertionError on failure.

    Parameters
    ----------
    filename : str
        The path to the file for which the doctests are run.
    raise_on_error : bool
        Whether to raise an AssertionError when a doctest fails. Default is
        True.

    Notes
    -----
    The doctests can be run by the user/developer by adding the ``doctests``
    argument to the ``test()`` call. For example, to run all tests (including
    doctests) for `numpy.lib`:

    >>> np.lib.test(doctests=True)  # doctest: +SKIP
    """
    from numpy.compat import npy_load_module
    import doctest
    if filename is None:
        f = sys._getframe1
        filename = f.f_globals['__file__']
    name = os.path.splitextos.path.basenamefilename[0]
    m = npy_load_module(name, filename)
    tests = doctest.DocTestFinder().findm
    runner = doctest.DocTestRunner(verbose=False)
    msg = []
    if raise_on_error:
        out = lambda s: msg.append(s)
    else:
        out = None
    for test in tests:
        runner.run(test, out=out)
    else:
        if runner.failures > 0:
            if raise_on_error:
                raise AssertionError('Some doctests failed:\n%s' % '\n'.join(msg))


def raises(*args):
    """Decorator to check for raised exceptions.

    The decorated test function must raise one of the passed exceptions to
    pass.  If you want to test many assertions about exceptions in a single
    test, you may want to use `assert_raises` instead.

    .. warning::
       This decorator is nose specific, do not use it if you are using a
       different test framework.

    Parameters
    ----------
    args : exceptions
        The test passes if any of the passed exceptions is raised.

    Raises
    ------
    AssertionError

    Examples
    --------

    Usage::

        @raises(TypeError, ValueError)
        def test_raises_type_error():
            raise TypeError("This test passes")

        @raises(Exception)
        def test_that_fails_by_passing():
            pass

    """
    nose = import_nose()
    return (nose.tools.raises)(*args)


import unittest

class _Dummy(unittest.TestCase):

    def nop(self):
        pass


_d = _Dummy('nop')

def assert_raises(*args, **kwargs):
    """
    assert_raises(exception_class, callable, *args, **kwargs)
    assert_raises(exception_class)

    Fail unless an exception of class exception_class is thrown
    by callable when invoked with arguments args and keyword
    arguments kwargs. If a different type of exception is
    thrown, it will not be caught, and the test case will be
    deemed to have suffered an error, exactly as for an
    unexpected exception.

    Alternatively, `assert_raises` can be used as a context manager:

    >>> from numpy.testing import assert_raises
    >>> with assert_raises(ZeroDivisionError):
    ...     1 / 0

    is equivalent to

    >>> def div(x, y):
    ...     return x / y
    >>> assert_raises(ZeroDivisionError, div, 1, 0)

    """
    __tracebackhide__ = True
    return (_d.assertRaises)(*args, **kwargs)


def assert_raises_regex(exception_class, expected_regexp, *args, **kwargs):
    """
    assert_raises_regex(exception_class, expected_regexp, callable, *args,
                        **kwargs)
    assert_raises_regex(exception_class, expected_regexp)

    Fail unless an exception of class exception_class and with message that
    matches expected_regexp is thrown by callable when invoked with arguments
    args and keyword arguments kwargs.

    Alternatively, can be used as a context manager like `assert_raises`.

    Name of this function adheres to Python 3.2+ reference, but should work in
    all versions down to 2.6.

    Notes
    -----
    .. versionadded:: 1.9.0

    """
    __tracebackhide__ = True
    return (_d.assertRaisesRegex)(exception_class, expected_regexp, *args, **kwargs)


def decorate_methods--- This code section failed: ---

 L.1375         0  LOAD_FAST                'testmatch'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    26  'to 26'

 L.1376         8  LOAD_GLOBAL              re
               10  LOAD_METHOD              compile
               12  LOAD_STR                 '(?:^|[\\\\b_\\\\.%s-])[Tt]est'
               14  LOAD_GLOBAL              os
               16  LOAD_ATTR                sep
               18  BINARY_MODULO    
               20  CALL_METHOD_1         1  ''
               22  STORE_FAST               'testmatch'
               24  JUMP_FORWARD         36  'to 36'
             26_0  COME_FROM             6  '6'

 L.1378        26  LOAD_GLOBAL              re
               28  LOAD_METHOD              compile
               30  LOAD_FAST                'testmatch'
               32  CALL_METHOD_1         1  ''
               34  STORE_FAST               'testmatch'
             36_0  COME_FROM            24  '24'

 L.1379        36  LOAD_FAST                'cls'
               38  LOAD_ATTR                __dict__
               40  STORE_FAST               'cls_attr'

 L.1382        42  LOAD_CONST               0
               44  LOAD_CONST               ('isfunction',)
               46  IMPORT_NAME              inspect
               48  IMPORT_FROM              isfunction
               50  STORE_DEREF              'isfunction'
               52  POP_TOP          

 L.1384        54  LOAD_CLOSURE             'isfunction'
               56  BUILD_TUPLE_1         1 
               58  LOAD_LISTCOMP            '<code_object <listcomp>>'
               60  LOAD_STR                 'decorate_methods.<locals>.<listcomp>'
               62  MAKE_FUNCTION_8          'closure'
               64  LOAD_FAST                'cls_attr'
               66  LOAD_METHOD              values
               68  CALL_METHOD_0         0  ''
               70  GET_ITER         
               72  CALL_FUNCTION_1       1  ''
               74  STORE_FAST               'methods'

 L.1385        76  LOAD_FAST                'methods'
               78  GET_ITER         
             80_0  COME_FROM           174  '174'
             80_1  COME_FROM           156  '156'
             80_2  COME_FROM           146  '146'
             80_3  COME_FROM           130  '130'
               80  FOR_ITER            176  'to 176'
               82  STORE_FAST               'function'

 L.1386        84  SETUP_FINALLY       114  'to 114'

 L.1387        86  LOAD_GLOBAL              hasattr
               88  LOAD_FAST                'function'
               90  LOAD_STR                 'compat_func_name'
               92  CALL_FUNCTION_2       2  ''
               94  POP_JUMP_IF_FALSE   104  'to 104'

 L.1388        96  LOAD_FAST                'function'
               98  LOAD_ATTR                compat_func_name
              100  STORE_FAST               'funcname'
              102  JUMP_FORWARD        110  'to 110'
            104_0  COME_FROM            94  '94'

 L.1390       104  LOAD_FAST                'function'
              106  LOAD_ATTR                __name__
              108  STORE_FAST               'funcname'
            110_0  COME_FROM           102  '102'
              110  POP_BLOCK        
              112  JUMP_FORWARD        138  'to 138'
            114_0  COME_FROM_FINALLY    84  '84'

 L.1391       114  DUP_TOP          
              116  LOAD_GLOBAL              AttributeError
              118  COMPARE_OP               exception-match
              120  POP_JUMP_IF_FALSE   136  'to 136'
              122  POP_TOP          
              124  POP_TOP          
              126  POP_TOP          

 L.1393       128  POP_EXCEPT       
              130  JUMP_BACK            80  'to 80'
              132  POP_EXCEPT       
              134  JUMP_FORWARD        138  'to 138'
            136_0  COME_FROM           120  '120'
              136  END_FINALLY      
            138_0  COME_FROM           134  '134'
            138_1  COME_FROM           112  '112'

 L.1394       138  LOAD_FAST                'testmatch'
              140  LOAD_METHOD              search
              142  LOAD_FAST                'funcname'
              144  CALL_METHOD_1         1  ''
              146  POP_JUMP_IF_FALSE_BACK    80  'to 80'
              148  LOAD_FAST                'funcname'
              150  LOAD_METHOD              startswith
              152  LOAD_STR                 '_'
              154  CALL_METHOD_1         1  ''
              156  POP_JUMP_IF_TRUE_BACK    80  'to 80'

 L.1395       158  LOAD_GLOBAL              setattr
              160  LOAD_FAST                'cls'
              162  LOAD_FAST                'funcname'
              164  LOAD_FAST                'decorator'
              166  LOAD_FAST                'function'
              168  CALL_FUNCTION_1       1  ''
              170  CALL_FUNCTION_3       3  ''
              172  POP_TOP          
              174  JUMP_BACK            80  'to 80'
            176_0  COME_FROM            80  '80'

Parse error at or near `COME_FROM' instruction at offset 136_0


def measure(code_str, times=1, label=None):
    """
    Return elapsed time for executing code in the namespace of the caller.

    The supplied code string is compiled with the Python builtin ``compile``.
    The precision of the timing is 10 milli-seconds. If the code will execute
    fast on this timescale, it can be executed many times to get reasonable
    timing accuracy.

    Parameters
    ----------
    code_str : str
        The code to be timed.
    times : int, optional
        The number of times the code is executed. Default is 1. The code is
        only compiled once.
    label : str, optional
        A label to identify `code_str` with. This is passed into ``compile``
        as the second argument (for run-time error messages).

    Returns
    -------
    elapsed : float
        Total elapsed time in seconds for executing `code_str` `times` times.

    Examples
    --------
    >>> times = 10
    >>> etime = np.testing.measure('for i in range(1000): np.sqrt(i**2)', times=times)
    >>> print("Time for a single execution : ", etime / times, "s")  # doctest: +SKIP
    Time for a single execution :  0.005 s

    """
    frame = sys._getframe(1)
    locs, globs = frame.f_locals, frame.f_globals
    code = compile(code_str, 'Test name: %s ' % label, 'exec')
    i = 0
    elapsed = jiffies()
    while True:
        if i < times:
            i += 1
            exec(code, globs, locs)

    elapsed = jiffies() - elapsed
    return 0.01 * elapsed


def _assert_valid_refcount(op):
    """
    Check that ufuncs don't mishandle refcount of object `1`.
    Used in a few regression tests.
    """
    if not HAS_REFCOUNT:
        return True
    import gc, numpy as np
    b = np.arange(10000).reshape100100
    c = b
    i = 1
    gc.disable()
    try:
        rc = sys.getrefcount(i)
        for j in range(15):
            d = op(b, c)
        else:
            assert_(sys.getrefcount(i) >= rc)

    finally:
        gc.enable()

    del d


def assert_allclose(actual, desired, rtol=1e-07, atol=0, equal_nan=True, err_msg='', verbose=True):
    """
    Raises an AssertionError if two objects are not equal up to desired
    tolerance.

    The test is equivalent to ``allclose(actual, desired, rtol, atol)`` (note
    that ``allclose`` has different default values). It compares the difference
    between `actual` and `desired` to ``atol + rtol * abs(desired)``.

    .. versionadded:: 1.5.0

    Parameters
    ----------
    actual : array_like
        Array obtained.
    desired : array_like
        Array desired.
    rtol : float, optional
        Relative tolerance.
    atol : float, optional
        Absolute tolerance.
    equal_nan : bool, optional.
        If True, NaNs will compare equal.
    err_msg : str, optional
        The error message to be printed in case of failure.
    verbose : bool, optional
        If True, the conflicting values are appended to the error message.

    Raises
    ------
    AssertionError
        If actual and desired are not equal up to specified precision.

    See Also
    --------
    assert_array_almost_equal_nulp, assert_array_max_ulp

    Examples
    --------
    >>> x = [1e-5, 1e-3, 1e-1]
    >>> y = np.arccos(np.cos(x))
    >>> np.testing.assert_allclose(x, y, rtol=1e-5, atol=0)

    """
    __tracebackhide__ = True
    import numpy as np

    def compare(x, y):
        return np.core.numeric.isclose(x, y, rtol=rtol, atol=atol, equal_nan=equal_nan)

    actual, desired = np.asanyarray(actual), np.asanyarray(desired)
    header = 'Not equal to tolerance rtol=%g, atol=%g' % (rtol, atol)
    assert_array_compare(compare, actual, desired, err_msg=(str(err_msg)), verbose=verbose,
      header=header,
      equal_nan=equal_nan)


def assert_array_almost_equal_nulp(x, y, nulp=1):
    """
    Compare two arrays relatively to their spacing.

    This is a relatively robust method to compare two arrays whose amplitude
    is variable.

    Parameters
    ----------
    x, y : array_like
        Input arrays.
    nulp : int, optional
        The maximum number of unit in the last place for tolerance (see Notes).
        Default is 1.

    Returns
    -------
    None

    Raises
    ------
    AssertionError
        If the spacing between `x` and `y` for one or more elements is larger
        than `nulp`.

    See Also
    --------
    assert_array_max_ulp : Check that all items of arrays differ in at most
        N Units in the Last Place.
    spacing : Return the distance between x and the nearest adjacent number.

    Notes
    -----
    An assertion is raised if the following condition is not met::

        abs(x - y) <= nulps * spacing(maximum(abs(x), abs(y)))

    Examples
    --------
    >>> x = np.array([1., 1e-10, 1e-20])
    >>> eps = np.finfo(x.dtype).eps
    >>> np.testing.assert_array_almost_equal_nulp(x, x*eps/2 + x)

    >>> np.testing.assert_array_almost_equal_nulp(x, x*eps + x)
    Traceback (most recent call last):
      ...
    AssertionError: X and Y are not equal to 1 ULP (max is 2)

    """
    __tracebackhide__ = True
    import numpy as np
    ax = np.abs(x)
    ay = np.abs(y)
    ref = nulp * np.spacing(np.where(ax > ay)axay)
    if not np.all(np.abs(x - y) <= ref):
        if np.iscomplexobj(x) or np.iscomplexobj(y):
            msg = 'X and Y are not equal to %d ULP' % nulp
        else:
            max_nulp = np.max(nulp_diff(x, y))
            msg = 'X and Y are not equal to %d ULP (max is %g)' % (nulp, max_nulp)
        raise AssertionError(msg)


def assert_array_max_ulp(a, b, maxulp=1, dtype=None):
    """
    Check that all items of arrays differ in at most N Units in the Last Place.

    Parameters
    ----------
    a, b : array_like
        Input arrays to be compared.
    maxulp : int, optional
        The maximum number of units in the last place that elements of `a` and
        `b` can differ. Default is 1.
    dtype : dtype, optional
        Data-type to convert `a` and `b` to if given. Default is None.

    Returns
    -------
    ret : ndarray
        Array containing number of representable floating point numbers between
        items in `a` and `b`.

    Raises
    ------
    AssertionError
        If one or more elements differ by more than `maxulp`.

    Notes
    -----
    For computing the ULP difference, this API does not differentiate between
    various representations of NAN (ULP difference between 0x7fc00000 and 0xffc00000
    is zero).

    See Also
    --------
    assert_array_almost_equal_nulp : Compare two arrays relatively to their
        spacing.

    Examples
    --------
    >>> a = np.linspace(0., 1., 100)
    >>> res = np.testing.assert_array_max_ulp(a, np.arcsin(np.sin(a)))

    """
    __tracebackhide__ = True
    import numpy as np
    ret = nulp_diff(a, b, dtype)
    assert np.all(ret <= maxulp), 'Arrays are not almost equal up to %g ULP (max difference is %g ULP)' % (
     maxulp, np.max(ret))
    return ret


def nulp_diff(x, y, dtype=None):
    """For each item in x and y, return the number of representable floating
    points between them.

    Parameters
    ----------
    x : array_like
        first input array
    y : array_like
        second input array
    dtype : dtype, optional
        Data-type to convert `x` and `y` to if given. Default is None.

    Returns
    -------
    nulp : array_like
        number of representable floating point numbers between each item in x
        and y.

    Notes
    -----
    For computing the ULP difference, this API does not differentiate between
    various representations of NAN (ULP difference between 0x7fc00000 and 0xffc00000
    is zero).

    Examples
    --------
    # By definition, epsilon is the smallest number such as 1 + eps != 1, so
    # there should be exactly one ULP between 1 and 1 + eps
    >>> nulp_diff(1, 1 + np.finfo(x.dtype).eps)
    1.0
    """
    import numpy as np
    if dtype:
        x = np.array(x, dtype=dtype)
        y = np.array(y, dtype=dtype)
    else:
        x = np.array(x)
        y = np.array(y)
    t = np.common_typexy
    if np.iscomplexobj(x) or (np.iscomplexobj(y)):
        raise NotImplementedError('_nulp not implemented for complex array')
    x = np.array([x], dtype=t)
    y = np.array([y], dtype=t)
    x[np.isnan(x)] = np.nan
    y[np.isnan(y)] = np.nan
    if not x.shape == y.shape:
        raise ValueError('x and y do not have the same shape: %s - %s' % (
         x.shape, y.shape))

    def _diff(rx, ry, vdt):
        diff = np.array((rx - ry), dtype=vdt)
        return np.abs(diff)

    rx = integer_repr(x)
    ry = integer_repr(y)
    return _diff(rx, ry, t)


def _integer_repr(x, vdt, comp):
    rx = x.view(vdt)
    if not rx.size == 1:
        rx[rx < 0] = comp - rx[(rx < 0)]
    elif rx < 0:
        rx = comp - rx
    return rx


def integer_repr(x):
    """Return the signed-magnitude interpretation of the binary representation of
    x."""
    import numpy as np
    if x.dtype == np.float16:
        return _integer_repr(x, np.int16, np.int16(-32768))
    if x.dtype == np.float32:
        return _integer_repr(x, np.int32, np.int32(-2147483648))
    if x.dtype == np.float64:
        return _integer_repr(x, np.int64, np.int64(-9223372036854775808))
    raise ValueError('Unsupported dtype %s' % x.dtype)


@contextlib.contextmanager
def _assert_warns_context(warning_class, name=None):
    __tracebackhide__ = True
    with suppress_warnings() as sup:
        l = sup.record(warning_class)
        yield
        if not len(l) > 0:
            name_str = ' when calling %s' % name if name is not None else ''
            raise AssertionError('No warning raised' + name_str)


def assert_warns(warning_class, *args, **kwargs):
    r"""
    Fail unless the given callable throws the specified warning.

    A warning of class warning_class should be thrown by the callable when
    invoked with arguments args and keyword arguments kwargs.
    If a different type of warning is thrown, it will not be caught.

    If called with all arguments other than the warning class omitted, may be
    used as a context manager:

        with assert_warns(SomeWarning):
            do_something()

    The ability to be used as a context manager is new in NumPy v1.11.0.

    .. versionadded:: 1.4.0

    Parameters
    ----------
    warning_class : class
        The class defining the warning that `func` is expected to throw.
    func : callable
        The callable to test.
    \*args : Arguments
        Arguments passed to `func`.
    \*\*kwargs : Kwargs
        Keyword arguments passed to `func`.

    Returns
    -------
    The value returned by `func`.

    """
    if not args:
        return _assert_warns_context(warning_class)
    func = args[0]
    args = args[1:]
    with _assert_warns_context(warning_class, name=(func.__name__)):
        return func(*args, **kwargs)


@contextlib.contextmanager
def _assert_no_warnings_context(name=None):
    __tracebackhide__ = True
    with warnings.catch_warnings(record=True) as l:
        warnings.simplefilter('always')
        yield
        if len(l) > 0:
            name_str = ' when calling %s' % name if name is not None else ''
            raise AssertionError('Got warnings%s: %s' % (name_str, l))


def assert_no_warnings(*args, **kwargs):
    r"""
    Fail if the given callable produces any warnings.

    If called with all arguments omitted, may be used as a context manager:

        with assert_no_warnings():
            do_something()

    The ability to be used as a context manager is new in NumPy v1.11.0.

    .. versionadded:: 1.7.0

    Parameters
    ----------
    func : callable
        The callable to test.
    \*args : Arguments
        Arguments passed to `func`.
    \*\*kwargs : Kwargs
        Keyword arguments passed to `func`.

    Returns
    -------
    The value returned by `func`.

    """
    if not args:
        return _assert_no_warnings_context()
    func = args[0]
    args = args[1:]
    with _assert_no_warnings_context(name=(func.__name__)):
        return func(*args, **kwargs)


def _gen_alignment_data(dtype=float32, type='binary', max_size=24):
    """
    generator producing data with different alignment and offsets
    to test simd vectorization

    Parameters
    ----------
    dtype : dtype
        data type to produce
    type : string
        'unary': create data for unary operations, creates one input
                 and output array
        'binary': create data for unary operations, creates two input
                 and output array
    max_size : integer
        maximum size of data to produce

    Returns
    -------
    if type is 'unary' yields one output, one input array and a message
    containing information on the data
    if type is 'binary' yields one output array, two input array and a message
    containing information on the data

    """
    ufmt = 'unary offset=(%d, %d), size=%d, dtype=%r, %s'
    bfmt = 'binary offset=(%d, %d, %d), size=%d, dtype=%r, %s'
    for o in range(3):
        for s in range(o + 2, max(o + 3, max_size)):
            if type == 'unary':
                inp = lambda: arange(s, dtype=dtype)[o:]
                out = empty((s,), dtype=dtype)[o:]
                yield (out, inp(), ufmt % (o, o, s, dtype, 'out of place'))
                d = inp()
                yield (d, d, ufmt % (o, o, s, dtype, 'in place'))
                yield (out[1:], inp()[:-1],
                 ufmt % (
                  o + 1, o, s - 1, dtype, 'out of place'))
                yield (out[:-1], inp()[1:],
                 ufmt % (
                  o, o + 1, s - 1, dtype, 'out of place'))
                yield (inp()[:-1], inp()[1:],
                 ufmt % (
                  o, o + 1, s - 1, dtype, 'aliased'))
                yield (inp()[1:], inp()[:-1],
                 ufmt % (
                  o + 1, o, s - 1, dtype, 'aliased'))
            if type == 'binary':
                inp1 = lambda: arange(s, dtype=dtype)[o:]
                inp2 = lambda: arange(s, dtype=dtype)[o:]
                out = empty((s,), dtype=dtype)[o:]
                yield (out, inp1(), inp2(),
                 bfmt % (
                  o, o, o, s, dtype, 'out of place'))
                d = inp1()
                yield (d, d, inp2(),
                 bfmt % (
                  o, o, o, s, dtype, 'in place1'))
                d = inp2()
                yield (d, inp1(), d,
                 bfmt % (
                  o, o, o, s, dtype, 'in place2'))
                yield (out[1:], inp1()[:-1], inp2()[:-1],
                 bfmt % (
                  o + 1, o, o, s - 1, dtype, 'out of place'))
                yield (out[:-1], inp1()[1:], inp2()[:-1],
                 bfmt % (
                  o, o + 1, o, s - 1, dtype, 'out of place'))
                yield (out[:-1], inp1()[:-1], inp2()[1:],
                 bfmt % (
                  o, o, o + 1, s - 1, dtype, 'out of place'))
                yield (inp1()[1:], inp1()[:-1], inp2()[:-1],
                 bfmt % (
                  o + 1, o, o, s - 1, dtype, 'aliased'))
                yield (inp1()[:-1], inp1()[1:], inp2()[:-1],
                 bfmt % (
                  o, o + 1, o, s - 1, dtype, 'aliased'))
                yield (inp1()[:-1], inp1()[:-1], inp2()[1:],
                 bfmt % (
                  o, o, o + 1, s - 1, dtype, 'aliased'))


class IgnoreException(Exception):
    __doc__ = 'Ignoring this exception due to disabled feature'


@contextlib.contextmanager
def tempdir(*args, **kwargs):
    """Context manager to provide a temporary test folder.

    All arguments are passed as this to the underlying tempfile.mkdtemp
    function.

    """
    tmpdir = mkdtemp(*args, **kwargs)
    try:
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir)


@contextlib.contextmanager
def temppath(*args, **kwargs):
    """Context manager for temporary files.

    Context manager that returns the path to a closed temporary file. Its
    parameters are the same as for tempfile.mkstemp and are passed directly
    to that function. The underlying file is removed when the context is
    exited, so it should be closed at that time.

    Windows does not allow a temporary file to be opened if it is already
    open, so the underlying file must be closed after opening before it
    can be opened again.

    """
    fd, path = mkstemp(*args, **kwargs)
    os.close(fd)
    try:
        yield path
    finally:
        os.remove(path)


class clear_and_catch_warnings(warnings.catch_warnings):
    __doc__ = " Context manager that resets warning registry for catching warnings\n\n    Warnings can be slippery, because, whenever a warning is triggered, Python\n    adds a ``__warningregistry__`` member to the *calling* module.  This makes\n    it impossible to retrigger the warning in this module, whatever you put in\n    the warnings filters.  This context manager accepts a sequence of `modules`\n    as a keyword argument to its constructor and:\n\n    * stores and removes any ``__warningregistry__`` entries in given `modules`\n      on entry;\n    * resets ``__warningregistry__`` to its previous state on exit.\n\n    This makes it possible to trigger any warning afresh inside the context\n    manager without disturbing the state of warnings outside.\n\n    For compatibility with Python 3.0, please consider all arguments to be\n    keyword-only.\n\n    Parameters\n    ----------\n    record : bool, optional\n        Specifies whether warnings should be captured by a custom\n        implementation of ``warnings.showwarning()`` and be appended to a list\n        returned by the context manager. Otherwise None is returned by the\n        context manager. The objects appended to the list are arguments whose\n        attributes mirror the arguments to ``showwarning()``.\n    modules : sequence, optional\n        Sequence of modules for which to reset warnings registry on entry and\n        restore on exit. To work correctly, all 'ignore' filters should\n        filter by one of these modules.\n\n    Examples\n    --------\n    >>> import warnings\n    >>> with np.testing.clear_and_catch_warnings(\n    ...         modules=[np.core.fromnumeric]):\n    ...     warnings.simplefilter('always')\n    ...     warnings.filterwarnings('ignore', module='np.core.fromnumeric')\n    ...     # do something that raises a warning but ignore those in\n    ...     # np.core.fromnumeric\n    "
    class_modules = ()

    def __init__(self, record=False, modules=()):
        self.modules = set(modules).union(self.class_modules)
        self._warnreg_copies = {}
        super(clear_and_catch_warnings, self).__init__(record=record)

    def __enter__(self):
        for mod in self.modules:
            if hasattr(mod, '__warningregistry__'):
                mod_reg = mod.__warningregistry__
                self._warnreg_copies[mod] = mod_reg.copy()
                mod_reg.clear()
        else:
            return super(clear_and_catch_warnings, self).__enter__()

    def __exit__(self, *exc_info):
        (super(clear_and_catch_warnings, self).__exit__)(*exc_info)
        for mod in self.modules:
            if hasattr(mod, '__warningregistry__'):
                mod.__warningregistry__.clear()
            if mod in self._warnreg_copies:
                mod.__warningregistry__.update(self._warnreg_copies[mod])


class suppress_warnings:
    __doc__ = '\n    Context manager and decorator doing much the same as\n    ``warnings.catch_warnings``.\n\n    However, it also provides a filter mechanism to work around\n    https://bugs.python.org/issue4180.\n\n    This bug causes Python before 3.4 to not reliably show warnings again\n    after they have been ignored once (even within catch_warnings). It\n    means that no "ignore" filter can be used easily, since following\n    tests might need to see the warning. Additionally it allows easier\n    specificity for testing warnings and can be nested.\n\n    Parameters\n    ----------\n    forwarding_rule : str, optional\n        One of "always", "once", "module", or "location". Analogous to\n        the usual warnings module filter mode, it is useful to reduce\n        noise mostly on the outmost level. Unsuppressed and unrecorded\n        warnings will be forwarded based on this rule. Defaults to "always".\n        "location" is equivalent to the warnings "default", match by exact\n        location the warning warning originated from.\n\n    Notes\n    -----\n    Filters added inside the context manager will be discarded again\n    when leaving it. Upon entering all filters defined outside a\n    context will be applied automatically.\n\n    When a recording filter is added, matching warnings are stored in the\n    ``log`` attribute as well as in the list returned by ``record``.\n\n    If filters are added and the ``module`` keyword is given, the\n    warning registry of this module will additionally be cleared when\n    applying it, entering the context, or exiting it. This could cause\n    warnings to appear a second time after leaving the context if they\n    were configured to be printed once (default) and were already\n    printed before the context was entered.\n\n    Nesting this context manager will work as expected when the\n    forwarding rule is "always" (default). Unfiltered and unrecorded\n    warnings will be passed out and be matched by the outer level.\n    On the outmost level they will be printed (or caught by another\n    warnings context). The forwarding rule argument can modify this\n    behaviour.\n\n    Like ``catch_warnings`` this context manager is not threadsafe.\n\n    Examples\n    --------\n\n    With a context manager::\n\n        with np.testing.suppress_warnings() as sup:\n            sup.filter(DeprecationWarning, "Some text")\n            sup.filter(module=np.ma.core)\n            log = sup.record(FutureWarning, "Does this occur?")\n            command_giving_warnings()\n            # The FutureWarning was given once, the filtered warnings were\n            # ignored. All other warnings abide outside settings (may be\n            # printed/error)\n            assert_(len(log) == 1)\n            assert_(len(sup.log) == 1)  # also stored in log attribute\n\n    Or as a decorator::\n\n        sup = np.testing.suppress_warnings()\n        sup.filter(module=np.ma.core)  # module must match exactly\n        @sup\n        def some_function():\n            # do something which causes a warning in np.ma.core\n            pass\n    '

    def __init__(self, forwarding_rule='always'):
        self._entered = False
        self._suppressions = []
        if forwarding_rule not in frozenset({'module', 'once', 'always', 'location'}):
            raise ValueError('unsupported forwarding rule.')
        self._forwarding_rule = forwarding_rule

    def _clear_registries(self):
        if hasattr(warnings, '_filters_mutated'):
            warnings._filters_mutated()
            return
        for module in self._tmp_modules:
            if hasattr(module, '__warningregistry__'):
                module.__warningregistry__.clear()

    def _filter(self, category=Warning, message='', module=None, record=False):
        if record:
            record = []
        else:
            record = None
        if self._entered:
            if module is None:
                warnings.filterwarnings('always',
                  category=category, message=message)
            else:
                module_regex = module.__name__.replace'.''\\.' + '$'
                warnings.filterwarnings('always',
                  category=category, message=message, module=module_regex)
                self._tmp_modules.add(module)
                self._clear_registries()
            self._tmp_suppressions.append((
             category, message, re.compilemessagere.I, module, record))
        else:
            self._suppressions.append((
             category, message, re.compilemessagere.I, module, record))
        return record

    def filter(self, category=Warning, message='', module=None):
        """
        Add a new suppressing filter or apply it if the state is entered.

        Parameters
        ----------
        category : class, optional
            Warning class to filter
        message : string, optional
            Regular expression matching the warning message.
        module : module, optional
            Module to filter for. Note that the module (and its file)
            must match exactly and cannot be a submodule. This may make
            it unreliable for external modules.

        Notes
        -----
        When added within a context, filters are only added inside
        the context and will be forgotten when the context is exited.
        """
        self._filter(category=category, message=message, module=module, record=False)

    def record(self, category=Warning, message='', module=None):
        """
        Append a new recording filter or apply it if the state is entered.

        All warnings matching will be appended to the ``log`` attribute.

        Parameters
        ----------
        category : class, optional
            Warning class to filter
        message : string, optional
            Regular expression matching the warning message.
        module : module, optional
            Module to filter for. Note that the module (and its file)
            must match exactly and cannot be a submodule. This may make
            it unreliable for external modules.

        Returns
        -------
        log : list
            A list which will be filled with all matched warnings.

        Notes
        -----
        When added within a context, filters are only added inside
        the context and will be forgotten when the context is exited.
        """
        return self._filter(category=category, message=message, module=module, record=True)

    def __enter__(self):
        if self._entered:
            raise RuntimeError('cannot enter suppress_warnings twice.')
        self._orig_show = warnings.showwarning
        self._filters = warnings.filters
        warnings.filters = self._filters[:]
        self._entered = True
        self._tmp_suppressions = []
        self._tmp_modules = set()
        self._forwarded = set()
        self.log = []
        for cat, mess, _, mod, log in self._suppressions:
            if log is not None:
                del log[:]
            if mod is None:
                warnings.filterwarnings('always',
                  category=cat, message=mess)
            else:
                module_regex = mod.__name__.replace'.''\\.' + '$'
                warnings.filterwarnings('always',
                  category=cat, message=mess, module=module_regex)
                self._tmp_modules.add(mod)
        else:
            warnings.showwarning = self._showwarning
            self._clear_registries()
            return self

    def __exit__(self, *exc_info):
        warnings.showwarning = self._orig_show
        warnings.filters = self._filters
        self._clear_registries()
        self._entered = False
        del self._orig_show
        del self._filters

    def _showwarning(self, message, category, filename, lineno, *args, use_warnmsg=None, **kwargs):
        for cat, _, pattern, mod, rec in (self._suppressions + self._tmp_suppressions)[::-1]:
            if issubclass(category, cat):
                if pattern.match(message.args[0]) is not None:
                    if mod is None:
                        if rec is not None:
                            msg = WarningMessage(message, category, filename, 
                             lineno, **kwargs)
                            self.log.append(msg)
                            rec.append(msg)
                        return None
                    if mod.__file__.startswith(filename):
                        if rec is not None:
                            msg = WarningMessage(message, category, filename, 
                             lineno, **kwargs)
                            self.log.append(msg)
                            rec.append(msg)
                        else:
                            return
        else:
            if self._forwarding_rule == 'always':
                if use_warnmsg is None:
                    (self._orig_show)(message, category, filename, lineno, *args, **kwargs)
                else:
                    self._orig_showmsg(use_warnmsg)
                return
            if self._forwarding_rule == 'once':
                signature = (
                 message.args, category)
            elif self._forwarding_rule == 'module':
                signature = (
                 message.args, category, filename)
            elif self._forwarding_rule == 'location':
                signature = (
                 message.args, category, filename, lineno)
            if signature in self._forwarded:
                return
            self._forwarded.add(signature)
            if use_warnmsg is None:
                (self._orig_show)(message, category, filename, lineno, *args, **kwargs)
            else:
                self._orig_showmsg(use_warnmsg)

    def __call__(self, func):
        """
        Function decorator to apply certain suppressions to a whole
        function.
        """

        @wraps(func)
        def new_func(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return new_func


@contextlib.contextmanager
def _assert_no_gc_cycles_context--- This code section failed: ---

 L.2296         0  LOAD_CONST               True
                2  STORE_FAST               '__tracebackhide__'

 L.2299         4  LOAD_GLOBAL              HAS_REFCOUNT
                6  POP_JUMP_IF_TRUE     18  'to 18'

 L.2300         8  LOAD_CONST               None
               10  YIELD_VALUE      
               12  POP_TOP          

 L.2301        14  LOAD_CONST               None
               16  RETURN_VALUE     
             18_0  COME_FROM             6  '6'

 L.2303        18  LOAD_GLOBAL              assert_
               20  LOAD_GLOBAL              gc
               22  LOAD_METHOD              isenabled
               24  CALL_METHOD_0         0  ''
               26  CALL_FUNCTION_1       1  ''
               28  POP_TOP          

 L.2304        30  LOAD_GLOBAL              gc
               32  LOAD_METHOD              disable
               34  CALL_METHOD_0         0  ''
               36  POP_TOP          

 L.2305        38  LOAD_GLOBAL              gc
               40  LOAD_METHOD              get_debug
               42  CALL_METHOD_0         0  ''
               44  STORE_FAST               'gc_debug'

 L.2306        46  SETUP_FINALLY       130  'to 130'

 L.2307        48  LOAD_GLOBAL              range
               50  LOAD_CONST               100
               52  CALL_FUNCTION_1       1  ''
               54  GET_ITER         
             56_0  COME_FROM            76  '76'
             56_1  COME_FROM            70  '70'
               56  FOR_ITER             78  'to 78'
               58  STORE_FAST               'i'

 L.2308        60  LOAD_GLOBAL              gc
               62  LOAD_METHOD              collect
               64  CALL_METHOD_0         0  ''
               66  LOAD_CONST               0
               68  COMPARE_OP               ==
               70  POP_JUMP_IF_FALSE_BACK    56  'to 56'

 L.2309        72  POP_TOP          
               74  BREAK_LOOP           86  'to 86'
               76  JUMP_BACK            56  'to 56'
             78_0  COME_FROM            56  '56'

 L.2311        78  LOAD_GLOBAL              RuntimeError

 L.2312        80  LOAD_STR                 'Unable to fully collect garbage - perhaps a __del__ method is creating more reference cycles?'

 L.2311        82  CALL_FUNCTION_1       1  ''
               84  RAISE_VARARGS_1       1  'exception instance'
             86_0  COME_FROM            74  '74'

 L.2315        86  LOAD_GLOBAL              gc
               88  LOAD_METHOD              set_debug
               90  LOAD_GLOBAL              gc
               92  LOAD_ATTR                DEBUG_SAVEALL
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          

 L.2316        98  LOAD_CONST               None
              100  YIELD_VALUE      
              102  POP_TOP          

 L.2319       104  LOAD_GLOBAL              gc
              106  LOAD_METHOD              collect
              108  CALL_METHOD_0         0  ''
              110  STORE_FAST               'n_objects_in_cycles'

 L.2320       112  LOAD_GLOBAL              gc
              114  LOAD_ATTR                garbage
              116  LOAD_CONST               None
              118  LOAD_CONST               None
              120  BUILD_SLICE_2         2 
              122  BINARY_SUBSCR    
              124  STORE_FAST               'objects_in_cycles'
              126  POP_BLOCK        
              128  BEGIN_FINALLY    
            130_0  COME_FROM_FINALLY    46  '46'

 L.2322       130  LOAD_GLOBAL              gc
              132  LOAD_ATTR                garbage
              134  LOAD_CONST               None
              136  LOAD_CONST               None
              138  BUILD_SLICE_2         2 
              140  DELETE_SUBSCR    

 L.2323       142  LOAD_GLOBAL              gc
              144  LOAD_METHOD              set_debug
              146  LOAD_FAST                'gc_debug'
              148  CALL_METHOD_1         1  ''
              150  POP_TOP          

 L.2324       152  LOAD_GLOBAL              gc
              154  LOAD_METHOD              enable
              156  CALL_METHOD_0         0  ''
              158  POP_TOP          
              160  END_FINALLY      

 L.2326       162  LOAD_FAST                'n_objects_in_cycles'
              164  POP_JUMP_IF_FALSE   226  'to 226'

 L.2327       166  LOAD_FAST                'name'
              168  LOAD_CONST               None
              170  COMPARE_OP               is-not
              172  POP_JUMP_IF_FALSE   182  'to 182'
              174  LOAD_STR                 ' when calling %s'
              176  LOAD_FAST                'name'
              178  BINARY_MODULO    
              180  JUMP_FORWARD        184  'to 184'
            182_0  COME_FROM           172  '172'
              182  LOAD_STR                 ''
            184_0  COME_FROM           180  '180'
              184  STORE_FAST               'name_str'

 L.2328       186  LOAD_GLOBAL              AssertionError

 L.2329       188  LOAD_STR                 'Reference cycles were found{}: {} objects were collected, of which {} are shown below:{}'
              190  LOAD_METHOD              format

 L.2332       192  LOAD_FAST                'name_str'

 L.2333       194  LOAD_FAST                'n_objects_in_cycles'

 L.2334       196  LOAD_GLOBAL              len
              198  LOAD_FAST                'objects_in_cycles'
              200  CALL_FUNCTION_1       1  ''

 L.2335       202  LOAD_STR                 ''
              204  LOAD_METHOD              join
              206  LOAD_GENEXPR             '<code_object <genexpr>>'
              208  LOAD_STR                 '_assert_no_gc_cycles_context.<locals>.<genexpr>'
              210  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.2340       212  LOAD_FAST                'objects_in_cycles'

 L.2335       214  GET_ITER         
              216  CALL_FUNCTION_1       1  ''
              218  CALL_METHOD_1         1  ''

 L.2329       220  CALL_METHOD_4         4  ''

 L.2328       222  CALL_FUNCTION_1       1  ''
              224  RAISE_VARARGS_1       1  'exception instance'
            226_0  COME_FROM           164  '164'

Parse error at or near `BEGIN_FINALLY' instruction at offset 128


def assert_no_gc_cycles(*args, **kwargs):
    r"""
    Fail if the given callable produces any reference cycles.

    If called with all arguments omitted, may be used as a context manager:

        with assert_no_gc_cycles():
            do_something()

    .. versionadded:: 1.15.0

    Parameters
    ----------
    func : callable
        The callable to test.
    \*args : Arguments
        Arguments passed to `func`.
    \*\*kwargs : Kwargs
        Keyword arguments passed to `func`.

    Returns
    -------
    Nothing. The result is deliberately discarded to ensure that all cycles
    are found.

    """
    if not args:
        return _assert_no_gc_cycles_context()
    func = args[0]
    args = args[1:]
    with _assert_no_gc_cycles_context(name=(func.__name__)):
        func(*args, **kwargs)


def break_cycles():
    """
    Break reference cycles by calling gc.collect
    Objects can call other objects' methods (for instance, another object's
     __del__) inside their own __del__. On PyPy, the interpreter only runs
    between calls to gc.collect, so multiple calls are needed to completely
    release all cycles.
    """
    gc.collect()
    if IS_PYPY:
        gc.collect()
        gc.collect()


def requires_memory(free_bytes):
    """Decorator to skip a test if not enough memory is available"""
    import pytest

    def decorator(func):

        @wraps(func)
        def wrapper(*a, **kw):
            msg = check_free_memory(free_bytes)
            if msg is not None:
                pytest.skip(msg)
            try:
                return func(*a, **kw)
            except MemoryError:
                pytest.xfail('MemoryError raised')

        return wrapper

    return decorator


def check_free_memory(free_bytes):
    """
    Check whether `free_bytes` amount of memory is currently free.
    Returns: None if enough memory available, otherwise error message
    """
    env_var = 'NPY_AVAILABLE_MEM'
    env_value = os.environ.get(env_var)
    if env_value is not None:
        try:
            mem_free = _parse_size(env_value)
        except ValueError as exc:
            try:
                raise ValueError('Invalid environment variable {}: {!s}'.formatenv_varexc)
            finally:
                exc = None
                del exc

        else:
            msg = '{0} GB memory required, but environment variable NPY_AVAILABLE_MEM={1} set'.format(free_bytes / 1000000000.0)env_value
    else:
        mem_free = _get_mem_available()
        if mem_free is None:
            msg = 'Could not determine available memory; set NPY_AVAILABLE_MEM environment variable (e.g. NPY_AVAILABLE_MEM=16GB) to run the test.'
            mem_free = -1
        else:
            msg = '{0} GB memory required, but {1} GB available'.format(free_bytes / 1000000000.0)(mem_free / 1000000000.0)
    if mem_free < free_bytes:
        return msg


def _parse_size(size_str):
    """Convert memory size strings ('12 GB' etc.) to float"""
    suffixes = {'':1, 
     'b':1,  'k':1000, 
     'm':1000000,  'g':1000000000,  't':1000000000000,  'kb':1000, 
     'mb':1000000,  'gb':1000000000,  'tb':1000000000000,  'kib':1024, 
     'mib':1048576,  'gib':1073741824,  'tib':1099511627776}
    size_re = re.compile'^\\s*(\\d+|\\d+\\.\\d+)\\s*({0})\\s*$'.format('|'.join(suffixes.keys()))re.I
    m = size_re.match(size_str.lower())
    if not m or m.group(2) not in suffixes:
        raise ValueError('value {!r} not a valid size'.format(size_str))
    return int(float(m.group(1)) * suffixes[m.group(2)])


def _get_mem_available--- This code section failed: ---

 L.2469         0  SETUP_FINALLY        22  'to 22'

 L.2470         2  LOAD_CONST               0
                4  LOAD_CONST               None
                6  IMPORT_NAME              psutil
                8  STORE_FAST               'psutil'

 L.2471        10  LOAD_FAST                'psutil'
               12  LOAD_METHOD              virtual_memory
               14  CALL_METHOD_0         0  ''
               16  LOAD_ATTR                available
               18  POP_BLOCK        
               20  RETURN_VALUE     
             22_0  COME_FROM_FINALLY     0  '0'

 L.2472        22  DUP_TOP          
               24  LOAD_GLOBAL              ImportError
               26  LOAD_GLOBAL              AttributeError
               28  BUILD_TUPLE_2         2 
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    44  'to 44'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L.2473        40  POP_EXCEPT       
               42  JUMP_FORWARD         46  'to 46'
             44_0  COME_FROM            32  '32'
               44  END_FINALLY      
             46_0  COME_FROM            42  '42'

 L.2475        46  LOAD_GLOBAL              sys
               48  LOAD_ATTR                platform
               50  LOAD_METHOD              startswith
               52  LOAD_STR                 'linux'
               54  CALL_METHOD_1         1  ''
               56  POP_JUMP_IF_FALSE   168  'to 168'

 L.2476        58  BUILD_MAP_0           0 
               60  STORE_FAST               'info'

 L.2477        62  LOAD_GLOBAL              open
               64  LOAD_STR                 '/proc/meminfo'
               66  LOAD_STR                 'r'
               68  CALL_FUNCTION_2       2  ''
               70  SETUP_WITH          130  'to 130'
               72  STORE_FAST               'f'

 L.2478        74  LOAD_FAST                'f'
               76  GET_ITER         
             78_0  COME_FROM           124  '124'
               78  FOR_ITER            126  'to 126'
               80  STORE_FAST               'line'

 L.2479        82  LOAD_FAST                'line'
               84  LOAD_METHOD              split
               86  CALL_METHOD_0         0  ''
               88  STORE_FAST               'p'

 L.2480        90  LOAD_GLOBAL              int
               92  LOAD_FAST                'p'
               94  LOAD_CONST               1
               96  BINARY_SUBSCR    
               98  CALL_FUNCTION_1       1  ''
              100  LOAD_CONST               1024
              102  BINARY_MULTIPLY  
              104  LOAD_FAST                'info'
              106  LOAD_FAST                'p'
              108  LOAD_CONST               0
              110  BINARY_SUBSCR    
              112  LOAD_METHOD              strip
              114  LOAD_STR                 ':'
              116  CALL_METHOD_1         1  ''
              118  LOAD_METHOD              lower
              120  CALL_METHOD_0         0  ''
              122  STORE_SUBSCR     
              124  JUMP_BACK            78  'to 78'
            126_0  COME_FROM            78  '78'
              126  POP_BLOCK        
              128  BEGIN_FINALLY    
            130_0  COME_FROM_WITH       70  '70'
              130  WITH_CLEANUP_START
              132  WITH_CLEANUP_FINISH
              134  END_FINALLY      

 L.2482       136  LOAD_STR                 'memavailable'
              138  LOAD_FAST                'info'
              140  COMPARE_OP               in
              142  POP_JUMP_IF_FALSE   152  'to 152'

 L.2484       144  LOAD_FAST                'info'
              146  LOAD_STR                 'memavailable'
              148  BINARY_SUBSCR    
              150  RETURN_VALUE     
            152_0  COME_FROM           142  '142'

 L.2486       152  LOAD_FAST                'info'
              154  LOAD_STR                 'memfree'
              156  BINARY_SUBSCR    
              158  LOAD_FAST                'info'
              160  LOAD_STR                 'cached'
              162  BINARY_SUBSCR    
              164  BINARY_ADD       
              166  RETURN_VALUE     
            168_0  COME_FROM            56  '56'

Parse error at or near `COME_FROM' instruction at offset 44_0


def _no_tracing(func):
    """
    Decorator to temporarily turn off tracing for the duration of a test.
    Needed in tests that check refcounting, otherwise the tracing itself
    influences the refcounts
    """
    if not hasattr(sys, 'gettrace'):
        return func

    @wraps(func)
    def wrapper--- This code section failed: ---

 L.2502         0  LOAD_GLOBAL              sys
                2  LOAD_METHOD              gettrace
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'original_trace'

 L.2503         8  SETUP_FINALLY        34  'to 34'

 L.2504        10  LOAD_GLOBAL              sys
               12  LOAD_METHOD              settrace
               14  LOAD_CONST               None
               16  CALL_METHOD_1         1  ''
               18  POP_TOP          

 L.2505        20  LOAD_DEREF               'func'
               22  LOAD_FAST                'args'
               24  LOAD_FAST                'kwargs'
               26  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               28  POP_BLOCK        
               30  CALL_FINALLY         34  'to 34'
               32  RETURN_VALUE     
             34_0  COME_FROM            30  '30'
             34_1  COME_FROM_FINALLY     8  '8'

 L.2507        34  LOAD_GLOBAL              sys
               36  LOAD_METHOD              settrace
               38  LOAD_FAST                'original_trace'
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          
               44  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 30

    return wrapper