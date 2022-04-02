# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: win32com\client\build.py
"""Contains knowledge to build a COM object definition.

This module is used by both the @dynamic@ and @makepy@ modules to build
all knowledge of a COM object.

This module contains classes which contain the actual knowledge of the object.
This include parameter and return type information, the COM dispid and CLSID, etc.

Other modules may use this information to generate .py files, use the information
dynamically, or possibly even generate .html documentation for objects.
"""
import sys, string
from keyword import iskeyword
import pythoncom
from pywintypes import TimeType
import winerror, datetime

def _makeDocString(s):
    if sys.version_info < (3, ):
        s = s.encode('mbcs')
    return repr(s)


error = 'PythonCOM.Client.Build error'

class NotSupportedException(Exception):
    pass


DropIndirection = 'DropIndirection'
NoTranslateTypes = [
 pythoncom.VT_BOOL, pythoncom.VT_CLSID, pythoncom.VT_CY,
 pythoncom.VT_DATE, pythoncom.VT_DECIMAL, pythoncom.VT_EMPTY,
 pythoncom.VT_ERROR, pythoncom.VT_FILETIME, pythoncom.VT_HRESULT,
 pythoncom.VT_I1, pythoncom.VT_I2, pythoncom.VT_I4,
 pythoncom.VT_I8, pythoncom.VT_INT, pythoncom.VT_NULL,
 pythoncom.VT_R4, pythoncom.VT_R8, pythoncom.VT_NULL,
 pythoncom.VT_STREAM,
 pythoncom.VT_UI1, pythoncom.VT_UI2, pythoncom.VT_UI4,
 pythoncom.VT_UI8, pythoncom.VT_UINT, pythoncom.VT_VOID]
NoTranslateMap = {}
for v in NoTranslateTypes:
    NoTranslateMap[v] = None
else:

    class MapEntry:
        __doc__ = 'Simple holder for named attibutes - items in a map.'

        def __init__(self, desc_or_id, names=None, doc=None, resultCLSID=pythoncom.IID_NULL, resultDoc=None, hidden=0):
            if type(desc_or_id) == type(0):
                self.dispid = desc_or_id
                self.desc = None
            else:
                self.dispid = desc_or_id[0]
                self.desc = desc_or_id
            self.names = names
            self.doc = doc
            self.resultCLSID = resultCLSID
            self.resultDocumentation = resultDoc
            self.wasProperty = 0
            self.hidden = hidden

        def GetResultCLSID(self):
            rc = self.resultCLSID
            if rc == pythoncom.IID_NULL:
                return
            return rc

        def GetResultCLSIDStr(self):
            rc = self.GetResultCLSID()
            if rc is None:
                return 'None'
            return repr(str(rc))

        def GetResultName(self):
            if self.resultDocumentation is None:
                return
            return self.resultDocumentation[0]


    class OleItem:
        typename = 'OleItem'

        def __init__(self, doc=None):
            self.doc = doc
            if self.doc:
                self.python_name = MakePublicAttributeName(self.doc[0])
            else:
                self.python_name = None
            self.bWritten = 0
            self.bIsDispatch = 0
            self.bIsSink = 0
            self.clsid = None
            self.co_class = None


    class DispatchItem(OleItem):
        typename = 'DispatchItem'

        def __init__(self, typeinfo=None, attr=None, doc=None, bForUser=1):
            OleItem.__init__(self, doc)
            self.propMap = {}
            self.propMapGet = {}
            self.propMapPut = {}
            self.mapFuncs = {}
            self.defaultDispatchName = None
            self.hidden = 0
            if typeinfo:
                self.Build(typeinfo, attr, bForUser)

        def _propMapPutCheck_(self, key, item):
            ins, outs, opts = self.CountInOutOptArgs(item.desc[2])
            if ins > 1:
                if opts + 1 == ins or ins == item.desc[6] + 1:
                    newKey = 'Set' + key
                    deleteExisting = 0
                else:
                    deleteExisting = 1
                    if key in self.mapFuncs or key in self.propMapGet:
                        newKey = 'Set' + key
                    else:
                        newKey = key
                item.wasProperty = 1
                self.mapFuncs[newKey] = item
                if deleteExisting:
                    del self.propMapPut[key]

        def _propMapGetCheck_(self, key, item):
            ins, outs, opts = self.CountInOutOptArgs(item.desc[2])
            if ins > 0:
                if item.desc[6] == ins or ins == opts:
                    newKey = 'Get' + key
                    deleteExisting = 0
                else:
                    deleteExisting = 1
                    if key in self.mapFuncs:
                        newKey = 'Get' + key
                    else:
                        newKey = key
                item.wasProperty = 1
                self.mapFuncs[newKey] = item
                if deleteExisting:
                    del self.propMapGet[key]

        def _AddFunc_(self, typeinfo, fdesc, bForUser):
            id = fdesc.memid
            funcflags = fdesc.wFuncFlags
            try:
                names = typeinfo.GetNames(id)
                name = names[0]
            except pythoncom.ole_error:
                name = ''
                names = None
            else:
                doc = None
                try:
                    if bForUser:
                        doc = typeinfo.GetDocumentation(id)
                except pythoncom.ole_error:
                    pass
                else:
                    if id == 0:
                        if name:
                            self.defaultDispatchName = name
                    invkind = fdesc.invkind
                    typerepr, flag, defval = fdesc.rettype
                    typerepr, resultCLSID, resultDoc = _ResolveType(typerepr, typeinfo)
                    fdesc.rettype = (
                     typerepr, flag, defval, resultCLSID)
                    argList = []
            for argDesc in fdesc.args:
                typerepr, flag, defval = argDesc
                arg_type, arg_clsid, arg_doc = _ResolveType(typerepr, typeinfo)
                argDesc = (arg_type, flag, defval, arg_clsid)
                argList.append(argDesc)
            else:
                fdesc.args = tuple(argList)
                hidden = funcflags & pythoncom.FUNCFLAG_FHIDDEN != 0
                if invkind == pythoncom.INVOKE_PROPERTYGET:
                    map = self.propMapGet
                elif invkind in (pythoncom.INVOKE_PROPERTYPUT, pythoncom.INVOKE_PROPERTYPUTREF):
                    existing = self.propMapPut.get(name, None)
                    if existing is not None:
                        if existing.desc[4] == pythoncom.INVOKE_PROPERTYPUT:
                            map = self.mapFuncs
                            name = 'Set' + name
                        else:
                            existing.wasProperty = 1
                            self.mapFuncs['Set' + name] = existing
                            map = self.propMapPut
                    else:
                        map = self.propMapPut
                elif invkind == pythoncom.INVOKE_FUNC:
                    map = self.mapFuncs
                else:
                    map = None
                if map is not None:
                    map[name] = MapEntry(tuple(fdesc), names, doc, resultCLSID, resultDoc, hidden)
                    if fdesc.funckind != pythoncom.FUNC_DISPATCH:
                        return
                    return (name, map)

        def _AddVar_(self, typeinfo, fdesc, bForUser):
            if fdesc.varkind == pythoncom.VAR_DISPATCH:
                id = fdesc.memid
                names = typeinfo.GetNames(id)
                typerepr, flags, defval = fdesc.elemdescVar
                typerepr, resultCLSID, resultDoc = _ResolveType(typerepr, typeinfo)
                fdesc.elemdescVar = (typerepr, flags, defval)
                doc = None
                try:
                    if bForUser:
                        doc = typeinfo.GetDocumentation(id)
                except pythoncom.ole_error:
                    pass
                else:
                    map = self.propMap
                    hidden = 0
                    if hasattr(fdesc, 'wVarFlags'):
                        hidden = fdesc.wVarFlags & 64 != 0
                    map[names[0]] = MapEntry(tuple(fdesc), names, doc, resultCLSID, resultDoc, hidden)
                    return (
                     names[0], map)
                return

        def Build(self, typeinfo, attr, bForUser=1):
            self.clsid = attr[0]
            self.bIsDispatch = attr.wTypeFlags & pythoncom.TYPEFLAG_FDISPATCHABLE != 0
            if typeinfo is None:
                return
            for j in range(attr[6]):
                fdesc = typeinfo.GetFuncDesc(j)
                self._AddFunc_(typeinfo, fdesc, bForUser)
            else:
                for j in range(attr[7]):
                    fdesc = typeinfo.GetVarDesc(j)
                    self._AddVar_(typeinfo, fdesc, bForUser)
                else:
                    for key, item in list(self.propMapGet.items()):
                        self._propMapGetCheck_(key, item)
                    else:
                        for key, item in list(self.propMapPut.items()):
                            self._propMapPutCheck_(key, item)

        def CountInOutOptArgs(self, argTuple):
            """Return tuple counting in/outs/OPTS.  Sum of result may not be len(argTuple), as some args may be in/out."""
            ins = out = opts = 0
            for argCheck in argTuple:
                inOut = argCheck[1]
                if inOut == 0:
                    ins = ins + 1
                    out = out + 1
                else:
                    if inOut & pythoncom.PARAMFLAG_FIN:
                        ins = ins + 1
                    elif inOut & pythoncom.PARAMFLAG_FOPT:
                        opts = opts + 1
                    if inOut & pythoncom.PARAMFLAG_FOUT:
                        out = out + 1
            else:
                return (
                 ins, out, opts)

        def MakeFuncMethod(self, entry, name, bMakeClass=1):
            if entry.desc is not None:
                if len(entry.desc) < 6 or (entry.desc[6] != -1):
                    return self.MakeDispatchFuncMethod(entry, name, bMakeClass)
                return self.MakeVarArgsFuncMethod(entry, name, bMakeClass)

        def MakeDispatchFuncMethod(self, entry, name, bMakeClass=1):
            fdesc = entry.desc
            doc = entry.doc
            names = entry.names
            ret = []
            if bMakeClass:
                linePrefix = '\t'
                defNamedOptArg = 'defaultNamedOptArg'
                defNamedNotOptArg = 'defaultNamedNotOptArg'
                defUnnamedArg = 'defaultUnnamedArg'
            else:
                linePrefix = ''
                defNamedOptArg = 'pythoncom.Missing'
                defNamedNotOptArg = 'pythoncom.Missing'
                defUnnamedArg = 'pythoncom.Missing'
            defOutArg = 'pythoncom.Missing'
            id = fdesc[0]
            s = linePrefix + 'def ' + name + '(self' + BuildCallList(fdesc, names, defNamedOptArg, defNamedNotOptArg, defUnnamedArg, defOutArg) + '):'
            ret.append(s)
            if doc:
                if doc[1]:
                    ret.append(linePrefix + '\t' + _makeDocString(doc[1]))
            resclsid = entry.GetResultCLSID()
            if resclsid:
                resclsid = "'%s'" % resclsid
            else:
                resclsid = 'None'
            retDesc = fdesc[8][:2]
            argsDesc = tuple([what[:2] for what in fdesc[2]])
            param_flags = [what[1] for what in fdesc[2]]
            bad_params = [flag for flag in param_flags if flag & (pythoncom.PARAMFLAG_FOUT | pythoncom.PARAMFLAG_FRETVAL) != 0]
            s = None
            if len(bad_params) == 0:
                if len(retDesc) == 2:
                    if retDesc[1] == 0:
                        rd = retDesc[0]
                        if rd in NoTranslateMap:
                            s = '%s\treturn self._oleobj_.InvokeTypes(%d, LCID, %s, %s, %s%s)' % (linePrefix, id, fdesc[4], retDesc, argsDesc, _BuildArgList(fdesc, names))
                        elif rd in (pythoncom.VT_DISPATCH, pythoncom.VT_UNKNOWN):
                            s = '%s\tret = self._oleobj_.InvokeTypes(%d, LCID, %s, %s, %s%s)\n' % (linePrefix, id, fdesc[4], retDesc, repr(argsDesc), _BuildArgList(fdesc, names))
                            s = s + '%s\tif ret is not None:\n' % (linePrefix,)
                            if rd == pythoncom.VT_UNKNOWN:
                                s = s + '%s\t\t# See if this IUnknown is really an IDispatch\n' % (linePrefix,)
                                s = s + '%s\t\ttry:\n' % (linePrefix,)
                                s = s + '%s\t\t\tret = ret.QueryInterface(pythoncom.IID_IDispatch)\n' % (linePrefix,)
                                s = s + '%s\t\texcept pythoncom.error:\n' % (linePrefix,)
                                s = s + '%s\t\t\treturn ret\n' % (linePrefix,)
                            s = s + '%s\t\tret = Dispatch(ret, %s, %s)\n' % (linePrefix, repr(name), resclsid)
                            s = s + '%s\treturn ret' % linePrefix
                        elif rd == pythoncom.VT_BSTR:
                            s = '%s\t# Result is a Unicode object\n' % (linePrefix,)
                            s = s + '%s\treturn self._oleobj_.InvokeTypes(%d, LCID, %s, %s, %s%s)' % (linePrefix, id, fdesc[4], retDesc, repr(argsDesc), _BuildArgList(fdesc, names))
            if s is None:
                s = '%s\treturn self._ApplyTypes_(%d, %s, %s, %s, %s, %s%s)' % (linePrefix, id, fdesc[4], retDesc, argsDesc, repr(name), resclsid, _BuildArgList(fdesc, names))
            ret.append(s)
            ret.append('')
            return ret

        def MakeVarArgsFuncMethod(self, entry, name, bMakeClass=1):
            fdesc = entry.desc
            names = entry.names
            doc = entry.doc
            ret = []
            argPrefix = 'self'
            if bMakeClass:
                linePrefix = '\t'
            else:
                linePrefix = ''
            ret.append(linePrefix + 'def ' + name + '(' + argPrefix + ', *args):')
            if doc:
                if doc[1]:
                    ret.append(linePrefix + '\t' + _makeDocString(doc[1]))
            if fdesc:
                invoketype = fdesc[4]
            else:
                invoketype = pythoncom.DISPATCH_METHOD
            s = linePrefix + '\treturn self._get_good_object_(self._oleobj_.Invoke(*(('
            ret.append(s + str(entry.dispid) + ",0,%d,1)+args)),'%s')" % (invoketype, names[0]))
            ret.append('')
            return ret


    class VTableItem(DispatchItem):

        def Build(self, typeinfo, attr, bForUser=1):
            DispatchItem.Build(self, typeinfo, attr, bForUser)
            assert typeinfo is not None, 'Cant build vtables without type info!'
            meth_list = list(self.mapFuncs.values()) + list(self.propMapGet.values()) + list(self.propMapPut.values())
            meth_list.sort(key=(lambda m: m.desc[7]))
            self.vtableFuncs = []
            for entry in meth_list:
                self.vtableFuncs.append((entry.names, entry.dispid, entry.desc))


    class LazyDispatchItem(DispatchItem):
        typename = 'LazyDispatchItem'

        def __init__(self, attr, doc):
            self.clsid = attr[0]
            DispatchItem.__init__(self, None, attr, doc, 0)


    typeSubstMap = {pythoncom.VT_INT: pythoncom.VT_I4, 
     pythoncom.VT_UINT: pythoncom.VT_UI4, 
     pythoncom.VT_HRESULT: pythoncom.VT_I4}

    def _ResolveType--- This code section failed: ---

 L. 423         0  LOAD_GLOBAL              type
                2  LOAD_FAST                'typerepr'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_GLOBAL              tuple
                8  COMPARE_OP               ==
            10_12  POP_JUMP_IF_FALSE   498  'to 498'

 L. 424        14  LOAD_FAST                'typerepr'
               16  UNPACK_SEQUENCE_2     2 
               18  STORE_FAST               'indir_vt'
               20  STORE_FAST               'subrepr'

 L. 425        22  LOAD_FAST                'indir_vt'
               24  LOAD_GLOBAL              pythoncom
               26  LOAD_ATTR                VT_PTR
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE   124  'to 124'

 L. 433        32  LOAD_GLOBAL              type
               34  LOAD_FAST                'subrepr'
               36  CALL_FUNCTION_1       1  ''
               38  LOAD_GLOBAL              tuple
               40  COMPARE_OP               ==
               42  JUMP_IF_FALSE_OR_POP    56  'to 56'
               44  LOAD_FAST                'subrepr'
               46  LOAD_CONST               0
               48  BINARY_SUBSCR    
               50  LOAD_GLOBAL              pythoncom
               52  LOAD_ATTR                VT_USERDEFINED
               54  COMPARE_OP               ==
             56_0  COME_FROM            42  '42'
               56  STORE_FAST               'was_user'

 L. 434        58  LOAD_GLOBAL              _ResolveType
               60  LOAD_FAST                'subrepr'
               62  LOAD_FAST                'itypeinfo'
               64  CALL_FUNCTION_2       2  ''
               66  UNPACK_SEQUENCE_3     3 
               68  STORE_FAST               'subrepr'
               70  STORE_FAST               'sub_clsid'
               72  STORE_FAST               'sub_doc'

 L. 435        74  LOAD_FAST                'was_user'
               76  POP_JUMP_IF_FALSE   108  'to 108'
               78  LOAD_FAST                'subrepr'
               80  LOAD_GLOBAL              pythoncom
               82  LOAD_ATTR                VT_DISPATCH
               84  LOAD_GLOBAL              pythoncom
               86  LOAD_ATTR                VT_UNKNOWN
               88  LOAD_GLOBAL              pythoncom
               90  LOAD_ATTR                VT_RECORD
               92  BUILD_TUPLE_3         3 
               94  COMPARE_OP               in
               96  POP_JUMP_IF_FALSE   108  'to 108'

 L. 437        98  LOAD_FAST                'subrepr'
              100  LOAD_FAST                'sub_clsid'
              102  LOAD_FAST                'sub_doc'
              104  BUILD_TUPLE_3         3 
              106  RETURN_VALUE     
            108_0  COME_FROM            96  '96'
            108_1  COME_FROM            76  '76'

 L. 439       108  LOAD_FAST                'subrepr'
              110  LOAD_GLOBAL              pythoncom
              112  LOAD_ATTR                VT_BYREF
              114  BINARY_OR        
              116  LOAD_FAST                'sub_clsid'
              118  LOAD_FAST                'sub_doc'
              120  BUILD_TUPLE_3         3 
              122  RETURN_VALUE     
            124_0  COME_FROM            30  '30'

 L. 440       124  LOAD_FAST                'indir_vt'
              126  LOAD_GLOBAL              pythoncom
              128  LOAD_ATTR                VT_SAFEARRAY
              130  COMPARE_OP               ==
              132  POP_JUMP_IF_FALSE   166  'to 166'

 L. 442       134  LOAD_GLOBAL              _ResolveType
              136  LOAD_FAST                'subrepr'
              138  LOAD_FAST                'itypeinfo'
              140  CALL_FUNCTION_2       2  ''
              142  UNPACK_SEQUENCE_3     3 
              144  STORE_FAST               'subrepr'
              146  STORE_FAST               'sub_clsid'
              148  STORE_FAST               'sub_doc'

 L. 443       150  LOAD_GLOBAL              pythoncom
              152  LOAD_ATTR                VT_ARRAY
              154  LOAD_FAST                'subrepr'
              156  BINARY_OR        
              158  LOAD_FAST                'sub_clsid'
              160  LOAD_FAST                'sub_doc'
              162  BUILD_TUPLE_3         3 
              164  RETURN_VALUE     
            166_0  COME_FROM           132  '132'

 L. 444       166  LOAD_FAST                'indir_vt'
              168  LOAD_GLOBAL              pythoncom
              170  LOAD_ATTR                VT_CARRAY
              172  COMPARE_OP               ==
              174  POP_JUMP_IF_FALSE   188  'to 188'

 L. 447       176  LOAD_GLOBAL              pythoncom
              178  LOAD_ATTR                VT_CARRAY
              180  LOAD_CONST               None
              182  LOAD_CONST               None
              184  BUILD_TUPLE_3         3 
              186  RETURN_VALUE     
            188_0  COME_FROM           174  '174'

 L. 448       188  LOAD_FAST                'indir_vt'
              190  LOAD_GLOBAL              pythoncom
              192  LOAD_ATTR                VT_USERDEFINED
              194  COMPARE_OP               ==
          196_198  POP_JUMP_IF_FALSE   498  'to 498'

 L. 449       200  SETUP_FINALLY       216  'to 216'

 L. 450       202  LOAD_FAST                'itypeinfo'
              204  LOAD_METHOD              GetRefTypeInfo
              206  LOAD_FAST                'subrepr'
              208  CALL_METHOD_1         1  ''
              210  STORE_FAST               'resultTypeInfo'
              212  POP_BLOCK        
              214  JUMP_FORWARD        296  'to 296'
            216_0  COME_FROM_FINALLY   200  '200'

 L. 451       216  DUP_TOP          
              218  LOAD_GLOBAL              pythoncom
              220  LOAD_ATTR                com_error
              222  COMPARE_OP               exception-match
          224_226  POP_JUMP_IF_FALSE   294  'to 294'
              228  POP_TOP          
              230  STORE_FAST               'details'
              232  POP_TOP          
              234  SETUP_FINALLY       282  'to 282'

 L. 452       236  LOAD_FAST                'details'
              238  LOAD_ATTR                hresult
              240  LOAD_GLOBAL              winerror
              242  LOAD_ATTR                TYPE_E_CANTLOADLIBRARY
              244  LOAD_GLOBAL              winerror
              246  LOAD_ATTR                TYPE_E_LIBNOTREGISTERED
              248  BUILD_TUPLE_2         2 
              250  COMPARE_OP               in
          252_254  POP_JUMP_IF_FALSE   276  'to 276'

 L. 454       256  LOAD_GLOBAL              pythoncom
              258  LOAD_ATTR                VT_UNKNOWN
              260  LOAD_CONST               None
              262  LOAD_CONST               None
              264  BUILD_TUPLE_3         3 
              266  ROT_FOUR         
              268  POP_BLOCK        
              270  POP_EXCEPT       
              272  CALL_FINALLY        282  'to 282'
              274  RETURN_VALUE     
            276_0  COME_FROM           252  '252'

 L. 455       276  RAISE_VARARGS_0       0  'reraise'
              278  POP_BLOCK        
              280  BEGIN_FINALLY    
            282_0  COME_FROM           272  '272'
            282_1  COME_FROM_FINALLY   234  '234'
              282  LOAD_CONST               None
              284  STORE_FAST               'details'
              286  DELETE_FAST              'details'
              288  END_FINALLY      
              290  POP_EXCEPT       
              292  JUMP_FORWARD        296  'to 296'
            294_0  COME_FROM           224  '224'
              294  END_FINALLY      
            296_0  COME_FROM           292  '292'
            296_1  COME_FROM           214  '214'

 L. 457       296  LOAD_FAST                'resultTypeInfo'
              298  LOAD_METHOD              GetTypeAttr
              300  CALL_METHOD_0         0  ''
              302  STORE_FAST               'resultAttr'

 L. 458       304  LOAD_FAST                'resultAttr'
              306  LOAD_ATTR                typekind
              308  STORE_FAST               'typeKind'

 L. 459       310  LOAD_FAST                'typeKind'
              312  LOAD_GLOBAL              pythoncom
              314  LOAD_ATTR                TKIND_ALIAS
              316  COMPARE_OP               ==
          318_320  POP_JUMP_IF_FALSE   338  'to 338'

 L. 460       322  LOAD_FAST                'resultAttr'
              324  LOAD_ATTR                tdescAlias
              326  STORE_FAST               'tdesc'

 L. 461       328  LOAD_GLOBAL              _ResolveType
              330  LOAD_FAST                'tdesc'
              332  LOAD_FAST                'resultTypeInfo'
              334  CALL_FUNCTION_2       2  ''
              336  RETURN_VALUE     
            338_0  COME_FROM           318  '318'

 L. 462       338  LOAD_FAST                'typeKind'
              340  LOAD_GLOBAL              pythoncom
              342  LOAD_ATTR                TKIND_ENUM
              344  LOAD_GLOBAL              pythoncom
              346  LOAD_ATTR                TKIND_MODULE
              348  BUILD_TUPLE_2         2 
              350  COMPARE_OP               in
          352_354  POP_JUMP_IF_FALSE   368  'to 368'

 L. 464       356  LOAD_GLOBAL              pythoncom
              358  LOAD_ATTR                VT_I4
              360  LOAD_CONST               None
              362  LOAD_CONST               None
              364  BUILD_TUPLE_3         3 
              366  RETURN_VALUE     
            368_0  COME_FROM           352  '352'

 L. 466       368  LOAD_FAST                'typeKind'
              370  LOAD_GLOBAL              pythoncom
              372  LOAD_ATTR                TKIND_DISPATCH
              374  COMPARE_OP               ==
          376_378  POP_JUMP_IF_FALSE   414  'to 414'

 L. 467       380  LOAD_FAST                'resultTypeInfo'
              382  LOAD_METHOD              GetTypeAttr
              384  CALL_METHOD_0         0  ''
              386  LOAD_CONST               0
              388  BINARY_SUBSCR    
              390  STORE_FAST               'clsid'

 L. 468       392  LOAD_FAST                'resultTypeInfo'
              394  LOAD_METHOD              GetDocumentation
              396  LOAD_CONST               -1
              398  CALL_METHOD_1         1  ''
              400  STORE_FAST               'retdoc'

 L. 469       402  LOAD_GLOBAL              pythoncom
              404  LOAD_ATTR                VT_DISPATCH
              406  LOAD_FAST                'clsid'
              408  LOAD_FAST                'retdoc'
              410  BUILD_TUPLE_3         3 
              412  RETURN_VALUE     
            414_0  COME_FROM           376  '376'

 L. 471       414  LOAD_FAST                'typeKind'
              416  LOAD_GLOBAL              pythoncom
              418  LOAD_ATTR                TKIND_INTERFACE

 L. 472       420  LOAD_GLOBAL              pythoncom
              422  LOAD_ATTR                TKIND_COCLASS

 L. 471       424  BUILD_TUPLE_2         2 
              426  COMPARE_OP               in
          428_430  POP_JUMP_IF_FALSE   466  'to 466'

 L. 474       432  LOAD_FAST                'resultTypeInfo'
              434  LOAD_METHOD              GetTypeAttr
              436  CALL_METHOD_0         0  ''
              438  LOAD_CONST               0
              440  BINARY_SUBSCR    
              442  STORE_FAST               'clsid'

 L. 475       444  LOAD_FAST                'resultTypeInfo'
              446  LOAD_METHOD              GetDocumentation
              448  LOAD_CONST               -1
              450  CALL_METHOD_1         1  ''
              452  STORE_FAST               'retdoc'

 L. 476       454  LOAD_GLOBAL              pythoncom
              456  LOAD_ATTR                VT_UNKNOWN
              458  LOAD_FAST                'clsid'
              460  LOAD_FAST                'retdoc'
              462  BUILD_TUPLE_3         3 
              464  RETURN_VALUE     
            466_0  COME_FROM           428  '428'

 L. 478       466  LOAD_FAST                'typeKind'
              468  LOAD_GLOBAL              pythoncom
              470  LOAD_ATTR                TKIND_RECORD
              472  COMPARE_OP               ==
          474_476  POP_JUMP_IF_FALSE   490  'to 490'

 L. 479       478  LOAD_GLOBAL              pythoncom
              480  LOAD_ATTR                VT_RECORD
              482  LOAD_CONST               None
              484  LOAD_CONST               None
              486  BUILD_TUPLE_3         3 
              488  RETURN_VALUE     
            490_0  COME_FROM           474  '474'

 L. 480       490  LOAD_GLOBAL              NotSupportedException
              492  LOAD_STR                 'Can not resolve alias or user-defined type'
              494  CALL_FUNCTION_1       1  ''
              496  RAISE_VARARGS_1       1  'exception instance'
            498_0  COME_FROM           196  '196'
            498_1  COME_FROM            10  '10'

 L. 481       498  LOAD_GLOBAL              typeSubstMap
              500  LOAD_METHOD              get
              502  LOAD_FAST                'typerepr'
              504  LOAD_FAST                'typerepr'
              506  CALL_METHOD_2         2  ''
              508  LOAD_CONST               None
              510  LOAD_CONST               None
              512  BUILD_TUPLE_3         3 
              514  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 268


    def _BuildArgList(fdesc, names):
        """Builds list of args to the underlying Invoke method."""
        numArgs = max(fdesc[6], len(fdesc[2]))
        names = list(names)
        while True:
            if None in names:
                i = names.index(None)
                names[i] = 'arg%d' % (i,)

        names = list(map(MakePublicAttributeName, names[1:numArgs + 1]))
        name_num = 0
        while True:
            if len(names) < numArgs:
                names.append('arg%d' % (len(names),))

        for i in range(0, len(names), 5):
            names[i] = names[i] + '\n\t\t\t'
        else:
            return ',' + ', '.join(names)


    valid_identifier_chars = string.ascii_letters + string.digits + '_'

    def demunge_leading_underscores(className):
        i = 0
        while True:
            if className[i] == '_':
                i += 1

        assert i >= 2, "Should only be here with names starting with '__'"
        return className[i - 1:] + className[:i - 1]


    def MakePublicAttributeName(className, is_global=False):
        if className[:2] == '__':
            return demunge_leading_underscores(className)
        if className == 'None':
            className = 'NONE'
        else:
            if iskeyword(className):
                ret = className.capitalize()
                if ret == className:
                    ret = ret.upper()
                return ret
            if is_global:
                if hasattr(__builtins__, className):
                    ret = className.capitalize()
                    if ret == className:
                        ret = ret.upper()
                    return ret
        return ''.join([char for char in className if char in valid_identifier_chars])


    def MakeDefaultArgRepr(defArgVal):
        try:
            inOut = defArgVal[1]
        except IndexError:
            inOut = pythoncom.PARAMFLAG_FIN
        else:
            if inOut & pythoncom.PARAMFLAG_FHASDEFAULT:
                val = defArgVal[2]
                if isinstance(val, datetime.datetime):
                    return repr(tuple(val.utctimetuple()))
                if type(val) is TimeType:
                    year = val.year
                    month = val.month
                    day = val.day
                    hour = val.hour
                    minute = val.minute
                    second = val.second
                    msec = val.msec
                    return 'pywintypes.Time((%(year)d, %(month)d, %(day)d, %(hour)d, %(minute)d, %(second)d,0,0,0,%(msec)d))' % locals()
                return repr(val)


    def BuildCallList(fdesc, names, defNamedOptArg, defNamedNotOptArg, defUnnamedArg, defOutArg, is_comment=False):
        """Builds a Python declaration for a method."""
        numArgs = len(fdesc[2])
        numOptArgs = fdesc[6]
        strval = ''
        if numOptArgs == -1:
            firstOptArg = numArgs
            numArgs = numArgs - 1
        else:
            firstOptArg = numArgs - numOptArgs
        for arg in range(numArgs):
            try:
                argName = names[(arg + 1)]
                namedArg = argName is not None
            except IndexError:
                namedArg = 0
            else:
                if not namedArg:
                    argName = 'arg%d' % arg
                else:
                    thisdesc = fdesc[2][arg]
                    defArgVal = MakeDefaultArgRepr(thisdesc)
                    if defArgVal is None:
                        if thisdesc[1] & (pythoncom.PARAMFLAG_FOUT | pythoncom.PARAMFLAG_FIN) == pythoncom.PARAMFLAG_FOUT:
                            defArgVal = defOutArg
                        elif namedArg:
                            if arg >= firstOptArg:
                                defArgVal = defNamedOptArg
                            else:
                                defArgVal = defNamedNotOptArg
                        else:
                            defArgVal = defUnnamedArg
                    argName = MakePublicAttributeName(argName)
                    if (arg + 1) % 5 == 0:
                        strval = strval + '\n'
                        if is_comment:
                            strval = strval + '#'
                        strval = strval + '\t\t\t'
                    strval = strval + ', ' + argName
                if defArgVal:
                    strval = strval + '=' + defArgVal
        else:
            if numOptArgs == -1:
                strval = strval + ', *' + names[(-1)]
            return strval


    if __name__ == '__main__':
        print("Use 'makepy.py' to generate Python code - this module is just a helper")