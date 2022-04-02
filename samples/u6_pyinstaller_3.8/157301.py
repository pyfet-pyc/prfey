# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\testing\_private\utils.py
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
        else:
            msg = nose_is_good or 'Need nose >= %d.%d.%d for tests - see https://nose.readthedocs.io' % minimum_nose_version
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
    """like isfinite, but always raise an error if type not supported instead
    of returning a TypeError object.

    Notes
    -----
    isfinite and other ufunc sometimes return a NotImplementedType object
    instead of raising any exception. This function is a wrapper to make sure
    an exception is always raised.

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

 L. 169        34  LOAD_FAST                'inum'

 L. 169        36  LOAD_FAST                'counter'

 L. 168        38  BUILD_TUPLE_6         6 
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'path'

 L. 170        44  LOAD_FAST                'win32pdh'
               46  LOAD_METHOD              OpenQuery
               48  CALL_METHOD_0         0  ''
               50  STORE_FAST               'hq'

 L. 171        52  SETUP_FINALLY       122  'to 122'

 L. 172        54  LOAD_FAST                'win32pdh'
               56  LOAD_METHOD              AddCounter
               58  LOAD_FAST                'hq'
               60  LOAD_FAST                'path'
               62  CALL_METHOD_2         2  ''
               64  STORE_FAST               'hc'

 L. 173        66  SETUP_FINALLY       106  'to 106'

 L. 174        68  LOAD_FAST                'win32pdh'
               70  LOAD_METHOD              CollectQueryData
               72  LOAD_FAST                'hq'
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          

 L. 175        78  LOAD_FAST                'win32pdh'
               80  LOAD_METHOD              GetFormattedCounterValue
               82  LOAD_FAST                'hc'
               84  LOAD_FAST                'format'
               86  CALL_METHOD_2         2  ''
               88  UNPACK_SEQUENCE_2     2 
               90  STORE_FAST               'type'
               92  STORE_FAST               'val'

 L. 176        94  LOAD_FAST                'val'
               96  POP_BLOCK        
               98  CALL_FINALLY        106  'to 106'
              100  POP_BLOCK        
              102  CALL_FINALLY        122  'to 122'
              104  RETURN_VALUE     
            106_0  COME_FROM            98  '98'
            106_1  COME_FROM_FINALLY    66  '66'

 L. 178       106  LOAD_FAST                'win32pdh'
              108  LOAD_METHOD              RemoveCounter
              110  LOAD_FAST                'hc'
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          
              116  END_FINALLY      
              118  POP_BLOCK        
              120  BEGIN_FINALLY    
            122_0  COME_FROM           102  '102'
            122_1  COME_FROM_FINALLY    52  '52'

 L. 180       122  LOAD_FAST                'win32pdh'
              124  LOAD_METHOD              CloseQuery
              126  LOAD_FAST                'hq'
              128  CALL_METHOD_1         1  ''
              130  POP_TOP          
              132  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 98


    def memusage(processName='python', instance=0):
        import win32pdh
        return GetPerformanceAttributes('Process', 'Virtual Bytes', processName, instance, win32pdh.PDH_FMT_LONG, None)


else:
    if sys.platform[:5] == 'linux':

        def memusage--- This code section failed: ---

 L. 195         0  SETUP_FINALLY        52  'to 52'

 L. 196         2  LOAD_GLOBAL              open
                4  LOAD_FAST                '_proc_pid_stat'
                6  LOAD_STR                 'r'
                8  CALL_FUNCTION_2       2  ''
               10  SETUP_WITH           32  'to 32'
               12  STORE_FAST               'f'

 L. 197        14  LOAD_FAST                'f'
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

 L. 198        38  LOAD_GLOBAL              int
               40  LOAD_FAST                'l'
               42  LOAD_CONST               22
               44  BINARY_SUBSCR    
               46  CALL_FUNCTION_1       1  ''
               48  POP_BLOCK        
               50  RETURN_VALUE     
             52_0  COME_FROM_FINALLY     0  '0'

 L. 199        52  DUP_TOP          
               54  LOAD_GLOBAL              Exception
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    72  'to 72'
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L. 200        66  POP_EXCEPT       
               68  LOAD_CONST               None
               70  RETURN_VALUE     
             72_0  COME_FROM            58  '58'
               72  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 62


    else:

        def memusage():
            """
        Return memory usage of running python. [Not implemented]

        """
            raise NotImplementedError


if sys.platform[:5] == 'linux':

    def jiffies--- This code section failed: ---

 L. 219         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              time
                6  STORE_FAST               'time'

 L. 220         8  LOAD_FAST                '_load_time'
               10  POP_JUMP_IF_TRUE     26  'to 26'

 L. 221        12  LOAD_FAST                '_load_time'
               14  LOAD_METHOD              append
               16  LOAD_FAST                'time'
               18  LOAD_METHOD              time
               20  CALL_METHOD_0         0  ''
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          
             26_0  COME_FROM            10  '10'

 L. 222        26  SETUP_FINALLY        78  'to 78'

 L. 223        28  LOAD_GLOBAL              open
               30  LOAD_FAST                '_proc_pid_stat'
               32  LOAD_STR                 'r'
               34  CALL_FUNCTION_2       2  ''
               36  SETUP_WITH           58  'to 58'
               38  STORE_FAST               'f'

 L. 224        40  LOAD_FAST                'f'
               42  LOAD_METHOD              readline
               44  CALL_METHOD_0         0  ''
               46  LOAD_METHOD              split
               48  LOAD_STR                 ' '
               50  CALL_METHOD_1         1  ''
               52  STORE_FAST               'l'
               54  POP_BLOCK        
               56  BEGIN_FINALLY    
             58_0  COME_FROM_WITH       36  '36'
               58  WITH_CLEANUP_START
               60  WITH_CLEANUP_FINISH
               62  END_FINALLY      

 L. 225        64  LOAD_GLOBAL              int
               66  LOAD_FAST                'l'
               68  LOAD_CONST               13
               70  BINARY_SUBSCR    
               72  CALL_FUNCTION_1       1  ''
               74  POP_BLOCK        
               76  RETURN_VALUE     
             78_0  COME_FROM_FINALLY    26  '26'

 L. 226        78  DUP_TOP          
               80  LOAD_GLOBAL              Exception
               82  COMPARE_OP               exception-match
               84  POP_JUMP_IF_FALSE   120  'to 120'
               86  POP_TOP          
               88  POP_TOP          
               90  POP_TOP          

 L. 227        92  LOAD_GLOBAL              int
               94  LOAD_CONST               100
               96  LOAD_FAST                'time'
               98  LOAD_METHOD              time
              100  CALL_METHOD_0         0  ''
              102  LOAD_FAST                '_load_time'
              104  LOAD_CONST               0
              106  BINARY_SUBSCR    
              108  BINARY_SUBTRACT  
              110  BINARY_MULTIPLY  
              112  CALL_FUNCTION_1       1  ''
              114  ROT_FOUR         
              116  POP_EXCEPT       
              118  RETURN_VALUE     
            120_0  COME_FROM            84  '84'
              120  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 88


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
                    r = f"[repr failed for <{type(a).__name__}>: {exc}]"
                finally:
                    exc = None
                    del exc

            else:
                if r.count'\n' > 3:
                    r = '\n'.joinr.splitlines()[:3]
                    r += '...'
                msg.appendf" {names[i]}: {r}"

    return '\n'.joinmsg


def assert_equal--- This code section failed: ---

 L. 324         0  LOAD_CONST               True
                2  STORE_FAST               '__tracebackhide__'

 L. 325         4  LOAD_GLOBAL              isinstance
                6  LOAD_FAST                'desired'
                8  LOAD_GLOBAL              dict
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_FALSE   138  'to 138'

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
               70  FOR_ITER            134  'to 134'
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
              112  LOAD_STR                 'key='
              114  LOAD_FAST                'k'
              116  FORMAT_VALUE          2  '!r'
              118  LOAD_STR                 '\n'
              120  LOAD_FAST                'err_msg'
              122  FORMAT_VALUE          0  ''
              124  BUILD_STRING_4        4 

 L. 333       126  LOAD_FAST                'verbose'

 L. 332       128  CALL_FUNCTION_4       4  ''
              130  POP_TOP          
              132  JUMP_BACK            70  'to 70'

 L. 334       134  LOAD_CONST               None
              136  RETURN_VALUE     
            138_0  COME_FROM            12  '12'

 L. 335       138  LOAD_GLOBAL              isinstance
              140  LOAD_FAST                'desired'
              142  LOAD_GLOBAL              list
              144  LOAD_GLOBAL              tuple
              146  BUILD_TUPLE_2         2 
              148  CALL_FUNCTION_2       2  ''
              150  POP_JUMP_IF_FALSE   244  'to 244'
              152  LOAD_GLOBAL              isinstance
              154  LOAD_FAST                'actual'
              156  LOAD_GLOBAL              list
              158  LOAD_GLOBAL              tuple
              160  BUILD_TUPLE_2         2 
              162  CALL_FUNCTION_2       2  ''
              164  POP_JUMP_IF_FALSE   244  'to 244'

 L. 336       166  LOAD_GLOBAL              assert_equal
              168  LOAD_GLOBAL              len
              170  LOAD_FAST                'actual'
              172  CALL_FUNCTION_1       1  ''
              174  LOAD_GLOBAL              len
              176  LOAD_FAST                'desired'
              178  CALL_FUNCTION_1       1  ''
              180  LOAD_FAST                'err_msg'
              182  LOAD_FAST                'verbose'
              184  CALL_FUNCTION_4       4  ''
              186  POP_TOP          

 L. 337       188  LOAD_GLOBAL              range
              190  LOAD_GLOBAL              len
              192  LOAD_FAST                'desired'
              194  CALL_FUNCTION_1       1  ''
              196  CALL_FUNCTION_1       1  ''
              198  GET_ITER         
              200  FOR_ITER            240  'to 240'
              202  STORE_FAST               'k'

 L. 338       204  LOAD_GLOBAL              assert_equal
              206  LOAD_FAST                'actual'
              208  LOAD_FAST                'k'
              210  BINARY_SUBSCR    
              212  LOAD_FAST                'desired'
              214  LOAD_FAST                'k'
              216  BINARY_SUBSCR    
              218  LOAD_STR                 'item='
              220  LOAD_FAST                'k'
              222  FORMAT_VALUE          2  '!r'
              224  LOAD_STR                 '\n'
              226  LOAD_FAST                'err_msg'
              228  FORMAT_VALUE          0  ''
              230  BUILD_STRING_4        4 

 L. 339       232  LOAD_FAST                'verbose'

 L. 338       234  CALL_FUNCTION_4       4  ''
              236  POP_TOP          
              238  JUMP_BACK           200  'to 200'

 L. 340       240  LOAD_CONST               None
              242  RETURN_VALUE     
            244_0  COME_FROM           164  '164'
            244_1  COME_FROM           150  '150'

 L. 341       244  LOAD_CONST               0
              246  LOAD_CONST               ('ndarray', 'isscalar', 'signbit')
              248  IMPORT_NAME_ATTR         numpy.core
              250  IMPORT_FROM              ndarray
              252  STORE_FAST               'ndarray'
              254  IMPORT_FROM              isscalar
              256  STORE_FAST               'isscalar'
              258  IMPORT_FROM              signbit
              260  STORE_FAST               'signbit'
              262  POP_TOP          

 L. 342       264  LOAD_CONST               0
              266  LOAD_CONST               ('iscomplexobj', 'real', 'imag')
              268  IMPORT_NAME_ATTR         numpy.lib
              270  IMPORT_FROM              iscomplexobj
              272  STORE_FAST               'iscomplexobj'
              274  IMPORT_FROM              real
              276  STORE_FAST               'real'
              278  IMPORT_FROM              imag
              280  STORE_FAST               'imag'
              282  POP_TOP          

 L. 343       284  LOAD_GLOBAL              isinstance
              286  LOAD_FAST                'actual'
              288  LOAD_FAST                'ndarray'
              290  CALL_FUNCTION_2       2  ''
          292_294  POP_JUMP_IF_TRUE    308  'to 308'
              296  LOAD_GLOBAL              isinstance
              298  LOAD_FAST                'desired'
              300  LOAD_FAST                'ndarray'
              302  CALL_FUNCTION_2       2  ''
          304_306  POP_JUMP_IF_FALSE   322  'to 322'
            308_0  COME_FROM           292  '292'

 L. 344       308  LOAD_GLOBAL              assert_array_equal
              310  LOAD_FAST                'actual'
              312  LOAD_FAST                'desired'
              314  LOAD_FAST                'err_msg'
              316  LOAD_FAST                'verbose'
              318  CALL_FUNCTION_4       4  ''
              320  RETURN_VALUE     
            322_0  COME_FROM           304  '304'

 L. 345       322  LOAD_GLOBAL              build_err_msg
              324  LOAD_FAST                'actual'
              326  LOAD_FAST                'desired'
              328  BUILD_LIST_2          2 
              330  LOAD_FAST                'err_msg'
              332  LOAD_FAST                'verbose'
              334  LOAD_CONST               ('verbose',)
              336  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              338  STORE_FAST               'msg'

 L. 350       340  SETUP_FINALLY       364  'to 364'

 L. 351       342  LOAD_FAST                'iscomplexobj'
              344  LOAD_FAST                'actual'
              346  CALL_FUNCTION_1       1  ''
          348_350  JUMP_IF_TRUE_OR_POP   358  'to 358'
              352  LOAD_FAST                'iscomplexobj'
              354  LOAD_FAST                'desired'
              356  CALL_FUNCTION_1       1  ''
            358_0  COME_FROM           348  '348'
              358  STORE_FAST               'usecomplex'
              360  POP_BLOCK        
              362  JUMP_FORWARD        394  'to 394'
            364_0  COME_FROM_FINALLY   340  '340'

 L. 352       364  DUP_TOP          
              366  LOAD_GLOBAL              ValueError
              368  LOAD_GLOBAL              TypeError
              370  BUILD_TUPLE_2         2 
              372  COMPARE_OP               exception-match
          374_376  POP_JUMP_IF_FALSE   392  'to 392'
              378  POP_TOP          
              380  POP_TOP          
              382  POP_TOP          

 L. 353       384  LOAD_CONST               False
              386  STORE_FAST               'usecomplex'
              388  POP_EXCEPT       
              390  JUMP_FORWARD        394  'to 394'
            392_0  COME_FROM           374  '374'
              392  END_FINALLY      
            394_0  COME_FROM           390  '390'
            394_1  COME_FROM           362  '362'

 L. 355       394  LOAD_FAST                'usecomplex'
          396_398  POP_JUMP_IF_FALSE   528  'to 528'

 L. 356       400  LOAD_FAST                'iscomplexobj'
              402  LOAD_FAST                'actual'
              404  CALL_FUNCTION_1       1  ''
          406_408  POP_JUMP_IF_FALSE   428  'to 428'

 L. 357       410  LOAD_FAST                'real'
              412  LOAD_FAST                'actual'
              414  CALL_FUNCTION_1       1  ''
              416  STORE_FAST               'actualr'

 L. 358       418  LOAD_FAST                'imag'
              420  LOAD_FAST                'actual'
              422  CALL_FUNCTION_1       1  ''
              424  STORE_FAST               'actuali'
              426  JUMP_FORWARD        436  'to 436'
            428_0  COME_FROM           406  '406'

 L. 360       428  LOAD_FAST                'actual'
              430  STORE_FAST               'actualr'

 L. 361       432  LOAD_CONST               0
              434  STORE_FAST               'actuali'
            436_0  COME_FROM           426  '426'

 L. 362       436  LOAD_FAST                'iscomplexobj'
              438  LOAD_FAST                'desired'
              440  CALL_FUNCTION_1       1  ''
          442_444  POP_JUMP_IF_FALSE   464  'to 464'

 L. 363       446  LOAD_FAST                'real'
              448  LOAD_FAST                'desired'
              450  CALL_FUNCTION_1       1  ''
              452  STORE_FAST               'desiredr'

 L. 364       454  LOAD_FAST                'imag'
              456  LOAD_FAST                'desired'
              458  CALL_FUNCTION_1       1  ''
              460  STORE_FAST               'desiredi'
              462  JUMP_FORWARD        472  'to 472'
            464_0  COME_FROM           442  '442'

 L. 366       464  LOAD_FAST                'desired'
              466  STORE_FAST               'desiredr'

 L. 367       468  LOAD_CONST               0
              470  STORE_FAST               'desiredi'
            472_0  COME_FROM           462  '462'

 L. 368       472  SETUP_FINALLY       498  'to 498'

 L. 369       474  LOAD_GLOBAL              assert_equal
              476  LOAD_FAST                'actualr'
              478  LOAD_FAST                'desiredr'
              480  CALL_FUNCTION_2       2  ''
              482  POP_TOP          

 L. 370       484  LOAD_GLOBAL              assert_equal
              486  LOAD_FAST                'actuali'
              488  LOAD_FAST                'desiredi'
              490  CALL_FUNCTION_2       2  ''
              492  POP_TOP          
              494  POP_BLOCK        
              496  JUMP_FORWARD        528  'to 528'
            498_0  COME_FROM_FINALLY   472  '472'

 L. 371       498  DUP_TOP          
              500  LOAD_GLOBAL              AssertionError
              502  COMPARE_OP               exception-match
          504_506  POP_JUMP_IF_FALSE   526  'to 526'
              508  POP_TOP          
              510  POP_TOP          
              512  POP_TOP          

 L. 372       514  LOAD_GLOBAL              AssertionError
              516  LOAD_FAST                'msg'
              518  CALL_FUNCTION_1       1  ''
              520  RAISE_VARARGS_1       1  'exception instance'
              522  POP_EXCEPT       
              524  JUMP_FORWARD        528  'to 528'
            526_0  COME_FROM           504  '504'
              526  END_FINALLY      
            528_0  COME_FROM           524  '524'
            528_1  COME_FROM           496  '496'
            528_2  COME_FROM           396  '396'

 L. 375       528  LOAD_FAST                'isscalar'
              530  LOAD_FAST                'desired'
              532  CALL_FUNCTION_1       1  ''
              534  LOAD_FAST                'isscalar'
              536  LOAD_FAST                'actual'
              538  CALL_FUNCTION_1       1  ''
              540  COMPARE_OP               !=
          542_544  POP_JUMP_IF_FALSE   554  'to 554'

 L. 376       546  LOAD_GLOBAL              AssertionError
              548  LOAD_FAST                'msg'
              550  CALL_FUNCTION_1       1  ''
              552  RAISE_VARARGS_1       1  'exception instance'
            554_0  COME_FROM           542  '542'

 L. 378       554  SETUP_FINALLY       632  'to 632'

 L. 379       556  LOAD_GLOBAL              isnat
              558  LOAD_FAST                'desired'
              560  CALL_FUNCTION_1       1  ''
              562  STORE_FAST               'isdesnat'

 L. 380       564  LOAD_GLOBAL              isnat
              566  LOAD_FAST                'actual'
              568  CALL_FUNCTION_1       1  ''
              570  STORE_FAST               'isactnat'

 L. 381       572  LOAD_GLOBAL              array
              574  LOAD_FAST                'desired'
              576  CALL_FUNCTION_1       1  ''
              578  LOAD_ATTR                dtype
              580  LOAD_ATTR                type
              582  LOAD_GLOBAL              array
              584  LOAD_FAST                'actual'
              586  CALL_FUNCTION_1       1  ''
              588  LOAD_ATTR                dtype
              590  LOAD_ATTR                type
              592  COMPARE_OP               ==
              594  STORE_FAST               'dtypes_match'

 L. 382       596  LOAD_FAST                'isdesnat'
          598_600  POP_JUMP_IF_FALSE   628  'to 628'
              602  LOAD_FAST                'isactnat'
          604_606  POP_JUMP_IF_FALSE   628  'to 628'

 L. 385       608  LOAD_FAST                'dtypes_match'
          610_612  POP_JUMP_IF_FALSE   620  'to 620'

 L. 386       614  POP_BLOCK        
              616  LOAD_CONST               None
              618  RETURN_VALUE     
            620_0  COME_FROM           610  '610'

 L. 388       620  LOAD_GLOBAL              AssertionError
              622  LOAD_FAST                'msg'
              624  CALL_FUNCTION_1       1  ''
              626  RAISE_VARARGS_1       1  'exception instance'
            628_0  COME_FROM           604  '604'
            628_1  COME_FROM           598  '598'
              628  POP_BLOCK        
              630  JUMP_FORWARD        660  'to 660'
            632_0  COME_FROM_FINALLY   554  '554'

 L. 390       632  DUP_TOP          
              634  LOAD_GLOBAL              TypeError
              636  LOAD_GLOBAL              ValueError
              638  LOAD_GLOBAL              NotImplementedError
              640  BUILD_TUPLE_3         3 
              642  COMPARE_OP               exception-match
          644_646  POP_JUMP_IF_FALSE   658  'to 658'
              648  POP_TOP          
              650  POP_TOP          
              652  POP_TOP          

 L. 391       654  POP_EXCEPT       
              656  JUMP_FORWARD        660  'to 660'
            658_0  COME_FROM           644  '644'
              658  END_FINALLY      
            660_0  COME_FROM           656  '656'
            660_1  COME_FROM           630  '630'

 L. 394       660  SETUP_FINALLY       798  'to 798'

 L. 395       662  LOAD_GLOBAL              gisnan
              664  LOAD_FAST                'desired'
              666  CALL_FUNCTION_1       1  ''
              668  STORE_FAST               'isdesnan'

 L. 396       670  LOAD_GLOBAL              gisnan
              672  LOAD_FAST                'actual'
              674  CALL_FUNCTION_1       1  ''
              676  STORE_FAST               'isactnan'

 L. 397       678  LOAD_FAST                'isdesnan'
          680_682  POP_JUMP_IF_FALSE   696  'to 696'
              684  LOAD_FAST                'isactnan'
          686_688  POP_JUMP_IF_FALSE   696  'to 696'

 L. 398       690  POP_BLOCK        
              692  LOAD_CONST               None
              694  RETURN_VALUE     
            696_0  COME_FROM           686  '686'
            696_1  COME_FROM           680  '680'

 L. 401       696  LOAD_GLOBAL              array
              698  LOAD_FAST                'actual'
              700  CALL_FUNCTION_1       1  ''
              702  STORE_FAST               'array_actual'

 L. 402       704  LOAD_GLOBAL              array
              706  LOAD_FAST                'desired'
              708  CALL_FUNCTION_1       1  ''
              710  STORE_FAST               'array_desired'

 L. 403       712  LOAD_FAST                'array_actual'
              714  LOAD_ATTR                dtype
              716  LOAD_ATTR                char
              718  LOAD_STR                 'Mm'
              720  COMPARE_OP               in
          722_724  POP_JUMP_IF_TRUE    740  'to 740'

 L. 404       726  LOAD_FAST                'array_desired'
              728  LOAD_ATTR                dtype
              730  LOAD_ATTR                char
              732  LOAD_STR                 'Mm'
              734  COMPARE_OP               in

 L. 403   736_738  POP_JUMP_IF_FALSE   748  'to 748'
            740_0  COME_FROM           722  '722'

 L. 410       740  LOAD_GLOBAL              NotImplementedError
              742  LOAD_STR                 'cannot compare to a scalar with a different type'
              744  CALL_FUNCTION_1       1  ''
              746  RAISE_VARARGS_1       1  'exception instance'
            748_0  COME_FROM           736  '736'

 L. 413       748  LOAD_FAST                'desired'
              750  LOAD_CONST               0
              752  COMPARE_OP               ==
          754_756  POP_JUMP_IF_FALSE   794  'to 794'
              758  LOAD_FAST                'actual'
              760  LOAD_CONST               0
              762  COMPARE_OP               ==
          764_766  POP_JUMP_IF_FALSE   794  'to 794'

 L. 414       768  LOAD_FAST                'signbit'
              770  LOAD_FAST                'desired'
              772  CALL_FUNCTION_1       1  ''
              774  LOAD_FAST                'signbit'
              776  LOAD_FAST                'actual'
              778  CALL_FUNCTION_1       1  ''
              780  COMPARE_OP               ==
          782_784  POP_JUMP_IF_TRUE    794  'to 794'

 L. 415       786  LOAD_ASSERT              AssertionError
              788  LOAD_FAST                'msg'
              790  CALL_FUNCTION_1       1  ''
              792  RAISE_VARARGS_1       1  'exception instance'
            794_0  COME_FROM           782  '782'
            794_1  COME_FROM           764  '764'
            794_2  COME_FROM           754  '754'
              794  POP_BLOCK        
              796  JUMP_FORWARD        826  'to 826'
            798_0  COME_FROM_FINALLY   660  '660'

 L. 417       798  DUP_TOP          
              800  LOAD_GLOBAL              TypeError
              802  LOAD_GLOBAL              ValueError
              804  LOAD_GLOBAL              NotImplementedError
              806  BUILD_TUPLE_3         3 
              808  COMPARE_OP               exception-match
          810_812  POP_JUMP_IF_FALSE   824  'to 824'
              814  POP_TOP          
              816  POP_TOP          
              818  POP_TOP          

 L. 418       820  POP_EXCEPT       
              822  JUMP_FORWARD        826  'to 826'
            824_0  COME_FROM           810  '810'
              824  END_FINALLY      
            826_0  COME_FROM           822  '822'
            826_1  COME_FROM           796  '796'

 L. 420       826  SETUP_FINALLY       850  'to 850'

 L. 422       828  LOAD_FAST                'desired'
              830  LOAD_FAST                'actual'
              832  COMPARE_OP               ==
          834_836  POP_JUMP_IF_TRUE    846  'to 846'

 L. 423       838  LOAD_ASSERT              AssertionError
              840  LOAD_FAST                'msg'
              842  CALL_FUNCTION_1       1  ''
              844  RAISE_VARARGS_1       1  'exception instance'
            846_0  COME_FROM           834  '834'
              846  POP_BLOCK        
              848  JUMP_FORWARD        918  'to 918'
            850_0  COME_FROM_FINALLY   826  '826'

 L. 425       850  DUP_TOP          
              852  LOAD_GLOBAL              DeprecationWarning
              854  LOAD_GLOBAL              FutureWarning
              856  BUILD_TUPLE_2         2 
              858  COMPARE_OP               exception-match
          860_862  POP_JUMP_IF_FALSE   916  'to 916'
              864  POP_TOP          
              866  STORE_FAST               'e'
              868  POP_TOP          
              870  SETUP_FINALLY       904  'to 904'

 L. 427       872  LOAD_STR                 'elementwise == comparison'
              874  LOAD_FAST                'e'
              876  LOAD_ATTR                args
              878  LOAD_CONST               0
              880  BINARY_SUBSCR    
              882  COMPARE_OP               in
          884_886  POP_JUMP_IF_FALSE   898  'to 898'

 L. 428       888  LOAD_GLOBAL              AssertionError
              890  LOAD_FAST                'msg'
              892  CALL_FUNCTION_1       1  ''
              894  RAISE_VARARGS_1       1  'exception instance'
              896  JUMP_FORWARD        900  'to 900'
            898_0  COME_FROM           884  '884'

 L. 430       898  RAISE_VARARGS_0       0  'reraise'
            900_0  COME_FROM           896  '896'
              900  POP_BLOCK        
              902  BEGIN_FINALLY    
            904_0  COME_FROM_FINALLY   870  '870'
              904  LOAD_CONST               None
              906  STORE_FAST               'e'
              908  DELETE_FAST              'e'
              910  END_FINALLY      
              912  POP_EXCEPT       
              914  JUMP_FORWARD        918  'to 918'
            916_0  COME_FROM           860  '860'
              916  END_FINALLY      
            918_0  COME_FROM           914  '914'
            918_1  COME_FROM           848  '848'

Parse error at or near `LOAD_CONST' instruction at offset 616


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

 L. 543         0  LOAD_CONST               True
                2  STORE_FAST               '__tracebackhide__'

 L. 544         4  LOAD_CONST               0
                6  LOAD_CONST               ('ndarray',)
                8  IMPORT_NAME_ATTR         numpy.core
               10  IMPORT_FROM              ndarray
               12  STORE_FAST               'ndarray'
               14  POP_TOP          

 L. 545        16  LOAD_CONST               0
               18  LOAD_CONST               ('iscomplexobj', 'real', 'imag')
               20  IMPORT_NAME_ATTR         numpy.lib
               22  IMPORT_FROM              iscomplexobj
               24  STORE_FAST               'iscomplexobj'
               26  IMPORT_FROM              real
               28  STORE_FAST               'real'
               30  IMPORT_FROM              imag
               32  STORE_FAST               'imag'
               34  POP_TOP          

 L. 550        36  SETUP_FINALLY        58  'to 58'

 L. 551        38  LOAD_FAST                'iscomplexobj'
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

 L. 552        58  DUP_TOP          
               60  LOAD_GLOBAL              ValueError
               62  COMPARE_OP               exception-match
               64  POP_JUMP_IF_FALSE    80  'to 80'
               66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          

 L. 553        72  LOAD_CONST               False
               74  STORE_FAST               'usecomplex'
               76  POP_EXCEPT       
               78  JUMP_FORWARD         82  'to 82'
             80_0  COME_FROM            64  '64'
               80  END_FINALLY      
             82_0  COME_FROM            78  '78'
             82_1  COME_FROM            56  '56'

 L. 555        82  LOAD_CLOSURE             'actual'
               84  LOAD_CLOSURE             'decimal'
               86  LOAD_CLOSURE             'desired'
               88  LOAD_CLOSURE             'err_msg'
               90  LOAD_CLOSURE             'verbose'
               92  BUILD_TUPLE_5         5 
               94  LOAD_CODE                <code_object _build_err_msg>
               96  LOAD_STR                 'assert_almost_equal.<locals>._build_err_msg'
               98  MAKE_FUNCTION_8          'closure'
              100  STORE_FAST               '_build_err_msg'

 L. 560       102  LOAD_FAST                'usecomplex'
              104  POP_JUMP_IF_FALSE   238  'to 238'

 L. 561       106  LOAD_FAST                'iscomplexobj'
              108  LOAD_DEREF               'actual'
              110  CALL_FUNCTION_1       1  ''
              112  POP_JUMP_IF_FALSE   132  'to 132'

 L. 562       114  LOAD_FAST                'real'
              116  LOAD_DEREF               'actual'
              118  CALL_FUNCTION_1       1  ''
              120  STORE_FAST               'actualr'

 L. 563       122  LOAD_FAST                'imag'
              124  LOAD_DEREF               'actual'
              126  CALL_FUNCTION_1       1  ''
              128  STORE_FAST               'actuali'
              130  JUMP_FORWARD        140  'to 140'
            132_0  COME_FROM           112  '112'

 L. 565       132  LOAD_DEREF               'actual'
              134  STORE_FAST               'actualr'

 L. 566       136  LOAD_CONST               0
              138  STORE_FAST               'actuali'
            140_0  COME_FROM           130  '130'

 L. 567       140  LOAD_FAST                'iscomplexobj'
              142  LOAD_DEREF               'desired'
              144  CALL_FUNCTION_1       1  ''
              146  POP_JUMP_IF_FALSE   166  'to 166'

 L. 568       148  LOAD_FAST                'real'
              150  LOAD_DEREF               'desired'
              152  CALL_FUNCTION_1       1  ''
              154  STORE_FAST               'desiredr'

 L. 569       156  LOAD_FAST                'imag'
              158  LOAD_DEREF               'desired'
              160  CALL_FUNCTION_1       1  ''
              162  STORE_FAST               'desiredi'
              164  JUMP_FORWARD        174  'to 174'
            166_0  COME_FROM           146  '146'

 L. 571       166  LOAD_DEREF               'desired'
              168  STORE_FAST               'desiredr'

 L. 572       170  LOAD_CONST               0
              172  STORE_FAST               'desiredi'
            174_0  COME_FROM           164  '164'

 L. 573       174  SETUP_FINALLY       208  'to 208'

 L. 574       176  LOAD_GLOBAL              assert_almost_equal
              178  LOAD_FAST                'actualr'
              180  LOAD_FAST                'desiredr'
              182  LOAD_DEREF               'decimal'
              184  LOAD_CONST               ('decimal',)
              186  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              188  POP_TOP          

 L. 575       190  LOAD_GLOBAL              assert_almost_equal
              192  LOAD_FAST                'actuali'
              194  LOAD_FAST                'desiredi'
              196  LOAD_DEREF               'decimal'
              198  LOAD_CONST               ('decimal',)
              200  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              202  POP_TOP          
              204  POP_BLOCK        
              206  JUMP_FORWARD        238  'to 238'
            208_0  COME_FROM_FINALLY   174  '174'

 L. 576       208  DUP_TOP          
              210  LOAD_GLOBAL              AssertionError
              212  COMPARE_OP               exception-match
              214  POP_JUMP_IF_FALSE   236  'to 236'
              216  POP_TOP          
              218  POP_TOP          
              220  POP_TOP          

 L. 577       222  LOAD_GLOBAL              AssertionError
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

 L. 579       238  LOAD_GLOBAL              isinstance
              240  LOAD_DEREF               'actual'
              242  LOAD_FAST                'ndarray'
              244  LOAD_GLOBAL              tuple
              246  LOAD_GLOBAL              list
              248  BUILD_TUPLE_3         3 
              250  CALL_FUNCTION_2       2  ''
          252_254  POP_JUMP_IF_TRUE    274  'to 274'

 L. 580       256  LOAD_GLOBAL              isinstance
              258  LOAD_DEREF               'desired'
              260  LOAD_FAST                'ndarray'
              262  LOAD_GLOBAL              tuple
              264  LOAD_GLOBAL              list
              266  BUILD_TUPLE_3         3 
              268  CALL_FUNCTION_2       2  ''

 L. 579   270_272  POP_JUMP_IF_FALSE   288  'to 288'
            274_0  COME_FROM           252  '252'

 L. 581       274  LOAD_GLOBAL              assert_array_almost_equal
              276  LOAD_DEREF               'actual'
              278  LOAD_DEREF               'desired'
              280  LOAD_DEREF               'decimal'
              282  LOAD_DEREF               'err_msg'
              284  CALL_FUNCTION_4       4  ''
              286  RETURN_VALUE     
            288_0  COME_FROM           270  '270'

 L. 582       288  SETUP_FINALLY       392  'to 392'

 L. 586       290  LOAD_GLOBAL              gisfinite
              292  LOAD_DEREF               'desired'
              294  CALL_FUNCTION_1       1  ''
          296_298  POP_JUMP_IF_FALSE   310  'to 310'
              300  LOAD_GLOBAL              gisfinite
              302  LOAD_DEREF               'actual'
              304  CALL_FUNCTION_1       1  ''
          306_308  POP_JUMP_IF_TRUE    388  'to 388'
            310_0  COME_FROM           296  '296'

 L. 587       310  LOAD_GLOBAL              gisnan
              312  LOAD_DEREF               'desired'
              314  CALL_FUNCTION_1       1  ''
          316_318  POP_JUMP_IF_TRUE    330  'to 330'
              320  LOAD_GLOBAL              gisnan
              322  LOAD_DEREF               'actual'
              324  CALL_FUNCTION_1       1  ''
          326_328  POP_JUMP_IF_FALSE   362  'to 362'
            330_0  COME_FROM           316  '316'

 L. 588       330  LOAD_GLOBAL              gisnan
              332  LOAD_DEREF               'desired'
              334  CALL_FUNCTION_1       1  ''
          336_338  POP_JUMP_IF_FALSE   350  'to 350'
              340  LOAD_GLOBAL              gisnan
              342  LOAD_DEREF               'actual'
              344  CALL_FUNCTION_1       1  ''
          346_348  POP_JUMP_IF_TRUE    382  'to 382'
            350_0  COME_FROM           336  '336'

 L. 589       350  LOAD_ASSERT              AssertionError
              352  LOAD_FAST                '_build_err_msg'
              354  CALL_FUNCTION_0       0  ''
              356  CALL_FUNCTION_1       1  ''
              358  RAISE_VARARGS_1       1  'exception instance'
              360  JUMP_FORWARD        382  'to 382'
            362_0  COME_FROM           326  '326'

 L. 591       362  LOAD_DEREF               'desired'
              364  LOAD_DEREF               'actual'
              366  COMPARE_OP               ==
          368_370  POP_JUMP_IF_TRUE    382  'to 382'

 L. 592       372  LOAD_ASSERT              AssertionError
              374  LOAD_FAST                '_build_err_msg'
              376  CALL_FUNCTION_0       0  ''
              378  CALL_FUNCTION_1       1  ''
              380  RAISE_VARARGS_1       1  'exception instance'
            382_0  COME_FROM           368  '368'
            382_1  COME_FROM           360  '360'
            382_2  COME_FROM           346  '346'

 L. 593       382  POP_BLOCK        
              384  LOAD_CONST               None
              386  RETURN_VALUE     
            388_0  COME_FROM           306  '306'
              388  POP_BLOCK        
              390  JUMP_FORWARD        418  'to 418'
            392_0  COME_FROM_FINALLY   288  '288'

 L. 594       392  DUP_TOP          
              394  LOAD_GLOBAL              NotImplementedError
              396  LOAD_GLOBAL              TypeError
              398  BUILD_TUPLE_2         2 
              400  COMPARE_OP               exception-match
          402_404  POP_JUMP_IF_FALSE   416  'to 416'
              406  POP_TOP          
              408  POP_TOP          
              410  POP_TOP          

 L. 595       412  POP_EXCEPT       
              414  JUMP_FORWARD        418  'to 418'
            416_0  COME_FROM           402  '402'
              416  END_FINALLY      
            418_0  COME_FROM           414  '414'
            418_1  COME_FROM           390  '390'

 L. 596       418  LOAD_GLOBAL              abs
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

 L. 597       446  LOAD_GLOBAL              AssertionError
              448  LOAD_FAST                '_build_err_msg'
              450  CALL_FUNCTION_0       0  ''
              452  CALL_FUNCTION_1       1  ''
              454  RAISE_VARARGS_1       1  'exception instance'
            456_0  COME_FROM           442  '442'

Parse error at or near `RETURN_VALUE' instruction at offset 386


def assert_approx_equal--- This code section failed: ---

 L. 658         0  LOAD_CONST               True
                2  STORE_FAST               '__tracebackhide__'

 L. 659         4  LOAD_CONST               0
                6  LOAD_CONST               None
                8  IMPORT_NAME              numpy
               10  STORE_FAST               'np'

 L. 661        12  LOAD_GLOBAL              map
               14  LOAD_GLOBAL              float
               16  LOAD_FAST                'actual'
               18  LOAD_FAST                'desired'
               20  BUILD_TUPLE_2         2 
               22  CALL_FUNCTION_2       2  ''
               24  UNPACK_SEQUENCE_2     2 
               26  STORE_FAST               'actual'
               28  STORE_FAST               'desired'

 L. 662        30  LOAD_FAST                'desired'
               32  LOAD_FAST                'actual'
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE    42  'to 42'

 L. 663        38  LOAD_CONST               None
               40  RETURN_VALUE     
             42_0  COME_FROM            36  '36'

 L. 666        42  LOAD_FAST                'np'
               44  LOAD_ATTR                errstate
               46  LOAD_STR                 'ignore'
               48  LOAD_CONST               ('invalid',)
               50  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               52  SETUP_WITH          108  'to 108'
               54  POP_TOP          

 L. 667        56  LOAD_CONST               0.5
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

 L. 668        80  LOAD_FAST                'np'
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

 L. 669       114  SETUP_FINALLY       128  'to 128'

 L. 670       116  LOAD_FAST                'desired'
              118  LOAD_FAST                'scale'
              120  BINARY_TRUE_DIVIDE
              122  STORE_FAST               'sc_desired'
              124  POP_BLOCK        
              126  JUMP_FORWARD        152  'to 152'
            128_0  COME_FROM_FINALLY   114  '114'

 L. 671       128  DUP_TOP          
              130  LOAD_GLOBAL              ZeroDivisionError
              132  COMPARE_OP               exception-match
              134  POP_JUMP_IF_FALSE   150  'to 150'
              136  POP_TOP          
              138  POP_TOP          
              140  POP_TOP          

 L. 672       142  LOAD_CONST               0.0
              144  STORE_FAST               'sc_desired'
              146  POP_EXCEPT       
              148  JUMP_FORWARD        152  'to 152'
            150_0  COME_FROM           134  '134'
              150  END_FINALLY      
            152_0  COME_FROM           148  '148'
            152_1  COME_FROM           126  '126'

 L. 673       152  SETUP_FINALLY       166  'to 166'

 L. 674       154  LOAD_FAST                'actual'
              156  LOAD_FAST                'scale'
              158  BINARY_TRUE_DIVIDE
              160  STORE_FAST               'sc_actual'
              162  POP_BLOCK        
              164  JUMP_FORWARD        190  'to 190'
            166_0  COME_FROM_FINALLY   152  '152'

 L. 675       166  DUP_TOP          
              168  LOAD_GLOBAL              ZeroDivisionError
              170  COMPARE_OP               exception-match
              172  POP_JUMP_IF_FALSE   188  'to 188'
              174  POP_TOP          
              176  POP_TOP          
              178  POP_TOP          

 L. 676       180  LOAD_CONST               0.0
              182  STORE_FAST               'sc_actual'
              184  POP_EXCEPT       
              186  JUMP_FORWARD        190  'to 190'
            188_0  COME_FROM           172  '172'
              188  END_FINALLY      
            190_0  COME_FROM           186  '186'
            190_1  COME_FROM           164  '164'

 L. 677       190  LOAD_GLOBAL              build_err_msg

 L. 678       192  LOAD_FAST                'actual'
              194  LOAD_FAST                'desired'
              196  BUILD_LIST_2          2 

 L. 678       198  LOAD_FAST                'err_msg'

 L. 679       200  LOAD_STR                 'Items are not equal to %d significant digits:'
              202  LOAD_FAST                'significant'
              204  BINARY_MODULO    

 L. 680       206  LOAD_FAST                'verbose'

 L. 677       208  LOAD_CONST               ('header', 'verbose')
              210  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              212  STORE_FAST               'msg'

 L. 681       214  SETUP_FINALLY       310  'to 310'

 L. 685       216  LOAD_GLOBAL              gisfinite
              218  LOAD_FAST                'desired'
              220  CALL_FUNCTION_1       1  ''
              222  POP_JUMP_IF_FALSE   234  'to 234'
              224  LOAD_GLOBAL              gisfinite
              226  LOAD_FAST                'actual'
              228  CALL_FUNCTION_1       1  ''
          230_232  POP_JUMP_IF_TRUE    306  'to 306'
            234_0  COME_FROM           222  '222'

 L. 686       234  LOAD_GLOBAL              gisnan
              236  LOAD_FAST                'desired'
              238  CALL_FUNCTION_1       1  ''
              240  POP_JUMP_IF_TRUE    252  'to 252'
              242  LOAD_GLOBAL              gisnan
              244  LOAD_FAST                'actual'
              246  CALL_FUNCTION_1       1  ''
          248_250  POP_JUMP_IF_FALSE   282  'to 282'
            252_0  COME_FROM           240  '240'

 L. 687       252  LOAD_GLOBAL              gisnan
              254  LOAD_FAST                'desired'
              256  CALL_FUNCTION_1       1  ''
          258_260  POP_JUMP_IF_FALSE   272  'to 272'
              262  LOAD_GLOBAL              gisnan
              264  LOAD_FAST                'actual'
              266  CALL_FUNCTION_1       1  ''
          268_270  POP_JUMP_IF_TRUE    300  'to 300'
            272_0  COME_FROM           258  '258'

 L. 688       272  LOAD_ASSERT              AssertionError
              274  LOAD_FAST                'msg'
              276  CALL_FUNCTION_1       1  ''
              278  RAISE_VARARGS_1       1  'exception instance'
              280  JUMP_FORWARD        300  'to 300'
            282_0  COME_FROM           248  '248'

 L. 690       282  LOAD_FAST                'desired'
              284  LOAD_FAST                'actual'
              286  COMPARE_OP               ==
          288_290  POP_JUMP_IF_TRUE    300  'to 300'

 L. 691       292  LOAD_ASSERT              AssertionError
              294  LOAD_FAST                'msg'
              296  CALL_FUNCTION_1       1  ''
              298  RAISE_VARARGS_1       1  'exception instance'
            300_0  COME_FROM           288  '288'
            300_1  COME_FROM           280  '280'
            300_2  COME_FROM           268  '268'

 L. 692       300  POP_BLOCK        
              302  LOAD_CONST               None
              304  RETURN_VALUE     
            306_0  COME_FROM           230  '230'
              306  POP_BLOCK        
              308  JUMP_FORWARD        336  'to 336'
            310_0  COME_FROM_FINALLY   214  '214'

 L. 693       310  DUP_TOP          
              312  LOAD_GLOBAL              TypeError
              314  LOAD_GLOBAL              NotImplementedError
              316  BUILD_TUPLE_2         2 
              318  COMPARE_OP               exception-match
          320_322  POP_JUMP_IF_FALSE   334  'to 334'
              324  POP_TOP          
              326  POP_TOP          
              328  POP_TOP          

 L. 694       330  POP_EXCEPT       
              332  JUMP_FORWARD        336  'to 336'
            334_0  COME_FROM           320  '320'
              334  END_FINALLY      
            336_0  COME_FROM           332  '332'
            336_1  COME_FROM           308  '308'

 L. 695       336  LOAD_FAST                'np'
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

 L. 696       370  LOAD_GLOBAL              AssertionError
              372  LOAD_FAST                'msg'
              374  CALL_FUNCTION_1       1  ''
              376  RAISE_VARARGS_1       1  'exception instance'
            378_0  COME_FROM           366  '366'

Parse error at or near `RETURN_VALUE' instruction at offset 304


def assert_array_compare--- This code section failed: ---

 L. 701         0  LOAD_CONST               True
                2  STORE_FAST               '__tracebackhide__'

 L. 702         4  LOAD_CONST               0
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

 L. 704        48  LOAD_FAST                'array'
               50  LOAD_FAST                'x'
               52  LOAD_CONST               False
               54  LOAD_CONST               True
               56  LOAD_CONST               ('copy', 'subok')
               58  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               60  STORE_FAST               'x'

 L. 705        62  LOAD_FAST                'array'
               64  LOAD_FAST                'y'
               66  LOAD_CONST               False
               68  LOAD_CONST               True
               70  LOAD_CONST               ('copy', 'subok')
               72  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               74  STORE_FAST               'y'

 L. 708        76  LOAD_FAST                'x'
               78  LOAD_FAST                'y'
               80  ROT_TWO          
               82  STORE_FAST               'ox'
               84  STORE_FAST               'oy'

 L. 710        86  LOAD_CODE                <code_object isnumber>
               88  LOAD_STR                 'assert_array_compare.<locals>.isnumber'
               90  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               92  STORE_FAST               'isnumber'

 L. 713        94  LOAD_CODE                <code_object istime>
               96  LOAD_STR                 'assert_array_compare.<locals>.istime'
               98  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              100  STORE_FAST               'istime'

 L. 716       102  LOAD_FAST                'isnan'
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

 L. 753   128_130  SETUP_FINALLY       886  'to 886'

 L. 754       132  LOAD_FAST                'x'
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

 L. 755       164  LOAD_FAST                'cond'
              166  POP_JUMP_IF_TRUE    222  'to 222'

 L. 756       168  LOAD_GLOBAL              build_err_msg
              170  LOAD_FAST                'x'
              172  LOAD_FAST                'y'
              174  BUILD_LIST_2          2 

 L. 757       176  LOAD_DEREF               'err_msg'

 L. 758       178  LOAD_STR                 '\n(shapes '
              180  LOAD_FAST                'x'
              182  LOAD_ATTR                shape
              184  FORMAT_VALUE          0  ''
              186  LOAD_STR                 ', '
              188  LOAD_FAST                'y'
              190  LOAD_ATTR                shape
              192  FORMAT_VALUE          0  ''
              194  LOAD_STR                 ' mismatch)'
              196  BUILD_STRING_5        5 

 L. 757       198  BINARY_ADD       

 L. 759       200  LOAD_DEREF               'verbose'

 L. 759       202  LOAD_DEREF               'header'

 L. 760       204  LOAD_CONST               ('x', 'y')

 L. 760       206  LOAD_DEREF               'precision'

 L. 756       208  LOAD_CONST               ('verbose', 'header', 'names', 'precision')
              210  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              212  STORE_FAST               'msg'

 L. 761       214  LOAD_GLOBAL              AssertionError
              216  LOAD_FAST                'msg'
              218  CALL_FUNCTION_1       1  ''
              220  RAISE_VARARGS_1       1  'exception instance'
            222_0  COME_FROM           166  '166'

 L. 763       222  LOAD_DEREF               'bool_'
              224  LOAD_CONST               False
              226  CALL_FUNCTION_1       1  ''
              228  STORE_FAST               'flagged'

 L. 764       230  LOAD_FAST                'isnumber'
              232  LOAD_FAST                'x'
              234  CALL_FUNCTION_1       1  ''
          236_238  POP_JUMP_IF_FALSE   336  'to 336'
              240  LOAD_FAST                'isnumber'
              242  LOAD_FAST                'y'
              244  CALL_FUNCTION_1       1  ''
          246_248  POP_JUMP_IF_FALSE   336  'to 336'

 L. 765       250  LOAD_FAST                'equal_nan'
          252_254  POP_JUMP_IF_FALSE   272  'to 272'

 L. 766       256  LOAD_FAST                'func_assert_same_pos'
              258  LOAD_FAST                'x'
              260  LOAD_FAST                'y'
              262  LOAD_FAST                'isnan'
              264  LOAD_STR                 'nan'
              266  LOAD_CONST               ('func', 'hasval')
              268  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              270  STORE_FAST               'flagged'
            272_0  COME_FROM           252  '252'

 L. 768       272  LOAD_FAST                'equal_inf'
          274_276  POP_JUMP_IF_FALSE   396  'to 396'

 L. 769       278  LOAD_FAST                'flagged'
              280  LOAD_FAST                'func_assert_same_pos'
              282  LOAD_FAST                'x'
              284  LOAD_FAST                'y'

 L. 770       286  LOAD_CLOSURE             'inf'
              288  BUILD_TUPLE_1         1 
              290  LOAD_LAMBDA              '<code_object <lambda>>'
              292  LOAD_STR                 'assert_array_compare.<locals>.<lambda>'
              294  MAKE_FUNCTION_8          'closure'

 L. 771       296  LOAD_STR                 '+inf'

 L. 769       298  LOAD_CONST               ('func', 'hasval')
              300  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              302  INPLACE_OR       
              304  STORE_FAST               'flagged'

 L. 772       306  LOAD_FAST                'flagged'
              308  LOAD_FAST                'func_assert_same_pos'
              310  LOAD_FAST                'x'
              312  LOAD_FAST                'y'

 L. 773       314  LOAD_CLOSURE             'inf'
              316  BUILD_TUPLE_1         1 
              318  LOAD_LAMBDA              '<code_object <lambda>>'
              320  LOAD_STR                 'assert_array_compare.<locals>.<lambda>'
              322  MAKE_FUNCTION_8          'closure'

 L. 774       324  LOAD_STR                 '-inf'

 L. 772       326  LOAD_CONST               ('func', 'hasval')
              328  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              330  INPLACE_OR       
              332  STORE_FAST               'flagged'
              334  JUMP_FORWARD        396  'to 396'
            336_0  COME_FROM           246  '246'
            336_1  COME_FROM           236  '236'

 L. 776       336  LOAD_FAST                'istime'
              338  LOAD_FAST                'x'
              340  CALL_FUNCTION_1       1  ''
          342_344  POP_JUMP_IF_FALSE   396  'to 396'
              346  LOAD_FAST                'istime'
              348  LOAD_FAST                'y'
              350  CALL_FUNCTION_1       1  ''
          352_354  POP_JUMP_IF_FALSE   396  'to 396'

 L. 778       356  LOAD_FAST                'equal_nan'
          358_360  POP_JUMP_IF_FALSE   396  'to 396'
              362  LOAD_FAST                'x'
              364  LOAD_ATTR                dtype
              366  LOAD_ATTR                type
              368  LOAD_FAST                'y'
              370  LOAD_ATTR                dtype
              372  LOAD_ATTR                type
              374  COMPARE_OP               ==
          376_378  POP_JUMP_IF_FALSE   396  'to 396'

 L. 779       380  LOAD_FAST                'func_assert_same_pos'
              382  LOAD_FAST                'x'
              384  LOAD_FAST                'y'
              386  LOAD_GLOBAL              isnat
              388  LOAD_STR                 'NaT'
              390  LOAD_CONST               ('func', 'hasval')
              392  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              394  STORE_FAST               'flagged'
            396_0  COME_FROM           376  '376'
            396_1  COME_FROM           358  '358'
            396_2  COME_FROM           352  '352'
            396_3  COME_FROM           342  '342'
            396_4  COME_FROM           334  '334'
            396_5  COME_FROM           274  '274'

 L. 781       396  LOAD_FAST                'flagged'
              398  LOAD_ATTR                ndim
              400  LOAD_CONST               0
              402  COMPARE_OP               >
          404_406  POP_JUMP_IF_FALSE   450  'to 450'

 L. 782       408  LOAD_FAST                'x'
              410  LOAD_FAST                'flagged'
              412  UNARY_INVERT     
              414  BINARY_SUBSCR    
              416  LOAD_FAST                'y'
              418  LOAD_FAST                'flagged'
              420  UNARY_INVERT     
              422  BINARY_SUBSCR    
              424  ROT_TWO          
              426  STORE_FAST               'x'
              428  STORE_FAST               'y'

 L. 784       430  LOAD_FAST                'x'
              432  LOAD_ATTR                size
              434  LOAD_CONST               0
              436  COMPARE_OP               ==
          438_440  POP_JUMP_IF_FALSE   462  'to 462'

 L. 785       442  POP_BLOCK        
              444  LOAD_CONST               None
              446  RETURN_VALUE     
              448  JUMP_FORWARD        462  'to 462'
            450_0  COME_FROM           404  '404'

 L. 786       450  LOAD_FAST                'flagged'
          452_454  POP_JUMP_IF_FALSE   462  'to 462'

 L. 788       456  POP_BLOCK        
              458  LOAD_CONST               None
              460  RETURN_VALUE     
            462_0  COME_FROM           452  '452'
            462_1  COME_FROM           448  '448'
            462_2  COME_FROM           438  '438'

 L. 790       462  LOAD_FAST                'comparison'
              464  LOAD_FAST                'x'
              466  LOAD_FAST                'y'
              468  CALL_FUNCTION_2       2  ''
              470  STORE_FAST               'val'

 L. 792       472  LOAD_GLOBAL              isinstance
              474  LOAD_FAST                'val'
              476  LOAD_GLOBAL              bool
              478  CALL_FUNCTION_2       2  ''
          480_482  POP_JUMP_IF_FALSE   500  'to 500'

 L. 793       484  LOAD_FAST                'val'
              486  STORE_FAST               'cond'

 L. 794       488  LOAD_FAST                'array'
              490  LOAD_FAST                'val'
              492  BUILD_LIST_1          1 
              494  CALL_FUNCTION_1       1  ''
              496  STORE_FAST               'reduced'
              498  JUMP_FORWARD        516  'to 516'
            500_0  COME_FROM           480  '480'

 L. 796       500  LOAD_FAST                'val'
              502  LOAD_METHOD              ravel
              504  CALL_METHOD_0         0  ''
              506  STORE_FAST               'reduced'

 L. 797       508  LOAD_FAST                'reduced'
              510  LOAD_METHOD              all
              512  CALL_METHOD_0         0  ''
              514  STORE_FAST               'cond'
            516_0  COME_FROM           498  '498'

 L. 803       516  LOAD_FAST                'cond'
              518  LOAD_CONST               True
              520  COMPARE_OP               !=
          522_524  POP_JUMP_IF_FALSE   882  'to 882'

 L. 804       526  LOAD_FAST                'reduced'
              528  LOAD_ATTR                size
              530  LOAD_FAST                'reduced'
              532  LOAD_ATTR                sum
              534  LOAD_GLOBAL              intp
              536  LOAD_CONST               ('dtype',)
              538  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              540  BINARY_SUBTRACT  
              542  STORE_FAST               'n_mismatch'

 L. 805       544  LOAD_FAST                'flagged'
              546  LOAD_ATTR                ndim
              548  LOAD_CONST               0
              550  COMPARE_OP               !=
          552_554  POP_JUMP_IF_FALSE   562  'to 562'
              556  LOAD_FAST                'flagged'
              558  LOAD_ATTR                size
              560  JUMP_FORWARD        566  'to 566'
            562_0  COME_FROM           552  '552'
              562  LOAD_FAST                'reduced'
              564  LOAD_ATTR                size
            566_0  COME_FROM           560  '560'
              566  STORE_FAST               'n_elements'

 L. 806       568  LOAD_CONST               100
              570  LOAD_FAST                'n_mismatch'
              572  BINARY_MULTIPLY  
              574  LOAD_FAST                'n_elements'
              576  BINARY_TRUE_DIVIDE
              578  STORE_FAST               'percent_mismatch'

 L. 808       580  LOAD_STR                 'Mismatched elements: {} / {} ({:.3g}%)'
              582  LOAD_METHOD              format

 L. 809       584  LOAD_FAST                'n_mismatch'

 L. 809       586  LOAD_FAST                'n_elements'

 L. 809       588  LOAD_FAST                'percent_mismatch'

 L. 808       590  CALL_METHOD_3         3  ''

 L. 807       592  BUILD_LIST_1          1 
              594  STORE_FAST               'remarks'

 L. 811       596  LOAD_FAST                'errstate'
              598  LOAD_STR                 'ignore'
              600  LOAD_STR                 'ignore'
              602  LOAD_CONST               ('invalid', 'divide')
              604  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              606  SETUP_WITH          826  'to 826'
              608  POP_TOP          

 L. 813       610  LOAD_GLOBAL              contextlib
              612  LOAD_METHOD              suppress
              614  LOAD_GLOBAL              TypeError
              616  CALL_METHOD_1         1  ''
              618  SETUP_WITH          816  'to 816'
              620  POP_TOP          

 L. 814       622  LOAD_GLOBAL              abs
              624  LOAD_FAST                'x'
              626  LOAD_FAST                'y'
              628  BINARY_SUBTRACT  
              630  CALL_FUNCTION_1       1  ''
              632  STORE_FAST               'error'

 L. 815       634  LOAD_FAST                'max'
              636  LOAD_FAST                'error'
              638  CALL_FUNCTION_1       1  ''
              640  STORE_FAST               'max_abs_error'

 L. 816       642  LOAD_GLOBAL              getattr
              644  LOAD_FAST                'error'
              646  LOAD_STR                 'dtype'
              648  LOAD_FAST                'object_'
              650  CALL_FUNCTION_3       3  ''
              652  LOAD_FAST                'object_'
              654  COMPARE_OP               ==
          656_658  POP_JUMP_IF_FALSE   680  'to 680'

 L. 817       660  LOAD_FAST                'remarks'
              662  LOAD_METHOD              append
              664  LOAD_STR                 'Max absolute difference: '

 L. 818       666  LOAD_GLOBAL              str
              668  LOAD_FAST                'max_abs_error'
              670  CALL_FUNCTION_1       1  ''

 L. 817       672  BINARY_ADD       
              674  CALL_METHOD_1         1  ''
              676  POP_TOP          
              678  JUMP_FORWARD        698  'to 698'
            680_0  COME_FROM           656  '656'

 L. 820       680  LOAD_FAST                'remarks'
              682  LOAD_METHOD              append
              684  LOAD_STR                 'Max absolute difference: '

 L. 821       686  LOAD_FAST                'array2string'
              688  LOAD_FAST                'max_abs_error'
              690  CALL_FUNCTION_1       1  ''

 L. 820       692  BINARY_ADD       
              694  CALL_METHOD_1         1  ''
              696  POP_TOP          
            698_0  COME_FROM           678  '678'

 L. 826       698  LOAD_DEREF               'bool_'
              700  LOAD_FAST                'y'
              702  LOAD_CONST               0
              704  COMPARE_OP               !=
              706  CALL_FUNCTION_1       1  ''
              708  STORE_FAST               'nonzero'

 L. 827       710  LOAD_FAST                'all'
              712  LOAD_FAST                'nonzero'
              714  UNARY_INVERT     
              716  CALL_FUNCTION_1       1  ''
          718_720  POP_JUMP_IF_FALSE   732  'to 732'

 L. 828       722  LOAD_FAST                'array'
              724  LOAD_DEREF               'inf'
              726  CALL_FUNCTION_1       1  ''
              728  STORE_FAST               'max_rel_error'
              730  JUMP_FORWARD        756  'to 756'
            732_0  COME_FROM           718  '718'

 L. 830       732  LOAD_FAST                'max'
              734  LOAD_FAST                'error'
              736  LOAD_FAST                'nonzero'
              738  BINARY_SUBSCR    
              740  LOAD_GLOBAL              abs
              742  LOAD_FAST                'y'
              744  LOAD_FAST                'nonzero'
              746  BINARY_SUBSCR    
              748  CALL_FUNCTION_1       1  ''
              750  BINARY_TRUE_DIVIDE
              752  CALL_FUNCTION_1       1  ''
              754  STORE_FAST               'max_rel_error'
            756_0  COME_FROM           730  '730'

 L. 831       756  LOAD_GLOBAL              getattr
              758  LOAD_FAST                'error'
              760  LOAD_STR                 'dtype'
              762  LOAD_FAST                'object_'
              764  CALL_FUNCTION_3       3  ''
              766  LOAD_FAST                'object_'
              768  COMPARE_OP               ==
          770_772  POP_JUMP_IF_FALSE   794  'to 794'

 L. 832       774  LOAD_FAST                'remarks'
              776  LOAD_METHOD              append
              778  LOAD_STR                 'Max relative difference: '

 L. 833       780  LOAD_GLOBAL              str
              782  LOAD_FAST                'max_rel_error'
              784  CALL_FUNCTION_1       1  ''

 L. 832       786  BINARY_ADD       
              788  CALL_METHOD_1         1  ''
              790  POP_TOP          
              792  JUMP_FORWARD        812  'to 812'
            794_0  COME_FROM           770  '770'

 L. 835       794  LOAD_FAST                'remarks'
              796  LOAD_METHOD              append
              798  LOAD_STR                 'Max relative difference: '

 L. 836       800  LOAD_FAST                'array2string'
              802  LOAD_FAST                'max_rel_error'
              804  CALL_FUNCTION_1       1  ''

 L. 835       806  BINARY_ADD       
              808  CALL_METHOD_1         1  ''
              810  POP_TOP          
            812_0  COME_FROM           792  '792'
              812  POP_BLOCK        
              814  BEGIN_FINALLY    
            816_0  COME_FROM_WITH      618  '618'
              816  WITH_CLEANUP_START
              818  WITH_CLEANUP_FINISH
              820  END_FINALLY      
              822  POP_BLOCK        
              824  BEGIN_FINALLY    
            826_0  COME_FROM_WITH      606  '606'
              826  WITH_CLEANUP_START
              828  WITH_CLEANUP_FINISH
              830  END_FINALLY      

 L. 838       832  LOAD_DEREF               'err_msg'
              834  LOAD_STR                 '\n'
              836  LOAD_STR                 '\n'
              838  LOAD_METHOD              join
              840  LOAD_FAST                'remarks'
              842  CALL_METHOD_1         1  ''
              844  BINARY_ADD       
              846  INPLACE_ADD      
              848  STORE_DEREF              'err_msg'

 L. 839       850  LOAD_GLOBAL              build_err_msg
              852  LOAD_FAST                'ox'
              854  LOAD_FAST                'oy'
              856  BUILD_LIST_2          2 
              858  LOAD_DEREF               'err_msg'

 L. 840       860  LOAD_DEREF               'verbose'

 L. 840       862  LOAD_DEREF               'header'

 L. 841       864  LOAD_CONST               ('x', 'y')

 L. 841       866  LOAD_DEREF               'precision'

 L. 839       868  LOAD_CONST               ('verbose', 'header', 'names', 'precision')
              870  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              872  STORE_FAST               'msg'

 L. 842       874  LOAD_GLOBAL              AssertionError
              876  LOAD_FAST                'msg'
              878  CALL_FUNCTION_1       1  ''
              880  RAISE_VARARGS_1       1  'exception instance'
            882_0  COME_FROM           522  '522'
              882  POP_BLOCK        
              884  JUMP_FORWARD        972  'to 972'
            886_0  COME_FROM_FINALLY   128  '128'

 L. 843       886  DUP_TOP          
              888  LOAD_GLOBAL              ValueError
              890  COMPARE_OP               exception-match
          892_894  POP_JUMP_IF_FALSE   970  'to 970'
              896  POP_TOP          
              898  POP_TOP          
              900  POP_TOP          

 L. 844       902  LOAD_CONST               0
              904  LOAD_CONST               None
              906  IMPORT_NAME              traceback
              908  STORE_FAST               'traceback'

 L. 845       910  LOAD_FAST                'traceback'
              912  LOAD_METHOD              format_exc
              914  CALL_METHOD_0         0  ''
              916  STORE_FAST               'efmt'

 L. 846       918  LOAD_STR                 'error during assertion:\n\n'
              920  LOAD_FAST                'efmt'
              922  FORMAT_VALUE          0  ''
              924  LOAD_STR                 '\n\n'
              926  LOAD_DEREF               'header'
              928  FORMAT_VALUE          0  ''
              930  BUILD_STRING_4        4 
              932  STORE_DEREF              'header'

 L. 848       934  LOAD_GLOBAL              build_err_msg
              936  LOAD_FAST                'x'
              938  LOAD_FAST                'y'
              940  BUILD_LIST_2          2 
              942  LOAD_DEREF               'err_msg'
              944  LOAD_DEREF               'verbose'
              946  LOAD_DEREF               'header'

 L. 849       948  LOAD_CONST               ('x', 'y')

 L. 849       950  LOAD_DEREF               'precision'

 L. 848       952  LOAD_CONST               ('verbose', 'header', 'names', 'precision')
              954  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              956  STORE_FAST               'msg'

 L. 850       958  LOAD_GLOBAL              ValueError
              960  LOAD_FAST                'msg'
              962  CALL_FUNCTION_1       1  ''
              964  RAISE_VARARGS_1       1  'exception instance'
              966  POP_EXCEPT       
              968  JUMP_FORWARD        972  'to 972'
            970_0  COME_FROM           892  '892'
              970  END_FINALLY      
            972_0  COME_FROM           968  '968'
            972_1  COME_FROM           884  '884'

Parse error at or near `LOAD_CONST' instruction at offset 444


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

 L.1019         0  SETUP_FINALLY       122  'to 122'

 L.1020         2  LOAD_DEREF               'npany'
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

 L.1021        26  LOAD_GLOBAL              gisinf
               28  LOAD_FAST                'x'
               30  CALL_FUNCTION_1       1  ''
               32  STORE_FAST               'xinfid'

 L.1022        34  LOAD_GLOBAL              gisinf
               36  LOAD_FAST                'y'
               38  CALL_FUNCTION_1       1  ''
               40  STORE_FAST               'yinfid'

 L.1023        42  LOAD_FAST                'xinfid'
               44  LOAD_FAST                'yinfid'
               46  COMPARE_OP               ==
               48  LOAD_METHOD              all
               50  CALL_METHOD_0         0  ''
               52  POP_JUMP_IF_TRUE     60  'to 60'

 L.1024        54  POP_BLOCK        
               56  LOAD_CONST               False
               58  RETURN_VALUE     
             60_0  COME_FROM            52  '52'

 L.1026        60  LOAD_FAST                'x'
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

 L.1027        88  LOAD_FAST                'x'
               90  LOAD_FAST                'y'
               92  COMPARE_OP               ==
               94  POP_BLOCK        
               96  RETURN_VALUE     
             98_0  COME_FROM            86  '86'
             98_1  COME_FROM            80  '80'

 L.1028        98  LOAD_FAST                'x'
              100  LOAD_FAST                'xinfid'
              102  UNARY_INVERT     
              104  BINARY_SUBSCR    
              106  STORE_FAST               'x'

 L.1029       108  LOAD_FAST                'y'
              110  LOAD_FAST                'yinfid'
              112  UNARY_INVERT     
              114  BINARY_SUBSCR    
              116  STORE_FAST               'y'
            118_0  COME_FROM            24  '24'
              118  POP_BLOCK        
              120  JUMP_FORWARD        146  'to 146'
            122_0  COME_FROM_FINALLY     0  '0'

 L.1030       122  DUP_TOP          
              124  LOAD_GLOBAL              TypeError
              126  LOAD_GLOBAL              NotImplementedError
              128  BUILD_TUPLE_2         2 
              130  COMPARE_OP               exception-match
              132  POP_JUMP_IF_FALSE   144  'to 144'
              134  POP_TOP          
              136  POP_TOP          
              138  POP_TOP          

 L.1031       140  POP_EXCEPT       
              142  JUMP_FORWARD        146  'to 146'
            144_0  COME_FROM           132  '132'
              144  END_FINALLY      
            146_0  COME_FROM           142  '142'
            146_1  COME_FROM           120  '120'

 L.1035       146  LOAD_DEREF               'result_type'
              148  LOAD_FAST                'y'
              150  LOAD_CONST               1.0
              152  CALL_FUNCTION_2       2  ''
              154  STORE_FAST               'dtype'

 L.1036       156  LOAD_DEREF               'array'
              158  LOAD_FAST                'y'
              160  LOAD_FAST                'dtype'
              162  LOAD_CONST               False
              164  LOAD_CONST               True
              166  LOAD_CONST               ('dtype', 'copy', 'subok')
              168  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              170  STORE_FAST               'y'

 L.1037       172  LOAD_GLOBAL              abs
              174  LOAD_FAST                'x'
              176  LOAD_FAST                'y'
              178  BINARY_SUBTRACT  
              180  CALL_FUNCTION_1       1  ''
              182  STORE_FAST               'z'

 L.1039       184  LOAD_DEREF               'issubdtype'
              186  LOAD_FAST                'z'
              188  LOAD_ATTR                dtype
              190  LOAD_DEREF               'number'
              192  CALL_FUNCTION_2       2  ''
              194  POP_JUMP_IF_TRUE    206  'to 206'

 L.1040       196  LOAD_FAST                'z'
              198  LOAD_METHOD              astype
              200  LOAD_DEREF               'float_'
              202  CALL_METHOD_1         1  ''
              204  STORE_FAST               'z'
            206_0  COME_FROM           194  '194'

 L.1042       206  LOAD_FAST                'z'
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
    if not isinstance(actual, str):
        raise AssertionError(repr(type(actual)))
    else:
        if not isinstance(desired, str):
            raise AssertionError(repr(type(desired)))
        else:
            if desired == actual:
                return
            diff = list(difflib.Differ().compareactual.splitlinesTruedesired.splitlinesTrue)
            diff_list = []
            while diff:
                d1 = diff.pop0
                if d1.startswith'  ':
                    pass
                elif d1.startswith'- ':
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
                else:
                    raise AssertionError(repr(d1))

        return diff_list or None
    msg = f"Differences in strings:\n{''.joindiff_list.rstrip()}"
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
    else:
        name = os.path.splitextos.path.basenamefilename[0]
        m = npy_load_module(name, filename)
        tests = doctest.DocTestFinder().findm
        runner = doctest.DocTestRunner(verbose=False)
        msg = []
        if raise_on_error:
            out = lambda s: msg.appends
        else:
            out = None
    for test in tests:
        runner.run(test, out=out)
    else:
        if runner.failures > 0:
            if raise_on_error:
                raise AssertionError('Some doctests failed:\n%s' % '\n'.joinmsg)


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

 L.1378         0  LOAD_FAST                'testmatch'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    26  'to 26'

 L.1379         8  LOAD_GLOBAL              re
               10  LOAD_METHOD              compile
               12  LOAD_STR                 '(?:^|[\\\\b_\\\\.%s-])[Tt]est'
               14  LOAD_GLOBAL              os
               16  LOAD_ATTR                sep
               18  BINARY_MODULO    
               20  CALL_METHOD_1         1  ''
               22  STORE_FAST               'testmatch'
               24  JUMP_FORWARD         36  'to 36'
             26_0  COME_FROM             6  '6'

 L.1381        26  LOAD_GLOBAL              re
               28  LOAD_METHOD              compile
               30  LOAD_FAST                'testmatch'
               32  CALL_METHOD_1         1  ''
               34  STORE_FAST               'testmatch'
             36_0  COME_FROM            24  '24'

 L.1382        36  LOAD_FAST                'cls'
               38  LOAD_ATTR                __dict__
               40  STORE_FAST               'cls_attr'

 L.1385        42  LOAD_CONST               0
               44  LOAD_CONST               ('isfunction',)
               46  IMPORT_NAME              inspect
               48  IMPORT_FROM              isfunction
               50  STORE_DEREF              'isfunction'
               52  POP_TOP          

 L.1387        54  LOAD_CLOSURE             'isfunction'
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

 L.1388        76  LOAD_FAST                'methods'
               78  GET_ITER         
             80_0  COME_FROM           156  '156'
             80_1  COME_FROM           146  '146'
               80  FOR_ITER            176  'to 176'
               82  STORE_FAST               'function'

 L.1389        84  SETUP_FINALLY       114  'to 114'

 L.1390        86  LOAD_GLOBAL              hasattr
               88  LOAD_FAST                'function'
               90  LOAD_STR                 'compat_func_name'
               92  CALL_FUNCTION_2       2  ''
               94  POP_JUMP_IF_FALSE   104  'to 104'

 L.1391        96  LOAD_FAST                'function'
               98  LOAD_ATTR                compat_func_name
              100  STORE_FAST               'funcname'
              102  JUMP_FORWARD        110  'to 110'
            104_0  COME_FROM            94  '94'

 L.1393       104  LOAD_FAST                'function'
              106  LOAD_ATTR                __name__
              108  STORE_FAST               'funcname'
            110_0  COME_FROM           102  '102'
              110  POP_BLOCK        
              112  JUMP_FORWARD        138  'to 138'
            114_0  COME_FROM_FINALLY    84  '84'

 L.1394       114  DUP_TOP          
              116  LOAD_GLOBAL              AttributeError
              118  COMPARE_OP               exception-match
              120  POP_JUMP_IF_FALSE   136  'to 136'
              122  POP_TOP          
              124  POP_TOP          
              126  POP_TOP          

 L.1396       128  POP_EXCEPT       
              130  JUMP_BACK            80  'to 80'
              132  POP_EXCEPT       
              134  JUMP_FORWARD        138  'to 138'
            136_0  COME_FROM           120  '120'
              136  END_FINALLY      
            138_0  COME_FROM           134  '134'
            138_1  COME_FROM           112  '112'

 L.1397       138  LOAD_FAST                'testmatch'
              140  LOAD_METHOD              search
              142  LOAD_FAST                'funcname'
              144  CALL_METHOD_1         1  ''
              146  POP_JUMP_IF_FALSE    80  'to 80'
              148  LOAD_FAST                'funcname'
              150  LOAD_METHOD              startswith
              152  LOAD_STR                 '_'
              154  CALL_METHOD_1         1  ''
              156  POP_JUMP_IF_TRUE     80  'to 80'

 L.1398       158  LOAD_GLOBAL              setattr
              160  LOAD_FAST                'cls'
              162  LOAD_FAST                'funcname'
              164  LOAD_FAST                'decorator'
              166  LOAD_FAST                'function'
              168  CALL_FUNCTION_1       1  ''
              170  CALL_FUNCTION_3       3  ''
              172  POP_TOP          
              174  JUMP_BACK            80  'to 80'

Parse error at or near `POP_EXCEPT' instruction at offset 132


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
    frame = sys._getframe1
    locs, globs = frame.f_locals, frame.f_globals
    code = compile(code_str, f"Test name: {label} ", 'exec')
    i = 0
    elapsed = jiffies()
    while i < times:
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
    b = np.arange10000.reshape100100
    c = b
    i = 1
    gc.disable()
    try:
        rc = sys.getrefcounti
        for j in range(15):
            d = op(b, c)
        else:
            assert_(sys.getrefcounti >= rc)

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

    actual, desired = np.asanyarrayactual, np.asanyarraydesired
    header = f"Not equal to tolerance rtol={rtol:g}, atol={atol:g}"
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
    ax = np.absx
    ay = np.absy
    ref = nulp * np.spacingnp.where(ax > ay)axay
    if not np.all(np.abs(x - y) <= ref):
        if np.iscomplexobjx or np.iscomplexobjy:
            msg = 'X and Y are not equal to %d ULP' % nulp
        else:
            max_nulp = np.maxnulp_diff(x, y)
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
     maxulp, np.maxret)
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
        x = np.arrayx
        y = np.arrayy
    t = np.common_typexy
    if np.iscomplexobjx or np.iscomplexobjy:
        raise NotImplementedError('_nulp not implemented for complex array')
    x = np.array([x], dtype=t)
    y = np.array([y], dtype=t)
    x[np.isnanx] = np.nan
    y[np.isnany] = np.nan
    if not x.shape == y.shape:
        raise ValueError('x and y do not have the same shape: %s - %s' % (
         x.shape, y.shape))

    def _diff(rx, ry, vdt):
        diff = np.array((rx - ry), dtype=vdt)
        return np.absdiff

    rx = integer_repr(x)
    ry = integer_repr(y)
    return _diff(rx, ry, t)


def _integer_repr(x, vdt, comp):
    rx = x.viewvdt
    if not rx.size == 1:
        rx[rx < 0] = comp - rx[(rx < 0)]
    else:
        if rx < 0:
            rx = comp - rx
    return rx


def integer_repr(x):
    """Return the signed-magnitude interpretation of the binary representation
    of x."""
    import numpy as np
    if x.dtype == np.float16:
        return _integer_repr(x, np.int16, np.int16(-32768))
    if x.dtype == np.float32:
        return _integer_repr(x, np.int32, np.int32(-2147483648))
    if x.dtype == np.float64:
        return _integer_repr(x, np.int64, np.int64(-9223372036854775808))
    raise ValueError(f"Unsupported dtype {x.dtype}")


@contextlib.contextmanager
def _assert_warns_context(warning_class, name=None):
    __tracebackhide__ = True
    with suppress_warnings() as (sup):
        l = sup.recordwarning_class
        (yield)
        if not len(l) > 0:
            name_str = f" when calling {name}" if name is not None else ''
            raise AssertionError('No warning raised' + name_str)


def assert_warns--- This code section failed: ---

 L.1795         0  LOAD_FAST                'args'
                2  POP_JUMP_IF_TRUE     12  'to 12'

 L.1796         4  LOAD_GLOBAL              _assert_warns_context
                6  LOAD_FAST                'warning_class'
                8  CALL_FUNCTION_1       1  ''
               10  RETURN_VALUE     
             12_0  COME_FROM             2  '2'

 L.1798        12  LOAD_FAST                'args'
               14  LOAD_CONST               0
               16  BINARY_SUBSCR    
               18  STORE_FAST               'func'

 L.1799        20  LOAD_FAST                'args'
               22  LOAD_CONST               1
               24  LOAD_CONST               None
               26  BUILD_SLICE_2         2 
               28  BINARY_SUBSCR    
               30  STORE_FAST               'args'

 L.1800        32  LOAD_GLOBAL              _assert_warns_context
               34  LOAD_FAST                'warning_class'
               36  LOAD_FAST                'func'
               38  LOAD_ATTR                __name__
               40  LOAD_CONST               ('name',)
               42  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               44  SETUP_WITH           70  'to 70'
               46  POP_TOP          

 L.1801        48  LOAD_FAST                'func'
               50  LOAD_FAST                'args'
               52  LOAD_FAST                'kwargs'
               54  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               56  POP_BLOCK        
               58  ROT_TWO          
               60  BEGIN_FINALLY    
               62  WITH_CLEANUP_START
               64  WITH_CLEANUP_FINISH
               66  POP_FINALLY           0  ''
               68  RETURN_VALUE     
             70_0  COME_FROM_WITH       44  '44'
               70  WITH_CLEANUP_START
               72  WITH_CLEANUP_FINISH
               74  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 58


@contextlib.contextmanager
def _assert_no_warnings_context(name=None):
    __tracebackhide__ = True
    with warnings.catch_warnings(record=True) as (l):
        warnings.simplefilter'always'
        (yield)
        if len(l) > 0:
            name_str = f" when calling {name}" if name is not None else ''
            raise AssertionError(f"Got warnings{name_str}: {l}")


def assert_no_warnings--- This code section failed: ---

 L.1842         0  LOAD_FAST                'args'
                2  POP_JUMP_IF_TRUE     10  'to 10'

 L.1843         4  LOAD_GLOBAL              _assert_no_warnings_context
                6  CALL_FUNCTION_0       0  ''
                8  RETURN_VALUE     
             10_0  COME_FROM             2  '2'

 L.1845        10  LOAD_FAST                'args'
               12  LOAD_CONST               0
               14  BINARY_SUBSCR    
               16  STORE_FAST               'func'

 L.1846        18  LOAD_FAST                'args'
               20  LOAD_CONST               1
               22  LOAD_CONST               None
               24  BUILD_SLICE_2         2 
               26  BINARY_SUBSCR    
               28  STORE_FAST               'args'

 L.1847        30  LOAD_GLOBAL              _assert_no_warnings_context
               32  LOAD_FAST                'func'
               34  LOAD_ATTR                __name__
               36  LOAD_CONST               ('name',)
               38  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               40  SETUP_WITH           66  'to 66'
               42  POP_TOP          

 L.1848        44  LOAD_FAST                'func'
               46  LOAD_FAST                'args'
               48  LOAD_FAST                'kwargs'
               50  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               52  POP_BLOCK        
               54  ROT_TWO          
               56  BEGIN_FINALLY    
               58  WITH_CLEANUP_START
               60  WITH_CLEANUP_FINISH
               62  POP_FINALLY           0  ''
               64  RETURN_VALUE     
             66_0  COME_FROM_WITH       40  '40'
               66  WITH_CLEANUP_START
               68  WITH_CLEANUP_FINISH
               70  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 54


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
                inp = lambda : arange(s, dtype=dtype)[o:]
                out = empty((s,), dtype=dtype)[o:]
                (yield (out, inp(), ufmt % (o, o, s, dtype, 'out of place')))
                d = inp()
                (yield (d, d, ufmt % (o, o, s, dtype, 'in place')))
                (yield (out[1:], inp()[:-1],
                 ufmt % (
                  o + 1, o, s - 1, dtype, 'out of place')))
                (yield (out[:-1], inp()[1:],
                 ufmt % (
                  o, o + 1, s - 1, dtype, 'out of place')))
                (yield (inp()[:-1], inp()[1:],
                 ufmt % (
                  o, o + 1, s - 1, dtype, 'aliased')))
                (yield (inp()[1:], inp()[:-1],
                 ufmt % (
                  o + 1, o, s - 1, dtype, 'aliased')))
            if type == 'binary':
                inp1 = lambda : arange(s, dtype=dtype)[o:]
                inp2 = lambda : arange(s, dtype=dtype)[o:]
                out = empty((s,), dtype=dtype)[o:]
                (yield (out, inp1(), inp2(),
                 bfmt % (
                  o, o, o, s, dtype, 'out of place')))
                d = inp1()
                (yield (d, d, inp2(),
                 bfmt % (
                  o, o, o, s, dtype, 'in place1')))
                d = inp2()
                (yield (d, inp1(), d,
                 bfmt % (
                  o, o, o, s, dtype, 'in place2')))
                (yield (out[1:], inp1()[:-1], inp2()[:-1],
                 bfmt % (
                  o + 1, o, o, s - 1, dtype, 'out of place')))
                (yield (out[:-1], inp1()[1:], inp2()[:-1],
                 bfmt % (
                  o, o + 1, o, s - 1, dtype, 'out of place')))
                (yield (out[:-1], inp1()[:-1], inp2()[1:],
                 bfmt % (
                  o, o, o + 1, s - 1, dtype, 'out of place')))
                (yield (inp1()[1:], inp1()[:-1], inp2()[:-1],
                 bfmt % (
                  o + 1, o, o, s - 1, dtype, 'aliased')))
                (yield (inp1()[:-1], inp1()[1:], inp2()[:-1],
                 bfmt % (
                  o, o + 1, o, s - 1, dtype, 'aliased')))
                (yield (inp1()[:-1], inp1()[:-1], inp2()[1:],
                 bfmt % (
                  o, o, o + 1, s - 1, dtype, 'aliased')))


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
        (yield tmpdir)
    finally:
        shutil.rmtreetmpdir


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
    os.closefd
    try:
        (yield path)
    finally:
        os.removepath


class clear_and_catch_warnings(warnings.catch_warnings):
    __doc__ = " Context manager that resets warning registry for catching warnings\n\n    Warnings can be slippery, because, whenever a warning is triggered, Python\n    adds a ``__warningregistry__`` member to the *calling* module.  This makes\n    it impossible to retrigger the warning in this module, whatever you put in\n    the warnings filters.  This context manager accepts a sequence of `modules`\n    as a keyword argument to its constructor and:\n\n    * stores and removes any ``__warningregistry__`` entries in given `modules`\n      on entry;\n    * resets ``__warningregistry__`` to its previous state on exit.\n\n    This makes it possible to trigger any warning afresh inside the context\n    manager without disturbing the state of warnings outside.\n\n    For compatibility with Python 3.0, please consider all arguments to be\n    keyword-only.\n\n    Parameters\n    ----------\n    record : bool, optional\n        Specifies whether warnings should be captured by a custom\n        implementation of ``warnings.showwarning()`` and be appended to a list\n        returned by the context manager. Otherwise None is returned by the\n        context manager. The objects appended to the list are arguments whose\n        attributes mirror the arguments to ``showwarning()``.\n    modules : sequence, optional\n        Sequence of modules for which to reset warnings registry on entry and\n        restore on exit. To work correctly, all 'ignore' filters should\n        filter by one of these modules.\n\n    Examples\n    --------\n    >>> import warnings\n    >>> with np.testing.clear_and_catch_warnings(\n    ...         modules=[np.core.fromnumeric]):\n    ...     warnings.simplefilter('always')\n    ...     warnings.filterwarnings('ignore', module='np.core.fromnumeric')\n    ...     # do something that raises a warning but ignore those in\n    ...     # np.core.fromnumeric\n    "
    class_modules = ()

    def __init__(self, record=False, modules=()):
        self.modules = set(modules).unionself.class_modules
        self._warnreg_copies = {}
        super(clear_and_catch_warnings, self).__init__(record=record)

    def __enter__(self):
        for mod in self.modules:
            if hasattr(mod, '__warningregistry__'):
                mod_reg = mod.__warningregistry__
                self._warnreg_copies[mod] = mod_reg.copy()
                mod_reg.clear()
            return super(clear_and_catch_warnings, self).__enter__()

    def __exit__(self, *exc_info):
        (super(clear_and_catch_warnings, self).__exit__)(*exc_info)
        for mod in self.modules:
            if hasattr(mod, '__warningregistry__'):
                mod.__warningregistry__.clear()
            if mod in self._warnreg_copies:
                mod.__warningregistry__.updateself._warnreg_copies[mod]


class suppress_warnings:
    __doc__ = '\n    Context manager and decorator doing much the same as\n    ``warnings.catch_warnings``.\n\n    However, it also provides a filter mechanism to work around\n    https://bugs.python.org/issue4180.\n\n    This bug causes Python before 3.4 to not reliably show warnings again\n    after they have been ignored once (even within catch_warnings). It\n    means that no "ignore" filter can be used easily, since following\n    tests might need to see the warning. Additionally it allows easier\n    specificity for testing warnings and can be nested.\n\n    Parameters\n    ----------\n    forwarding_rule : str, optional\n        One of "always", "once", "module", or "location". Analogous to\n        the usual warnings module filter mode, it is useful to reduce\n        noise mostly on the outmost level. Unsuppressed and unrecorded\n        warnings will be forwarded based on this rule. Defaults to "always".\n        "location" is equivalent to the warnings "default", match by exact\n        location the warning warning originated from.\n\n    Notes\n    -----\n    Filters added inside the context manager will be discarded again\n    when leaving it. Upon entering all filters defined outside a\n    context will be applied automatically.\n\n    When a recording filter is added, matching warnings are stored in the\n    ``log`` attribute as well as in the list returned by ``record``.\n\n    If filters are added and the ``module`` keyword is given, the\n    warning registry of this module will additionally be cleared when\n    applying it, entering the context, or exiting it. This could cause\n    warnings to appear a second time after leaving the context if they\n    were configured to be printed once (default) and were already\n    printed before the context was entered.\n\n    Nesting this context manager will work as expected when the\n    forwarding rule is "always" (default). Unfiltered and unrecorded\n    warnings will be passed out and be matched by the outer level.\n    On the outmost level they will be printed (or caught by another\n    warnings context). The forwarding rule argument can modify this\n    behaviour.\n\n    Like ``catch_warnings`` this context manager is not threadsafe.\n\n    Examples\n    --------\n\n    With a context manager::\n\n        with np.testing.suppress_warnings() as sup:\n            sup.filter(DeprecationWarning, "Some text")\n            sup.filter(module=np.ma.core)\n            log = sup.record(FutureWarning, "Does this occur?")\n            command_giving_warnings()\n            # The FutureWarning was given once, the filtered warnings were\n            # ignored. All other warnings abide outside settings (may be\n            # printed/error)\n            assert_(len(log) == 1)\n            assert_(len(sup.log) == 1)  # also stored in log attribute\n\n    Or as a decorator::\n\n        sup = np.testing.suppress_warnings()\n        sup.filter(module=np.ma.core)  # module must match exactly\n        @sup\n        def some_function():\n            # do something which causes a warning in np.ma.core\n            pass\n    '

    def __init__(self, forwarding_rule='always'):
        self._entered = False
        self._suppressions = []
        if forwarding_rule not in {'location', 'always', 'once', 'module'}:
            raise ValueError('unsupported forwarding rule.')
        self._forwarding_rule = forwarding_rule

    def _clear_registries(self):
        if hasattr(warnings, '_filters_mutated'):
            warnings._filters_mutated()
            return None
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
                self._tmp_modules.addmodule
                self._clear_registries()
            self._tmp_suppressions.append(
             category, message, re.compilemessagere.I, module, record)
        else:
            self._suppressions.append(
             category, message, re.compilemessagere.I, module, record)
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
                self._tmp_modules.addmod
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
                if pattern.matchmessage.args[0] is not None:
                    if mod is None:
                        if rec is not None:
                            msg = WarningMessage(message, category, filename, 
                             lineno, **kwargs)
                            self.log.appendmsg
                            rec.appendmsg
                        return None
                if mod.__file__.startswithfilename:
                    if rec is not None:
                        msg = WarningMessage(message, category, filename, 
                         lineno, **kwargs)
                        self.log.appendmsg
                        rec.appendmsg
                    return None
        else:
            if self._forwarding_rule == 'always':
                if use_warnmsg is None:
                    (self._orig_show)(message, category, filename, lineno, *args, **kwargs)
                else:
                    self._orig_showmsguse_warnmsg
                return
                if self._forwarding_rule == 'once':
                    signature = (
                     message.args, category)
            elif self._forwarding_rule == 'module':
                signature = (
                 message.args, category, filename)
            else:
                if self._forwarding_rule == 'location':
                    signature = (
                     message.args, category, filename, lineno)
                if signature in self._forwarded:
                    return
                    self._forwarded.addsignature
                    if use_warnmsg is None:
                        (self._orig_show)(message, category, filename, lineno, *args, **kwargs)
                else:
                    self._orig_showmsguse_warnmsg

    def __call__(self, func):
        """
        Function decorator to apply certain suppressions to a whole
        function.
        """

        @wraps(func)
        def new_func--- This code section failed: ---

 L.2300         0  LOAD_DEREF               'self'
                2  SETUP_WITH           28  'to 28'
                4  POP_TOP          

 L.2301         6  LOAD_DEREF               'func'
                8  LOAD_FAST                'args'
               10  LOAD_FAST                'kwargs'
               12  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               14  POP_BLOCK        
               16  ROT_TWO          
               18  BEGIN_FINALLY    
               20  WITH_CLEANUP_START
               22  WITH_CLEANUP_FINISH
               24  POP_FINALLY           0  ''
               26  RETURN_VALUE     
             28_0  COME_FROM_WITH        2  '2'
               28  WITH_CLEANUP_START
               30  WITH_CLEANUP_FINISH
               32  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 16

        return new_func


@contextlib.contextmanager
def _assert_no_gc_cycles_context(name=None):
    __tracebackhide__ = True
    if not HAS_REFCOUNT:
        (yield)
        return
    assert_(gc.isenabled())
    gc.disable()
    gc_debug = gc.get_debug()
    try:
        for i in range(100):
            if gc.collect() == 0:
                break
            raise RuntimeError('Unable to fully collect garbage - perhaps a __del__ method is creating more reference cycles?')
            gc.set_debuggc.DEBUG_SAVEALL
            (yield)
            n_objects_in_cycles = gc.collect()
            objects_in_cycles = gc.garbage[:]

    finally:
        del gc.garbage[:]
        gc.set_debuggc_debug
        gc.enable()

    if n_objects_in_cycles:
        name_str = f" when calling {name}" if name is not None else ''
        raise AssertionError('Reference cycles were found{}: {} objects were collected, of which {} are shown below:{}'.format(name_str, n_objects_in_cycles, len(objects_in_cycles), ''.join('\n  {} object with id={}:\n    {}'.formattype(o).__name__id(o)pprint.pformato.replace'\n''\n    ' for o in objects_in_cycles)))


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
        gc.collect()


def requires_memory(free_bytes):
    """Decorator to skip a test if not enough memory is available"""
    import pytest

    def decorator(func):

        @wraps(func)
        def wrapper--- This code section failed: ---

 L.2417         0  LOAD_GLOBAL              check_free_memory
                2  LOAD_DEREF               'free_bytes'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'msg'

 L.2418         8  LOAD_FAST                'msg'
               10  LOAD_CONST               None
               12  COMPARE_OP               is-not
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L.2419        16  LOAD_DEREF               'pytest'
               18  LOAD_METHOD              skip
               20  LOAD_FAST                'msg'
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          
             26_0  COME_FROM            14  '14'

 L.2421        26  SETUP_FINALLY        40  'to 40'

 L.2422        28  LOAD_DEREF               'func'
               30  LOAD_FAST                'a'
               32  LOAD_FAST                'kw'
               34  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               36  POP_BLOCK        
               38  RETURN_VALUE     
             40_0  COME_FROM_FINALLY    26  '26'

 L.2423        40  DUP_TOP          
               42  LOAD_GLOBAL              MemoryError
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE    68  'to 68'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L.2425        54  LOAD_DEREF               'pytest'
               56  LOAD_METHOD              xfail
               58  LOAD_STR                 'MemoryError raised'
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          
               64  POP_EXCEPT       
               66  JUMP_FORWARD         70  'to 70'
             68_0  COME_FROM            46  '46'
               68  END_FINALLY      
             70_0  COME_FROM            66  '66'

Parse error at or near `POP_TOP' instruction at offset 50

        return wrapper

    return decorator


def check_free_memory(free_bytes):
    """
    Check whether `free_bytes` amount of memory is currently free.
    Returns: None if enough memory available, otherwise error message
    """
    env_var = 'NPY_AVAILABLE_MEM'
    env_value = os.environ.getenv_var
    if env_value is not None:
        try:
            mem_free = _parse_size(env_value)
        except ValueError as exc:
            try:
                raise ValueError(f"Invalid environment variable {env_var}: {exc}")
            finally:
                exc = None
                del exc

        else:
            msg = f"{free_bytes / 1000000000.0} GB memory required, but environment variable NPY_AVAILABLE_MEM={env_value} set"
    else:
        mem_free = _get_mem_available()
        if mem_free is None:
            msg = 'Could not determine available memory; set NPY_AVAILABLE_MEM environment variable (e.g. NPY_AVAILABLE_MEM=16GB) to run the test.'
            mem_free = -1
        else:
            msg = f"{free_bytes / 1000000000.0} GB memory required, but {mem_free / 1000000000.0} GB available"
    if mem_free < free_bytes:
        return msg


def _parse_size(size_str):
    """Convert memory size strings ('12 GB' etc.) to float"""
    suffixes = {'':1,  'b':1,  'k':1000, 
     'm':1000000,  'g':1000000000,  't':1000000000000,  'kb':1000, 
     'mb':1000000,  'gb':1000000000,  'tb':1000000000000,  'kib':1024, 
     'mib':1048576,  'gib':1073741824,  'tib':1099511627776}
    size_re = re.compile'^\\s*(\\d+|\\d+\\.\\d+)\\s*({0})\\s*$'.format'|'.joinsuffixes.keys()re.I
    m = size_re.matchsize_str.lower()
    if not m or m.group2 not in suffixes:
        raise ValueError(f"value {size_str!r} not a valid size")
    return int(float(m.group1) * suffixes[m.group2])


def _get_mem_available--- This code section failed: ---

 L.2479         0  SETUP_FINALLY        22  'to 22'

 L.2480         2  LOAD_CONST               0
                4  LOAD_CONST               None
                6  IMPORT_NAME              psutil
                8  STORE_FAST               'psutil'

 L.2481        10  LOAD_FAST                'psutil'
               12  LOAD_METHOD              virtual_memory
               14  CALL_METHOD_0         0  ''
               16  LOAD_ATTR                available
               18  POP_BLOCK        
               20  RETURN_VALUE     
             22_0  COME_FROM_FINALLY     0  '0'

 L.2482        22  DUP_TOP          
               24  LOAD_GLOBAL              ImportError
               26  LOAD_GLOBAL              AttributeError
               28  BUILD_TUPLE_2         2 
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    44  'to 44'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L.2483        40  POP_EXCEPT       
               42  JUMP_FORWARD         46  'to 46'
             44_0  COME_FROM            32  '32'
               44  END_FINALLY      
             46_0  COME_FROM            42  '42'

 L.2485        46  LOAD_GLOBAL              sys
               48  LOAD_ATTR                platform
               50  LOAD_METHOD              startswith
               52  LOAD_STR                 'linux'
               54  CALL_METHOD_1         1  ''
               56  POP_JUMP_IF_FALSE   168  'to 168'

 L.2486        58  BUILD_MAP_0           0 
               60  STORE_FAST               'info'

 L.2487        62  LOAD_GLOBAL              open
               64  LOAD_STR                 '/proc/meminfo'
               66  LOAD_STR                 'r'
               68  CALL_FUNCTION_2       2  ''
               70  SETUP_WITH          130  'to 130'
               72  STORE_FAST               'f'

 L.2488        74  LOAD_FAST                'f'
               76  GET_ITER         
               78  FOR_ITER            126  'to 126'
               80  STORE_FAST               'line'

 L.2489        82  LOAD_FAST                'line'
               84  LOAD_METHOD              split
               86  CALL_METHOD_0         0  ''
               88  STORE_FAST               'p'

 L.2490        90  LOAD_GLOBAL              int
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
              126  POP_BLOCK        
              128  BEGIN_FINALLY    
            130_0  COME_FROM_WITH       70  '70'
              130  WITH_CLEANUP_START
              132  WITH_CLEANUP_FINISH
              134  END_FINALLY      

 L.2492       136  LOAD_STR                 'memavailable'
              138  LOAD_FAST                'info'
              140  COMPARE_OP               in
              142  POP_JUMP_IF_FALSE   152  'to 152'

 L.2494       144  LOAD_FAST                'info'
              146  LOAD_STR                 'memavailable'
              148  BINARY_SUBSCR    
              150  RETURN_VALUE     
            152_0  COME_FROM           142  '142'

 L.2496       152  LOAD_FAST                'info'
              154  LOAD_STR                 'memfree'
              156  BINARY_SUBSCR    
              158  LOAD_FAST                'info'
              160  LOAD_STR                 'cached'
              162  BINARY_SUBSCR    
              164  BINARY_ADD       
              166  RETURN_VALUE     
            168_0  COME_FROM            56  '56'

Parse error at or near `POP_TOP' instruction at offset 36


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

 L.2512         0  LOAD_GLOBAL              sys
                2  LOAD_METHOD              gettrace
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'original_trace'

 L.2513         8  SETUP_FINALLY        34  'to 34'

 L.2514        10  LOAD_GLOBAL              sys
               12  LOAD_METHOD              settrace
               14  LOAD_CONST               None
               16  CALL_METHOD_1         1  ''
               18  POP_TOP          

 L.2515        20  LOAD_DEREF               'func'
               22  LOAD_FAST                'args'
               24  LOAD_FAST                'kwargs'
               26  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               28  POP_BLOCK        
               30  CALL_FINALLY         34  'to 34'
               32  RETURN_VALUE     
             34_0  COME_FROM            30  '30'
             34_1  COME_FROM_FINALLY     8  '8'

 L.2517        34  LOAD_GLOBAL              sys
               36  LOAD_METHOD              settrace
               38  LOAD_FAST                'original_trace'
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          
               44  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 30

    return wrapper