# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: comtypes\__init__.py
import types, sys, os
__version__ = '1.1.8'
import logging

class NullHandler(logging.Handler):
    __doc__ = 'A Handler that does nothing.'

    def emit(self, record):
        pass


logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())
from ctypes import *
from _ctypes import COMError
from comtypes import patcher

def _check_version(actual, tlib_cached_mtime=None):
    import comtypes.tools.codegenerator as required
    if actual != required:
        raise ImportError('Wrong version')
    g = hasattr(sys, 'frozen') or sys._getframe(1).f_globals
    tlb_path = g.get('typelib_path')
    try:
        tlib_curr_mtime = os.stat(tlb_path).st_mtime
    except (OSError, TypeError):
        return
    else:
        if not tlib_cached_mtime or abs(tlib_curr_mtime - tlib_cached_mtime) >= 1:
            raise ImportError('Typelib different than module')


try:
    COMError()
except TypeError:
    pass
else:

    def monkeypatch_COMError():

        def __init__(self, hresult, text, details):
            self.hresult = hresult
            self.text = text
            self.details = details
            super(COMError, self).__init__(hresult, text, details)

        COMError.__init__ = __init__


    monkeypatch_COMError()
    del monkeypatch_COMError
if sys.version_info >= (3, 0):
    pythonapi.PyInstanceMethod_New.argtypes = [
     py_object]
    pythonapi.PyInstanceMethod_New.restype = py_object
    PyInstanceMethod_Type = type(pythonapi.PyInstanceMethod_New(id))

    def instancemethod(func, inst, cls):
        mth = PyInstanceMethod_Type(func)
        if inst is None:
            return mth
        return mth.__get__(inst)


else:

    def instancemethod(func, inst, cls):
        return types.MethodType(func, inst, cls)


class ReturnHRESULT(Exception):
    __doc__ = 'ReturnHRESULT(hresult, text)\n\n    Return a hresult code from a COM method implementation\n    without logging an error.\n    '


import comtypes.GUID as GUID
_GUID = GUID
IID = GUID
DWORD = c_ulong
wireHWND = c_ulong
CLSCTX_INPROC_SERVER = 1
CLSCTX_INPROC_HANDLER = 2
CLSCTX_LOCAL_SERVER = 4
CLSCTX_INPROC = 3
CLSCTX_SERVER = 5
CLSCTX_ALL = 7
CLSCTX_INPROC_SERVER16 = 8
CLSCTX_REMOTE_SERVER = 16
CLSCTX_INPROC_HANDLER16 = 32
CLSCTX_RESERVED1 = 64
CLSCTX_RESERVED2 = 128
CLSCTX_RESERVED3 = 256
CLSCTX_RESERVED4 = 512
CLSCTX_NO_CODE_DOWNLOAD = 1024
CLSCTX_RESERVED5 = 2048
CLSCTX_NO_CUSTOM_MARSHAL = 4096
CLSCTX_ENABLE_CODE_DOWNLOAD = 8192
CLSCTX_NO_FAILURE_LOG = 16384
CLSCTX_DISABLE_AAA = 32768
CLSCTX_ENABLE_AAA = 65536
CLSCTX_FROM_DEFAULT_CONTEXT = 131072
tagCLSCTX = c_int
CLSCTX = tagCLSCTX
SEC_WINNT_AUTH_IDENTITY_UNICODE = 2
RPC_C_AUTHN_WINNT = 10
RPC_C_AUTHZ_NONE = 0
RPC_C_AUTHN_LEVEL_CONNECT = 2
RPC_C_IMP_LEVEL_IMPERSONATE = 3
EOAC_NONE = 0
_ole32 = oledll.ole32
_ole32_nohresult = windll.ole32
COINIT_MULTITHREADED = 0
COINIT_APARTMENTTHREADED = 2
COINIT_DISABLE_OLE1DDE = 4
COINIT_SPEED_OVER_MEMORY = 8

def CoInitialize():
    return CoInitializeEx(COINIT_APARTMENTTHREADED)


def CoInitializeEx(flags=None):
    if flags is None:
        flags = getattr(sys, 'coinit_flags', COINIT_APARTMENTTHREADED)
    logger.debug('CoInitializeEx(None, %s)', flags)
    _ole32.CoInitializeEx(None, flags)


CoInitializeEx()

def CoUninitialize():
    logger.debug('CoUninitialize()')
    _ole32_nohresult.CoUninitialize()


def _shutdown(func=_ole32_nohresult.CoUninitialize, _debug=logger.debug, _exc_clear=getattr(sys, 'exc_clear', lambda : None)):
    _exc_clear()
    _debug('Calling CoUnititialize()')
    func()
    if _cominterface_meta is not None:
        _cominterface_meta._com_shutting_down = True
    _debug('CoUnititialize() done.')


import atexit
atexit.register(_shutdown)
com_interface_registry = {}
com_coclass_registry = {}

def _is_object(obj):
    """This function determines if the argument is a COM object.  It
    is used in several places to determine whether propputref or
    propput setters have to be used."""
    from comtypes.automation import VARIANT
    if isinstance(obj, POINTER(IUnknown)):
        return True
    if isinstance(obj, VARIANT):
        if isinstance(obj.value, POINTER(IUnknown)):
            return True
    return hasattr(obj, '_comobj')


class _cominterface_meta(type):
    __doc__ = 'Metaclass for COM interfaces.  Automatically creates high level\n    methods from COMMETHOD lists.\n    '
    _com_shutting_down = False

    def __new__(self, name, bases, namespace):
        methods = namespace.pop('_methods_', None)
        dispmethods = namespace.pop('_disp_methods_', None)
        cls = type.__new__(self, name, bases, namespace)
        if methods is not None:
            cls._methods_ = methods
        else:
            if dispmethods is not None:
                cls._disp_methods_ = dispmethods
            if bases == (object,):
                _ptr_bases = (
                 cls, _compointer_base)
            else:
                _ptr_bases = (
                 cls, POINTER(bases[0]))
        p = type(_compointer_base)('POINTER(%s)' % cls.__name__, _ptr_bases, {'__com_interface__':cls, 
         '_needs_com_addref_':None})
        from ctypes import _pointer_type_cache
        _pointer_type_cache[cls] = p
        if cls._case_insensitive_:

            @patcher.Patch(p)
            class CaseInsensitive(object):

                def __getattr__(self, name):
                    """Implement case insensitive access to methods and properties"""
                    try:
                        fixed_name = self.__map_case__[name.lower()]
                    except KeyError:
                        raise AttributeError(name)
                    else:
                        if fixed_name != name:
                            return getattr(self, fixed_name)
                        raise AttributeError(name)

                def __setattr__(self, name, value):
                    """Implement case insensitive access to methods and properties"""
                    object.__setattr__(self, self.__map_case__.get(name.lower(), name), value)

        @patcher.Patch(POINTER(p))
        class ReferenceFix(object):

            def __setitem__(self, index, value):
                if index != 0:
                    if bool(value):
                        value.AddRef()
                    super(POINTER(p), self).__setitem__(index, value)
                    return None
                from _ctypes import CopyComPointer
                CopyComPointer(value, self)

        return cls

    def __setattr__(self, name, value):
        if name == '_methods_':
            self._make_methods(value)
            self._make_specials()
        else:
            if name == '_disp_methods_':
                assert self.__dict__.get('_disp_methods_', None) is None
                self._make_dispmethods(value)
                self._make_specials()
        type.__setattr__(self, name, value)

    def _make_specials(self):

        def has_name(name):
            if self._case_insensitive_:
                return name.lower() in self.__map_case__
            return hasattr(self, name)

        if has_name('Count'):

            @patcher.Patch(self)
            class _(object):

                def __len__(self):
                    """Return the the 'self.Count' property."""
                    return self.Count

        if has_name('Item'):

            @patcher.Patch(self)
            class _(object):

                def __call__(self, *args, **kw):
                    """Return 'self.Item(*args, **kw)'"""
                    return (self.Item)(*args, **kw)

                @patcher.no_replace
                def __getitem__(self, index):
                    """Return 'self.Item(index)'"""
                    if isinstance(index, tuple):
                        args = index
                    else:
                        if index == _all_slice:
                            args = ()
                        else:
                            args = (
                             index,)
                    try:
                        result = (self.Item)(*args)
                    except COMError as err:
                        try:
                            hresult, text, details = err.args
                            if hresult == -2147352565:
                                raise IndexError('invalid index')
                            else:
                                raise
                        finally:
                            err = None
                            del err

                    else:
                        return result

                @patcher.no_replace
                def __setitem__(self, index, value):
                    """Attempt 'self.Item[index] = value'"""
                    try:
                        self.Item[index] = value
                    except COMError as err:
                        try:
                            hresult, text, details = err.args
                            if hresult == -2147352565:
                                raise IndexError('invalid index')
                            else:
                                raise
                        finally:
                            err = None
                            del err

                    except TypeError:
                        msg = '%r object does not support item assignment'
                        raise TypeError(msg % type(self))

        if has_name('_NewEnum'):

            @patcher.Patch(self)
            class _(object):

                def __iter__(self):
                    """Return an iterator over the _NewEnum collection."""
                    enum = self._NewEnum
                    if isinstance(enum, types.MethodType):
                        enum = enum()
                    if hasattr(enum, 'Next'):
                        return enum
                    from comtypes.automation import IEnumVARIANT
                    return enum.QueryInterface(IEnumVARIANT)

    def _make_case_insensitive(self):
        try:
            self.__dict__['__map_case__']
        except KeyError:
            d = {}
            d.update(getattr(self, '__map_case__', {}))
            self.__map_case__ = d

    def _make_dispmethods(self, methods):
        if self._case_insensitive_:
            self._make_case_insensitive()
        properties = {}
        for m in methods:
            what, name, idlflags, restype, argspec = m
            is_prop = False
            try:
                memid = [x for x in idlflags if isinstance(x, int)][0]
            except IndexError:
                raise TypeError('no dispid found in idlflags')

        if what == 'DISPPROPERTY':
            assert not argspec
            accessor = self._disp_property(memid, idlflags)
            is_prop = True
            setattr(self, name, accessor)
        else:
            if what == 'DISPMETHOD':
                method = self._disp_method(memid, name, idlflags, restype, argspec)
                if 'propget' in idlflags:
                    nargs = len(argspec)
                    properties.setdefault((name, nargs), [None, None, None])[0] = method
                    is_prop = True
                else:
                    if 'propput' in idlflags:
                        nargs = len(argspec) - 1
                        properties.setdefault((name, nargs), [None, None, None])[1] = method
                        is_prop = True
                    else:
                        if 'propputref' in idlflags:
                            nargs = len(argspec) - 1
                            properties.setdefault((name, nargs), [None, None, None])[2] = method
                            is_prop = True
                        else:
                            setattr(self, name, method)
            if self._case_insensitive_:
                self.__map_case__[name.lower()] = name
                if is_prop:
                    self.__map_case__[name[5:].lower()] = name[5:]
            for (name, nargs), methods in list(properties.items()):
                if methods[1] is not None:
                    if methods[2] is not None:
                        propput = methods[1]
                        propputref = methods[2]

                        def put_or_putref(self, *args):
                            if _is_object(args[(-1)]):
                                return propputref(self, *args)
                            return propput(self, *args)

                        methods[1] = put_or_putref
                        del methods[2]
                    else:
                        if methods[2] is not None:
                            del methods[1]
                        else:
                            del methods[2]
                elif nargs:
                    setattr(self, name, named_property('%s.%s' % (self.__name__, name), *methods))
                else:
                    assert len(methods) <= 2
                    setattr(self, name, property(*methods))
                if self._case_insensitive_:
                    self.__map_case__[name.lower()] = name

    def _disp_method(self, memid, name, idlflags, restype, argspec):
        if 'propget' in idlflags:

            def getfunc(obj, *args, **kw):
                return (self.Invoke)(obj, memid, *args, _invkind=2, **kw)

            return getfunc
        elif 'propput' in idlflags:

            def putfunc(obj, *args, **kw):
                return (self.Invoke)(obj, memid, *args, _invkind=4, **kw)

            return putfunc
            if 'propputref' in idlflags:

                def putfunc(obj, *args, **kw):
                    return (self.Invoke)(obj, memid, *args, _invkind=8, **kw)

                return putfunc
            if hasattr(restype, '__com_interface__'):
                interface = restype.__com_interface__

                def func(s, *args, **kw):
                    result = (self.Invoke)(s, memid, *args, _invkind=1, **kw)
                    if result is None:
                        return
                    return result.QueryInterface(interface)

        else:

            def func(obj, *args, **kw):
                return (self.Invoke)(obj, memid, *args, _invkind=1, **kw)

        return func

    def _disp_property(self, memid, idlflags):

        def _get(obj):
            return obj.Invoke(memid, _invkind=2)

        if 'readonly' in idlflags:
            return property(_get)

        def _set(obj, value):
            invkind = 8 if _is_object(value) else 4
            return obj.Invoke(memid, value, _invkind=invkind)

        return property(_get, _set)

    def __get_baseinterface_methodcount(self):
        """Return the number of com methods in the base interfaces"""
        try:
            result = 0
            for itf in self.mro()[1:-1]:
                result += len(itf.__dict__['_methods_'])
            else:
                return result

            except KeyError as err:
            try:
                name, = err.args
                if name == '_methods_':
                    raise TypeError("baseinterface '%s' has no _methods_" % itf.__name__)
                raise
            finally:
                err = None
                del err

    def _fix_inout_args(self, func, argtypes, paramflags):
        SIMPLETYPE = type(c_int)
        BYREFTYPE = type(byref(c_int()))

        def call_with_inout(self_, *args, **kw):
            args = list(args)
            outargs = {}
            outnum = 0
            for i, info in enumerate(paramflags):
                direction = info[0]
                if direction & 3 == 3:
                    name = info[1]
                    atyp = argtypes[i]._type_
                    try:
                        try:
                            v = args[i]
                        except IndexError:
                            v = kw[name]

                    except KeyError:
                        v = atyp()
                    else:
                        if getattr(v, '_type_', None) is atyp:
                            pass
                        elif type(atyp) is SIMPLETYPE:
                            v = atyp(v)
                        else:
                            v = atyp.from_param(v)
                            if isinstance(v, BYREFTYPE):
                                raise AssertionError
                            else:
                                outargs[outnum] = v
                                outnum += 1
                                if len(args) > i:
                                    args[i] = v
                                else:
                                    kw[name] = v
                else:
                    if direction & 2 == 2:
                        outnum += 1
                    rescode = func(self_, *args, **kw)
                    if outnum == 1:
                        if len(outargs) == 1:
                            rescode = rescode.__ctypes_from_outparam__()
                        return rescode
                    rescode = list(rescode)
                    for outnum, o in list(outargs.items()):
                        rescode[outnum] = o.__ctypes_from_outparam__()
                    else:
                        return rescode

        return call_with_inout

    def _make_methods(self, methods):
        if self._case_insensitive_:
            self._make_case_insensitive()
        try:
            iid = self.__dict__['_iid_']
        except KeyError:
            raise AttributeError('this class must define an _iid_')
        else:
            iid = str(iid)
            com_interface_registry[iid] = self
            del iid
        vtbl_offset = self._cominterface_meta__get_baseinterface_methodcount()
        properties = {}
        for i, item in enumerate(methods):
            restype, name, argtypes, paramflags, idlflags, doc = item
            prototype = WINFUNCTYPE(restype, *argtypes)
            if restype == HRESULT:
                raw_func = prototype(i + vtbl_offset, name, None, self._iid_)
                func = prototype(i + vtbl_offset, name, paramflags, self._iid_)
            else:
                raw_func = prototype(i + vtbl_offset, name, None, None)
                func = prototype(i + vtbl_offset, name, paramflags, None)
            setattr(self, '_%s__com_%s' % (self.__name__, name), instancemethod(raw_func, None, self))
            if paramflags:
                dirflags = [p[0] & 3 for p in paramflags]
                if 3 in dirflags:
                    func = self._fix_inout_args(func, argtypes, paramflags)
            func.__doc__ = doc
            try:
                func.__name__ = name
            except TypeError:
                pass
            else:
                mth = instancemethod(func, None, self)
                is_prop = False

        if 'propget' in idlflags:
            assert name.startswith('_get_')
            nargs = len([flags for flags in paramflags if flags[0] & 7 in (0, 1)])
            propname = name[len('_get_'):]
            properties.setdefault((propname, doc, nargs), [None, None, None])[0] = func
            is_prop = True
        else:
            if 'propput' in idlflags:
                assert name.startswith('_set_')
                nargs = len([flags for flags in paramflags if flags[0] & 7 in (0, 1)]) - 1
                propname = name[len('_set_'):]
                properties.setdefault((propname, doc, nargs), [None, None, None])[1] = func
                is_prop = True
            else:
                if 'propputref' in idlflags:
                    assert name.startswith('_setref_')
                    nargs = len([flags for flags in paramflags if flags[0] & 7 in (0,
                                                                                   1)]) - 1
                    propname = name[len('_setref_'):]
                    properties.setdefault((propname, doc, nargs), [None, None, None])[2] = func
                    is_prop = True
                elif (is_prop or hasattr)(self, name):
                    setattr(self, '_' + name, mth)
                else:
                    setattr(self, name, mth)
                if self._case_insensitive_:
                    self.__map_case__[name.lower()] = name
                    if is_prop:
                        self.__map_case__[name[5:].lower()] = name[5:]
                for (name, doc, nargs), methods in list(properties.items()):
                    if methods[1] is not None:
                        if methods[2] is not None:
                            propput = methods[1]
                            propputref = methods[2]

                            def put_or_putref(self, *args):
                                if _is_object(args[(-1)]):
                                    return propputref(self, *args)
                                return propput(self, *args)

                            methods[1] = put_or_putref
                            del methods[2]
                        else:
                            if methods[2] is not None:
                                del methods[1]
                            else:
                                del methods[2]
                    else:
                        if nargs == 0:
                            prop = property(*methods + [None, doc])
                        else:
                            prop = named_property('%s.%s' % (self.__name__, name), *methods + [doc])
                        if hasattr(self, name):
                            setattr(self, '_' + name, prop)
                        else:
                            setattr(self, name, prop)
                    if self._case_insensitive_:
                        self.__map_case__[name.lower()] = name


_all_slice = slice(None, None, None)

class bound_named_property(object):

    def __init__(self, name, getter, setter, im_inst):
        self.name = name
        self.im_inst = im_inst
        self.getter = getter
        self.setter = setter

    def __getitem__(self, index):
        if self.getter is None:
            raise TypeError('unsubscriptable object')
        if isinstance(index, tuple):
            return (self.getter)(self.im_inst, *index)
        if index == _all_slice:
            return self.getter(self.im_inst)
        return self.getter(self.im_inst, index)

    def __call__(self, *args):
        if self.getter is None:
            raise TypeError('object is not callable')
        return (self.getter)(self.im_inst, *args)

    def __setitem__(self, index, value):
        if self.setter is None:
            raise TypeError('object does not support item assignment')
        elif isinstance(index, tuple):
            (self.setter)(self.im_inst, *index + (value,))
        else:
            if index == _all_slice:
                self.setter(self.im_inst, value)
            else:
                self.setter(self.im_inst, index, value)

    def __repr__(self):
        return '<bound_named_property %r at %x>' % (self.name, id(self))

    def __iter__(self):
        """ Explicitly disallow iteration. """
        msg = '%r is not iterable' % self.name
        raise TypeError(msg)


class named_property(object):

    def __init__(self, name, fget=None, fset=None, doc=None):
        self.name = name
        self.getter = fget
        self.setter = fset
        self.__doc__ = doc

    def __get__(self, im_inst, im_class=None):
        if im_inst is None:
            return self
        return bound_named_property(self.name, self.getter, self.setter, im_inst)

    def __set__(self, obj):
        raise AttributeError('Unsettable attribute')

    def __repr__(self):
        return '<named_property %r at %x>' % (self.name, id(self))


class _compointer_meta(type(c_void_p), _cominterface_meta):
    __doc__ = 'metaclass for COM interface pointer classes'


class _compointer_base(c_void_p, metaclass=_compointer_meta):
    __doc__ = 'base class for COM interface pointer classes'

    def __del__(self, _debug=logger.debug):
        """Release the COM refcount we own."""
        if self:
            if not type(self)._com_shutting_down:
                _debug('Release %s', self)
                self.Release()

    def __cmp__(self, other):
        if not isinstance(other, _compointer_base):
            return 1
        return cmp(super(_compointer_base, self).value, super(_compointer_base, other).value)

    def __eq__(self, other):
        if not isinstance(other, _compointer_base):
            return False
        return super(_compointer_base, self).value == super(_compointer_base, other).value

    def __hash__(self):
        return hash(super(_compointer_base, self).value)

    def __get_value(self):
        return self

    value = property(_compointer_base__get_value, doc='Return self.')

    def __repr__(self):
        ptr = super(_compointer_base, self).value
        return '<%s ptr=0x%x at %x>' % (self.__class__.__name__, ptr or 0, id(self))

    def from_param--- This code section failed: ---

 L. 958         0  LOAD_FAST                'value'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 959         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 962        12  LOAD_FAST                'value'
               14  LOAD_CONST               0
               16  COMPARE_OP               ==
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L. 963        20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L. 964        24  LOAD_GLOBAL              isinstance
               26  LOAD_FAST                'value'
               28  LOAD_FAST                'klass'
               30  CALL_FUNCTION_2       2  ''
               32  POP_JUMP_IF_FALSE    38  'to 38'

 L. 965        34  LOAD_FAST                'value'
               36  RETURN_VALUE     
             38_0  COME_FROM            32  '32'

 L. 968        38  LOAD_FAST                'klass'
               40  LOAD_ATTR                _iid_
               42  LOAD_GLOBAL              getattr
               44  LOAD_FAST                'value'
               46  LOAD_STR                 '_iid_'
               48  LOAD_CONST               None
               50  CALL_FUNCTION_3       3  ''
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    60  'to 60'

 L. 969        56  LOAD_FAST                'value'
               58  RETURN_VALUE     
             60_0  COME_FROM            54  '54'

 L. 971        60  SETUP_FINALLY        72  'to 72'

 L. 972        62  LOAD_FAST                'value'
               64  LOAD_ATTR                _com_pointers_
               66  STORE_FAST               'table'
               68  POP_BLOCK        
               70  JUMP_FORWARD         92  'to 92'
             72_0  COME_FROM_FINALLY    60  '60'

 L. 973        72  DUP_TOP          
               74  LOAD_GLOBAL              AttributeError
               76  COMPARE_OP               exception-match
               78  POP_JUMP_IF_FALSE    90  'to 90'
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          

 L. 974        86  POP_EXCEPT       
               88  JUMP_FORWARD        140  'to 140'
             90_0  COME_FROM            78  '78'
               90  END_FINALLY      
             92_0  COME_FROM            70  '70'

 L. 976        92  SETUP_FINALLY       106  'to 106'

 L. 978        94  LOAD_FAST                'table'
               96  LOAD_FAST                'klass'
               98  LOAD_ATTR                _iid_
              100  BINARY_SUBSCR    
              102  POP_BLOCK        
              104  RETURN_VALUE     
            106_0  COME_FROM_FINALLY    92  '92'

 L. 979       106  DUP_TOP          
              108  LOAD_GLOBAL              KeyError
              110  COMPARE_OP               exception-match
              112  POP_JUMP_IF_FALSE   138  'to 138'
              114  POP_TOP          
              116  POP_TOP          
              118  POP_TOP          

 L. 980       120  LOAD_GLOBAL              TypeError
              122  LOAD_STR                 'Interface %s not supported'
              124  LOAD_FAST                'klass'
              126  LOAD_ATTR                _iid_
              128  BINARY_MODULO    
              130  CALL_FUNCTION_1       1  ''
              132  RAISE_VARARGS_1       1  'exception instance'
              134  POP_EXCEPT       
              136  JUMP_FORWARD        140  'to 140'
            138_0  COME_FROM           112  '112'
              138  END_FINALLY      
            140_0  COME_FROM           136  '136'
            140_1  COME_FROM            88  '88'

 L. 981       140  LOAD_FAST                'value'
              142  LOAD_METHOD              QueryInterface
              144  LOAD_FAST                'klass'
              146  LOAD_ATTR                __com_interface__
              148  CALL_METHOD_1         1  ''
              150  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 116

    from_param = classmethod(from_param)


from ctypes import _SimpleCData

class BSTR(_SimpleCData):
    __doc__ = 'The windows BSTR data type'
    _type_ = 'X'
    _needsfree = False

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.value)

    def __ctypes_from_outparam__(self):
        self._needsfree = True
        return self.value

    def __del__(self, _free=windll.oleaut32.SysFreeString):
        if self._b_base_ is None or self._needsfree:
            _free(self)

    def from_param(cls, value):
        """Convert into a foreign function call parameter."""
        if isinstance(value, cls):
            return value
        return cls(value)

    from_param = classmethod(from_param)


class helpstring(str):
    __doc__ = 'Specifies the helpstring for a COM method or property.'


class defaultvalue(object):
    __doc__ = 'Specifies the default value for parameters marked optional.'

    def __init__(self, value):
        self.value = value


class dispid(int):
    __doc__ = 'Specifies the DISPID of a method or property.'


def STDMETHOD(restype, name, argtypes=()):
    """Specifies a COM method slot without idlflags"""
    return (
     restype, name, argtypes, None, (), None)


def DISPMETHOD(idlflags, restype, name, *argspec):
    """Specifies a method of a dispinterface"""
    return (
     'DISPMETHOD', name, idlflags, restype, argspec)


def DISPPROPERTY(idlflags, proptype, name):
    """Specifies a property of a dispinterface"""
    return (
     'DISPPROPERTY', name, idlflags, proptype, ())


_PARAMFLAGS = {'in':1, 
 'out':2, 
 'lcid':4, 
 'retval':8, 
 'optional':16}

def _encode_idl(names):
    return sum([_PARAMFLAGS.get(n, 0) for n in names])


_NOTHING = object()

def _unpack_argspec(idl, typ, name=None, defval=_NOTHING):
    return (idl, typ, name, defval)


def COMMETHOD(idlflags, restype, methodname, *argspec):
    """Specifies a COM method slot with idlflags.

    XXX should explain the sematics of the arguments.
    """
    paramflags = []
    argtypes = []
    helptext = [t for t in idlflags if isinstance(t, helpstring)]
    helptext = ''.join(helptext) or None
    from comtypes.automation import VARIANT
    for item in argspec:
        idl, typ, argname, defval = _unpack_argspec(*item)
        pflags = _encode_idl(idl)
        if 'optional' in idl:
            if defval is _NOTHING:
                if typ is VARIANT:
                    defval = VARIANT.missing
                else:
                    if typ is POINTER(VARIANT):
                        defval = pointer(VARIANT.missing)
                    else:
                        defval = typ()
        elif defval is _NOTHING:
            paramflags.append((pflags, argname))
        else:
            paramflags.append((pflags, argname, defval))
        argtypes.append(typ)
    else:
        if 'propget' in idlflags:
            methodname = '_get_%s' % methodname
        else:
            if 'propput' in idlflags:
                methodname = '_set_%s' % methodname
            else:
                if 'propputref' in idlflags:
                    methodname = '_setref_%s' % methodname
        return (
         restype, methodname, tuple(argtypes), tuple(paramflags), tuple(idlflags), helptext)


class IUnknown(object, metaclass=_cominterface_meta):
    __doc__ = 'The most basic COM interface.\n\n    Each subclasses of IUnknown must define these class attributes:\n\n    _iid_ - a GUID instance defining the identifier of this interface\n\n    _methods_ - a list of methods for this interface.\n\n    The _methods_ list must in VTable order.  Methods are specified\n    with STDMETHOD or COMMETHOD calls.\n    '
    _case_insensitive_ = False
    _iid_ = GUID('{00000000-0000-0000-C000-000000000046}')
    _methods_ = [
     STDMETHOD(HRESULT, 'QueryInterface', [
      POINTER(GUID), POINTER(c_void_p)]),
     STDMETHOD(c_ulong, 'AddRef'),
     STDMETHOD(c_ulong, 'Release')]

    def QueryInterface(self, interface, iid=None):
        """QueryInterface(interface) -> instance"""
        p = POINTER(interface)()
        if iid is None:
            iid = interface._iid_
        self._IUnknown__com_QueryInterface(byref(iid), byref(p))
        clsid = self.__dict__.get('__clsid')
        if clsid is not None:
            p.__dict__['__clsid'] = clsid
        return p

    def AddRef(self):
        """Increase the internal refcount by one and return it."""
        return self._IUnknown__com_AddRef()

    def Release(self):
        """Decrease the internal refcount by one and return it."""
        return self._IUnknown__com_Release()


class IPersist(IUnknown):
    _iid_ = GUID('{0000010C-0000-0000-C000-000000000046}')
    _idlflags_ = []
    _methods_ = [
     COMMETHOD([], HRESULT, 'GetClassID', (
      [
       'out'], POINTER(GUID), 'pClassID'))]


class IServiceProvider(IUnknown):
    _iid_ = GUID('{6D5140C1-7436-11CE-8034-00AA006009FA}')

    def QueryService(self, serviceIID, interface):
        p = POINTER(interface)()
        self._QueryService(byref(serviceIID), byref(interface._iid_), byref(p))
        return p

    _methods_ = [
     COMMETHOD([], HRESULT, 'QueryService', (
      [
       'in'], POINTER(GUID), 'guidService'), (
      [
       'in'], POINTER(GUID), 'riid'), (
      [
       'in'], POINTER(c_void_p), 'ppvObject'))]


def CoGetObject(displayname, interface):
    """Convert a displayname to a moniker, then bind and return the object
    identified by the moniker."""
    if interface is None:
        interface = IUnknown
    punk = POINTER(interface)()
    _ole32.CoGetObject(str(displayname), None, byref(interface._iid_), byref(punk))
    return punk


def CoCreateInstance(clsid, interface=None, clsctx=None, punkouter=None):
    """The basic windows api to create a COM class object and return a
    pointer to an interface.
    """
    if clsctx is None:
        clsctx = CLSCTX_SERVER
    if interface is None:
        interface = IUnknown
    p = POINTER(interface)()
    iid = interface._iid_
    _ole32.CoCreateInstance(byref(clsid), punkouter, clsctx, byref(iid), byref(p))
    return p


def CoGetClassObject(clsid, clsctx=None, pServerInfo=None, interface=None):
    if clsctx is None:
        clsctx = CLSCTX_SERVER
    if interface is None:
        import comtypes.server
        interface = comtypes.server.IClassFactory
    p = POINTER(interface)()
    _CoGetClassObject(clsid, clsctx, pServerInfo, interface._iid_, byref(p))
    return p


def GetActiveObject(clsid, interface=None):
    """Retrieves a pointer to a running object"""
    p = POINTER(IUnknown)()
    oledll.oleaut32.GetActiveObject(byref(clsid), None, byref(p))
    if interface is not None:
        p = p.QueryInterface(interface)
    return p


class MULTI_QI(Structure):
    _fields_ = [
     (
      'pIID', POINTER(GUID)),
     (
      'pItf', POINTER(c_void_p)),
     (
      'hr', HRESULT)]


class _COAUTHIDENTITY(Structure):
    _fields_ = [
     (
      'User', POINTER(c_ushort)),
     (
      'UserLength', c_ulong),
     (
      'Domain', POINTER(c_ushort)),
     (
      'DomainLength', c_ulong),
     (
      'Password', POINTER(c_ushort)),
     (
      'PasswordLength', c_ulong),
     (
      'Flags', c_ulong)]


COAUTHIDENTITY = _COAUTHIDENTITY

class _COAUTHINFO(Structure):
    _fields_ = [
     (
      'dwAuthnSvc', c_ulong),
     (
      'dwAuthzSvc', c_ulong),
     (
      'pwszServerPrincName', c_wchar_p),
     (
      'dwAuthnLevel', c_ulong),
     (
      'dwImpersonationLevel', c_ulong),
     (
      'pAuthIdentityData', POINTER(_COAUTHIDENTITY)),
     (
      'dwCapabilities', c_ulong)]


COAUTHINFO = _COAUTHINFO

class _COSERVERINFO(Structure):
    _fields_ = [
     (
      'dwReserved1', c_ulong),
     (
      'pwszName', c_wchar_p),
     (
      'pAuthInfo', POINTER(_COAUTHINFO)),
     (
      'dwReserved2', c_ulong)]


COSERVERINFO = _COSERVERINFO
_CoGetClassObject = _ole32.CoGetClassObject
_CoGetClassObject.argtypes = [POINTER(GUID), DWORD, POINTER(COSERVERINFO),
 POINTER(GUID), POINTER(c_void_p)]

class tagBIND_OPTS(Structure):
    _fields_ = [
     (
      'cbStruct', c_ulong),
     (
      'grfFlags', c_ulong),
     (
      'grfMode', c_ulong),
     (
      'dwTickCountDeadline', c_ulong)]


BIND_OPTS = tagBIND_OPTS

class tagBIND_OPTS2(Structure):
    _fields_ = [
     (
      'cbStruct', c_ulong),
     (
      'grfFlags', c_ulong),
     (
      'grfMode', c_ulong),
     (
      'dwTickCountDeadline', c_ulong),
     (
      'dwTrackFlags', c_ulong),
     (
      'dwClassContext', c_ulong),
     (
      'locale', c_ulong),
     (
      'pServerInfo', POINTER(_COSERVERINFO))]


BINDOPTS2 = tagBIND_OPTS2

class _SEC_WINNT_AUTH_IDENTITY(Structure):
    _fields_ = [
     (
      'User', POINTER(c_ushort)),
     (
      'UserLength', c_ulong),
     (
      'Domain', POINTER(c_ushort)),
     (
      'DomainLength', c_ulong),
     (
      'Password', POINTER(c_ushort)),
     (
      'PasswordLength', c_ulong),
     (
      'Flags', c_ulong)]


SEC_WINNT_AUTH_IDENTITY = _SEC_WINNT_AUTH_IDENTITY

class _SOLE_AUTHENTICATION_INFO(Structure):
    _fields_ = [
     (
      'dwAuthnSvc', c_ulong),
     (
      'dwAuthzSvc', c_ulong),
     (
      'pAuthInfo', POINTER(_SEC_WINNT_AUTH_IDENTITY))]


SOLE_AUTHENTICATION_INFO = _SOLE_AUTHENTICATION_INFO

class _SOLE_AUTHENTICATION_LIST(Structure):
    _fields_ = [
     (
      'cAuthInfo', c_ulong),
     (
      'pAuthInfo', POINTER(_SOLE_AUTHENTICATION_INFO))]


SOLE_AUTHENTICATION_LIST = _SOLE_AUTHENTICATION_LIST

def CoCreateInstanceEx(clsid, interface=None, clsctx=None, machine=None, pServerInfo=None):
    """The basic windows api to create a COM class object and return a
    pointer to an interface, possibly on another machine.

    Passing both "machine" and "pServerInfo" results in a ValueError.

    """
    if clsctx is None:
        clsctx = CLSCTX_LOCAL_SERVER | CLSCTX_REMOTE_SERVER
    elif pServerInfo is not None:
        if machine is not None:
            msg = 'Can not specify both machine name and server info'
            raise ValueError(msg)
    elif machine is not None:
        serverinfo = COSERVERINFO()
        serverinfo.pwszName = machine
        pServerInfo = byref(serverinfo)
    if interface is None:
        interface = IUnknown
    multiqi = MULTI_QI()
    multiqi.pIID = pointer(interface._iid_)
    _ole32.CoCreateInstanceEx(byref(clsid), None, clsctx, pServerInfo, 1, byref(multiqi))
    return cast(multiqi.pItf, POINTER(interface))


from comtypes._comobject import COMObject
from comtypes._meta import _coclass_meta

class CoClass(COMObject, metaclass=_coclass_meta):
    pass