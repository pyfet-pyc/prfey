# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: win32com\client\__init__.py
import pythoncom
from . import dynamic
from . import gencache
import sys, pywintypes
_PyIDispatchType = pythoncom.TypeIIDs[pythoncom.IID_IDispatch]

def __WrapDispatch--- This code section failed: ---

 L.  25         0  LOAD_FAST                'UnicodeToString'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  <74>             
               10  LOAD_STR                 'this is deprecated and will go away'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L.  26        16  LOAD_FAST                'resultCLSID'
               18  LOAD_CONST               None
               20  <117>                 0  ''
               22  POP_JUMP_IF_FALSE    86  'to 86'

 L.  27        24  SETUP_FINALLY        62  'to 62'

 L.  28        26  LOAD_FAST                'dispatch'
               28  LOAD_METHOD              GetTypeInfo
               30  CALL_METHOD_0         0  ''
               32  STORE_FAST               'typeinfo'

 L.  29        34  LOAD_FAST                'typeinfo'
               36  LOAD_CONST               None
               38  <117>                 1  ''
               40  POP_JUMP_IF_FALSE    58  'to 58'

 L.  30        42  LOAD_GLOBAL              str
               44  LOAD_FAST                'typeinfo'
               46  LOAD_METHOD              GetTypeAttr
               48  CALL_METHOD_0         0  ''
               50  LOAD_CONST               0
               52  BINARY_SUBSCR    
               54  CALL_FUNCTION_1       1  ''
               56  STORE_FAST               'resultCLSID'
             58_0  COME_FROM            40  '40'
               58  POP_BLOCK        
               60  JUMP_FORWARD         86  'to 86'
             62_0  COME_FROM_FINALLY    24  '24'

 L.  31        62  DUP_TOP          
               64  LOAD_GLOBAL              pythoncom
               66  LOAD_ATTR                com_error
               68  LOAD_GLOBAL              AttributeError
               70  BUILD_TUPLE_2         2 
               72  <121>                84  ''
               74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          

 L.  32        80  POP_EXCEPT       
               82  JUMP_FORWARD         86  'to 86'
               84  <48>             
             86_0  COME_FROM            82  '82'
             86_1  COME_FROM            60  '60'
             86_2  COME_FROM            22  '22'

 L.  33        86  LOAD_FAST                'resultCLSID'
               88  LOAD_CONST               None
               90  <117>                 1  ''
               92  POP_JUMP_IF_FALSE   132  'to 132'

 L.  34        94  LOAD_CONST               1
               96  LOAD_CONST               ('gencache',)
               98  IMPORT_NAME              
              100  IMPORT_FROM              gencache
              102  STORE_FAST               'gencache'
              104  POP_TOP          

 L.  37       106  LOAD_FAST                'gencache'
              108  LOAD_METHOD              GetClassForCLSID
              110  LOAD_FAST                'resultCLSID'
              112  CALL_METHOD_1         1  ''
              114  STORE_FAST               'klass'

 L.  38       116  LOAD_FAST                'klass'
              118  LOAD_CONST               None
              120  <117>                 1  ''
              122  POP_JUMP_IF_FALSE   132  'to 132'

 L.  39       124  LOAD_FAST                'klass'
              126  LOAD_FAST                'dispatch'
              128  CALL_FUNCTION_1       1  ''
              130  RETURN_VALUE     
            132_0  COME_FROM           122  '122'
            132_1  COME_FROM            92  '92'

 L.  42       132  LOAD_FAST                'WrapperClass'
              134  LOAD_CONST               None
              136  <117>                 0  ''
              138  POP_JUMP_IF_FALSE   144  'to 144'
              140  LOAD_GLOBAL              CDispatch
              142  STORE_FAST               'WrapperClass'
            144_0  COME_FROM           138  '138'

 L.  43       144  LOAD_GLOBAL              dynamic
              146  LOAD_ATTR                Dispatch
              148  LOAD_FAST                'dispatch'
              150  LOAD_FAST                'userName'
              152  LOAD_FAST                'WrapperClass'
              154  LOAD_FAST                'typeinfo'
              156  LOAD_FAST                'clsctx'
              158  LOAD_CONST               ('clsctx',)
              160  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              162  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def GetObject--- This code section failed: ---

 L.  62         0  LOAD_FAST                'clsctx'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L.  63         8  LOAD_GLOBAL              pythoncom
               10  LOAD_ATTR                CLSCTX_ALL
               12  STORE_FAST               'clsctx'
             14_0  COME_FROM             6  '6'

 L.  65        14  LOAD_FAST                'Pathname'
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    30  'to 30'
               22  LOAD_FAST                'Class'
               24  LOAD_CONST               None
               26  <117>                 0  ''
               28  POP_JUMP_IF_TRUE     46  'to 46'
             30_0  COME_FROM            20  '20'

 L.  66        30  LOAD_FAST                'Pathname'
               32  LOAD_CONST               None
               34  <117>                 1  ''

 L.  65        36  POP_JUMP_IF_FALSE    54  'to 54'

 L.  66        38  LOAD_FAST                'Class'
               40  LOAD_CONST               None
               42  <117>                 1  ''

 L.  65        44  POP_JUMP_IF_FALSE    54  'to 54'
             46_0  COME_FROM            28  '28'

 L.  67        46  LOAD_GLOBAL              ValueError
               48  LOAD_STR                 'You must specify a value for Pathname or Class, but not both.'
               50  CALL_FUNCTION_1       1  ''
               52  RAISE_VARARGS_1       1  'exception instance'
             54_0  COME_FROM            44  '44'
             54_1  COME_FROM            36  '36'

 L.  69        54  LOAD_FAST                'Class'
               56  LOAD_CONST               None
               58  <117>                 1  ''
               60  POP_JUMP_IF_FALSE    72  'to 72'

 L.  70        62  LOAD_GLOBAL              GetActiveObject
               64  LOAD_FAST                'Class'
               66  LOAD_FAST                'clsctx'
               68  CALL_FUNCTION_2       2  ''
               70  RETURN_VALUE     
             72_0  COME_FROM            60  '60'

 L.  72        72  LOAD_GLOBAL              Moniker
               74  LOAD_FAST                'Pathname'
               76  LOAD_FAST                'clsctx'
               78  CALL_FUNCTION_2       2  ''
               80  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1


def GetActiveObject(Class, clsctx=pythoncom.CLSCTX_ALL):
    """
    Python friendly version of GetObject's ProgID/CLSID functionality.
  """
    resultCLSID = pywintypes.IIDClass
    dispatch = pythoncom.GetActiveObjectresultCLSID
    dispatch = dispatch.QueryInterfacepythoncom.IID_IDispatch
    return __WrapDispatch(dispatch, Class, resultCLSID=resultCLSID, clsctx=clsctx)


def Moniker(Pathname, clsctx=pythoncom.CLSCTX_ALL):
    """
    Python friendly version of GetObject's moniker functionality.
  """
    moniker, i, bindCtx = pythoncom.MkParseDisplayNamePathname
    dispatch = moniker.BindToObject(bindCtx, None, pythoncom.IID_IDispatch)
    return __WrapDispatch(dispatch, Pathname, clsctx=clsctx)


def Dispatch--- This code section failed: ---

 L.  94         0  LOAD_FAST                'UnicodeToString'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  <74>             
               10  LOAD_STR                 'this is deprecated and will go away'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L.  95        16  LOAD_GLOBAL              dynamic
               18  LOAD_METHOD              _GetGoodDispatchAndUserName
               20  LOAD_FAST                'dispatch'
               22  LOAD_FAST                'userName'
               24  LOAD_FAST                'clsctx'
               26  CALL_METHOD_3         3  ''
               28  UNPACK_SEQUENCE_2     2 
               30  STORE_FAST               'dispatch'
               32  STORE_FAST               'userName'

 L.  96        34  LOAD_GLOBAL              __WrapDispatch
               36  LOAD_FAST                'dispatch'
               38  LOAD_FAST                'userName'
               40  LOAD_FAST                'resultCLSID'
               42  LOAD_FAST                'typeinfo'
               44  LOAD_FAST                'clsctx'
               46  LOAD_CONST               ('clsctx',)
               48  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               50  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def DispatchEx--- This code section failed: ---

 L. 101         0  LOAD_FAST                'UnicodeToString'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  <74>             
               10  LOAD_STR                 'this is deprecated and will go away'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 105        16  LOAD_FAST                'clsctx'
               18  LOAD_CONST               None
               20  <117>                 0  ''
               22  POP_JUMP_IF_FALSE    50  'to 50'

 L. 106        24  LOAD_GLOBAL              pythoncom
               26  LOAD_ATTR                CLSCTX_SERVER
               28  STORE_FAST               'clsctx'

 L. 107        30  LOAD_FAST                'machine'
               32  LOAD_CONST               None
               34  <117>                 1  ''
               36  POP_JUMP_IF_FALSE    50  'to 50'
               38  LOAD_FAST                'clsctx'
               40  LOAD_GLOBAL              pythoncom
               42  LOAD_ATTR                CLSCTX_INPROC
               44  UNARY_INVERT     
               46  BINARY_AND       
               48  STORE_FAST               'clsctx'
             50_0  COME_FROM            36  '36'
             50_1  COME_FROM            22  '22'

 L. 108        50  LOAD_FAST                'machine'
               52  LOAD_CONST               None
               54  <117>                 0  ''
               56  POP_JUMP_IF_FALSE    64  'to 64'

 L. 109        58  LOAD_CONST               None
               60  STORE_FAST               'serverInfo'
               62  JUMP_FORWARD         70  'to 70'
             64_0  COME_FROM            56  '56'

 L. 111        64  LOAD_FAST                'machine'
               66  BUILD_TUPLE_1         1 
               68  STORE_FAST               'serverInfo'
             70_0  COME_FROM            62  '62'

 L. 112        70  LOAD_FAST                'userName'
               72  LOAD_CONST               None
               74  <117>                 0  ''
               76  POP_JUMP_IF_FALSE    82  'to 82'
               78  LOAD_FAST                'clsid'
               80  STORE_FAST               'userName'
             82_0  COME_FROM            76  '76'

 L. 113        82  LOAD_GLOBAL              pythoncom
               84  LOAD_METHOD              CoCreateInstanceEx
               86  LOAD_FAST                'clsid'
               88  LOAD_CONST               None
               90  LOAD_FAST                'clsctx'
               92  LOAD_FAST                'serverInfo'
               94  LOAD_GLOBAL              pythoncom
               96  LOAD_ATTR                IID_IDispatch
               98  BUILD_TUPLE_1         1 
              100  CALL_METHOD_5         5  ''
              102  LOAD_CONST               0
              104  BINARY_SUBSCR    
              106  STORE_FAST               'dispatch'

 L. 114       108  LOAD_GLOBAL              Dispatch
              110  LOAD_FAST                'dispatch'
              112  LOAD_FAST                'userName'
              114  LOAD_FAST                'resultCLSID'
              116  LOAD_FAST                'typeinfo'
              118  LOAD_FAST                'clsctx'
              120  LOAD_CONST               ('clsctx',)
              122  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              124  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class CDispatch(dynamic.CDispatch):
    __doc__ = '\n    The dynamic class used as a last resort.\n    The purpose of this overriding of dynamic.CDispatch is to perpetuate the policy\n    of using the makepy generated wrapper Python class instead of dynamic.CDispatch\n    if/when possible.\n  '

    def _wrap_dispatch_--- This code section failed: ---

 L. 124         0  LOAD_FAST                'UnicodeToString'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  <74>             
               10  LOAD_STR                 'this is deprecated and will go away'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 125        16  LOAD_GLOBAL              Dispatch
               18  LOAD_FAST                'ob'
               20  LOAD_FAST                'userName'
               22  LOAD_FAST                'returnCLSID'
               24  LOAD_CONST               None
               26  CALL_FUNCTION_4       4  ''
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __dir__(self):
        return dynamic.CDispatch.__dir__self


def CastTo--- This code section failed: ---

 L. 132         0  LOAD_CONST               None
                2  STORE_FAST               'mod'

 L. 133         4  LOAD_FAST                'typelib'
                6  LOAD_CONST               None
                8  <117>                 1  ''
               10  POP_JUMP_IF_FALSE    78  'to 78'

 L. 134        12  LOAD_GLOBAL              gencache
               14  LOAD_METHOD              MakeModuleForTypelib
               16  LOAD_FAST                'typelib'
               18  LOAD_ATTR                clsid
               20  LOAD_FAST                'typelib'
               22  LOAD_ATTR                lcid
               24  LOAD_GLOBAL              int
               26  LOAD_FAST                'typelib'
               28  LOAD_ATTR                major
               30  LOAD_CONST               16
               32  CALL_FUNCTION_2       2  ''
               34  LOAD_GLOBAL              int
               36  LOAD_FAST                'typelib'
               38  LOAD_ATTR                minor
               40  LOAD_CONST               16
               42  CALL_FUNCTION_2       2  ''
               44  CALL_METHOD_4         4  ''
               46  STORE_FAST               'mod'

 L. 135        48  LOAD_GLOBAL              hasattr
               50  LOAD_FAST                'mod'
               52  LOAD_FAST                'target'
               54  CALL_FUNCTION_2       2  ''
               56  POP_JUMP_IF_TRUE    216  'to 216'

 L. 136        58  LOAD_GLOBAL              ValueError
               60  LOAD_STR                 "The interface name '%s' does not appear in the specified library %r"

 L. 137        62  LOAD_FAST                'target'
               64  LOAD_FAST                'typelib'
               66  LOAD_ATTR                ver_desc
               68  BUILD_TUPLE_2         2 

 L. 136        70  BINARY_MODULO    
               72  CALL_FUNCTION_1       1  ''
               74  RAISE_VARARGS_1       1  'exception instance'
               76  JUMP_FORWARD        216  'to 216'
             78_0  COME_FROM            10  '10'

 L. 139        78  LOAD_GLOBAL              hasattr
               80  LOAD_FAST                'target'
               82  LOAD_STR                 'index'
               84  CALL_FUNCTION_2       2  ''
               86  POP_JUMP_IF_FALSE   216  'to 216'

 L. 141        88  LOAD_STR                 'CLSID'
               90  LOAD_FAST                'ob'
               92  LOAD_ATTR                __class__
               94  LOAD_ATTR                __dict__
               96  <118>                 1  ''
               98  POP_JUMP_IF_FALSE   110  'to 110'

 L. 143       100  LOAD_GLOBAL              gencache
              102  LOAD_METHOD              EnsureDispatch
              104  LOAD_FAST                'ob'
              106  CALL_METHOD_1         1  ''
              108  STORE_FAST               'ob'
            110_0  COME_FROM            98  '98'

 L. 144       110  LOAD_STR                 'CLSID'
              112  LOAD_FAST                'ob'
              114  LOAD_ATTR                __class__
              116  LOAD_ATTR                __dict__
              118  <118>                 1  ''
              120  POP_JUMP_IF_FALSE   130  'to 130'

 L. 145       122  LOAD_GLOBAL              ValueError
              124  LOAD_STR                 'Must be a makepy-able object for this to work'
              126  CALL_FUNCTION_1       1  ''
              128  RAISE_VARARGS_1       1  'exception instance'
            130_0  COME_FROM           120  '120'

 L. 146       130  LOAD_FAST                'ob'
              132  LOAD_ATTR                CLSID
              134  STORE_FAST               'clsid'

 L. 154       136  LOAD_GLOBAL              gencache
              138  LOAD_METHOD              GetModuleForCLSID
              140  LOAD_FAST                'clsid'
              142  CALL_METHOD_1         1  ''
              144  STORE_FAST               'mod'

 L. 156       146  LOAD_GLOBAL              gencache
              148  LOAD_METHOD              GetModuleForTypelib
              150  LOAD_FAST                'mod'
              152  LOAD_ATTR                CLSID
              154  LOAD_FAST                'mod'
              156  LOAD_ATTR                LCID

 L. 157       158  LOAD_FAST                'mod'
              160  LOAD_ATTR                MajorVersion
              162  LOAD_FAST                'mod'
              164  LOAD_ATTR                MinorVersion

 L. 156       166  CALL_METHOD_4         4  ''
              168  STORE_FAST               'mod'

 L. 159       170  LOAD_FAST                'mod'
              172  LOAD_ATTR                NamesToIIDMap
              174  LOAD_METHOD              get
              176  LOAD_FAST                'target'
              178  CALL_METHOD_1         1  ''
              180  STORE_FAST               'target_clsid'

 L. 160       182  LOAD_FAST                'target_clsid'
              184  LOAD_CONST               None
              186  <117>                 0  ''
              188  POP_JUMP_IF_FALSE   206  'to 206'

 L. 161       190  LOAD_GLOBAL              ValueError
              192  LOAD_STR                 "The interface name '%s' does not appear in the same library as object '%r'"

 L. 162       194  LOAD_FAST                'target'
              196  LOAD_FAST                'ob'
              198  BUILD_TUPLE_2         2 

 L. 161       200  BINARY_MODULO    
              202  CALL_FUNCTION_1       1  ''
              204  RAISE_VARARGS_1       1  'exception instance'
            206_0  COME_FROM           188  '188'

 L. 163       206  LOAD_GLOBAL              gencache
              208  LOAD_METHOD              GetModuleForCLSID
              210  LOAD_FAST                'target_clsid'
              212  CALL_METHOD_1         1  ''
              214  STORE_FAST               'mod'
            216_0  COME_FROM            86  '86'
            216_1  COME_FROM            76  '76'
            216_2  COME_FROM            56  '56'

 L. 164       216  LOAD_FAST                'mod'
              218  LOAD_CONST               None
              220  <117>                 1  ''
              222  POP_JUMP_IF_FALSE   254  'to 254'

 L. 165       224  LOAD_GLOBAL              getattr
              226  LOAD_FAST                'mod'
              228  LOAD_FAST                'target'
              230  CALL_FUNCTION_2       2  ''
              232  STORE_FAST               'target_class'

 L. 167       234  LOAD_GLOBAL              getattr
              236  LOAD_FAST                'target_class'
              238  LOAD_STR                 'default_interface'
              240  LOAD_FAST                'target_class'
              242  CALL_FUNCTION_3       3  ''
              244  STORE_FAST               'target_class'

 L. 168       246  LOAD_FAST                'target_class'
              248  LOAD_FAST                'ob'
              250  CALL_FUNCTION_1       1  ''
              252  RETURN_VALUE     
            254_0  COME_FROM           222  '222'

 L. 169       254  LOAD_GLOBAL              ValueError
              256  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<117>' instruction at offset 8


class Constants:
    __doc__ = 'A container for generated COM constants.\n  '

    def __init__(self):
        self.__dicts__ = []

    def __getattr__--- This code section failed: ---

 L. 177         0  LOAD_FAST                'self'
                2  LOAD_ATTR                __dicts__
                4  GET_ITER         
              6_0  COME_FROM            16  '16'
                6  FOR_ITER             32  'to 32'
                8  STORE_FAST               'd'

 L. 178        10  LOAD_FAST                'a'
               12  LOAD_FAST                'd'
               14  <118>                 0  ''
               16  POP_JUMP_IF_FALSE     6  'to 6'

 L. 179        18  LOAD_FAST                'd'
               20  LOAD_FAST                'a'
               22  BINARY_SUBSCR    
               24  ROT_TWO          
               26  POP_TOP          
               28  RETURN_VALUE     
               30  JUMP_BACK             6  'to 6'

 L. 180        32  LOAD_GLOBAL              AttributeError
               34  LOAD_FAST                'a'
               36  CALL_FUNCTION_1       1  ''
               38  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<118>' instruction at offset 14


constants = Constants()

def _event_setattr_--- This code section failed: ---

 L. 188         0  SETUP_FINALLY        28  'to 28'

 L. 190         2  LOAD_FAST                'self'
                4  LOAD_ATTR                __class__
                6  LOAD_ATTR                __bases__
                8  LOAD_CONST               0
               10  BINARY_SUBSCR    
               12  LOAD_METHOD              __setattr__
               14  LOAD_FAST                'self'
               16  LOAD_FAST                'attr'
               18  LOAD_FAST                'val'
               20  CALL_METHOD_3         3  ''
               22  POP_TOP          
               24  POP_BLOCK        
               26  JUMP_FORWARD         56  'to 56'
             28_0  COME_FROM_FINALLY     0  '0'

 L. 191        28  DUP_TOP          
               30  LOAD_GLOBAL              AttributeError
               32  <121>                54  ''
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L. 193        40  LOAD_FAST                'val'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                __dict__
               46  LOAD_FAST                'attr'
               48  STORE_SUBSCR     
               50  POP_EXCEPT       
               52  JUMP_FORWARD         56  'to 56'
               54  <48>             
             56_0  COME_FROM            52  '52'
             56_1  COME_FROM            26  '26'

Parse error at or near `<121>' instruction at offset 32


class EventsProxy:

    def __init__(self, ob):
        self.__dict__['_obj_'] = ob

    def __del__--- This code section failed: ---

 L. 204         0  SETUP_FINALLY        16  'to 16'

 L. 207         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _obj_
                6  LOAD_METHOD              close
                8  CALL_METHOD_0         0  ''
               10  POP_TOP          
               12  POP_BLOCK        
               14  JUMP_FORWARD         36  'to 36'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 208        16  DUP_TOP          
               18  LOAD_GLOBAL              pythoncom
               20  LOAD_ATTR                com_error
               22  <121>                34  ''
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 209        30  POP_EXCEPT       
               32  JUMP_FORWARD         36  'to 36'
               34  <48>             
             36_0  COME_FROM            32  '32'
             36_1  COME_FROM            14  '14'

Parse error at or near `<121>' instruction at offset 22

    def __getattr__(self, attr):
        return getattr(self._obj_, attr)

    def __setattr__(self, attr, val):
        setattr(self._obj_, attr, val)


def DispatchWithEvents--- This code section failed: ---

 L. 255         0  LOAD_GLOBAL              Dispatch
                2  LOAD_FAST                'clsid'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'disp'

 L. 256         8  LOAD_FAST                'disp'
               10  LOAD_ATTR                __class__
               12  LOAD_ATTR                __dict__
               14  LOAD_METHOD              get
               16  LOAD_STR                 'CLSID'
               18  CALL_METHOD_1         1  ''
               20  POP_JUMP_IF_TRUE    150  'to 150'

 L. 257        22  SETUP_FINALLY       120  'to 120'

 L. 258        24  LOAD_FAST                'disp'
               26  LOAD_ATTR                _oleobj_
               28  LOAD_METHOD              GetTypeInfo
               30  CALL_METHOD_0         0  ''
               32  STORE_FAST               'ti'

 L. 259        34  LOAD_FAST                'ti'
               36  LOAD_METHOD              GetTypeAttr
               38  CALL_METHOD_0         0  ''
               40  LOAD_CONST               0
               42  BINARY_SUBSCR    
               44  STORE_FAST               'disp_clsid'

 L. 260        46  LOAD_FAST                'ti'
               48  LOAD_METHOD              GetContainingTypeLib
               50  CALL_METHOD_0         0  ''
               52  UNPACK_SEQUENCE_2     2 
               54  STORE_FAST               'tlb'
               56  STORE_FAST               'index'

 L. 261        58  LOAD_FAST                'tlb'
               60  LOAD_METHOD              GetLibAttr
               62  CALL_METHOD_0         0  ''
               64  STORE_FAST               'tla'

 L. 262        66  LOAD_GLOBAL              gencache
               68  LOAD_ATTR                EnsureModule
               70  LOAD_FAST                'tla'
               72  LOAD_CONST               0
               74  BINARY_SUBSCR    
               76  LOAD_FAST                'tla'
               78  LOAD_CONST               1
               80  BINARY_SUBSCR    
               82  LOAD_FAST                'tla'
               84  LOAD_CONST               3
               86  BINARY_SUBSCR    
               88  LOAD_FAST                'tla'
               90  LOAD_CONST               4
               92  BINARY_SUBSCR    
               94  LOAD_CONST               0
               96  LOAD_CONST               ('bValidateFile',)
               98  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              100  POP_TOP          

 L. 264       102  LOAD_GLOBAL              gencache
              104  LOAD_METHOD              GetClassForProgID
              106  LOAD_GLOBAL              str
              108  LOAD_FAST                'disp_clsid'
              110  CALL_FUNCTION_1       1  ''
              112  CALL_METHOD_1         1  ''
              114  STORE_FAST               'disp_class'
              116  POP_BLOCK        
              118  JUMP_ABSOLUTE       156  'to 156'
            120_0  COME_FROM_FINALLY    22  '22'

 L. 265       120  DUP_TOP          
              122  LOAD_GLOBAL              pythoncom
              124  LOAD_ATTR                com_error
              126  <121>               146  ''
              128  POP_TOP          
              130  POP_TOP          
              132  POP_TOP          

 L. 266       134  LOAD_GLOBAL              TypeError
              136  LOAD_STR                 'This COM object can not automate the makepy process - please run makepy manually for this object'
              138  CALL_FUNCTION_1       1  ''
              140  RAISE_VARARGS_1       1  'exception instance'
              142  POP_EXCEPT       
              144  JUMP_ABSOLUTE       156  'to 156'
              146  <48>             
              148  JUMP_FORWARD        156  'to 156'
            150_0  COME_FROM            20  '20'

 L. 268       150  LOAD_FAST                'disp'
              152  LOAD_ATTR                __class__
              154  STORE_FAST               'disp_class'
            156_0  COME_FROM_EXCEPT_CLAUSE   148  '148'
            156_1  COME_FROM_EXCEPT_CLAUSE   144  '144'

 L. 270       156  LOAD_FAST                'disp_class'
              158  LOAD_ATTR                CLSID
              160  STORE_FAST               'clsid'

 L. 274       162  SETUP_FINALLY       180  'to 180'

 L. 275       164  LOAD_CONST               0
              166  LOAD_CONST               ('ClassType',)
              168  IMPORT_NAME              types
              170  IMPORT_FROM              ClassType
              172  STORE_FAST               'new_type'
              174  POP_TOP          
              176  POP_BLOCK        
              178  JUMP_FORWARD        202  'to 202'
            180_0  COME_FROM_FINALLY   162  '162'

 L. 276       180  DUP_TOP          
              182  LOAD_GLOBAL              ImportError
              184  <121>               200  ''
              186  POP_TOP          
              188  POP_TOP          
              190  POP_TOP          

 L. 277       192  LOAD_GLOBAL              type
              194  STORE_FAST               'new_type'
              196  POP_EXCEPT       
              198  JUMP_FORWARD        202  'to 202'
              200  <48>             
            202_0  COME_FROM           198  '198'
            202_1  COME_FROM           178  '178'

 L. 278       202  LOAD_GLOBAL              getevents
              204  LOAD_FAST                'clsid'
              206  CALL_FUNCTION_1       1  ''
              208  STORE_FAST               'events_class'

 L. 279       210  LOAD_FAST                'events_class'
              212  LOAD_CONST               None
              214  <117>                 0  ''
              216  POP_JUMP_IF_FALSE   226  'to 226'

 L. 280       218  LOAD_GLOBAL              ValueError
              220  LOAD_STR                 'This COM object does not support events.'
              222  CALL_FUNCTION_1       1  ''
              224  RAISE_VARARGS_1       1  'exception instance'
            226_0  COME_FROM           216  '216'

 L. 281       226  LOAD_FAST                'new_type'
              228  LOAD_STR                 'COMEventClass'
              230  LOAD_FAST                'disp_class'
              232  LOAD_FAST                'events_class'
              234  LOAD_FAST                'user_event_class'
              236  BUILD_TUPLE_3         3 
              238  LOAD_STR                 '__setattr__'
              240  LOAD_GLOBAL              _event_setattr_
              242  BUILD_MAP_1           1 
              244  CALL_FUNCTION_3       3  ''
              246  STORE_FAST               'result_class'

 L. 282       248  LOAD_FAST                'result_class'
              250  LOAD_FAST                'disp'
              252  LOAD_ATTR                _oleobj_
              254  CALL_FUNCTION_1       1  ''
              256  STORE_FAST               'instance'

 L. 283       258  LOAD_FAST                'events_class'
              260  LOAD_METHOD              __init__
              262  LOAD_FAST                'instance'
              264  LOAD_FAST                'instance'
              266  CALL_METHOD_2         2  ''
              268  POP_TOP          

 L. 284       270  LOAD_GLOBAL              hasattr
              272  LOAD_FAST                'user_event_class'
              274  LOAD_STR                 '__init__'
              276  CALL_FUNCTION_2       2  ''
          278_280  POP_JUMP_IF_FALSE   292  'to 292'

 L. 285       282  LOAD_FAST                'user_event_class'
              284  LOAD_METHOD              __init__
              286  LOAD_FAST                'instance'
              288  CALL_METHOD_1         1  ''
              290  POP_TOP          
            292_0  COME_FROM           278  '278'

 L. 286       292  LOAD_GLOBAL              EventsProxy
              294  LOAD_FAST                'instance'
              296  CALL_FUNCTION_1       1  ''
              298  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 126


def WithEvents--- This code section failed: ---

 L. 312         0  LOAD_GLOBAL              Dispatch
                2  LOAD_FAST                'disp'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'disp'

 L. 313         8  LOAD_FAST                'disp'
               10  LOAD_ATTR                __class__
               12  LOAD_ATTR                __dict__
               14  LOAD_METHOD              get
               16  LOAD_STR                 'CLSID'
               18  CALL_METHOD_1         1  ''
               20  POP_JUMP_IF_TRUE    150  'to 150'

 L. 314        22  SETUP_FINALLY       120  'to 120'

 L. 315        24  LOAD_FAST                'disp'
               26  LOAD_ATTR                _oleobj_
               28  LOAD_METHOD              GetTypeInfo
               30  CALL_METHOD_0         0  ''
               32  STORE_FAST               'ti'

 L. 316        34  LOAD_FAST                'ti'
               36  LOAD_METHOD              GetTypeAttr
               38  CALL_METHOD_0         0  ''
               40  LOAD_CONST               0
               42  BINARY_SUBSCR    
               44  STORE_FAST               'disp_clsid'

 L. 317        46  LOAD_FAST                'ti'
               48  LOAD_METHOD              GetContainingTypeLib
               50  CALL_METHOD_0         0  ''
               52  UNPACK_SEQUENCE_2     2 
               54  STORE_FAST               'tlb'
               56  STORE_FAST               'index'

 L. 318        58  LOAD_FAST                'tlb'
               60  LOAD_METHOD              GetLibAttr
               62  CALL_METHOD_0         0  ''
               64  STORE_FAST               'tla'

 L. 319        66  LOAD_GLOBAL              gencache
               68  LOAD_ATTR                EnsureModule
               70  LOAD_FAST                'tla'
               72  LOAD_CONST               0
               74  BINARY_SUBSCR    
               76  LOAD_FAST                'tla'
               78  LOAD_CONST               1
               80  BINARY_SUBSCR    
               82  LOAD_FAST                'tla'
               84  LOAD_CONST               3
               86  BINARY_SUBSCR    
               88  LOAD_FAST                'tla'
               90  LOAD_CONST               4
               92  BINARY_SUBSCR    
               94  LOAD_CONST               0
               96  LOAD_CONST               ('bValidateFile',)
               98  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              100  POP_TOP          

 L. 321       102  LOAD_GLOBAL              gencache
              104  LOAD_METHOD              GetClassForProgID
              106  LOAD_GLOBAL              str
              108  LOAD_FAST                'disp_clsid'
              110  CALL_FUNCTION_1       1  ''
              112  CALL_METHOD_1         1  ''
              114  STORE_FAST               'disp_class'
              116  POP_BLOCK        
              118  JUMP_ABSOLUTE       156  'to 156'
            120_0  COME_FROM_FINALLY    22  '22'

 L. 322       120  DUP_TOP          
              122  LOAD_GLOBAL              pythoncom
              124  LOAD_ATTR                com_error
              126  <121>               146  ''
              128  POP_TOP          
              130  POP_TOP          
              132  POP_TOP          

 L. 323       134  LOAD_GLOBAL              TypeError
              136  LOAD_STR                 'This COM object can not automate the makepy process - please run makepy manually for this object'
              138  CALL_FUNCTION_1       1  ''
              140  RAISE_VARARGS_1       1  'exception instance'
              142  POP_EXCEPT       
              144  JUMP_ABSOLUTE       156  'to 156'
              146  <48>             
              148  JUMP_FORWARD        156  'to 156'
            150_0  COME_FROM            20  '20'

 L. 325       150  LOAD_FAST                'disp'
              152  LOAD_ATTR                __class__
              154  STORE_FAST               'disp_class'
            156_0  COME_FROM_EXCEPT_CLAUSE   148  '148'
            156_1  COME_FROM_EXCEPT_CLAUSE   144  '144'

 L. 327       156  LOAD_FAST                'disp_class'
              158  LOAD_ATTR                CLSID
              160  STORE_FAST               'clsid'

 L. 330       162  SETUP_FINALLY       180  'to 180'

 L. 331       164  LOAD_CONST               0
              166  LOAD_CONST               ('ClassType',)
              168  IMPORT_NAME              types
              170  IMPORT_FROM              ClassType
              172  STORE_FAST               'new_type'
              174  POP_TOP          
              176  POP_BLOCK        
              178  JUMP_FORWARD        202  'to 202'
            180_0  COME_FROM_FINALLY   162  '162'

 L. 332       180  DUP_TOP          
              182  LOAD_GLOBAL              ImportError
              184  <121>               200  ''
              186  POP_TOP          
              188  POP_TOP          
              190  POP_TOP          

 L. 333       192  LOAD_GLOBAL              type
              194  STORE_FAST               'new_type'
              196  POP_EXCEPT       
              198  JUMP_FORWARD        202  'to 202'
              200  <48>             
            202_0  COME_FROM           198  '198'
            202_1  COME_FROM           178  '178'

 L. 334       202  LOAD_GLOBAL              getevents
              204  LOAD_FAST                'clsid'
              206  CALL_FUNCTION_1       1  ''
              208  STORE_FAST               'events_class'

 L. 335       210  LOAD_FAST                'events_class'
              212  LOAD_CONST               None
              214  <117>                 0  ''
              216  POP_JUMP_IF_FALSE   226  'to 226'

 L. 336       218  LOAD_GLOBAL              ValueError
              220  LOAD_STR                 'This COM object does not support events.'
              222  CALL_FUNCTION_1       1  ''
              224  RAISE_VARARGS_1       1  'exception instance'
            226_0  COME_FROM           216  '216'

 L. 337       226  LOAD_FAST                'new_type'
              228  LOAD_STR                 'COMEventClass'
              230  LOAD_FAST                'events_class'
              232  LOAD_FAST                'user_event_class'
              234  BUILD_TUPLE_2         2 
              236  BUILD_MAP_0           0 
              238  CALL_FUNCTION_3       3  ''
              240  STORE_FAST               'result_class'

 L. 338       242  LOAD_FAST                'result_class'
              244  LOAD_FAST                'disp'
              246  CALL_FUNCTION_1       1  ''
              248  STORE_FAST               'instance'

 L. 339       250  LOAD_GLOBAL              hasattr
              252  LOAD_FAST                'user_event_class'
              254  LOAD_STR                 '__init__'
              256  CALL_FUNCTION_2       2  ''
          258_260  POP_JUMP_IF_FALSE   272  'to 272'

 L. 340       262  LOAD_FAST                'user_event_class'
              264  LOAD_METHOD              __init__
              266  LOAD_FAST                'instance'
              268  CALL_METHOD_1         1  ''
              270  POP_TOP          
            272_0  COME_FROM           258  '258'

 L. 341       272  LOAD_FAST                'instance'
              274  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 126


def getevents--- This code section failed: ---

 L. 386         0  LOAD_GLOBAL              str
                2  LOAD_GLOBAL              pywintypes
                4  LOAD_METHOD              IID
                6  LOAD_FAST                'clsid'
                8  CALL_METHOD_1         1  ''
               10  CALL_FUNCTION_1       1  ''
               12  STORE_FAST               'clsid'

 L. 388        14  LOAD_GLOBAL              gencache
               16  LOAD_METHOD              GetClassForCLSID
               18  LOAD_FAST                'clsid'
               20  CALL_METHOD_1         1  ''
               22  STORE_FAST               'klass'

 L. 389        24  SETUP_FINALLY        34  'to 34'

 L. 390        26  LOAD_FAST                'klass'
               28  LOAD_ATTR                default_source
               30  POP_BLOCK        
               32  RETURN_VALUE     
             34_0  COME_FROM_FINALLY    24  '24'

 L. 391        34  DUP_TOP          
               36  LOAD_GLOBAL              AttributeError
               38  <121>                94  ''
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L. 393        46  SETUP_FINALLY        68  'to 68'

 L. 394        48  LOAD_GLOBAL              gencache
               50  LOAD_METHOD              GetClassForCLSID
               52  LOAD_FAST                'klass'
               54  LOAD_ATTR                coclass_clsid
               56  CALL_METHOD_1         1  ''
               58  LOAD_ATTR                default_source
               60  POP_BLOCK        
               62  ROT_FOUR         
               64  POP_EXCEPT       
               66  RETURN_VALUE     
             68_0  COME_FROM_FINALLY    46  '46'

 L. 395        68  DUP_TOP          
               70  LOAD_GLOBAL              AttributeError
               72  <121>                88  ''
               74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          

 L. 396        80  POP_EXCEPT       
               82  POP_EXCEPT       
               84  LOAD_CONST               None
               86  RETURN_VALUE     
               88  <48>             
               90  POP_EXCEPT       
               92  JUMP_FORWARD         96  'to 96'
               94  <48>             
             96_0  COME_FROM            92  '92'

Parse error at or near `<121>' instruction at offset 38


def Record--- This code section failed: ---

 L. 411         0  LOAD_CONST               1
                2  LOAD_CONST               ('gencache',)
                4  IMPORT_NAME              
                6  IMPORT_FROM              gencache
                8  STORE_FAST               'gencache'
               10  POP_TOP          

 L. 412        12  LOAD_FAST                'gencache'
               14  LOAD_METHOD              EnsureDispatch
               16  LOAD_FAST                'object'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'object'

 L. 413        22  LOAD_GLOBAL              sys
               24  LOAD_ATTR                modules
               26  LOAD_FAST                'object'
               28  LOAD_ATTR                __class__
               30  LOAD_ATTR                __module__
               32  BINARY_SUBSCR    
               34  STORE_FAST               'module'

 L. 419        36  LOAD_FAST                'gencache'
               38  LOAD_METHOD              GetModuleForTypelib
               40  LOAD_FAST                'module'
               42  LOAD_ATTR                CLSID
               44  LOAD_FAST                'module'
               46  LOAD_ATTR                LCID
               48  LOAD_FAST                'module'
               50  LOAD_ATTR                MajorVersion
               52  LOAD_FAST                'module'
               54  LOAD_ATTR                MinorVersion
               56  CALL_METHOD_4         4  ''
               58  STORE_FAST               'package'

 L. 420        60  SETUP_FINALLY        76  'to 76'

 L. 421        62  LOAD_FAST                'package'
               64  LOAD_ATTR                RecordMap
               66  LOAD_FAST                'name'
               68  BINARY_SUBSCR    
               70  STORE_FAST               'struct_guid'
               72  POP_BLOCK        
               74  JUMP_FORWARD        110  'to 110'
             76_0  COME_FROM_FINALLY    60  '60'

 L. 422        76  DUP_TOP          
               78  LOAD_GLOBAL              KeyError
               80  <121>               108  ''
               82  POP_TOP          
               84  POP_TOP          
               86  POP_TOP          

 L. 423        88  LOAD_GLOBAL              ValueError
               90  LOAD_STR                 "The structure '%s' is not defined in module '%s'"
               92  LOAD_FAST                'name'
               94  LOAD_FAST                'package'
               96  BUILD_TUPLE_2         2 
               98  BINARY_MODULO    
              100  CALL_FUNCTION_1       1  ''
              102  RAISE_VARARGS_1       1  'exception instance'
              104  POP_EXCEPT       
              106  JUMP_FORWARD        110  'to 110'
              108  <48>             
            110_0  COME_FROM           106  '106'
            110_1  COME_FROM            74  '74'

 L. 424       110  LOAD_GLOBAL              pythoncom
              112  LOAD_METHOD              GetRecordFromGuids
              114  LOAD_FAST                'module'
              116  LOAD_ATTR                CLSID
              118  LOAD_FAST                'module'
              120  LOAD_ATTR                MajorVersion
              122  LOAD_FAST                'module'
              124  LOAD_ATTR                MinorVersion
              126  LOAD_FAST                'module'
              128  LOAD_ATTR                LCID
              130  LOAD_FAST                'struct_guid'
              132  CALL_METHOD_5         5  ''
              134  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 80


class DispatchBaseClass:

    def __init__--- This code section failed: ---

 L. 432         0  LOAD_FAST                'oobj'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    22  'to 22'

 L. 433         8  LOAD_GLOBAL              pythoncom
               10  LOAD_METHOD              new
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                CLSID
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'oobj'
               20  JUMP_FORWARD        122  'to 122'
             22_0  COME_FROM             6  '6'

 L. 434        22  LOAD_GLOBAL              isinstance
               24  LOAD_FAST                'oobj'
               26  LOAD_GLOBAL              DispatchBaseClass
               28  CALL_FUNCTION_2       2  ''
               30  POP_JUMP_IF_FALSE   122  'to 122'

 L. 435        32  SETUP_FINALLY        56  'to 56'

 L. 436        34  LOAD_FAST                'oobj'
               36  LOAD_ATTR                _oleobj_
               38  LOAD_METHOD              QueryInterface
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                CLSID
               44  LOAD_GLOBAL              pythoncom
               46  LOAD_ATTR                IID_IDispatch
               48  CALL_METHOD_2         2  ''
               50  STORE_FAST               'oobj'
               52  POP_BLOCK        
               54  JUMP_FORWARD        122  'to 122'
             56_0  COME_FROM_FINALLY    32  '32'

 L. 437        56  DUP_TOP          
               58  LOAD_GLOBAL              pythoncom
               60  LOAD_ATTR                com_error
               62  <121>               120  ''
               64  POP_TOP          
               66  STORE_FAST               'details'
               68  POP_TOP          
               70  SETUP_FINALLY       112  'to 112'

 L. 438        72  LOAD_CONST               0
               74  LOAD_CONST               None
               76  IMPORT_NAME              winerror
               78  STORE_FAST               'winerror'

 L. 442        80  LOAD_FAST                'details'
               82  LOAD_ATTR                hresult
               84  LOAD_FAST                'winerror'
               86  LOAD_ATTR                E_NOINTERFACE
               88  COMPARE_OP               !=
               90  POP_JUMP_IF_FALSE    94  'to 94'

 L. 443        92  RAISE_VARARGS_0       0  'reraise'
             94_0  COME_FROM            90  '90'

 L. 444        94  LOAD_FAST                'oobj'
               96  LOAD_ATTR                _oleobj_
               98  STORE_FAST               'oobj'
              100  POP_BLOCK        
              102  POP_EXCEPT       
              104  LOAD_CONST               None
              106  STORE_FAST               'details'
              108  DELETE_FAST              'details'
              110  JUMP_FORWARD        122  'to 122'
            112_0  COME_FROM_FINALLY    70  '70'
              112  LOAD_CONST               None
              114  STORE_FAST               'details'
              116  DELETE_FAST              'details'
              118  <48>             
              120  <48>             
            122_0  COME_FROM           110  '110'
            122_1  COME_FROM            54  '54'
            122_2  COME_FROM            30  '30'
            122_3  COME_FROM            20  '20'

 L. 445       122  LOAD_FAST                'oobj'
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                __dict__
              128  LOAD_STR                 '_oleobj_'
              130  STORE_SUBSCR     

Parse error at or near `None' instruction at offset -1

    def __dir__--- This code section failed: ---

 L. 448         0  LOAD_GLOBAL              list
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                __dict__
                6  LOAD_METHOD              keys
                8  CALL_METHOD_0         0  ''
               10  CALL_FUNCTION_1       1  ''
               12  LOAD_GLOBAL              dir
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                __class__
               18  CALL_FUNCTION_1       1  ''
               20  BINARY_ADD       

 L. 449        22  LOAD_GLOBAL              list
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                _prop_map_get_
               28  LOAD_METHOD              keys
               30  CALL_METHOD_0         0  ''
               32  CALL_FUNCTION_1       1  ''

 L. 448        34  BINARY_ADD       

 L. 449        36  LOAD_GLOBAL              list
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                _prop_map_put_
               42  LOAD_METHOD              keys
               44  CALL_METHOD_0         0  ''
               46  CALL_FUNCTION_1       1  ''

 L. 448        48  BINARY_ADD       
               50  STORE_FAST               'lst'

 L. 450        52  SETUP_FINALLY        78  'to 78'
               54  LOAD_FAST                'lst'
               56  LOAD_LISTCOMP            '<code_object <listcomp>>'
               58  LOAD_STR                 'DispatchBaseClass.__dir__.<locals>.<listcomp>'
               60  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                Properties_
               66  GET_ITER         
               68  CALL_FUNCTION_1       1  ''
               70  INPLACE_ADD      
               72  STORE_FAST               'lst'
               74  POP_BLOCK        
               76  JUMP_FORWARD         96  'to 96'
             78_0  COME_FROM_FINALLY    52  '52'

 L. 451        78  DUP_TOP          
               80  LOAD_GLOBAL              AttributeError
               82  <121>                94  ''
               84  POP_TOP          
               86  POP_TOP          
               88  POP_TOP          

 L. 452        90  POP_EXCEPT       
               92  JUMP_FORWARD         96  'to 96'
               94  <48>             
             96_0  COME_FROM            92  '92'
             96_1  COME_FROM            76  '76'

 L. 453        96  LOAD_GLOBAL              list
               98  LOAD_GLOBAL              set
              100  LOAD_FAST                'lst'
              102  CALL_FUNCTION_1       1  ''
              104  CALL_FUNCTION_1       1  ''
              106  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 82

    def __repr__--- This code section failed: ---

 L. 458         0  SETUP_FINALLY        52  'to 52'

 L. 459         2  LOAD_GLOBAL              sys
                4  LOAD_ATTR                modules
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                __class__
               10  LOAD_ATTR                __module__
               12  BINARY_SUBSCR    
               14  LOAD_ATTR                __doc__
               16  STORE_FAST               'mod_doc'

 L. 460        18  LOAD_FAST                'mod_doc'
               20  POP_JUMP_IF_FALSE    32  'to 32'

 L. 461        22  LOAD_STR                 'win32com.gen_py.'
               24  LOAD_FAST                'mod_doc'
               26  BINARY_ADD       
               28  STORE_FAST               'mod_name'
               30  JUMP_FORWARD         48  'to 48'
             32_0  COME_FROM            20  '20'

 L. 463        32  LOAD_GLOBAL              sys
               34  LOAD_ATTR                modules
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                __class__
               40  LOAD_ATTR                __module__
               42  BINARY_SUBSCR    
               44  LOAD_ATTR                __name__
               46  STORE_FAST               'mod_name'
             48_0  COME_FROM            30  '30'
               48  POP_BLOCK        
               50  JUMP_FORWARD         74  'to 74'
             52_0  COME_FROM_FINALLY     0  '0'

 L. 464        52  DUP_TOP          
               54  LOAD_GLOBAL              KeyError
               56  <121>                72  ''
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L. 465        64  LOAD_STR                 'win32com.gen_py.unknown'
               66  STORE_FAST               'mod_name'
               68  POP_EXCEPT       
               70  JUMP_FORWARD         74  'to 74'
               72  <48>             
             74_0  COME_FROM            70  '70'
             74_1  COME_FROM            50  '50'

 L. 466        74  LOAD_STR                 '<%s.%s instance at 0x%s>'
               76  LOAD_FAST                'mod_name'
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                __class__
               82  LOAD_ATTR                __name__
               84  LOAD_GLOBAL              id
               86  LOAD_FAST                'self'
               88  CALL_FUNCTION_1       1  ''
               90  BUILD_TUPLE_3         3 
               92  BINARY_MODULO    
               94  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 56

    def __eq__(self, other):
        other = getattr(other, '_oleobj_', other)
        return self._oleobj_ == other

    def __ne__(self, other):
        other = getattr(other, '_oleobj_', other)
        return self._oleobj_ != other

    def _ApplyTypes_--- This code section failed: ---

 L. 477         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _get_good_object_

 L. 478         4  LOAD_FAST                'self'
                6  LOAD_ATTR                _oleobj_
                8  LOAD_ATTR                InvokeTypes
               10  LOAD_FAST                'dispid'
               12  LOAD_CONST               0
               14  LOAD_FAST                'wFlags'
               16  LOAD_FAST                'retType'
               18  LOAD_FAST                'argTypes'
               20  BUILD_LIST_5          5 
               22  LOAD_FAST                'args'
               24  CALL_FINALLY         27  'to 27'
               26  WITH_CLEANUP_FINISH
               28  CALL_FUNCTION_EX      0  'positional arguments only'

 L. 479        30  LOAD_FAST                'user'
               32  LOAD_FAST                'resultCLSID'

 L. 477        34  CALL_METHOD_3         3  ''
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 24

    def __getattr__--- This code section failed: ---

 L. 482         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _prop_map_get_
                4  LOAD_METHOD              get
                6  LOAD_FAST                'attr'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'args'

 L. 483        12  LOAD_FAST                'args'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    40  'to 40'

 L. 484        20  LOAD_GLOBAL              AttributeError
               22  LOAD_STR                 "'%s' object has no attribute '%s'"
               24  LOAD_GLOBAL              repr
               26  LOAD_FAST                'self'
               28  CALL_FUNCTION_1       1  ''
               30  LOAD_FAST                'attr'
               32  BUILD_TUPLE_2         2 
               34  BINARY_MODULO    
               36  CALL_FUNCTION_1       1  ''
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            18  '18'

 L. 485        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _ApplyTypes_
               44  LOAD_FAST                'args'
               46  CALL_FUNCTION_EX      0  'positional arguments only'
               48  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 16

    def __setattr__--- This code section failed: ---

 L. 488         0  LOAD_FAST                'attr'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                __dict__
                6  <118>                 0  ''
                8  POP_JUMP_IF_FALSE    24  'to 24'
               10  LOAD_FAST                'value'
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                __dict__
               16  LOAD_FAST                'attr'
               18  STORE_SUBSCR     
               20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM             8  '8'

 L. 489        24  SETUP_FINALLY        44  'to 44'

 L. 490        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _prop_map_put_
               30  LOAD_FAST                'attr'
               32  BINARY_SUBSCR    
               34  UNPACK_SEQUENCE_2     2 
               36  STORE_FAST               'args'
               38  STORE_FAST               'defArgs'
               40  POP_BLOCK        
               42  JUMP_FORWARD         82  'to 82'
             44_0  COME_FROM_FINALLY    24  '24'

 L. 491        44  DUP_TOP          
               46  LOAD_GLOBAL              KeyError
               48  <121>                80  ''
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L. 492        56  LOAD_GLOBAL              AttributeError
               58  LOAD_STR                 "'%s' object has no attribute '%s'"
               60  LOAD_GLOBAL              repr
               62  LOAD_FAST                'self'
               64  CALL_FUNCTION_1       1  ''
               66  LOAD_FAST                'attr'
               68  BUILD_TUPLE_2         2 
               70  BINARY_MODULO    
               72  CALL_FUNCTION_1       1  ''
               74  RAISE_VARARGS_1       1  'exception instance'
               76  POP_EXCEPT       
               78  JUMP_FORWARD         82  'to 82'
               80  <48>             
             82_0  COME_FROM            78  '78'
             82_1  COME_FROM            42  '42'

 L. 493        82  LOAD_FAST                'self'
               84  LOAD_ATTR                _oleobj_
               86  LOAD_ATTR                Invoke
               88  LOAD_FAST                'args'
               90  LOAD_FAST                'value'
               92  BUILD_TUPLE_1         1 
               94  BINARY_ADD       
               96  LOAD_FAST                'defArgs'
               98  BINARY_ADD       
              100  CALL_FUNCTION_EX      0  'positional arguments only'
              102  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def _get_good_single_object_(self, obj, obUserName=None, resultCLSID=None):
        return _get_good_single_object_(obj, obUserName, resultCLSID)

    def _get_good_object_(self, obj, obUserName=None, resultCLSID=None):
        return _get_good_object_(obj, obUserName, resultCLSID)


def _get_good_single_object_(obj, obUserName=None, resultCLSID=None):
    if _PyIDispatchType == type(obj):
        return Dispatch(obj, obUserName, resultCLSID)
    return obj


def _get_good_object_--- This code section failed: ---

 L. 506         0  LOAD_FAST                'obj'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 507         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 508        12  LOAD_GLOBAL              isinstance
               14  LOAD_FAST                'obj'
               16  LOAD_GLOBAL              tuple
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_FALSE    68  'to 68'

 L. 509        22  LOAD_FAST                'obUserName'
               24  BUILD_TUPLE_1         1 
               26  LOAD_GLOBAL              len
               28  LOAD_FAST                'obj'
               30  CALL_FUNCTION_1       1  ''
               32  BINARY_MULTIPLY  
               34  STORE_FAST               'obUserNameTuple'

 L. 510        36  LOAD_FAST                'resultCLSID'
               38  BUILD_TUPLE_1         1 
               40  LOAD_GLOBAL              len
               42  LOAD_FAST                'obj'
               44  CALL_FUNCTION_1       1  ''
               46  BINARY_MULTIPLY  
               48  STORE_FAST               'resultCLSIDTuple'

 L. 511        50  LOAD_GLOBAL              tuple
               52  LOAD_GLOBAL              map
               54  LOAD_GLOBAL              _get_good_object_
               56  LOAD_FAST                'obj'
               58  LOAD_FAST                'obUserNameTuple'
               60  LOAD_FAST                'resultCLSIDTuple'
               62  CALL_FUNCTION_4       4  ''
               64  CALL_FUNCTION_1       1  ''
               66  RETURN_VALUE     
             68_0  COME_FROM            20  '20'

 L. 513        68  LOAD_GLOBAL              _get_good_single_object_
               70  LOAD_FAST                'obj'
               72  LOAD_FAST                'obUserName'
               74  LOAD_FAST                'resultCLSID'
               76  CALL_FUNCTION_3       3  ''
               78  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1


class CoClassBaseClass:

    def __init__--- This code section failed: ---

 L. 517         0  LOAD_FAST                'oobj'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    20  'to 20'
                8  LOAD_GLOBAL              pythoncom
               10  LOAD_METHOD              new
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                CLSID
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'oobj'
             20_0  COME_FROM             6  '6'

 L. 518        20  LOAD_FAST                'self'
               22  LOAD_METHOD              default_interface
               24  LOAD_FAST                'oobj'
               26  CALL_METHOD_1         1  ''
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                __dict__
               32  LOAD_STR                 '_dispobj_'
               34  STORE_SUBSCR     

Parse error at or near `None' instruction at offset -1

    def __repr__(self):
        return '<win32com.gen_py.%s.%s>' % (__doc__, self.__class__.__name__)

    def __getattr__--- This code section failed: ---

 L. 523         0  LOAD_FAST                'self'
                2  LOAD_ATTR                __dict__
                4  LOAD_STR                 '_dispobj_'
                6  BINARY_SUBSCR    
                8  STORE_FAST               'd'

 L. 524        10  LOAD_FAST                'd'
               12  LOAD_CONST               None
               14  <117>                 1  ''
               16  POP_JUMP_IF_FALSE    28  'to 28'
               18  LOAD_GLOBAL              getattr
               20  LOAD_FAST                'd'
               22  LOAD_FAST                'attr'
               24  CALL_FUNCTION_2       2  ''
               26  RETURN_VALUE     
             28_0  COME_FROM            16  '16'

 L. 525        28  LOAD_GLOBAL              AttributeError
               30  LOAD_FAST                'attr'
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<117>' instruction at offset 14

    def __setattr__--- This code section failed: ---

 L. 527         0  LOAD_FAST                'attr'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                __dict__
                6  <118>                 0  ''
                8  POP_JUMP_IF_FALSE    24  'to 24'
               10  LOAD_FAST                'value'
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                __dict__
               16  LOAD_FAST                'attr'
               18  STORE_SUBSCR     
               20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM             8  '8'

 L. 528        24  SETUP_FINALLY        66  'to 66'

 L. 529        26  LOAD_FAST                'self'
               28  LOAD_ATTR                __dict__
               30  LOAD_STR                 '_dispobj_'
               32  BINARY_SUBSCR    
               34  STORE_FAST               'd'

 L. 530        36  LOAD_FAST                'd'
               38  LOAD_CONST               None
               40  <117>                 1  ''
               42  POP_JUMP_IF_FALSE    62  'to 62'

 L. 531        44  LOAD_FAST                'd'
               46  LOAD_METHOD              __setattr__
               48  LOAD_FAST                'attr'
               50  LOAD_FAST                'value'
               52  CALL_METHOD_2         2  ''
               54  POP_TOP          

 L. 532        56  POP_BLOCK        
               58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            42  '42'
               62  POP_BLOCK        
               64  JUMP_FORWARD         84  'to 84'
             66_0  COME_FROM_FINALLY    24  '24'

 L. 533        66  DUP_TOP          
               68  LOAD_GLOBAL              AttributeError
               70  <121>                82  ''
               72  POP_TOP          
               74  POP_TOP          
               76  POP_TOP          

 L. 534        78  POP_EXCEPT       
               80  JUMP_FORWARD         84  'to 84'
               82  <48>             
             84_0  COME_FROM            80  '80'
             84_1  COME_FROM            64  '64'

 L. 535        84  LOAD_FAST                'value'
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                __dict__
               90  LOAD_FAST                'attr'
               92  STORE_SUBSCR     

Parse error at or near `None' instruction at offset -1

    def __call__--- This code section failed: ---

 L. 541         0  LOAD_FAST                'self'
                2  LOAD_ATTR                __dict__
                4  LOAD_STR                 '_dispobj_'
                6  BINARY_SUBSCR    
                8  LOAD_ATTR                __call__
               10  LOAD_FAST                'args'
               12  BUILD_MAP_0           0 
               14  LOAD_FAST                'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __str__(self, *args):
        return (self.__dict__['_dispobj_'].__str__)(*args)

    def __int__(self, *args):
        return (self.__dict__['_dispobj_'].__int__)(*args)

    def __iter__(self):
        return self.__dict__['_dispobj_'].__iter__

    def __len__(self):
        return self.__dict__['_dispobj_'].__len__

    def __nonzero__(self):
        return self.__dict__['_dispobj_'].__nonzero__


class VARIANT(object):

    def __init__(self, vt, value):
        self.varianttype = vt
        self._value = value

    def _get_value(self):
        return self._value

    def _set_value(self, newval):
        self._value = _get_good_object_(newval)

    def _del_value(self):
        del self._value

    value = property(_get_value, _set_value, _del_value)

    def __repr__(self):
        return 'win32com.client.VARIANT(%r, %r)' % (self.varianttype, self._value)