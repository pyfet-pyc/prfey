# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\comtypes\client\lazybind.py
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

    def __getitem__(self, arg):
        if self.get is None:
            raise TypeError('unsubscriptable object')
        if isinstance(arg, tuple):
            return (self.disp._comobj._invoke)(self.get.memid, self.get.invkind, 0, *arg)
        if arg == _all_slice:
            return self.disp._comobj._invoke(self.get.memid, self.get.invkind, 0)
        return (self.disp._comobj._invoke)(self.get.memid, self.get.invkind, 0, *[
         arg])

    def __call__(self, *args):
        if self.get is None:
            raise TypeError('object is not callable')
        return (self.disp._comobj._invoke)(self.get.memid, self.get.invkind, 0, *args)

    def __setitem__(self, name, value):
        if self.put is None:
            if self.putref is None:
                raise TypeError('object does not support item assignment')
        else:
            if comtypes._is_object(value):
                descr = self.putref or self.put
            else:
                descr = self.put or self.putref
            if isinstance(name, tuple):
                (self.disp._comobj._invoke)(descr.memid, descr.invkind, 0, *name + (value,))
            else:
                if name == _all_slice:
                    self.disp._comobj._invoke(descr.memid, descr.invkind, 0, value)
                else:
                    self.disp._comobj._invoke(descr.memid, descr.invkind, 0, name, value)

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
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE   128  'to 128'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 125        32  SETUP_FINALLY        56  'to 56'

 L. 126        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _tcomp
               38  LOAD_METHOD              Bind
               40  LOAD_FAST                'name'
               42  LOAD_FAST                'invkind'
               44  CALL_METHOD_2         2  ''
               46  LOAD_CONST               1
               48  BINARY_SUBSCR    
               50  STORE_FAST               'descr'
               52  POP_BLOCK        
               54  JUMP_FORWARD         82  'to 82'
             56_0  COME_FROM_FINALLY    32  '32'

 L. 127        56  DUP_TOP          
               58  LOAD_GLOBAL              comtypes
               60  LOAD_ATTR                COMError
               62  COMPARE_OP               exception-match
               64  POP_JUMP_IF_FALSE    80  'to 80'
               66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          

 L. 128        72  LOAD_CONST               None
               74  STORE_FAST               'info'
               76  POP_EXCEPT       
               78  JUMP_FORWARD        106  'to 106'
             80_0  COME_FROM            64  '64'
               80  END_FINALLY      
             82_0  COME_FROM            54  '54'

 L. 133        82  LOAD_GLOBAL              FuncDesc
               84  LOAD_FAST                'descr'
               86  LOAD_ATTR                memid

 L. 134        88  LOAD_FAST                'descr'
               90  LOAD_ATTR                invkind

 L. 135        92  LOAD_FAST                'descr'
               94  LOAD_ATTR                cParams

 L. 136        96  LOAD_FAST                'descr'
               98  LOAD_ATTR                funckind

 L. 133       100  LOAD_CONST               ('memid', 'invkind', 'cParams', 'funckind')
              102  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              104  STORE_FAST               'info'
            106_0  COME_FROM            78  '78'

 L. 137       106  LOAD_FAST                'info'
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                _tdesc
              112  LOAD_FAST                'name'
              114  LOAD_FAST                'invkind'
              116  BUILD_TUPLE_2         2 
              118  STORE_SUBSCR     

 L. 138       120  LOAD_FAST                'info'
              122  ROT_FOUR         
              124  POP_EXCEPT       
              126  RETURN_VALUE     
            128_0  COME_FROM            24  '24'
              128  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 28

    def QueryInterface(self, *args):
        """QueryInterface is forwarded to the real com object."""
        return (self._comobj.QueryInterface)(*args)

    def __cmp__(self, other):
        if not isinstance(other, Dispatch):
            return 1
        return cmp(self._comobj, other._comobj)

    def __eq__(self, other):
        return isinstance(other, Dispatch) and self._comobj == other._comobj

    def __hash__(self):
        return hash(self._comobj)

    def __getattr__(self, name):
        """Get a COM attribute."""
        if name.startswith('__'):
            if name.endswith('__'):
                raise AttributeError(name)
        else:
            descr = self._Dispatch__bindname(DISPATCH_METHOD | DISPATCH_PROPERTYGET)
            if descr is None:
                raise AttributeError(name)
            elif descr.invkind == DISPATCH_PROPERTYGET:
                if descr.funckind == FUNC_DISPATCH:
                    if descr.cParams == 0:
                        return self._comobj._invoke(descr.memid, descr.invkind, 0)
            elif descr.funckind == FUNC_PUREVIRTUAL:
                if descr.cParams == 1:
                    return self._comobj._invoke(descr.memid, descr.invkind, 0)
            else:
                raise RuntimeError('funckind %d not yet implemented' % descr.funckind)
            put = self._Dispatch__bindnameDISPATCH_PROPERTYPUT
            putref = self._Dispatch__bindnameDISPATCH_PROPERTYPUTREF
            return NamedProperty(self, descr, put, putref)

        def caller(*args):
            return (self._comobj._invoke)(descr.memid, descr.invkind, 0, *args)

        try:
            caller.__name__ = name
        except TypeError:
            pass
        else:
            return caller

    def __setattr__(self, name, value):
        put = self._Dispatch__bindnameDISPATCH_PROPERTYPUT
        putref = self._Dispatch__bindnameDISPATCH_PROPERTYPUTREF
        if not put:
            if not putref:
                raise AttributeError(name)
        elif comtypes._is_object(value):
            descr = putref or put
        else:
            descr = put or putref
        if descr.cParams == 1:
            self._comobj._invoke(descr.memid, descr.invkind, 0, value)
            return None
        raise AttributeError(name)

    def __call__(self, *args):
        return (self._comobj._invoke)(DISPID_VALUE, DISPATCH_METHOD | DISPATCH_PROPERTYGET, 0, *args)

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

 L. 236        36  SETUP_FINALLY        66  'to 66'

 L. 237        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _comobj
               42  LOAD_ATTR                _invoke
               44  LOAD_GLOBAL              DISPID_VALUE

 L. 238        46  LOAD_GLOBAL              DISPATCH_METHOD
               48  LOAD_GLOBAL              DISPATCH_PROPERTYGET
               50  BINARY_OR        

 L. 239        52  LOAD_CONST               0

 L. 237        54  BUILD_TUPLE_3         3 

 L. 240        56  LOAD_FAST                'args'

 L. 237        58  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
               60  CALL_FUNCTION_EX      0  'positional arguments only'
               62  POP_BLOCK        
               64  RETURN_VALUE     
             66_0  COME_FROM_FINALLY    36  '36'

 L. 241        66  DUP_TOP          
               68  LOAD_GLOBAL              comtypes
               70  LOAD_ATTR                COMError
               72  COMPARE_OP               exception-match
               74  POP_JUMP_IF_FALSE    98  'to 98'
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
             98_0  COME_FROM            74  '74'
               98  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 78

    def __setitem__(self, name, value):
        if comtypes._is_object(value):
            invkind = DISPATCH_PROPERTYPUTREF
        else:
            invkind = DISPATCH_PROPERTYPUT
        if isinstance(name, tuple):
            args = name + (value,)
        else:
            if name == _all_slice:
                args = (
                 value,)
            else:
                args = (
                 name, value)
        return (self._comobj._invoke)(DISPID_VALUE, invkind, 0, *args)

    def __iter__(self):
        punk = self._comobj._invoke(DISPID_NEWENUM, DISPATCH_METHOD | DISPATCH_PROPERTYGET, 0)
        enum = punk.QueryInterface(IEnumVARIANT)
        enum._dynamic = True
        return enum