# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: win32com\client\dynamic.py
"""Support for dynamic COM client support.

Introduction
 Dynamic COM client support is the ability to use a COM server without
 prior knowledge of the server.  This can be used to talk to almost all
 COM servers, including much of MS Office.

 In general, you should not use this module directly - see below.

Example
 >>> import win32com.client
 >>> xl = win32com.client.Dispatch("Excel.Application")
 # The line above invokes the functionality of this class.
 # xl is now an object we can use to talk to Excel.
 >>> xl.Visible = 1 # The Excel window becomes visible.

"""
import sys, traceback, types, pythoncom, winerror
from . import build
from pywintypes import IIDType
import win32com.client
debugging = 0
debugging_attr = 0
LCID = 0
ERRORS_BAD_CONTEXT = [
 winerror.DISP_E_MEMBERNOTFOUND,
 winerror.DISP_E_BADPARAMCOUNT,
 winerror.DISP_E_PARAMNOTOPTIONAL,
 winerror.DISP_E_TYPEMISMATCH,
 winerror.E_INVALIDARG]
ALL_INVOKE_TYPES = [
 pythoncom.INVOKE_PROPERTYGET,
 pythoncom.INVOKE_PROPERTYPUT,
 pythoncom.INVOKE_PROPERTYPUTREF,
 pythoncom.INVOKE_FUNC]

def debug_print(*args):
    if debugging:
        for arg in args:
            print(arg, end=' ')
        else:
            print()


def debug_attr_print(*args):
    if debugging_attr:
        for arg in args:
            print(arg, end=' ')
        else:
            print()


def MakeMethod(func, inst, cls):
    return types.MethodType(func, inst)


PyIDispatchType = pythoncom.TypeIIDs[pythoncom.IID_IDispatch]
PyIUnknownType = pythoncom.TypeIIDs[pythoncom.IID_IUnknown]
_GoodDispatchTypes = (
 str, IIDType)
_defaultDispatchItem = build.DispatchItem

def _GetGoodDispatch--- This code section failed: ---

 L.  77         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'IDispatch'
                4  LOAD_GLOBAL              PyIDispatchType
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L.  78        10  LOAD_FAST                'IDispatch'
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L.  79        14  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'IDispatch'
               18  LOAD_GLOBAL              _GoodDispatchTypes
               20  CALL_FUNCTION_2       2  ''
               22  POP_JUMP_IF_FALSE    80  'to 80'

 L.  80        24  SETUP_FINALLY        40  'to 40'

 L.  81        26  LOAD_GLOBAL              pythoncom
               28  LOAD_METHOD              connect
               30  LOAD_FAST                'IDispatch'
               32  CALL_METHOD_1         1  ''
               34  STORE_FAST               'IDispatch'
               36  POP_BLOCK        
               38  JUMP_ABSOLUTE        92  'to 92'
             40_0  COME_FROM_FINALLY    24  '24'

 L.  82        40  DUP_TOP          
               42  LOAD_GLOBAL              pythoncom
               44  LOAD_ATTR                ole_error
               46  <121>                76  ''
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L.  83        54  LOAD_GLOBAL              pythoncom
               56  LOAD_METHOD              CoCreateInstance
               58  LOAD_FAST                'IDispatch'
               60  LOAD_CONST               None
               62  LOAD_FAST                'clsctx'
               64  LOAD_GLOBAL              pythoncom
               66  LOAD_ATTR                IID_IDispatch
               68  CALL_METHOD_4         4  ''
               70  STORE_FAST               'IDispatch'
               72  POP_EXCEPT       
               74  JUMP_ABSOLUTE        92  'to 92'
               76  <48>             
               78  JUMP_FORWARD         92  'to 92'
             80_0  COME_FROM            22  '22'

 L.  86        80  LOAD_GLOBAL              getattr
               82  LOAD_FAST                'IDispatch'
               84  LOAD_STR                 '_oleobj_'
               86  LOAD_FAST                'IDispatch'
               88  CALL_FUNCTION_3       3  ''
               90  STORE_FAST               'IDispatch'
             92_0  COME_FROM_EXCEPT_CLAUSE    78  '78'
             92_1  COME_FROM_EXCEPT_CLAUSE    74  '74'

 L.  87        92  LOAD_FAST                'IDispatch'
               94  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 46


def _GetGoodDispatchAndUserName--- This code section failed: ---

 L.  92         0  LOAD_FAST                'userName'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    24  'to 24'

 L.  93         8  LOAD_GLOBAL              isinstance
               10  LOAD_FAST                'IDispatch'
               12  LOAD_GLOBAL              str
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_FALSE    32  'to 32'

 L.  94        18  LOAD_FAST                'IDispatch'
               20  STORE_FAST               'userName'
               22  JUMP_FORWARD         32  'to 32'
             24_0  COME_FROM             6  '6'

 L.  97        24  LOAD_GLOBAL              str
               26  LOAD_FAST                'userName'
               28  CALL_FUNCTION_1       1  ''
               30  STORE_FAST               'userName'
             32_0  COME_FROM            22  '22'
             32_1  COME_FROM            16  '16'

 L.  98        32  LOAD_GLOBAL              _GetGoodDispatch
               34  LOAD_FAST                'IDispatch'
               36  LOAD_FAST                'clsctx'
               38  CALL_FUNCTION_2       2  ''
               40  LOAD_FAST                'userName'
               42  BUILD_TUPLE_2         2 
               44  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _GetDescInvokeType(entry, invoke_type):
    return entry and entry.desc or invoke_type
    varkind = entry.desc[4]
    if varkind == pythoncom.VAR_DISPATCH:
        if invoke_type == pythoncom.INVOKE_PROPERTYGET:
            return pythoncom.INVOKE_FUNC | invoke_type
    return varkind


def Dispatch--- This code section failed: ---

 L. 110         0  LOAD_FAST                'UnicodeToString'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  <74>             
               10  LOAD_STR                 'this is deprecated and will go away'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 111        16  LOAD_GLOBAL              _GetGoodDispatchAndUserName
               18  LOAD_FAST                'IDispatch'
               20  LOAD_FAST                'userName'
               22  LOAD_FAST                'clsctx'
               24  CALL_FUNCTION_3       3  ''
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'IDispatch'
               30  STORE_FAST               'userName'

 L. 112        32  LOAD_FAST                'createClass'
               34  LOAD_CONST               None
               36  <117>                 0  ''
               38  POP_JUMP_IF_FALSE    44  'to 44'

 L. 113        40  LOAD_GLOBAL              CDispatch
               42  STORE_FAST               'createClass'
             44_0  COME_FROM            38  '38'

 L. 114        44  LOAD_CONST               None
               46  STORE_FAST               'lazydata'

 L. 115        48  SETUP_FINALLY       120  'to 120'

 L. 116        50  LOAD_FAST                'typeinfo'
               52  LOAD_CONST               None
               54  <117>                 0  ''
               56  POP_JUMP_IF_FALSE    66  'to 66'

 L. 117        58  LOAD_FAST                'IDispatch'
               60  LOAD_METHOD              GetTypeInfo
               62  CALL_METHOD_0         0  ''
               64  STORE_FAST               'typeinfo'
             66_0  COME_FROM            56  '56'

 L. 118        66  LOAD_FAST                'typeinfo'
               68  LOAD_CONST               None
               70  <117>                 1  ''
               72  POP_JUMP_IF_FALSE   116  'to 116'

 L. 119        74  SETUP_FINALLY        96  'to 96'

 L. 121        76  LOAD_FAST                'typeinfo'
               78  LOAD_METHOD              GetTypeComp
               80  CALL_METHOD_0         0  ''
               82  STORE_FAST               'typecomp'

 L. 122        84  LOAD_FAST                'typeinfo'
               86  LOAD_FAST                'typecomp'
               88  BUILD_TUPLE_2         2 
               90  STORE_FAST               'lazydata'
               92  POP_BLOCK        
               94  JUMP_FORWARD        116  'to 116'
             96_0  COME_FROM_FINALLY    74  '74'

 L. 123        96  DUP_TOP          
               98  LOAD_GLOBAL              pythoncom
              100  LOAD_ATTR                com_error
              102  <121>               114  ''
              104  POP_TOP          
              106  POP_TOP          
              108  POP_TOP          

 L. 124       110  POP_EXCEPT       
              112  JUMP_FORWARD        116  'to 116'
              114  <48>             
            116_0  COME_FROM           112  '112'
            116_1  COME_FROM            94  '94'
            116_2  COME_FROM            72  '72'
              116  POP_BLOCK        
              118  JUMP_FORWARD        144  'to 144'
            120_0  COME_FROM_FINALLY    48  '48'

 L. 125       120  DUP_TOP          
              122  LOAD_GLOBAL              pythoncom
              124  LOAD_ATTR                com_error
              126  <121>               142  ''
              128  POP_TOP          
              130  POP_TOP          
              132  POP_TOP          

 L. 126       134  LOAD_CONST               None
              136  STORE_FAST               'typeinfo'
              138  POP_EXCEPT       
              140  JUMP_FORWARD        144  'to 144'
              142  <48>             
            144_0  COME_FROM           140  '140'
            144_1  COME_FROM           118  '118'

 L. 127       144  LOAD_GLOBAL              MakeOleRepr
              146  LOAD_FAST                'IDispatch'
              148  LOAD_FAST                'typeinfo'
              150  LOAD_FAST                'lazydata'
              152  CALL_FUNCTION_3       3  ''
              154  STORE_FAST               'olerepr'

 L. 128       156  LOAD_FAST                'createClass'
              158  LOAD_FAST                'IDispatch'
              160  LOAD_FAST                'olerepr'
              162  LOAD_FAST                'userName'
              164  LOAD_FAST                'lazydata'
              166  LOAD_CONST               ('lazydata',)
              168  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              170  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def MakeOleRepr--- This code section failed: ---

 L. 131         0  LOAD_CONST               None
                2  STORE_FAST               'olerepr'

 L. 132         4  LOAD_FAST                'typeinfo'
                6  LOAD_CONST               None
                8  <117>                 1  ''
               10  POP_JUMP_IF_FALSE   140  'to 140'

 L. 133        12  SETUP_FINALLY       120  'to 120'

 L. 134        14  LOAD_FAST                'typeinfo'
               16  LOAD_METHOD              GetTypeAttr
               18  CALL_METHOD_0         0  ''
               20  STORE_FAST               'attr'

 L. 137        22  LOAD_FAST                'attr'
               24  LOAD_CONST               5
               26  BINARY_SUBSCR    
               28  LOAD_GLOBAL              pythoncom
               30  LOAD_ATTR                TKIND_INTERFACE
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_FALSE    78  'to 78'
               36  LOAD_FAST                'attr'
               38  LOAD_CONST               11
               40  BINARY_SUBSCR    
               42  LOAD_GLOBAL              pythoncom
               44  LOAD_ATTR                TYPEFLAG_FDUAL
               46  BINARY_AND       
               48  POP_JUMP_IF_FALSE    78  'to 78'

 L. 140        50  LOAD_FAST                'typeinfo'
               52  LOAD_METHOD              GetRefTypeOfImplType
               54  LOAD_CONST               -1
               56  CALL_METHOD_1         1  ''
               58  STORE_FAST               'href'

 L. 141        60  LOAD_FAST                'typeinfo'
               62  LOAD_METHOD              GetRefTypeInfo
               64  LOAD_FAST                'href'
               66  CALL_METHOD_1         1  ''
               68  STORE_FAST               'typeinfo'

 L. 142        70  LOAD_FAST                'typeinfo'
               72  LOAD_METHOD              GetTypeAttr
               74  CALL_METHOD_0         0  ''
               76  STORE_FAST               'attr'
             78_0  COME_FROM            48  '48'
             78_1  COME_FROM            34  '34'

 L. 143        78  LOAD_FAST                'typecomp'
               80  LOAD_CONST               None
               82  <117>                 0  ''
               84  POP_JUMP_IF_FALSE   104  'to 104'

 L. 144        86  LOAD_GLOBAL              build
               88  LOAD_METHOD              DispatchItem
               90  LOAD_FAST                'typeinfo'
               92  LOAD_FAST                'attr'
               94  LOAD_CONST               None
               96  LOAD_CONST               0
               98  CALL_METHOD_4         4  ''
              100  STORE_FAST               'olerepr'
              102  JUMP_FORWARD        116  'to 116'
            104_0  COME_FROM            84  '84'

 L. 146       104  LOAD_GLOBAL              build
              106  LOAD_METHOD              LazyDispatchItem
              108  LOAD_FAST                'attr'
              110  LOAD_CONST               None
              112  CALL_METHOD_2         2  ''
              114  STORE_FAST               'olerepr'
            116_0  COME_FROM           102  '102'
              116  POP_BLOCK        
              118  JUMP_FORWARD        140  'to 140'
            120_0  COME_FROM_FINALLY    12  '12'

 L. 147       120  DUP_TOP          
              122  LOAD_GLOBAL              pythoncom
              124  LOAD_ATTR                ole_error
              126  <121>               138  ''
              128  POP_TOP          
              130  POP_TOP          
              132  POP_TOP          

 L. 148       134  POP_EXCEPT       
              136  JUMP_FORWARD        140  'to 140'
              138  <48>             
            140_0  COME_FROM           136  '136'
            140_1  COME_FROM           118  '118'
            140_2  COME_FROM            10  '10'

 L. 149       140  LOAD_FAST                'olerepr'
              142  LOAD_CONST               None
              144  <117>                 0  ''
              146  POP_JUMP_IF_FALSE   156  'to 156'
              148  LOAD_GLOBAL              build
              150  LOAD_METHOD              DispatchItem
              152  CALL_METHOD_0         0  ''
              154  STORE_FAST               'olerepr'
            156_0  COME_FROM           146  '146'

 L. 150       156  LOAD_FAST                'olerepr'
              158  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 8


def DumbDispatch--- This code section failed: ---

 L. 154         0  LOAD_FAST                'UnicodeToString'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  <74>             
               10  LOAD_STR                 'this is deprecated and will go away'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 155        16  LOAD_GLOBAL              _GetGoodDispatchAndUserName
               18  LOAD_FAST                'IDispatch'
               20  LOAD_FAST                'userName'
               22  LOAD_FAST                'clsctx'
               24  CALL_FUNCTION_3       3  ''
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'IDispatch'
               30  STORE_FAST               'userName'

 L. 156        32  LOAD_FAST                'createClass'
               34  LOAD_CONST               None
               36  <117>                 0  ''
               38  POP_JUMP_IF_FALSE    44  'to 44'

 L. 157        40  LOAD_GLOBAL              CDispatch
               42  STORE_FAST               'createClass'
             44_0  COME_FROM            38  '38'

 L. 158        44  LOAD_FAST                'createClass'
               46  LOAD_FAST                'IDispatch'
               48  LOAD_GLOBAL              build
               50  LOAD_METHOD              DispatchItem
               52  CALL_METHOD_0         0  ''
               54  LOAD_FAST                'userName'
               56  CALL_FUNCTION_3       3  ''
               58  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class CDispatch:

    def __init__--- This code section failed: ---

 L. 162         0  LOAD_FAST                'UnicodeToString'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  <74>             
               10  LOAD_STR                 'this is deprecated and will go away'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 163        16  LOAD_FAST                'userName'
               18  LOAD_CONST               None
               20  <117>                 0  ''
               22  POP_JUMP_IF_FALSE    28  'to 28'
               24  LOAD_STR                 '<unknown>'
               26  STORE_FAST               'userName'
             28_0  COME_FROM            22  '22'

 L. 164        28  LOAD_FAST                'IDispatch'
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                __dict__
               34  LOAD_STR                 '_oleobj_'
               36  STORE_SUBSCR     

 L. 165        38  LOAD_FAST                'userName'
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                __dict__
               44  LOAD_STR                 '_username_'
               46  STORE_SUBSCR     

 L. 166        48  LOAD_FAST                'olerepr'
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                __dict__
               54  LOAD_STR                 '_olerepr_'
               56  STORE_SUBSCR     

 L. 167        58  BUILD_MAP_0           0 
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                __dict__
               64  LOAD_STR                 '_mapCachedItems_'
               66  STORE_SUBSCR     

 L. 168        68  BUILD_MAP_0           0 
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                __dict__
               74  LOAD_STR                 '_builtMethods_'
               76  STORE_SUBSCR     

 L. 169        78  LOAD_CONST               None
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                __dict__
               84  LOAD_STR                 '_enum_'
               86  STORE_SUBSCR     

 L. 170        88  LOAD_CONST               None
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                __dict__
               94  LOAD_STR                 '_unicode_to_string_'
               96  STORE_SUBSCR     

 L. 171        98  LOAD_FAST                'lazydata'
              100  LOAD_FAST                'self'
              102  LOAD_ATTR                __dict__
              104  LOAD_STR                 '_lazydata_'
              106  STORE_SUBSCR     

Parse error at or near `None' instruction at offset -1

    def __call__--- This code section failed: ---

 L. 175         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _olerepr_
                4  LOAD_ATTR                defaultDispatchName
                6  POP_JUMP_IF_FALSE    28  'to 28'

 L. 176         8  LOAD_FAST                'self'
               10  LOAD_METHOD              _find_dispatch_type_
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                _olerepr_
               16  LOAD_ATTR                defaultDispatchName
               18  CALL_METHOD_1         1  ''
               20  UNPACK_SEQUENCE_2     2 
               22  STORE_FAST               'invkind'
               24  STORE_FAST               'dispid'
               26  JUMP_FORWARD         48  'to 48'
             28_0  COME_FROM             6  '6'

 L. 178        28  LOAD_GLOBAL              pythoncom
               30  LOAD_ATTR                DISPATCH_METHOD
               32  LOAD_GLOBAL              pythoncom
               34  LOAD_ATTR                DISPATCH_PROPERTYGET
               36  BINARY_OR        
               38  LOAD_GLOBAL              pythoncom
               40  LOAD_ATTR                DISPID_VALUE
               42  ROT_TWO          
               44  STORE_FAST               'invkind'
               46  STORE_FAST               'dispid'
             48_0  COME_FROM            26  '26'

 L. 179        48  LOAD_FAST                'invkind'
               50  LOAD_CONST               None
               52  <117>                 1  ''
               54  POP_JUMP_IF_FALSE    98  'to 98'

 L. 180        56  LOAD_FAST                'dispid'
               58  LOAD_GLOBAL              LCID
               60  LOAD_FAST                'invkind'
               62  LOAD_CONST               1
               64  BUILD_TUPLE_4         4 
               66  LOAD_FAST                'args'
               68  BINARY_ADD       
               70  STORE_FAST               'allArgs'

 L. 181        72  LOAD_FAST                'self'
               74  LOAD_METHOD              _get_good_object_
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                _oleobj_
               80  LOAD_ATTR                Invoke
               82  LOAD_FAST                'allArgs'
               84  CALL_FUNCTION_EX      0  'positional arguments only'
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                _olerepr_
               90  LOAD_ATTR                defaultDispatchName
               92  LOAD_CONST               None
               94  CALL_METHOD_3         3  ''
               96  RETURN_VALUE     
             98_0  COME_FROM            54  '54'

 L. 182        98  LOAD_GLOBAL              TypeError
              100  LOAD_STR                 'This dispatch object does not define a default method'
              102  CALL_FUNCTION_1       1  ''
              104  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<117>' instruction at offset 52

    def __bool__(self):
        return True

    def __repr__(self):
        return '<COMObject %s>' % self._username_

    def __str__--- This code section failed: ---

 L. 195         0  SETUP_FINALLY        16  'to 16'

 L. 196         2  LOAD_GLOBAL              str
                4  LOAD_FAST                'self'
                6  LOAD_METHOD              __call__
                8  CALL_METHOD_0         0  ''
               10  CALL_FUNCTION_1       1  ''
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 197        16  DUP_TOP          
               18  LOAD_GLOBAL              pythoncom
               20  LOAD_ATTR                com_error
               22  <121>                72  ''
               24  POP_TOP          
               26  STORE_FAST               'details'
               28  POP_TOP          
               30  SETUP_FINALLY        64  'to 64'

 L. 198        32  LOAD_FAST                'details'
               34  LOAD_ATTR                hresult
               36  LOAD_GLOBAL              ERRORS_BAD_CONTEXT
               38  <118>                 1  ''
               40  POP_JUMP_IF_FALSE    44  'to 44'

 L. 199        42  RAISE_VARARGS_0       0  'reraise'
             44_0  COME_FROM            40  '40'

 L. 200        44  LOAD_FAST                'self'
               46  LOAD_METHOD              __repr__
               48  CALL_METHOD_0         0  ''
               50  POP_BLOCK        
               52  ROT_FOUR         
               54  POP_EXCEPT       
               56  LOAD_CONST               None
               58  STORE_FAST               'details'
               60  DELETE_FAST              'details'
               62  RETURN_VALUE     
             64_0  COME_FROM_FINALLY    30  '30'
               64  LOAD_CONST               None
               66  STORE_FAST               'details'
               68  DELETE_FAST              'details'
               70  <48>             
               72  <48>             

Parse error at or near `<121>' instruction at offset 22

    def __eq__(self, other):
        other = getattrother'_oleobj_'other
        return self._oleobj_ == other

    def __ne__(self, other):
        other = getattrother'_oleobj_'other
        return self._oleobj_ != other

    def __int__(self):
        return int(self.__call__)

    def __len__(self):
        invkind, dispid = self._find_dispatch_type_'Count'
        if invkind:
            return self._oleobj_.InvokedispidLCIDinvkind1
        raise TypeError('This dispatch object does not define a Count method')

    def _NewEnum--- This code section failed: ---

 L. 221         0  SETUP_FINALLY        40  'to 40'

 L. 222         2  LOAD_GLOBAL              pythoncom
                4  LOAD_ATTR                DISPATCH_METHOD
                6  LOAD_GLOBAL              pythoncom
                8  LOAD_ATTR                DISPATCH_PROPERTYGET
               10  BINARY_OR        
               12  STORE_FAST               'invkind'

 L. 223        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _oleobj_
               18  LOAD_METHOD              InvokeTypes
               20  LOAD_GLOBAL              pythoncom
               22  LOAD_ATTR                DISPID_NEWENUM
               24  LOAD_GLOBAL              LCID
               26  LOAD_FAST                'invkind'
               28  LOAD_CONST               (13, 10)
               30  LOAD_CONST               ()
               32  CALL_METHOD_5         5  ''
               34  STORE_FAST               'enum'
               36  POP_BLOCK        
               38  JUMP_FORWARD         62  'to 62'
             40_0  COME_FROM_FINALLY     0  '0'

 L. 224        40  DUP_TOP          
               42  LOAD_GLOBAL              pythoncom
               44  LOAD_ATTR                com_error
               46  <121>                60  ''
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 225        54  POP_EXCEPT       
               56  LOAD_CONST               None
               58  RETURN_VALUE     
               60  <48>             
             62_0  COME_FROM            38  '38'

 L. 226        62  LOAD_CONST               1
               64  LOAD_CONST               ('util',)
               66  IMPORT_NAME              
               68  IMPORT_FROM              util
               70  STORE_FAST               'util'
               72  POP_TOP          

 L. 227        74  LOAD_FAST                'util'
               76  LOAD_METHOD              WrapEnum
               78  LOAD_FAST                'enum'
               80  LOAD_CONST               None
               82  CALL_METHOD_2         2  ''
               84  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 46

    def __getitem__--- This code section failed: ---

 L. 232         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'index'
                4  LOAD_GLOBAL              int
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    70  'to 70'

 L. 233        10  LOAD_FAST                'self'
               12  LOAD_ATTR                __dict__
               14  LOAD_STR                 '_enum_'
               16  BINARY_SUBSCR    
               18  LOAD_CONST               None
               20  <117>                 0  ''
               22  POP_JUMP_IF_FALSE    38  'to 38'

 L. 234        24  LOAD_FAST                'self'
               26  LOAD_METHOD              _NewEnum
               28  CALL_METHOD_0         0  ''
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                __dict__
               34  LOAD_STR                 '_enum_'
               36  STORE_SUBSCR     
             38_0  COME_FROM            22  '22'

 L. 235        38  LOAD_FAST                'self'
               40  LOAD_ATTR                __dict__
               42  LOAD_STR                 '_enum_'
               44  BINARY_SUBSCR    
               46  LOAD_CONST               None
               48  <117>                 1  ''
               50  POP_JUMP_IF_FALSE    70  'to 70'

 L. 236        52  LOAD_FAST                'self'
               54  LOAD_METHOD              _get_good_object_
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                _enum_
               60  LOAD_METHOD              __getitem__
               62  LOAD_FAST                'index'
               64  CALL_METHOD_1         1  ''
               66  CALL_METHOD_1         1  ''
               68  RETURN_VALUE     
             70_0  COME_FROM            50  '50'
             70_1  COME_FROM             8  '8'

 L. 238        70  LOAD_FAST                'self'
               72  LOAD_METHOD              _find_dispatch_type_
               74  LOAD_STR                 'Item'
               76  CALL_METHOD_1         1  ''
               78  UNPACK_SEQUENCE_2     2 
               80  STORE_FAST               'invkind'
               82  STORE_FAST               'dispid'

 L. 239        84  LOAD_FAST                'invkind'
               86  LOAD_CONST               None
               88  <117>                 1  ''
               90  POP_JUMP_IF_FALSE   118  'to 118'

 L. 240        92  LOAD_FAST                'self'
               94  LOAD_METHOD              _get_good_object_
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                _oleobj_
              100  LOAD_METHOD              Invoke
              102  LOAD_FAST                'dispid'
              104  LOAD_GLOBAL              LCID
              106  LOAD_FAST                'invkind'
              108  LOAD_CONST               1
              110  LOAD_FAST                'index'
              112  CALL_METHOD_5         5  ''
              114  CALL_METHOD_1         1  ''
              116  RETURN_VALUE     
            118_0  COME_FROM            90  '90'

 L. 241       118  LOAD_GLOBAL              TypeError
              120  LOAD_STR                 'This object does not support enumeration'
              122  CALL_FUNCTION_1       1  ''
              124  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<117>' instruction at offset 20

    def __setitem__--- This code section failed: ---

 L. 246         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _olerepr_
                4  LOAD_ATTR                defaultDispatchName
                6  POP_JUMP_IF_FALSE    28  'to 28'

 L. 247         8  LOAD_FAST                'self'
               10  LOAD_METHOD              _find_dispatch_type_
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                _olerepr_
               16  LOAD_ATTR                defaultDispatchName
               18  CALL_METHOD_1         1  ''
               20  UNPACK_SEQUENCE_2     2 
               22  STORE_FAST               'invkind'
               24  STORE_FAST               'dispid'
               26  JUMP_FORWARD         48  'to 48'
             28_0  COME_FROM             6  '6'

 L. 249        28  LOAD_GLOBAL              pythoncom
               30  LOAD_ATTR                DISPATCH_PROPERTYPUT
               32  LOAD_GLOBAL              pythoncom
               34  LOAD_ATTR                DISPATCH_PROPERTYPUTREF
               36  BINARY_OR        
               38  LOAD_GLOBAL              pythoncom
               40  LOAD_ATTR                DISPID_VALUE
               42  ROT_TWO          
               44  STORE_FAST               'invkind'
               46  STORE_FAST               'dispid'
             48_0  COME_FROM            26  '26'

 L. 250        48  LOAD_FAST                'invkind'
               50  LOAD_CONST               None
               52  <117>                 1  ''
               54  POP_JUMP_IF_FALSE   100  'to 100'

 L. 251        56  LOAD_FAST                'dispid'
               58  LOAD_GLOBAL              LCID
               60  LOAD_FAST                'invkind'
               62  LOAD_CONST               0
               64  LOAD_FAST                'index'
               66  BUILD_TUPLE_5         5 
               68  LOAD_FAST                'args'
               70  BINARY_ADD       
               72  STORE_FAST               'allArgs'

 L. 252        74  LOAD_FAST                'self'
               76  LOAD_METHOD              _get_good_object_
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                _oleobj_
               82  LOAD_ATTR                Invoke
               84  LOAD_FAST                'allArgs'
               86  CALL_FUNCTION_EX      0  'positional arguments only'
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                _olerepr_
               92  LOAD_ATTR                defaultDispatchName
               94  LOAD_CONST               None
               96  CALL_METHOD_3         3  ''
               98  RETURN_VALUE     
            100_0  COME_FROM            54  '54'

 L. 253       100  LOAD_GLOBAL              TypeError
              102  LOAD_STR                 'This dispatch object does not define a default method'
              104  CALL_FUNCTION_1       1  ''
              106  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<117>' instruction at offset 52

    def _find_dispatch_type_--- This code section failed: ---

 L. 256         0  LOAD_FAST                'methodName'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _olerepr_
                6  LOAD_ATTR                mapFuncs
                8  <118>                 0  ''
               10  POP_JUMP_IF_FALSE    40  'to 40'

 L. 257        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _olerepr_
               16  LOAD_ATTR                mapFuncs
               18  LOAD_FAST                'methodName'
               20  BINARY_SUBSCR    
               22  STORE_FAST               'item'

 L. 258        24  LOAD_FAST                'item'
               26  LOAD_ATTR                desc
               28  LOAD_CONST               4
               30  BINARY_SUBSCR    
               32  LOAD_FAST                'item'
               34  LOAD_ATTR                dispid
               36  BUILD_TUPLE_2         2 
               38  RETURN_VALUE     
             40_0  COME_FROM            10  '10'

 L. 260        40  LOAD_FAST                'methodName'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                _olerepr_
               46  LOAD_ATTR                propMapGet
               48  <118>                 0  ''
               50  POP_JUMP_IF_FALSE    80  'to 80'

 L. 261        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _olerepr_
               56  LOAD_ATTR                propMapGet
               58  LOAD_FAST                'methodName'
               60  BINARY_SUBSCR    
               62  STORE_FAST               'item'

 L. 262        64  LOAD_FAST                'item'
               66  LOAD_ATTR                desc
               68  LOAD_CONST               4
               70  BINARY_SUBSCR    
               72  LOAD_FAST                'item'
               74  LOAD_ATTR                dispid
               76  BUILD_TUPLE_2         2 
               78  RETURN_VALUE     
             80_0  COME_FROM            50  '50'

 L. 264        80  SETUP_FINALLY       100  'to 100'

 L. 265        82  LOAD_FAST                'self'
               84  LOAD_ATTR                _oleobj_
               86  LOAD_METHOD              GetIDsOfNames
               88  LOAD_CONST               0
               90  LOAD_FAST                'methodName'
               92  CALL_METHOD_2         2  ''
               94  STORE_FAST               'dispid'
               96  POP_BLOCK        
               98  JUMP_FORWARD        114  'to 114'
            100_0  COME_FROM_FINALLY    80  '80'

 L. 266       100  POP_TOP          
              102  POP_TOP          
              104  POP_TOP          

 L. 267       106  POP_EXCEPT       
              108  LOAD_CONST               (None, None)
              110  RETURN_VALUE     
              112  <48>             
            114_0  COME_FROM            98  '98'

 L. 268       114  LOAD_GLOBAL              pythoncom
              116  LOAD_ATTR                DISPATCH_METHOD
              118  LOAD_GLOBAL              pythoncom
              120  LOAD_ATTR                DISPATCH_PROPERTYGET
              122  BINARY_OR        
              124  LOAD_FAST                'dispid'
              126  BUILD_TUPLE_2         2 
              128  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _ApplyTypes_(self, dispid, wFlags, retType, argTypes, user, resultCLSID, *args):
        result = (self._oleobj_.InvokeTypes)(*(dispid, LCID, wFlags, retType, argTypes) + args)
        return self._get_good_object_resultuserresultCLSID

    def _wrap_dispatch_--- This code section failed: ---

 L. 276         0  LOAD_FAST                'UnicodeToString'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  <74>             
               10  LOAD_STR                 'this is deprecated and will go away'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 277        16  LOAD_GLOBAL              Dispatch
               18  LOAD_FAST                'ob'
               20  LOAD_FAST                'userName'
               22  CALL_FUNCTION_2       2  ''
               24  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _get_good_single_object_--- This code section failed: ---

 L. 280         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'ob'
                4  LOAD_GLOBAL              PyIDispatchType
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L. 282        10  LOAD_FAST                'self'
               12  LOAD_METHOD              _wrap_dispatch_
               14  LOAD_FAST                'ob'
               16  LOAD_FAST                'userName'
               18  LOAD_FAST                'ReturnCLSID'
               20  CALL_METHOD_3         3  ''
               22  RETURN_VALUE     
             24_0  COME_FROM             8  '8'

 L. 283        24  LOAD_GLOBAL              isinstance
               26  LOAD_FAST                'ob'
               28  LOAD_GLOBAL              PyIUnknownType
               30  CALL_FUNCTION_2       2  ''
               32  POP_JUMP_IF_FALSE    90  'to 90'

 L. 284        34  SETUP_FINALLY        52  'to 52'

 L. 285        36  LOAD_FAST                'ob'
               38  LOAD_METHOD              QueryInterface
               40  LOAD_GLOBAL              pythoncom
               42  LOAD_ATTR                IID_IDispatch
               44  CALL_METHOD_1         1  ''
               46  STORE_FAST               'ob'
               48  POP_BLOCK        
               50  JUMP_FORWARD         76  'to 76'
             52_0  COME_FROM_FINALLY    34  '34'

 L. 286        52  DUP_TOP          
               54  LOAD_GLOBAL              pythoncom
               56  LOAD_ATTR                com_error
               58  <121>                74  ''
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L. 288        66  LOAD_FAST                'ob'
               68  ROT_FOUR         
               70  POP_EXCEPT       
               72  RETURN_VALUE     
               74  <48>             
             76_0  COME_FROM            50  '50'

 L. 289        76  LOAD_FAST                'self'
               78  LOAD_METHOD              _wrap_dispatch_
               80  LOAD_FAST                'ob'
               82  LOAD_FAST                'userName'
               84  LOAD_FAST                'ReturnCLSID'
               86  CALL_METHOD_3         3  ''
               88  RETURN_VALUE     
             90_0  COME_FROM            32  '32'

 L. 290        90  LOAD_FAST                'ob'
               92  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 58

    def _get_good_object_--- This code section failed: ---

 L. 296         0  LOAD_FAST                'ob'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 297         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 298        12  LOAD_GLOBAL              isinstance
               14  LOAD_FAST                'ob'
               16  LOAD_GLOBAL              tuple
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_FALSE    48  'to 48'

 L. 299        22  LOAD_GLOBAL              tuple
               24  LOAD_GLOBAL              map
               26  LOAD_FAST                'self'
               28  LOAD_FAST                'userName'
               30  LOAD_FAST                'ReturnCLSID'
               32  BUILD_TUPLE_3         3 
               34  LOAD_LAMBDA              '<code_object <lambda>>'
               36  LOAD_STR                 'CDispatch._get_good_object_.<locals>.<lambda>'
               38  MAKE_FUNCTION_1          'default'
               40  LOAD_FAST                'ob'
               42  CALL_FUNCTION_2       2  ''
               44  CALL_FUNCTION_1       1  ''
               46  RETURN_VALUE     
             48_0  COME_FROM            20  '20'

 L. 301        48  LOAD_FAST                'self'
               50  LOAD_METHOD              _get_good_single_object_
               52  LOAD_FAST                'ob'
               54  CALL_METHOD_1         1  ''
               56  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1

    def _make_method_--- This code section failed: ---

 L. 305         0  LOAD_GLOBAL              build
                2  LOAD_METHOD              MakePublicAttributeName
                4  LOAD_FAST                'name'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'methodName'

 L. 306        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _olerepr_
               14  LOAD_METHOD              MakeFuncMethod
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _olerepr_
               20  LOAD_ATTR                mapFuncs
               22  LOAD_FAST                'name'
               24  BINARY_SUBSCR    
               26  LOAD_FAST                'methodName'
               28  LOAD_CONST               0
               30  CALL_METHOD_3         3  ''
               32  STORE_FAST               'methodCodeList'

 L. 307        34  LOAD_STR                 '\n'
               36  LOAD_METHOD              join
               38  LOAD_FAST                'methodCodeList'
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'methodCode'

 L. 308        44  SETUP_FINALLY       144  'to 144'

 L. 311        46  LOAD_GLOBAL              compile
               48  LOAD_FAST                'methodCode'
               50  LOAD_STR                 '<COMObject %s>'
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                _username_
               56  BINARY_MODULO    
               58  LOAD_STR                 'exec'
               60  CALL_FUNCTION_3       3  ''
               62  STORE_FAST               'codeObject'

 L. 313        64  BUILD_MAP_0           0 
               66  STORE_FAST               'tempNameSpace'

 L. 315        68  LOAD_GLOBAL              globals
               70  CALL_FUNCTION_0       0  ''
               72  LOAD_METHOD              copy
               74  CALL_METHOD_0         0  ''
               76  STORE_FAST               'globNameSpace'

 L. 316        78  LOAD_GLOBAL              win32com
               80  LOAD_ATTR                client
               82  LOAD_ATTR                Dispatch
               84  LOAD_FAST                'globNameSpace'
               86  LOAD_STR                 'Dispatch'
               88  STORE_SUBSCR     

 L. 317        90  LOAD_GLOBAL              exec
               92  LOAD_FAST                'codeObject'
               94  LOAD_FAST                'globNameSpace'
               96  LOAD_FAST                'tempNameSpace'
               98  CALL_FUNCTION_3       3  ''
              100  POP_TOP          

 L. 318       102  LOAD_FAST                'methodName'
              104  STORE_FAST               'name'

 L. 320       106  LOAD_FAST                'tempNameSpace'
              108  LOAD_FAST                'name'
              110  BINARY_SUBSCR    
              112  DUP_TOP          
              114  STORE_FAST               'fn'
              116  LOAD_FAST                'self'
              118  LOAD_ATTR                _builtMethods_
              120  LOAD_FAST                'name'
              122  STORE_SUBSCR     

 L. 321       124  LOAD_GLOBAL              MakeMethod
              126  LOAD_FAST                'fn'
              128  LOAD_FAST                'self'
              130  LOAD_FAST                'self'
              132  LOAD_ATTR                __class__
              134  CALL_FUNCTION_3       3  ''
              136  STORE_FAST               'newMeth'

 L. 322       138  LOAD_FAST                'newMeth'
              140  POP_BLOCK        
              142  RETURN_VALUE     
            144_0  COME_FROM_FINALLY    44  '44'

 L. 323       144  POP_TOP          
              146  POP_TOP          
              148  POP_TOP          

 L. 324       150  LOAD_GLOBAL              debug_print
              152  LOAD_STR                 'Error building OLE definition for code '
              154  LOAD_FAST                'methodCode'
              156  CALL_FUNCTION_2       2  ''
              158  POP_TOP          

 L. 325       160  LOAD_GLOBAL              traceback
              162  LOAD_METHOD              print_exc
              164  CALL_METHOD_0         0  ''
              166  POP_TOP          
              168  POP_EXCEPT       
              170  JUMP_FORWARD        174  'to 174'
              172  <48>             
            174_0  COME_FROM           170  '170'

Parse error at or near `POP_TOP' instruction at offset 158

    def _Release_(self):
        """Cleanup object - like a close - to force cleanup when you dont
                   want to rely on Python's reference counting."""
        for childCont in self._mapCachedItems_.values:
            childCont._Release_
        else:
            self._mapCachedItems_ = {}
            if self._oleobj_:
                self._oleobj_.Release
                self.__dict__['_oleobj_'] = None
            if self._olerepr_:
                self.__dict__['_olerepr_'] = None
            self._enum_ = None

    def _proc_--- This code section failed: ---

 L. 344         0  SETUP_FINALLY        58  'to 58'

 L. 345         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _olerepr_
                6  LOAD_ATTR                mapFuncs
                8  LOAD_FAST                'name'
               10  BINARY_SUBSCR    
               12  STORE_FAST               'item'

 L. 346        14  LOAD_FAST                'item'
               16  LOAD_ATTR                dispid
               18  STORE_FAST               'dispId'

 L. 347        20  LOAD_FAST                'self'
               22  LOAD_METHOD              _get_good_object_
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                _oleobj_
               28  LOAD_ATTR                Invoke
               30  LOAD_FAST                'dispId'
               32  LOAD_GLOBAL              LCID
               34  LOAD_FAST                'item'
               36  LOAD_ATTR                desc
               38  LOAD_CONST               4
               40  BINARY_SUBSCR    
               42  LOAD_CONST               0
               44  BUILD_TUPLE_4         4 
               46  LOAD_FAST                'args'
               48  BINARY_ADD       
               50  CALL_FUNCTION_EX      0  'positional arguments only'
               52  CALL_METHOD_1         1  ''
               54  POP_BLOCK        
               56  RETURN_VALUE     
             58_0  COME_FROM_FINALLY     0  '0'

 L. 348        58  DUP_TOP          
               60  LOAD_GLOBAL              KeyError
               62  <121>                82  ''
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          

 L. 349        70  LOAD_GLOBAL              AttributeError
               72  LOAD_FAST                'name'
               74  CALL_FUNCTION_1       1  ''
               76  RAISE_VARARGS_1       1  'exception instance'
               78  POP_EXCEPT       
               80  JUMP_FORWARD         84  'to 84'
               82  <48>             
             84_0  COME_FROM            80  '80'

Parse error at or near `<121>' instruction at offset 62

    def _print_details_--- This code section failed: ---

 L. 353         0  LOAD_GLOBAL              print
                2  LOAD_STR                 'AxDispatch container'
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _username_
                8  CALL_FUNCTION_2       2  ''
               10  POP_TOP          

 L. 354        12  SETUP_FINALLY       216  'to 216'

 L. 355        14  LOAD_GLOBAL              print
               16  LOAD_STR                 'Methods:'
               18  CALL_FUNCTION_1       1  ''
               20  POP_TOP          

 L. 356        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _olerepr_
               26  LOAD_ATTR                mapFuncs
               28  LOAD_METHOD              keys
               30  CALL_METHOD_0         0  ''
               32  GET_ITER         
               34  FOR_ITER             50  'to 50'
               36  STORE_FAST               'method'

 L. 357        38  LOAD_GLOBAL              print
               40  LOAD_STR                 '\t'
               42  LOAD_FAST                'method'
               44  CALL_FUNCTION_2       2  ''
               46  POP_TOP          
               48  JUMP_BACK            34  'to 34'

 L. 358        50  LOAD_GLOBAL              print
               52  LOAD_STR                 'Props:'
               54  CALL_FUNCTION_1       1  ''
               56  POP_TOP          

 L. 359        58  LOAD_FAST                'self'
               60  LOAD_ATTR                _olerepr_
               62  LOAD_ATTR                propMap
               64  LOAD_METHOD              items
               66  CALL_METHOD_0         0  ''
               68  GET_ITER         
               70  FOR_ITER            104  'to 104'
               72  UNPACK_SEQUENCE_2     2 
               74  STORE_FAST               'prop'
               76  STORE_FAST               'entry'

 L. 360        78  LOAD_GLOBAL              print
               80  LOAD_STR                 '\t%s = 0x%x - %s'
               82  LOAD_FAST                'prop'
               84  LOAD_FAST                'entry'
               86  LOAD_ATTR                dispid
               88  LOAD_GLOBAL              repr
               90  LOAD_FAST                'entry'
               92  CALL_FUNCTION_1       1  ''
               94  BUILD_TUPLE_3         3 
               96  BINARY_MODULO    
               98  CALL_FUNCTION_1       1  ''
              100  POP_TOP          
              102  JUMP_BACK            70  'to 70'

 L. 361       104  LOAD_GLOBAL              print
              106  LOAD_STR                 'Get Props:'
              108  CALL_FUNCTION_1       1  ''
              110  POP_TOP          

 L. 362       112  LOAD_FAST                'self'
              114  LOAD_ATTR                _olerepr_
              116  LOAD_ATTR                propMapGet
              118  LOAD_METHOD              items
              120  CALL_METHOD_0         0  ''
              122  GET_ITER         
              124  FOR_ITER            158  'to 158'
              126  UNPACK_SEQUENCE_2     2 
              128  STORE_FAST               'prop'
              130  STORE_FAST               'entry'

 L. 363       132  LOAD_GLOBAL              print
              134  LOAD_STR                 '\t%s = 0x%x - %s'
              136  LOAD_FAST                'prop'
              138  LOAD_FAST                'entry'
              140  LOAD_ATTR                dispid
              142  LOAD_GLOBAL              repr
              144  LOAD_FAST                'entry'
              146  CALL_FUNCTION_1       1  ''
              148  BUILD_TUPLE_3         3 
              150  BINARY_MODULO    
              152  CALL_FUNCTION_1       1  ''
              154  POP_TOP          
              156  JUMP_BACK           124  'to 124'

 L. 364       158  LOAD_GLOBAL              print
              160  LOAD_STR                 'Put Props:'
              162  CALL_FUNCTION_1       1  ''
              164  POP_TOP          

 L. 365       166  LOAD_FAST                'self'
              168  LOAD_ATTR                _olerepr_
              170  LOAD_ATTR                propMapPut
              172  LOAD_METHOD              items
              174  CALL_METHOD_0         0  ''
              176  GET_ITER         
              178  FOR_ITER            212  'to 212'
              180  UNPACK_SEQUENCE_2     2 
              182  STORE_FAST               'prop'
              184  STORE_FAST               'entry'

 L. 366       186  LOAD_GLOBAL              print
              188  LOAD_STR                 '\t%s = 0x%x - %s'
              190  LOAD_FAST                'prop'
              192  LOAD_FAST                'entry'
              194  LOAD_ATTR                dispid
              196  LOAD_GLOBAL              repr
              198  LOAD_FAST                'entry'
              200  CALL_FUNCTION_1       1  ''
              202  BUILD_TUPLE_3         3 
              204  BINARY_MODULO    
              206  CALL_FUNCTION_1       1  ''
              208  POP_TOP          
              210  JUMP_BACK           178  'to 178'
              212  POP_BLOCK        
              214  JUMP_FORWARD        236  'to 236'
            216_0  COME_FROM_FINALLY    12  '12'

 L. 367       216  POP_TOP          
              218  POP_TOP          
              220  POP_TOP          

 L. 368       222  LOAD_GLOBAL              traceback
              224  LOAD_METHOD              print_exc
              226  CALL_METHOD_0         0  ''
              228  POP_TOP          
              230  POP_EXCEPT       
              232  JUMP_FORWARD        236  'to 236'
              234  <48>             
            236_0  COME_FROM           232  '232'
            236_1  COME_FROM           214  '214'

Parse error at or near `<48>' instruction at offset 234

    def __LazyMap__--- This code section failed: ---

 L. 371         0  SETUP_FINALLY        40  'to 40'

 L. 372         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _LazyAddAttr_
                6  LOAD_FAST                'attr'
                8  CALL_METHOD_1         1  ''
               10  POP_JUMP_IF_FALSE    36  'to 36'

 L. 373        12  LOAD_GLOBAL              debug_attr_print
               14  LOAD_STR                 '%s.__LazyMap__(%s) added something'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _username_
               20  LOAD_FAST                'attr'
               22  BUILD_TUPLE_2         2 
               24  BINARY_MODULO    
               26  CALL_FUNCTION_1       1  ''
               28  POP_TOP          

 L. 374        30  POP_BLOCK        
               32  LOAD_CONST               1
               34  RETURN_VALUE     
             36_0  COME_FROM            10  '10'
               36  POP_BLOCK        
               38  JUMP_FORWARD         60  'to 60'
             40_0  COME_FROM_FINALLY     0  '0'

 L. 375        40  DUP_TOP          
               42  LOAD_GLOBAL              AttributeError
               44  <121>                58  ''
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L. 376        52  POP_EXCEPT       
               54  LOAD_CONST               0
               56  RETURN_VALUE     
               58  <48>             
             60_0  COME_FROM            38  '38'

Parse error at or near `LOAD_CONST' instruction at offset 32

    def _LazyAddAttr_--- This code section failed: ---

 L. 380         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _lazydata_
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'
               10  LOAD_CONST               0
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 381        14  LOAD_CONST               0
               16  STORE_FAST               'res'

 L. 382        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _lazydata_
               22  UNPACK_SEQUENCE_2     2 
               24  STORE_FAST               'typeinfo'
               26  STORE_FAST               'typecomp'

 L. 383        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _olerepr_
               32  STORE_FAST               'olerepr'

 L. 388        34  LOAD_GLOBAL              ALL_INVOKE_TYPES
               36  GET_ITER         
               38  FOR_ITER            262  'to 262'
               40  STORE_FAST               'i'

 L. 389        42  SETUP_FINALLY       248  'to 248'

 L. 390        44  LOAD_FAST                'typecomp'
               46  LOAD_METHOD              Bind
               48  LOAD_FAST                'attr'
               50  LOAD_FAST                'i'
               52  CALL_METHOD_2         2  ''
               54  UNPACK_SEQUENCE_2     2 
               56  STORE_FAST               'x'
               58  STORE_FAST               't'

 L. 393        60  LOAD_FAST                'x'
               62  LOAD_CONST               0
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE   108  'to 108'
               68  LOAD_FAST                'attr'
               70  LOAD_CONST               None
               72  LOAD_CONST               3
               74  BUILD_SLICE_2         2 
               76  BINARY_SUBSCR    
               78  LOAD_CONST               ('Set', 'Get')
               80  <118>                 0  ''
               82  POP_JUMP_IF_FALSE   108  'to 108'

 L. 394        84  LOAD_FAST                'typecomp'
               86  LOAD_METHOD              Bind
               88  LOAD_FAST                'attr'
               90  LOAD_CONST               3
               92  LOAD_CONST               None
               94  BUILD_SLICE_2         2 
               96  BINARY_SUBSCR    
               98  LOAD_FAST                'i'
              100  CALL_METHOD_2         2  ''
              102  UNPACK_SEQUENCE_2     2 
              104  STORE_FAST               'x'
              106  STORE_FAST               't'
            108_0  COME_FROM            82  '82'
            108_1  COME_FROM            66  '66'

 L. 395       108  LOAD_FAST                'x'
              110  LOAD_CONST               1
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   132  'to 132'

 L. 396       116  LOAD_FAST                'olerepr'
              118  LOAD_METHOD              _AddFunc_
              120  LOAD_FAST                'typeinfo'
              122  LOAD_FAST                't'
              124  LOAD_CONST               0
              126  CALL_METHOD_3         3  ''
              128  STORE_FAST               'r'
              130  JUMP_FORWARD        160  'to 160'
            132_0  COME_FROM           114  '114'

 L. 397       132  LOAD_FAST                'x'
              134  LOAD_CONST               2
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_FALSE   156  'to 156'

 L. 398       140  LOAD_FAST                'olerepr'
              142  LOAD_METHOD              _AddVar_
              144  LOAD_FAST                'typeinfo'
              146  LOAD_FAST                't'
              148  LOAD_CONST               0
              150  CALL_METHOD_3         3  ''
              152  STORE_FAST               'r'
              154  JUMP_FORWARD        160  'to 160'
            156_0  COME_FROM           138  '138'

 L. 400       156  LOAD_CONST               None
              158  STORE_FAST               'r'
            160_0  COME_FROM           154  '154'
            160_1  COME_FROM           130  '130'

 L. 401       160  LOAD_FAST                'r'
              162  LOAD_CONST               None
              164  <117>                 1  ''
              166  POP_JUMP_IF_FALSE   244  'to 244'

 L. 402       168  LOAD_FAST                'r'
              170  LOAD_CONST               0
              172  BINARY_SUBSCR    
              174  LOAD_FAST                'r'
              176  LOAD_CONST               1
              178  BINARY_SUBSCR    
              180  ROT_TWO          
              182  STORE_FAST               'key'
              184  STORE_FAST               'map'

 L. 403       186  LOAD_FAST                'map'
              188  LOAD_FAST                'key'
              190  BINARY_SUBSCR    
              192  STORE_FAST               'item'

 L. 404       194  LOAD_FAST                'map'
              196  LOAD_FAST                'olerepr'
              198  LOAD_ATTR                propMapPut
              200  COMPARE_OP               ==
              202  POP_JUMP_IF_FALSE   218  'to 218'

 L. 405       204  LOAD_FAST                'olerepr'
              206  LOAD_METHOD              _propMapPutCheck_
              208  LOAD_FAST                'key'
              210  LOAD_FAST                'item'
              212  CALL_METHOD_2         2  ''
              214  POP_TOP          
              216  JUMP_FORWARD        240  'to 240'
            218_0  COME_FROM           202  '202'

 L. 406       218  LOAD_FAST                'map'
              220  LOAD_FAST                'olerepr'
              222  LOAD_ATTR                propMapGet
              224  COMPARE_OP               ==
              226  POP_JUMP_IF_FALSE   240  'to 240'

 L. 407       228  LOAD_FAST                'olerepr'
              230  LOAD_METHOD              _propMapGetCheck_
              232  LOAD_FAST                'key'
              234  LOAD_FAST                'item'
              236  CALL_METHOD_2         2  ''
              238  POP_TOP          
            240_0  COME_FROM           226  '226'
            240_1  COME_FROM           216  '216'

 L. 408       240  LOAD_CONST               1
              242  STORE_FAST               'res'
            244_0  COME_FROM           166  '166'
              244  POP_BLOCK        
              246  JUMP_BACK            38  'to 38'
            248_0  COME_FROM_FINALLY    42  '42'

 L. 409       248  POP_TOP          
              250  POP_TOP          
              252  POP_TOP          

 L. 410       254  POP_EXCEPT       
              256  JUMP_BACK            38  'to 38'
              258  <48>             
              260  JUMP_BACK            38  'to 38'

 L. 411       262  LOAD_FAST                'res'
              264  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _FlagAsMethod(self, *methodNames):
        """Flag these attribute names as being methods.
                Some objects do not correctly differentiate methods and
                properties, leading to problems when calling these methods.

                Specifically, trying to say: ob.SomeFunc()
                may yield an exception "None object is not callable"
                In this case, an attempt to fetch the *property*has worked
                and returned None, rather than indicating it is really a method.
                Calling: ob._FlagAsMethod("SomeFunc")
                should then allow this to work.
                """
        for name in methodNames:
            details = build.MapEntry(self.__AttrToID__name, (name,))
            self._olerepr_.mapFuncs[name] = details

    def __AttrToID__(self, attr):
        debug_attr_print('Calling GetIDsOfNames for property %s in Dispatch container %s' % (attr, self._username_))
        return self._oleobj_.GetIDsOfNames(0, attr)

    def __getattr__--- This code section failed: ---

 L. 434         0  LOAD_FAST                'attr'
                2  LOAD_STR                 '__iter__'
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    98  'to 98'

 L. 437         8  SETUP_FINALLY        48  'to 48'

 L. 438        10  LOAD_GLOBAL              pythoncom
               12  LOAD_ATTR                DISPATCH_METHOD
               14  LOAD_GLOBAL              pythoncom
               16  LOAD_ATTR                DISPATCH_PROPERTYGET
               18  BINARY_OR        
               20  STORE_FAST               'invkind'

 L. 439        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _oleobj_
               26  LOAD_METHOD              InvokeTypes
               28  LOAD_GLOBAL              pythoncom
               30  LOAD_ATTR                DISPID_NEWENUM
               32  LOAD_GLOBAL              LCID
               34  LOAD_FAST                'invkind'
               36  LOAD_CONST               (13, 10)
               38  LOAD_CONST               ()
               40  CALL_METHOD_5         5  ''
               42  STORE_FAST               'enum'
               44  POP_BLOCK        
               46  JUMP_FORWARD         76  'to 76'
             48_0  COME_FROM_FINALLY     8  '8'

 L. 440        48  DUP_TOP          
               50  LOAD_GLOBAL              pythoncom
               52  LOAD_ATTR                com_error
               54  <121>                74  ''
               56  POP_TOP          
               58  POP_TOP          
               60  POP_TOP          

 L. 441        62  LOAD_GLOBAL              AttributeError
               64  LOAD_STR                 'This object can not function as an iterator'
               66  CALL_FUNCTION_1       1  ''
               68  RAISE_VARARGS_1       1  'exception instance'
               70  POP_EXCEPT       
               72  JUMP_FORWARD         76  'to 76'
               74  <48>             
             76_0  COME_FROM            72  '72'
             76_1  COME_FROM            46  '46'

 L. 443        76  LOAD_BUILD_CLASS 
               78  LOAD_CODE                <code_object Factory>
               80  LOAD_STR                 'Factory'
               82  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               84  LOAD_STR                 'Factory'
               86  CALL_FUNCTION_2       2  ''
               88  STORE_FAST               'Factory'

 L. 449        90  LOAD_FAST                'Factory'
               92  LOAD_FAST                'enum'
               94  CALL_FUNCTION_1       1  ''
               96  RETURN_VALUE     
             98_0  COME_FROM             6  '6'

 L. 451        98  LOAD_FAST                'attr'
              100  LOAD_METHOD              startswith
              102  LOAD_STR                 '_'
              104  CALL_METHOD_1         1  ''
              106  POP_JUMP_IF_FALSE   126  'to 126'
              108  LOAD_FAST                'attr'
              110  LOAD_METHOD              endswith
              112  LOAD_STR                 '_'
              114  CALL_METHOD_1         1  ''
              116  POP_JUMP_IF_FALSE   126  'to 126'

 L. 452       118  LOAD_GLOBAL              AttributeError
              120  LOAD_FAST                'attr'
              122  CALL_FUNCTION_1       1  ''
              124  RAISE_VARARGS_1       1  'exception instance'
            126_0  COME_FROM           116  '116'
            126_1  COME_FROM           106  '106'

 L. 454       126  SETUP_FINALLY       150  'to 150'

 L. 455       128  LOAD_GLOBAL              MakeMethod
              130  LOAD_FAST                'self'
              132  LOAD_ATTR                _builtMethods_
              134  LOAD_FAST                'attr'
              136  BINARY_SUBSCR    
              138  LOAD_FAST                'self'
              140  LOAD_FAST                'self'
              142  LOAD_ATTR                __class__
              144  CALL_FUNCTION_3       3  ''
              146  POP_BLOCK        
              148  RETURN_VALUE     
            150_0  COME_FROM_FINALLY   126  '126'

 L. 456       150  DUP_TOP          
              152  LOAD_GLOBAL              KeyError
              154  <121>               166  ''
              156  POP_TOP          
              158  POP_TOP          
              160  POP_TOP          

 L. 457       162  POP_EXCEPT       
              164  JUMP_FORWARD        168  'to 168'
              166  <48>             
            168_0  COME_FROM           164  '164'

 L. 464       168  LOAD_FAST                'attr'
              170  LOAD_FAST                'self'
              172  LOAD_ATTR                _olerepr_
              174  LOAD_ATTR                mapFuncs
              176  <118>                 0  ''
              178  POP_JUMP_IF_FALSE   190  'to 190'

 L. 465       180  LOAD_FAST                'self'
              182  LOAD_METHOD              _make_method_
              184  LOAD_FAST                'attr'
              186  CALL_METHOD_1         1  ''
              188  RETURN_VALUE     
            190_0  COME_FROM           178  '178'

 L. 468       190  LOAD_CONST               None
              192  STORE_FAST               'retEntry'

 L. 469       194  LOAD_FAST                'self'
              196  LOAD_ATTR                _olerepr_
          198_200  POP_JUMP_IF_FALSE   390  'to 390'
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                _oleobj_
          206_208  POP_JUMP_IF_FALSE   390  'to 390'

 L. 471       210  LOAD_FAST                'self'
              212  LOAD_ATTR                _olerepr_
              214  LOAD_ATTR                propMap
              216  LOAD_METHOD              get
              218  LOAD_FAST                'attr'
              220  CALL_METHOD_1         1  ''
              222  STORE_FAST               'retEntry'

 L. 472       224  LOAD_FAST                'retEntry'
              226  LOAD_CONST               None
              228  <117>                 0  ''
              230  POP_JUMP_IF_FALSE   246  'to 246'

 L. 473       232  LOAD_FAST                'self'
              234  LOAD_ATTR                _olerepr_
              236  LOAD_ATTR                propMapGet
              238  LOAD_METHOD              get
              240  LOAD_FAST                'attr'
              242  CALL_METHOD_1         1  ''
              244  STORE_FAST               'retEntry'
            246_0  COME_FROM           230  '230'

 L. 475       246  LOAD_FAST                'retEntry'
              248  LOAD_CONST               None
              250  <117>                 0  ''
          252_254  POP_JUMP_IF_FALSE   390  'to 390'

 L. 476       256  SETUP_FINALLY       368  'to 368'

 L. 477       258  LOAD_FAST                'self'
              260  LOAD_METHOD              __LazyMap__
              262  LOAD_FAST                'attr'
              264  CALL_METHOD_1         1  ''
          266_268  POP_JUMP_IF_FALSE   334  'to 334'

 L. 478       270  LOAD_FAST                'attr'
              272  LOAD_FAST                'self'
              274  LOAD_ATTR                _olerepr_
              276  LOAD_ATTR                mapFuncs
              278  <118>                 0  ''
          280_282  POP_JUMP_IF_FALSE   296  'to 296'
              284  LOAD_FAST                'self'
              286  LOAD_METHOD              _make_method_
              288  LOAD_FAST                'attr'
              290  CALL_METHOD_1         1  ''
              292  POP_BLOCK        
              294  RETURN_VALUE     
            296_0  COME_FROM           280  '280'

 L. 479       296  LOAD_FAST                'self'
              298  LOAD_ATTR                _olerepr_
              300  LOAD_ATTR                propMap
              302  LOAD_METHOD              get
              304  LOAD_FAST                'attr'
              306  CALL_METHOD_1         1  ''
              308  STORE_FAST               'retEntry'

 L. 480       310  LOAD_FAST                'retEntry'
              312  LOAD_CONST               None
              314  <117>                 0  ''
          316_318  POP_JUMP_IF_FALSE   334  'to 334'

 L. 481       320  LOAD_FAST                'self'
              322  LOAD_ATTR                _olerepr_
              324  LOAD_ATTR                propMapGet
              326  LOAD_METHOD              get
              328  LOAD_FAST                'attr'
              330  CALL_METHOD_1         1  ''
              332  STORE_FAST               'retEntry'
            334_0  COME_FROM           316  '316'
            334_1  COME_FROM           266  '266'

 L. 482       334  LOAD_FAST                'retEntry'
              336  LOAD_CONST               None
              338  <117>                 0  ''
          340_342  POP_JUMP_IF_FALSE   364  'to 364'

 L. 483       344  LOAD_GLOBAL              build
              346  LOAD_METHOD              MapEntry
              348  LOAD_FAST                'self'
              350  LOAD_METHOD              __AttrToID__
              352  LOAD_FAST                'attr'
              354  CALL_METHOD_1         1  ''
              356  LOAD_FAST                'attr'
              358  BUILD_TUPLE_1         1 
              360  CALL_METHOD_2         2  ''
              362  STORE_FAST               'retEntry'
            364_0  COME_FROM           340  '340'
              364  POP_BLOCK        
              366  JUMP_FORWARD        390  'to 390'
            368_0  COME_FROM_FINALLY   256  '256'

 L. 484       368  DUP_TOP          
              370  LOAD_GLOBAL              pythoncom
              372  LOAD_ATTR                ole_error
          374_376  <121>               388  ''
              378  POP_TOP          
              380  POP_TOP          
              382  POP_TOP          

 L. 485       384  POP_EXCEPT       
              386  JUMP_FORWARD        390  'to 390'
              388  <48>             
            390_0  COME_FROM           386  '386'
            390_1  COME_FROM           366  '366'
            390_2  COME_FROM           252  '252'
            390_3  COME_FROM           206  '206'
            390_4  COME_FROM           198  '198'

 L. 487       390  LOAD_FAST                'retEntry'
              392  LOAD_CONST               None
              394  <117>                 1  ''
          396_398  POP_JUMP_IF_FALSE   466  'to 466'

 L. 488       400  SETUP_FINALLY       430  'to 430'

 L. 489       402  LOAD_FAST                'self'
              404  LOAD_ATTR                _mapCachedItems_
              406  LOAD_FAST                'retEntry'
              408  LOAD_ATTR                dispid
              410  BINARY_SUBSCR    
              412  STORE_FAST               'ret'

 L. 490       414  LOAD_GLOBAL              debug_attr_print
              416  LOAD_STR                 'Cached items has attribute!'
              418  LOAD_FAST                'ret'
              420  CALL_FUNCTION_2       2  ''
              422  POP_TOP          

 L. 491       424  LOAD_FAST                'ret'
              426  POP_BLOCK        
              428  RETURN_VALUE     
            430_0  COME_FROM_FINALLY   400  '400'

 L. 492       430  DUP_TOP          
              432  LOAD_GLOBAL              KeyError
              434  LOAD_GLOBAL              AttributeError
              436  BUILD_TUPLE_2         2 
          438_440  <121>               464  ''
              442  POP_TOP          
              444  POP_TOP          
              446  POP_TOP          

 L. 493       448  LOAD_GLOBAL              debug_attr_print
              450  LOAD_STR                 'Attribute %s not in cache'
              452  LOAD_FAST                'attr'
              454  BINARY_MODULO    
              456  CALL_FUNCTION_1       1  ''
              458  POP_TOP          
              460  POP_EXCEPT       
              462  JUMP_FORWARD        466  'to 466'
              464  <48>             
            466_0  COME_FROM           462  '462'
            466_1  COME_FROM           396  '396'

 L. 496       466  LOAD_FAST                'retEntry'
              468  LOAD_CONST               None
              470  <117>                 1  ''
          472_474  POP_JUMP_IF_FALSE   636  'to 636'

 L. 497       476  LOAD_GLOBAL              _GetDescInvokeType
              478  LOAD_FAST                'retEntry'
              480  LOAD_GLOBAL              pythoncom
              482  LOAD_ATTR                INVOKE_PROPERTYGET
              484  CALL_FUNCTION_2       2  ''
              486  STORE_FAST               'invoke_type'

 L. 498       488  LOAD_GLOBAL              debug_attr_print
              490  LOAD_STR                 'Getting property Id 0x%x from OLE object'
              492  LOAD_FAST                'retEntry'
              494  LOAD_ATTR                dispid
              496  BINARY_MODULO    
              498  CALL_FUNCTION_1       1  ''
              500  POP_TOP          

 L. 499       502  SETUP_FINALLY       528  'to 528'

 L. 500       504  LOAD_FAST                'self'
              506  LOAD_ATTR                _oleobj_
              508  LOAD_METHOD              Invoke
              510  LOAD_FAST                'retEntry'
              512  LOAD_ATTR                dispid
              514  LOAD_CONST               0
              516  LOAD_FAST                'invoke_type'
              518  LOAD_CONST               1
              520  CALL_METHOD_4         4  ''
              522  STORE_FAST               'ret'
              524  POP_BLOCK        
              526  JUMP_FORWARD        616  'to 616'
            528_0  COME_FROM_FINALLY   502  '502'

 L. 501       528  DUP_TOP          
              530  LOAD_GLOBAL              pythoncom
              532  LOAD_ATTR                com_error
          534_536  <121>               614  ''
              538  POP_TOP          
              540  STORE_FAST               'details'
              542  POP_TOP          
              544  SETUP_FINALLY       606  'to 606'

 L. 502       546  LOAD_FAST                'details'
              548  LOAD_ATTR                hresult
              550  LOAD_GLOBAL              ERRORS_BAD_CONTEXT
              552  <118>                 0  ''
          554_556  POP_JUMP_IF_FALSE   592  'to 592'

 L. 504       558  LOAD_FAST                'retEntry'
              560  LOAD_FAST                'self'
              562  LOAD_ATTR                _olerepr_
              564  LOAD_ATTR                mapFuncs
              566  LOAD_FAST                'attr'
              568  STORE_SUBSCR     

 L. 505       570  LOAD_FAST                'self'
              572  LOAD_METHOD              _make_method_
              574  LOAD_FAST                'attr'
              576  CALL_METHOD_1         1  ''
              578  POP_BLOCK        
              580  ROT_FOUR         
              582  POP_EXCEPT       
              584  LOAD_CONST               None
              586  STORE_FAST               'details'
              588  DELETE_FAST              'details'
              590  RETURN_VALUE     
            592_0  COME_FROM           554  '554'

 L. 506       592  RAISE_VARARGS_0       0  'reraise'
              594  POP_BLOCK        
              596  POP_EXCEPT       
              598  LOAD_CONST               None
              600  STORE_FAST               'details'
              602  DELETE_FAST              'details'
              604  JUMP_FORWARD        616  'to 616'
            606_0  COME_FROM_FINALLY   544  '544'
              606  LOAD_CONST               None
              608  STORE_FAST               'details'
              610  DELETE_FAST              'details'
              612  <48>             
              614  <48>             
            616_0  COME_FROM           604  '604'
            616_1  COME_FROM           526  '526'

 L. 507       616  LOAD_GLOBAL              debug_attr_print
              618  LOAD_STR                 'OLE returned '
              620  LOAD_FAST                'ret'
              622  CALL_FUNCTION_2       2  ''
              624  POP_TOP          

 L. 508       626  LOAD_FAST                'self'
              628  LOAD_METHOD              _get_good_object_
              630  LOAD_FAST                'ret'
              632  CALL_METHOD_1         1  ''
              634  RETURN_VALUE     
            636_0  COME_FROM           472  '472'

 L. 511       636  LOAD_GLOBAL              AttributeError
              638  LOAD_STR                 '%s.%s'
              640  LOAD_FAST                'self'
              642  LOAD_ATTR                _username_
              644  LOAD_FAST                'attr'
              646  BUILD_TUPLE_2         2 
              648  BINARY_MODULO    
              650  CALL_FUNCTION_1       1  ''
              652  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<121>' instruction at offset 54

    def __setattr__--- This code section failed: ---

 L. 514         0  LOAD_FAST                'attr'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                __dict__
                6  <118>                 0  ''
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L. 517        10  LOAD_FAST                'value'
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                __dict__
               16  LOAD_FAST                'attr'
               18  STORE_SUBSCR     

 L. 518        20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM             8  '8'

 L. 520        24  LOAD_GLOBAL              debug_attr_print
               26  LOAD_STR                 'SetAttr called for %s.%s=%s on DispatchContainer'
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                _username_
               32  LOAD_FAST                'attr'
               34  LOAD_GLOBAL              repr
               36  LOAD_FAST                'value'
               38  CALL_FUNCTION_1       1  ''
               40  BUILD_TUPLE_3         3 
               42  BINARY_MODULO    
               44  CALL_FUNCTION_1       1  ''
               46  POP_TOP          

 L. 522        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _olerepr_
               52  POP_JUMP_IF_FALSE   178  'to 178'

 L. 524        54  LOAD_FAST                'attr'
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                _olerepr_
               60  LOAD_ATTR                propMap
               62  <118>                 0  ''
               64  POP_JUMP_IF_FALSE   116  'to 116'

 L. 525        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _olerepr_
               70  LOAD_ATTR                propMap
               72  LOAD_FAST                'attr'
               74  BINARY_SUBSCR    
               76  STORE_FAST               'entry'

 L. 526        78  LOAD_GLOBAL              _GetDescInvokeType
               80  LOAD_FAST                'entry'
               82  LOAD_GLOBAL              pythoncom
               84  LOAD_ATTR                INVOKE_PROPERTYPUT
               86  CALL_FUNCTION_2       2  ''
               88  STORE_FAST               'invoke_type'

 L. 527        90  LOAD_FAST                'self'
               92  LOAD_ATTR                _oleobj_
               94  LOAD_METHOD              Invoke
               96  LOAD_FAST                'entry'
               98  LOAD_ATTR                dispid
              100  LOAD_CONST               0
              102  LOAD_FAST                'invoke_type'
              104  LOAD_CONST               0
              106  LOAD_FAST                'value'
              108  CALL_METHOD_5         5  ''
              110  POP_TOP          

 L. 528       112  LOAD_CONST               None
              114  RETURN_VALUE     
            116_0  COME_FROM            64  '64'

 L. 530       116  LOAD_FAST                'attr'
              118  LOAD_FAST                'self'
              120  LOAD_ATTR                _olerepr_
              122  LOAD_ATTR                propMapPut
              124  <118>                 0  ''
              126  POP_JUMP_IF_FALSE   178  'to 178'

 L. 531       128  LOAD_FAST                'self'
              130  LOAD_ATTR                _olerepr_
              132  LOAD_ATTR                propMapPut
              134  LOAD_FAST                'attr'
              136  BINARY_SUBSCR    
              138  STORE_FAST               'entry'

 L. 532       140  LOAD_GLOBAL              _GetDescInvokeType
              142  LOAD_FAST                'entry'
              144  LOAD_GLOBAL              pythoncom
              146  LOAD_ATTR                INVOKE_PROPERTYPUT
              148  CALL_FUNCTION_2       2  ''
              150  STORE_FAST               'invoke_type'

 L. 533       152  LOAD_FAST                'self'
              154  LOAD_ATTR                _oleobj_
              156  LOAD_METHOD              Invoke
              158  LOAD_FAST                'entry'
              160  LOAD_ATTR                dispid
              162  LOAD_CONST               0
              164  LOAD_FAST                'invoke_type'
              166  LOAD_CONST               0
              168  LOAD_FAST                'value'
              170  CALL_METHOD_5         5  ''
              172  POP_TOP          

 L. 534       174  LOAD_CONST               None
              176  RETURN_VALUE     
            178_0  COME_FROM           126  '126'
            178_1  COME_FROM            52  '52'

 L. 537       178  LOAD_FAST                'self'
              180  LOAD_ATTR                _oleobj_
          182_184  POP_JUMP_IF_FALSE   486  'to 486'

 L. 538       186  LOAD_FAST                'self'
              188  LOAD_METHOD              __LazyMap__
              190  LOAD_FAST                'attr'
              192  CALL_METHOD_1         1  ''
          194_196  POP_JUMP_IF_FALSE   326  'to 326'

 L. 540       198  LOAD_FAST                'attr'
              200  LOAD_FAST                'self'
              202  LOAD_ATTR                _olerepr_
              204  LOAD_ATTR                propMap
              206  <118>                 0  ''
          208_210  POP_JUMP_IF_FALSE   262  'to 262'

 L. 541       212  LOAD_FAST                'self'
              214  LOAD_ATTR                _olerepr_
              216  LOAD_ATTR                propMap
              218  LOAD_FAST                'attr'
              220  BINARY_SUBSCR    
              222  STORE_FAST               'entry'

 L. 542       224  LOAD_GLOBAL              _GetDescInvokeType
              226  LOAD_FAST                'entry'
              228  LOAD_GLOBAL              pythoncom
              230  LOAD_ATTR                INVOKE_PROPERTYPUT
              232  CALL_FUNCTION_2       2  ''
              234  STORE_FAST               'invoke_type'

 L. 543       236  LOAD_FAST                'self'
              238  LOAD_ATTR                _oleobj_
              240  LOAD_METHOD              Invoke
              242  LOAD_FAST                'entry'
              244  LOAD_ATTR                dispid
              246  LOAD_CONST               0
              248  LOAD_FAST                'invoke_type'
              250  LOAD_CONST               0
              252  LOAD_FAST                'value'
              254  CALL_METHOD_5         5  ''
              256  POP_TOP          

 L. 544       258  LOAD_CONST               None
              260  RETURN_VALUE     
            262_0  COME_FROM           208  '208'

 L. 546       262  LOAD_FAST                'attr'
              264  LOAD_FAST                'self'
              266  LOAD_ATTR                _olerepr_
              268  LOAD_ATTR                propMapPut
              270  <118>                 0  ''
          272_274  POP_JUMP_IF_FALSE   326  'to 326'

 L. 547       276  LOAD_FAST                'self'
              278  LOAD_ATTR                _olerepr_
              280  LOAD_ATTR                propMapPut
              282  LOAD_FAST                'attr'
              284  BINARY_SUBSCR    
              286  STORE_FAST               'entry'

 L. 548       288  LOAD_GLOBAL              _GetDescInvokeType
              290  LOAD_FAST                'entry'
              292  LOAD_GLOBAL              pythoncom
              294  LOAD_ATTR                INVOKE_PROPERTYPUT
              296  CALL_FUNCTION_2       2  ''
              298  STORE_FAST               'invoke_type'

 L. 549       300  LOAD_FAST                'self'
              302  LOAD_ATTR                _oleobj_
              304  LOAD_METHOD              Invoke
              306  LOAD_FAST                'entry'
              308  LOAD_ATTR                dispid
              310  LOAD_CONST               0
              312  LOAD_FAST                'invoke_type'
              314  LOAD_CONST               0
              316  LOAD_FAST                'value'
              318  CALL_METHOD_5         5  ''
              320  POP_TOP          

 L. 550       322  LOAD_CONST               None
              324  RETURN_VALUE     
            326_0  COME_FROM           272  '272'
            326_1  COME_FROM           194  '194'

 L. 551       326  SETUP_FINALLY       352  'to 352'

 L. 552       328  LOAD_GLOBAL              build
              330  LOAD_METHOD              MapEntry
              332  LOAD_FAST                'self'
              334  LOAD_METHOD              __AttrToID__
              336  LOAD_FAST                'attr'
              338  CALL_METHOD_1         1  ''
              340  LOAD_FAST                'attr'
              342  BUILD_TUPLE_1         1 
              344  CALL_METHOD_2         2  ''
              346  STORE_FAST               'entry'
              348  POP_BLOCK        
              350  JUMP_FORWARD        378  'to 378'
            352_0  COME_FROM_FINALLY   326  '326'

 L. 553       352  DUP_TOP          
              354  LOAD_GLOBAL              pythoncom
              356  LOAD_ATTR                com_error
          358_360  <121>               376  ''
              362  POP_TOP          
              364  POP_TOP          
              366  POP_TOP          

 L. 555       368  LOAD_CONST               None
              370  STORE_FAST               'entry'
              372  POP_EXCEPT       
              374  JUMP_FORWARD        378  'to 378'
              376  <48>             
            378_0  COME_FROM           374  '374'
            378_1  COME_FROM           350  '350'

 L. 556       378  LOAD_FAST                'entry'
              380  LOAD_CONST               None
              382  <117>                 1  ''
          384_386  POP_JUMP_IF_FALSE   486  'to 486'

 L. 557       388  SETUP_FINALLY       464  'to 464'

 L. 558       390  LOAD_GLOBAL              _GetDescInvokeType
              392  LOAD_FAST                'entry'
              394  LOAD_GLOBAL              pythoncom
              396  LOAD_ATTR                INVOKE_PROPERTYPUT
              398  CALL_FUNCTION_2       2  ''
              400  STORE_FAST               'invoke_type'

 L. 559       402  LOAD_FAST                'self'
              404  LOAD_ATTR                _oleobj_
              406  LOAD_METHOD              Invoke
              408  LOAD_FAST                'entry'
              410  LOAD_ATTR                dispid
              412  LOAD_CONST               0
              414  LOAD_FAST                'invoke_type'
              416  LOAD_CONST               0
              418  LOAD_FAST                'value'
              420  CALL_METHOD_5         5  ''
              422  POP_TOP          

 L. 560       424  LOAD_FAST                'entry'
              426  LOAD_FAST                'self'
              428  LOAD_ATTR                _olerepr_
              430  LOAD_ATTR                propMap
              432  LOAD_FAST                'attr'
              434  STORE_SUBSCR     

 L. 561       436  LOAD_GLOBAL              debug_attr_print
              438  LOAD_STR                 '__setattr__ property %s (id=0x%x) in Dispatch container %s'
              440  LOAD_FAST                'attr'
              442  LOAD_FAST                'entry'
              444  LOAD_ATTR                dispid
              446  LOAD_FAST                'self'
              448  LOAD_ATTR                _username_
              450  BUILD_TUPLE_3         3 
              452  BINARY_MODULO    
              454  CALL_FUNCTION_1       1  ''
              456  POP_TOP          

 L. 562       458  POP_BLOCK        
              460  LOAD_CONST               None
              462  RETURN_VALUE     
            464_0  COME_FROM_FINALLY   388  '388'

 L. 563       464  DUP_TOP          
              466  LOAD_GLOBAL              pythoncom
              468  LOAD_ATTR                com_error
          470_472  <121>               484  ''
              474  POP_TOP          
              476  POP_TOP          
              478  POP_TOP          

 L. 564       480  POP_EXCEPT       
              482  JUMP_FORWARD        486  'to 486'
              484  <48>             
            486_0  COME_FROM           482  '482'
            486_1  COME_FROM           384  '384'
            486_2  COME_FROM           182  '182'

 L. 565       486  LOAD_GLOBAL              AttributeError
              488  LOAD_STR                 "Property '%s.%s' can not be set."
              490  LOAD_FAST                'self'
              492  LOAD_ATTR                _username_
              494  LOAD_FAST                'attr'
              496  BUILD_TUPLE_2         2 
              498  BINARY_MODULO    
              500  CALL_FUNCTION_1       1  ''
              502  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `None' instruction at offset -1