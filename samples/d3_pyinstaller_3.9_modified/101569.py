# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: comtypes\client\lazybind.py
import comtypes, comtypes.automation
from comtypes.automation import IEnumVARIANT
from comtypes.automation import DISPATCH_METHOD
from comtypes.automation import DISPATCH_PROPERTYGET
from comtypes.automation import DISPATCH_PROPERTYPUT
from comtypes.automation import DISPATCH_PROPERTYPUTREF
from comtypes.automation import DISPID_VALUE
from comtypes.automation import DISPID_NEWENUM
from comtypes.typeinfo import FUNC_PUREVIRTUAL, FUNC_DISPATCH

class FuncDesc(object):
    __doc__ = 'Stores important FUNCDESC properties by copying them from a\n    real FUNCDESC instance.\n    '

    def __init__(self, **kw):
        self.__dict__.update(kw)


_all_slice = slice(None, None, None)

class NamedProperty(object):

    def __init__(self, disp, get, put, putref):
        self.get = get
        self.put = put
        self.putref = putref
        self.disp = disp

    def __getitem__--- This code section failed: ---

 L.  38         0  LOAD_FAST                'self'
                2  LOAD_ATTR                get
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L.  39        10  LOAD_GLOBAL              TypeError
               12  LOAD_STR                 'unsubscriptable object'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L.  40        18  LOAD_GLOBAL              isinstance
               20  LOAD_FAST                'arg'
               22  LOAD_GLOBAL              tuple
               24  CALL_FUNCTION_2       2  ''
               26  POP_JUMP_IF_FALSE    62  'to 62'

 L.  41        28  LOAD_FAST                'self'
               30  LOAD_ATTR                disp
               32  LOAD_ATTR                _comobj
               34  LOAD_ATTR                _invoke
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                get
               40  LOAD_ATTR                memid

 L.  42        42  LOAD_FAST                'self'
               44  LOAD_ATTR                get
               46  LOAD_ATTR                invkind

 L.  43        48  LOAD_CONST               0

 L.  41        50  BUILD_LIST_3          3 

 L.  44        52  LOAD_FAST                'arg'

 L.  41        54  CALL_FINALLY         57  'to 57'
               56  WITH_CLEANUP_FINISH
               58  CALL_FUNCTION_EX      0  'positional arguments only'
               60  RETURN_VALUE     
             62_0  COME_FROM            26  '26'

 L.  45        62  LOAD_FAST                'arg'
               64  LOAD_GLOBAL              _all_slice
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE    96  'to 96'

 L.  46        70  LOAD_FAST                'self'
               72  LOAD_ATTR                disp
               74  LOAD_ATTR                _comobj
               76  LOAD_METHOD              _invoke
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                get
               82  LOAD_ATTR                memid

 L.  47        84  LOAD_FAST                'self'
               86  LOAD_ATTR                get
               88  LOAD_ATTR                invkind

 L.  48        90  LOAD_CONST               0

 L.  46        92  CALL_METHOD_3         3  ''
               94  RETURN_VALUE     
             96_0  COME_FROM            68  '68'

 L.  49        96  LOAD_FAST                'self'
               98  LOAD_ATTR                disp
              100  LOAD_ATTR                _comobj
              102  LOAD_ATTR                _invoke
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                get
              108  LOAD_ATTR                memid

 L.  50       110  LOAD_FAST                'self'
              112  LOAD_ATTR                get
              114  LOAD_ATTR                invkind

 L.  51       116  LOAD_CONST               0

 L.  49       118  BUILD_LIST_3          3 

 L.  52       120  LOAD_FAST                'arg'
              122  BUILD_LIST_1          1 

 L.  49       124  CALL_FINALLY        127  'to 127'
              126  WITH_CLEANUP_FINISH
              128  CALL_FUNCTION_EX      0  'positional arguments only'
              130  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __call__--- This code section failed: ---

 L.  55         0  LOAD_FAST                'self'
                2  LOAD_ATTR                get
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L.  56        10  LOAD_GLOBAL              TypeError
               12  LOAD_STR                 'object is not callable'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L.  57        18  LOAD_FAST                'self'
               20  LOAD_ATTR                disp
               22  LOAD_ATTR                _comobj
               24  LOAD_ATTR                _invoke
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                get
               30  LOAD_ATTR                memid

 L.  58        32  LOAD_FAST                'self'
               34  LOAD_ATTR                get
               36  LOAD_ATTR                invkind

 L.  59        38  LOAD_CONST               0

 L.  57        40  BUILD_LIST_3          3 

 L.  60        42  LOAD_FAST                'args'

 L.  57        44  CALL_FINALLY         47  'to 47'
               46  WITH_CLEANUP_FINISH
               48  CALL_FUNCTION_EX      0  'positional arguments only'
               50  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __setitem__--- This code section failed: ---

 L.  64         0  LOAD_FAST                'self'
                2  LOAD_ATTR                put
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    28  'to 28'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                putref
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    28  'to 28'

 L.  65        20  LOAD_GLOBAL              TypeError
               22  LOAD_STR                 'object does not support item assignment'
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            18  '18'
             28_1  COME_FROM             8  '8'

 L.  66        28  LOAD_GLOBAL              comtypes
               30  LOAD_METHOD              _is_object
               32  LOAD_FAST                'value'
               34  CALL_METHOD_1         1  ''
               36  POP_JUMP_IF_FALSE    52  'to 52'

 L.  67        38  LOAD_FAST                'self'
               40  LOAD_ATTR                putref
               42  JUMP_IF_TRUE_OR_POP    48  'to 48'
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                put
             48_0  COME_FROM            42  '42'
               48  STORE_FAST               'descr'
               50  JUMP_FORWARD         64  'to 64'
             52_0  COME_FROM            36  '36'

 L.  69        52  LOAD_FAST                'self'
               54  LOAD_ATTR                put
               56  JUMP_IF_TRUE_OR_POP    62  'to 62'
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                putref
             62_0  COME_FROM            56  '56'
               62  STORE_FAST               'descr'
             64_0  COME_FROM            50  '50'

 L.  70        64  LOAD_GLOBAL              isinstance
               66  LOAD_FAST                'name'
               68  LOAD_GLOBAL              tuple
               70  CALL_FUNCTION_2       2  ''
               72  POP_JUMP_IF_FALSE   112  'to 112'

 L.  71        74  LOAD_FAST                'self'
               76  LOAD_ATTR                disp
               78  LOAD_ATTR                _comobj
               80  LOAD_ATTR                _invoke
               82  LOAD_FAST                'descr'
               84  LOAD_ATTR                memid

 L.  72        86  LOAD_FAST                'descr'
               88  LOAD_ATTR                invkind

 L.  73        90  LOAD_CONST               0

 L.  71        92  BUILD_LIST_3          3 

 L.  74        94  LOAD_FAST                'name'
               96  LOAD_FAST                'value'
               98  BUILD_TUPLE_1         1 
              100  BINARY_ADD       

 L.  71       102  CALL_FINALLY        105  'to 105'
              104  WITH_CLEANUP_FINISH
              106  CALL_FUNCTION_EX      0  'positional arguments only'
              108  POP_TOP          
              110  JUMP_FORWARD        172  'to 172'
            112_0  COME_FROM            72  '72'

 L.  75       112  LOAD_FAST                'name'
              114  LOAD_GLOBAL              _all_slice
              116  COMPARE_OP               ==
              118  POP_JUMP_IF_FALSE   146  'to 146'

 L.  76       120  LOAD_FAST                'self'
              122  LOAD_ATTR                disp
              124  LOAD_ATTR                _comobj
              126  LOAD_METHOD              _invoke
              128  LOAD_FAST                'descr'
              130  LOAD_ATTR                memid

 L.  77       132  LOAD_FAST                'descr'
              134  LOAD_ATTR                invkind

 L.  78       136  LOAD_CONST               0

 L.  79       138  LOAD_FAST                'value'

 L.  76       140  CALL_METHOD_4         4  ''
              142  POP_TOP          
              144  JUMP_FORWARD        172  'to 172'
            146_0  COME_FROM           118  '118'

 L.  81       146  LOAD_FAST                'self'
              148  LOAD_ATTR                disp
              150  LOAD_ATTR                _comobj
              152  LOAD_METHOD              _invoke
              154  LOAD_FAST                'descr'
              156  LOAD_ATTR                memid

 L.  82       158  LOAD_FAST                'descr'
              160  LOAD_ATTR                invkind

 L.  83       162  LOAD_CONST               0

 L.  84       164  LOAD_FAST                'name'

 L.  85       166  LOAD_FAST                'value'

 L.  81       168  CALL_METHOD_5         5  ''
              170  POP_TOP          
            172_0  COME_FROM           144  '144'
            172_1  COME_FROM           110  '110'

Parse error at or near `None' instruction at offset -1

    def __iter__(self):
        """ Explicitly disallow iteration. """
        msg = '%r is not iterable' % self.disp
        raise TypeError(msg)


class Dispatch(object):
    __doc__ = 'Dynamic dispatch for an object the exposes type information.\n    Binding at runtime is done via ITypeComp::Bind calls.\n    '

    def __init__(self, comobj, tinfo):
        self.__dict__['_comobj'] = comobj
        self.__dict__['_tinfo'] = tinfo
        self.__dict__['_tcomp'] = tinfo.GetTypeComp()
        self.__dict__['_tdesc'] = {}

    def __bind--- This code section failed: ---

 L. 122         0  SETUP_FINALLY        18  'to 18'

 L. 123         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _tdesc
                6  LOAD_FAST                'name'
                8  LOAD_FAST                'invkind'
               10  BUILD_TUPLE_2         2 
               12  BINARY_SUBSCR    
               14  POP_BLOCK        
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L. 124        18  DUP_TOP          
               20  LOAD_GLOBAL              KeyError
               22  <121>               124  ''
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 125        30  SETUP_FINALLY        54  'to 54'

 L. 126        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _tcomp
               36  LOAD_METHOD              Bind
               38  LOAD_FAST                'name'
               40  LOAD_FAST                'invkind'
               42  CALL_METHOD_2         2  ''
               44  LOAD_CONST               1
               46  BINARY_SUBSCR    
               48  STORE_FAST               'descr'
               50  POP_BLOCK        
               52  JUMP_FORWARD         78  'to 78'
             54_0  COME_FROM_FINALLY    30  '30'

 L. 127        54  DUP_TOP          
               56  LOAD_GLOBAL              comtypes
               58  LOAD_ATTR                COMError
               60  <121>                76  ''
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L. 128        68  LOAD_CONST               None
               70  STORE_FAST               'info'
               72  POP_EXCEPT       
               74  JUMP_FORWARD        102  'to 102'
               76  <48>             
             78_0  COME_FROM            52  '52'

 L. 133        78  LOAD_GLOBAL              FuncDesc
               80  LOAD_FAST                'descr'
               82  LOAD_ATTR                memid

 L. 134        84  LOAD_FAST                'descr'
               86  LOAD_ATTR                invkind

 L. 135        88  LOAD_FAST                'descr'
               90  LOAD_ATTR                cParams

 L. 136        92  LOAD_FAST                'descr'
               94  LOAD_ATTR                funckind

 L. 133        96  LOAD_CONST               ('memid', 'invkind', 'cParams', 'funckind')
               98  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              100  STORE_FAST               'info'
            102_0  COME_FROM            74  '74'

 L. 137       102  LOAD_FAST                'info'
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                _tdesc
              108  LOAD_FAST                'name'
              110  LOAD_FAST                'invkind'
              112  BUILD_TUPLE_2         2 
              114  STORE_SUBSCR     

 L. 138       116  LOAD_FAST                'info'
              118  ROT_FOUR         
              120  POP_EXCEPT       
              122  RETURN_VALUE     
              124  <48>             

Parse error at or near `<121>' instruction at offset 22

    def QueryInterface(self, *args):
        """QueryInterface is forwarded to the real com object."""
        return (self._comobj.QueryInterface)(*args)

    def __cmp__(self, other):
        if not isinstanceotherDispatch:
            return 1
        return cmpself._comobjother._comobj

    def __eq__(self, other):
        return isinstanceotherDispatch and self._comobj == other._comobj

    def __hash__(self):
        return hash(self._comobj)

    def __getattr__--- This code section failed: ---

 L. 158         0  LOAD_FAST                'name'
                2  LOAD_METHOD              startswith
                4  LOAD_STR                 '__'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_FALSE    28  'to 28'
               10  LOAD_FAST                'name'
               12  LOAD_METHOD              endswith
               14  LOAD_STR                 '__'
               16  CALL_METHOD_1         1  ''
               18  POP_JUMP_IF_FALSE    28  'to 28'

 L. 159        20  LOAD_GLOBAL              AttributeError
               22  LOAD_FAST                'name'
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            18  '18'
             28_1  COME_FROM             8  '8'

 L. 161        28  LOAD_DEREF               'self'
               30  LOAD_METHOD              _Dispatch__bind
               32  LOAD_FAST                'name'
               34  LOAD_GLOBAL              DISPATCH_METHOD
               36  LOAD_GLOBAL              DISPATCH_PROPERTYGET
               38  BINARY_OR        
               40  CALL_METHOD_2         2  ''
               42  STORE_DEREF              'descr'

 L. 162        44  LOAD_DEREF               'descr'
               46  LOAD_CONST               None
               48  <117>                 0  ''
               50  POP_JUMP_IF_FALSE    60  'to 60'

 L. 163        52  LOAD_GLOBAL              AttributeError
               54  LOAD_FAST                'name'
               56  CALL_FUNCTION_1       1  ''
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            50  '50'

 L. 164        60  LOAD_DEREF               'descr'
               62  LOAD_ATTR                invkind
               64  LOAD_GLOBAL              DISPATCH_PROPERTYGET
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE   206  'to 206'

 L. 166        70  LOAD_DEREF               'descr'
               72  LOAD_ATTR                funckind
               74  LOAD_GLOBAL              FUNC_DISPATCH
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_FALSE   112  'to 112'

 L. 167        80  LOAD_DEREF               'descr'
               82  LOAD_ATTR                cParams
               84  LOAD_CONST               0
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_FALSE   168  'to 168'

 L. 168        90  LOAD_DEREF               'self'
               92  LOAD_ATTR                _comobj
               94  LOAD_METHOD              _invoke
               96  LOAD_DEREF               'descr'
               98  LOAD_ATTR                memid
              100  LOAD_DEREF               'descr'
              102  LOAD_ATTR                invkind
              104  LOAD_CONST               0
              106  CALL_METHOD_3         3  ''
              108  RETURN_VALUE     
              110  JUMP_FORWARD        168  'to 168'
            112_0  COME_FROM            78  '78'

 L. 169       112  LOAD_DEREF               'descr'
              114  LOAD_ATTR                funckind
              116  LOAD_GLOBAL              FUNC_PUREVIRTUAL
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   154  'to 154'

 L. 172       122  LOAD_DEREF               'descr'
              124  LOAD_ATTR                cParams
              126  LOAD_CONST               1
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE   168  'to 168'

 L. 173       132  LOAD_DEREF               'self'
              134  LOAD_ATTR                _comobj
              136  LOAD_METHOD              _invoke
              138  LOAD_DEREF               'descr'
              140  LOAD_ATTR                memid
              142  LOAD_DEREF               'descr'
              144  LOAD_ATTR                invkind
              146  LOAD_CONST               0
              148  CALL_METHOD_3         3  ''
              150  RETURN_VALUE     
              152  JUMP_FORWARD        168  'to 168'
            154_0  COME_FROM           120  '120'

 L. 175       154  LOAD_GLOBAL              RuntimeError
              156  LOAD_STR                 'funckind %d not yet implemented'
              158  LOAD_DEREF               'descr'
              160  LOAD_ATTR                funckind
              162  BINARY_MODULO    
              164  CALL_FUNCTION_1       1  ''
              166  RAISE_VARARGS_1       1  'exception instance'
            168_0  COME_FROM           152  '152'
            168_1  COME_FROM           130  '130'
            168_2  COME_FROM           110  '110'
            168_3  COME_FROM            88  '88'

 L. 176       168  LOAD_DEREF               'self'
              170  LOAD_METHOD              _Dispatch__bind
              172  LOAD_FAST                'name'
              174  LOAD_GLOBAL              DISPATCH_PROPERTYPUT
              176  CALL_METHOD_2         2  ''
              178  STORE_FAST               'put'

 L. 177       180  LOAD_DEREF               'self'
              182  LOAD_METHOD              _Dispatch__bind
              184  LOAD_FAST                'name'
              186  LOAD_GLOBAL              DISPATCH_PROPERTYPUTREF
              188  CALL_METHOD_2         2  ''
              190  STORE_FAST               'putref'

 L. 178       192  LOAD_GLOBAL              NamedProperty
              194  LOAD_DEREF               'self'
              196  LOAD_DEREF               'descr'
              198  LOAD_FAST                'put'
              200  LOAD_FAST                'putref'
              202  CALL_FUNCTION_4       4  ''
              204  RETURN_VALUE     
            206_0  COME_FROM            68  '68'

 L. 181       206  LOAD_CLOSURE             'descr'
              208  LOAD_CLOSURE             'self'
              210  BUILD_TUPLE_2         2 
              212  LOAD_CODE                <code_object caller>
              214  LOAD_STR                 'Dispatch.__getattr__.<locals>.caller'
              216  MAKE_FUNCTION_8          'closure'
              218  STORE_FAST               'caller'

 L. 183       220  SETUP_FINALLY       232  'to 232'

 L. 184       222  LOAD_FAST                'name'
              224  LOAD_FAST                'caller'
              226  STORE_ATTR               __name__
              228  POP_BLOCK        
              230  JUMP_FORWARD        250  'to 250'
            232_0  COME_FROM_FINALLY   220  '220'

 L. 185       232  DUP_TOP          
              234  LOAD_GLOBAL              TypeError
              236  <121>               248  ''
              238  POP_TOP          
              240  POP_TOP          
              242  POP_TOP          

 L. 187       244  POP_EXCEPT       
              246  JUMP_FORWARD        250  'to 250'
              248  <48>             
            250_0  COME_FROM           246  '246'
            250_1  COME_FROM           230  '230'

 L. 188       250  LOAD_FAST                'caller'
              252  RETURN_VALUE     

Parse error at or near `<117>' instruction at offset 48

    def __setattr__(self, name, value):
        put = self._Dispatch__bindnameDISPATCH_PROPERTYPUT
        putref = self._Dispatch__bindnameDISPATCH_PROPERTYPUTREF
        if not put:
            if not putref:
                raise AttributeError(name)
        if comtypes._is_object(value):
            descr = putref or put
        else:
            descr = put or putref
        if descr.cParams == 1:
            self._comobj._invokedescr.memiddescr.invkind0value
            return
        raise AttributeError(name)

    def __call__--- This code section failed: ---

 L. 223         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _comobj
                4  LOAD_ATTR                _invoke
                6  LOAD_GLOBAL              DISPID_VALUE

 L. 224         8  LOAD_GLOBAL              DISPATCH_METHOD
               10  LOAD_GLOBAL              DISPATCH_PROPERTYGET
               12  BINARY_OR        

 L. 225        14  LOAD_CONST               0

 L. 223        16  BUILD_LIST_3          3 

 L. 226        18  LOAD_FAST                'args'

 L. 223        20  CALL_FINALLY         23  'to 23'
               22  WITH_CLEANUP_FINISH
               24  CALL_FUNCTION_EX      0  'positional arguments only'
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 20

    def __getitem__--- This code section failed: ---

 L. 229         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'arg'
                4  LOAD_GLOBAL              tuple
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    16  'to 16'

 L. 230        10  LOAD_FAST                'arg'
               12  STORE_FAST               'args'
               14  JUMP_FORWARD         36  'to 36'
             16_0  COME_FROM             8  '8'

 L. 231        16  LOAD_FAST                'arg'
               18  LOAD_GLOBAL              _all_slice
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_FALSE    30  'to 30'

 L. 232        24  LOAD_CONST               ()
               26  STORE_FAST               'args'
               28  JUMP_FORWARD         36  'to 36'
             30_0  COME_FROM            22  '22'

 L. 234        30  LOAD_FAST                'arg'
               32  BUILD_TUPLE_1         1 
               34  STORE_FAST               'args'
             36_0  COME_FROM            28  '28'
             36_1  COME_FROM            14  '14'

 L. 236        36  SETUP_FINALLY        68  'to 68'

 L. 237        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _comobj
               42  LOAD_ATTR                _invoke
               44  LOAD_GLOBAL              DISPID_VALUE

 L. 238        46  LOAD_GLOBAL              DISPATCH_METHOD
               48  LOAD_GLOBAL              DISPATCH_PROPERTYGET
               50  BINARY_OR        

 L. 239        52  LOAD_CONST               0

 L. 237        54  BUILD_LIST_3          3 

 L. 240        56  LOAD_FAST                'args'

 L. 237        58  CALL_FINALLY         61  'to 61'
               60  WITH_CLEANUP_FINISH
               62  CALL_FUNCTION_EX      0  'positional arguments only'
               64  POP_BLOCK        
               66  RETURN_VALUE     
             68_0  COME_FROM_FINALLY    36  '36'

 L. 241        68  DUP_TOP          
               70  LOAD_GLOBAL              comtypes
               72  LOAD_ATTR                COMError
               74  <121>                98  ''
               76  POP_TOP          
               78  POP_TOP          
               80  POP_TOP          

 L. 242        82  LOAD_GLOBAL              iter
               84  LOAD_FAST                'self'
               86  CALL_FUNCTION_1       1  ''
               88  LOAD_FAST                'arg'
               90  BINARY_SUBSCR    
               92  ROT_FOUR         
               94  POP_EXCEPT       
               96  RETURN_VALUE     
               98  <48>             

Parse error at or near `CALL_FINALLY' instruction at offset 58

    def __setitem__--- This code section failed: ---

 L. 245         0  LOAD_GLOBAL              comtypes
                2  LOAD_METHOD              _is_object
                4  LOAD_FAST                'value'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_FALSE    16  'to 16'

 L. 246        10  LOAD_GLOBAL              DISPATCH_PROPERTYPUTREF
               12  STORE_FAST               'invkind'
               14  JUMP_FORWARD         20  'to 20'
             16_0  COME_FROM             8  '8'

 L. 248        16  LOAD_GLOBAL              DISPATCH_PROPERTYPUT
               18  STORE_FAST               'invkind'
             20_0  COME_FROM            14  '14'

 L. 250        20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'name'
               24  LOAD_GLOBAL              tuple
               26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_FALSE    42  'to 42'

 L. 251        30  LOAD_FAST                'name'
               32  LOAD_FAST                'value'
               34  BUILD_TUPLE_1         1 
               36  BINARY_ADD       
               38  STORE_FAST               'args'
               40  JUMP_FORWARD         66  'to 66'
             42_0  COME_FROM            28  '28'

 L. 252        42  LOAD_FAST                'name'
               44  LOAD_GLOBAL              _all_slice
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE    58  'to 58'

 L. 253        50  LOAD_FAST                'value'
               52  BUILD_TUPLE_1         1 
               54  STORE_FAST               'args'
               56  JUMP_FORWARD         66  'to 66'
             58_0  COME_FROM            48  '48'

 L. 255        58  LOAD_FAST                'name'
               60  LOAD_FAST                'value'
               62  BUILD_TUPLE_2         2 
               64  STORE_FAST               'args'
             66_0  COME_FROM            56  '56'
             66_1  COME_FROM            40  '40'

 L. 256        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _comobj
               70  LOAD_ATTR                _invoke
               72  LOAD_GLOBAL              DISPID_VALUE

 L. 257        74  LOAD_FAST                'invkind'

 L. 258        76  LOAD_CONST               0

 L. 256        78  BUILD_LIST_3          3 

 L. 259        80  LOAD_FAST                'args'

 L. 256        82  CALL_FINALLY         85  'to 85'
               84  WITH_CLEANUP_FINISH
               86  CALL_FUNCTION_EX      0  'positional arguments only'
               88  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 82

    def __iter__(self):
        punk = self._comobj._invokeDISPID_NEWENUM(DISPATCH_METHOD | DISPATCH_PROPERTYGET)0
        enum = punk.QueryInterface(IEnumVARIANT)
        enum._dynamic = True
        return enum