# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
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

    def __del__(self):
        try:
            if self.cookie is not None:
                self.cp.Unadvise(self.cookie)
        except (comtypes.COMError, WindowsError):
            pass


def FindOutgoingInterface(source):
    """XXX Describe the strategy that is used..."""
    try:
        pci = source.QueryInterface(comtypes.typeinfo.IProvideClassInfo2)
        guid = pci.GetGUID(1)
    except comtypes.COMError:
        pass
    else:
        try:
            interface = comtypes.com_interface_registry[str(guid)]
        except KeyError:
            tinfo = pci.GetClassInfo()
            tlib, index = tinfo.GetContainingTypeLib()
            GetModule(tlib)
            interface = comtypes.com_interface_registry[str(guid)]
        else:
            logger.debug('%s using sinkinterface %s', source, interface)
            return interface
            clsid = source.__dict__.get('__clsid')
            try:
                interface = comtypes.com_coclass_registry[clsid]._outgoing_interfaces_[0]
            except KeyError:
                pass
            else:
                logger.debug('%s using sinkinterface from clsid %s', source, interface)
                return interface
                raise TypeError('cannot determine source interface')


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
               46  JUMP_FORWARD        134  'to 134'
             48_0  COME_FROM_FINALLY    34  '34'

 L.  90        48  DUP_TOP          
               50  LOAD_GLOBAL              StopIteration
               52  COMPARE_OP               exception-match
               54  POP_JUMP_IF_FALSE   132  'to 132'
               56  POP_TOP          
               58  POP_TOP          
               60  POP_TOP          

 L.  91        62  SETUP_FINALLY        82  'to 82'

 L.  92        64  LOAD_GLOBAL              comtypes
               66  LOAD_ATTR                com_interface_registry
               68  LOAD_GLOBAL              str
               70  LOAD_FAST                'iid'
               72  CALL_FUNCTION_1       1  ''
               74  BINARY_SUBSCR    
               76  STORE_FAST               'interface'
               78  POP_BLOCK        
               80  JUMP_FORWARD        106  'to 106'
             82_0  COME_FROM_FINALLY    62  '62'

 L.  93        82  DUP_TOP          
               84  LOAD_GLOBAL              KeyError
               86  COMPARE_OP               exception-match
               88  POP_JUMP_IF_FALSE   104  'to 104'
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          

 L.  94        96  POP_EXCEPT       
               98  POP_EXCEPT       
              100  LOAD_CONST               None
              102  RETURN_VALUE     
            104_0  COME_FROM            88  '88'
              104  END_FINALLY      
            106_0  COME_FROM            80  '80'

 L.  96       106  LOAD_GLOBAL              logger
              108  LOAD_METHOD              debug
              110  LOAD_STR                 '%s using sinkinterface from iid %s'
              112  LOAD_FAST                'source'
              114  LOAD_FAST                'interface'
              116  CALL_METHOD_3         3  ''
              118  POP_TOP          

 L.  97       120  LOAD_FAST                'interface'
              122  ROT_FOUR         
              124  POP_EXCEPT       
              126  RETURN_VALUE     
              128  POP_EXCEPT       
              130  JUMP_FORWARD        146  'to 146'
            132_0  COME_FROM            54  '54'
              132  END_FINALLY      
            134_0  COME_FROM            46  '46'

 L.  99       134  LOAD_GLOBAL              logger
              136  LOAD_METHOD              debug
              138  LOAD_STR                 '%s has more than one connection point'
              140  LOAD_FAST                'source'
              142  CALL_METHOD_2         2  ''
              144  POP_TOP          
            146_0  COME_FROM           130  '130'

Parse error at or near `LOAD_CONST' instruction at offset 100


def report_errors(func):
    if func.__code__.co_varnames[:2] == ('self', 'this'):

        def error_printer--- This code section failed: ---

 L. 109         0  SETUP_FINALLY        22  'to 22'

 L. 110         2  LOAD_DEREF               'func'
                4  LOAD_FAST                'self'
                6  LOAD_FAST                'this'
                8  BUILD_TUPLE_2         2 
               10  LOAD_FAST                'args'
               12  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
               14  LOAD_FAST                'kw'
               16  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               18  POP_BLOCK        
               20  RETURN_VALUE     
             22_0  COME_FROM_FINALLY     0  '0'

 L. 111        22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 112        28  LOAD_GLOBAL              traceback
               30  LOAD_METHOD              print_exc
               32  CALL_METHOD_0         0  ''
               34  POP_TOP          

 L. 113        36  RAISE_VARARGS_0       0  'reraise'
               38  POP_EXCEPT       
               40  JUMP_FORWARD         44  'to 44'
               42  END_FINALLY      
             44_0  COME_FROM            40  '40'

Parse error at or near `POP_TOP' instruction at offset 34

    else:

        def error_printer--- This code section failed: ---

 L. 116         0  SETUP_FINALLY        14  'to 14'

 L. 117         2  LOAD_DEREF               'func'
                4  LOAD_FAST                'args'
                6  LOAD_FAST                'kw'
                8  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 118        14  POP_TOP          
               16  POP_TOP          
               18  POP_TOP          

 L. 119        20  LOAD_GLOBAL              traceback
               22  LOAD_METHOD              print_exc
               24  CALL_METHOD_0         0  ''
               26  POP_TOP          

 L. 120        28  RAISE_VARARGS_0       0  'reraise'
               30  POP_EXCEPT       
               32  JUMP_FORWARD         36  'to 36'
               34  END_FINALLY      
             36_0  COME_FROM            32  '32'

Parse error at or near `POP_TOP' instruction at offset 26

    return error_printer


from comtypes._comobject import _MethodFinder

class _SinkMethodFinder(_MethodFinder):
    __doc__ = "Special MethodFinder, for finding and decorating event handler\n    methods.  Looks for methods on two objects. Also decorates the\n    event handlers with 'report_errors' which will print exceptions in\n    event handlers.\n    "

    def __init__(self, inst, sink):
        super(_SinkMethodFinder, self).__init__(inst)
        self.sink = sink

    def find_method(self, fq_name, mthname):
        impl = self._find_method(fq_name, mthname)
        try:
            im_self, im_func = impl.__self__, impl.__func__
            method = report_errors(im_func)
            return comtypes.instancemethod(method, im_self, type(im_self))
            except AttributeError as details:
            try:
                raise RuntimeError(details)
            finally:
                details = None
                del details

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
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    96  'to 96'
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L. 155        36  SETUP_FINALLY        56  'to 56'

 L. 156        38  LOAD_GLOBAL              getattr
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                sink
               44  LOAD_FAST                'fq_name'
               46  CALL_FUNCTION_2       2  ''
               48  POP_BLOCK        
               50  ROT_FOUR         
               52  POP_EXCEPT       
               54  RETURN_VALUE     
             56_0  COME_FROM_FINALLY    36  '36'

 L. 157        56  DUP_TOP          
               58  LOAD_GLOBAL              AttributeError
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE    90  'to 90'
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          

 L. 158        70  LOAD_GLOBAL              getattr
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                sink
               76  LOAD_FAST                'mthname'
               78  CALL_FUNCTION_2       2  ''
               80  ROT_FOUR         
               82  POP_EXCEPT       
               84  ROT_FOUR         
               86  POP_EXCEPT       
               88  RETURN_VALUE     
             90_0  COME_FROM            62  '62'
               90  END_FINALLY      
               92  POP_EXCEPT       
               94  JUMP_FORWARD         98  'to 98'
             96_0  COME_FROM            28  '28'
               96  END_FINALLY      
             98_0  COME_FROM            94  '94'

Parse error at or near `POP_TOP' instruction at offset 32


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


def GetEvents(source, sink, interface=None):
    """Receive COM events from 'source'.  Events will call methods on
    the 'sink' object.  'interface' is the source interface to use.
    """
    if interface is None:
        interface = FindOutgoingInterface(source)
    rcv = CreateEventReceiver(interface, sink)
    return _AdviseConnection(source, interface, rcv)


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

def PumpEvents(timeout):
    """This following code waits for 'timeout' seconds in the way
    required for COM, internally doing the correct things depending
    on the COM appartment of the current thread.  It is possible to
    terminate the message loop by pressing CTRL+C, which will raise
    a KeyboardInterrupt.
    """
    hevt = ctypes.windll.kernel32.CreateEventA(None, True, False, None)
    handles = _handles_type(hevt)
    RPC_S_CALLPENDING = -2147417835

    def HandlerRoutine(dwCtrlType):
        if dwCtrlType == 0:
            ctypes.windll.kernel32.SetEvent(hevt)
            return 1
        return 0

    HandlerRoutine = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_uint)(HandlerRoutine)
    ctypes.windll.kernel32.SetConsoleCtrlHandler(HandlerRoutine, 1)
    try:
        try:
            res = ctypes.oledll.ole32.CoWaitForMultipleHandles(0, int(timeout * 1000), len(handles), handles, ctypes.byref(ctypes.c_ulong()))
        except WindowsError as details:
            try:
                if details.args[0] != RPC_S_CALLPENDING:
                    raise
            finally:
                details = None
                del details

        else:
            raise KeyboardInterrupt
    finally:
        ctypes.windll.kernel32.CloseHandle(hevt)
        ctypes.windll.kernel32.SetConsoleCtrlHandler(HandlerRoutine, 0)