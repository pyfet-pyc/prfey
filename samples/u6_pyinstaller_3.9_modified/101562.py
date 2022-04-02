# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: comtypes\safearray.py
import threading, array
from ctypes import POINTER, Structure, byref, cast, c_long, memmove, pointer, sizeof
from comtypes import _safearray, IUnknown, com_interface_registry, npsupport
from comtypes.patcher import Patch
numpy = npsupport.numpy
_safearray_type_cache = {}

class _SafeArrayAsNdArrayContextManager(object):
    __doc__ = 'Context manager allowing safe arrays to be extracted as ndarrays.\n\n    This is thread-safe.\n\n    Example\n    -------\n\n    This works in python >= 2.5\n    >>> with safearray_as_ndarray:\n    >>>     my_arr = com_object.AsSafeArray\n    >>> type(my_arr)\n    numpy.ndarray\n\n    '
    thread_local = threading.local()

    def __enter__--- This code section failed: ---

 L.  30         0  SETUP_FINALLY        22  'to 22'

 L.  31         2  LOAD_FAST                'self'
                4  LOAD_ATTR                thread_local
                6  DUP_TOP          
                8  LOAD_ATTR                count
               10  LOAD_CONST               1
               12  INPLACE_ADD      
               14  ROT_TWO          
               16  STORE_ATTR               count
               18  POP_BLOCK        
               20  JUMP_FORWARD         48  'to 48'
             22_0  COME_FROM_FINALLY     0  '0'

 L.  32        22  DUP_TOP          
               24  LOAD_GLOBAL              AttributeError
               26  <121>                46  ''
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L.  33        34  LOAD_CONST               1
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                thread_local
               40  STORE_ATTR               count
               42  POP_EXCEPT       
               44  JUMP_FORWARD         48  'to 48'
               46  <48>             
             48_0  COME_FROM            44  '44'
             48_1  COME_FROM            20  '20'

Parse error at or near `<121>' instruction at offset 26

    def __exit__(self, exc_type, exc_value, traceback):
        self.thread_local.count -= 1

    def __bool__(self):
        """True if context manager is currently entered on given thread.

        """
        return bool(getattr(self.thread_local, 'count', 0))


safearray_as_ndarray = _SafeArrayAsNdArrayContextManager()

def _midlSAFEARRAY--- This code section failed: ---

 L.  57         0  SETUP_FINALLY        16  'to 16'

 L.  58         2  LOAD_GLOBAL              POINTER
                4  LOAD_GLOBAL              _safearray_type_cache
                6  LOAD_FAST                'itemtype'
                8  BINARY_SUBSCR    
               10  CALL_FUNCTION_1       1  ''
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L.  59        16  DUP_TOP          
               18  LOAD_GLOBAL              KeyError
               20  <121>                56  ''
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.  60        28  LOAD_GLOBAL              _make_safearray_type
               30  LOAD_FAST                'itemtype'
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'sa_type'

 L.  61        36  LOAD_FAST                'sa_type'
               38  LOAD_GLOBAL              _safearray_type_cache
               40  LOAD_FAST                'itemtype'
               42  STORE_SUBSCR     

 L.  62        44  LOAD_GLOBAL              POINTER
               46  LOAD_FAST                'sa_type'
               48  CALL_FUNCTION_1       1  ''
               50  ROT_FOUR         
               52  POP_EXCEPT       
               54  RETURN_VALUE     
               56  <48>             

Parse error at or near `<121>' instruction at offset 20


def _make_safearray_type--- This code section failed: ---

 L.  67         0  LOAD_CONST               0
                2  LOAD_CONST               ('_ctype_to_vartype', 'VT_RECORD', 'VT_UNKNOWN', 'IDispatch', 'VT_DISPATCH')
                4  IMPORT_NAME_ATTR         comtypes.automation
                6  IMPORT_FROM              _ctype_to_vartype
                8  STORE_FAST               '_ctype_to_vartype'
               10  IMPORT_FROM              VT_RECORD
               12  STORE_DEREF              'VT_RECORD'
               14  IMPORT_FROM              VT_UNKNOWN
               16  STORE_FAST               'VT_UNKNOWN'
               18  IMPORT_FROM              IDispatch
               20  STORE_FAST               'IDispatch'
               22  IMPORT_FROM              VT_DISPATCH
               24  STORE_FAST               'VT_DISPATCH'
               26  POP_TOP          

 L.  70        28  LOAD_GLOBAL              type
               30  LOAD_GLOBAL              _safearray
               32  LOAD_ATTR                tagSAFEARRAY
               34  CALL_FUNCTION_1       1  ''
               36  STORE_FAST               'meta'

 L.  71        38  LOAD_FAST                'meta'
               40  LOAD_METHOD              __new__
               42  LOAD_FAST                'meta'

 L.  72        44  LOAD_STR                 'SAFEARRAY_%s'
               46  LOAD_DEREF               'itemtype'
               48  LOAD_ATTR                __name__
               50  BINARY_MODULO    

 L.  73        52  LOAD_GLOBAL              _safearray
               54  LOAD_ATTR                tagSAFEARRAY
               56  BUILD_TUPLE_1         1 
               58  BUILD_MAP_0           0 

 L.  71        60  CALL_METHOD_4         4  ''
               62  STORE_DEREF              'sa_type'

 L.  75        64  SETUP_FINALLY        82  'to 82'

 L.  76        66  LOAD_FAST                '_ctype_to_vartype'
               68  LOAD_DEREF               'itemtype'
               70  BINARY_SUBSCR    
               72  STORE_DEREF              'vartype'

 L.  77        74  LOAD_CONST               None
               76  STORE_DEREF              'extra'
               78  POP_BLOCK        
               80  JUMP_FORWARD        238  'to 238'
             82_0  COME_FROM_FINALLY    64  '64'

 L.  78        82  DUP_TOP          
               84  LOAD_GLOBAL              KeyError
               86  <121>               236  ''
               88  POP_TOP          
               90  POP_TOP          
               92  POP_TOP          

 L.  79        94  LOAD_GLOBAL              issubclass
               96  LOAD_DEREF               'itemtype'
               98  LOAD_GLOBAL              Structure
              100  CALL_FUNCTION_2       2  ''
              102  POP_JUMP_IF_FALSE   164  'to 164'

 L.  80       104  SETUP_FINALLY       116  'to 116'

 L.  81       106  LOAD_DEREF               'itemtype'
              108  LOAD_ATTR                _recordinfo_
              110  STORE_FAST               'guids'
              112  POP_BLOCK        
              114  JUMP_FORWARD        138  'to 138'
            116_0  COME_FROM_FINALLY   104  '104'

 L.  82       116  DUP_TOP          
              118  LOAD_GLOBAL              AttributeError
              120  <121>               136  ''
              122  POP_TOP          
              124  POP_TOP          
              126  POP_TOP          

 L.  83       128  LOAD_CONST               None
              130  STORE_DEREF              'extra'
              132  POP_EXCEPT       
              134  JUMP_FORWARD        158  'to 158'
              136  <48>             
            138_0  COME_FROM           114  '114'

 L.  85       138  LOAD_CONST               0
              140  LOAD_CONST               ('GetRecordInfoFromGuids',)
              142  IMPORT_NAME_ATTR         comtypes.typeinfo
              144  IMPORT_FROM              GetRecordInfoFromGuids
              146  STORE_FAST               'GetRecordInfoFromGuids'
              148  POP_TOP          

 L.  86       150  LOAD_FAST                'GetRecordInfoFromGuids'
              152  LOAD_FAST                'guids'
              154  CALL_FUNCTION_EX      0  'positional arguments only'
              156  STORE_DEREF              'extra'
            158_0  COME_FROM           134  '134'

 L.  87       158  LOAD_DEREF               'VT_RECORD'
              160  STORE_DEREF              'vartype'
              162  JUMP_FORWARD        232  'to 232'
            164_0  COME_FROM           102  '102'

 L.  88       164  LOAD_GLOBAL              issubclass
              166  LOAD_DEREF               'itemtype'
              168  LOAD_GLOBAL              POINTER
              170  LOAD_FAST                'IDispatch'
              172  CALL_FUNCTION_1       1  ''
              174  CALL_FUNCTION_2       2  ''
              176  POP_JUMP_IF_FALSE   194  'to 194'

 L.  89       178  LOAD_FAST                'VT_DISPATCH'
              180  STORE_DEREF              'vartype'

 L.  90       182  LOAD_GLOBAL              pointer
              184  LOAD_DEREF               'itemtype'
              186  LOAD_ATTR                _iid_
              188  CALL_FUNCTION_1       1  ''
              190  STORE_DEREF              'extra'
              192  JUMP_FORWARD        232  'to 232'
            194_0  COME_FROM           176  '176'

 L.  91       194  LOAD_GLOBAL              issubclass
              196  LOAD_DEREF               'itemtype'
              198  LOAD_GLOBAL              POINTER
              200  LOAD_GLOBAL              IUnknown
              202  CALL_FUNCTION_1       1  ''
              204  CALL_FUNCTION_2       2  ''
              206  POP_JUMP_IF_FALSE   224  'to 224'

 L.  92       208  LOAD_FAST                'VT_UNKNOWN'
              210  STORE_DEREF              'vartype'

 L.  93       212  LOAD_GLOBAL              pointer
              214  LOAD_DEREF               'itemtype'
              216  LOAD_ATTR                _iid_
              218  CALL_FUNCTION_1       1  ''
              220  STORE_DEREF              'extra'
              222  JUMP_FORWARD        232  'to 232'
            224_0  COME_FROM           206  '206'

 L.  95       224  LOAD_GLOBAL              TypeError
              226  LOAD_DEREF               'itemtype'
              228  CALL_FUNCTION_1       1  ''
              230  RAISE_VARARGS_1       1  'exception instance'
            232_0  COME_FROM           222  '222'
            232_1  COME_FROM           192  '192'
            232_2  COME_FROM           162  '162'
              232  POP_EXCEPT       
              234  JUMP_FORWARD        238  'to 238'
              236  <48>             
            238_0  COME_FROM           234  '234'
            238_1  COME_FROM            80  '80'

 L.  97       238  LOAD_GLOBAL              Patch
              240  LOAD_GLOBAL              POINTER
              242  LOAD_DEREF               'sa_type'
              244  CALL_FUNCTION_1       1  ''
              246  CALL_FUNCTION_1       1  ''

 L.  98       248  LOAD_BUILD_CLASS 
              250  LOAD_CLOSURE             'VT_RECORD'
              252  LOAD_CLOSURE             'extra'
              254  LOAD_CLOSURE             'itemtype'
              256  LOAD_CLOSURE             'vartype'
              258  BUILD_TUPLE_4         4 
              260  LOAD_CODE                <code_object _>
              262  LOAD_STR                 '_'
              264  MAKE_FUNCTION_8          'closure'
              266  LOAD_STR                 '_'
              268  LOAD_GLOBAL              object
              270  CALL_FUNCTION_3       3  ''
              272  CALL_FUNCTION_1       1  ''
              274  STORE_FAST               '_'

 L. 346       276  LOAD_GLOBAL              Patch
              278  LOAD_GLOBAL              POINTER
              280  LOAD_GLOBAL              POINTER
              282  LOAD_DEREF               'sa_type'
              284  CALL_FUNCTION_1       1  ''
              286  CALL_FUNCTION_1       1  ''
              288  CALL_FUNCTION_1       1  ''

 L. 347       290  LOAD_BUILD_CLASS 
              292  LOAD_CLOSURE             'extra'
              294  LOAD_CLOSURE             'sa_type'
              296  BUILD_TUPLE_2         2 
              298  LOAD_CODE                <code_object __>
              300  LOAD_STR                 '__'
              302  MAKE_FUNCTION_8          'closure'
              304  LOAD_STR                 '__'
              306  LOAD_GLOBAL              object
              308  CALL_FUNCTION_3       3  ''
              310  CALL_FUNCTION_1       1  ''
              312  STORE_FAST               '__'

 L. 362       314  LOAD_DEREF               'sa_type'
              316  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 86


def _ndarray_to_variant_array--- This code section failed: ---

 L. 368         0  LOAD_GLOBAL              npsupport
                2  LOAD_ATTR                VARIANT_dtype
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    22  'to 22'

 L. 369        10  LOAD_STR                 'VARIANT ndarrays require NumPy 1.7 or newer.'
               12  STORE_FAST               'msg'

 L. 370        14  LOAD_GLOBAL              RuntimeError
               16  LOAD_FAST                'msg'
               18  CALL_FUNCTION_1       1  ''
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM             8  '8'

 L. 373        22  LOAD_GLOBAL              numpy
               24  LOAD_METHOD              issubdtype
               26  LOAD_FAST                'value'
               28  LOAD_ATTR                dtype
               30  LOAD_GLOBAL              npsupport
               32  LOAD_ATTR                datetime64
               34  CALL_METHOD_2         2  ''
               36  POP_JUMP_IF_FALSE    46  'to 46'

 L. 374        38  LOAD_GLOBAL              _datetime64_ndarray_to_variant_array
               40  LOAD_FAST                'value'
               42  CALL_FUNCTION_1       1  ''
               44  RETURN_VALUE     
             46_0  COME_FROM            36  '36'

 L. 376        46  LOAD_CONST               0
               48  LOAD_CONST               ('VARIANT',)
               50  IMPORT_NAME_ATTR         comtypes.automation
               52  IMPORT_FROM              VARIANT
               54  STORE_DEREF              'VARIANT'
               56  POP_TOP          

 L. 378        58  LOAD_GLOBAL              numpy
               60  LOAD_ATTR                zeros
               62  LOAD_FAST                'value'
               64  LOAD_ATTR                shape
               66  LOAD_GLOBAL              npsupport
               68  LOAD_ATTR                VARIANT_dtype
               70  LOAD_STR                 'F'
               72  LOAD_CONST               ('order',)
               74  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               76  STORE_FAST               'varr'

 L. 380        78  LOAD_CLOSURE             'VARIANT'
               80  BUILD_TUPLE_1         1 
               82  LOAD_LISTCOMP            '<code_object <listcomp>>'
               84  LOAD_STR                 '_ndarray_to_variant_array.<locals>.<listcomp>'
               86  MAKE_FUNCTION_8          'closure'
               88  LOAD_FAST                'value'
               90  LOAD_ATTR                flat
               92  GET_ITER         
               94  CALL_FUNCTION_1       1  ''
               96  LOAD_FAST                'varr'
               98  STORE_ATTR               flat

 L. 381       100  LOAD_FAST                'varr'
              102  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _datetime64_ndarray_to_variant_array(value):
    """ Convert an ndarray of datetime64 to VARIANT_dtype array """
    from comtypes.automation import VT_DATE
    value = numpy.arrayvalue'datetime64[ns]'
    value = value - npsupport.com_null_date64
    value = value / numpy.timedelta641'D'
    varr = numpy.zeros((value.shape), (npsupport.VARIANT_dtype), order='F')
    varr['vt'] = VT_DATE
    varr['_']['VT_R8'].flat = value.flat
    return varr