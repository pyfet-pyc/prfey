# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: comtypes\_comobject.py
from ctypes import FormatError, POINTER, Structure, WINFUNCTYPE, byref, c_long, c_void_p, oledll, pointer, windll
from _ctypes import CopyComPointer
import logging, os
from comtypes import COMError, ReturnHRESULT, instancemethod, _encode_idl
from comtypes.errorinfo import ISupportErrorInfo, ReportException, ReportError
from comtypes import IPersist
from comtypes.hresult import DISP_E_BADINDEX, DISP_E_MEMBERNOTFOUND, E_FAIL, E_NOINTERFACE, E_INVALIDARG, E_NOTIMPL, RPC_E_CHANGED_MODE, S_FALSE, S_OK
from comtypes.typeinfo import IProvideClassInfo, IProvideClassInfo2
logger = logging.getLogger(__name__)
_debug = logger.debug
_warning = logger.warning
_error = logger.error
DISPATCH_METHOD = 1
DISPATCH_PROPERTYGET = 2
DISPATCH_PROPERTYPUT = 4
DISPATCH_PROPERTYPUTREF = 8

class E_NotImplemented(Exception):
    __doc__ = 'COM method is not implemented'


def HRESULT_FROM_WIN32(errcode):
    """Convert a Windows error code into a HRESULT value."""
    if errcode is None:
        return 2147483648
    if errcode & 2147483648:
        return errcode
    return errcode & 65535 | 2147942400


def winerror(exc):
    """Return the windows error code from a WindowsError or COMError
    instance."""
    try:
        code = exc[0]
        if isinstance(code, int):
            return code
    except IndexError:
        pass
    else:
        return E_FAIL


def _do_implement(interface_name, method_name):

    def _not_implemented(*args):
        _debug('unimplemented method %s_%s called', interface_name, method_name)
        return E_NOTIMPL

    return _not_implemented


def catch_errors(obj, mth, paramflags, interface, mthname):
    clsid = getattr(obj, '_reg_clsid_', None)

    def call_with_this--- This code section failed: ---

 L.  75         0  SETUP_FINALLY        16  'to 16'

 L.  76         2  LOAD_DEREF               'mth'
                4  LOAD_FAST                'args'
                6  LOAD_FAST                'kw'
                8  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               10  STORE_FAST               'result'
               12  POP_BLOCK        
               14  JUMP_FORWARD        232  'to 232'
             16_0  COME_FROM_FINALLY     0  '0'

 L.  77        16  DUP_TOP          
               18  LOAD_GLOBAL              ReturnHRESULT
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    80  'to 80'
               24  POP_TOP          
               26  STORE_FAST               'err'
               28  POP_TOP          
               30  SETUP_FINALLY        68  'to 68'

 L.  78        32  LOAD_FAST                'err'
               34  LOAD_ATTR                args
               36  UNPACK_SEQUENCE_2     2 
               38  STORE_FAST               'hresult'
               40  STORE_FAST               'text'

 L.  79        42  LOAD_GLOBAL              ReportError
               44  LOAD_FAST                'text'
               46  LOAD_DEREF               'interface'
               48  LOAD_ATTR                _iid_
               50  LOAD_DEREF               'clsid'

 L.  80        52  LOAD_FAST                'hresult'

 L.  79        54  LOAD_CONST               ('iid', 'clsid', 'hresult')
               56  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               58  ROT_FOUR         
               60  POP_BLOCK        
               62  POP_EXCEPT       
               64  CALL_FINALLY         68  'to 68'
               66  RETURN_VALUE     
             68_0  COME_FROM            64  '64'
             68_1  COME_FROM_FINALLY    30  '30'
               68  LOAD_CONST               None
               70  STORE_FAST               'err'
               72  DELETE_FAST              'err'
               74  END_FINALLY      
               76  POP_EXCEPT       
               78  JUMP_FORWARD        232  'to 232'
             80_0  COME_FROM            22  '22'

 L.  81        80  DUP_TOP          
               82  LOAD_GLOBAL              COMError
               84  LOAD_GLOBAL              WindowsError
               86  BUILD_TUPLE_2         2 
               88  COMPARE_OP               exception-match
               90  POP_JUMP_IF_FALSE   150  'to 150'
               92  POP_TOP          
               94  STORE_FAST               'details'
               96  POP_TOP          
               98  SETUP_FINALLY       138  'to 138'

 L.  82       100  LOAD_GLOBAL              _error
              102  LOAD_STR                 'Exception in %s.%s implementation:'
              104  LOAD_DEREF               'interface'
              106  LOAD_ATTR                __name__

 L.  83       108  LOAD_DEREF               'mthname'

 L.  83       110  LOAD_CONST               True

 L.  82       112  LOAD_CONST               ('exc_info',)
              114  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              116  POP_TOP          

 L.  84       118  LOAD_GLOBAL              HRESULT_FROM_WIN32
              120  LOAD_GLOBAL              winerror
              122  LOAD_FAST                'details'
              124  CALL_FUNCTION_1       1  ''
              126  CALL_FUNCTION_1       1  ''
              128  ROT_FOUR         
              130  POP_BLOCK        
              132  POP_EXCEPT       
              134  CALL_FINALLY        138  'to 138'
              136  RETURN_VALUE     
            138_0  COME_FROM           134  '134'
            138_1  COME_FROM_FINALLY    98  '98'
              138  LOAD_CONST               None
              140  STORE_FAST               'details'
              142  DELETE_FAST              'details'
              144  END_FINALLY      
              146  POP_EXCEPT       
              148  JUMP_FORWARD        232  'to 232'
            150_0  COME_FROM            90  '90'

 L.  85       150  DUP_TOP          
              152  LOAD_GLOBAL              E_NotImplemented
              154  COMPARE_OP               exception-match
              156  POP_JUMP_IF_FALSE   186  'to 186'
              158  POP_TOP          
              160  POP_TOP          
              162  POP_TOP          

 L.  86       164  LOAD_GLOBAL              _warning
              166  LOAD_STR                 'Unimplemented method %s.%s called'
              168  LOAD_DEREF               'interface'
              170  LOAD_ATTR                __name__

 L.  87       172  LOAD_DEREF               'mthname'

 L.  86       174  CALL_FUNCTION_3       3  ''
              176  POP_TOP          

 L.  88       178  LOAD_GLOBAL              E_NOTIMPL
              180  ROT_FOUR         
              182  POP_EXCEPT       
              184  RETURN_VALUE     
            186_0  COME_FROM           156  '156'

 L.  89       186  POP_TOP          
              188  POP_TOP          
              190  POP_TOP          

 L.  90       192  LOAD_GLOBAL              _error
              194  LOAD_STR                 'Exception in %s.%s implementation:'
              196  LOAD_DEREF               'interface'
              198  LOAD_ATTR                __name__

 L.  91       200  LOAD_DEREF               'mthname'

 L.  91       202  LOAD_CONST               True

 L.  90       204  LOAD_CONST               ('exc_info',)
              206  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              208  POP_TOP          

 L.  92       210  LOAD_GLOBAL              ReportException
              212  LOAD_GLOBAL              E_FAIL
              214  LOAD_DEREF               'interface'
              216  LOAD_ATTR                _iid_
              218  LOAD_DEREF               'clsid'
              220  LOAD_CONST               ('clsid',)
              222  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              224  ROT_FOUR         
              226  POP_EXCEPT       
              228  RETURN_VALUE     
              230  END_FINALLY      
            232_0  COME_FROM           148  '148'
            232_1  COME_FROM            78  '78'
            232_2  COME_FROM            14  '14'

 L.  93       232  LOAD_FAST                'result'
              234  LOAD_CONST               None
              236  COMPARE_OP               is
          238_240  POP_JUMP_IF_FALSE   246  'to 246'

 L.  94       242  LOAD_GLOBAL              S_OK
              244  RETURN_VALUE     
            246_0  COME_FROM           238  '238'

 L.  95       246  LOAD_FAST                'result'
              248  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 60

    if paramflags is None:
        has_outargs = False
    else:
        has_outargs = bool([x[0] for x in paramflags if x[0] & 2])
    call_with_this.has_outargs = has_outargs
    return call_with_this


def hack(inst, mth, paramflags, interface, mthname):
    if paramflags is None:
        return catch_errors(inst, mth, paramflags, interface, mthname)
    code = mth.__code__
    if code.co_varnames[1:2] == ('this', ):
        return catch_errors(inst, mth, paramflags, interface, mthname)
    dirflags = [f[0] for f in paramflags]
    args_out_idx = []
    args_in_idx = []
    for i, a in enumerate(dirflags):
        if a & 2:
            args_out_idx.append(i)
        if not a & 1:
            if a == 0:
                pass
        args_in_idx.append(i)
    else:
        args_out = len(args_out_idx)
        clsid = getattr(inst, '_reg_clsid_', None)

        def call_without_this--- This code section failed: ---

 L. 143         0  BUILD_LIST_0          0 
                2  STORE_FAST               'inargs'

 L. 144         4  LOAD_DEREF               'args_in_idx'
                6  GET_ITER         
              8_0  COME_FROM            26  '26'
                8  FOR_ITER             28  'to 28'
               10  STORE_FAST               'a'

 L. 145        12  LOAD_FAST                'inargs'
               14  LOAD_METHOD              append
               16  LOAD_FAST                'args'
               18  LOAD_FAST                'a'
               20  BINARY_SUBSCR    
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          
               26  JUMP_BACK             8  'to 8'
             28_0  COME_FROM             8  '8'

 L. 146        28  SETUP_FINALLY       140  'to 140'

 L. 147        30  LOAD_DEREF               'mth'
               32  LOAD_FAST                'inargs'
               34  CALL_FUNCTION_EX      0  'positional arguments only'
               36  STORE_FAST               'result'

 L. 148        38  LOAD_DEREF               'args_out'
               40  LOAD_CONST               1
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_FALSE    64  'to 64'

 L. 149        46  LOAD_FAST                'result'
               48  LOAD_FAST                'args'
               50  LOAD_DEREF               'args_out_idx'
               52  LOAD_CONST               0
               54  BINARY_SUBSCR    
               56  BINARY_SUBSCR    
               58  LOAD_CONST               0
               60  STORE_SUBSCR     
               62  JUMP_FORWARD        134  'to 134'
             64_0  COME_FROM            44  '44'

 L. 150        64  LOAD_DEREF               'args_out'
               66  LOAD_CONST               0
               68  COMPARE_OP               !=
               70  POP_JUMP_IF_FALSE   134  'to 134'

 L. 151        72  LOAD_GLOBAL              len
               74  LOAD_FAST                'result'
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_DEREF               'args_out'
               80  COMPARE_OP               !=
               82  POP_JUMP_IF_FALSE   100  'to 100'

 L. 152        84  LOAD_STR                 'Method should have returned a %s-tuple'
               86  LOAD_DEREF               'args_out'
               88  BINARY_MODULO    
               90  STORE_FAST               'msg'

 L. 153        92  LOAD_GLOBAL              ValueError
               94  LOAD_FAST                'msg'
               96  CALL_FUNCTION_1       1  ''
               98  RAISE_VARARGS_1       1  'exception instance'
            100_0  COME_FROM            82  '82'

 L. 154       100  LOAD_GLOBAL              enumerate
              102  LOAD_FAST                'result'
              104  CALL_FUNCTION_1       1  ''
              106  GET_ITER         
            108_0  COME_FROM           132  '132'
              108  FOR_ITER            134  'to 134'
              110  UNPACK_SEQUENCE_2     2 
              112  STORE_FAST               'i'
              114  STORE_FAST               'value'

 L. 155       116  LOAD_FAST                'value'
              118  LOAD_FAST                'args'
              120  LOAD_DEREF               'args_out_idx'
              122  LOAD_FAST                'i'
              124  BINARY_SUBSCR    
              126  BINARY_SUBSCR    
              128  LOAD_CONST               0
              130  STORE_SUBSCR     
              132  JUMP_BACK           108  'to 108'
            134_0  COME_FROM           108  '108'
            134_1  COME_FROM            70  '70'
            134_2  COME_FROM            62  '62'
              134  POP_BLOCK        
          136_138  JUMP_FORWARD        534  'to 534'
            140_0  COME_FROM_FINALLY    28  '28'

 L. 156       140  DUP_TOP          
              142  LOAD_GLOBAL              ReturnHRESULT
              144  COMPARE_OP               exception-match
              146  POP_JUMP_IF_FALSE   206  'to 206'
              148  POP_TOP          
              150  STORE_FAST               'err'
              152  POP_TOP          
              154  SETUP_FINALLY       192  'to 192'

 L. 157       156  LOAD_FAST                'err'
              158  LOAD_ATTR                args
              160  UNPACK_SEQUENCE_2     2 
              162  STORE_FAST               'hresult'
              164  STORE_FAST               'text'

 L. 158       166  LOAD_GLOBAL              ReportError
              168  LOAD_FAST                'text'
              170  LOAD_DEREF               'interface'
              172  LOAD_ATTR                _iid_
              174  LOAD_DEREF               'clsid'

 L. 159       176  LOAD_FAST                'hresult'

 L. 158       178  LOAD_CONST               ('iid', 'clsid', 'hresult')
              180  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              182  ROT_FOUR         
              184  POP_BLOCK        
              186  POP_EXCEPT       
              188  CALL_FINALLY        192  'to 192'
              190  RETURN_VALUE     
            192_0  COME_FROM           188  '188'
            192_1  COME_FROM_FINALLY   154  '154'
              192  LOAD_CONST               None
              194  STORE_FAST               'err'
              196  DELETE_FAST              'err'
              198  END_FINALLY      
              200  POP_EXCEPT       
          202_204  JUMP_FORWARD        534  'to 534'
            206_0  COME_FROM           146  '146'

 L. 160       206  DUP_TOP          
              208  LOAD_GLOBAL              COMError
              210  COMPARE_OP               exception-match
          212_214  POP_JUMP_IF_FALSE   366  'to 366'
              216  POP_TOP          
              218  STORE_FAST               'err'
              220  POP_TOP          
              222  SETUP_FINALLY       354  'to 354'

 L. 161       224  LOAD_FAST                'err'
              226  LOAD_ATTR                args
              228  UNPACK_SEQUENCE_3     3 
              230  STORE_FAST               'hr'
              232  STORE_FAST               'text'
              234  STORE_FAST               'details'

 L. 162       236  LOAD_GLOBAL              _error
              238  LOAD_STR                 'Exception in %s.%s implementation:'
              240  LOAD_DEREF               'interface'
              242  LOAD_ATTR                __name__

 L. 163       244  LOAD_DEREF               'mthname'

 L. 163       246  LOAD_CONST               True

 L. 162       248  LOAD_CONST               ('exc_info',)
              250  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              252  POP_TOP          

 L. 164       254  SETUP_FINALLY       274  'to 274'

 L. 165       256  LOAD_FAST                'details'
              258  UNPACK_SEQUENCE_5     5 
              260  STORE_FAST               'descr'
              262  STORE_FAST               'source'
              264  STORE_FAST               'helpfile'
              266  STORE_FAST               'helpcontext'
              268  STORE_FAST               'progid'
              270  POP_BLOCK        
              272  JUMP_FORWARD        308  'to 308'
            274_0  COME_FROM_FINALLY   254  '254'

 L. 166       274  DUP_TOP          
              276  LOAD_GLOBAL              ValueError
              278  LOAD_GLOBAL              TypeError
              280  BUILD_TUPLE_2         2 
              282  COMPARE_OP               exception-match
          284_286  POP_JUMP_IF_FALSE   306  'to 306'
              288  POP_TOP          
              290  POP_TOP          
              292  POP_TOP          

 L. 167       294  LOAD_GLOBAL              str
              296  LOAD_FAST                'details'
              298  CALL_FUNCTION_1       1  ''
              300  STORE_FAST               'msg'
              302  POP_EXCEPT       
              304  JUMP_FORWARD        320  'to 320'
            306_0  COME_FROM           284  '284'
              306  END_FINALLY      
            308_0  COME_FROM           272  '272'

 L. 169       308  LOAD_STR                 '%s: %s'
              310  LOAD_FAST                'source'
              312  LOAD_FAST                'descr'
              314  BUILD_TUPLE_2         2 
              316  BINARY_MODULO    
              318  STORE_FAST               'msg'
            320_0  COME_FROM           304  '304'

 L. 170       320  LOAD_GLOBAL              HRESULT_FROM_WIN32
              322  LOAD_FAST                'hr'
              324  CALL_FUNCTION_1       1  ''
              326  STORE_FAST               'hr'

 L. 171       328  LOAD_GLOBAL              ReportError
              330  LOAD_FAST                'msg'
              332  LOAD_DEREF               'interface'
              334  LOAD_ATTR                _iid_
              336  LOAD_DEREF               'clsid'

 L. 172       338  LOAD_FAST                'hr'

 L. 171       340  LOAD_CONST               ('iid', 'clsid', 'hresult')
              342  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              344  ROT_FOUR         
              346  POP_BLOCK        
              348  POP_EXCEPT       
              350  CALL_FINALLY        354  'to 354'
              352  RETURN_VALUE     
            354_0  COME_FROM           350  '350'
            354_1  COME_FROM_FINALLY   222  '222'
              354  LOAD_CONST               None
              356  STORE_FAST               'err'
              358  DELETE_FAST              'err'
              360  END_FINALLY      
              362  POP_EXCEPT       
              364  JUMP_FORWARD        534  'to 534'
            366_0  COME_FROM           212  '212'

 L. 173       366  DUP_TOP          
              368  LOAD_GLOBAL              WindowsError
              370  COMPARE_OP               exception-match
          372_374  POP_JUMP_IF_FALSE   450  'to 450'
              376  POP_TOP          
              378  STORE_FAST               'details'
              380  POP_TOP          
              382  SETUP_FINALLY       438  'to 438'

 L. 174       384  LOAD_GLOBAL              _error
              386  LOAD_STR                 'Exception in %s.%s implementation:'
              388  LOAD_DEREF               'interface'
              390  LOAD_ATTR                __name__

 L. 175       392  LOAD_DEREF               'mthname'

 L. 175       394  LOAD_CONST               True

 L. 174       396  LOAD_CONST               ('exc_info',)
              398  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              400  POP_TOP          

 L. 176       402  LOAD_GLOBAL              HRESULT_FROM_WIN32
              404  LOAD_GLOBAL              winerror
              406  LOAD_FAST                'details'
              408  CALL_FUNCTION_1       1  ''
              410  CALL_FUNCTION_1       1  ''
              412  STORE_FAST               'hr'

 L. 177       414  LOAD_GLOBAL              ReportException
              416  LOAD_FAST                'hr'
              418  LOAD_DEREF               'interface'
              420  LOAD_ATTR                _iid_
              422  LOAD_DEREF               'clsid'
              424  LOAD_CONST               ('clsid',)
              426  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              428  ROT_FOUR         
              430  POP_BLOCK        
              432  POP_EXCEPT       
              434  CALL_FINALLY        438  'to 438'
              436  RETURN_VALUE     
            438_0  COME_FROM           434  '434'
            438_1  COME_FROM_FINALLY   382  '382'
              438  LOAD_CONST               None
              440  STORE_FAST               'details'
              442  DELETE_FAST              'details'
              444  END_FINALLY      
              446  POP_EXCEPT       
              448  JUMP_FORWARD        534  'to 534'
            450_0  COME_FROM           372  '372'

 L. 178       450  DUP_TOP          
              452  LOAD_GLOBAL              E_NotImplemented
              454  COMPARE_OP               exception-match
          456_458  POP_JUMP_IF_FALSE   488  'to 488'
              460  POP_TOP          
              462  POP_TOP          
              464  POP_TOP          

 L. 179       466  LOAD_GLOBAL              _warning
              468  LOAD_STR                 'Unimplemented method %s.%s called'
              470  LOAD_DEREF               'interface'
              472  LOAD_ATTR                __name__

 L. 180       474  LOAD_DEREF               'mthname'

 L. 179       476  CALL_FUNCTION_3       3  ''
              478  POP_TOP          

 L. 181       480  LOAD_GLOBAL              E_NOTIMPL
              482  ROT_FOUR         
              484  POP_EXCEPT       
              486  RETURN_VALUE     
            488_0  COME_FROM           456  '456'

 L. 182       488  POP_TOP          
              490  POP_TOP          
              492  POP_TOP          

 L. 183       494  LOAD_GLOBAL              _error
              496  LOAD_STR                 'Exception in %s.%s implementation:'
              498  LOAD_DEREF               'interface'
              500  LOAD_ATTR                __name__

 L. 184       502  LOAD_DEREF               'mthname'

 L. 184       504  LOAD_CONST               True

 L. 183       506  LOAD_CONST               ('exc_info',)
              508  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              510  POP_TOP          

 L. 185       512  LOAD_GLOBAL              ReportException
              514  LOAD_GLOBAL              E_FAIL
              516  LOAD_DEREF               'interface'
              518  LOAD_ATTR                _iid_
              520  LOAD_DEREF               'clsid'
              522  LOAD_CONST               ('clsid',)
              524  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              526  ROT_FOUR         
              528  POP_EXCEPT       
              530  RETURN_VALUE     
              532  END_FINALLY      
            534_0  COME_FROM           448  '448'
            534_1  COME_FROM           364  '364'
            534_2  COME_FROM           202  '202'
            534_3  COME_FROM           136  '136'

 L. 186       534  LOAD_GLOBAL              S_OK
              536  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 184

        if args_out:
            call_without_this.has_outargs = True
        return call_without_this


class _MethodFinder(object):

    def __init__(self, inst):
        self.inst = inst
        self.names = dict([(n.lower(), n) for n in dir(inst)])

    def get_impl(self, interface, mthname, paramflags, idlflags):
        mth = self.find_impl(interface, mthname, paramflags, idlflags)
        if mth is None:
            return _do_implement(interface.__name__, mthname)
        return hack(self.inst, mth, paramflags, interface, mthname)

    def find_method--- This code section failed: ---

 L. 208         0  SETUP_FINALLY        16  'to 16'

 L. 209         2  LOAD_GLOBAL              getattr
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                inst
                8  LOAD_FAST                'fq_name'
               10  CALL_FUNCTION_2       2  ''
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 210        16  DUP_TOP          
               18  LOAD_GLOBAL              AttributeError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    34  'to 34'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 211        30  POP_EXCEPT       
               32  JUMP_FORWARD         36  'to 36'
             34_0  COME_FROM            22  '22'
               34  END_FINALLY      
             36_0  COME_FROM            32  '32'

 L. 212        36  LOAD_GLOBAL              getattr
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                inst
               42  LOAD_FAST                'mthname'
               44  CALL_FUNCTION_2       2  ''
               46  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 34_0

    def find_impl--- This code section failed: ---

 L. 215         0  LOAD_STR                 '%s_%s'
                2  LOAD_FAST                'interface'
                4  LOAD_ATTR                __name__
                6  LOAD_FAST                'mthname'
                8  BUILD_TUPLE_2         2 
               10  BINARY_MODULO    
               12  STORE_FAST               'fq_name'

 L. 216        14  LOAD_FAST                'interface'
               16  LOAD_ATTR                _case_insensitive_
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 218        20  LOAD_FAST                'self'
               22  LOAD_ATTR                names
               24  LOAD_METHOD              get
               26  LOAD_FAST                'mthname'
               28  LOAD_METHOD              lower
               30  CALL_METHOD_0         0  ''
               32  LOAD_FAST                'mthname'
               34  CALL_METHOD_2         2  ''
               36  STORE_FAST               'mthname'

 L. 220        38  LOAD_FAST                'self'
               40  LOAD_ATTR                names
               42  LOAD_METHOD              get
               44  LOAD_FAST                'fq_name'
               46  LOAD_METHOD              lower
               48  CALL_METHOD_0         0  ''
               50  LOAD_FAST                'fq_name'
               52  CALL_METHOD_2         2  ''
               54  STORE_FAST               'fq_name'
             56_0  COME_FROM            18  '18'

 L. 222        56  SETUP_FINALLY        72  'to 72'

 L. 223        58  LOAD_FAST                'self'
               60  LOAD_METHOD              find_method
               62  LOAD_FAST                'fq_name'
               64  LOAD_FAST                'mthname'
               66  CALL_METHOD_2         2  ''
               68  POP_BLOCK        
               70  RETURN_VALUE     
             72_0  COME_FROM_FINALLY    56  '56'

 L. 224        72  DUP_TOP          
               74  LOAD_GLOBAL              AttributeError
               76  COMPARE_OP               exception-match
               78  POP_JUMP_IF_FALSE    90  'to 90'
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          

 L. 225        86  POP_EXCEPT       
               88  JUMP_FORWARD         92  'to 92'
             90_0  COME_FROM            78  '78'
               90  END_FINALLY      
             92_0  COME_FROM            88  '88'

 L. 226        92  LOAD_FAST                'mthname'
               94  LOAD_CONST               5
               96  LOAD_CONST               None
               98  BUILD_SLICE_2         2 
              100  BINARY_SUBSCR    
              102  STORE_FAST               'propname'

 L. 227       104  LOAD_FAST                'interface'
              106  LOAD_ATTR                _case_insensitive_
              108  POP_JUMP_IF_FALSE   128  'to 128'

 L. 228       110  LOAD_FAST                'self'
              112  LOAD_ATTR                names
              114  LOAD_METHOD              get
              116  LOAD_FAST                'propname'
              118  LOAD_METHOD              lower
              120  CALL_METHOD_0         0  ''
              122  LOAD_FAST                'propname'
              124  CALL_METHOD_2         2  ''
              126  STORE_FAST               'propname'
            128_0  COME_FROM           108  '108'

 L. 233       128  LOAD_STR                 'propget'
              130  LOAD_FAST                'idlflags'
              132  COMPARE_OP               in
              134  POP_JUMP_IF_FALSE   158  'to 158'
              136  LOAD_GLOBAL              len
              138  LOAD_FAST                'paramflags'
              140  CALL_FUNCTION_1       1  ''
              142  LOAD_CONST               1
              144  COMPARE_OP               ==
              146  POP_JUMP_IF_FALSE   158  'to 158'

 L. 234       148  LOAD_FAST                'self'
              150  LOAD_METHOD              getter
              152  LOAD_FAST                'propname'
              154  CALL_METHOD_1         1  ''
              156  RETURN_VALUE     
            158_0  COME_FROM           146  '146'
            158_1  COME_FROM           134  '134'

 L. 235       158  LOAD_STR                 'propput'
              160  LOAD_FAST                'idlflags'
              162  COMPARE_OP               in
              164  POP_JUMP_IF_FALSE   188  'to 188'
              166  LOAD_GLOBAL              len
              168  LOAD_FAST                'paramflags'
              170  CALL_FUNCTION_1       1  ''
              172  LOAD_CONST               1
              174  COMPARE_OP               ==
              176  POP_JUMP_IF_FALSE   188  'to 188'

 L. 236       178  LOAD_FAST                'self'
              180  LOAD_METHOD              setter
              182  LOAD_FAST                'propname'
              184  CALL_METHOD_1         1  ''
              186  RETURN_VALUE     
            188_0  COME_FROM           176  '176'
            188_1  COME_FROM           164  '164'

 L. 237       188  LOAD_GLOBAL              _debug
              190  LOAD_STR                 '%r: %s.%s not implemented'
              192  LOAD_FAST                'self'
              194  LOAD_ATTR                inst
              196  LOAD_FAST                'interface'
              198  LOAD_ATTR                __name__

 L. 238       200  LOAD_FAST                'mthname'

 L. 237       202  CALL_FUNCTION_4       4  ''
              204  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 90_0

    def setter(self, propname):

        def set(self, value):
            try:
                setattr(self, propname, value)
            except AttributeError:
                raise E_NotImplemented()

        return instancemethod(set, self.inst, type(self.inst))

    def getter(self, propname):

        def get(self):
            try:
                return getattr(self, propname)
            except AttributeError:
                raise E_NotImplemented()

        return instancemethod(get, self.inst, type(self.inst))


def _create_vtbl_type(fields, itf):
    try:
        return _vtbl_types[fields]
    except KeyError:

        class Vtbl(Structure):
            _fields_ = fields

        Vtbl.__name__ = 'Vtbl_%s' % itf.__name__
        _vtbl_types[fields] = Vtbl
        return Vtbl


_vtbl_types = {}
try:
    if os.name == 'ce':
        _InterlockedIncrement = windll.coredll.InterlockedIncrement
        _InterlockedDecrement = windll.coredll.InterlockedDecrement
    else:
        _InterlockedIncrement = windll.kernel32.InterlockedIncrement
        _InterlockedDecrement = windll.kernel32.InterlockedDecrement
except AttributeError:
    import threading
    _lock = threading.Lock()
    _acquire = _lock.acquire
    _release = _lock.release

    def _InterlockedIncrement(ob):
        _acquire()
        refcnt = ob.value + 1
        ob.value = refcnt
        _release()
        return refcnt


    def _InterlockedDecrement(ob):
        _acquire()
        refcnt = ob.value - 1
        ob.value = refcnt
        _release()
        return refcnt


else:
    _InterlockedIncrement.argtypes = [
     POINTER(c_long)]
    _InterlockedDecrement.argtypes = [POINTER(c_long)]
    _InterlockedIncrement.restype = c_long
    _InterlockedDecrement.restype = c_long

class LocalServer(object):
    _queue = None

    def run(self, classobjects):
        result = windll.ole32.CoInitialize(None)
        if RPC_E_CHANGED_MODE == result:
            _debug('Server running in MTA')
            self.run_mta()
        else:
            _debug('Server running in STA')
            if result >= 0:
                windll.ole32.CoUninitialize()
            self.run_sta()
        for obj in classobjects:
            obj._revoke_class()

    def run_sta(self):
        from comtypes import messageloop
        messageloop.run()

    def run_mta(self):
        import queue
        self._queue = queue.Queue()
        self._queue.get()

    def Lock(self):
        oledll.ole32.CoAddRefServerProcess()

    def Unlock(self):
        rc = oledll.ole32.CoReleaseServerProcess()
        if rc == 0:
            if self._queue:
                self._queue.put(42)
            else:
                windll.user32.PostQuitMessage(0)


class InprocServer(object):

    def __init__(self):
        self.locks = c_long(0)

    def Lock(self):
        _InterlockedIncrement(self.locks)

    def Unlock(self):
        _InterlockedDecrement(self.locks)

    def DllCanUnloadNow(self):
        if self.locks.value:
            return S_FALSE
        if COMObject._instances_:
            return S_FALSE
        return S_OK


class COMObject(object):
    _instances_ = {}

    def __new__(cls, *args, **kw):
        self = super(COMObject, cls).__new__(cls)
        if isinstance(self, c_void_p):
            return self
        if hasattr(self, '_com_interfaces_'):
            self._COMObject__prepare_comobject()
        return self

    def __prepare_comobject(self):
        self._com_pointers_ = {}
        self._refcnt = c_long(0)
        interfaces = tuple(self._com_interfaces_)
        if ISupportErrorInfo not in interfaces:
            interfaces += (ISupportErrorInfo,)
        if hasattr(self, '_reg_typelib_'):
            from comtypes.typeinfo import LoadRegTypeLib
            self._COMObject__typelib = LoadRegTypeLib(*self._reg_typelib_)
            if hasattr(self, '_reg_clsid_'):
                if IProvideClassInfo not in interfaces:
                    interfaces += (IProvideClassInfo,)
                if hasattr(self, '_outgoing_interfaces_'):
                    if IProvideClassInfo2 not in interfaces:
                        interfaces += (IProvideClassInfo2,)
        if hasattr(self, '_reg_clsid_'):
            if IPersist not in interfaces:
                interfaces += (IPersist,)
        for itf in interfaces[::-1]:
            self._COMObject__make_interface_pointer(itf)

    def __make_interface_pointer(self, itf):
        methods = []
        fields = []
        iids = []
        finder = self._get_method_finder_(itf)
        for interface in itf.__mro__[-2::-1]:
            iids.append(interface._iid_)
            for m in interface._methods_:
                restype, mthname, argtypes, paramflags, idlflags, helptext = m
                proto = WINFUNCTYPE(restype, c_void_p, *argtypes)
                fields.append((mthname, proto))
                mth = finder.get_impl(interface, mthname, paramflags, idlflags)
                methods.append(proto(mth))

        else:
            Vtbl = _create_vtbl_type(tuple(fields), itf)
            vtbl = Vtbl(*methods)
            for iid in iids:
                self._com_pointers_[iid] = pointer(pointer(vtbl))
            else:
                if hasattr(itf, '_disp_methods_'):
                    self._dispimpl_ = {}
                    for m in itf._disp_methods_:
                        what, mthname, idlflags, restype, argspec = m
                        if what == 'DISPMETHOD':
                            if 'propget' in idlflags:
                                invkind = 2
                                mthname = '_get_' + mthname
                            elif 'propput' in idlflags:
                                invkind = 4
                                mthname = '_set_' + mthname
                            elif 'propputref' in idlflags:
                                invkind = 8
                                mthname = '_setref_' + mthname
                            else:
                                invkind = 1
                                if restype:
                                    argspec = argspec + ((['out'], restype, ''),)
                            self._COMObject__make_dispentry(finder, interface, mthname, idlflags, argspec, invkind)
                        else:
                            if what == 'DISPPROPERTY':
                                if restype:
                                    argspec += ((['out'], restype, ''),)
                                else:
                                    self._COMObject__make_dispentry(finder, interface, '_get_' + mthname, idlflags, argspec, 2)
                                if 'readonly' not in idlflags:
                                    self._COMObject__make_dispentry(finder, interface, '_set_' + mthname, idlflags, argspec, 4)

    def __make_dispentry(self, finder, interface, mthname, idlflags, argspec, invkind):
        paramflags = [(_encode_idl(x[0]), x[1]) + tuple(x[3:]) for x in argspec]
        dispid = idlflags[0]
        impl = finder.get_impl(interface, mthname, paramflags, idlflags)
        self._dispimpl_[(dispid, invkind)] = impl
        if invkind in (1, 2):
            self._dispimpl_[(dispid, 3)] = impl

    def _get_method_finder_(self, itf):
        return _MethodFinder(self)

    __server__ = None

    @staticmethod
    def __run_inprocserver__():
        if COMObject.__server__ is None:
            COMObject.__server__ = InprocServer()
        elif isinstance(COMObject.__server__, InprocServer):
            pass
        else:
            raise RuntimeError('Wrong server type')

    @staticmethod
    def __run_localserver__(classobjects):
        assert COMObject.__server__ is None
        server = COMObject.__server__ = LocalServer()
        server.run(classobjects)
        COMObject.__server__ = None

    @staticmethod
    def __keep__(obj):
        COMObject._instances_[obj] = None
        _debug('%d active COM objects: Added   %r', len(COMObject._instances_), obj)
        if COMObject.__server__:
            COMObject.__server__.Lock()

    @staticmethod
    def __unkeep__(obj):
        try:
            del COMObject._instances_[obj]
        except AttributeError:
            _debug('? active COM objects: Removed %r', obj)
        else:
            _debug('%d active COM objects: Removed %r', len(COMObject._instances_), obj)
        _debug('Remaining: %s', list(COMObject._instances_.keys()))
        if COMObject.__server__:
            COMObject.__server__.Unlock()

    def IUnknown_AddRef(self, this, _COMObject__InterlockedIncrement=_InterlockedIncrement, _debug=_debug):
        result = _COMObject__InterlockedIncrement(self._refcnt)
        if result == 1:
            self.__keep__(self)
        _debug('%r.AddRef() -> %s', self, result)
        return result

    def _final_release_(self):
        """This method may be overridden in subclasses
        to free allocated resources or so."""
        pass

    def IUnknown_Release(self, this, _COMObject__InterlockedDecrement=_InterlockedDecrement, _debug=_debug):
        result = _COMObject__InterlockedDecrement(self._refcnt)
        _debug('%r.Release() -> %s', self, result)
        if result == 0:
            self._final_release_()
            self.__unkeep__(self)
            self._com_pointers_ = {}
        return result

    def IUnknown_QueryInterface(self, this, riid, ppvObj, _debug=_debug):
        iid = riid[0]
        ptr = self._com_pointers_.getiidNone
        if ptr is not None:
            _debug('%r.QueryInterface(%s) -> S_OK', self, iid)
            return CopyComPointer(ptr, ppvObj)
        _debug('%r.QueryInterface(%s) -> E_NOINTERFACE', self, iid)
        return E_NOINTERFACE

    def QueryInterface(self, interface):
        """Query the object for an interface pointer"""
        ptr = self._com_pointers_.getinterface._iid_None
        if ptr is None:
            raise COMError(E_NOINTERFACE, FormatError(E_NOINTERFACE), (None, None,
                                                                       0, None, None))
        result = POINTER(interface)()
        CopyComPointer(ptr, byref(result))
        return result

    def ISupportErrorInfo_InterfaceSupportsErrorInfo(self, this, riid):
        if riid[0] in self._com_pointers_:
            return S_OK
        return S_FALSE

    def IProvideClassInfo_GetClassInfo(self):
        try:
            self._COMObject__typelib
        except AttributeError:
            raise WindowsError(E_NOTIMPL)
        else:
            return self._COMObject__typelib.GetTypeInfoOfGuid(self._reg_clsid_)

    def IProvideClassInfo2_GetGUID(self, dwGuidKind):
        if dwGuidKind != 1:
            raise WindowsError(E_INVALIDARG)
        return self._outgoing_interfaces_[0]._iid_

    @property
    def __typeinfo(self):
        iid = self._com_interfaces_[0]._iid_
        return self._COMObject__typelib.GetTypeInfoOfGuid(iid)

    def IDispatch_GetTypeInfoCount(self):
        try:
            self._COMObject__typelib
        except AttributeError:
            return 0
        else:
            return 1

    def IDispatch_GetTypeInfo(self, this, itinfo, lcid, ptinfo):
        if itinfo != 0:
            return DISP_E_BADINDEX
        try:
            ptinfo[0] = self._COMObject__typeinfo
            return S_OK
        except AttributeError:
            return E_NOTIMPL

    def IDispatch_GetIDsOfNames(self, this, riid, rgszNames, cNames, lcid, rgDispId):
        try:
            tinfo = self._COMObject__typeinfo
        except AttributeError:
            return E_NOTIMPL
        else:
            return windll.oleaut32.DispGetIDsOfNames(tinfo, rgszNames, cNames, rgDispId)

    def IDispatch_Invoke--- This code section failed: ---

 L. 694         0  SETUP_FINALLY        12  'to 12'

 L. 695         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _dispimpl_
                6  POP_TOP          
                8  POP_BLOCK        
               10  JUMP_FORWARD        120  'to 120'
             12_0  COME_FROM_FINALLY     0  '0'

 L. 696        12  DUP_TOP          
               14  LOAD_GLOBAL              AttributeError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE   118  'to 118'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 697        26  SETUP_FINALLY        38  'to 38'

 L. 698        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _COMObject__typeinfo
               32  STORE_FAST               'tinfo'
               34  POP_BLOCK        
               36  JUMP_FORWARD         66  'to 66'
             38_0  COME_FROM_FINALLY    26  '26'

 L. 699        38  DUP_TOP          
               40  LOAD_GLOBAL              AttributeError
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE    64  'to 64'
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L. 705        52  LOAD_GLOBAL              DISP_E_MEMBERNOTFOUND
               54  ROT_FOUR         
               56  POP_EXCEPT       
               58  ROT_FOUR         
               60  POP_EXCEPT       
               62  RETURN_VALUE     
             64_0  COME_FROM            44  '44'
               64  END_FINALLY      
             66_0  COME_FROM            36  '36'

 L. 709        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _com_interfaces_
               70  LOAD_CONST               0
               72  BINARY_SUBSCR    
               74  STORE_FAST               'interface'

 L. 710        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _com_pointers_
               80  LOAD_FAST                'interface'
               82  LOAD_ATTR                _iid_
               84  BINARY_SUBSCR    
               86  STORE_FAST               'ptr'

 L. 711        88  LOAD_GLOBAL              windll
               90  LOAD_ATTR                oleaut32
               92  LOAD_METHOD              DispInvoke

 L. 712        94  LOAD_FAST                'ptr'

 L. 712        96  LOAD_FAST                'tinfo'

 L. 712        98  LOAD_FAST                'dispIdMember'

 L. 712       100  LOAD_FAST                'wFlags'

 L. 712       102  LOAD_FAST                'pDispParams'

 L. 712       104  LOAD_FAST                'pVarResult'

 L. 713       106  LOAD_FAST                'pExcepInfo'

 L. 713       108  LOAD_FAST                'puArgErr'

 L. 711       110  CALL_METHOD_8         8  ''
              112  ROT_FOUR         
              114  POP_EXCEPT       
              116  RETURN_VALUE     
            118_0  COME_FROM            18  '18'
              118  END_FINALLY      
            120_0  COME_FROM            10  '10'

 L. 716       120  SETUP_FINALLY       140  'to 140'

 L. 718       122  LOAD_FAST                'self'
              124  LOAD_ATTR                _dispimpl_
              126  LOAD_FAST                'dispIdMember'
              128  LOAD_FAST                'wFlags'
              130  BUILD_TUPLE_2         2 
              132  BINARY_SUBSCR    
              134  STORE_FAST               'mth'
              136  POP_BLOCK        
              138  JUMP_FORWARD        164  'to 164'
            140_0  COME_FROM_FINALLY   120  '120'

 L. 719       140  DUP_TOP          
              142  LOAD_GLOBAL              KeyError
              144  COMPARE_OP               exception-match
              146  POP_JUMP_IF_FALSE   162  'to 162'
              148  POP_TOP          
              150  POP_TOP          
              152  POP_TOP          

 L. 720       154  LOAD_GLOBAL              DISP_E_MEMBERNOTFOUND
              156  ROT_FOUR         
              158  POP_EXCEPT       
              160  RETURN_VALUE     
            162_0  COME_FROM           146  '146'
              162  END_FINALLY      
            164_0  COME_FROM           138  '138'

 L. 732       164  LOAD_FAST                'pDispParams'
              166  LOAD_CONST               0
              168  BINARY_SUBSCR    
              170  STORE_DEREF              'params'

 L. 734       172  LOAD_FAST                'wFlags'
              174  LOAD_CONST               12
              176  BINARY_AND       
              178  POP_JUMP_IF_FALSE   226  'to 226'

 L. 741       180  LOAD_CLOSURE             'params'
              182  BUILD_TUPLE_1         1 
              184  LOAD_LISTCOMP            '<code_object <listcomp>>'
              186  LOAD_STR                 'COMObject.IDispatch_Invoke.<locals>.<listcomp>'
              188  MAKE_FUNCTION_8          'closure'

 L. 742       190  LOAD_GLOBAL              reversed
              192  LOAD_GLOBAL              list
              194  LOAD_GLOBAL              range
              196  LOAD_DEREF               'params'
              198  LOAD_ATTR                cNamedArgs
              200  CALL_FUNCTION_1       1  ''
              202  CALL_FUNCTION_1       1  ''
              204  CALL_FUNCTION_1       1  ''

 L. 741       206  GET_ITER         
              208  CALL_FUNCTION_1       1  ''
              210  STORE_FAST               'args'

 L. 745       212  LOAD_FAST                'mth'
              214  LOAD_FAST                'this'
              216  BUILD_TUPLE_1         1 
              218  LOAD_FAST                'args'
              220  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
              222  CALL_FUNCTION_EX      0  'positional arguments only'
              224  RETURN_VALUE     
            226_0  COME_FROM           178  '178'

 L. 755       226  LOAD_CLOSURE             'params'
              228  BUILD_TUPLE_1         1 
              230  LOAD_LISTCOMP            '<code_object <listcomp>>'
              232  LOAD_STR                 'COMObject.IDispatch_Invoke.<locals>.<listcomp>'
              234  MAKE_FUNCTION_8          'closure'

 L. 756       236  LOAD_GLOBAL              range
              238  LOAD_DEREF               'params'
              240  LOAD_ATTR                cNamedArgs
              242  CALL_FUNCTION_1       1  ''

 L. 755       244  GET_ITER         
              246  CALL_FUNCTION_1       1  ''
              248  STORE_FAST               'named_indexes'

 L. 758       250  LOAD_DEREF               'params'
              252  LOAD_ATTR                cArgs
              254  LOAD_DEREF               'params'
              256  LOAD_ATTR                cNamedArgs
              258  BINARY_SUBTRACT  
              260  STORE_FAST               'num_unnamed'

 L. 759       262  LOAD_GLOBAL              list
              264  LOAD_GLOBAL              reversed
              266  LOAD_GLOBAL              list
              268  LOAD_GLOBAL              range
              270  LOAD_FAST                'num_unnamed'
              272  CALL_FUNCTION_1       1  ''
              274  CALL_FUNCTION_1       1  ''
              276  CALL_FUNCTION_1       1  ''
              278  CALL_FUNCTION_1       1  ''
              280  STORE_FAST               'unnamed_indexes'

 L. 762       282  LOAD_FAST                'named_indexes'
              284  LOAD_FAST                'unnamed_indexes'
              286  BINARY_ADD       
              288  STORE_FAST               'indexes'

 L. 763       290  LOAD_CLOSURE             'params'
              292  BUILD_TUPLE_1         1 
              294  LOAD_LISTCOMP            '<code_object <listcomp>>'
              296  LOAD_STR                 'COMObject.IDispatch_Invoke.<locals>.<listcomp>'
              298  MAKE_FUNCTION_8          'closure'
              300  LOAD_FAST                'indexes'
              302  GET_ITER         
              304  CALL_FUNCTION_1       1  ''
              306  STORE_FAST               'args'

 L. 765       308  LOAD_FAST                'pVarResult'
          310_312  POP_JUMP_IF_FALSE   338  'to 338'
              314  LOAD_GLOBAL              getattr
              316  LOAD_FAST                'mth'
              318  LOAD_STR                 'has_outargs'
              320  LOAD_CONST               False
              322  CALL_FUNCTION_3       3  ''
          324_326  POP_JUMP_IF_FALSE   338  'to 338'

 L. 766       328  LOAD_FAST                'args'
              330  LOAD_METHOD              append
              332  LOAD_FAST                'pVarResult'
              334  CALL_METHOD_1         1  ''
              336  POP_TOP          
            338_0  COME_FROM           324  '324'
            338_1  COME_FROM           310  '310'

 L. 767       338  LOAD_FAST                'mth'
              340  LOAD_FAST                'this'
              342  BUILD_TUPLE_1         1 
              344  LOAD_FAST                'args'
              346  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
              348  CALL_FUNCTION_EX      0  'positional arguments only'
              350  RETURN_VALUE     

Parse error at or near `ROT_FOUR' instruction at offset 58

    def IPersist_GetClassID(self):
        return self._reg_clsid_


__all__ = [
 'COMObject']