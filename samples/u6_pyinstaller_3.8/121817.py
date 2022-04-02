# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: comtypes\client\__init__.py
"""comtypes.client - High level client level COM support package.
"""
import sys, os, ctypes, comtypes
from comtypes.hresult import *
import comtypes.automation, comtypes.typeinfo, comtypes.client.dynamic
from comtypes.client._events import GetEvents, ShowEvents, PumpEvents
from comtypes.client._generate import GetModule
import logging
logger = logging.getLogger(__name__)
__all__ = [
 'CreateObject', 'GetActiveObject', 'CoGetObject',
 'GetEvents', 'ShowEvents', 'PumpEvents', 'GetModule',
 'GetClassObject']
from comtypes.client._code_cache import _find_gen_dir
gen_dir = _find_gen_dir()
import comtypes.gen

def wrap_outparam(punk):
    logger.debug('wrap_outparam(%s)', punk)
    if not punk:
        return
    if punk.__com_interface__ == comtypes.automation.IDispatch:
        return GetBestInterface(punk)
    return punk


def GetBestInterface--- This code section failed: ---

 L.  56         0  LOAD_FAST                'punk'
                2  POP_JUMP_IF_TRUE      8  'to 8'

 L.  57         4  LOAD_FAST                'punk'
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L.  59         8  LOAD_GLOBAL              logger
               10  LOAD_METHOD              debug
               12  LOAD_STR                 'GetBestInterface(%s)'
               14  LOAD_FAST                'punk'
               16  CALL_METHOD_2         2  ''
               18  POP_TOP          

 L.  60        20  SETUP_FINALLY       204  'to 204'

 L.  61        22  SETUP_FINALLY        52  'to 52'

 L.  62        24  LOAD_FAST                'punk'
               26  LOAD_METHOD              QueryInterface
               28  LOAD_GLOBAL              comtypes
               30  LOAD_ATTR                typeinfo
               32  LOAD_ATTR                IProvideClassInfo
               34  CALL_METHOD_1         1  ''
               36  STORE_FAST               'pci'

 L.  63        38  LOAD_GLOBAL              logger
               40  LOAD_METHOD              debug
               42  LOAD_STR                 'Does implement IProvideClassInfo'
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          
               48  POP_BLOCK        
               50  JUMP_FORWARD        108  'to 108'
             52_0  COME_FROM_FINALLY    22  '22'

 L.  64        52  DUP_TOP          
               54  LOAD_GLOBAL              comtypes
               56  LOAD_ATTR                COMError
               58  COMPARE_OP               exception-match
               60  POP_JUMP_IF_FALSE   106  'to 106'
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L.  67        68  LOAD_GLOBAL              logger
               70  LOAD_METHOD              debug
               72  LOAD_STR                 'Does NOT implement IProvideClassInfo, trying IProvideClassInfo2'
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          

 L.  68        78  LOAD_FAST                'punk'
               80  LOAD_METHOD              QueryInterface
               82  LOAD_GLOBAL              comtypes
               84  LOAD_ATTR                typeinfo
               86  LOAD_ATTR                IProvideClassInfo2
               88  CALL_METHOD_1         1  ''
               90  STORE_FAST               'pci'

 L.  69        92  LOAD_GLOBAL              logger
               94  LOAD_METHOD              debug
               96  LOAD_STR                 'Does implement IProvideClassInfo2'
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          
              102  POP_EXCEPT       
              104  JUMP_FORWARD        108  'to 108'
            106_0  COME_FROM            60  '60'
              106  END_FINALLY      
            108_0  COME_FROM           104  '104'
            108_1  COME_FROM            50  '50'

 L.  70       108  LOAD_FAST                'pci'
              110  LOAD_METHOD              GetClassInfo
              112  CALL_METHOD_0         0  ''
              114  STORE_FAST               'tinfo'

 L.  72       116  LOAD_FAST                'tinfo'
              118  LOAD_METHOD              GetTypeAttr
              120  CALL_METHOD_0         0  ''
              122  STORE_FAST               'ta'

 L.  73       124  LOAD_GLOBAL              range
              126  LOAD_FAST                'ta'
              128  LOAD_ATTR                cImplTypes
              130  CALL_FUNCTION_1       1  ''
              132  GET_ITER         
            134_0  COME_FROM           150  '150'
              134  FOR_ITER            158  'to 158'
              136  STORE_FAST               'index'

 L.  74       138  LOAD_FAST                'tinfo'
              140  LOAD_METHOD              GetImplTypeFlags
              142  LOAD_FAST                'index'
              144  CALL_METHOD_1         1  ''
              146  LOAD_CONST               1
              148  COMPARE_OP               ==
              150  POP_JUMP_IF_FALSE   134  'to 134'

 L.  75       152  POP_TOP          
              154  BREAK_LOOP          180  'to 180'
              156  JUMP_BACK           134  'to 134'

 L.  77       158  LOAD_FAST                'ta'
              160  LOAD_ATTR                cImplTypes
              162  LOAD_CONST               1
              164  COMPARE_OP               !=
              166  POP_JUMP_IF_FALSE   176  'to 176'

 L.  79       168  LOAD_GLOBAL              TypeError
              170  LOAD_STR                 'No default interface found'
              172  CALL_FUNCTION_1       1  ''
              174  RAISE_VARARGS_1       1  'exception instance'
            176_0  COME_FROM           166  '166'

 L.  82       176  LOAD_CONST               0
              178  STORE_FAST               'index'

 L.  83       180  LOAD_FAST                'tinfo'
              182  LOAD_METHOD              GetRefTypeOfImplType
              184  LOAD_FAST                'index'
              186  CALL_METHOD_1         1  ''
              188  STORE_FAST               'href'

 L.  84       190  LOAD_FAST                'tinfo'
              192  LOAD_METHOD              GetRefTypeInfo
              194  LOAD_FAST                'href'
              196  CALL_METHOD_1         1  ''
              198  STORE_FAST               'tinfo'
              200  POP_BLOCK        
              202  JUMP_FORWARD        378  'to 378'
            204_0  COME_FROM_FINALLY    20  '20'

 L.  85       204  DUP_TOP          
              206  LOAD_GLOBAL              comtypes
              208  LOAD_ATTR                COMError
              210  COMPARE_OP               exception-match
          212_214  POP_JUMP_IF_FALSE   376  'to 376'
              216  POP_TOP          
              218  POP_TOP          
              220  POP_TOP          

 L.  86       222  LOAD_GLOBAL              logger
              224  LOAD_METHOD              debug
              226  LOAD_STR                 'Does NOT implement IProvideClassInfo/IProvideClassInfo2'
              228  CALL_METHOD_1         1  ''
              230  POP_TOP          

 L.  87       232  SETUP_FINALLY       252  'to 252'

 L.  88       234  LOAD_FAST                'punk'
              236  LOAD_METHOD              QueryInterface
              238  LOAD_GLOBAL              comtypes
              240  LOAD_ATTR                automation
              242  LOAD_ATTR                IDispatch
              244  CALL_METHOD_1         1  ''
              246  STORE_FAST               'pdisp'
              248  POP_BLOCK        
              250  JUMP_FORWARD        296  'to 296'
            252_0  COME_FROM_FINALLY   232  '232'

 L.  89       252  DUP_TOP          
              254  LOAD_GLOBAL              comtypes
              256  LOAD_ATTR                COMError
              258  COMPARE_OP               exception-match
          260_262  POP_JUMP_IF_FALSE   294  'to 294'
              264  POP_TOP          
              266  POP_TOP          
              268  POP_TOP          

 L.  90       270  LOAD_GLOBAL              logger
              272  LOAD_METHOD              debug
              274  LOAD_STR                 'No Dispatch interface: %s'
              276  LOAD_FAST                'punk'
              278  CALL_METHOD_2         2  ''
              280  POP_TOP          

 L.  91       282  LOAD_FAST                'punk'
              284  ROT_FOUR         
              286  POP_EXCEPT       
              288  ROT_FOUR         
              290  POP_EXCEPT       
              292  RETURN_VALUE     
            294_0  COME_FROM           260  '260'
              294  END_FINALLY      
            296_0  COME_FROM           250  '250'

 L.  92       296  SETUP_FINALLY       312  'to 312'

 L.  93       298  LOAD_FAST                'pdisp'
              300  LOAD_METHOD              GetTypeInfo
              302  LOAD_CONST               0
              304  CALL_METHOD_1         1  ''
              306  STORE_FAST               'tinfo'
              308  POP_BLOCK        
              310  JUMP_FORWARD        372  'to 372'
            312_0  COME_FROM_FINALLY   296  '296'

 L.  94       312  DUP_TOP          
              314  LOAD_GLOBAL              comtypes
              316  LOAD_ATTR                COMError
              318  COMPARE_OP               exception-match
          320_322  POP_JUMP_IF_FALSE   370  'to 370'
              324  POP_TOP          
              326  POP_TOP          
              328  POP_TOP          

 L.  95       330  LOAD_GLOBAL              comtypes
              332  LOAD_ATTR                client
              334  LOAD_ATTR                dynamic
              336  LOAD_METHOD              Dispatch
              338  LOAD_FAST                'pdisp'
              340  CALL_METHOD_1         1  ''
              342  STORE_FAST               'pdisp'

 L.  96       344  LOAD_GLOBAL              logger
              346  LOAD_METHOD              debug
              348  LOAD_STR                 'IDispatch.GetTypeInfo(0) failed: %s'
              350  LOAD_FAST                'pdisp'
              352  BINARY_MODULO    
              354  CALL_METHOD_1         1  ''
              356  POP_TOP          

 L.  97       358  LOAD_FAST                'pdisp'
              360  ROT_FOUR         
              362  POP_EXCEPT       
              364  ROT_FOUR         
              366  POP_EXCEPT       
              368  RETURN_VALUE     
            370_0  COME_FROM           320  '320'
              370  END_FINALLY      
            372_0  COME_FROM           310  '310'
              372  POP_EXCEPT       
              374  JUMP_FORWARD        378  'to 378'
            376_0  COME_FROM           212  '212'
              376  END_FINALLY      
            378_0  COME_FROM           374  '374'
            378_1  COME_FROM           202  '202'

 L.  98       378  LOAD_FAST                'tinfo'
              380  LOAD_METHOD              GetTypeAttr
              382  CALL_METHOD_0         0  ''
              384  STORE_FAST               'typeattr'

 L.  99       386  LOAD_GLOBAL              logger
              388  LOAD_METHOD              debug
              390  LOAD_STR                 'Default interface is %s'
              392  LOAD_FAST                'typeattr'
              394  LOAD_ATTR                guid
              396  CALL_METHOD_2         2  ''
              398  POP_TOP          

 L. 100       400  SETUP_FINALLY       422  'to 422'

 L. 101       402  LOAD_FAST                'punk'
              404  LOAD_METHOD              QueryInterface
              406  LOAD_GLOBAL              comtypes
              408  LOAD_ATTR                IUnknown
              410  LOAD_FAST                'typeattr'
              412  LOAD_ATTR                guid
              414  CALL_METHOD_2         2  ''
              416  POP_TOP          
              418  POP_BLOCK        
              420  JUMP_FORWARD        470  'to 470'
            422_0  COME_FROM_FINALLY   400  '400'

 L. 102       422  DUP_TOP          
              424  LOAD_GLOBAL              comtypes
              426  LOAD_ATTR                COMError
              428  COMPARE_OP               exception-match
          430_432  POP_JUMP_IF_FALSE   468  'to 468'
              434  POP_TOP          
              436  POP_TOP          
              438  POP_TOP          

 L. 103       440  LOAD_GLOBAL              logger
              442  LOAD_METHOD              debug
              444  LOAD_STR                 'Does not implement default interface, returning dynamic object'
              446  CALL_METHOD_1         1  ''
              448  POP_TOP          

 L. 104       450  LOAD_GLOBAL              comtypes
              452  LOAD_ATTR                client
              454  LOAD_ATTR                dynamic
              456  LOAD_METHOD              Dispatch
              458  LOAD_FAST                'punk'
              460  CALL_METHOD_1         1  ''
              462  ROT_FOUR         
              464  POP_EXCEPT       
              466  RETURN_VALUE     
            468_0  COME_FROM           430  '430'
              468  END_FINALLY      
            470_0  COME_FROM           420  '420'

 L. 106       470  LOAD_FAST                'tinfo'
              472  LOAD_METHOD              GetDocumentation
              474  LOAD_CONST               -1
              476  CALL_METHOD_1         1  ''
              478  LOAD_CONST               0
              480  BINARY_SUBSCR    
              482  STORE_FAST               'itf_name'

 L. 107       484  LOAD_FAST                'tinfo'
              486  LOAD_METHOD              GetContainingTypeLib
              488  CALL_METHOD_0         0  ''
              490  LOAD_CONST               0
              492  BINARY_SUBSCR    
              494  STORE_FAST               'tlib'

 L. 110       496  LOAD_GLOBAL              GetModule
              498  LOAD_FAST                'tlib'
              500  CALL_FUNCTION_1       1  ''
              502  STORE_FAST               'mod'

 L. 112       504  LOAD_GLOBAL              getattr
              506  LOAD_FAST                'mod'
              508  LOAD_FAST                'itf_name'
              510  CALL_FUNCTION_2       2  ''
              512  STORE_FAST               'interface'

 L. 113       514  LOAD_GLOBAL              logger
              516  LOAD_METHOD              debug
              518  LOAD_STR                 'Implements default interface from typeinfo %s'
              520  LOAD_FAST                'interface'
              522  CALL_METHOD_2         2  ''
              524  POP_TOP          

 L. 126       526  LOAD_FAST                'punk'
              528  LOAD_METHOD              QueryInterface
              530  LOAD_FAST                'interface'
              532  CALL_METHOD_1         1  ''
              534  STORE_FAST               'result'

 L. 127       536  LOAD_GLOBAL              logger
              538  LOAD_METHOD              debug
              540  LOAD_STR                 'Final result is %s'
              542  LOAD_FAST                'result'
              544  CALL_METHOD_2         2  ''
              546  POP_TOP          

 L. 128       548  LOAD_FAST                'result'
              550  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_FOUR' instruction at offset 288


wrap = GetBestInterface
ctypes.POINTER(comtypes.automation.IDispatch).__ctypes_from_outparam__ = wrap_outparam

class Constants(object):
    __doc__ = 'This class loads the type library from the supplied object,\n    then exposes constants in the type library as attributes.'

    def __init__(self, obj):
        obj = obj.QueryInterface(comtypes.automation.IDispatch)
        tlib, index = obj.GetTypeInfo(0).GetContainingTypeLib
        self.tcomp = tlib.GetTypeComp

    def __getattr__(self, name):
        try:
            kind, desc = self.tcomp.Bind(name)
        except (WindowsError, comtypes.COMError):
            raise AttributeError(name)
        else:
            if kind != 'variable':
                raise AttributeError(name)
            return desc._.lpvarValue[0].value

    def _bind_type(self, name):
        return self.tcomp.BindType(name)


def GetActiveObject(progid, interface=None, dynamic=False):
    """Return a pointer to a running COM object that has been
    registered with COM.

    'progid' may be a string like "Excel.Application",
       a string specifying a clsid, a GUID instance, or an object with
       a _clsid_ attribute which should be any of the above.
    'interface' allows to force a certain interface.
    'dynamic=True' will return a dynamic dispatch object.
    """
    clsid = comtypes.GUID.from_progid(progid)
    if dynamic:
        if interface is not None:
            raise ValueError('interface and dynamic are mutually exclusive')
        interface = comtypes.automation.IDispatch
    else:
        if interface is None:
            interface = getattr(progid, '_com_interfaces_', [None])[0]
    obj = comtypes.GetActiveObject(clsid, interface=interface)
    if dynamic:
        return comtypes.client.dynamic.Dispatch(obj)
    return _manage(obj, clsid, interface=interface)


def _manage(obj, clsid, interface):
    obj.__dict__['__clsid'] = str(clsid)
    if interface is None:
        obj = GetBestInterface(obj)
    return obj


def GetClassObject(progid, clsctx=None, pServerInfo=None, interface=None):
    """Create and return the class factory for a COM object.

    'clsctx' specifies how to create the object, use the CLSCTX_... constants.
    'pServerInfo', if used, must be a pointer to a comtypes.COSERVERINFO instance
    'interface' may be used to request an interface other than IClassFactory
    """
    clsid = comtypes.GUID.from_progid(progid)
    return comtypes.CoGetClassObject(clsid, clsctx, pServerInfo, interface)


def CreateObject(progid, clsctx=None, machine=None, interface=None, dynamic=False, pServerInfo=None):
    """Create a COM object from 'progid', and try to QueryInterface()
    it to the most useful interface, generating typelib support on
    demand.  A pointer to this interface is returned.

    'progid' may be a string like "InternetExplorer.Application",
       a string specifying a clsid, a GUID instance, or an object with
       a _clsid_ attribute which should be any of the above.
    'clsctx' specifies how to create the object, use the CLSCTX_... constants.
    'machine' allows to specify a remote machine to create the object on.
    'interface' allows to force a certain interface
    'dynamic=True' will return a dynamic dispatch object
    'pServerInfo', if used, must be a pointer to a comtypes.COSERVERINFO instance
        This supercedes 'machine'.

    You can also later request to receive events with GetEvents().
    """
    clsid = comtypes.GUID.from_progid(progid)
    logger.debug('%s -> %s', progid, clsid)
    if dynamic:
        if interface:
            raise ValueError('interface and dynamic are mutually exclusive')
        interface = comtypes.automation.IDispatch
    else:
        if interface is None:
            interface = getattr(progid, '_com_interfaces_', [None])[0]
        elif machine is None and pServerInfo is None:
            logger.debug('CoCreateInstance(%s, clsctx=%s, interface=%s)', clsid, clsctx, interface)
            obj = comtypes.CoCreateInstance(clsid, clsctx=clsctx, interface=interface)
        else:
            logger.debug('CoCreateInstanceEx(%s, clsctx=%s, interface=%s, machine=%s,                        pServerInfo=%s)', clsid, clsctx, interface, machine, pServerInfo)
            if machine is not None:
                if pServerInfo is not None:
                    msg = 'You can notset both the machine name and server info.'
                    raise ValueError(msg)
            obj = comtypes.CoCreateInstanceEx(clsid, clsctx=clsctx, interface=interface,
              machine=machine,
              pServerInfo=pServerInfo)
        if dynamic:
            return comtypes.client.dynamic.Dispatch(obj)
        return _manage(obj, clsid, interface=interface)


def CoGetObject(displayname, interface=None, dynamic=False):
    """Create an object by calling CoGetObject(displayname).

    Additional parameters have the same meaning as in CreateObject().
    """
    if dynamic:
        if interface is not None:
            raise ValueError('interface and dynamic are mutually exclusive')
        interface = comtypes.automation.IDispatch
    punk = comtypes.CoGetObject(displayname, interface)
    if dynamic:
        return comtypes.client.dynamic.Dispatch(punk)
    return _manage(punk, clsid=None,
      interface=interface)