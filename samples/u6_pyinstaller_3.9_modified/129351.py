# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: comtypes\client\_events.py
import ctypes, traceback, comtypes, comtypes.hresult, comtypes.automation, comtypes.typeinfo, comtypes.connectionpoints
from comtypes.client._generate import GetModule
import logging
logger = logging.getLogger(__name__)

class _AdviseConnection(object):

    def __init__(self, source, interface, receiver):
        self.cp = None
        self.cookie = None
        self.receiver = None
        self._connect(source, interface, receiver)

    def _connect(self, source, interface, receiver):
        cpc = source.QueryInterface(comtypes.connectionpoints.IConnectionPointContainer)
        self.cp = cpc.FindConnectionPoint(ctypes.byref(interface._iid_))
        logger.debug('Start advise %s', interface)
        self.cookie = self.cp.Advise(receiver)
        self.receiver = receiver

    def disconnect(self):
        if self.cookie:
            self.cp.Unadvise(self.cookie)
            logger.debug('Unadvised %s', self.cp)
            self.cp = None
            self.cookie = None
            del self.receiver

    def __del__--- This code section failed: ---

 L.  35         0  SETUP_FINALLY        30  'to 30'

 L.  36         2  LOAD_FAST                'self'
                4  LOAD_ATTR                cookie
                6  LOAD_CONST               None
                8  <117>                 1  ''
               10  POP_JUMP_IF_FALSE    26  'to 26'

 L.  37        12  LOAD_FAST                'self'
               14  LOAD_ATTR                cp
               16  LOAD_METHOD              Unadvise
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                cookie
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          
             26_0  COME_FROM            10  '10'
               26  POP_BLOCK        
               28  JUMP_FORWARD         54  'to 54'
             30_0  COME_FROM_FINALLY     0  '0'

 L.  38        30  DUP_TOP          
               32  LOAD_GLOBAL              comtypes
               34  LOAD_ATTR                COMError
               36  LOAD_GLOBAL              WindowsError
               38  BUILD_TUPLE_2         2 
               40  <121>                52  ''
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L.  40        48  POP_EXCEPT       
               50  JUMP_FORWARD         54  'to 54'
               52  <48>             
             54_0  COME_FROM            50  '50'
             54_1  COME_FROM            28  '28'

Parse error at or near `<117>' instruction at offset 8


def FindOutgoingInterface--- This code section failed: ---

 L.  46         0  SETUP_FINALLY        30  'to 30'

 L.  47         2  LOAD_FAST                'source'
                4  LOAD_METHOD              QueryInterface
                6  LOAD_GLOBAL              comtypes
                8  LOAD_ATTR                typeinfo
               10  LOAD_ATTR                IProvideClassInfo2
               12  CALL_METHOD_1         1  ''
               14  STORE_FAST               'pci'

 L.  48        16  LOAD_FAST                'pci'
               18  LOAD_METHOD              GetGUID
               20  LOAD_CONST               1
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'guid'
               26  POP_BLOCK        
               28  JUMP_FORWARD         50  'to 50'
             30_0  COME_FROM_FINALLY     0  '0'

 L.  49        30  DUP_TOP          
               32  LOAD_GLOBAL              comtypes
               34  LOAD_ATTR                COMError
               36  <121>                48  ''
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L.  50        44  POP_EXCEPT       
               46  JUMP_FORWARD        148  'to 148'
               48  <48>             
             50_0  COME_FROM            28  '28'

 L.  53        50  SETUP_FINALLY        70  'to 70'

 L.  54        52  LOAD_GLOBAL              comtypes
               54  LOAD_ATTR                com_interface_registry
               56  LOAD_GLOBAL              str
               58  LOAD_FAST                'guid'
               60  CALL_FUNCTION_1       1  ''
               62  BINARY_SUBSCR    
               64  STORE_FAST               'interface'
               66  POP_BLOCK        
               68  JUMP_FORWARD        130  'to 130'
             70_0  COME_FROM_FINALLY    50  '50'

 L.  55        70  DUP_TOP          
               72  LOAD_GLOBAL              KeyError
               74  <121>               128  ''
               76  POP_TOP          
               78  POP_TOP          
               80  POP_TOP          

 L.  56        82  LOAD_FAST                'pci'
               84  LOAD_METHOD              GetClassInfo
               86  CALL_METHOD_0         0  ''
               88  STORE_FAST               'tinfo'

 L.  57        90  LOAD_FAST                'tinfo'
               92  LOAD_METHOD              GetContainingTypeLib
               94  CALL_METHOD_0         0  ''
               96  UNPACK_SEQUENCE_2     2 
               98  STORE_FAST               'tlib'
              100  STORE_FAST               'index'

 L.  58       102  LOAD_GLOBAL              GetModule
              104  LOAD_FAST                'tlib'
              106  CALL_FUNCTION_1       1  ''
              108  POP_TOP          

 L.  59       110  LOAD_GLOBAL              comtypes
              112  LOAD_ATTR                com_interface_registry
              114  LOAD_GLOBAL              str
              116  LOAD_FAST                'guid'
              118  CALL_FUNCTION_1       1  ''
              120  BINARY_SUBSCR    
              122  STORE_FAST               'interface'
              124  POP_EXCEPT       
              126  JUMP_FORWARD        130  'to 130'
              128  <48>             
            130_0  COME_FROM           126  '126'
            130_1  COME_FROM            68  '68'

 L.  60       130  LOAD_GLOBAL              logger
              132  LOAD_METHOD              debug
              134  LOAD_STR                 '%s using sinkinterface %s'
              136  LOAD_FAST                'source'
              138  LOAD_FAST                'interface'
              140  CALL_METHOD_3         3  ''
              142  POP_TOP          

 L.  61       144  LOAD_FAST                'interface'
              146  RETURN_VALUE     
            148_0  COME_FROM            46  '46'

 L.  66       148  LOAD_FAST                'source'
              150  LOAD_ATTR                __dict__
              152  LOAD_METHOD              get
              154  LOAD_STR                 '__clsid'
              156  CALL_METHOD_1         1  ''
              158  STORE_FAST               'clsid'

 L.  67       160  SETUP_FINALLY       182  'to 182'

 L.  68       162  LOAD_GLOBAL              comtypes
              164  LOAD_ATTR                com_coclass_registry
              166  LOAD_FAST                'clsid'
              168  BINARY_SUBSCR    
              170  LOAD_ATTR                _outgoing_interfaces_
              172  LOAD_CONST               0
              174  BINARY_SUBSCR    
              176  STORE_FAST               'interface'
              178  POP_BLOCK        
              180  JUMP_FORWARD        200  'to 200'
            182_0  COME_FROM_FINALLY   160  '160'

 L.  69       182  DUP_TOP          
              184  LOAD_GLOBAL              KeyError
              186  <121>               198  ''
              188  POP_TOP          
              190  POP_TOP          
              192  POP_TOP          

 L.  70       194  POP_EXCEPT       
              196  JUMP_FORWARD        218  'to 218'
              198  <48>             
            200_0  COME_FROM           180  '180'

 L.  72       200  LOAD_GLOBAL              logger
              202  LOAD_METHOD              debug
              204  LOAD_STR                 '%s using sinkinterface from clsid %s'
              206  LOAD_FAST                'source'
              208  LOAD_FAST                'interface'
              210  CALL_METHOD_3         3  ''
              212  POP_TOP          

 L.  73       214  LOAD_FAST                'interface'
              216  RETURN_VALUE     
            218_0  COME_FROM           196  '196'

 L.  79       218  LOAD_GLOBAL              TypeError
              220  LOAD_STR                 'cannot determine source interface'
              222  CALL_FUNCTION_1       1  ''
              224  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<121>' instruction at offset 36


def find_single_connection_interface--- This code section failed: ---

 L.  85         0  LOAD_FAST                'source'
                2  LOAD_METHOD              QueryInterface
                4  LOAD_GLOBAL              comtypes
                6  LOAD_ATTR                connectionpoints
                8  LOAD_ATTR                IConnectionPointContainer
               10  CALL_METHOD_1         1  ''
               12  STORE_FAST               'cpc'

 L.  86        14  LOAD_FAST                'cpc'
               16  LOAD_METHOD              EnumConnectionPoints
               18  CALL_METHOD_0         0  ''
               20  STORE_FAST               'enum'

 L.  87        22  LOAD_FAST                'enum'
               24  LOAD_METHOD              next
               26  CALL_METHOD_0         0  ''
               28  LOAD_METHOD              GetConnectionInterface
               30  CALL_METHOD_0         0  ''
               32  STORE_FAST               'iid'

 L.  88        34  SETUP_FINALLY        48  'to 48'

 L.  89        36  LOAD_GLOBAL              next
               38  LOAD_FAST                'enum'
               40  CALL_FUNCTION_1       1  ''
               42  POP_TOP          
               44  POP_BLOCK        
               46  JUMP_FORWARD        130  'to 130'
             48_0  COME_FROM_FINALLY    34  '34'

 L.  90        48  DUP_TOP          
               50  LOAD_GLOBAL              StopIteration
               52  <121>               128  ''
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L.  91        60  SETUP_FINALLY        80  'to 80'

 L.  92        62  LOAD_GLOBAL              comtypes
               64  LOAD_ATTR                com_interface_registry
               66  LOAD_GLOBAL              str
               68  LOAD_FAST                'iid'
               70  CALL_FUNCTION_1       1  ''
               72  BINARY_SUBSCR    
               74  STORE_FAST               'interface'
               76  POP_BLOCK        
               78  JUMP_FORWARD        102  'to 102'
             80_0  COME_FROM_FINALLY    60  '60'

 L.  93        80  DUP_TOP          
               82  LOAD_GLOBAL              KeyError
               84  <121>               100  ''
               86  POP_TOP          
               88  POP_TOP          
               90  POP_TOP          

 L.  94        92  POP_EXCEPT       
               94  POP_EXCEPT       
               96  LOAD_CONST               None
               98  RETURN_VALUE     
              100  <48>             
            102_0  COME_FROM            78  '78'

 L.  96       102  LOAD_GLOBAL              logger
              104  LOAD_METHOD              debug
              106  LOAD_STR                 '%s using sinkinterface from iid %s'
              108  LOAD_FAST                'source'
              110  LOAD_FAST                'interface'
              112  CALL_METHOD_3         3  ''
              114  POP_TOP          

 L.  97       116  LOAD_FAST                'interface'
              118  ROT_FOUR         
              120  POP_EXCEPT       
              122  RETURN_VALUE     
              124  POP_EXCEPT       
              126  JUMP_FORWARD        142  'to 142'
              128  <48>             
            130_0  COME_FROM            46  '46'

 L.  99       130  LOAD_GLOBAL              logger
              132  LOAD_METHOD              debug
              134  LOAD_STR                 '%s has more than one connection point'
              136  LOAD_FAST                'source'
              138  CALL_METHOD_2         2  ''
              140  POP_TOP          
            142_0  COME_FROM           126  '126'

Parse error at or near `<121>' instruction at offset 52


def report_errors(func):
    if func.__code__.co_varnames[:2] == ('self', 'this'):

        def error_printer--- This code section failed: ---

 L. 109         0  SETUP_FINALLY        28  'to 28'

 L. 110         2  LOAD_DEREF               'func'
                4  LOAD_FAST                'self'
                6  LOAD_FAST                'this'
                8  BUILD_LIST_2          2 
               10  LOAD_FAST                'args'
               12  CALL_FINALLY         15  'to 15'
               14  WITH_CLEANUP_FINISH
               16  BUILD_MAP_0           0 
               18  LOAD_FAST                'kw'
               20  <164>                 1  ''
               22  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               24  POP_BLOCK        
               26  RETURN_VALUE     
             28_0  COME_FROM_FINALLY     0  '0'

 L. 111        28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 112        34  LOAD_GLOBAL              traceback
               36  LOAD_METHOD              print_exc
               38  CALL_METHOD_0         0  ''
               40  POP_TOP          

 L. 113        42  RAISE_VARARGS_0       0  'reraise'
               44  POP_EXCEPT       
               46  JUMP_FORWARD         50  'to 50'
               48  <48>             
             50_0  COME_FROM            46  '46'

Parse error at or near `CALL_FINALLY' instruction at offset 12

    else:

        def error_printer--- This code section failed: ---

 L. 116         0  SETUP_FINALLY        18  'to 18'

 L. 117         2  LOAD_DEREF               'func'
                4  LOAD_FAST                'args'
                6  BUILD_MAP_0           0 
                8  LOAD_FAST                'kw'
               10  <164>                 1  ''
               12  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               14  POP_BLOCK        
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L. 118        18  POP_TOP          
               20  POP_TOP          
               22  POP_TOP          

 L. 119        24  LOAD_GLOBAL              traceback
               26  LOAD_METHOD              print_exc
               28  CALL_METHOD_0         0  ''
               30  POP_TOP          

 L. 120        32  RAISE_VARARGS_0       0  'reraise'
               34  POP_EXCEPT       
               36  JUMP_FORWARD         40  'to 40'
               38  <48>             
             40_0  COME_FROM            36  '36'

Parse error at or near `<164>' instruction at offset 10

    return error_printer


from comtypes._comobject import _MethodFinder

class _SinkMethodFinder(_MethodFinder):
    __doc__ = "Special MethodFinder, for finding and decorating event handler\n    methods.  Looks for methods on two objects. Also decorates the\n    event handlers with 'report_errors' which will print exceptions in\n    event handlers.\n    "

    def __init__(self, inst, sink):
        super(_SinkMethodFinder, self).__init__(inst)
        self.sink = sink

    def find_method--- This code section failed: ---

 L. 135         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _find_method
                4  LOAD_FAST                'fq_name'
                6  LOAD_FAST                'mthname'
                8  CALL_METHOD_2         2  ''
               10  STORE_FAST               'impl'

 L. 139        12  SETUP_FINALLY        56  'to 56'

 L. 141        14  LOAD_FAST                'impl'
               16  LOAD_ATTR                __self__
               18  LOAD_FAST                'impl'
               20  LOAD_ATTR                __func__
               22  ROT_TWO          
               24  STORE_FAST               'im_self'
               26  STORE_FAST               'im_func'

 L. 143        28  LOAD_GLOBAL              report_errors
               30  LOAD_FAST                'im_func'
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'method'

 L. 145        36  LOAD_GLOBAL              comtypes
               38  LOAD_METHOD              instancemethod
               40  LOAD_FAST                'method'

 L. 146        42  LOAD_FAST                'im_self'

 L. 147        44  LOAD_GLOBAL              type
               46  LOAD_FAST                'im_self'
               48  CALL_FUNCTION_1       1  ''

 L. 145        50  CALL_METHOD_3         3  ''
               52  POP_BLOCK        
               54  RETURN_VALUE     
             56_0  COME_FROM_FINALLY    12  '12'

 L. 148        56  DUP_TOP          
               58  LOAD_GLOBAL              AttributeError
               60  <121>                98  ''
               62  POP_TOP          
               64  STORE_FAST               'details'
               66  POP_TOP          
               68  SETUP_FINALLY        90  'to 90'

 L. 149        70  LOAD_GLOBAL              RuntimeError
               72  LOAD_FAST                'details'
               74  CALL_FUNCTION_1       1  ''
               76  RAISE_VARARGS_1       1  'exception instance'
               78  POP_BLOCK        
               80  POP_EXCEPT       
               82  LOAD_CONST               None
               84  STORE_FAST               'details'
               86  DELETE_FAST              'details'
               88  JUMP_FORWARD        100  'to 100'
             90_0  COME_FROM_FINALLY    68  '68'
               90  LOAD_CONST               None
               92  STORE_FAST               'details'
               94  DELETE_FAST              'details'
               96  <48>             
               98  <48>             
            100_0  COME_FROM            88  '88'

Parse error at or near `<121>' instruction at offset 60

    def _find_method--- This code section failed: ---

 L. 152         0  SETUP_FINALLY        22  'to 22'

 L. 153         2  LOAD_GLOBAL              super
                4  LOAD_GLOBAL              _SinkMethodFinder
                6  LOAD_FAST                'self'
                8  CALL_FUNCTION_2       2  ''
               10  LOAD_METHOD              find_method
               12  LOAD_FAST                'fq_name'
               14  LOAD_FAST                'mthname'
               16  CALL_METHOD_2         2  ''
               18  POP_BLOCK        
               20  RETURN_VALUE     
             22_0  COME_FROM_FINALLY     0  '0'

 L. 154        22  DUP_TOP          
               24  LOAD_GLOBAL              AttributeError
               26  <121>                92  ''
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 155        34  SETUP_FINALLY        54  'to 54'

 L. 156        36  LOAD_GLOBAL              getattr
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                sink
               42  LOAD_FAST                'fq_name'
               44  CALL_FUNCTION_2       2  ''
               46  POP_BLOCK        
               48  ROT_FOUR         
               50  POP_EXCEPT       
               52  RETURN_VALUE     
             54_0  COME_FROM_FINALLY    34  '34'

 L. 157        54  DUP_TOP          
               56  LOAD_GLOBAL              AttributeError
               58  <121>                86  ''
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L. 158        66  LOAD_GLOBAL              getattr
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                sink
               72  LOAD_FAST                'mthname'
               74  CALL_FUNCTION_2       2  ''
               76  ROT_FOUR         
               78  POP_EXCEPT       
               80  ROT_FOUR         
               82  POP_EXCEPT       
               84  RETURN_VALUE     
               86  <48>             
               88  POP_EXCEPT       
               90  JUMP_FORWARD         94  'to 94'
               92  <48>             
             94_0  COME_FROM            90  '90'

Parse error at or near `<121>' instruction at offset 26


def CreateEventReceiver(interface, handler):

    class Sink(comtypes.COMObject):
        _com_interfaces_ = [
         interface]

        def _get_method_finder_(self, itf):
            return _SinkMethodFinder(self, handler)

    sink = Sink()
    if issubclass(interface, comtypes.automation.IDispatch):
        if not hasattr(sink, '_dispimpl_'):
            finder = sink._get_method_finder_(interface)
            dispimpl = sink._dispimpl_ = {}
            for m in interface._methods_:
                restype, mthname, argtypes, paramflags, idlflags, helptext = m
                dispid = idlflags[0]
                impl = finder.get_impl(interface, mthname, paramflags, idlflags)
                dispimpl[(dispid, comtypes.automation.DISPATCH_METHOD)] = impl

    return sink


def GetEvents--- This code section failed: ---

 L. 198         0  LOAD_FAST                'interface'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 199         8  LOAD_GLOBAL              FindOutgoingInterface
               10  LOAD_FAST                'source'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'interface'
             16_0  COME_FROM             6  '6'

 L. 201        16  LOAD_GLOBAL              CreateEventReceiver
               18  LOAD_FAST                'interface'
               20  LOAD_FAST                'sink'
               22  CALL_FUNCTION_2       2  ''
               24  STORE_FAST               'rcv'

 L. 202        26  LOAD_GLOBAL              _AdviseConnection
               28  LOAD_FAST                'source'
               30  LOAD_FAST                'interface'
               32  LOAD_FAST                'rcv'
               34  CALL_FUNCTION_3       3  ''
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class EventDumper(object):
    __doc__ = 'Universal sink for COM events.'

    def __getattr__(self, name):
        """Create event handler methods on demand"""
        if name.startswith('__'):
            if name.endswith('__'):
                raise AttributeError(name)
        print('# event found:', name)

        def handler(self, this, *args, **kw):
            args = (None, ) + args
            print('Event %s(%s)' % (name, ', '.join([repr(a) for a in args])))

        return comtypes.instancemethod(handler, self, EventDumper)


def ShowEvents(source, interface=None):
    """Receive COM events from 'source'.  A special event sink will be
    used that first prints the names of events that are found in the
    outgoing interface, and will also print out the events when they
    are fired.
    """
    return comtypes.client.GetEvents(source, sink=(EventDumper()), interface=interface)


_handles_type = ctypes.c_void_p * 1

def PumpEvents--- This code section failed: ---

 L. 258         0  LOAD_GLOBAL              ctypes
                2  LOAD_ATTR                windll
                4  LOAD_ATTR                kernel32
                6  LOAD_METHOD              CreateEventA
                8  LOAD_CONST               None
               10  LOAD_CONST               True
               12  LOAD_CONST               False
               14  LOAD_CONST               None
               16  CALL_METHOD_4         4  ''
               18  STORE_DEREF              'hevt'

 L. 259        20  LOAD_GLOBAL              _handles_type
               22  LOAD_DEREF               'hevt'
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'handles'

 L. 260        28  LOAD_CONST               -2147417835
               30  STORE_FAST               'RPC_S_CALLPENDING'

 L. 263        32  LOAD_CLOSURE             'hevt'
               34  BUILD_TUPLE_1         1 
               36  LOAD_CODE                <code_object HandlerRoutine>
               38  LOAD_STR                 'PumpEvents.<locals>.HandlerRoutine'
               40  MAKE_FUNCTION_8          'closure'
               42  STORE_FAST               'HandlerRoutine'

 L. 268        44  LOAD_GLOBAL              ctypes
               46  LOAD_METHOD              WINFUNCTYPE
               48  LOAD_GLOBAL              ctypes
               50  LOAD_ATTR                c_int
               52  LOAD_GLOBAL              ctypes
               54  LOAD_ATTR                c_uint
               56  CALL_METHOD_2         2  ''
               58  LOAD_FAST                'HandlerRoutine'
               60  CALL_FUNCTION_1       1  ''
               62  STORE_FAST               'HandlerRoutine'

 L. 270        64  LOAD_GLOBAL              ctypes
               66  LOAD_ATTR                windll
               68  LOAD_ATTR                kernel32
               70  LOAD_METHOD              SetConsoleCtrlHandler
               72  LOAD_FAST                'HandlerRoutine'
               74  LOAD_CONST               1
               76  CALL_METHOD_2         2  ''
               78  POP_TOP          

 L. 272        80  SETUP_FINALLY       218  'to 218'

 L. 273        82  SETUP_FINALLY       132  'to 132'

 L. 274        84  LOAD_GLOBAL              ctypes
               86  LOAD_ATTR                oledll
               88  LOAD_ATTR                ole32
               90  LOAD_METHOD              CoWaitForMultipleHandles
               92  LOAD_CONST               0

 L. 275        94  LOAD_GLOBAL              int
               96  LOAD_FAST                'timeout'
               98  LOAD_CONST               1000
              100  BINARY_MULTIPLY  
              102  CALL_FUNCTION_1       1  ''

 L. 276       104  LOAD_GLOBAL              len
              106  LOAD_FAST                'handles'
              108  CALL_FUNCTION_1       1  ''
              110  LOAD_FAST                'handles'

 L. 277       112  LOAD_GLOBAL              ctypes
              114  LOAD_METHOD              byref
              116  LOAD_GLOBAL              ctypes
              118  LOAD_METHOD              c_ulong
              120  CALL_METHOD_0         0  ''
              122  CALL_METHOD_1         1  ''

 L. 274       124  CALL_METHOD_5         5  ''
              126  STORE_FAST               'res'
              128  POP_BLOCK        
              130  JUMP_FORWARD        180  'to 180'
            132_0  COME_FROM_FINALLY    82  '82'

 L. 278       132  DUP_TOP          
              134  LOAD_GLOBAL              WindowsError
              136  <121>               178  ''
              138  POP_TOP          
              140  STORE_FAST               'details'
              142  POP_TOP          
              144  SETUP_FINALLY       170  'to 170'

 L. 279       146  LOAD_FAST                'details'
              148  LOAD_ATTR                winerror
              150  LOAD_FAST                'RPC_S_CALLPENDING'
              152  COMPARE_OP               !=
              154  POP_JUMP_IF_FALSE   158  'to 158'

 L. 280       156  RAISE_VARARGS_0       0  'reraise'
            158_0  COME_FROM           154  '154'
              158  POP_BLOCK        
              160  POP_EXCEPT       
              162  LOAD_CONST               None
              164  STORE_FAST               'details'
              166  DELETE_FAST              'details'
              168  JUMP_FORWARD        184  'to 184'
            170_0  COME_FROM_FINALLY   144  '144'
              170  LOAD_CONST               None
              172  STORE_FAST               'details'
              174  DELETE_FAST              'details'
              176  <48>             
              178  <48>             
            180_0  COME_FROM           130  '130'

 L. 282       180  LOAD_GLOBAL              KeyboardInterrupt
              182  RAISE_VARARGS_1       1  'exception instance'
            184_0  COME_FROM           168  '168'
              184  POP_BLOCK        

 L. 284       186  LOAD_GLOBAL              ctypes
              188  LOAD_ATTR                windll
              190  LOAD_ATTR                kernel32
              192  LOAD_METHOD              CloseHandle
              194  LOAD_DEREF               'hevt'
              196  CALL_METHOD_1         1  ''
              198  POP_TOP          

 L. 285       200  LOAD_GLOBAL              ctypes
              202  LOAD_ATTR                windll
              204  LOAD_ATTR                kernel32
              206  LOAD_METHOD              SetConsoleCtrlHandler
              208  LOAD_FAST                'HandlerRoutine'
              210  LOAD_CONST               0
              212  CALL_METHOD_2         2  ''
              214  POP_TOP          
              216  JUMP_FORWARD        250  'to 250'
            218_0  COME_FROM_FINALLY    80  '80'

 L. 284       218  LOAD_GLOBAL              ctypes
              220  LOAD_ATTR                windll
              222  LOAD_ATTR                kernel32
              224  LOAD_METHOD              CloseHandle
              226  LOAD_DEREF               'hevt'
              228  CALL_METHOD_1         1  ''
              230  POP_TOP          

 L. 285       232  LOAD_GLOBAL              ctypes
              234  LOAD_ATTR                windll
              236  LOAD_ATTR                kernel32
              238  LOAD_METHOD              SetConsoleCtrlHandler
              240  LOAD_FAST                'HandlerRoutine'
              242  LOAD_CONST               0
              244  CALL_METHOD_2         2  ''
              246  POP_TOP          
              248  <48>             
            250_0  COME_FROM           216  '216'

Parse error at or near `<121>' instruction at offset 136