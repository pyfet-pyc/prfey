# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: comtypes\persist.py
"""This module defines the following interfaces:

  IErrorLog
  IPropertyBag
  IPersistPropertyBag
  IPropertyBag2
  IPersistPropertyBag2

The 'DictPropertyBag' class is a class implementing the IPropertyBag
interface, useful in client code.
"""
from ctypes import *
from ctypes.wintypes import WORD, DWORD, BOOL
from comtypes import GUID, IUnknown, COMMETHOD, HRESULT, dispid
from comtypes import IPersist
from comtypes.automation import VARIANT, tagEXCEPINFO
WSTRING = c_wchar_p

class IErrorLog(IUnknown):
    _iid_ = GUID('{3127CA40-446E-11CE-8135-00AA004BB851}')
    _idlflags_ = []
    _methods_ = [
     COMMETHOD([], HRESULT, 'AddError', (
      [
       'in'], WSTRING, 'pszPropName'), (
      [
       'in'], POINTER(tagEXCEPINFO), 'pExcepInfo'))]


class IPropertyBag(IUnknown):
    _iid_ = GUID('{55272A00-42CB-11CE-8135-00AA004BB851}')
    _idlflags_ = []
    _methods_ = [
     COMMETHOD([], HRESULT, 'Read', (
      [
       'in'], WSTRING, 'pszPropName'), (
      [
       'in', 'out'], POINTER(VARIANT), 'pVar'), (
      [
       'in'], POINTER(IErrorLog), 'pErrorLog')),
     COMMETHOD([], HRESULT, 'Write', (
      [
       'in'], WSTRING, 'pszPropName'), (
      [
       'in'], POINTER(VARIANT), 'pVar'))]


class IPersistPropertyBag(IPersist):
    _iid_ = GUID('{37D84F60-42CB-11CE-8135-00AA004BB851}')
    _idlflags_ = []
    _methods_ = [
     COMMETHOD([], HRESULT, 'InitNew'),
     COMMETHOD([], HRESULT, 'Load', (
      [
       'in'], POINTER(IPropertyBag), 'pPropBag'), (
      [
       'in'], POINTER(IErrorLog), 'pErrorLog')),
     COMMETHOD([], HRESULT, 'Save', (
      [
       'in'], POINTER(IPropertyBag), 'pPropBag'), (
      [
       'in'], c_int, 'fClearDirty'), (
      [
       'in'], c_int, 'fSaveAllProperties'))]


CLIPFORMAT = WORD
PROPBAG2_TYPE_UNDEFINED = 0
PROPBAG2_TYPE_DATA = 1
PROPBAG2_TYPE_URL = 2
PROPBAG2_TYPE_OBJECT = 3
PROPBAG2_TYPE_STREAM = 4
PROPBAG2_TYPE_STORAGE = 5
PROPBAG2_TYPE_MONIKER = 6

class tagPROPBAG2(Structure):
    _fields_ = [
     (
      'dwType', c_ulong),
     (
      'vt', c_ushort),
     (
      'cfType', CLIPFORMAT),
     (
      'dwHint', c_ulong),
     (
      'pstrName', WSTRING),
     (
      'clsid', GUID)]


class IPropertyBag2(IUnknown):
    _iid_ = GUID('{22F55882-280B-11D0-A8A9-00A0C90C2004}')
    _idlflags_ = []
    _methods_ = [
     COMMETHOD([], HRESULT, 'Read', (
      [
       'in'], c_ulong, 'cProperties'), (
      [
       'in'], POINTER(tagPROPBAG2), 'pPropBag'), (
      [
       'in'], POINTER(IErrorLog), 'pErrLog'), (
      [
       'out'], POINTER(VARIANT), 'pvarValue'), (
      [
       'out'], POINTER(HRESULT), 'phrError')),
     COMMETHOD([], HRESULT, 'Write', (
      [
       'in'], c_ulong, 'cProperties'), (
      [
       'in'], POINTER(tagPROPBAG2), 'pPropBag'), (
      [
       'in'], POINTER(VARIANT), 'pvarValue')),
     COMMETHOD([], HRESULT, 'CountProperties', (
      [
       'out'], POINTER(c_ulong), 'pcProperties')),
     COMMETHOD([], HRESULT, 'GetPropertyInfo', (
      [
       'in'], c_ulong, 'iProperty'), (
      [
       'in'], c_ulong, 'cProperties'), (
      [
       'out'], POINTER(tagPROPBAG2), 'pPropBag'), (
      [
       'out'], POINTER(c_ulong), 'pcProperties')),
     COMMETHOD([], HRESULT, 'LoadObject', (
      [
       'in'], WSTRING, 'pstrName'), (
      [
       'in'], c_ulong, 'dwHint'), (
      [
       'in'], POINTER(IUnknown), 'punkObject'), (
      [
       'in'], POINTER(IErrorLog), 'pErrLog'))]


class IPersistPropertyBag2(IPersist):
    _iid_ = GUID('{22F55881-280B-11D0-A8A9-00A0C90C2004}')
    _idlflags_ = []
    _methods_ = [
     COMMETHOD([], HRESULT, 'InitNew'),
     COMMETHOD([], HRESULT, 'Load', (
      [
       'in'], POINTER(IPropertyBag2), 'pPropBag'), (
      [
       'in'], POINTER(IErrorLog), 'pErrLog')),
     COMMETHOD([], HRESULT, 'Save', (
      [
       'in'], POINTER(IPropertyBag2), 'pPropBag'), (
      [
       'in'], c_int, 'fClearDirty'), (
      [
       'in'], c_int, 'fSaveAllProperties')),
     COMMETHOD([], HRESULT, 'IsDirty')]


STGM_READ = 0
STGM_WRITE = 1
STGM_READWRITE = 2
STGM_SHARE_EXCLUSIVE = 16
STGM_SHARE_DENY_WRITE = 32
STGM_SHARE_DENY_READ = 48
STGM_SHARE_DENY_NONE = 64
STGM_PRIORITY = 262144
STGM_FAILIFTHERE = 0
STGM_CREATE = 4096
STGM_CONVERT = 131072
STGM_DIRECT = 0
STGM_TRANSACTED = 65536
STGM_NOSCRATCH = 1048576
STGM_NOSNAPSHOT = 2097152
STGM_SIMPLE = 134217728
STGM_DIRECT_SWMR = 4194304
STGM_DELETEONRELEASE = 67108864
LPOLESTR = LPCOLESTR = c_wchar_p

class IPersistFile(IPersist):
    _iid_ = GUID('{0000010B-0000-0000-C000-000000000046}')
    _idlflags_ = []
    _methods_ = [
     COMMETHOD([], HRESULT, 'IsDirty'),
     COMMETHOD([], HRESULT, 'Load', (
      [
       'in'], LPCOLESTR, 'pszFileName'), (
      [
       'in'], DWORD, 'dwMode')),
     COMMETHOD([], HRESULT, 'Save', (
      [
       'in'], LPCOLESTR, 'pszFileName'), (
      [
       'in'], BOOL, 'fRemember')),
     COMMETHOD([], HRESULT, 'SaveCompleted', (
      [
       'in'], LPCOLESTR, 'pszFileName')),
     COMMETHOD([], HRESULT, 'GetCurFile', (
      [
       'out'], POINTER(LPOLESTR), 'ppszFileName'))]


from comtypes import COMObject
from comtypes.hresult import *

class DictPropertyBag(COMObject):
    __doc__ = 'An object implementing the IProperty interface on a dictionary.\n\n    Pass named values in the constructor for the client to Read(), or\n    retrieve from the .values instance variable after the client has\n    called Load().\n    '
    _com_interfaces_ = [
     IPropertyBag]

    def __init__(self, **kw):
        super(DictPropertyBag, self).__init__()
        self.values = kw

    def Read--- This code section failed: ---

 L. 196         0  SETUP_FINALLY        16  'to 16'

 L. 197         2  LOAD_FAST                'self'
                4  LOAD_ATTR                values
                6  LOAD_FAST                'name'
                8  BINARY_SUBSCR    
               10  STORE_FAST               'val'
               12  POP_BLOCK        
               14  JUMP_FORWARD         38  'to 38'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 198        16  DUP_TOP          
               18  LOAD_GLOBAL              KeyError
               20  <121>                36  ''
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 199        28  LOAD_GLOBAL              E_INVALIDARG
               30  ROT_FOUR         
               32  POP_EXCEPT       
               34  RETURN_VALUE     
               36  <48>             
             38_0  COME_FROM            14  '14'

 L. 202        38  LOAD_FAST                'pVar'
               40  LOAD_CONST               0
               42  BINARY_SUBSCR    
               44  STORE_FAST               'var'

 L. 203        46  LOAD_FAST                'var'
               48  LOAD_ATTR                vt
               50  STORE_FAST               'typecode'

 L. 204        52  LOAD_FAST                'val'
               54  LOAD_FAST                'var'
               56  STORE_ATTR               value

 L. 205        58  LOAD_FAST                'typecode'
               60  POP_JUMP_IF_FALSE    72  'to 72'

 L. 206        62  LOAD_FAST                'var'
               64  LOAD_METHOD              ChangeType
               66  LOAD_FAST                'typecode'
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          
             72_0  COME_FROM            60  '60'

 L. 207        72  LOAD_GLOBAL              S_OK
               74  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 20

    def Write(self, this, name, var):
        val = var[0].value
        self.values[name] = val
        return S_OK