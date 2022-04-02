# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: comtypes\client\dynamic.py
import ctypes, comtypes.automation, comtypes.typeinfo, comtypes.client, comtypes.client.lazybind
from comtypes import COMError, IUnknown, _is_object
import comtypes.hresult as hres
ERRORS_BAD_CONTEXT = [
 hres.DISP_E_MEMBERNOTFOUND,
 hres.DISP_E_BADPARAMCOUNT,
 hres.DISP_E_PARAMNOTOPTIONAL,
 hres.DISP_E_TYPEMISMATCH,
 hres.E_INVALIDARG]

def Dispatch--- This code section failed: ---

 L.  24         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'obj'
                4  LOAD_GLOBAL              _Dispatch
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L.  25        10  LOAD_FAST                'obj'
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L.  26        14  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'obj'
               18  LOAD_GLOBAL              ctypes
               20  LOAD_METHOD              POINTER
               22  LOAD_GLOBAL              comtypes
               24  LOAD_ATTR                automation
               26  LOAD_ATTR                IDispatch
               28  CALL_METHOD_1         1  ''
               30  CALL_FUNCTION_2       2  ''
               32  POP_JUMP_IF_FALSE    98  'to 98'

 L.  27        34  SETUP_FINALLY        50  'to 50'

 L.  28        36  LOAD_FAST                'obj'
               38  LOAD_METHOD              GetTypeInfo
               40  LOAD_CONST               0
               42  CALL_METHOD_1         1  ''
               44  STORE_FAST               'tinfo'
               46  POP_BLOCK        
               48  JUMP_FORWARD         82  'to 82'
             50_0  COME_FROM_FINALLY    34  '34'

 L.  29        50  DUP_TOP          
               52  LOAD_GLOBAL              comtypes
               54  LOAD_ATTR                COMError
               56  LOAD_GLOBAL              WindowsError
               58  BUILD_TUPLE_2         2 
               60  <121>                80  ''
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L.  30        68  LOAD_GLOBAL              _Dispatch
               70  LOAD_FAST                'obj'
               72  CALL_FUNCTION_1       1  ''
               74  ROT_FOUR         
               76  POP_EXCEPT       
               78  RETURN_VALUE     
               80  <48>             
             82_0  COME_FROM            48  '48'

 L.  31        82  LOAD_GLOBAL              comtypes
               84  LOAD_ATTR                client
               86  LOAD_ATTR                lazybind
               88  LOAD_METHOD              Dispatch
               90  LOAD_FAST                'obj'
               92  LOAD_FAST                'tinfo'
               94  CALL_METHOD_2         2  ''
               96  RETURN_VALUE     
             98_0  COME_FROM            32  '32'

 L.  32        98  LOAD_FAST                'obj'
              100  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 60


class MethodCaller:

    def __init__(self, _id, _obj):
        self._id = _id
        self._obj = _obj

    def __call__--- This code section failed: ---

 L.  42         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _obj
                4  LOAD_ATTR                _comobj
                6  LOAD_ATTR                Invoke
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                _id
               12  BUILD_LIST_1          1 
               14  LOAD_FAST                'args'
               16  CALL_FINALLY         19  'to 19'
               18  WITH_CLEANUP_FINISH
               20  CALL_FUNCTION_EX      0  'positional arguments only'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __getitem__--- This code section failed: ---

 L.  45         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _obj
                4  LOAD_ATTR                _comobj
                6  LOAD_ATTR                Invoke
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                _id
               12  BUILD_LIST_1          1 
               14  LOAD_FAST                'args'
               16  CALL_FINALLY         19  'to 19'
               18  WITH_CLEANUP_FINISH
               20  BUILD_MAP_0           0 

 L.  46        22  LOAD_GLOBAL              dict
               24  LOAD_GLOBAL              comtypes
               26  LOAD_ATTR                automation
               28  LOAD_ATTR                DISPATCH_PROPERTYGET
               30  LOAD_CONST               ('_invkind',)
               32  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L.  45        34  <164>                 1  ''
               36  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               38  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __setitem__--- This code section failed: ---

 L.  49         0  LOAD_GLOBAL              _is_object
                2  LOAD_FAST                'args'
                4  LOAD_CONST               -1
                6  BINARY_SUBSCR    
                8  CALL_FUNCTION_1       1  ''
               10  POP_JUMP_IF_FALSE    54  'to 54'

 L.  50        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _obj
               16  LOAD_ATTR                _comobj
               18  LOAD_ATTR                Invoke
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                _id
               24  BUILD_LIST_1          1 
               26  LOAD_FAST                'args'
               28  CALL_FINALLY         31  'to 31'
               30  WITH_CLEANUP_FINISH
               32  BUILD_MAP_0           0 

 L.  51        34  LOAD_GLOBAL              dict
               36  LOAD_GLOBAL              comtypes
               38  LOAD_ATTR                automation
               40  LOAD_ATTR                DISPATCH_PROPERTYPUTREF
               42  LOAD_CONST               ('_invkind',)
               44  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L.  50        46  <164>                 1  ''
               48  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               50  POP_TOP          
               52  JUMP_FORWARD         94  'to 94'
             54_0  COME_FROM            10  '10'

 L.  53        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _obj
               58  LOAD_ATTR                _comobj
               60  LOAD_ATTR                Invoke
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                _id
               66  BUILD_LIST_1          1 
               68  LOAD_FAST                'args'
               70  CALL_FINALLY         73  'to 73'
               72  WITH_CLEANUP_FINISH
               74  BUILD_MAP_0           0 

 L.  54        76  LOAD_GLOBAL              dict
               78  LOAD_GLOBAL              comtypes
               80  LOAD_ATTR                automation
               82  LOAD_ATTR                DISPATCH_PROPERTYPUT
               84  LOAD_CONST               ('_invkind',)
               86  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L.  53        88  <164>                 1  ''
               90  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               92  POP_TOP          
             94_0  COME_FROM            52  '52'

Parse error at or near `CALL_FINALLY' instruction at offset 28


class _Dispatch(object):

    def __init__(self, comobj):
        self.__dict__['_comobj'] = comobj
        self.__dict__['_ids'] = {}
        self.__dict__['_methods'] = set()

    def __enum(self):
        e = self._comobj.Invoke(-4)
        return e.QueryInterfacecomtypes.automation.IEnumVARIANT

    def __cmp__(self, other):
        if not isinstance(other, _Dispatch):
            return 1
        return cmp(self._comobj, other._comobj)

    def __hash__(self):
        return hash(self._comobj)

    def __getitem__(self, index):
        enum = self._Dispatch__enum()
        if index > 0:
            if 0 != enum.Skipindex:
                raise IndexError('index out of range')
        item, fetched = enum.Next1
        if not fetched:
            raise IndexError('index out of range')
        return item

    def QueryInterface(self, *args):
        """QueryInterface is forwarded to the real com object."""
        return (self._comobj.QueryInterface)(*args)

    def _FlagAsMethod(self, *names):
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
        self._methods.updatenames

    def __getattr__--- This code section failed: ---

 L. 104         0  LOAD_FAST                'name'
                2  LOAD_METHOD              startswith
                4  LOAD_STR                 '__'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_FALSE    28  'to 28'
               10  LOAD_FAST                'name'
               12  LOAD_METHOD              endswith
               14  LOAD_STR                 '__'
               16  CALL_METHOD_1         1  ''
               18  POP_JUMP_IF_FALSE    28  'to 28'

 L. 105        20  LOAD_GLOBAL              AttributeError
               22  LOAD_FAST                'name'
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            18  '18'
             28_1  COME_FROM             8  '8'

 L. 108        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _ids
               32  LOAD_METHOD              get
               34  LOAD_FAST                'name'
               36  CALL_METHOD_1         1  ''
               38  STORE_FAST               'dispid'

 L. 109        40  LOAD_FAST                'dispid'
               42  POP_JUMP_IF_TRUE     70  'to 70'

 L. 110        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _comobj
               48  LOAD_METHOD              GetIDsOfNames
               50  LOAD_FAST                'name'
               52  CALL_METHOD_1         1  ''
               54  LOAD_CONST               0
               56  BINARY_SUBSCR    
               58  STORE_FAST               'dispid'

 L. 111        60  LOAD_FAST                'dispid'
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                _ids
               66  LOAD_FAST                'name'
               68  STORE_SUBSCR     
             70_0  COME_FROM            42  '42'

 L. 113        70  LOAD_FAST                'name'
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                _methods
               76  <118>                 0  ''
               78  POP_JUMP_IF_FALSE   104  'to 104'

 L. 114        80  LOAD_GLOBAL              MethodCaller
               82  LOAD_FAST                'dispid'
               84  LOAD_FAST                'self'
               86  CALL_FUNCTION_2       2  ''
               88  STORE_FAST               'result'

 L. 115        90  LOAD_FAST                'result'
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                __dict__
               96  LOAD_FAST                'name'
               98  STORE_SUBSCR     

 L. 116       100  LOAD_FAST                'result'
              102  RETURN_VALUE     
            104_0  COME_FROM            78  '78'

 L. 118       104  LOAD_GLOBAL              comtypes
              106  LOAD_ATTR                automation
              108  LOAD_ATTR                DISPATCH_PROPERTYGET
              110  STORE_FAST               'flags'

 L. 119       112  SETUP_FINALLY       134  'to 134'

 L. 120       114  LOAD_FAST                'self'
              116  LOAD_ATTR                _comobj
              118  LOAD_ATTR                Invoke
              120  LOAD_FAST                'dispid'
              122  LOAD_FAST                'flags'
              124  LOAD_CONST               ('_invkind',)
              126  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              128  STORE_FAST               'result'
              130  POP_BLOCK        
              132  JUMP_FORWARD        226  'to 226'
            134_0  COME_FROM_FINALLY   112  '112'

 L. 121       134  DUP_TOP          
              136  LOAD_GLOBAL              COMError
              138  <121>               212  ''
              140  POP_TOP          
              142  STORE_FAST               'err'
              144  POP_TOP          
              146  SETUP_FINALLY       204  'to 204'

 L. 122       148  LOAD_FAST                'err'
              150  LOAD_ATTR                args
              152  UNPACK_SEQUENCE_3     3 
              154  STORE_FAST               'hresult'
              156  STORE_FAST               'text'
              158  STORE_FAST               'details'

 L. 123       160  LOAD_FAST                'hresult'
              162  LOAD_GLOBAL              ERRORS_BAD_CONTEXT
              164  <118>                 0  ''
              166  POP_JUMP_IF_FALSE   190  'to 190'

 L. 124       168  LOAD_GLOBAL              MethodCaller
              170  LOAD_FAST                'dispid'
              172  LOAD_FAST                'self'
              174  CALL_FUNCTION_2       2  ''
              176  STORE_FAST               'result'

 L. 125       178  LOAD_FAST                'result'
              180  LOAD_FAST                'self'
              182  LOAD_ATTR                __dict__
              184  LOAD_FAST                'name'
              186  STORE_SUBSCR     
              188  JUMP_FORWARD        192  'to 192'
            190_0  COME_FROM           166  '166'

 L. 128       190  RAISE_VARARGS_0       0  'reraise'
            192_0  COME_FROM           188  '188'
              192  POP_BLOCK        
              194  POP_EXCEPT       
              196  LOAD_CONST               None
              198  STORE_FAST               'err'
              200  DELETE_FAST              'err'
              202  JUMP_FORWARD        226  'to 226'
            204_0  COME_FROM_FINALLY   146  '146'
              204  LOAD_CONST               None
              206  STORE_FAST               'err'
              208  DELETE_FAST              'err'
              210  <48>             

 L. 129       212  POP_TOP          
              214  POP_TOP          
              216  POP_TOP          

 L. 131       218  RAISE_VARARGS_0       0  'reraise'
              220  POP_EXCEPT       
              222  JUMP_FORWARD        226  'to 226'
              224  <48>             
            226_0  COME_FROM           222  '222'
            226_1  COME_FROM           202  '202'
            226_2  COME_FROM           132  '132'

 L. 133       226  LOAD_FAST                'result'
              228  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 76

    def __setattr__(self, name, value):
        dispid = self._ids.getname
        if not dispid:
            dispid = self._comobj.GetIDsOfNamesname[0]
            self._ids[name] = dispid
        flags = 8 if _is_object(value) else 4
        return self._comobj.Invoke(dispid, value, _invkind=flags)

    def __iter__(self):
        return _Collection(self._Dispatch__enum())


class _Collection(object):

    def __init__(self, enum):
        self.enum = enum

    def __next__(self):
        item, fetched = self.enum.Next1
        if fetched:
            return item
        raise StopIteration

    def __iter__(self):
        return self


__all__ = [
 'Dispatch']