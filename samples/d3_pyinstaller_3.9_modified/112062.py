# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: win32com\universal.py
import types, pythoncom
from win32com.client import gencache
com_error = pythoncom.com_error
_univgw = pythoncom._univgw

def RegisterInterfaces--- This code section failed: ---

 L.  12         0  BUILD_LIST_0          0 
                2  STORE_FAST               'ret'

 L.  14         4  SETUP_FINALLY        26  'to 26'

 L.  15         6  LOAD_GLOBAL              gencache
                8  LOAD_METHOD              GetModuleForTypelib
               10  LOAD_FAST                'typelibGUID'
               12  LOAD_FAST                'lcid'
               14  LOAD_FAST                'major'
               16  LOAD_FAST                'minor'
               18  CALL_METHOD_4         4  ''
               20  STORE_FAST               'mod'
               22  POP_BLOCK        
               24  JUMP_FORWARD         48  'to 48'
             26_0  COME_FROM_FINALLY     4  '4'

 L.  16        26  DUP_TOP          
               28  LOAD_GLOBAL              ImportError
               30  <121>                46  ''
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L.  17        38  LOAD_CONST               None
               40  STORE_FAST               'mod'
               42  POP_EXCEPT       
               44  JUMP_FORWARD         48  'to 48'
               46  <48>             
             48_0  COME_FROM            44  '44'
             48_1  COME_FROM            24  '24'

 L.  18        48  LOAD_FAST                'mod'
               50  LOAD_CONST               None
               52  <117>                 0  ''
            54_56  POP_JUMP_IF_FALSE   394  'to 394'

 L.  19        58  LOAD_CONST               0
               60  LOAD_CONST               None
               62  IMPORT_NAME_ATTR         win32com.client.build
               64  STORE_FAST               'win32com'

 L.  21        66  LOAD_GLOBAL              pythoncom
               68  LOAD_METHOD              LoadRegTypeLib
               70  LOAD_FAST                'typelibGUID'
               72  LOAD_FAST                'major'
               74  LOAD_FAST                'minor'
               76  LOAD_FAST                'lcid'
               78  CALL_METHOD_4         4  ''
               80  STORE_FAST               'tlb'

 L.  22        82  LOAD_FAST                'tlb'
               84  LOAD_METHOD              GetTypeComp
               86  CALL_METHOD_0         0  ''
               88  STORE_FAST               'typecomp_lib'

 L.  23        90  LOAD_FAST                'interface_names'
               92  LOAD_CONST               None
               94  <117>                 0  ''
               96  POP_JUMP_IF_FALSE   198  'to 198'

 L.  24        98  BUILD_LIST_0          0 
              100  STORE_FAST               'interface_names'

 L.  25       102  LOAD_GLOBAL              range
              104  LOAD_FAST                'tlb'
              106  LOAD_METHOD              GetTypeInfoCount
              108  CALL_METHOD_0         0  ''
              110  CALL_FUNCTION_1       1  ''
              112  GET_ITER         
            114_0  COME_FROM           196  '196'
            114_1  COME_FROM           180  '180'
            114_2  COME_FROM           168  '168'
              114  FOR_ITER            198  'to 198'
              116  STORE_FAST               'i'

 L.  26       118  LOAD_FAST                'tlb'
              120  LOAD_METHOD              GetTypeInfo
              122  LOAD_FAST                'i'
              124  CALL_METHOD_1         1  ''
              126  STORE_FAST               'info'

 L.  27       128  LOAD_FAST                'tlb'
              130  LOAD_METHOD              GetDocumentation
              132  LOAD_FAST                'i'
              134  CALL_METHOD_1         1  ''
              136  STORE_FAST               'doc'

 L.  28       138  LOAD_FAST                'info'
              140  LOAD_METHOD              GetTypeAttr
              142  CALL_METHOD_0         0  ''
              144  STORE_FAST               'attr'

 L.  29       146  LOAD_FAST                'attr'
              148  LOAD_ATTR                typekind
              150  LOAD_GLOBAL              pythoncom
              152  LOAD_ATTR                TKIND_INTERFACE
              154  COMPARE_OP               ==
              156  POP_JUMP_IF_TRUE    182  'to 182'

 L.  30       158  LOAD_FAST                'attr'
              160  LOAD_ATTR                typekind
              162  LOAD_GLOBAL              pythoncom
              164  LOAD_ATTR                TKIND_DISPATCH
              166  COMPARE_OP               ==

 L.  29       168  POP_JUMP_IF_FALSE_BACK   114  'to 114'

 L.  30       170  LOAD_FAST                'attr'
              172  LOAD_ATTR                wTypeFlags
              174  LOAD_GLOBAL              pythoncom
              176  LOAD_ATTR                TYPEFLAG_FDUAL
              178  BINARY_AND       

 L.  29       180  POP_JUMP_IF_FALSE_BACK   114  'to 114'
            182_0  COME_FROM           156  '156'

 L.  31       182  LOAD_FAST                'interface_names'
              184  LOAD_METHOD              append
              186  LOAD_FAST                'doc'
              188  LOAD_CONST               0
              190  BINARY_SUBSCR    
              192  CALL_METHOD_1         1  ''
              194  POP_TOP          
              196  JUMP_BACK           114  'to 114'
            198_0  COME_FROM           114  '114'
            198_1  COME_FROM            96  '96'

 L.  32       198  LOAD_FAST                'interface_names'
              200  GET_ITER         
            202_0  COME_FROM           390  '390'
              202  FOR_ITER            392  'to 392'
              204  STORE_FAST               'name'

 L.  33       206  LOAD_FAST                'typecomp_lib'
              208  LOAD_METHOD              BindType
              210  LOAD_FAST                'name'
              212  CALL_METHOD_1         1  ''
              214  UNPACK_SEQUENCE_2     2 
              216  STORE_FAST               'type_info'
              218  STORE_FAST               'type_comp'

 L.  36       220  LOAD_FAST                'type_info'
              222  LOAD_CONST               None
              224  <117>                 0  ''
              226  POP_JUMP_IF_FALSE   242  'to 242'

 L.  37       228  LOAD_GLOBAL              ValueError
              230  LOAD_STR                 "The interface '%s' can not be located"
              232  LOAD_FAST                'name'
              234  BUILD_TUPLE_1         1 
              236  BINARY_MODULO    
              238  CALL_FUNCTION_1       1  ''
              240  RAISE_VARARGS_1       1  'exception instance'
            242_0  COME_FROM           226  '226'

 L.  39       242  LOAD_FAST                'type_info'
              244  LOAD_METHOD              GetTypeAttr
              246  CALL_METHOD_0         0  ''
              248  STORE_FAST               'attr'

 L.  40       250  LOAD_FAST                'attr'
              252  LOAD_ATTR                typekind
              254  LOAD_GLOBAL              pythoncom
              256  LOAD_ATTR                TKIND_DISPATCH
              258  COMPARE_OP               ==
          260_262  POP_JUMP_IF_FALSE   292  'to 292'

 L.  41       264  LOAD_FAST                'type_info'
              266  LOAD_METHOD              GetRefTypeOfImplType
              268  LOAD_CONST               -1
              270  CALL_METHOD_1         1  ''
              272  STORE_FAST               'refhtype'

 L.  42       274  LOAD_FAST                'type_info'
              276  LOAD_METHOD              GetRefTypeInfo
              278  LOAD_FAST                'refhtype'
              280  CALL_METHOD_1         1  ''
              282  STORE_FAST               'type_info'

 L.  43       284  LOAD_FAST                'type_info'
              286  LOAD_METHOD              GetTypeAttr
              288  CALL_METHOD_0         0  ''
              290  STORE_FAST               'attr'
            292_0  COME_FROM           260  '260'

 L.  44       292  LOAD_FAST                'win32com'
              294  LOAD_ATTR                client
              296  LOAD_ATTR                build
              298  LOAD_METHOD              VTableItem
              300  LOAD_FAST                'type_info'
              302  LOAD_FAST                'attr'
              304  LOAD_FAST                'type_info'
              306  LOAD_METHOD              GetDocumentation
              308  LOAD_CONST               -1
              310  CALL_METHOD_1         1  ''
              312  CALL_METHOD_3         3  ''
              314  STORE_FAST               'item'

 L.  45       316  LOAD_GLOBAL              _doCreateVTable
              318  LOAD_FAST                'item'
              320  LOAD_ATTR                clsid
              322  LOAD_FAST                'item'
              324  LOAD_ATTR                python_name
              326  LOAD_FAST                'item'
              328  LOAD_ATTR                bIsDispatch
              330  LOAD_FAST                'item'
              332  LOAD_ATTR                vtableFuncs
              334  CALL_FUNCTION_4       4  ''
              336  POP_TOP          

 L.  46       338  LOAD_FAST                'item'
              340  LOAD_ATTR                vtableFuncs
              342  GET_ITER         
            344_0  COME_FROM           386  '386'
              344  FOR_ITER            390  'to 390'
              346  STORE_FAST               'info'

 L.  47       348  LOAD_FAST                'info'
              350  UNPACK_SEQUENCE_3     3 
              352  STORE_FAST               'names'
              354  STORE_FAST               'dispid'
              356  STORE_FAST               'desc'

 L.  48       358  LOAD_FAST                'desc'
              360  LOAD_CONST               4
              362  BINARY_SUBSCR    
              364  STORE_FAST               'invkind'

 L.  49       366  LOAD_FAST                'ret'
              368  LOAD_METHOD              append
              370  LOAD_FAST                'dispid'
              372  LOAD_FAST                'invkind'
              374  LOAD_FAST                'names'
              376  LOAD_CONST               0
              378  BINARY_SUBSCR    
              380  BUILD_TUPLE_3         3 
              382  CALL_METHOD_1         1  ''
              384  POP_TOP          
          386_388  JUMP_BACK           344  'to 344'
            390_0  COME_FROM           344  '344'
              390  JUMP_BACK           202  'to 202'
            392_0  COME_FROM           202  '202'
              392  JUMP_FORWARD        616  'to 616'
            394_0  COME_FROM            54  '54'

 L.  52       394  LOAD_FAST                'interface_names'
          396_398  POP_JUMP_IF_TRUE    414  'to 414'

 L.  53       400  LOAD_GLOBAL              list
              402  LOAD_FAST                'mod'
              404  LOAD_ATTR                VTablesToClassMap
              406  LOAD_METHOD              values
              408  CALL_METHOD_0         0  ''
              410  CALL_FUNCTION_1       1  ''
              412  STORE_FAST               'interface_names'
            414_0  COME_FROM           396  '396'

 L.  54       414  LOAD_FAST                'interface_names'
              416  GET_ITER         
            418_0  COME_FROM           612  '612'
              418  FOR_ITER            616  'to 616'
              420  STORE_FAST               'name'

 L.  55       422  SETUP_FINALLY       438  'to 438'

 L.  56       424  LOAD_FAST                'mod'
              426  LOAD_ATTR                NamesToIIDMap
              428  LOAD_FAST                'name'
              430  BINARY_SUBSCR    
              432  STORE_FAST               'iid'
              434  POP_BLOCK        
              436  JUMP_FORWARD        472  'to 472'
            438_0  COME_FROM_FINALLY   422  '422'

 L.  57       438  DUP_TOP          
              440  LOAD_GLOBAL              KeyError
          442_444  <121>               470  ''
              446  POP_TOP          
              448  POP_TOP          
              450  POP_TOP          

 L.  58       452  LOAD_GLOBAL              ValueError
              454  LOAD_STR                 "Interface '%s' does not exist in this cached typelib"
              456  LOAD_FAST                'name'
              458  BUILD_TUPLE_1         1 
              460  BINARY_MODULO    
              462  CALL_FUNCTION_1       1  ''
              464  RAISE_VARARGS_1       1  'exception instance'
              466  POP_EXCEPT       
              468  JUMP_FORWARD        472  'to 472'
              470  <48>             
            472_0  COME_FROM           468  '468'
            472_1  COME_FROM           436  '436'

 L.  60       472  LOAD_GLOBAL              gencache
              474  LOAD_METHOD              GetModuleForCLSID
              476  LOAD_FAST                'iid'
              478  CALL_METHOD_1         1  ''
              480  STORE_FAST               'sub_mod'

 L.  61       482  LOAD_GLOBAL              getattr
              484  LOAD_FAST                'sub_mod'
              486  LOAD_FAST                'name'
              488  LOAD_STR                 '_vtables_dispatch_'
              490  BINARY_ADD       
              492  LOAD_CONST               None
              494  CALL_FUNCTION_3       3  ''
              496  STORE_FAST               'is_dispatch'

 L.  62       498  LOAD_GLOBAL              getattr
              500  LOAD_FAST                'sub_mod'
              502  LOAD_FAST                'name'
              504  LOAD_STR                 '_vtables_'
              506  BINARY_ADD       
              508  LOAD_CONST               None
              510  CALL_FUNCTION_3       3  ''
              512  STORE_FAST               'method_defs'

 L.  63       514  LOAD_FAST                'is_dispatch'
              516  LOAD_CONST               None
              518  <117>                 0  ''
          520_522  POP_JUMP_IF_TRUE    534  'to 534'
              524  LOAD_FAST                'method_defs'
              526  LOAD_CONST               None
              528  <117>                 0  ''
          530_532  POP_JUMP_IF_FALSE   548  'to 548'
            534_0  COME_FROM           520  '520'

 L.  64       534  LOAD_GLOBAL              ValueError
              536  LOAD_STR                 "Interface '%s' is IDispatch only"
              538  LOAD_FAST                'name'
              540  BUILD_TUPLE_1         1 
              542  BINARY_MODULO    
              544  CALL_FUNCTION_1       1  ''
              546  RAISE_VARARGS_1       1  'exception instance'
            548_0  COME_FROM           530  '530'

 L.  67       548  LOAD_GLOBAL              _doCreateVTable
              550  LOAD_FAST                'iid'
              552  LOAD_FAST                'name'
              554  LOAD_FAST                'is_dispatch'
              556  LOAD_FAST                'method_defs'
              558  CALL_FUNCTION_4       4  ''
              560  POP_TOP          

 L.  68       562  LOAD_FAST                'method_defs'
              564  GET_ITER         
            566_0  COME_FROM           608  '608'
              566  FOR_ITER            612  'to 612'
              568  STORE_FAST               'info'

 L.  69       570  LOAD_FAST                'info'
              572  UNPACK_SEQUENCE_3     3 
              574  STORE_FAST               'names'
              576  STORE_FAST               'dispid'
              578  STORE_FAST               'desc'

 L.  70       580  LOAD_FAST                'desc'
              582  LOAD_CONST               4
              584  BINARY_SUBSCR    
              586  STORE_FAST               'invkind'

 L.  71       588  LOAD_FAST                'ret'
              590  LOAD_METHOD              append
              592  LOAD_FAST                'dispid'
              594  LOAD_FAST                'invkind'
              596  LOAD_FAST                'names'
              598  LOAD_CONST               0
              600  BINARY_SUBSCR    
              602  BUILD_TUPLE_3         3 
              604  CALL_METHOD_1         1  ''
              606  POP_TOP          
          608_610  JUMP_BACK           566  'to 566'
            612_0  COME_FROM           566  '566'
          612_614  JUMP_BACK           418  'to 418'
            616_0  COME_FROM           418  '418'
            616_1  COME_FROM           392  '392'

 L.  72       616  LOAD_FAST                'ret'
              618  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 30


def _doCreateVTable(iid, interface_name, is_dispatch, method_defs):
    defn = Definitioniidis_dispatchmethod_defs
    vtbl = _univgw.CreateVTable(defn, is_dispatch)
    _univgw.RegisterVTablevtbliidinterface_name


def _CalcTypeSize(typeTuple):
    t = typeTuple[0]
    if t & (pythoncom.VT_BYREF | pythoncom.VT_ARRAY):
        cb = _univgw.SizeOfVTpythoncom.VT_PTR[1]
    elif t == pythoncom.VT_RECORD:
        cb = _univgw.SizeOfVTpythoncom.VT_PTR[1]
    else:
        cb = _univgw.SizeOfVTt[1]
    return cb


class Arg:

    def __init__(self, arg_info, name=None):
        self.name = name
        self.vt, self.inOut, self.default, self.clsid = arg_info
        self.size = _CalcTypeSize(arg_info)
        self.offset = 0


class Method:

    def __init__(self, method_info, isEventSink=0):
        all_names, dispid, desc = method_info
        name = all_names[0]
        names = all_names[1:]
        invkind = desc[4]
        arg_defs = desc[2]
        ret_def = desc[8]
        self.dispid = dispid
        self.invkind = invkind
        if isEventSink:
            if name[:2] != 'On':
                name = 'On%s' % name
        self.name = name
        cbArgs = 0
        self.args = []
        for argDesc in arg_defs:
            arg = Arg(argDesc)
            arg.offset = cbArgs
            cbArgs = cbArgs + arg.size
            self.args.appendarg
        else:
            self.cbArgs = cbArgs
            self._gw_in_args = self._GenerateInArgTuple
            self._gw_out_args = self._GenerateOutArgTuple

    def _GenerateInArgTuple(self):
        l = []
        for arg in self.args:
            if not arg.inOut & pythoncom.PARAMFLAG_FIN:
                if arg.inOut == 0:
                    pass
            l.append(arg.vt, arg.offset, arg.size)
        else:
            return tuple(l)

    def _GenerateOutArgTuple(self):
        l = []
        for arg in self.args:
            if not arg.inOut & pythoncom.PARAMFLAG_FOUT:
                if not arg.inOut & pythoncom.PARAMFLAG_FRETVAL:
                    if arg.inOut == 0:
                        pass
            l.append(arg.vt, arg.offset, arg.size, arg.clsid)
        else:
            return tuple(l)


class Definition:

    def __init__(self, iid, is_dispatch, method_defs):
        self._iid = iid
        self._methods = []
        self._is_dispatch = is_dispatch
        for info in method_defs:
            entry = Method(info)
            self._methods.appendentry

    def iid(self):
        return self._iid

    def vtbl_argsizes(self):
        return [m.cbArgs for m in self._methods]

    def vtbl_argcounts(self):
        return [len(m.args) for m in self._methods]

    def dispatch(self, ob, index, argPtr, ReadFromInTuple=_univgw.ReadFromInTuple, WriteFromOutTuple=_univgw.WriteFromOutTuple):
        """Dispatch a call to an interface method."""
        meth = self._methods[index]
        hr = 0
        args = ReadFromInTuple(meth._gw_in_args, argPtr)
        ob = getattrob'policy'ob
        ob._dispid_to_func_[meth.dispid] = meth.name
        retVal = ob._InvokeEx_(meth.dispid, 0, meth.invkind, args, None, None)
        if type(retVal) == tuple:
            if len(retVal) == len(meth._gw_out_args) + 1:
                hr = retVal[0]
                retVal = retVal[1:]
            else:
                raise TypeError('Expected %s return values, got: %s' % (len(meth._gw_out_args) + 1, len(retVal)))
        else:
            retVal = [
             retVal]
            retVal.extend([None] * (len(meth._gw_out_args) - 1))
            retVal = tuple(retVal)
        WriteFromOutTupleretValmeth._gw_out_argsargPtr
        return hr