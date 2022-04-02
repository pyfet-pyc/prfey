# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: comtypes\_meta.py
from ctypes import POINTER, c_void_p, cast
import comtypes

def _wrap_coclass(self):
    itf = self._com_interfaces_[0]
    punk = cast(self, POINTER(itf))
    result = punk.QueryInterface(itf)
    result.__dict__['__clsid'] = str(self._reg_clsid_)
    return result


def _coclass_from_param(cls, obj):
    if isinstance(obj, (cls._com_interfaces_[0], cls)):
        return obj
    raise TypeError(obj)


class _coclass_meta(type):

    def __new__--- This code section failed: ---

 L.  42         0  LOAD_GLOBAL              type
                2  LOAD_METHOD              __new__
                4  LOAD_FAST                'cls'
                6  LOAD_FAST                'name'
                8  LOAD_FAST                'bases'
               10  LOAD_FAST                'namespace'
               12  CALL_METHOD_4         4  ''
               14  STORE_FAST               'klass'

 L.  43        16  LOAD_FAST                'bases'
               18  LOAD_GLOBAL              object
               20  BUILD_TUPLE_1         1 
               22  COMPARE_OP               ==
               24  POP_JUMP_IF_FALSE    30  'to 30'

 L.  44        26  LOAD_FAST                'klass'
               28  RETURN_VALUE     
             30_0  COME_FROM            24  '24'

 L.  46        30  LOAD_STR                 '_reg_clsid_'
               32  LOAD_FAST                'namespace'
               34  <118>                 0  ''
               36  POP_JUMP_IF_FALSE    60  'to 60'

 L.  47        38  LOAD_FAST                'namespace'
               40  LOAD_STR                 '_reg_clsid_'
               42  BINARY_SUBSCR    
               44  STORE_FAST               'clsid'

 L.  48        46  LOAD_FAST                'klass'
               48  LOAD_GLOBAL              comtypes
               50  LOAD_ATTR                com_coclass_registry
               52  LOAD_GLOBAL              str
               54  LOAD_FAST                'clsid'
               56  CALL_FUNCTION_1       1  ''
               58  STORE_SUBSCR     
             60_0  COME_FROM            36  '36'

 L.  49        60  LOAD_GLOBAL              _coclass_pointer_meta
               62  LOAD_STR                 'POINTER(%s)'
               64  LOAD_FAST                'klass'
               66  LOAD_ATTR                __name__
               68  BINARY_MODULO    

 L.  50        70  LOAD_FAST                'klass'
               72  LOAD_GLOBAL              c_void_p
               74  BUILD_TUPLE_2         2 

 L.  51        76  LOAD_GLOBAL              _wrap_coclass

 L.  52        78  LOAD_GLOBAL              classmethod
               80  LOAD_GLOBAL              _coclass_from_param
               82  CALL_FUNCTION_1       1  ''

 L.  51        84  LOAD_CONST               ('__ctypes_from_outparam__', 'from_param')
               86  BUILD_CONST_KEY_MAP_2     2 

 L.  49        88  CALL_FUNCTION_3       3  ''
               90  STORE_FAST               'PTR'

 L.  54        92  LOAD_CONST               0
               94  LOAD_CONST               ('_pointer_type_cache',)
               96  IMPORT_NAME              ctypes
               98  IMPORT_FROM              _pointer_type_cache
              100  STORE_FAST               '_pointer_type_cache'
              102  POP_TOP          

 L.  55       104  LOAD_FAST                'PTR'
              106  LOAD_FAST                '_pointer_type_cache'
              108  LOAD_FAST                'klass'
              110  STORE_SUBSCR     

 L.  57       112  LOAD_FAST                'klass'
              114  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 34


class _coclass_pointer_meta(type(c_void_p), _coclass_meta):
    pass