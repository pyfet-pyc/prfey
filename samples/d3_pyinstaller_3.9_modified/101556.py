# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: comtypes\GUID.py
from ctypes import *
import sys
if sys.version_info >= (2, 6):

    def binary(obj):
        return bytes(obj)


else:

    def binary(obj):
        return buffer(obj)


BYTE = c_byte
WORD = c_ushort
DWORD = c_ulong
_ole32 = oledll.ole32
_StringFromCLSID = _ole32.StringFromCLSID
_CoTaskMemFree = windll.ole32.CoTaskMemFree
_ProgIDFromCLSID = _ole32.ProgIDFromCLSID
_CLSIDFromString = _ole32.CLSIDFromString
_CLSIDFromProgID = _ole32.CLSIDFromProgID
_CoCreateGuid = _ole32.CoCreateGuid

class GUID(Structure):
    _fields_ = [
     (
      'Data1', DWORD),
     (
      'Data2', WORD),
     (
      'Data3', WORD),
     (
      'Data4', BYTE * 8)]

    def __init__--- This code section failed: ---

 L.  34         0  LOAD_FAST                'name'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    26  'to 26'

 L.  35         8  LOAD_GLOBAL              _CLSIDFromString
               10  LOAD_GLOBAL              str
               12  LOAD_FAST                'name'
               14  CALL_FUNCTION_1       1  ''
               16  LOAD_GLOBAL              byref
               18  LOAD_FAST                'self'
               20  CALL_FUNCTION_1       1  ''
               22  CALL_FUNCTION_2       2  ''
               24  POP_TOP          
             26_0  COME_FROM             6  '6'

Parse error at or near `None' instruction at offset -1

    def __repr__(self):
        return 'GUID("%s")' % str(self)

    def __unicode__(self):
        p = c_wchar_p()
        _StringFromCLSIDbyref(self)byref(p)
        result = p.value
        _CoTaskMemFree(p)
        return result

    __str__ = __unicode__

    def __cmp__(self, other):
        if isinstanceotherGUID:
            return cmpbinary(self)binary(other)
        return -1

    def __bool__(self):
        return self != GUID_null

    def __eq__(self, other):
        return isinstanceotherGUID and binary(self) == binary(other)

    def __hash__(self):
        return hash(binary(self))

    def copy(self):
        return GUID(str(self))

    def from_progid(cls, progid):
        """Get guid from progid, ...
        """
        if hasattrprogid'_reg_clsid_':
            progid = progid._reg_clsid_
        if isinstanceprogidcls:
            return progid
        if isinstanceprogidstr:
            if progid.startswith('{'):
                return cls(progid)
            inst = cls()
            _CLSIDFromProgIDstr(progid)byref(inst)
            return inst
        raise TypeError('Cannot construct guid from %r' % progid)

    from_progid = classmethod(from_progid)

    def as_progid(self):
        """Convert a GUID into a progid"""
        progid = c_wchar_p()
        _ProgIDFromCLSIDbyref(self)byref(progid)
        result = progid.value
        _CoTaskMemFree(progid)
        return result

    def create_new(cls):
        """Create a brand new guid"""
        guid = cls()
        _CoCreateGuid(byref(guid))
        return guid

    create_new = classmethod(create_new)


GUID_null = GUID()
__all__ = [
 'GUID']