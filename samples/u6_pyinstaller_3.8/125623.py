# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: win32com\server\policy.py
"""Policies 

Note that Dispatchers are now implemented in "dispatcher.py", but
are still documented here.

Policies

 A policy is an object which manages the interaction between a public 
 Python object, and COM .  In simple terms, the policy object is the 
 object which is actually called by COM, and it invokes the requested 
 method, fetches/sets the requested property, etc.  See the 
 @win32com.server.policy.CreateInstance@ method for a description of
 how a policy is specified or created.

 Exactly how a policy determines which underlying object method/property 
 is obtained is up to the policy.  A few policies are provided, but you 
 can build your own.  See each policy class for a description of how it 
 implements its policy.

 There is a policy that allows the object to specify exactly which 
 methods and properties will be exposed.  There is also a policy that 
 will dynamically expose all Python methods and properties - even those 
 added after the object has been instantiated.

Dispatchers

 A Dispatcher is a level in front of a Policy.  A dispatcher is the 
 thing which actually receives the COM calls, and passes them to the 
 policy object (which in turn somehow does something with the wrapped 
 object).

 It is important to note that a policy does not need to have a dispatcher.
 A dispatcher has the same interface as a policy, and simply steps in its 
 place, delegating to the real policy.  The primary use for a Dispatcher 
 is to support debugging when necessary, but without imposing overheads 
 when not (ie, by not using a dispatcher at all).

 There are a few dispatchers provided - "tracing" dispatchers which simply 
 prints calls and args (including a variation which uses 
 win32api.OutputDebugString), and a "debugger" dispatcher, which can 
 invoke the debugger when necessary.

Error Handling

 It is important to realise that the caller of these interfaces may
 not be Python.  Therefore, general Python exceptions and tracebacks aren't 
 much use.

 In general, there is an Exception class that should be raised, to allow 
 the framework to extract rich COM type error information.

 The general rule is that the **only** exception returned from Python COM 
 Server code should be an Exception instance.  Any other Python exception 
 should be considered an implementation bug in the server (if not, it 
 should be handled, and an appropriate Exception instance raised).  Any 
 other exception is considered "unexpected", and a dispatcher may take 
 special action (see Dispatchers above)

 Occasionally, the implementation will raise the policy.error error.  
 This usually means there is a problem in the implementation that the 
 Python programmer should fix.

 For example, if policy is asked to wrap an object which it can not 
 support (because, eg, it does not provide _public_methods_ or _dynamic_) 
 then policy.error will be raised, indicating it is a Python programmers 
 problem, rather than a COM error.
 
"""
__author__ = 'Greg Stein and Mark Hammond'
import win32api, winerror, sys, types, pywintypes, win32con, pythoncom
from pythoncom import DISPATCH_METHOD, DISPATCH_PROPERTYGET, DISPATCH_PROPERTYPUT, DISPATCH_PROPERTYPUTREF, DISPID_UNKNOWN, DISPID_VALUE, DISPID_PROPERTYPUT, DISPID_NEWENUM, DISPID_EVALUATE, DISPID_CONSTRUCTOR, DISPID_DESTRUCTOR, DISPID_COLLECT, DISPID_STARTENUM
S_OK = 0
IDispatchType = pythoncom.TypeIIDs[pythoncom.IID_IDispatch]
IUnknownType = pythoncom.TypeIIDs[pythoncom.IID_IUnknown]
from .exception import COMException
error = __name__ + ' error'
regSpec = 'CLSID\\%s\\PythonCOM'
regPolicy = 'CLSID\\%s\\PythonCOMPolicy'
regDispatcher = 'CLSID\\%s\\PythonCOMDispatcher'
regAddnPath = 'CLSID\\%s\\PythonCOMPath'

def CreateInstance(clsid, reqIID):
    """Create a new instance of the specified IID

  The COM framework **always** calls this function to create a new 
  instance for the specified CLSID.  This function looks up the
  registry for the name of a policy, creates the policy, and asks the
  policy to create the specified object by calling the _CreateInstance_ method.
  
  Exactly how the policy creates the instance is up to the policy.  See the
  specific policy documentation for more details.
  """
    try:
        addnPaths = win32api.RegQueryValue(win32con.HKEY_CLASSES_ROOT, regAddnPath % clsid).split(';')
        for newPath in addnPaths:
            if newPath not in sys.path:
                sys.path.insert(0, newPath)

    except win32api.error:
        pass
    else:
        try:
            policy = win32api.RegQueryValue(win32con.HKEY_CLASSES_ROOT, regPolicy % clsid)
            policy = resolve_func(policy)
        except win32api.error:
            policy = DefaultPolicy
        else:
            try:
                dispatcher = win32api.RegQueryValue(win32con.HKEY_CLASSES_ROOT, regDispatcher % clsid)
                if dispatcher:
                    dispatcher = resolve_func(dispatcher)
            except win32api.error:
                dispatcher = None
            else:
                if dispatcher:
                    retObj = dispatcher(policy, None)
                else:
                    retObj = policy(None)
                return retObj._CreateInstance_(clsid, reqIID)


class BasicWrapPolicy:
    __doc__ = "The base class of policies.\n\n     Normally not used directly (use a child class, instead)\n\n     This policy assumes we are wrapping another object\n     as the COM server.  This supports the delegation of the core COM entry points\n     to either the wrapped object, or to a child class.\n\n     This policy supports the following special attributes on the wrapped object\n\n     _query_interface_ -- A handler which can respond to the COM 'QueryInterface' call.\n     _com_interfaces_ -- An optional list of IIDs which the interface will assume are\n         valid for the object.\n     _invoke_ -- A handler which can respond to the COM 'Invoke' call.  If this attribute\n         is not provided, then the default policy implementation is used.  If this attribute\n         does exist, it is responsible for providing all required functionality - ie, the\n         policy _invoke_ method is not invoked at all (and nor are you able to call it!)\n     _getidsofnames_ -- A handler which can respond to the COM 'GetIDsOfNames' call.  If this attribute\n         is not provided, then the default policy implementation is used.  If this attribute\n         does exist, it is responsible for providing all required functionality - ie, the\n         policy _getidsofnames_ method is not invoked at all (and nor are you able to call it!)\n\n     IDispatchEx functionality:\n\n     _invokeex_ -- Very similar to _invoke_, except slightly different arguments are used.\n         And the result is just the _real_ result (rather than the (hresult, argErr, realResult)\n         tuple that _invoke_ uses.\t\n         This is the new, prefered handler (the default _invoke_ handler simply called _invokeex_)\n     _getdispid_ -- Very similar to _getidsofnames_, except slightly different arguments are used,\n         and only 1 property at a time can be fetched (which is all we support in getidsofnames anyway!)\n         This is the new, prefered handler (the default _invoke_ handler simply called _invokeex_)\n     _getnextdispid_- uses self._name_to_dispid_ to enumerate the DISPIDs\n  "

    def __init__(self, object):
        """Initialise the policy object

       Params:

       object -- The object to wrap.  May be None *iff* @BasicWrapPolicy._CreateInstance_@ will be
       called immediately after this to setup a brand new object
    """
        if object is not None:
            self._wrap_(object)

    def _CreateInstance_(self, clsid, reqIID):
        """Creates a new instance of a **wrapped** object

       This method looks up a "@win32com.server.policy.regSpec@" % clsid entry
       in the registry (using @DefaultPolicy@)
    """
        try:
            classSpec = win32api.RegQueryValue(win32con.HKEY_CLASSES_ROOT, regSpec % clsid)
        except win32api.error:
            raise error('The object is not correctly registered - %s key can not be read' % (regSpec % clsid))
        else:
            myob = call_func(classSpec)
            self._wrap_(myob)
            try:
                return pythoncom.WrapObject(self, reqIID)
                    except pythoncom.com_error as xxx_todo_changeme:
                try:
                    hr, desc, exc, arg = xxx_todo_changeme.args
                    from win32com.util import IIDToInterfaceName
                    desc = "The object '%r' was created, but does not support the interface '%s'(%s): %s" % (
                     myob, IIDToInterfaceName(reqIID), reqIID, desc)
                    raise pythoncom.com_error(hr, desc, exc, arg)
                finally:
                    xxx_todo_changeme = None
                    del xxx_todo_changeme

    def _wrap_(self, object):
        """Wraps up the specified object.

       This function keeps a reference to the passed
       object, and may interogate it to determine how to respond to COM requests, etc.
    """
        self._name_to_dispid_ = {}
        ob = self._obj_ = object
        if hasattr(ob, '_query_interface_'):
            self._query_interface_ = ob._query_interface_
        else:
            if hasattr(ob, '_invoke_'):
                self._invoke_ = ob._invoke_
            if hasattr(ob, '_invokeex_'):
                self._invokeex_ = ob._invokeex_
            if hasattr(ob, '_getidsofnames_'):
                self._getidsofnames_ = ob._getidsofnames_
            if hasattr(ob, '_getdispid_'):
                self._getdispid_ = ob._getdispid_
            if hasattr(ob, '_com_interfaces_'):
                self._com_interfaces_ = []
                for i in ob._com_interfaces_:
                    if type(i) != pywintypes.IIDType:
                        if i[0] != '{':
                            i = pythoncom.InterfaceNames[i]
                        else:
                            i = pythoncom.MakeIID(i)
                    self._com_interfaces_.append(i)

            else:
                self._com_interfaces_ = []

    def _QueryInterface_(self, iid):
        """The main COM entry-point for QueryInterface. 

       This checks the _com_interfaces_ attribute and if the interface is not specified 
       there, it calls the derived helper _query_interface_
    """
        if iid in self._com_interfaces_:
            return 1
        return self._query_interface_(iid)

    def _query_interface_(self, iid):
        """Called if the object does not provide the requested interface in _com_interfaces_,
       and does not provide a _query_interface_ handler.

       Returns a result to the COM framework indicating the interface is not supported.
    """
        return 0

    def _Invoke_(self, dispid, lcid, wFlags, args):
        """The main COM entry-point for Invoke.  

       This calls the _invoke_ helper.
    """
        if type(dispid) == type(''):
            try:
                dispid = self._name_to_dispid_[dispid.lower()]
            except KeyError:
                raise COMException(scode=(winerror.DISP_E_MEMBERNOTFOUND), desc='Member not found')

        return self._invoke_(dispid, lcid, wFlags, args)

    def _invoke_(self, dispid, lcid, wFlags, args):
        return (
         S_OK, -1, self._invokeex_(dispid, lcid, wFlags, args, None, None))

    def _GetIDsOfNames_(self, names, lcid):
        """The main COM entry-point for GetIDsOfNames.

       This checks the validity of the arguments, and calls the _getidsofnames_ helper.
    """
        if len(names) > 1:
            raise COMException(scode=(winerror.DISP_E_INVALID), desc='Cannot support member argument names')
        return self._getidsofnames_(names, lcid)

    def _getidsofnames_(self, names, lcid):
        return (
         self._getdispid_(names[0], 0),)

    def _GetDispID_(self, name, fdex):
        return self._getdispid_(name, fdex)

    def _getdispid_--- This code section failed: ---

 L. 307         0  SETUP_FINALLY        18  'to 18'

 L. 309         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _name_to_dispid_
                6  LOAD_FAST                'name'
                8  LOAD_METHOD              lower
               10  CALL_METHOD_0         0  ''
               12  BINARY_SUBSCR    
               14  POP_BLOCK        
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L. 310        18  DUP_TOP          
               20  LOAD_GLOBAL              KeyError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    48  'to 48'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 311        32  LOAD_GLOBAL              COMException
               34  LOAD_GLOBAL              winerror
               36  LOAD_ATTR                DISP_E_UNKNOWNNAME
               38  LOAD_CONST               ('scode',)
               40  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               42  RAISE_VARARGS_1       1  'exception instance'
               44  POP_EXCEPT       
               46  JUMP_FORWARD         50  'to 50'
             48_0  COME_FROM            24  '24'
               48  END_FINALLY      
             50_0  COME_FROM            46  '46'

Parse error at or near `POP_TOP' instruction at offset 28

    def _InvokeEx_(self, dispid, lcid, wFlags, args, kwargs, serviceProvider):
        """The main COM entry-point for InvokeEx.  

       This calls the _invokeex_ helper.
    """
        if type(dispid) == type(''):
            try:
                dispid = self._name_to_dispid_[dispid.lower()]
            except KeyError:
                raise COMException(scode=(winerror.DISP_E_MEMBERNOTFOUND), desc='Member not found')

        return self._invokeex_(dispid, lcid, wFlags, args, kwargs, serviceProvider)

    def _invokeex_(self, dispid, lcid, wFlags, args, kwargs, serviceProvider):
        """A stub for _invokeex_ - should never be called.  
 
       Simply raises an exception.
    """
        raise error('This class does not provide _invokeex_ semantics')

    def _DeleteMemberByName_(self, name, fdex):
        return self._deletememberbyname_(name, fdex)

    def _deletememberbyname_(self, name, fdex):
        raise COMException(scode=(winerror.E_NOTIMPL))

    def _DeleteMemberByDispID_(self, id):
        return self._deletememberbydispid(id)

    def _deletememberbydispid_(self, id):
        raise COMException(scode=(winerror.E_NOTIMPL))

    def _GetMemberProperties_(self, id, fdex):
        return self._getmemberproperties_(id, fdex)

    def _getmemberproperties_(self, id, fdex):
        raise COMException(scode=(winerror.E_NOTIMPL))

    def _GetMemberName_(self, dispid):
        return self._getmembername_(dispid)

    def _getmembername_(self, dispid):
        raise COMException(scode=(winerror.E_NOTIMPL))

    def _GetNextDispID_(self, fdex, dispid):
        return self._getnextdispid_(fdex, dispid)

    def _getnextdispid_--- This code section failed: ---

 L. 358         0  LOAD_GLOBAL              list
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _name_to_dispid_
                6  LOAD_METHOD              values
                8  CALL_METHOD_0         0  ''
               10  CALL_FUNCTION_1       1  ''
               12  STORE_FAST               'ids'

 L. 359        14  LOAD_FAST                'ids'
               16  LOAD_METHOD              sort
               18  CALL_METHOD_0         0  ''
               20  POP_TOP          

 L. 360        22  LOAD_GLOBAL              DISPID_STARTENUM
               24  LOAD_FAST                'ids'
               26  COMPARE_OP               in
               28  POP_JUMP_IF_FALSE    40  'to 40'

 L. 360        30  LOAD_FAST                'ids'
               32  LOAD_METHOD              remove
               34  LOAD_GLOBAL              DISPID_STARTENUM
               36  CALL_METHOD_1         1  ''
               38  POP_TOP          
             40_0  COME_FROM            28  '28'

 L. 361        40  LOAD_FAST                'dispid'
               42  LOAD_GLOBAL              DISPID_STARTENUM
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_FALSE    56  'to 56'

 L. 362        48  LOAD_FAST                'ids'
               50  LOAD_CONST               0
               52  BINARY_SUBSCR    
               54  RETURN_VALUE     
             56_0  COME_FROM            46  '46'

 L. 364        56  SETUP_FINALLY        78  'to 78'

 L. 365        58  LOAD_FAST                'ids'
               60  LOAD_FAST                'ids'
               62  LOAD_METHOD              index
               64  LOAD_FAST                'dispid'
               66  CALL_METHOD_1         1  ''
               68  LOAD_CONST               1
               70  BINARY_ADD       
               72  BINARY_SUBSCR    
               74  POP_BLOCK        
               76  RETURN_VALUE     
             78_0  COME_FROM_FINALLY    56  '56'

 L. 366        78  DUP_TOP          
               80  LOAD_GLOBAL              ValueError
               82  COMPARE_OP               exception-match
               84  POP_JUMP_IF_FALSE   108  'to 108'
               86  POP_TOP          
               88  POP_TOP          
               90  POP_TOP          

 L. 367        92  LOAD_GLOBAL              COMException
               94  LOAD_GLOBAL              winerror
               96  LOAD_ATTR                E_UNEXPECTED
               98  LOAD_CONST               ('scode',)
              100  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              102  RAISE_VARARGS_1       1  'exception instance'
              104  POP_EXCEPT       
              106  JUMP_FORWARD        140  'to 140'
            108_0  COME_FROM            84  '84'

 L. 368       108  DUP_TOP          
              110  LOAD_GLOBAL              IndexError
              112  COMPARE_OP               exception-match
              114  POP_JUMP_IF_FALSE   138  'to 138'
              116  POP_TOP          
              118  POP_TOP          
              120  POP_TOP          

 L. 369       122  LOAD_GLOBAL              COMException
              124  LOAD_GLOBAL              winerror
              126  LOAD_ATTR                S_FALSE
              128  LOAD_CONST               ('scode',)
              130  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              132  RAISE_VARARGS_1       1  'exception instance'
              134  POP_EXCEPT       
              136  JUMP_FORWARD        140  'to 140'
            138_0  COME_FROM           114  '114'
              138  END_FINALLY      
            140_0  COME_FROM           136  '136'
            140_1  COME_FROM           106  '106'

Parse error at or near `POP_TOP' instruction at offset 88

    def _GetNameSpaceParent_(self):
        return self._getnamespaceparent()

    def _getnamespaceparent_(self):
        raise COMException(scode=(winerror.E_NOTIMPL))


class MappedWrapPolicy(BasicWrapPolicy):
    __doc__ = 'Wraps an object using maps to do its magic\n\n     This policy wraps up a Python object, using a number of maps\n     which translate from a Dispatch ID and flags, into an object to call/getattr, etc.\n\n     It is the responsibility of derived classes to determine exactly how the\n     maps are filled (ie, the derived classes determine the map filling policy.\n\n     This policy supports the following special attributes on the wrapped object\n\n     _dispid_to_func_/_dispid_to_get_/_dispid_to_put_ -- These are dictionaries\n       (keyed by integer dispid, values are string attribute names) which the COM\n       implementation uses when it is processing COM requests.  Note that the implementation\n       uses this dictionary for its own purposes - not a copy - which means the contents of \n       these dictionaries will change as the object is used.\n\n  '

    def _wrap_(self, object):
        BasicWrapPolicy._wrap_(self, object)
        ob = self._obj_
        if hasattr(ob, '_dispid_to_func_'):
            self._dispid_to_func_ = ob._dispid_to_func_
        else:
            self._dispid_to_func_ = {}
        if hasattr(ob, '_dispid_to_get_'):
            self._dispid_to_get_ = ob._dispid_to_get_
        else:
            self._dispid_to_get_ = {}
        if hasattr(ob, '_dispid_to_put_'):
            self._dispid_to_put_ = ob._dispid_to_put_
        else:
            self._dispid_to_put_ = {}

    def _getmembername_(self, dispid):
        if dispid in self._dispid_to_func_:
            return self._dispid_to_func_[dispid]
        if dispid in self._dispid_to_get_:
            return self._dispid_to_get_[dispid]
        if dispid in self._dispid_to_put_:
            return self._dispid_to_put_[dispid]
        raise COMException(scode=(winerror.DISP_E_MEMBERNOTFOUND))


class DesignatedWrapPolicy(MappedWrapPolicy):
    __doc__ = 'A policy which uses a mapping to link functions and dispid\n     \n     A MappedWrappedPolicy which allows the wrapped object to specify, via certain\n     special named attributes, exactly which methods and properties are exposed.\n\n     All a wrapped object need do is provide the special attributes, and the policy\n     will handle everything else.\n\n     Attributes:\n\n     _public_methods_ -- Required, unless a typelib GUID is given -- A list\n                  of strings, which must be the names of methods the object\n                  provides.  These methods will be exposed and callable\n                  from other COM hosts.\n     _public_attrs_ A list of strings, which must be the names of attributes on the object.\n                  These attributes will be exposed and readable and possibly writeable from other COM hosts.\n     _readonly_attrs_ -- A list of strings, which must also appear in _public_attrs.  These\n                  attributes will be readable, but not writable, by other COM hosts.\n     _value_ -- A method that will be called if the COM host requests the "default" method\n                  (ie, calls Invoke with dispid==DISPID_VALUE)\n     _NewEnum -- A method that will be called if the COM host requests an enumerator on the\n                  object (ie, calls Invoke with dispid==DISPID_NEWENUM.)\n                  It is the responsibility of the method to ensure the returned\n                  object conforms to the required Enum interface.\n\n    _typelib_guid_ -- The GUID of the typelibrary with interface definitions we use.\n    _typelib_version_ -- A tuple of (major, minor) with a default of 1,1\n    _typelib_lcid_ -- The LCID of the typelib, default = LOCALE_USER_DEFAULT\n\n     _Evaluate -- Dunno what this means, except the host has called Invoke with dispid==DISPID_EVALUATE!\n                  See the COM documentation for details.\n  '

    def _wrap_(self, ob):
        tlb_guid = getattr(ob, '_typelib_guid_', None)
        if tlb_guid is not None:
            tlb_major, tlb_minor = getattr(ob, '_typelib_version_', (1, 0))
            tlb_lcid = getattr(ob, '_typelib_lcid_', 0)
            from win32com import universal
            interfaces = [i for i in getattr(ob, '_com_interfaces_', []) if type(i) != pywintypes.IIDType if not i.startswith('{')]
            universal_data = universal.RegisterInterfaces(tlb_guid, tlb_lcid, tlb_major, tlb_minor, interfaces)
        else:
            universal_data = []
        MappedWrapPolicy._wrap_(self, ob)
        if not hasattr(ob, '_public_methods_'):
            if not hasattr(ob, '_typelib_guid_'):
                raise error('Object does not support DesignatedWrapPolicy, as it does not have either _public_methods_ or _typelib_guid_ attributes.')
        for dispid, name in self._dispid_to_func_.items():
            self._name_to_dispid_[name.lower()] = dispid
        else:
            for dispid, name in self._dispid_to_get_.items():
                self._name_to_dispid_[name.lower()] = dispid
            else:
                for dispid, name in self._dispid_to_put_.items():
                    self._name_to_dispid_[name.lower()] = dispid
                else:
                    for dispid, invkind, name in universal_data:
                        self._name_to_dispid_[name.lower()] = dispid
                        if invkind == DISPATCH_METHOD:
                            self._dispid_to_func_[dispid] = name
                        elif invkind in (DISPATCH_PROPERTYPUT, DISPATCH_PROPERTYPUTREF):
                            self._dispid_to_put_[dispid] = name
                        elif invkind == DISPATCH_PROPERTYGET:
                            self._dispid_to_get_[dispid] = name
                        else:
                            raise ValueError('unexpected invkind: %d (%s)' % (invkind, name))
                    else:
                        if hasattr(ob, '_value_'):
                            self._dispid_to_get_[DISPID_VALUE] = '_value_'
                            self._dispid_to_put_[DISPID_PROPERTYPUT] = '_value_'
                        else:
                            if hasattr(ob, '_NewEnum'):
                                self._name_to_dispid_['_newenum'] = DISPID_NEWENUM
                                self._dispid_to_func_[DISPID_NEWENUM] = '_NewEnum'
                            if hasattr(ob, '_Evaluate'):
                                self._name_to_dispid_['_evaluate'] = DISPID_EVALUATE
                                self._dispid_to_func_[DISPID_EVALUATE] = '_Evaluate'
                            next_dispid = self._allocnextdispid(999)
                            if hasattr(ob, '_public_attrs_'):
                                if hasattr(ob, '_readonly_attrs_'):
                                    readonly = ob._readonly_attrs_
                                else:
                                    readonly = []
                                for name in ob._public_attrs_:
                                    dispid = self._name_to_dispid_.get(name.lower())
                                    if dispid is None:
                                        dispid = next_dispid
                                        self._name_to_dispid_[name.lower()] = dispid
                                        next_dispid = self._allocnextdispid(next_dispid)
                                    self._dispid_to_get_[dispid] = name
                                    if name not in readonly:
                                        self._dispid_to_put_[dispid] = name

                        for name in getattr(ob, '_public_methods_', []):
                            dispid = self._name_to_dispid_.get(name.lower())
                            if dispid is None:
                                dispid = next_dispid
                                self._name_to_dispid_[name.lower()] = dispid
                                next_dispid = self._allocnextdispid(next_dispid)
                            self._dispid_to_func_[dispid] = name
                        else:
                            self._typeinfos_ = None

    def _build_typeinfos_--- This code section failed: ---

 L. 532         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _obj_
                6  LOAD_STR                 '_typelib_guid_'
                8  LOAD_CONST               None
               10  CALL_FUNCTION_3       3  ''
               12  STORE_FAST               'tlb_guid'

 L. 533        14  LOAD_FAST                'tlb_guid'
               16  LOAD_CONST               None
               18  COMPARE_OP               is
               20  POP_JUMP_IF_FALSE    26  'to 26'

 L. 534        22  BUILD_LIST_0          0 
               24  RETURN_VALUE     
             26_0  COME_FROM            20  '20'

 L. 535        26  LOAD_GLOBAL              getattr
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                _obj_
               32  LOAD_STR                 '_typelib_version_'
               34  LOAD_CONST               (1, 0)
               36  CALL_FUNCTION_3       3  ''
               38  UNPACK_SEQUENCE_2     2 
               40  STORE_FAST               'tlb_major'
               42  STORE_FAST               'tlb_minor'

 L. 536        44  LOAD_GLOBAL              pythoncom
               46  LOAD_METHOD              LoadRegTypeLib
               48  LOAD_FAST                'tlb_guid'
               50  LOAD_FAST                'tlb_major'
               52  LOAD_FAST                'tlb_minor'
               54  CALL_METHOD_3         3  ''
               56  STORE_FAST               'tlb'

 L. 537        58  LOAD_FAST                'tlb'
               60  LOAD_METHOD              GetTypeComp
               62  CALL_METHOD_0         0  ''
               64  STORE_FAST               'typecomp'

 L. 540        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _obj_
               70  LOAD_ATTR                _com_interfaces_
               72  GET_ITER         
               74  FOR_ITER            142  'to 142'
               76  STORE_FAST               'iname'

 L. 541        78  SETUP_FINALLY       118  'to 118'

 L. 542        80  LOAD_FAST                'typecomp'
               82  LOAD_METHOD              BindType
               84  LOAD_FAST                'iname'
               86  CALL_METHOD_1         1  ''
               88  UNPACK_SEQUENCE_2     2 
               90  STORE_FAST               'type_info'
               92  STORE_FAST               'type_comp'

 L. 543        94  LOAD_FAST                'type_info'
               96  LOAD_CONST               None
               98  COMPARE_OP               is-not
              100  POP_JUMP_IF_FALSE   114  'to 114'

 L. 544       102  LOAD_FAST                'type_info'
              104  BUILD_LIST_1          1 
              106  POP_BLOCK        
              108  ROT_TWO          
              110  POP_TOP          
              112  RETURN_VALUE     
            114_0  COME_FROM           100  '100'
              114  POP_BLOCK        
              116  JUMP_BACK            74  'to 74'
            118_0  COME_FROM_FINALLY    78  '78'

 L. 545       118  DUP_TOP          
              120  LOAD_GLOBAL              pythoncom
              122  LOAD_ATTR                com_error
              124  COMPARE_OP               exception-match
              126  POP_JUMP_IF_FALSE   138  'to 138'
              128  POP_TOP          
              130  POP_TOP          
              132  POP_TOP          

 L. 546       134  POP_EXCEPT       
              136  JUMP_BACK            74  'to 74'
            138_0  COME_FROM           126  '126'
              138  END_FINALLY      
              140  JUMP_BACK            74  'to 74'

 L. 547       142  BUILD_LIST_0          0 
              144  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_TWO' instruction at offset 108

    def _GetTypeInfoCount_(self):
        if self._typeinfos_ is None:
            self._typeinfos_ = self._build_typeinfos_()
        return len(self._typeinfos_)

    def _GetTypeInfo_(self, index, lcid):
        if self._typeinfos_ is None:
            self._typeinfos_ = self._build_typeinfos_()
        if index < 0 or index >= len(self._typeinfos_):
            raise COMException(scode=(winerror.DISP_E_BADINDEX))
        return (
         0, self._typeinfos_[index])

    def _allocnextdispid(self, last_dispid):
        while True:
            last_dispid = last_dispid + 1
            if last_dispid not in self._dispid_to_func_ and last_dispid not in self._dispid_to_get_ and last_dispid not in self._dispid_to_put_:
                return last_dispid

    def _invokeex_(self, dispid, lcid, wFlags, args, kwArgs, serviceProvider):
        if wFlags & DISPATCH_METHOD:
            try:
                funcname = self._dispid_to_func_[dispid]
            except KeyError:
                if not wFlags & DISPATCH_PROPERTYGET:
                    raise COMException(scode=(winerror.DISP_E_MEMBERNOTFOUND))

        else:
            try:
                func = getattr(self._obj_, funcname)
            except AttributeError:
                raise COMException(scode=(winerror.DISP_E_MEMBERNOTFOUND))
            else:
                try:
                    return func(*args)
                            except TypeError as v:
                    try:
                        if str(v).find('arguments') >= 0:
                            print('** TypeError %s calling function %r(%r)' % (v, func, args))
                        raise
                    finally:
                        v = None
                        del v

            if wFlags & DISPATCH_PROPERTYGET:
                try:
                    name = self._dispid_to_get_[dispid]
                except KeyError:
                    raise COMException(scode=(winerror.DISP_E_MEMBERNOTFOUND))
                else:
                    retob = getattr(self._obj_, name)
                    if type(retob) == types.MethodType:
                        retob = retob(*args)
                    return retob
                    if wFlags & (DISPATCH_PROPERTYPUT | DISPATCH_PROPERTYPUTREF):
                        try:
                            name = self._dispid_to_put_[dispid]
                        except KeyError:
                            raise COMException(scode=(winerror.DISP_E_MEMBERNOTFOUND))
                        else:
                            if type(getattr(self._obj_, name, None)) == types.MethodType and type(getattr(self._obj_, 'Set' + name, None)) == types.MethodType:
                                fn = getattr(self._obj_, 'Set' + name)
                                fn(*args)
            else:
                setattr(self._obj_, name, args[0])
            return
        raise COMException(scode=(winerror.E_INVALIDARG), desc='invalid wFlags')


class EventHandlerPolicy(DesignatedWrapPolicy):
    __doc__ = 'The default policy used by event handlers in the win32com.client package.\n\n    In addition to the base policy, this provides argument conversion semantics for\n    params\n      * dispatch params are converted to dispatch objects.\n      * Unicode objects are converted to strings (1.5.2 and earlier)\n\n    NOTE: Later, we may allow the object to override this process??\n    '

    def _transform_args_(self, args, kwArgs, dispid, lcid, wFlags, serviceProvider):
        ret = []
        for arg in args:
            arg_type = type(arg)
            if arg_type == IDispatchType:
                import win32com.client
                arg = win32com.client.Dispatch(arg)
            else:
                if arg_type == IUnknownType:
                    try:
                        import win32com.client
                        arg = win32com.client.Dispatch(arg.QueryInterface(pythoncom.IID_IDispatch))
                    except pythoncom.error:
                        pass

            ret.append(arg)
        else:
            return (
             tuple(ret), kwArgs)

    def _invokeex_(self, dispid, lcid, wFlags, args, kwArgs, serviceProvider):
        args, kwArgs = self._transform_args_(args, kwArgs, dispid, lcid, wFlags, serviceProvider)
        return DesignatedWrapPolicy._invokeex_(self, dispid, lcid, wFlags, args, kwArgs, serviceProvider)


class DynamicPolicy(BasicWrapPolicy):
    __doc__ = "A policy which dynamically (ie, at run-time) determines public interfaces.\n  \n     A dynamic policy is used to dynamically dispatch methods and properties to the\n     wrapped object.  The list of objects and properties does not need to be known in\n     advance, and methods or properties added to the wrapped object after construction\n     are also handled.\n\n     The wrapped object must provide the following attributes:\n\n     _dynamic_ -- A method that will be called whenever an invoke on the object\n            is called.  The method is called with the name of the underlying method/property\n            (ie, the mapping of dispid to/from name has been resolved.)  This name property\n            may also be '_value_' to indicate the default, and '_NewEnum' to indicate a new\n            enumerator is requested.\n            \n  "

    def _wrap_(self, object):
        BasicWrapPolicy._wrap_(self, object)
        if not hasattr(self._obj_, '_dynamic_'):
            raise error('Object does not support Dynamic COM Policy')
        self._next_dynamic_ = self._min_dynamic_ = 1000
        self._dyn_dispid_to_name_ = {DISPID_VALUE: '_value_', DISPID_NEWENUM: '_NewEnum'}

    def _getdispid_--- This code section failed: ---

 L. 678         0  LOAD_FAST                'name'
                2  LOAD_METHOD              lower
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'lname'

 L. 679         8  SETUP_FINALLY        22  'to 22'

 L. 680        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _name_to_dispid_
               14  LOAD_FAST                'lname'
               16  BINARY_SUBSCR    
               18  POP_BLOCK        
               20  RETURN_VALUE     
             22_0  COME_FROM_FINALLY     8  '8'

 L. 681        22  DUP_TOP          
               24  LOAD_GLOBAL              KeyError
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    80  'to 80'
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L. 682        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _next_dynamic_
               40  LOAD_CONST               1
               42  BINARY_ADD       
               44  DUP_TOP          
               46  STORE_FAST               'dispid'
               48  LOAD_FAST                'self'
               50  STORE_ATTR               _next_dynamic_

 L. 683        52  LOAD_FAST                'dispid'
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                _name_to_dispid_
               58  LOAD_FAST                'lname'
               60  STORE_SUBSCR     

 L. 684        62  LOAD_FAST                'name'
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                _dyn_dispid_to_name_
               68  LOAD_FAST                'dispid'
               70  STORE_SUBSCR     

 L. 685        72  LOAD_FAST                'dispid'
               74  ROT_FOUR         
               76  POP_EXCEPT       
               78  RETURN_VALUE     
             80_0  COME_FROM            28  '28'
               80  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 32

    def _invoke_(self, dispid, lcid, wFlags, args):
        return (
         S_OK, -1, self._invokeex_(dispid, lcid, wFlags, args, None, None))

    def _invokeex_(self, dispid, lcid, wFlags, args, kwargs, serviceProvider):
        try:
            name = self._dyn_dispid_to_name_[dispid]
        except KeyError:
            raise COMException(scode=(winerror.DISP_E_MEMBERNOTFOUND), desc='Member not found')
        else:
            return self._obj_._dynamic_(name, lcid, wFlags, args)


DefaultPolicy = DesignatedWrapPolicy

def resolve_func--- This code section failed: ---

 L. 710         0  SETUP_FINALLY        60  'to 60'

 L. 711         2  LOAD_FAST                'spec'
                4  LOAD_METHOD              rindex
                6  LOAD_STR                 '.'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'idx'

 L. 712        12  LOAD_FAST                'spec'
               14  LOAD_CONST               None
               16  LOAD_FAST                'idx'
               18  BUILD_SLICE_2         2 
               20  BINARY_SUBSCR    
               22  STORE_FAST               'mname'

 L. 713        24  LOAD_FAST                'spec'
               26  LOAD_FAST                'idx'
               28  LOAD_CONST               1
               30  BINARY_ADD       
               32  LOAD_CONST               None
               34  BUILD_SLICE_2         2 
               36  BINARY_SUBSCR    
               38  STORE_FAST               'fname'

 L. 717        40  LOAD_GLOBAL              _import_module
               42  LOAD_FAST                'mname'
               44  CALL_FUNCTION_1       1  ''
               46  STORE_FAST               'module'

 L. 718        48  LOAD_GLOBAL              getattr
               50  LOAD_FAST                'module'
               52  LOAD_FAST                'fname'
               54  CALL_FUNCTION_2       2  ''
               56  POP_BLOCK        
               58  RETURN_VALUE     
             60_0  COME_FROM_FINALLY     0  '0'

 L. 719        60  DUP_TOP          
               62  LOAD_GLOBAL              ValueError
               64  COMPARE_OP               exception-match
               66  POP_JUMP_IF_FALSE    88  'to 88'
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L. 720        74  LOAD_GLOBAL              globals
               76  CALL_FUNCTION_0       0  ''
               78  LOAD_FAST                'spec'
               80  BINARY_SUBSCR    
               82  ROT_FOUR         
               84  POP_EXCEPT       
               86  RETURN_VALUE     
             88_0  COME_FROM            66  '66'
               88  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 70


def call_func(spec, *args):
    """Call a function specified by name.
  
  Call a function specified by 'module.function' and return the result.
  """
    return (resolve_func(spec))(*args)


def _import_module(mname):
    """Import a module just like the 'import' statement.

  Having this function is much nicer for importing arbitrary modules than
  using the 'exec' keyword.  It is more efficient and obvious to the reader.
  """
    __import__(mname)
    return sys.modules[mname]


try:
    from .dispatcher import DispatcherTrace, DispatcherWin32trace
except ImportError:
    pass