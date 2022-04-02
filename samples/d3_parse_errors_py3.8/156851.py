# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\comtypes\tools\tlbparser.py
import os, sys
from ctypes import windll
from ctypes import c_void_p
from ctypes import sizeof
from ctypes import alignment
from comtypes import automation
from comtypes import typeinfo
from comtypes import COMError
from comtypes.tools import typedesc
from comtypes.client._code_cache import _get_module_filename
try:
    set
except NameError:
    from sets import Set as set
else:
    is_64bits = sys.maxsize > 4294967296

    def PTR(typ):
        return typedesc.PointerType(typ, sizeof(c_void_p) * 8, alignment(c_void_p) * 8)


    char_type = typedesc.FundamentalType('char', 8, 8)
    uchar_type = typedesc.FundamentalType('unsigned char', 8, 8)
    wchar_t_type = typedesc.FundamentalType('wchar_t', 16, 16)
    short_type = typedesc.FundamentalType('short int', 16, 16)
    ushort_type = typedesc.FundamentalType('short unsigned int', 16, 16)
    int_type = typedesc.FundamentalType('int', 32, 32)
    uint_type = typedesc.FundamentalType('unsigned int', 32, 32)
    long_type = typedesc.FundamentalType('long int', 32, 32)
    ulong_type = typedesc.FundamentalType('long unsigned int', 32, 32)
    longlong_type = typedesc.FundamentalType('long long int', 64, 64)
    ulonglong_type = typedesc.FundamentalType('long long unsigned int', 64, 64)
    float_type = typedesc.FundamentalType('float', 32, 32)
    double_type = typedesc.FundamentalType('double', 64, 64)
    BSTR_type = typedesc.Typedef('BSTR', PTR(wchar_t_type))
    SCODE_type = typedesc.Typedef('SCODE', int_type)
    VARIANT_BOOL_type = typedesc.Typedef('VARIANT_BOOL', short_type)
    HRESULT_type = typedesc.Typedef('HRESULT', ulong_type)
    VARIANT_type = typedesc.Structure('VARIANT', align=(alignment(automation.VARIANT) * 8),
      members=[],
      bases=[],
      size=(sizeof(automation.VARIANT) * 8))
    IDISPATCH_type = typedesc.Typedef('IDispatch', None)
    IUNKNOWN_type = typedesc.Typedef('IUnknown', None)
    DECIMAL_type = typedesc.Structure('DECIMAL', align=(alignment(automation.DECIMAL) * 8),
      members=[],
      bases=[],
      size=(sizeof(automation.DECIMAL) * 8))

    def midlSAFEARRAY(typ):
        return typedesc.SAFEARRAYType(typ)


    CURRENCY_type = longlong_type
    DATE_type = double_type
    COMTYPES = {automation.VT_I2: short_type, 
     automation.VT_I4: int_type, 
     automation.VT_R4: float_type, 
     automation.VT_R8: double_type, 
     automation.VT_CY: CURRENCY_type, 
     automation.VT_DATE: DATE_type, 
     automation.VT_BSTR: BSTR_type, 
     automation.VT_DISPATCH: PTR(IDISPATCH_type), 
     automation.VT_ERROR: SCODE_type, 
     automation.VT_BOOL: VARIANT_BOOL_type, 
     automation.VT_VARIANT: VARIANT_type, 
     automation.VT_UNKNOWN: PTR(IUNKNOWN_type), 
     automation.VT_DECIMAL: DECIMAL_type, 
     automation.VT_I1: char_type, 
     automation.VT_UI1: uchar_type, 
     automation.VT_UI2: ushort_type, 
     automation.VT_UI4: ulong_type, 
     automation.VT_I8: longlong_type, 
     automation.VT_UI8: ulonglong_type, 
     automation.VT_INT: int_type, 
     automation.VT_UINT: uint_type, 
     automation.VT_VOID: typedesc.FundamentalType('void', 0, 0), 
     automation.VT_HRESULT: HRESULT_type, 
     automation.VT_LPSTR: PTR(char_type), 
     automation.VT_LPWSTR: PTR(wchar_t_type)}

    class Parser(object):

        def make_type--- This code section failed: ---

 L. 113         0  SETUP_FINALLY        14  'to 14'

 L. 114         2  LOAD_GLOBAL              COMTYPES
                4  LOAD_FAST                'tdesc'
                6  LOAD_ATTR                vt
                8  BINARY_SUBSCR    
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 115        14  DUP_TOP          
               16  LOAD_GLOBAL              KeyError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    32  'to 32'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 116        28  POP_EXCEPT       
               30  JUMP_FORWARD         34  'to 34'
             32_0  COME_FROM            20  '20'
               32  END_FINALLY      
             34_0  COME_FROM            30  '30'

 L. 118        34  LOAD_FAST                'tdesc'
               36  LOAD_ATTR                vt
               38  LOAD_GLOBAL              automation
               40  LOAD_ATTR                VT_CARRAY
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_FALSE   146  'to 146'

 L. 119        46  LOAD_FAST                'self'
               48  LOAD_METHOD              make_type
               50  LOAD_FAST                'tdesc'
               52  LOAD_ATTR                _
               54  LOAD_ATTR                lpadesc
               56  LOAD_CONST               0
               58  BINARY_SUBSCR    
               60  LOAD_ATTR                tdescElem
               62  LOAD_FAST                'tinfo'
               64  CALL_METHOD_2         2  ''
               66  STORE_FAST               'typ'

 L. 120        68  LOAD_GLOBAL              range
               70  LOAD_FAST                'tdesc'
               72  LOAD_ATTR                _
               74  LOAD_ATTR                lpadesc
               76  LOAD_CONST               0
               78  BINARY_SUBSCR    
               80  LOAD_ATTR                cDims
               82  CALL_FUNCTION_1       1  ''
               84  GET_ITER         
             86_0  COME_FROM           140  '140'
               86  FOR_ITER            142  'to 142'
               88  STORE_FAST               'i'

 L. 121        90  LOAD_GLOBAL              typedesc
               92  LOAD_METHOD              ArrayType
               94  LOAD_FAST                'typ'

 L. 122        96  LOAD_FAST                'tdesc'
               98  LOAD_ATTR                _
              100  LOAD_ATTR                lpadesc
              102  LOAD_CONST               0
              104  BINARY_SUBSCR    
              106  LOAD_ATTR                rgbounds
              108  LOAD_FAST                'i'
              110  BINARY_SUBSCR    
              112  LOAD_ATTR                lLbound

 L. 123       114  LOAD_FAST                'tdesc'
              116  LOAD_ATTR                _
              118  LOAD_ATTR                lpadesc
              120  LOAD_CONST               0
              122  BINARY_SUBSCR    
              124  LOAD_ATTR                rgbounds
              126  LOAD_FAST                'i'
              128  BINARY_SUBSCR    
              130  LOAD_ATTR                cElements
              132  LOAD_CONST               1
              134  BINARY_SUBTRACT  

 L. 121       136  CALL_METHOD_3         3  ''
              138  STORE_FAST               'typ'
              140  JUMP_BACK            86  'to 86'
            142_0  COME_FROM            86  '86'

 L. 124       142  LOAD_FAST                'typ'
              144  RETURN_VALUE     
            146_0  COME_FROM            44  '44'

 L. 126       146  LOAD_FAST                'tdesc'
              148  LOAD_ATTR                vt
              150  LOAD_GLOBAL              automation
              152  LOAD_ATTR                VT_PTR
              154  COMPARE_OP               ==
              156  POP_JUMP_IF_FALSE   186  'to 186'

 L. 127       158  LOAD_FAST                'self'
              160  LOAD_METHOD              make_type
              162  LOAD_FAST                'tdesc'
              164  LOAD_ATTR                _
              166  LOAD_ATTR                lptdesc
              168  LOAD_CONST               0
              170  BINARY_SUBSCR    
              172  LOAD_FAST                'tinfo'
              174  CALL_METHOD_2         2  ''
              176  STORE_FAST               'typ'

 L. 128       178  LOAD_GLOBAL              PTR
              180  LOAD_FAST                'typ'
              182  CALL_FUNCTION_1       1  ''
              184  RETURN_VALUE     
            186_0  COME_FROM           156  '156'

 L. 130       186  LOAD_FAST                'tdesc'
              188  LOAD_ATTR                vt
              190  LOAD_GLOBAL              automation
              192  LOAD_ATTR                VT_USERDEFINED
              194  COMPARE_OP               ==
          196_198  POP_JUMP_IF_FALSE   396  'to 396'

 L. 131       200  SETUP_FINALLY       220  'to 220'

 L. 132       202  LOAD_FAST                'tinfo'
              204  LOAD_METHOD              GetRefTypeInfo
              206  LOAD_FAST                'tdesc'
              208  LOAD_ATTR                _
              210  LOAD_ATTR                hreftype
              212  CALL_METHOD_1         1  ''
              214  STORE_FAST               'ti'
              216  POP_BLOCK        
              218  JUMP_FORWARD        354  'to 354'
            220_0  COME_FROM_FINALLY   200  '200'

 L. 133       220  DUP_TOP          
              222  LOAD_GLOBAL              COMError
              224  COMPARE_OP               exception-match
          226_228  POP_JUMP_IF_FALSE   352  'to 352'
              230  POP_TOP          
              232  STORE_FAST               'details'
              234  POP_TOP          
              236  SETUP_FINALLY       340  'to 340'

 L. 134       238  LOAD_STR                 '__error_hreftype_%d__'
              240  LOAD_FAST                'tdesc'
              242  LOAD_ATTR                _
              244  LOAD_ATTR                hreftype
              246  BINARY_MODULO    
              248  STORE_FAST               'type_name'

 L. 135       250  LOAD_GLOBAL              get_tlib_filename
              252  LOAD_FAST                'self'
              254  LOAD_ATTR                tlib
              256  CALL_FUNCTION_1       1  ''
              258  STORE_FAST               'tlib_name'

 L. 136       260  LOAD_FAST                'tlib_name'
              262  LOAD_CONST               None
              264  COMPARE_OP               is
          266_268  POP_JUMP_IF_FALSE   274  'to 274'

 L. 137       270  LOAD_STR                 'unknown typelib'
              272  STORE_FAST               'tlib_name'
            274_0  COME_FROM           266  '266'

 L. 138       274  LOAD_STR                 "\n\tGetRefTypeInfo failed in %s: %s\n\tgenerating type '%s' instead"

 L. 139       276  LOAD_FAST                'tlib_name'
              278  LOAD_FAST                'details'
              280  LOAD_FAST                'type_name'
              282  BUILD_TUPLE_3         3 

 L. 138       284  BINARY_MODULO    
              286  STORE_FAST               'message'

 L. 140       288  LOAD_CONST               0
              290  LOAD_CONST               None
              292  IMPORT_NAME              warnings
              294  STORE_FAST               'warnings'

 L. 141       296  LOAD_FAST                'warnings'
              298  LOAD_METHOD              warn
              300  LOAD_FAST                'message'
              302  LOAD_GLOBAL              UserWarning
              304  CALL_METHOD_2         2  ''
              306  POP_TOP          

 L. 142       308  LOAD_GLOBAL              typedesc
              310  LOAD_ATTR                Structure
              312  LOAD_FAST                'type_name'

 L. 143       314  LOAD_CONST               8

 L. 144       316  BUILD_LIST_0          0 

 L. 144       318  BUILD_LIST_0          0 

 L. 145       320  LOAD_CONST               0

 L. 142       322  LOAD_CONST               ('align', 'members', 'bases', 'size')
              324  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              326  STORE_FAST               'result'

 L. 146       328  LOAD_FAST                'result'
              330  ROT_FOUR         
              332  POP_BLOCK        
              334  POP_EXCEPT       
              336  CALL_FINALLY        340  'to 340'
              338  RETURN_VALUE     
            340_0  COME_FROM           336  '336'
            340_1  COME_FROM_FINALLY   236  '236'
              340  LOAD_CONST               None
              342  STORE_FAST               'details'
              344  DELETE_FAST              'details'
              346  END_FINALLY      
              348  POP_EXCEPT       
              350  JUMP_FORWARD        354  'to 354'
            352_0  COME_FROM           226  '226'
              352  END_FINALLY      
            354_0  COME_FROM           350  '350'
            354_1  COME_FROM           218  '218'

 L. 147       354  LOAD_FAST                'self'
              356  LOAD_METHOD              parse_typeinfo
              358  LOAD_FAST                'ti'
              360  CALL_METHOD_1         1  ''
              362  STORE_FAST               'result'

 L. 148       364  LOAD_FAST                'result'
              366  LOAD_CONST               None
              368  COMPARE_OP               is-not
          370_372  POP_JUMP_IF_TRUE    392  'to 392'
              374  LOAD_ASSERT              AssertionError
              376  LOAD_FAST                'ti'
              378  LOAD_METHOD              GetDocumentation
              380  LOAD_CONST               -1
              382  CALL_METHOD_1         1  ''
              384  LOAD_CONST               0
              386  BINARY_SUBSCR    
              388  CALL_FUNCTION_1       1  ''
              390  RAISE_VARARGS_1       1  'exception instance'
            392_0  COME_FROM           370  '370'

 L. 149       392  LOAD_FAST                'result'
              394  RETURN_VALUE     
            396_0  COME_FROM           196  '196'

 L. 151       396  LOAD_FAST                'tdesc'
              398  LOAD_ATTR                vt
              400  LOAD_GLOBAL              automation
              402  LOAD_ATTR                VT_SAFEARRAY
              404  COMPARE_OP               ==
          406_408  POP_JUMP_IF_FALSE   438  'to 438'

 L. 153       410  LOAD_FAST                'self'
              412  LOAD_METHOD              make_type
              414  LOAD_FAST                'tdesc'
              416  LOAD_ATTR                _
              418  LOAD_ATTR                lptdesc
              420  LOAD_CONST               0
              422  BINARY_SUBSCR    
              424  LOAD_FAST                'tinfo'
              426  CALL_METHOD_2         2  ''
              428  STORE_FAST               'itemtype'

 L. 154       430  LOAD_GLOBAL              midlSAFEARRAY
              432  LOAD_FAST                'itemtype'
              434  CALL_FUNCTION_1       1  ''
              436  RETURN_VALUE     
            438_0  COME_FROM           406  '406'

 L. 156       438  LOAD_GLOBAL              NotImplementedError
              440  LOAD_FAST                'tdesc'
              442  LOAD_ATTR                vt
              444  CALL_FUNCTION_1       1  ''
              446  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `COME_FROM' instruction at offset 32_0

        def ParseEnum(self, tinfo, ta):
            ta = tinfo.GetTypeAttr()
            enum_name = tinfo.GetDocumentation(-1)[0]
            enum = typedesc.Enumeration(enum_name, 32, 32)
            self._register(enum_name, enum)
            for i in range(ta.cVars):
                vd = tinfo.GetVarDesc(i)
                name = tinfo.GetDocumentation(vd.memid)[0]
                if not vd.varkind == typeinfo.VAR_CONST:
                    raise AssertionError
                else:
                    num_val = vd._.lpvarValue[0].value
                    v = typedesc.EnumValue(name, num_val, enum)
                    enum.add_value(v)
            else:
                return enum

        def ParseRecord(self, tinfo, ta):
            members = []
            struct_name, doc, helpcntext, helpfile = tinfo.GetDocumentation(-1)
            struct = typedesc.Structure(struct_name, align=(ta.cbAlignment * 8),
              members=members,
              bases=[],
              size=(ta.cbSizeInstance * 8))
            self._register(struct_name, struct)
            tlib, _ = tinfo.GetContainingTypeLib()
            tlib_ta = tlib.GetLibAttr()
            if is_64bits:
                if tlib_ta.syskind == typeinfo.SYS_WIN32:
                    struct.size = None
                    struct.align = 64
            if ta.guid:
                struct._recordinfo_ = (
                 str(tlib_ta.guid),
                 tlib_ta.wMajorVerNum, tlib_ta.wMinorVerNum,
                 tlib_ta.lcid,
                 str(ta.guid))
            for i in range(ta.cVars):
                vd = tinfo.GetVarDesc(i)
                name = tinfo.GetDocumentation(vd.memid)[0]
                offset = vd._.oInst * 8
                if not vd.varkind == typeinfo.VAR_PERINSTANCE:
                    raise AssertionError
                else:
                    typ = self.make_type(vd.elemdescVar.tdesc, tinfo)
                    field = typedesc.Field(name, typ, None, offset)
                    members.append(field)
            else:
                return struct

        def ParseModule--- This code section failed: ---

 L. 217         0  LOAD_CONST               0
                2  LOAD_FAST                'ta'
                4  LOAD_ATTR                cImplTypes
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  LOAD_ASSERT              AssertionError
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L. 219        14  LOAD_GLOBAL              range
               16  LOAD_FAST                'ta'
               18  LOAD_ATTR                cFuncs
               20  CALL_FUNCTION_1       1  ''
               22  GET_ITER         
             24_0  COME_FROM           260  '260'
             24_1  COME_FROM            28  '28'
               24  FOR_ITER            262  'to 262'
               26  STORE_FAST               'i'

 L. 222        28  JUMP_BACK            24  'to 24'

 L. 223        30  LOAD_FAST                'tinfo'
               32  LOAD_METHOD              GetFuncDesc
               34  LOAD_FAST                'i'
               36  CALL_METHOD_1         1  ''
               38  STORE_FAST               'fd'

 L. 224        40  LOAD_FAST                'tinfo'
               42  LOAD_METHOD              GetDllEntry
               44  LOAD_FAST                'fd'
               46  LOAD_ATTR                memid
               48  LOAD_FAST                'fd'
               50  LOAD_ATTR                invkind
               52  CALL_METHOD_2         2  ''
               54  UNPACK_SEQUENCE_3     3 
               56  STORE_FAST               'dllname'
               58  STORE_FAST               'func_name'
               60  STORE_FAST               'ordinal'

 L. 225        62  LOAD_FAST                'tinfo'
               64  LOAD_METHOD              GetDocumentation
               66  LOAD_FAST                'fd'
               68  LOAD_ATTR                memid
               70  CALL_METHOD_1         1  ''
               72  LOAD_CONST               1
               74  BINARY_SUBSCR    
               76  STORE_FAST               'func_doc'

 L. 226        78  LOAD_CONST               0
               80  LOAD_FAST                'fd'
               82  LOAD_ATTR                cParamsOpt
               84  COMPARE_OP               ==
               86  POP_JUMP_IF_TRUE     92  'to 92'
               88  LOAD_ASSERT              AssertionError
               90  RAISE_VARARGS_1       1  'exception instance'
             92_0  COME_FROM            86  '86'

 L. 227        92  LOAD_FAST                'self'
               94  LOAD_METHOD              make_type
               96  LOAD_FAST                'fd'
               98  LOAD_ATTR                elemdescFunc
              100  LOAD_ATTR                tdesc
              102  LOAD_FAST                'tinfo'
              104  CALL_METHOD_2         2  ''
              106  STORE_FAST               'returns'

 L. 229       108  LOAD_FAST                'fd'
              110  LOAD_ATTR                callconv
              112  LOAD_GLOBAL              typeinfo
              114  LOAD_ATTR                CC_CDECL
              116  COMPARE_OP               ==
              118  POP_JUMP_IF_FALSE   126  'to 126'

 L. 230       120  LOAD_STR                 '__cdecl__'
              122  STORE_FAST               'attributes'
              124  JUMP_FORWARD        158  'to 158'
            126_0  COME_FROM           118  '118'

 L. 231       126  LOAD_FAST                'fd'
              128  LOAD_ATTR                callconv
              130  LOAD_GLOBAL              typeinfo
              132  LOAD_ATTR                CC_STDCALL
              134  COMPARE_OP               ==
              136  POP_JUMP_IF_FALSE   144  'to 144'

 L. 232       138  LOAD_STR                 '__stdcall__'
              140  STORE_FAST               'attributes'
              142  JUMP_FORWARD        158  'to 158'
            144_0  COME_FROM           136  '136'

 L. 234       144  LOAD_GLOBAL              ValueError
              146  LOAD_STR                 'calling convention %d'
              148  LOAD_FAST                'fd'
              150  LOAD_ATTR                callconv
              152  BINARY_MODULO    
              154  CALL_FUNCTION_1       1  ''
              156  RAISE_VARARGS_1       1  'exception instance'
            158_0  COME_FROM           142  '142'
            158_1  COME_FROM           124  '124'

 L. 236       158  LOAD_GLOBAL              typedesc
              160  LOAD_ATTR                Function
              162  LOAD_FAST                'func_name'
              164  LOAD_FAST                'returns'
              166  LOAD_FAST                'attributes'
              168  LOAD_CONST               1
              170  LOAD_CONST               ('extern',)
              172  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              174  STORE_FAST               'func'

 L. 237       176  LOAD_FAST                'func_doc'
              178  LOAD_CONST               None
              180  COMPARE_OP               is-not
              182  POP_JUMP_IF_FALSE   196  'to 196'

 L. 238       184  LOAD_FAST                'func_doc'
              186  LOAD_METHOD              encode
              188  LOAD_STR                 'mbcs'
              190  CALL_METHOD_1         1  ''
              192  LOAD_FAST                'func'
              194  STORE_ATTR               doc
            196_0  COME_FROM           182  '182'

 L. 239       196  LOAD_FAST                'dllname'
              198  LOAD_FAST                'func'
              200  STORE_ATTR               dllname

 L. 240       202  LOAD_FAST                'self'
              204  LOAD_METHOD              _register
              206  LOAD_FAST                'func_name'
              208  LOAD_FAST                'func'
              210  CALL_METHOD_2         2  ''
              212  POP_TOP          

 L. 241       214  LOAD_GLOBAL              range
              216  LOAD_FAST                'fd'
              218  LOAD_ATTR                cParams
              220  CALL_FUNCTION_1       1  ''
              222  GET_ITER         
            224_0  COME_FROM           258  '258'
              224  FOR_ITER            260  'to 260'
              226  STORE_FAST               'i'

 L. 242       228  LOAD_FAST                'self'
              230  LOAD_METHOD              make_type
              232  LOAD_FAST                'fd'
              234  LOAD_ATTR                lprgelemdescParam
              236  LOAD_FAST                'i'
              238  BINARY_SUBSCR    
              240  LOAD_ATTR                tdesc
              242  LOAD_FAST                'tinfo'
              244  CALL_METHOD_2         2  ''
              246  STORE_FAST               'argtype'

 L. 243       248  LOAD_FAST                'func'
              250  LOAD_METHOD              add_argument
              252  LOAD_FAST                'argtype'
              254  CALL_METHOD_1         1  ''
              256  POP_TOP          
              258  JUMP_BACK           224  'to 224'
            260_0  COME_FROM           224  '224'
              260  JUMP_BACK            24  'to 24'
            262_0  COME_FROM            24  '24'

 L. 246       262  LOAD_GLOBAL              range
              264  LOAD_FAST                'ta'
              266  LOAD_ATTR                cVars
              268  CALL_FUNCTION_1       1  ''
              270  GET_ITER         
            272_0  COME_FROM           400  '400'
            272_1  COME_FROM           390  '390'
              272  FOR_ITER            404  'to 404'
              274  STORE_FAST               'i'

 L. 247       276  LOAD_FAST                'tinfo'
              278  LOAD_METHOD              GetVarDesc
              280  LOAD_FAST                'i'
              282  CALL_METHOD_1         1  ''
              284  STORE_FAST               'vd'

 L. 248       286  LOAD_FAST                'tinfo'
              288  LOAD_METHOD              GetDocumentation
              290  LOAD_FAST                'vd'
              292  LOAD_ATTR                memid
              294  CALL_METHOD_1         1  ''
              296  LOAD_CONST               0
              298  LOAD_CONST               2
              300  BUILD_SLICE_2         2 
              302  BINARY_SUBSCR    
              304  UNPACK_SEQUENCE_2     2 
              306  STORE_FAST               'name'
              308  STORE_FAST               'var_doc'

 L. 249       310  LOAD_FAST                'vd'
              312  LOAD_ATTR                varkind
              314  LOAD_GLOBAL              typeinfo
              316  LOAD_ATTR                VAR_CONST
              318  COMPARE_OP               ==
          320_322  POP_JUMP_IF_TRUE    328  'to 328'
              324  LOAD_ASSERT              AssertionError
              326  RAISE_VARARGS_1       1  'exception instance'
            328_0  COME_FROM           320  '320'

 L. 250       328  LOAD_FAST                'self'
              330  LOAD_METHOD              make_type
              332  LOAD_FAST                'vd'
              334  LOAD_ATTR                elemdescVar
              336  LOAD_ATTR                tdesc
              338  LOAD_FAST                'tinfo'
              340  CALL_METHOD_2         2  ''
              342  STORE_FAST               'typ'

 L. 251       344  LOAD_FAST                'vd'
              346  LOAD_ATTR                _
              348  LOAD_ATTR                lpvarValue
              350  LOAD_CONST               0
              352  BINARY_SUBSCR    
              354  LOAD_ATTR                value
              356  STORE_FAST               'var_value'

 L. 252       358  LOAD_GLOBAL              typedesc
              360  LOAD_METHOD              Constant
              362  LOAD_FAST                'name'
              364  LOAD_FAST                'typ'
              366  LOAD_FAST                'var_value'
              368  CALL_METHOD_3         3  ''
              370  STORE_FAST               'v'

 L. 253       372  LOAD_FAST                'self'
              374  LOAD_METHOD              _register
              376  LOAD_FAST                'name'
              378  LOAD_FAST                'v'
              380  CALL_METHOD_2         2  ''
              382  POP_TOP          

 L. 254       384  LOAD_FAST                'var_doc'
              386  LOAD_CONST               None
              388  COMPARE_OP               is-not
          390_392  POP_JUMP_IF_FALSE_BACK   272  'to 272'

 L. 255       394  LOAD_FAST                'var_doc'
              396  LOAD_FAST                'v'
              398  STORE_ATTR               doc
          400_402  JUMP_BACK           272  'to 272'
            404_0  COME_FROM           272  '272'

Parse error at or near `LOAD_FAST' instruction at offset 30

        def ParseInterface(self, tinfo, ta):
            itf_name, itf_doc = tinfo.GetDocumentation(-1)[0:2]
            assert ta.cImplTypes <= 1
            if ta.cImplTypes == 0:
                if itf_name != 'IUnknown':
                    if itf_name != 'IOleControlTypes':
                        message = 'Ignoring interface %s which has no base interface' % itf_name
                        import warnings
                        warnings.warn(message, UserWarning)
                    return
            itf = typedesc.ComInterface(itf_name, members=[], base=None,
              iid=(str(ta.guid)),
              idlflags=(self.interface_type_flags(ta.wTypeFlags)))
            if itf_doc:
                itf.doc = itf_doc
            self._register(itf_name, itf)
            if ta.cImplTypes:
                hr = tinfo.GetRefTypeOfImplType(0)
                tibase = tinfo.GetRefTypeInfo(hr)
                itf.base = self.parse_typeinfo(tibase)
            assert ta.cVars == 0, 'vars on an Interface?'
            members = []
            for i in range(ta.cFuncs):
                fd = tinfo.GetFuncDesc(i)
                func_name, func_doc = tinfo.GetDocumentation(fd.memid)[:2]
                if not fd.funckind == typeinfo.FUNC_PUREVIRTUAL:
                    raise AssertionError
                else:
                    returns = self.make_type(fd.elemdescFunc.tdesc, tinfo)
                    names = tinfo.GetNames(fd.memid, fd.cParams + 1)
                    names.append('rhs')
                    names = names[:fd.cParams + 1]
                    assert len(names) == fd.cParams + 1
                    flags = self.func_flags(fd.wFuncFlags)
                    flags += self.inv_kind(fd.invkind)
                    mth = typedesc.ComMethod(fd.invkind, fd.memid, func_name, returns, flags, func_doc)
                    mth.oVft = fd.oVft
                    for p in range(fd.cParams):
                        typ = self.make_type(fd.lprgelemdescParam[p].tdesc, tinfo)
                        name = names[(p + 1)]
                        flags = fd.lprgelemdescParam[p]._.paramdesc.wParamFlags
                        if flags & typeinfo.PARAMFLAG_FHASDEFAULT:
                            var = fd.lprgelemdescParam[p]._.paramdesc.pparamdescex[0].varDefaultValue
                            default = var.value
                        else:
                            default = None
                        mth.add_argument(typ, name, self.param_flags(flags), default)
                    else:
                        members.append((fd.oVft, mth))

            else:
                members.sort()
                itf.members.extend([m[1] for m in members])
                return itf

        def ParseDispatch(self, tinfo, ta):
            itf_name, doc = tinfo.GetDocumentation(-1)[0:2]
            assert ta.cImplTypes == 1
            hr = tinfo.GetRefTypeOfImplType(0)
            tibase = tinfo.GetRefTypeInfo(hr)
            base = self.parse_typeinfo(tibase)
            members = []
            itf = typedesc.DispInterface(itf_name, members=members,
              base=base,
              iid=(str(ta.guid)),
              idlflags=(self.interface_type_flags(ta.wTypeFlags)))
            if doc is not None:
                itf.doc = str(doc.split('\x00')[0])
            self._register(itf_name, itf)
            assert ta.wTypeFlags & typeinfo.TYPEFLAG_FDUAL == 0
            for i in range(ta.cVars):
                vd = tinfo.GetVarDesc(i)
                if not vd.varkind == typeinfo.VAR_DISPATCH:
                    raise AssertionError
                else:
                    var_name, var_doc = tinfo.GetDocumentation(vd.memid)[0:2]
                    typ = self.make_type(vd.elemdescVar.tdesc, tinfo)
                    mth = typedesc.DispProperty(vd.memid, var_name, typ, self.var_flags(vd.wVarFlags), var_doc)
                    itf.members.append(mth)
            else:
                ignored_names = set(['QueryInterface', 'AddRef', 'Release',
                 'GetTypeInfoCount', 'GetTypeInfo',
                 'GetIDsOfNames', 'Invoke'])
                for i in range(ta.cFuncs):
                    fd = tinfo.GetFuncDesc(i)
                    func_name, func_doc = tinfo.GetDocumentation(fd.memid)[:2]
                    if func_name in ignored_names:
                        pass
                    else:
                        assert fd.funckind == typeinfo.FUNC_DISPATCH
                        returns = self.make_type(fd.elemdescFunc.tdesc, tinfo)
                        names = tinfo.GetNames(fd.memid, fd.cParams + 1)
                        names.append('rhs')
                        names = names[:fd.cParams + 1]
                        assert len(names) == fd.cParams + 1
                        flags = self.func_flags(fd.wFuncFlags)
                        flags += self.inv_kind(fd.invkind)
                        mth = typedesc.DispMethod(fd.memid, fd.invkind, func_name, returns, flags, func_doc)
                        for p in range(fd.cParams):
                            typ = self.make_type(fd.lprgelemdescParam[p].tdesc, tinfo)
                            name = names[(p + 1)]
                            flags = fd.lprgelemdescParam[p]._.paramdesc.wParamFlags
                            if flags & typeinfo.PARAMFLAG_FHASDEFAULT:
                                var = fd.lprgelemdescParam[p]._.paramdesc.pparamdescex[0].varDefaultValue
                                default = var.value
                            else:
                                default = None
                            mth.add_argument(typ, name, self.param_flags(flags), default)
                        else:
                            itf.members.append(mth)

                else:
                    return itf

        def inv_kind(self, invkind):
            NAMES = {automation.DISPATCH_METHOD: [], 
             automation.DISPATCH_PROPERTYPUT: ['propput'], 
             automation.DISPATCH_PROPERTYPUTREF: ['propputref'], 
             automation.DISPATCH_PROPERTYGET: ['propget']}
            return NAMES[invkind]

        def func_flags(self, flags):
            NAMES = {typeinfo.FUNCFLAG_FRESTRICTED: 'restricted', 
             typeinfo.FUNCFLAG_FSOURCE: 'source', 
             typeinfo.FUNCFLAG_FBINDABLE: 'bindable', 
             typeinfo.FUNCFLAG_FREQUESTEDIT: 'requestedit', 
             typeinfo.FUNCFLAG_FDISPLAYBIND: 'displaybind', 
             typeinfo.FUNCFLAG_FDEFAULTBIND: 'defaultbind', 
             typeinfo.FUNCFLAG_FHIDDEN: 'hidden', 
             typeinfo.FUNCFLAG_FUSESGETLASTERROR: 'usesgetlasterror', 
             typeinfo.FUNCFLAG_FDEFAULTCOLLELEM: 'defaultcollelem', 
             typeinfo.FUNCFLAG_FUIDEFAULT: 'uidefault', 
             typeinfo.FUNCFLAG_FNONBROWSABLE: 'nonbrowsable', 
             typeinfo.FUNCFLAG_FIMMEDIATEBIND: 'immediatebind'}
            return [NAMES[bit] for bit in NAMES if bit & flags]

        def param_flags(self, flags):
            NAMES = {typeinfo.PARAMFLAG_FIN: 'in', 
             typeinfo.PARAMFLAG_FOUT: 'out', 
             typeinfo.PARAMFLAG_FLCID: 'lcid', 
             typeinfo.PARAMFLAG_FRETVAL: 'retval', 
             typeinfo.PARAMFLAG_FOPT: 'optional'}
            return [NAMES[bit] for bit in NAMES if bit & flags]

        def coclass_type_flags(self, flags):
            NAMES = {typeinfo.TYPEFLAG_FAPPOBJECT: 'appobject', 
             typeinfo.TYPEFLAG_FLICENSED: 'licensed', 
             typeinfo.TYPEFLAG_FHIDDEN: 'hidden', 
             typeinfo.TYPEFLAG_FCONTROL: 'control', 
             typeinfo.TYPEFLAG_FDUAL: 'dual', 
             typeinfo.TYPEFLAG_FNONEXTENSIBLE: 'nonextensible', 
             typeinfo.TYPEFLAG_FOLEAUTOMATION: 'oleautomation', 
             typeinfo.TYPEFLAG_FRESTRICTED: 'restricted', 
             typeinfo.TYPEFLAG_FAGGREGATABLE: 'aggregatable', 
             typeinfo.TYPEFLAG_FREVERSEBIND: 'reversebind', 
             typeinfo.TYPEFLAG_FPROXY: 'proxy'}
            NEGATIVE_NAMES = {typeinfo.TYPEFLAG_FCANCREATE: 'noncreatable'}
            return [NAMES[bit] for bit in NAMES if bit & flags] + [NEGATIVE_NAMES[bit] for bit in NEGATIVE_NAMES if not bit & flags]

        def interface_type_flags(self, flags):
            NAMES = {typeinfo.TYPEFLAG_FAPPOBJECT: 'appobject', 
             typeinfo.TYPEFLAG_FLICENSED: 'licensed', 
             typeinfo.TYPEFLAG_FHIDDEN: 'hidden', 
             typeinfo.TYPEFLAG_FCONTROL: 'control', 
             typeinfo.TYPEFLAG_FDUAL: 'dual', 
             typeinfo.TYPEFLAG_FNONEXTENSIBLE: 'nonextensible', 
             typeinfo.TYPEFLAG_FOLEAUTOMATION: 'oleautomation', 
             typeinfo.TYPEFLAG_FRESTRICTED: 'restricted', 
             typeinfo.TYPEFLAG_FAGGREGATABLE: 'aggregatable', 
             typeinfo.TYPEFLAG_FREVERSEBIND: 'reversebind', 
             typeinfo.TYPEFLAG_FPROXY: 'proxy'}
            NEGATIVE_NAMES = {}
            return [NAMES[bit] for bit in NAMES if bit & flags] + [NEGATIVE_NAMES[bit] for bit in NEGATIVE_NAMES if not bit & flags]

        def var_flags(self, flags):
            NAMES = {typeinfo.VARFLAG_FREADONLY: 'readonly', 
             typeinfo.VARFLAG_FSOURCE: 'source', 
             typeinfo.VARFLAG_FBINDABLE: 'bindable', 
             typeinfo.VARFLAG_FREQUESTEDIT: 'requestedit', 
             typeinfo.VARFLAG_FDISPLAYBIND: 'displaybind', 
             typeinfo.VARFLAG_FDEFAULTBIND: 'defaultbind', 
             typeinfo.VARFLAG_FHIDDEN: 'hidden', 
             typeinfo.VARFLAG_FRESTRICTED: 'restricted', 
             typeinfo.VARFLAG_FDEFAULTCOLLELEM: 'defaultcollelem', 
             typeinfo.VARFLAG_FUIDEFAULT: 'uidefault', 
             typeinfo.VARFLAG_FNONBROWSABLE: 'nonbrowsable', 
             typeinfo.VARFLAG_FREPLACEABLE: 'replaceable', 
             typeinfo.VARFLAG_FIMMEDIATEBIND: 'immediatebind'}
            return [NAMES[bit] for bit in NAMES if bit & flags]

        def ParseCoClass(self, tinfo, ta):
            coclass_name, doc = tinfo.GetDocumentation(-1)[0:2]
            tlibattr = tinfo.GetContainingTypeLib()[0].GetLibAttr()
            coclass = typedesc.CoClass(coclass_name, str(ta.guid), self.coclass_type_flags(ta.wTypeFlags), tlibattr)
            if doc is not None:
                coclass.doc = doc
            self._register(coclass_name, coclass)
            for i in range(ta.cImplTypes):
                hr = tinfo.GetRefTypeOfImplType(i)
                ti = tinfo.GetRefTypeInfo(hr)
                itf = self.parse_typeinfo(ti)
                flags = tinfo.GetImplTypeFlags(i)
                coclass.add_interface(itf, flags)
            else:
                return coclass

        def ParseAlias(self, tinfo, ta):
            name = tinfo.GetDocumentation(-1)[0]
            typ = self.make_type(ta.tdescAlias, tinfo)
            alias = typedesc.Typedef(name, typ)
            self._register(name, alias)
            return alias

        def ParseUnion(self, tinfo, ta):
            union_name, doc, helpcntext, helpfile = tinfo.GetDocumentation(-1)
            members = []
            union = typedesc.Union(union_name, align=(ta.cbAlignment * 8),
              members=members,
              bases=[],
              size=(ta.cbSizeInstance * 8))
            self._register(union_name, union)
            tlib, _ = tinfo.GetContainingTypeLib()
            tlib_ta = tlib.GetLibAttr()
            if is_64bits:
                if tlib_ta.syskind == typeinfo.SYS_WIN32:
                    union.size = None
                    union.align = 64
            for i in range(ta.cVars):
                vd = tinfo.GetVarDesc(i)
                name = tinfo.GetDocumentation(vd.memid)[0]
                offset = vd._.oInst * 8
                if not vd.varkind == typeinfo.VAR_PERINSTANCE:
                    raise AssertionError
                else:
                    typ = self.make_type(vd.elemdescVar.tdesc, tinfo)
                    field = typedesc.Field(name, typ, None, offset)
                    members.append(field)
            else:
                return union

        def _typelib_module(self, tlib=None):
            if tlib is None:
                tlib = self.tlib
            return str(tlib.GetLibAttr())

        def _register(self, name, value, tlib=None):
            modname = self._typelib_module(tlib)
            fullname = '%s.%s' % (modname, name)
            if fullname in self.items:
                if isinstance(value, typedesc.External):
                    return
                raise ValueError("Bug: Multiple registered name '%s': %r" % (name, value))
            self.items[fullname] = value

        def parse_typeinfo--- This code section failed: ---

 L. 573         0  LOAD_FAST                'tinfo'
                2  LOAD_METHOD              GetDocumentation
                4  LOAD_CONST               -1
                6  CALL_METHOD_1         1  ''
                8  LOAD_CONST               0
               10  BINARY_SUBSCR    
               12  STORE_FAST               'name'

 L. 574        14  LOAD_FAST                'self'
               16  LOAD_METHOD              _typelib_module
               18  CALL_METHOD_0         0  ''
               20  STORE_FAST               'modname'

 L. 575        22  SETUP_FINALLY        44  'to 44'

 L. 576        24  LOAD_FAST                'self'
               26  LOAD_ATTR                items
               28  LOAD_STR                 '%s.%s'
               30  LOAD_FAST                'modname'
               32  LOAD_FAST                'name'
               34  BUILD_TUPLE_2         2 
               36  BINARY_MODULO    
               38  BINARY_SUBSCR    
               40  POP_BLOCK        
               42  RETURN_VALUE     
             44_0  COME_FROM_FINALLY    22  '22'

 L. 577        44  DUP_TOP          
               46  LOAD_GLOBAL              KeyError
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE    62  'to 62'
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L. 578        58  POP_EXCEPT       
               60  JUMP_FORWARD         64  'to 64'
             62_0  COME_FROM            50  '50'
               62  END_FINALLY      
             64_0  COME_FROM            60  '60'

 L. 580        64  LOAD_FAST                'tinfo'
               66  LOAD_METHOD              GetContainingTypeLib
               68  CALL_METHOD_0         0  ''
               70  LOAD_CONST               0
               72  BINARY_SUBSCR    
               74  STORE_FAST               'tlib'

 L. 581        76  LOAD_FAST                'tlib'
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                tlib
               82  COMPARE_OP               !=
               84  POP_JUMP_IF_FALSE   164  'to 164'

 L. 582        86  LOAD_FAST                'tinfo'
               88  LOAD_METHOD              GetTypeAttr
               90  CALL_METHOD_0         0  ''
               92  STORE_FAST               'ta'

 L. 583        94  LOAD_FAST                'ta'
               96  LOAD_ATTR                cbSizeInstance
               98  LOAD_CONST               8
              100  BINARY_MULTIPLY  
              102  STORE_FAST               'size'

 L. 584       104  LOAD_FAST                'ta'
              106  LOAD_ATTR                cbAlignment
              108  LOAD_CONST               8
              110  BINARY_MULTIPLY  
              112  STORE_FAST               'align'

 L. 585       114  LOAD_GLOBAL              typedesc
              116  LOAD_METHOD              External
              118  LOAD_FAST                'tlib'

 L. 586       120  LOAD_FAST                'name'

 L. 587       122  LOAD_FAST                'size'

 L. 588       124  LOAD_FAST                'align'

 L. 589       126  LOAD_FAST                'tlib'
              128  LOAD_METHOD              GetDocumentation
              130  LOAD_CONST               -1
              132  CALL_METHOD_1         1  ''
              134  LOAD_CONST               None
              136  LOAD_CONST               2
              138  BUILD_SLICE_2         2 
              140  BINARY_SUBSCR    

 L. 585       142  CALL_METHOD_5         5  ''
              144  STORE_FAST               'typ'

 L. 590       146  LOAD_FAST                'self'
              148  LOAD_METHOD              _register
              150  LOAD_FAST                'name'
              152  LOAD_FAST                'typ'
              154  LOAD_FAST                'tlib'
              156  CALL_METHOD_3         3  ''
              158  POP_TOP          

 L. 591       160  LOAD_FAST                'typ'
              162  RETURN_VALUE     
            164_0  COME_FROM            84  '84'

 L. 593       164  LOAD_FAST                'tinfo'
              166  LOAD_METHOD              GetTypeAttr
              168  CALL_METHOD_0         0  ''
              170  STORE_FAST               'ta'

 L. 594       172  LOAD_FAST                'ta'
              174  LOAD_ATTR                typekind
              176  STORE_FAST               'tkind'

 L. 596       178  LOAD_FAST                'tkind'
              180  LOAD_GLOBAL              typeinfo
              182  LOAD_ATTR                TKIND_ENUM
              184  COMPARE_OP               ==
              186  POP_JUMP_IF_FALSE   200  'to 200'

 L. 597       188  LOAD_FAST                'self'
              190  LOAD_METHOD              ParseEnum
              192  LOAD_FAST                'tinfo'
              194  LOAD_FAST                'ta'
              196  CALL_METHOD_2         2  ''
              198  RETURN_VALUE     
            200_0  COME_FROM           186  '186'

 L. 598       200  LOAD_FAST                'tkind'
              202  LOAD_GLOBAL              typeinfo
              204  LOAD_ATTR                TKIND_RECORD
              206  COMPARE_OP               ==
              208  POP_JUMP_IF_FALSE   222  'to 222'

 L. 599       210  LOAD_FAST                'self'
              212  LOAD_METHOD              ParseRecord
              214  LOAD_FAST                'tinfo'
              216  LOAD_FAST                'ta'
              218  CALL_METHOD_2         2  ''
              220  RETURN_VALUE     
            222_0  COME_FROM           208  '208'

 L. 600       222  LOAD_FAST                'tkind'
              224  LOAD_GLOBAL              typeinfo
              226  LOAD_ATTR                TKIND_MODULE
              228  COMPARE_OP               ==
          230_232  POP_JUMP_IF_FALSE   246  'to 246'

 L. 601       234  LOAD_FAST                'self'
              236  LOAD_METHOD              ParseModule
              238  LOAD_FAST                'tinfo'
              240  LOAD_FAST                'ta'
              242  CALL_METHOD_2         2  ''
              244  RETURN_VALUE     
            246_0  COME_FROM           230  '230'

 L. 602       246  LOAD_FAST                'tkind'
              248  LOAD_GLOBAL              typeinfo
              250  LOAD_ATTR                TKIND_INTERFACE
              252  COMPARE_OP               ==
          254_256  POP_JUMP_IF_FALSE   270  'to 270'

 L. 603       258  LOAD_FAST                'self'
              260  LOAD_METHOD              ParseInterface
              262  LOAD_FAST                'tinfo'
              264  LOAD_FAST                'ta'
              266  CALL_METHOD_2         2  ''
              268  RETURN_VALUE     
            270_0  COME_FROM           254  '254'

 L. 604       270  LOAD_FAST                'tkind'
              272  LOAD_GLOBAL              typeinfo
              274  LOAD_ATTR                TKIND_DISPATCH
              276  COMPARE_OP               ==
          278_280  POP_JUMP_IF_FALSE   380  'to 380'

 L. 605       282  SETUP_FINALLY       298  'to 298'

 L. 608       284  LOAD_FAST                'tinfo'
              286  LOAD_METHOD              GetRefTypeOfImplType
              288  LOAD_CONST               -1
              290  CALL_METHOD_1         1  ''
              292  STORE_FAST               'href'
              294  POP_BLOCK        
              296  JUMP_FORWARD        332  'to 332'
            298_0  COME_FROM_FINALLY   282  '282'

 L. 609       298  DUP_TOP          
              300  LOAD_GLOBAL              COMError
              302  COMPARE_OP               exception-match
          304_306  POP_JUMP_IF_FALSE   330  'to 330'
              308  POP_TOP          
              310  POP_TOP          
              312  POP_TOP          

 L. 611       314  LOAD_FAST                'self'
              316  LOAD_METHOD              ParseDispatch
              318  LOAD_FAST                'tinfo'
              320  LOAD_FAST                'ta'
              322  CALL_METHOD_2         2  ''
              324  ROT_FOUR         
              326  POP_EXCEPT       
              328  RETURN_VALUE     
            330_0  COME_FROM           304  '304'
              330  END_FINALLY      
            332_0  COME_FROM           296  '296'

 L. 612       332  LOAD_FAST                'tinfo'
              334  LOAD_METHOD              GetRefTypeInfo
              336  LOAD_FAST                'href'
              338  CALL_METHOD_1         1  ''
              340  STORE_FAST               'tinfo'

 L. 613       342  LOAD_FAST                'tinfo'
              344  LOAD_METHOD              GetTypeAttr
              346  CALL_METHOD_0         0  ''
              348  STORE_FAST               'ta'

 L. 614       350  LOAD_FAST                'ta'
              352  LOAD_ATTR                typekind
              354  LOAD_GLOBAL              typeinfo
              356  LOAD_ATTR                TKIND_INTERFACE
              358  COMPARE_OP               ==
          360_362  POP_JUMP_IF_TRUE    368  'to 368'
              364  LOAD_ASSERT              AssertionError
              366  RAISE_VARARGS_1       1  'exception instance'
            368_0  COME_FROM           360  '360'

 L. 615       368  LOAD_FAST                'self'
              370  LOAD_METHOD              ParseInterface
              372  LOAD_FAST                'tinfo'
              374  LOAD_FAST                'ta'
              376  CALL_METHOD_2         2  ''
              378  RETURN_VALUE     
            380_0  COME_FROM           278  '278'

 L. 616       380  LOAD_FAST                'tkind'
              382  LOAD_GLOBAL              typeinfo
              384  LOAD_ATTR                TKIND_COCLASS
              386  COMPARE_OP               ==
          388_390  POP_JUMP_IF_FALSE   404  'to 404'

 L. 617       392  LOAD_FAST                'self'
              394  LOAD_METHOD              ParseCoClass
              396  LOAD_FAST                'tinfo'
              398  LOAD_FAST                'ta'
              400  CALL_METHOD_2         2  ''
              402  RETURN_VALUE     
            404_0  COME_FROM           388  '388'

 L. 618       404  LOAD_FAST                'tkind'
              406  LOAD_GLOBAL              typeinfo
              408  LOAD_ATTR                TKIND_ALIAS
              410  COMPARE_OP               ==
          412_414  POP_JUMP_IF_FALSE   428  'to 428'

 L. 619       416  LOAD_FAST                'self'
              418  LOAD_METHOD              ParseAlias
              420  LOAD_FAST                'tinfo'
              422  LOAD_FAST                'ta'
              424  CALL_METHOD_2         2  ''
              426  RETURN_VALUE     
            428_0  COME_FROM           412  '412'

 L. 620       428  LOAD_FAST                'tkind'
              430  LOAD_GLOBAL              typeinfo
              432  LOAD_ATTR                TKIND_UNION
              434  COMPARE_OP               ==
          436_438  POP_JUMP_IF_FALSE   452  'to 452'

 L. 621       440  LOAD_FAST                'self'
              442  LOAD_METHOD              ParseUnion
              444  LOAD_FAST                'tinfo'
              446  LOAD_FAST                'ta'
              448  CALL_METHOD_2         2  ''
              450  RETURN_VALUE     
            452_0  COME_FROM           436  '436'

 L. 623       452  LOAD_GLOBAL              print
              454  LOAD_STR                 'NYI'
              456  LOAD_FAST                'tkind'
              458  CALL_FUNCTION_2       2  ''
              460  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 62_0

        def parse_LibraryDescription(self):
            la = self.tlib.GetLibAttr()
            name, doc = self.tlib.GetDocumentation(-1)[:2]
            desc = typedesc.TypeLib(name, str(la.guid), la.wMajorVerNum, la.wMinorVerNum, doc)
            self._register(None, desc)

        def parse(self):
            self.parse_LibraryDescription()
            for i in range(self.tlib.GetTypeInfoCount()):
                tinfo = self.tlib.GetTypeInfo(i)
                self.parse_typeinfo(tinfo)
            else:
                return self.items


    class TlbFileParser(Parser):
        __doc__ = 'Parses a type library from a file'

        def __init__(self, path):
            self.tlib = typeinfo.LoadTypeLibEx(path)
            self.items = {}


    class TypeLibParser(Parser):

        def __init__(self, tlib):
            self.tlib = tlib
            self.items = {}


    def get_tlib_filename(tlib):
        from ctypes import windll, byref
        from comtypes import BSTR
        la = tlib.GetLibAttr()
        name = BSTR()
        try:
            windll.oleaut32.QueryPathOfRegTypeLib
        except AttributeError:
            return
        else:
            if 0 == windll.oleaut32.QueryPathOfRegTypeLib(byref(la.guid), la.wMajorVerNum, la.wMinorVerNum, 0, byref(name)):
                full_filename = name.value.split('\x00')[0]
                if not os.path.isabs(full_filename):
                    try:
                        dll = windll.LoadLibrary(full_filename)
                        full_filename = _get_module_filename(dll._handle)
                        del dll
                    except OSError:
                        return

                    return full_filename


    def _py2exe_hint():
        import comtypes.persist, comtypes.typeinfo, comtypes.automation


    def generate_module--- This code section failed: ---

 L. 737         0  BUILD_MAP_0           0 
                2  STORE_FAST               'known_symbols'

 L. 738         4  LOAD_CONST               ('comtypes.persist', 'comtypes.typeinfo', 'comtypes.automation', 'comtypes._others', 'comtypes', 'ctypes.wintypes', 'ctypes')
                6  GET_ITER         
              8_0  COME_FROM           116  '116'
              8_1  COME_FROM            50  '50'
                8  FOR_ITER            118  'to 118'
               10  STORE_FAST               'name'

 L. 745        12  SETUP_FINALLY        26  'to 26'

 L. 746        14  LOAD_GLOBAL              __import__
               16  LOAD_FAST                'name'
               18  CALL_FUNCTION_1       1  ''
               20  STORE_FAST               'mod'
               22  POP_BLOCK        
               24  JUMP_FORWARD         60  'to 60'
             26_0  COME_FROM_FINALLY    12  '12'

 L. 747        26  DUP_TOP          
               28  LOAD_GLOBAL              ImportError
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    58  'to 58'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L. 748        40  LOAD_FAST                'name'
               42  LOAD_STR                 'comtypes._others'
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_FALSE    52  'to 52'

 L. 749        48  POP_EXCEPT       
               50  JUMP_BACK             8  'to 8'
             52_0  COME_FROM            46  '46'

 L. 750        52  RAISE_VARARGS_0       0  'reraise'
               54  POP_EXCEPT       
               56  JUMP_FORWARD         60  'to 60'
             58_0  COME_FROM            32  '32'
               58  END_FINALLY      
             60_0  COME_FROM            56  '56'
             60_1  COME_FROM            24  '24'

 L. 751        60  LOAD_FAST                'name'
               62  LOAD_METHOD              split
               64  LOAD_STR                 '.'
               66  CALL_METHOD_1         1  ''
               68  LOAD_CONST               1
               70  LOAD_CONST               None
               72  BUILD_SLICE_2         2 
               74  BINARY_SUBSCR    
               76  GET_ITER         
             78_0  COME_FROM            92  '92'
               78  FOR_ITER             94  'to 94'
               80  STORE_FAST               'submodule'

 L. 752        82  LOAD_GLOBAL              getattr
               84  LOAD_FAST                'mod'
               86  LOAD_FAST                'submodule'
               88  CALL_FUNCTION_2       2  ''
               90  STORE_FAST               'mod'
               92  JUMP_BACK            78  'to 78'
             94_0  COME_FROM            78  '78'

 L. 753        94  LOAD_FAST                'mod'
               96  LOAD_ATTR                __dict__
               98  GET_ITER         
            100_0  COME_FROM           114  '114'
              100  FOR_ITER            116  'to 116'
              102  STORE_FAST               'name'

 L. 754       104  LOAD_FAST                'mod'
              106  LOAD_ATTR                __name__
              108  LOAD_FAST                'known_symbols'
              110  LOAD_FAST                'name'
              112  STORE_SUBSCR     
              114  JUMP_BACK           100  'to 100'
            116_0  COME_FROM           100  '100'
              116  JUMP_BACK             8  'to 8'
            118_0  COME_FROM             8  '8'

 L. 755       118  LOAD_GLOBAL              TypeLibParser
              120  LOAD_FAST                'tlib'
              122  CALL_FUNCTION_1       1  ''
              124  STORE_FAST               'p'

 L. 756       126  LOAD_FAST                'pathname'
              128  LOAD_CONST               None
              130  COMPARE_OP               is
              132  POP_JUMP_IF_FALSE   142  'to 142'

 L. 757       134  LOAD_GLOBAL              get_tlib_filename
              136  LOAD_FAST                'tlib'
              138  CALL_FUNCTION_1       1  ''
              140  STORE_FAST               'pathname'
            142_0  COME_FROM           132  '132'

 L. 758       142  LOAD_FAST                'p'
              144  LOAD_METHOD              parse
              146  CALL_METHOD_0         0  ''
              148  STORE_FAST               'items'

 L. 760       150  LOAD_CONST               1
              152  LOAD_CONST               ('Generator',)
              154  IMPORT_NAME              codegenerator
              156  IMPORT_FROM              Generator
              158  STORE_FAST               'Generator'
              160  POP_TOP          

 L. 762       162  LOAD_FAST                'Generator'
              164  LOAD_FAST                'ofi'

 L. 763       166  LOAD_FAST                'known_symbols'

 L. 762       168  LOAD_CONST               ('known_symbols',)
              170  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              172  STORE_FAST               'gen'

 L. 766       174  LOAD_FAST                'gen'
              176  LOAD_ATTR                generate_code
              178  LOAD_GLOBAL              list
              180  LOAD_FAST                'items'
              182  LOAD_METHOD              values
              184  CALL_METHOD_0         0  ''
              186  CALL_FUNCTION_1       1  ''
              188  LOAD_FAST                'pathname'
              190  LOAD_CONST               ('filename',)
              192  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              194  POP_TOP          

Parse error at or near `JUMP_BACK' instruction at offset 50