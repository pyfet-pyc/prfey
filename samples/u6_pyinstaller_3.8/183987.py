# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\win32com\client\dynamic.py
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


py3k = sys.version_info > (3, 0)
if py3k:

    def MakeMethod(func, inst, cls):
        return types.MethodType(func, inst)


else:
    MakeMethod = types.MethodType
PyIDispatchType = pythoncom.TypeIIDs[pythoncom.IID_IDispatch]
PyIUnknownType = pythoncom.TypeIIDs[pythoncom.IID_IUnknown]
if py3k:
    _GoodDispatchTypes = (
     str, IIDType)
else:
    _GoodDispatchTypes = (
     str, IIDType, str)
_defaultDispatchItem = build.DispatchItem

def _GetGoodDispatch(IDispatch, clsctx=pythoncom.CLSCTX_SERVER):
    if isinstance(IDispatch, PyIDispatchType):
        return IDispatch
    elif isinstance(IDispatch, _GoodDispatchTypes):
        try:
            IDispatch = pythoncom.connect(IDispatch)
        except pythoncom.ole_error:
            IDispatch = pythoncom.CoCreateInstance(IDispatch, None, clsctx, pythoncom.IID_IDispatch)

    else:
        IDispatch = getattr(IDispatch, '_oleobj_', IDispatch)
    return IDispatch


def _GetGoodDispatchAndUserName(IDispatch, userName, clsctx):
    if userName is None:
        if isinstance(IDispatch, str):
            userName = IDispatch
        elif not py3k:
            if isinstance(IDispatch, str):
                userName = IDispatch.encode('ascii', 'replace')
    elif (py3k or isinstance)(userName, str):
        userName = userName.encode('ascii', 'replace')
    else:
        userName = str(userName)
    return (
     _GetGoodDispatch(IDispatch, clsctx), userName)


def _GetDescInvokeType(entry, invoke_type):
    return entry and entry.desc or invoke_type
    varkind = entry.desc[4]
    if varkind == pythoncom.VAR_DISPATCH:
        if invoke_type == pythoncom.INVOKE_PROPERTYGET:
            return pythoncom.INVOKE_FUNC | invoke_type
    return varkind


def Dispatch(IDispatch, userName=None, createClass=None, typeinfo=None, UnicodeToString=None, clsctx=pythoncom.CLSCTX_SERVER):
    assert UnicodeToString is None, 'this is deprecated and will go away'
    IDispatch, userName = _GetGoodDispatchAndUserName(IDispatch, userName, clsctx)
    if createClass is None:
        createClass = CDispatch
    lazydata = None
    try:
        if typeinfo is None:
            typeinfo = IDispatch.GetTypeInfo()
        if typeinfo is not None:
            try:
                typecomp = typeinfo.GetTypeComp()
                lazydata = (typeinfo, typecomp)
            except pythoncom.com_error:
                pass

    except pythoncom.com_error:
        typeinfo = None
    else:
        olerepr = MakeOleRepr(IDispatch, typeinfo, lazydata)
        return createClass(IDispatch, olerepr, userName, lazydata=lazydata)


def MakeOleRepr(IDispatch, typeinfo, typecomp):
    olerepr = None
    if typeinfo is not None:
        try:
            attr = typeinfo.GetTypeAttr()
            if attr[5] == pythoncom.TKIND_INTERFACE:
                if attr[11] & pythoncom.TYPEFLAG_FDUAL:
                    href = typeinfo.GetRefTypeOfImplType(-1)
                    typeinfo = typeinfo.GetRefTypeInfo(href)
                    attr = typeinfo.GetTypeAttr()
            elif typecomp is None:
                olerepr = build.DispatchItem(typeinfo, attr, None, 0)
            else:
                olerepr = build.LazyDispatchItem(attr, None)
        except pythoncom.ole_error:
            pass

    if olerepr is None:
        olerepr = build.DispatchItem()
    return olerepr


def DumbDispatch(IDispatch, userName=None, createClass=None, UnicodeToString=None, clsctx=pythoncom.CLSCTX_SERVER):
    """Dispatch with no type info"""
    assert UnicodeToString is None, 'this is deprecated and will go away'
    IDispatch, userName = _GetGoodDispatchAndUserName(IDispatch, userName, clsctx)
    if createClass is None:
        createClass = CDispatch
    return createClass(IDispatch, build.DispatchItem(), userName)


class CDispatch:

    def __init__(self, IDispatch, olerepr, userName=None, UnicodeToString=None, lazydata=None):
        assert UnicodeToString is None, 'this is deprecated and will go away'
        if userName is None:
            userName = '<unknown>'
        self.__dict__['_oleobj_'] = IDispatch
        self.__dict__['_username_'] = userName
        self.__dict__['_olerepr_'] = olerepr
        self.__dict__['_mapCachedItems_'] = {}
        self.__dict__['_builtMethods_'] = {}
        self.__dict__['_enum_'] = None
        self.__dict__['_unicode_to_string_'] = None
        self.__dict__['_lazydata_'] = lazydata

    def __call__(self, *args):
        """Provide 'default dispatch' COM functionality - allow instance to be called"""
        if self._olerepr_.defaultDispatchName:
            invkind, dispid = self._find_dispatch_type_(self._olerepr_.defaultDispatchName)
        else:
            invkind, dispid = pythoncom.DISPATCH_METHOD | pythoncom.DISPATCH_PROPERTYGET, pythoncom.DISPID_VALUE
        if invkind is not None:
            allArgs = (
             dispid, LCID, invkind, 1) + args
            return self._get_good_object_((self._oleobj_.Invoke)(*allArgs), self._olerepr_.defaultDispatchName, None)
        raise TypeError('This dispatch object does not define a default method')

    def __bool__(self):
        return True

    def __repr__(self):
        return '<COMObject %s>' % self._username_

    def __str__--- This code section failed: ---

 L. 211         0  SETUP_FINALLY        16  'to 16'

 L. 212         2  LOAD_GLOBAL              str
                4  LOAD_FAST                'self'
                6  LOAD_METHOD              __call__
                8  CALL_METHOD_0         0  ''
               10  CALL_FUNCTION_1       1  ''
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 213        16  DUP_TOP          
               18  LOAD_GLOBAL              pythoncom
               20  LOAD_ATTR                com_error
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    74  'to 74'
               26  POP_TOP          
               28  STORE_FAST               'details'
               30  POP_TOP          
               32  SETUP_FINALLY        62  'to 62'

 L. 214        34  LOAD_FAST                'details'
               36  LOAD_ATTR                hresult
               38  LOAD_GLOBAL              ERRORS_BAD_CONTEXT
               40  COMPARE_OP               not-in
               42  POP_JUMP_IF_FALSE    46  'to 46'

 L. 215        44  RAISE_VARARGS_0       0  'reraise'
             46_0  COME_FROM            42  '42'

 L. 216        46  LOAD_FAST                'self'
               48  LOAD_METHOD              __repr__
               50  CALL_METHOD_0         0  ''
               52  ROT_FOUR         
               54  POP_BLOCK        
               56  POP_EXCEPT       
               58  CALL_FINALLY         62  'to 62'
               60  RETURN_VALUE     
             62_0  COME_FROM            58  '58'
             62_1  COME_FROM_FINALLY    32  '32'
               62  LOAD_CONST               None
               64  STORE_FAST               'details'
               66  DELETE_FAST              'details'
               68  END_FINALLY      
               70  POP_EXCEPT       
               72  JUMP_FORWARD         76  'to 76'
             74_0  COME_FROM            24  '24'
               74  END_FINALLY      
             76_0  COME_FROM            72  '72'

Parse error at or near `POP_BLOCK' instruction at offset 54

    def __eq__(self, other):
        other = getattr(other, '_oleobj_', other)
        return self._oleobj_ == other

    def __ne__(self, other):
        other = getattr(other, '_oleobj_', other)
        return self._oleobj_ != other

    def __int__(self):
        return int(self.__call__())

    def __len__(self):
        invkind, dispid = self._find_dispatch_type_('Count')
        if invkind:
            return self._oleobj_.Invoke(dispid, LCID, invkind, 1)
        raise TypeError('This dispatch object does not define a Count method')

    def _NewEnum(self):
        try:
            invkind = pythoncom.DISPATCH_METHOD | pythoncom.DISPATCH_PROPERTYGET
            enum = self._oleobj_.InvokeTypes(pythoncom.DISPID_NEWENUM, LCID, invkind, (13,
                                                                                       10), ())
        except pythoncom.com_error:
            return
        else:
            from . import util
            return util.WrapEnum(enum, None)

    def __getitem__(self, index):
        if isinstance(index, int):
            if self.__dict__['_enum_'] is None:
                self.__dict__['_enum_'] = self._NewEnum()
            if self.__dict__['_enum_'] is not None:
                return self._get_good_object_(self._enum_.__getitem__(index))
        invkind, dispid = self._find_dispatch_type_('Item')
        if invkind is not None:
            return self._get_good_object_(self._oleobj_.Invoke(dispid, LCID, invkind, 1, index))
        raise TypeError('This object does not support enumeration')

    def __setitem__(self, index, *args):
        if self._olerepr_.defaultDispatchName:
            invkind, dispid = self._find_dispatch_type_(self._olerepr_.defaultDispatchName)
        else:
            invkind, dispid = pythoncom.DISPATCH_PROPERTYPUT | pythoncom.DISPATCH_PROPERTYPUTREF, pythoncom.DISPID_VALUE
        if invkind is not None:
            allArgs = (
             dispid, LCID, invkind, 0, index) + args
            return self._get_good_object_((self._oleobj_.Invoke)(*allArgs), self._olerepr_.defaultDispatchName, None)
        raise TypeError('This dispatch object does not define a default method')

    def _find_dispatch_type_--- This code section failed: ---

 L. 272         0  LOAD_FAST                'methodName'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _olerepr_
                6  LOAD_ATTR                mapFuncs
                8  COMPARE_OP               in
               10  POP_JUMP_IF_FALSE    40  'to 40'

 L. 273        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _olerepr_
               16  LOAD_ATTR                mapFuncs
               18  LOAD_FAST                'methodName'
               20  BINARY_SUBSCR    
               22  STORE_FAST               'item'

 L. 274        24  LOAD_FAST                'item'
               26  LOAD_ATTR                desc
               28  LOAD_CONST               4
               30  BINARY_SUBSCR    
               32  LOAD_FAST                'item'
               34  LOAD_ATTR                dispid
               36  BUILD_TUPLE_2         2 
               38  RETURN_VALUE     
             40_0  COME_FROM            10  '10'

 L. 276        40  LOAD_FAST                'methodName'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                _olerepr_
               46  LOAD_ATTR                propMapGet
               48  COMPARE_OP               in
               50  POP_JUMP_IF_FALSE    80  'to 80'

 L. 277        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _olerepr_
               56  LOAD_ATTR                propMapGet
               58  LOAD_FAST                'methodName'
               60  BINARY_SUBSCR    
               62  STORE_FAST               'item'

 L. 278        64  LOAD_FAST                'item'
               66  LOAD_ATTR                desc
               68  LOAD_CONST               4
               70  BINARY_SUBSCR    
               72  LOAD_FAST                'item'
               74  LOAD_ATTR                dispid
               76  BUILD_TUPLE_2         2 
               78  RETURN_VALUE     
             80_0  COME_FROM            50  '50'

 L. 280        80  SETUP_FINALLY       100  'to 100'

 L. 281        82  LOAD_FAST                'self'
               84  LOAD_ATTR                _oleobj_
               86  LOAD_METHOD              GetIDsOfNames
               88  LOAD_CONST               0
               90  LOAD_FAST                'methodName'
               92  CALL_METHOD_2         2  ''
               94  STORE_FAST               'dispid'
               96  POP_BLOCK        
               98  JUMP_FORWARD        114  'to 114'
            100_0  COME_FROM_FINALLY    80  '80'

 L. 282       100  POP_TOP          
              102  POP_TOP          
              104  POP_TOP          

 L. 283       106  POP_EXCEPT       
              108  LOAD_CONST               (None, None)
              110  RETURN_VALUE     
              112  END_FINALLY      
            114_0  COME_FROM            98  '98'

 L. 284       114  LOAD_GLOBAL              pythoncom
              116  LOAD_ATTR                DISPATCH_METHOD
              118  LOAD_GLOBAL              pythoncom
              120  LOAD_ATTR                DISPATCH_PROPERTYGET
              122  BINARY_OR        
              124  LOAD_FAST                'dispid'
              126  BUILD_TUPLE_2         2 
              128  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 108

    def _ApplyTypes_(self, dispid, wFlags, retType, argTypes, user, resultCLSID, *args):
        result = (self._oleobj_.InvokeTypes)(*(dispid, LCID, wFlags, retType, argTypes) + args)
        return self._get_good_object_(result, user, resultCLSID)

    def _wrap_dispatch_(self, ob, userName=None, returnCLSID=None, UnicodeToString=None):
        assert UnicodeToString is None, 'this is deprecated and will go away'
        return Dispatch(ob, userName)

    def _get_good_single_object_(self, ob, userName=None, ReturnCLSID=None):
        if isinstance(ob, PyIDispatchType):
            return self._wrap_dispatch_(ob, userName, ReturnCLSID)
        if isinstance(ob, PyIUnknownType):
            try:
                ob = ob.QueryInterface(pythoncom.IID_IDispatch)
            except pythoncom.com_error:
                return ob
            else:
                return self._wrap_dispatch_(ob, userName, ReturnCLSID)
        return ob

    def _get_good_object_(self, ob, userName=None, ReturnCLSID=None):
        """Given an object (usually the retval from a method), make it a good object to return.
                   Basically checks if it is a COM object, and wraps it up.
                   Also handles the fact that a retval may be a tuple of retvals"""
        if ob is None:
            return
        if isinstance(ob, tuple):
            return tuple(map(lambda o, s=self, oun=userName, rc=ReturnCLSID: s._get_good_single_object_(o, oun, rc), ob))
        return self._get_good_single_object_(ob)

    def _make_method_--- This code section failed: ---

 L. 321         0  LOAD_GLOBAL              build
                2  LOAD_METHOD              MakePublicAttributeName
                4  LOAD_FAST                'name'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'methodName'

 L. 322        10  LOAD_FAST                'self'
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

 L. 323        34  LOAD_STR                 '\n'
               36  LOAD_METHOD              join
               38  LOAD_FAST                'methodCodeList'
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'methodCode'

 L. 324        44  SETUP_FINALLY       144  'to 144'

 L. 327        46  LOAD_GLOBAL              compile
               48  LOAD_FAST                'methodCode'
               50  LOAD_STR                 '<COMObject %s>'
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                _username_
               56  BINARY_MODULO    
               58  LOAD_STR                 'exec'
               60  CALL_FUNCTION_3       3  ''
               62  STORE_FAST               'codeObject'

 L. 329        64  BUILD_MAP_0           0 
               66  STORE_FAST               'tempNameSpace'

 L. 331        68  LOAD_GLOBAL              globals
               70  CALL_FUNCTION_0       0  ''
               72  LOAD_METHOD              copy
               74  CALL_METHOD_0         0  ''
               76  STORE_FAST               'globNameSpace'

 L. 332        78  LOAD_GLOBAL              win32com
               80  LOAD_ATTR                client
               82  LOAD_ATTR                Dispatch
               84  LOAD_FAST                'globNameSpace'
               86  LOAD_STR                 'Dispatch'
               88  STORE_SUBSCR     

 L. 333        90  LOAD_GLOBAL              exec
               92  LOAD_FAST                'codeObject'
               94  LOAD_FAST                'globNameSpace'
               96  LOAD_FAST                'tempNameSpace'
               98  CALL_FUNCTION_3       3  ''
              100  POP_TOP          

 L. 334       102  LOAD_FAST                'methodName'
              104  STORE_FAST               'name'

 L. 336       106  LOAD_FAST                'tempNameSpace'
              108  LOAD_FAST                'name'
              110  BINARY_SUBSCR    
              112  DUP_TOP          
              114  STORE_FAST               'fn'
              116  LOAD_FAST                'self'
              118  LOAD_ATTR                _builtMethods_
              120  LOAD_FAST                'name'
              122  STORE_SUBSCR     

 L. 337       124  LOAD_GLOBAL              MakeMethod
              126  LOAD_FAST                'fn'
              128  LOAD_FAST                'self'
              130  LOAD_FAST                'self'
              132  LOAD_ATTR                __class__
              134  CALL_FUNCTION_3       3  ''
              136  STORE_FAST               'newMeth'

 L. 338       138  LOAD_FAST                'newMeth'
              140  POP_BLOCK        
              142  RETURN_VALUE     
            144_0  COME_FROM_FINALLY    44  '44'

 L. 339       144  POP_TOP          
              146  POP_TOP          
              148  POP_TOP          

 L. 340       150  LOAD_GLOBAL              debug_print
              152  LOAD_STR                 'Error building OLE definition for code '
              154  LOAD_FAST                'methodCode'
              156  CALL_FUNCTION_2       2  ''
              158  POP_TOP          

 L. 341       160  LOAD_GLOBAL              traceback
              162  LOAD_METHOD              print_exc
              164  CALL_METHOD_0         0  ''
              166  POP_TOP          
              168  POP_EXCEPT       
              170  JUMP_FORWARD        174  'to 174'
              172  END_FINALLY      
            174_0  COME_FROM           170  '170'

Parse error at or near `POP_TOP' instruction at offset 158

    def _Release_(self):
        """Cleanup object - like a close - to force cleanup when you dont 
                   want to rely on Python's reference counting."""
        for childCont in self._mapCachedItems_.values():
            childCont._Release_()
        else:
            self._mapCachedItems_ = {}
            if self._oleobj_:
                self._oleobj_.Release()
                self.__dict__['_oleobj_'] = None
            if self._olerepr_:
                self.__dict__['_olerepr_'] = None
            self._enum_ = None

    def _proc_--- This code section failed: ---

 L. 360         0  SETUP_FINALLY        58  'to 58'

 L. 361         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _olerepr_
                6  LOAD_ATTR                mapFuncs
                8  LOAD_FAST                'name'
               10  BINARY_SUBSCR    
               12  STORE_FAST               'item'

 L. 362        14  LOAD_FAST                'item'
               16  LOAD_ATTR                dispid
               18  STORE_FAST               'dispId'

 L. 363        20  LOAD_FAST                'self'
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

 L. 364        58  DUP_TOP          
               60  LOAD_GLOBAL              KeyError
               62  COMPARE_OP               exception-match
               64  POP_JUMP_IF_FALSE    84  'to 84'
               66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          

 L. 365        72  LOAD_GLOBAL              AttributeError
               74  LOAD_FAST                'name'
               76  CALL_FUNCTION_1       1  ''
               78  RAISE_VARARGS_1       1  'exception instance'
               80  POP_EXCEPT       
               82  JUMP_FORWARD         86  'to 86'
             84_0  COME_FROM            64  '64'
               84  END_FINALLY      
             86_0  COME_FROM            82  '82'

Parse error at or near `POP_TOP' instruction at offset 68

    def _print_details_(self):
        """Debug routine - dumps what it knows about an object."""
        print('AxDispatch container', self._username_)
        try:
            print('Methods:')
            for method in self._olerepr_.mapFuncs.keys():
                print('\t', method)
            else:
                print('Props:')
                for prop, entry in self._olerepr_.propMap.items():
                    print('\t%s = 0x%x - %s' % (prop, entry.dispid, repr(entry)))
                else:
                    print('Get Props:')
                    for prop, entry in self._olerepr_.propMapGet.items():
                        print('\t%s = 0x%x - %s' % (prop, entry.dispid, repr(entry)))
                    else:
                        print('Put Props:')
                        for prop, entry in self._olerepr_.propMapPut.items():
                            print('\t%s = 0x%x - %s' % (prop, entry.dispid, repr(entry)))

        except:
            traceback.print_exc()

    def __LazyMap__--- This code section failed: ---

 L. 387         0  SETUP_FINALLY        40  'to 40'

 L. 388         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _LazyAddAttr_
                6  LOAD_FAST                'attr'
                8  CALL_METHOD_1         1  ''
               10  POP_JUMP_IF_FALSE    36  'to 36'

 L. 389        12  LOAD_GLOBAL              debug_attr_print
               14  LOAD_STR                 '%s.__LazyMap__(%s) added something'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _username_
               20  LOAD_FAST                'attr'
               22  BUILD_TUPLE_2         2 
               24  BINARY_MODULO    
               26  CALL_FUNCTION_1       1  ''
               28  POP_TOP          

 L. 390        30  POP_BLOCK        
               32  LOAD_CONST               1
               34  RETURN_VALUE     
             36_0  COME_FROM            10  '10'
               36  POP_BLOCK        
               38  JUMP_FORWARD         62  'to 62'
             40_0  COME_FROM_FINALLY     0  '0'

 L. 391        40  DUP_TOP          
               42  LOAD_GLOBAL              AttributeError
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE    60  'to 60'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 392        54  POP_EXCEPT       
               56  LOAD_CONST               0
               58  RETURN_VALUE     
             60_0  COME_FROM            46  '46'
               60  END_FINALLY      
             62_0  COME_FROM            38  '38'

Parse error at or near `LOAD_CONST' instruction at offset 32

    def _LazyAddAttr_(self, attr):
        if self._lazydata_ is None:
            return 0
        res = 0
        typeinfo, typecomp = self._lazydata_
        olerepr = self._olerepr_
        for i in ALL_INVOKE_TYPES:
            try:
                x, t = typecomp.Bind(attr, i)
                if x == 0:
                    if attr[:3] in ('Set', 'Get'):
                        x, t = typecomp.Bind(attr[3:], i)
                elif x == 1:
                    r = olerepr._AddFunc_(typeinfo, t, 0)
                else:
                    if x == 2:
                        r = olerepr._AddVar_(typeinfo, t, 0)
                    else:
                        r = None
                if r is not None:
                    key, map = r[0], r[1]
                    item = map[key]
                    if map == olerepr.propMapPut:
                        olerepr._propMapPutCheck_(key, item)
                    else:
                        if map == olerepr.propMapGet:
                            olerepr._propMapGetCheck_(key, item)
                    res = 1
            except:
                pass

        else:
            return res

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
            details = build.MapEntry(self.__AttrToID__(name), (name,))
            self._olerepr_.mapFuncs[name] = details

    def __AttrToID__(self, attr):
        debug_attr_print('Calling GetIDsOfNames for property %s in Dispatch container %s' % (attr, self._username_))
        return self._oleobj_.GetIDsOfNames(0, attr)

    def __getattr__--- This code section failed: ---

 L. 450         0  LOAD_FAST                'attr'
                2  LOAD_STR                 '__iter__'
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE   100  'to 100'

 L. 453         8  SETUP_FINALLY        48  'to 48'

 L. 454        10  LOAD_GLOBAL              pythoncom
               12  LOAD_ATTR                DISPATCH_METHOD
               14  LOAD_GLOBAL              pythoncom
               16  LOAD_ATTR                DISPATCH_PROPERTYGET
               18  BINARY_OR        
               20  STORE_FAST               'invkind'

 L. 455        22  LOAD_FAST                'self'
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
               46  JUMP_FORWARD         78  'to 78'
             48_0  COME_FROM_FINALLY     8  '8'

 L. 456        48  DUP_TOP          
               50  LOAD_GLOBAL              pythoncom
               52  LOAD_ATTR                com_error
               54  COMPARE_OP               exception-match
               56  POP_JUMP_IF_FALSE    76  'to 76'
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L. 457        64  LOAD_GLOBAL              AttributeError
               66  LOAD_STR                 'This object can not function as an iterator'
               68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
               72  POP_EXCEPT       
               74  JUMP_FORWARD         78  'to 78'
             76_0  COME_FROM            56  '56'
               76  END_FINALLY      
             78_0  COME_FROM            74  '74'
             78_1  COME_FROM            46  '46'

 L. 459        78  LOAD_BUILD_CLASS 
               80  LOAD_CODE                <code_object Factory>
               82  LOAD_STR                 'Factory'
               84  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               86  LOAD_STR                 'Factory'
               88  CALL_FUNCTION_2       2  ''
               90  STORE_FAST               'Factory'

 L. 465        92  LOAD_FAST                'Factory'
               94  LOAD_FAST                'enum'
               96  CALL_FUNCTION_1       1  ''
               98  RETURN_VALUE     
            100_0  COME_FROM             6  '6'

 L. 467       100  LOAD_FAST                'attr'
              102  LOAD_METHOD              startswith
              104  LOAD_STR                 '_'
              106  CALL_METHOD_1         1  ''
              108  POP_JUMP_IF_FALSE   128  'to 128'
              110  LOAD_FAST                'attr'
              112  LOAD_METHOD              endswith
              114  LOAD_STR                 '_'
              116  CALL_METHOD_1         1  ''
              118  POP_JUMP_IF_FALSE   128  'to 128'

 L. 468       120  LOAD_GLOBAL              AttributeError
              122  LOAD_FAST                'attr'
              124  CALL_FUNCTION_1       1  ''
              126  RAISE_VARARGS_1       1  'exception instance'
            128_0  COME_FROM           118  '118'
            128_1  COME_FROM           108  '108'

 L. 470       128  SETUP_FINALLY       152  'to 152'

 L. 471       130  LOAD_GLOBAL              MakeMethod
              132  LOAD_FAST                'self'
              134  LOAD_ATTR                _builtMethods_
              136  LOAD_FAST                'attr'
              138  BINARY_SUBSCR    
              140  LOAD_FAST                'self'
              142  LOAD_FAST                'self'
              144  LOAD_ATTR                __class__
              146  CALL_FUNCTION_3       3  ''
              148  POP_BLOCK        
              150  RETURN_VALUE     
            152_0  COME_FROM_FINALLY   128  '128'

 L. 472       152  DUP_TOP          
              154  LOAD_GLOBAL              KeyError
              156  COMPARE_OP               exception-match
              158  POP_JUMP_IF_FALSE   170  'to 170'
              160  POP_TOP          
              162  POP_TOP          
              164  POP_TOP          

 L. 473       166  POP_EXCEPT       
              168  JUMP_FORWARD        172  'to 172'
            170_0  COME_FROM           158  '158'
              170  END_FINALLY      
            172_0  COME_FROM           168  '168'

 L. 480       172  LOAD_FAST                'attr'
              174  LOAD_FAST                'self'
              176  LOAD_ATTR                _olerepr_
              178  LOAD_ATTR                mapFuncs
              180  COMPARE_OP               in
              182  POP_JUMP_IF_FALSE   194  'to 194'

 L. 481       184  LOAD_FAST                'self'
              186  LOAD_METHOD              _make_method_
              188  LOAD_FAST                'attr'
              190  CALL_METHOD_1         1  ''
              192  RETURN_VALUE     
            194_0  COME_FROM           182  '182'

 L. 484       194  LOAD_CONST               None
              196  STORE_FAST               'retEntry'

 L. 485       198  LOAD_FAST                'self'
              200  LOAD_ATTR                _olerepr_
          202_204  POP_JUMP_IF_FALSE   396  'to 396'
              206  LOAD_FAST                'self'
              208  LOAD_ATTR                _oleobj_
          210_212  POP_JUMP_IF_FALSE   396  'to 396'

 L. 487       214  LOAD_FAST                'self'
              216  LOAD_ATTR                _olerepr_
              218  LOAD_ATTR                propMap
              220  LOAD_METHOD              get
              222  LOAD_FAST                'attr'
              224  CALL_METHOD_1         1  ''
              226  STORE_FAST               'retEntry'

 L. 488       228  LOAD_FAST                'retEntry'
              230  LOAD_CONST               None
              232  COMPARE_OP               is
              234  POP_JUMP_IF_FALSE   250  'to 250'

 L. 489       236  LOAD_FAST                'self'
              238  LOAD_ATTR                _olerepr_
              240  LOAD_ATTR                propMapGet
              242  LOAD_METHOD              get
              244  LOAD_FAST                'attr'
              246  CALL_METHOD_1         1  ''
              248  STORE_FAST               'retEntry'
            250_0  COME_FROM           234  '234'

 L. 491       250  LOAD_FAST                'retEntry'
              252  LOAD_CONST               None
              254  COMPARE_OP               is
          256_258  POP_JUMP_IF_FALSE   396  'to 396'

 L. 492       260  SETUP_FINALLY       372  'to 372'

 L. 493       262  LOAD_FAST                'self'
              264  LOAD_METHOD              __LazyMap__
              266  LOAD_FAST                'attr'
              268  CALL_METHOD_1         1  ''
          270_272  POP_JUMP_IF_FALSE   338  'to 338'

 L. 494       274  LOAD_FAST                'attr'
              276  LOAD_FAST                'self'
              278  LOAD_ATTR                _olerepr_
              280  LOAD_ATTR                mapFuncs
              282  COMPARE_OP               in
          284_286  POP_JUMP_IF_FALSE   300  'to 300'

 L. 494       288  LOAD_FAST                'self'
              290  LOAD_METHOD              _make_method_
              292  LOAD_FAST                'attr'
              294  CALL_METHOD_1         1  ''
              296  POP_BLOCK        
              298  RETURN_VALUE     
            300_0  COME_FROM           284  '284'

 L. 495       300  LOAD_FAST                'self'
              302  LOAD_ATTR                _olerepr_
              304  LOAD_ATTR                propMap
              306  LOAD_METHOD              get
              308  LOAD_FAST                'attr'
              310  CALL_METHOD_1         1  ''
              312  STORE_FAST               'retEntry'

 L. 496       314  LOAD_FAST                'retEntry'
              316  LOAD_CONST               None
              318  COMPARE_OP               is
          320_322  POP_JUMP_IF_FALSE   338  'to 338'

 L. 497       324  LOAD_FAST                'self'
              326  LOAD_ATTR                _olerepr_
              328  LOAD_ATTR                propMapGet
              330  LOAD_METHOD              get
              332  LOAD_FAST                'attr'
              334  CALL_METHOD_1         1  ''
              336  STORE_FAST               'retEntry'
            338_0  COME_FROM           320  '320'
            338_1  COME_FROM           270  '270'

 L. 498       338  LOAD_FAST                'retEntry'
              340  LOAD_CONST               None
              342  COMPARE_OP               is
          344_346  POP_JUMP_IF_FALSE   368  'to 368'

 L. 499       348  LOAD_GLOBAL              build
              350  LOAD_METHOD              MapEntry
              352  LOAD_FAST                'self'
              354  LOAD_METHOD              __AttrToID__
              356  LOAD_FAST                'attr'
              358  CALL_METHOD_1         1  ''
              360  LOAD_FAST                'attr'
              362  BUILD_TUPLE_1         1 
              364  CALL_METHOD_2         2  ''
              366  STORE_FAST               'retEntry'
            368_0  COME_FROM           344  '344'
              368  POP_BLOCK        
              370  JUMP_FORWARD        396  'to 396'
            372_0  COME_FROM_FINALLY   260  '260'

 L. 500       372  DUP_TOP          
              374  LOAD_GLOBAL              pythoncom
              376  LOAD_ATTR                ole_error
              378  COMPARE_OP               exception-match
          380_382  POP_JUMP_IF_FALSE   394  'to 394'
              384  POP_TOP          
              386  POP_TOP          
              388  POP_TOP          

 L. 501       390  POP_EXCEPT       
              392  JUMP_FORWARD        396  'to 396'
            394_0  COME_FROM           380  '380'
              394  END_FINALLY      
            396_0  COME_FROM           392  '392'
            396_1  COME_FROM           370  '370'
            396_2  COME_FROM           256  '256'
            396_3  COME_FROM           210  '210'
            396_4  COME_FROM           202  '202'

 L. 503       396  LOAD_FAST                'retEntry'
              398  LOAD_CONST               None
              400  COMPARE_OP               is-not
          402_404  POP_JUMP_IF_FALSE   474  'to 474'

 L. 504       406  SETUP_FINALLY       436  'to 436'

 L. 505       408  LOAD_FAST                'self'
              410  LOAD_ATTR                _mapCachedItems_
              412  LOAD_FAST                'retEntry'
              414  LOAD_ATTR                dispid
              416  BINARY_SUBSCR    
              418  STORE_FAST               'ret'

 L. 506       420  LOAD_GLOBAL              debug_attr_print
              422  LOAD_STR                 'Cached items has attribute!'
              424  LOAD_FAST                'ret'
              426  CALL_FUNCTION_2       2  ''
              428  POP_TOP          

 L. 507       430  LOAD_FAST                'ret'
              432  POP_BLOCK        
              434  RETURN_VALUE     
            436_0  COME_FROM_FINALLY   406  '406'

 L. 508       436  DUP_TOP          
              438  LOAD_GLOBAL              KeyError
              440  LOAD_GLOBAL              AttributeError
              442  BUILD_TUPLE_2         2 
              444  COMPARE_OP               exception-match
          446_448  POP_JUMP_IF_FALSE   472  'to 472'
              450  POP_TOP          
              452  POP_TOP          
              454  POP_TOP          

 L. 509       456  LOAD_GLOBAL              debug_attr_print
              458  LOAD_STR                 'Attribute %s not in cache'
              460  LOAD_FAST                'attr'
              462  BINARY_MODULO    
              464  CALL_FUNCTION_1       1  ''
              466  POP_TOP          
              468  POP_EXCEPT       
              470  JUMP_FORWARD        474  'to 474'
            472_0  COME_FROM           446  '446'
              472  END_FINALLY      
            474_0  COME_FROM           470  '470'
            474_1  COME_FROM           402  '402'

 L. 512       474  LOAD_FAST                'retEntry'
              476  LOAD_CONST               None
              478  COMPARE_OP               is-not
          480_482  POP_JUMP_IF_FALSE   638  'to 638'

 L. 513       484  LOAD_GLOBAL              _GetDescInvokeType
              486  LOAD_FAST                'retEntry'
              488  LOAD_GLOBAL              pythoncom
              490  LOAD_ATTR                INVOKE_PROPERTYGET
              492  CALL_FUNCTION_2       2  ''
              494  STORE_FAST               'invoke_type'

 L. 514       496  LOAD_GLOBAL              debug_attr_print
              498  LOAD_STR                 'Getting property Id 0x%x from OLE object'
              500  LOAD_FAST                'retEntry'
              502  LOAD_ATTR                dispid
              504  BINARY_MODULO    
              506  CALL_FUNCTION_1       1  ''
              508  POP_TOP          

 L. 515       510  SETUP_FINALLY       536  'to 536'

 L. 516       512  LOAD_FAST                'self'
              514  LOAD_ATTR                _oleobj_
              516  LOAD_METHOD              Invoke
              518  LOAD_FAST                'retEntry'
              520  LOAD_ATTR                dispid
              522  LOAD_CONST               0
              524  LOAD_FAST                'invoke_type'
              526  LOAD_CONST               1
              528  CALL_METHOD_4         4  ''
              530  STORE_FAST               'ret'
              532  POP_BLOCK        
              534  JUMP_FORWARD        618  'to 618'
            536_0  COME_FROM_FINALLY   510  '510'

 L. 517       536  DUP_TOP          
              538  LOAD_GLOBAL              pythoncom
              540  LOAD_ATTR                com_error
              542  COMPARE_OP               exception-match
          544_546  POP_JUMP_IF_FALSE   616  'to 616'
              548  POP_TOP          
              550  STORE_FAST               'details'
              552  POP_TOP          
              554  SETUP_FINALLY       604  'to 604'

 L. 518       556  LOAD_FAST                'details'
              558  LOAD_ATTR                hresult
              560  LOAD_GLOBAL              ERRORS_BAD_CONTEXT
              562  COMPARE_OP               in
          564_566  POP_JUMP_IF_FALSE   598  'to 598'

 L. 520       568  LOAD_FAST                'retEntry'
              570  LOAD_FAST                'self'
              572  LOAD_ATTR                _olerepr_
              574  LOAD_ATTR                mapFuncs
              576  LOAD_FAST                'attr'
              578  STORE_SUBSCR     

 L. 521       580  LOAD_FAST                'self'
              582  LOAD_METHOD              _make_method_
              584  LOAD_FAST                'attr'
              586  CALL_METHOD_1         1  ''
              588  ROT_FOUR         
              590  POP_BLOCK        
              592  POP_EXCEPT       
              594  CALL_FINALLY        604  'to 604'
              596  RETURN_VALUE     
            598_0  COME_FROM           564  '564'

 L. 522       598  RAISE_VARARGS_0       0  'reraise'
              600  POP_BLOCK        
              602  BEGIN_FINALLY    
            604_0  COME_FROM           594  '594'
            604_1  COME_FROM_FINALLY   554  '554'
              604  LOAD_CONST               None
              606  STORE_FAST               'details'
              608  DELETE_FAST              'details'
              610  END_FINALLY      
              612  POP_EXCEPT       
              614  JUMP_FORWARD        618  'to 618'
            616_0  COME_FROM           544  '544'
              616  END_FINALLY      
            618_0  COME_FROM           614  '614'
            618_1  COME_FROM           534  '534'

 L. 523       618  LOAD_GLOBAL              debug_attr_print
              620  LOAD_STR                 'OLE returned '
              622  LOAD_FAST                'ret'
              624  CALL_FUNCTION_2       2  ''
              626  POP_TOP          

 L. 524       628  LOAD_FAST                'self'
              630  LOAD_METHOD              _get_good_object_
              632  LOAD_FAST                'ret'
              634  CALL_METHOD_1         1  ''
              636  RETURN_VALUE     
            638_0  COME_FROM           480  '480'

 L. 527       638  LOAD_GLOBAL              AttributeError
              640  LOAD_STR                 '%s.%s'
              642  LOAD_FAST                'self'
              644  LOAD_ATTR                _username_
              646  LOAD_FAST                'attr'
              648  BUILD_TUPLE_2         2 
              650  BINARY_MODULO    
              652  CALL_FUNCTION_1       1  ''
              654  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `POP_TOP' instruction at offset 162

    def __setattr__--- This code section failed: ---

 L. 530         0  LOAD_FAST                'attr'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                __dict__
                6  COMPARE_OP               in
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L. 533        10  LOAD_FAST                'value'
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                __dict__
               16  LOAD_FAST                'attr'
               18  STORE_SUBSCR     

 L. 534        20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM             8  '8'

 L. 536        24  LOAD_GLOBAL              debug_attr_print
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

 L. 538        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _olerepr_
               52  POP_JUMP_IF_FALSE   178  'to 178'

 L. 540        54  LOAD_FAST                'attr'
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                _olerepr_
               60  LOAD_ATTR                propMap
               62  COMPARE_OP               in
               64  POP_JUMP_IF_FALSE   116  'to 116'

 L. 541        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _olerepr_
               70  LOAD_ATTR                propMap
               72  LOAD_FAST                'attr'
               74  BINARY_SUBSCR    
               76  STORE_FAST               'entry'

 L. 542        78  LOAD_GLOBAL              _GetDescInvokeType
               80  LOAD_FAST                'entry'
               82  LOAD_GLOBAL              pythoncom
               84  LOAD_ATTR                INVOKE_PROPERTYPUT
               86  CALL_FUNCTION_2       2  ''
               88  STORE_FAST               'invoke_type'

 L. 543        90  LOAD_FAST                'self'
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

 L. 544       112  LOAD_CONST               None
              114  RETURN_VALUE     
            116_0  COME_FROM            64  '64'

 L. 546       116  LOAD_FAST                'attr'
              118  LOAD_FAST                'self'
              120  LOAD_ATTR                _olerepr_
              122  LOAD_ATTR                propMapPut
              124  COMPARE_OP               in
              126  POP_JUMP_IF_FALSE   178  'to 178'

 L. 547       128  LOAD_FAST                'self'
              130  LOAD_ATTR                _olerepr_
              132  LOAD_ATTR                propMapPut
              134  LOAD_FAST                'attr'
              136  BINARY_SUBSCR    
              138  STORE_FAST               'entry'

 L. 548       140  LOAD_GLOBAL              _GetDescInvokeType
              142  LOAD_FAST                'entry'
              144  LOAD_GLOBAL              pythoncom
              146  LOAD_ATTR                INVOKE_PROPERTYPUT
              148  CALL_FUNCTION_2       2  ''
              150  STORE_FAST               'invoke_type'

 L. 549       152  LOAD_FAST                'self'
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

 L. 550       174  LOAD_CONST               None
              176  RETURN_VALUE     
            178_0  COME_FROM           126  '126'
            178_1  COME_FROM            52  '52'

 L. 553       178  LOAD_FAST                'self'
              180  LOAD_ATTR                _oleobj_
          182_184  POP_JUMP_IF_FALSE   490  'to 490'

 L. 554       186  LOAD_FAST                'self'
              188  LOAD_METHOD              __LazyMap__
              190  LOAD_FAST                'attr'
              192  CALL_METHOD_1         1  ''
          194_196  POP_JUMP_IF_FALSE   326  'to 326'

 L. 556       198  LOAD_FAST                'attr'
              200  LOAD_FAST                'self'
              202  LOAD_ATTR                _olerepr_
              204  LOAD_ATTR                propMap
              206  COMPARE_OP               in
          208_210  POP_JUMP_IF_FALSE   262  'to 262'

 L. 557       212  LOAD_FAST                'self'
              214  LOAD_ATTR                _olerepr_
              216  LOAD_ATTR                propMap
              218  LOAD_FAST                'attr'
              220  BINARY_SUBSCR    
              222  STORE_FAST               'entry'

 L. 558       224  LOAD_GLOBAL              _GetDescInvokeType
              226  LOAD_FAST                'entry'
              228  LOAD_GLOBAL              pythoncom
              230  LOAD_ATTR                INVOKE_PROPERTYPUT
              232  CALL_FUNCTION_2       2  ''
              234  STORE_FAST               'invoke_type'

 L. 559       236  LOAD_FAST                'self'
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

 L. 560       258  LOAD_CONST               None
              260  RETURN_VALUE     
            262_0  COME_FROM           208  '208'

 L. 562       262  LOAD_FAST                'attr'
              264  LOAD_FAST                'self'
              266  LOAD_ATTR                _olerepr_
              268  LOAD_ATTR                propMapPut
              270  COMPARE_OP               in
          272_274  POP_JUMP_IF_FALSE   326  'to 326'

 L. 563       276  LOAD_FAST                'self'
              278  LOAD_ATTR                _olerepr_
              280  LOAD_ATTR                propMapPut
              282  LOAD_FAST                'attr'
              284  BINARY_SUBSCR    
              286  STORE_FAST               'entry'

 L. 564       288  LOAD_GLOBAL              _GetDescInvokeType
              290  LOAD_FAST                'entry'
              292  LOAD_GLOBAL              pythoncom
              294  LOAD_ATTR                INVOKE_PROPERTYPUT
              296  CALL_FUNCTION_2       2  ''
              298  STORE_FAST               'invoke_type'

 L. 565       300  LOAD_FAST                'self'
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

 L. 566       322  LOAD_CONST               None
              324  RETURN_VALUE     
            326_0  COME_FROM           272  '272'
            326_1  COME_FROM           194  '194'

 L. 567       326  SETUP_FINALLY       352  'to 352'

 L. 568       328  LOAD_GLOBAL              build
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
              350  JUMP_FORWARD        380  'to 380'
            352_0  COME_FROM_FINALLY   326  '326'

 L. 569       352  DUP_TOP          
              354  LOAD_GLOBAL              pythoncom
              356  LOAD_ATTR                com_error
              358  COMPARE_OP               exception-match
          360_362  POP_JUMP_IF_FALSE   378  'to 378'
              364  POP_TOP          
              366  POP_TOP          
              368  POP_TOP          

 L. 571       370  LOAD_CONST               None
              372  STORE_FAST               'entry'
              374  POP_EXCEPT       
              376  JUMP_FORWARD        380  'to 380'
            378_0  COME_FROM           360  '360'
              378  END_FINALLY      
            380_0  COME_FROM           376  '376'
            380_1  COME_FROM           350  '350'

 L. 572       380  LOAD_FAST                'entry'
              382  LOAD_CONST               None
              384  COMPARE_OP               is-not
          386_388  POP_JUMP_IF_FALSE   490  'to 490'

 L. 573       390  SETUP_FINALLY       466  'to 466'

 L. 574       392  LOAD_GLOBAL              _GetDescInvokeType
              394  LOAD_FAST                'entry'
              396  LOAD_GLOBAL              pythoncom
              398  LOAD_ATTR                INVOKE_PROPERTYPUT
              400  CALL_FUNCTION_2       2  ''
              402  STORE_FAST               'invoke_type'

 L. 575       404  LOAD_FAST                'self'
              406  LOAD_ATTR                _oleobj_
              408  LOAD_METHOD              Invoke
              410  LOAD_FAST                'entry'
              412  LOAD_ATTR                dispid
              414  LOAD_CONST               0
              416  LOAD_FAST                'invoke_type'
              418  LOAD_CONST               0
              420  LOAD_FAST                'value'
              422  CALL_METHOD_5         5  ''
              424  POP_TOP          

 L. 576       426  LOAD_FAST                'entry'
              428  LOAD_FAST                'self'
              430  LOAD_ATTR                _olerepr_
              432  LOAD_ATTR                propMap
              434  LOAD_FAST                'attr'
              436  STORE_SUBSCR     

 L. 577       438  LOAD_GLOBAL              debug_attr_print
              440  LOAD_STR                 '__setattr__ property %s (id=0x%x) in Dispatch container %s'
              442  LOAD_FAST                'attr'
              444  LOAD_FAST                'entry'
              446  LOAD_ATTR                dispid
              448  LOAD_FAST                'self'
              450  LOAD_ATTR                _username_
              452  BUILD_TUPLE_3         3 
              454  BINARY_MODULO    
              456  CALL_FUNCTION_1       1  ''
              458  POP_TOP          

 L. 578       460  POP_BLOCK        
              462  LOAD_CONST               None
              464  RETURN_VALUE     
            466_0  COME_FROM_FINALLY   390  '390'

 L. 579       466  DUP_TOP          
              468  LOAD_GLOBAL              pythoncom
              470  LOAD_ATTR                com_error
              472  COMPARE_OP               exception-match
          474_476  POP_JUMP_IF_FALSE   488  'to 488'
              478  POP_TOP          
              480  POP_TOP          
              482  POP_TOP          

 L. 580       484  POP_EXCEPT       
              486  JUMP_FORWARD        490  'to 490'
            488_0  COME_FROM           474  '474'
              488  END_FINALLY      
            490_0  COME_FROM           486  '486'
            490_1  COME_FROM           386  '386'
            490_2  COME_FROM           182  '182'

 L. 581       490  LOAD_GLOBAL              AttributeError
              492  LOAD_STR                 "Property '%s.%s' can not be set."
              494  LOAD_FAST                'self'
              496  LOAD_ATTR                _username_
              498  LOAD_FAST                'attr'
              500  BUILD_TUPLE_2         2 
              502  BINARY_MODULO    
              504  CALL_FUNCTION_1       1  ''
              506  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `RETURN_VALUE' instruction at offset 464