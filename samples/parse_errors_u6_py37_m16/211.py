# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.11 (default, Sep  3 2021, 20:46:09) 
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

    return E_FAIL


def _do_implement(interface_name, method_name):

    def _not_implemented(*args):
        _debug('unimplemented method %s_%s called', interface_name, method_name)
        return E_NOTIMPL

    return _not_implemented


def catch_errors(obj, mth, paramflags, interface, mthname):
    clsid = getattr(obj, '_reg_clsid_', None)

    def call_with_this--- This code section failed: ---

 L.  75         0  SETUP_EXCEPT         16  'to 16'

 L.  76         2  LOAD_DEREF               'mth'
                4  LOAD_FAST                'args'
                6  LOAD_FAST                'kw'
                8  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               10  STORE_FAST               'result'
               12  POP_BLOCK        
               14  JUMP_FORWARD        206  'to 206'
             16_0  COME_FROM_EXCEPT      0  '0'

 L.  77        16  DUP_TOP          
               18  LOAD_GLOBAL              ReturnHRESULT
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    72  'to 72'
               24  POP_TOP          
               26  STORE_FAST               'err'
               28  POP_TOP          
               30  SETUP_FINALLY        60  'to 60'

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
               54  LOAD_CONST               ('iid', 'clsid', 'hresult')
               56  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               58  RETURN_VALUE     
             60_0  COME_FROM_FINALLY    30  '30'
               60  LOAD_CONST               None
               62  STORE_FAST               'err'
               64  DELETE_FAST              'err'
               66  END_FINALLY      
               68  POP_EXCEPT       
               70  JUMP_FORWARD        206  'to 206'
             72_0  COME_FROM            22  '22'

 L.  81        72  DUP_TOP          
               74  LOAD_GLOBAL              COMError
               76  LOAD_GLOBAL              WindowsError
               78  BUILD_TUPLE_2         2 
               80  COMPARE_OP               exception-match
               82  POP_JUMP_IF_FALSE   134  'to 134'
               84  POP_TOP          
               86  STORE_FAST               'details'
               88  POP_TOP          
               90  SETUP_FINALLY       122  'to 122'

 L.  82        92  LOAD_GLOBAL              _error
               94  LOAD_STR                 'Exception in %s.%s implementation:'
               96  LOAD_DEREF               'interface'
               98  LOAD_ATTR                __name__

 L.  83       100  LOAD_DEREF               'mthname'
              102  LOAD_CONST               True
              104  LOAD_CONST               ('exc_info',)
              106  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              108  POP_TOP          

 L.  84       110  LOAD_GLOBAL              HRESULT_FROM_WIN32
              112  LOAD_GLOBAL              winerror
              114  LOAD_FAST                'details'
              116  CALL_FUNCTION_1       1  '1 positional argument'
              118  CALL_FUNCTION_1       1  '1 positional argument'
              120  RETURN_VALUE     
            122_0  COME_FROM_FINALLY    90  '90'
              122  LOAD_CONST               None
              124  STORE_FAST               'details'
              126  DELETE_FAST              'details'
              128  END_FINALLY      
              130  POP_EXCEPT       
              132  JUMP_FORWARD        206  'to 206'
            134_0  COME_FROM            82  '82'

 L.  85       134  DUP_TOP          
              136  LOAD_GLOBAL              E_NotImplemented
              138  COMPARE_OP               exception-match
              140  POP_JUMP_IF_FALSE   166  'to 166'
              142  POP_TOP          
              144  POP_TOP          
              146  POP_TOP          

 L.  86       148  LOAD_GLOBAL              _warning
              150  LOAD_STR                 'Unimplemented method %s.%s called'
              152  LOAD_DEREF               'interface'
              154  LOAD_ATTR                __name__

 L.  87       156  LOAD_DEREF               'mthname'
              158  CALL_FUNCTION_3       3  '3 positional arguments'
              160  POP_TOP          

 L.  88       162  LOAD_GLOBAL              E_NOTIMPL
              164  RETURN_VALUE     
            166_0  COME_FROM           140  '140'

 L.  89       166  POP_TOP          
              168  POP_TOP          
              170  POP_TOP          

 L.  90       172  LOAD_GLOBAL              _error
              174  LOAD_STR                 'Exception in %s.%s implementation:'
              176  LOAD_DEREF               'interface'
              178  LOAD_ATTR                __name__

 L.  91       180  LOAD_DEREF               'mthname'
              182  LOAD_CONST               True
              184  LOAD_CONST               ('exc_info',)
              186  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              188  POP_TOP          

 L.  92       190  LOAD_GLOBAL              ReportException
              192  LOAD_GLOBAL              E_FAIL
              194  LOAD_DEREF               'interface'
              196  LOAD_ATTR                _iid_
              198  LOAD_DEREF               'clsid'
              200  LOAD_CONST               ('clsid',)
              202  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              204  RETURN_VALUE     
            206_0  COME_FROM           132  '132'
            206_1  COME_FROM            70  '70'
            206_2  COME_FROM            14  '14'

 L.  93       206  LOAD_FAST                'result'
              208  LOAD_CONST               None
              210  COMPARE_OP               is
              212  POP_JUMP_IF_FALSE   218  'to 218'

 L.  94       214  LOAD_GLOBAL              S_OK
              216  RETURN_VALUE     
            218_0  COME_FROM           212  '212'

 L.  95       218  LOAD_FAST                'result'
              220  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 206

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
        if a & 1 or a == 0:
            args_in_idx.append(i)

    args_out = len(args_out_idx)
    clsid = getattr(inst, '_reg_clsid_', None)

    def call_without_this--- This code section failed: ---

 L. 143         0  BUILD_LIST_0          0 
                2  STORE_FAST               'inargs'

 L. 144         4  SETUP_LOOP           32  'to 32'
                6  LOAD_DEREF               'args_in_idx'
                8  GET_ITER         
               10  FOR_ITER             30  'to 30'
               12  STORE_FAST               'a'

 L. 145        14  LOAD_FAST                'inargs'
               16  LOAD_METHOD              append
               18  LOAD_FAST                'args'
               20  LOAD_FAST                'a'
               22  BINARY_SUBSCR    
               24  CALL_METHOD_1         1  '1 positional argument'
               26  POP_TOP          
               28  JUMP_BACK            10  'to 10'
               30  POP_BLOCK        
             32_0  COME_FROM_LOOP        4  '4'

 L. 146        32  SETUP_EXCEPT        148  'to 148'

 L. 147        34  LOAD_DEREF               'mth'
               36  LOAD_FAST                'inargs'
               38  CALL_FUNCTION_EX      0  'positional arguments only'
               40  STORE_FAST               'result'

 L. 148        42  LOAD_DEREF               'args_out'
               44  LOAD_CONST               1
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE    68  'to 68'

 L. 149        50  LOAD_FAST                'result'
               52  LOAD_FAST                'args'
               54  LOAD_DEREF               'args_out_idx'
               56  LOAD_CONST               0
               58  BINARY_SUBSCR    
               60  BINARY_SUBSCR    
               62  LOAD_CONST               0
               64  STORE_SUBSCR     
               66  JUMP_FORWARD        142  'to 142'
             68_0  COME_FROM            48  '48'

 L. 150        68  LOAD_DEREF               'args_out'
               70  LOAD_CONST               0
               72  COMPARE_OP               !=
               74  POP_JUMP_IF_FALSE   142  'to 142'

 L. 151        76  LOAD_GLOBAL              len
               78  LOAD_FAST                'result'
               80  CALL_FUNCTION_1       1  '1 positional argument'
               82  LOAD_DEREF               'args_out'
               84  COMPARE_OP               !=
               86  POP_JUMP_IF_FALSE   104  'to 104'

 L. 152        88  LOAD_STR                 'Method should have returned a %s-tuple'
               90  LOAD_DEREF               'args_out'
               92  BINARY_MODULO    
               94  STORE_FAST               'msg'

 L. 153        96  LOAD_GLOBAL              ValueError
               98  LOAD_FAST                'msg'
              100  CALL_FUNCTION_1       1  '1 positional argument'
              102  RAISE_VARARGS_1       1  'exception instance'
            104_0  COME_FROM            86  '86'

 L. 154       104  SETUP_LOOP          142  'to 142'
              106  LOAD_GLOBAL              enumerate
              108  LOAD_FAST                'result'
              110  CALL_FUNCTION_1       1  '1 positional argument'
              112  GET_ITER         
              114  FOR_ITER            140  'to 140'
              116  UNPACK_SEQUENCE_2     2 
              118  STORE_FAST               'i'
              120  STORE_FAST               'value'

 L. 155       122  LOAD_FAST                'value'
              124  LOAD_FAST                'args'
              126  LOAD_DEREF               'args_out_idx'
              128  LOAD_FAST                'i'
              130  BINARY_SUBSCR    
              132  BINARY_SUBSCR    
              134  LOAD_CONST               0
              136  STORE_SUBSCR     
              138  JUMP_BACK           114  'to 114'
              140  POP_BLOCK        
            142_0  COME_FROM_LOOP      104  '104'
            142_1  COME_FROM            74  '74'
            142_2  COME_FROM            66  '66'
              142  POP_BLOCK        
          144_146  JUMP_FORWARD        508  'to 508'
            148_0  COME_FROM_EXCEPT     32  '32'

 L. 156       148  DUP_TOP          
              150  LOAD_GLOBAL              ReturnHRESULT
              152  COMPARE_OP               exception-match
              154  POP_JUMP_IF_FALSE   206  'to 206'
              156  POP_TOP          
              158  STORE_FAST               'err'
              160  POP_TOP          
              162  SETUP_FINALLY       192  'to 192'

 L. 157       164  LOAD_FAST                'err'
              166  LOAD_ATTR                args
              168  UNPACK_SEQUENCE_2     2 
              170  STORE_FAST               'hresult'
              172  STORE_FAST               'text'

 L. 158       174  LOAD_GLOBAL              ReportError
              176  LOAD_FAST                'text'
              178  LOAD_DEREF               'interface'
              180  LOAD_ATTR                _iid_
              182  LOAD_DEREF               'clsid'

 L. 159       184  LOAD_FAST                'hresult'
              186  LOAD_CONST               ('iid', 'clsid', 'hresult')
              188  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              190  RETURN_VALUE     
            192_0  COME_FROM_FINALLY   162  '162'
              192  LOAD_CONST               None
              194  STORE_FAST               'err'
              196  DELETE_FAST              'err'
              198  END_FINALLY      
              200  POP_EXCEPT       
          202_204  JUMP_FORWARD        508  'to 508'
            206_0  COME_FROM           154  '154'

 L. 160       206  DUP_TOP          
              208  LOAD_GLOBAL              COMError
              210  COMPARE_OP               exception-match
          212_214  POP_JUMP_IF_FALSE   358  'to 358'
              216  POP_TOP          
              218  STORE_FAST               'err'
              220  POP_TOP          
              222  SETUP_FINALLY       346  'to 346'

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
              246  LOAD_CONST               True
              248  LOAD_CONST               ('exc_info',)
              250  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              252  POP_TOP          

 L. 164       254  SETUP_EXCEPT        274  'to 274'

 L. 165       256  LOAD_FAST                'details'
              258  UNPACK_SEQUENCE_5     5 
              260  STORE_FAST               'descr'
              262  STORE_FAST               'source'
              264  STORE_FAST               'helpfile'
              266  STORE_FAST               'helpcontext'
              268  STORE_FAST               'progid'
              270  POP_BLOCK        
              272  JUMP_FORWARD        308  'to 308'
            274_0  COME_FROM_EXCEPT    254  '254'

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
              298  CALL_FUNCTION_1       1  '1 positional argument'
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
              324  CALL_FUNCTION_1       1  '1 positional argument'
              326  STORE_FAST               'hr'

 L. 171       328  LOAD_GLOBAL              ReportError
              330  LOAD_FAST                'msg'
              332  LOAD_DEREF               'interface'
              334  LOAD_ATTR                _iid_
              336  LOAD_DEREF               'clsid'

 L. 172       338  LOAD_FAST                'hr'
              340  LOAD_CONST               ('iid', 'clsid', 'hresult')
              342  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              344  RETURN_VALUE     
            346_0  COME_FROM_FINALLY   222  '222'
              346  LOAD_CONST               None
              348  STORE_FAST               'err'
              350  DELETE_FAST              'err'
              352  END_FINALLY      
              354  POP_EXCEPT       
              356  JUMP_FORWARD        508  'to 508'
            358_0  COME_FROM           212  '212'

 L. 173       358  DUP_TOP          
              360  LOAD_GLOBAL              WindowsError
              362  COMPARE_OP               exception-match
          364_366  POP_JUMP_IF_FALSE   434  'to 434'
              368  POP_TOP          
              370  STORE_FAST               'details'
              372  POP_TOP          
              374  SETUP_FINALLY       422  'to 422'

 L. 174       376  LOAD_GLOBAL              _error
              378  LOAD_STR                 'Exception in %s.%s implementation:'
              380  LOAD_DEREF               'interface'
              382  LOAD_ATTR                __name__

 L. 175       384  LOAD_DEREF               'mthname'
              386  LOAD_CONST               True
              388  LOAD_CONST               ('exc_info',)
              390  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              392  POP_TOP          

 L. 176       394  LOAD_GLOBAL              HRESULT_FROM_WIN32
              396  LOAD_GLOBAL              winerror
              398  LOAD_FAST                'details'
              400  CALL_FUNCTION_1       1  '1 positional argument'
              402  CALL_FUNCTION_1       1  '1 positional argument'
              404  STORE_FAST               'hr'

 L. 177       406  LOAD_GLOBAL              ReportException
              408  LOAD_FAST                'hr'
              410  LOAD_DEREF               'interface'
              412  LOAD_ATTR                _iid_
              414  LOAD_DEREF               'clsid'
              416  LOAD_CONST               ('clsid',)
              418  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              420  RETURN_VALUE     
            422_0  COME_FROM_FINALLY   374  '374'
              422  LOAD_CONST               None
              424  STORE_FAST               'details'
              426  DELETE_FAST              'details'
              428  END_FINALLY      
              430  POP_EXCEPT       
              432  JUMP_FORWARD        508  'to 508'
            434_0  COME_FROM           364  '364'

 L. 178       434  DUP_TOP          
              436  LOAD_GLOBAL              E_NotImplemented
              438  COMPARE_OP               exception-match
          440_442  POP_JUMP_IF_FALSE   468  'to 468'
              444  POP_TOP          
              446  POP_TOP          
              448  POP_TOP          

 L. 179       450  LOAD_GLOBAL              _warning
              452  LOAD_STR                 'Unimplemented method %s.%s called'
              454  LOAD_DEREF               'interface'
              456  LOAD_ATTR                __name__

 L. 180       458  LOAD_DEREF               'mthname'
              460  CALL_FUNCTION_3       3  '3 positional arguments'
              462  POP_TOP          

 L. 181       464  LOAD_GLOBAL              E_NOTIMPL
              466  RETURN_VALUE     
            468_0  COME_FROM           440  '440'

 L. 182       468  POP_TOP          
              470  POP_TOP          
              472  POP_TOP          

 L. 183       474  LOAD_GLOBAL              _error
              476  LOAD_STR                 'Exception in %s.%s implementation:'
              478  LOAD_DEREF               'interface'
              480  LOAD_ATTR                __name__

 L. 184       482  LOAD_DEREF               'mthname'
              484  LOAD_CONST               True
              486  LOAD_CONST               ('exc_info',)
              488  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              490  POP_TOP          

 L. 185       492  LOAD_GLOBAL              ReportException
              494  LOAD_GLOBAL              E_FAIL
              496  LOAD_DEREF               'interface'
              498  LOAD_ATTR                _iid_
              500  LOAD_DEREF               'clsid'
              502  LOAD_CONST               ('clsid',)
              504  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              506  RETURN_VALUE     
            508_0  COME_FROM           432  '432'
            508_1  COME_FROM           356  '356'
            508_2  COME_FROM           202  '202'
            508_3  COME_FROM           144  '144'

 L. 186       508  LOAD_GLOBAL              S_OK
              510  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_GLOBAL' instruction at offset 508

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

    def find_method(self, fq_name, mthname):
        try:
            return getattr(self.inst, fq_name)
        except AttributeError:
            pass

        return getattr(self.inst, mthname)

    def find_impl(self, interface, mthname, paramflags, idlflags):
        fq_name = '%s_%s' % (interface.__name__, mthname)
        if interface._case_insensitive_:
            mthname = self.names.get(mthname.lower(), mthname)
            fq_name = self.names.get(fq_name.lower(), fq_name)
        try:
            return self.find_method(fq_name, mthname)
        except AttributeError:
            pass

        propname = mthname[5:]
        if interface._case_insensitive_:
            propname = self.names.get(propname.lower(), propname)
        if 'propget' in idlflags:
            if len(paramflags) == 1:
                return self.getter(propname)
        if 'propput' in idlflags:
            if len(paramflags) == 1:
                return self.setter(propname)
        _debug('%r: %s.%s not implemented', self.inst, interface.__name__, mthname)

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

        Vtbl = _create_vtbl_type(tuple(fields), itf)
        vtbl = Vtbl(*methods)
        for iid in iids:
            self._com_pointers_[iid] = pointer(pointer(vtbl))

        if hasattr(itf, '_disp_methods_'):
            self._dispimpl_ = {}
            for m in itf._disp_methods_:
                what, mthname, idlflags, restype, argspec = m
                if what == 'DISPMETHOD':
                    if 'propget' in idlflags:
                        invkind = 2
                        mthname = '_get_' + mthname
                    else:
                        if 'propput' in idlflags:
                            invkind = 4
                            mthname = '_set_' + mthname
                        else:
                            if 'propputref' in idlflags:
                                invkind = 8
                                mthname = '_setref_' + mthname
                            else:
                                invkind = 1
                                if restype:
                                    argspec = argspec + ((['out'], restype, ''),)
                                self._COMObject__make_dispentry(finder, interface, mthname, idlflags, argspec, invkind)
                elif what == 'DISPPROPERTY':
                    if restype:
                        argspec += ((['out'], restype, ''),)
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
        else:
            if isinstance(COMObject.__server__, InprocServer):
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
        ptr = self._com_pointers_.get(iid, None)
        if ptr is not None:
            _debug('%r.QueryInterface(%s) -> S_OK', self, iid)
            return CopyComPointer(ptr, ppvObj)
        _debug('%r.QueryInterface(%s) -> E_NOINTERFACE', self, iid)
        return E_NOINTERFACE

    def QueryInterface(self, interface):
        """Query the object for an interface pointer"""
        ptr = self._com_pointers_.get(interface._iid_, None)
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

    def IDispatch_Invoke(self, this, dispIdMember, riid, lcid, wFlags, pDispParams, pVarResult, pExcepInfo, puArgErr):
        try:
            self._dispimpl_
        except AttributeError:
            try:
                tinfo = self._COMObject__typeinfo
            except AttributeError:
                return DISP_E_MEMBERNOTFOUND
            else:
                interface = self._com_interfaces_[0]
                ptr = self._com_pointers_[interface._iid_]
            return windll.oleaut32.DispInvoke(ptr, tinfo, dispIdMember, wFlags, pDispParams, pVarResult, pExcepInfo, puArgErr)
        else:
            try:
                mth = self._dispimpl_[(dispIdMember, wFlags)]
            except KeyError:
                return DISP_E_MEMBERNOTFOUND
            else:
                params = pDispParams[0]
                if wFlags & 12:
                    args = [params.rgvarg[i].value for i in reversed(list(range(params.cNamedArgs)))]
                    return mth(this, *args)
                named_indexes = [params.rgdispidNamedArgs[i] for i in range(params.cNamedArgs)]
                num_unnamed = params.cArgs - params.cNamedArgs
                unnamed_indexes = list(reversed(list(range(num_unnamed))))
                indexes = named_indexes + unnamed_indexes
                args = [params.rgvarg[i].value for i in indexes]
                if pVarResult:
                    if getattr(mth, 'has_outargs', False):
                        args.append(pVarResult)
                return mth(this, *args)

    def IPersist_GetClassID(self):
        return self._reg_clsid_


__all__ = [
 'COMObject']