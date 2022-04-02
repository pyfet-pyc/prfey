# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: comtypes\server\__init__.py
import comtypes.client, ctypes

class IClassFactory(comtypes.IUnknown):
    _iid_ = comtypes.GUID('{00000001-0000-0000-C000-000000000046}')
    _methods_ = [
     comtypes.STDMETHOD(comtypes.HRESULT, 'CreateInstance', [
      ctypes.POINTER(comtypes.IUnknown),
      ctypes.POINTER(comtypes.GUID),
      ctypes.POINTER(ctypes.c_void_p)]),
     comtypes.STDMETHOD(comtypes.HRESULT, 'LockServer', [
      ctypes.c_int])]

    def CreateInstance--- This code section failed: ---

 L.  16         0  LOAD_FAST                'dynamic'
                2  POP_JUMP_IF_FALSE    30  'to 30'

 L.  17         4  LOAD_FAST                'interface'
                6  LOAD_CONST               None
                8  <117>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L.  18        12  LOAD_GLOBAL              ValueError
               14  LOAD_STR                 'interface and dynamic are mutually exclusive'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L.  19        20  LOAD_GLOBAL              comtypes
               22  LOAD_ATTR                automation
               24  LOAD_ATTR                IDispatch
               26  STORE_FAST               'realInterface'
               28  JUMP_FORWARD         50  'to 50'
             30_0  COME_FROM             2  '2'

 L.  20        30  LOAD_FAST                'interface'
               32  LOAD_CONST               None
               34  <117>                 0  ''
               36  POP_JUMP_IF_FALSE    46  'to 46'

 L.  21        38  LOAD_GLOBAL              comtypes
               40  LOAD_ATTR                IUnknown
               42  STORE_FAST               'realInterface'
               44  JUMP_FORWARD         50  'to 50'
             46_0  COME_FROM            36  '36'

 L.  23        46  LOAD_FAST                'interface'
               48  STORE_FAST               'realInterface'
             50_0  COME_FROM            44  '44'
             50_1  COME_FROM            28  '28'

 L.  24        50  LOAD_GLOBAL              ctypes
               52  LOAD_METHOD              POINTER
               54  LOAD_FAST                'realInterface'
               56  CALL_METHOD_1         1  ''
               58  CALL_FUNCTION_0       0  ''
               60  STORE_FAST               'obj'

 L.  25        62  LOAD_FAST                'self'
               64  LOAD_METHOD              _IClassFactory__com_CreateInstance
               66  LOAD_FAST                'punkouter'
               68  LOAD_FAST                'realInterface'
               70  LOAD_ATTR                _iid_
               72  LOAD_GLOBAL              ctypes
               74  LOAD_METHOD              byref
               76  LOAD_FAST                'obj'
               78  CALL_METHOD_1         1  ''
               80  CALL_METHOD_3         3  ''
               82  POP_TOP          

 L.  26        84  LOAD_FAST                'dynamic'
               86  POP_JUMP_IF_FALSE   102  'to 102'

 L.  27        88  LOAD_GLOBAL              comtypes
               90  LOAD_ATTR                client
               92  LOAD_ATTR                dynamic
               94  LOAD_METHOD              Dispatch
               96  LOAD_FAST                'obj'
               98  CALL_METHOD_1         1  ''
              100  RETURN_VALUE     
            102_0  COME_FROM            86  '86'

 L.  28       102  LOAD_FAST                'interface'
              104  LOAD_CONST               None
              106  <117>                 0  ''
              108  POP_JUMP_IF_FALSE   122  'to 122'

 L.  30       110  LOAD_GLOBAL              comtypes
              112  LOAD_ATTR                client
              114  LOAD_METHOD              GetBestInterface
              116  LOAD_FAST                'obj'
              118  CALL_METHOD_1         1  ''
              120  RETURN_VALUE     
            122_0  COME_FROM           108  '108'

 L.  32       122  LOAD_FAST                'obj'
              124  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 8


ACTIVEOBJECT_STRONG = 0
ACTIVEOBJECT_WEAK = 1
oleaut32 = ctypes.oledll.oleaut32

def RegisterActiveObject(comobj, weak=True):
    punk = comobj._com_pointers_[comtypes.IUnknown._iid_]
    clsid = comobj._reg_clsid_
    if weak:
        flags = ACTIVEOBJECT_WEAK
    else:
        flags = ACTIVEOBJECT_STRONG
    handle = ctypes.c_ulong()
    oleaut32.RegisterActiveObject(punk, ctypes.byref(clsid), flags, ctypes.byref(handle))
    return handle.value


def RevokeActiveObject(handle):
    oleaut32.RevokeActiveObject(handle, None)