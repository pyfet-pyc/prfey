# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: win32com\client\genpy.py
"""genpy.py - The worker for makepy.  See makepy.py for more details

This code was moved simply to speed Python in normal circumstances.  As the makepy.py
is normally run from the command line, it reparses the code each time.  Now makepy
is nothing more than the command line handler and public interface.

The makepy command line etc handling is also getting large enough in its own right!
"""
import os, sys, time, win32com, pythoncom
from . import build
error = 'makepy.error'
makepy_version = '0.5.01'
GEN_FULL = 'full'
GEN_DEMAND_BASE = 'demand(base)'
GEN_DEMAND_CHILD = 'demand(child)'
mapVTToTypeString = {pythoncom.VT_I2: 'types.IntType', 
 pythoncom.VT_I4: 'types.IntType', 
 pythoncom.VT_R4: 'types.FloatType', 
 pythoncom.VT_R8: 'types.FloatType', 
 pythoncom.VT_BSTR: 'types.StringType', 
 pythoncom.VT_BOOL: 'types.IntType', 
 pythoncom.VT_VARIANT: 'types.TypeType', 
 pythoncom.VT_I1: 'types.IntType', 
 pythoncom.VT_UI1: 'types.IntType', 
 pythoncom.VT_UI2: 'types.IntType', 
 pythoncom.VT_UI4: 'types.IntType', 
 pythoncom.VT_I8: 'types.LongType', 
 pythoncom.VT_UI8: 'types.LongType', 
 pythoncom.VT_INT: 'types.IntType', 
 pythoncom.VT_DATE: 'pythoncom.PyTimeType', 
 pythoncom.VT_UINT: 'types.IntType'}

def MakeDefaultArgsForPropertyPut(argsDesc):
    ret = []
    for desc in argsDesc[1:]:
        default = build.MakeDefaultArgRepr(desc)
        if default is None:
            break
        ret.append(default)
    else:
        return tuple(ret)


def MakeMapLineEntry(dispid, wFlags, retType, argTypes, user, resultCLSID):
    argTypes = tuple([what[:2] for what in argTypes])
    return '(%s, %d, %s, %s, "%s", %s)' % (
     dispid, wFlags, retType[:2], argTypes, user, resultCLSID)


def MakeEventMethodName(eventName):
    if eventName[:2] == 'On':
        return eventName
    return 'On' + eventName


def WriteSinkEventMap(obj, stream):
    print('\t_dispid_to_func_ = {', file=stream)
    for name, entry in list(obj.propMapGet.items()) + list(obj.propMapPut.items()) + list(obj.mapFuncs.items()):
        fdesc = entry.desc
        print(('\t\t%9d : "%s",' % (entry.desc[0], MakeEventMethodName(entry.names[0]))), file=stream)
    else:
        print('\t\t}', file=stream)


class WritableItem:

    def __cmp__(self, other):
        """Compare for sorting"""
        ret = cmp(self.order, other.order)
        if ret == 0:
            if self.doc:
                ret = cmp(self.doc[0], other.doc[0])
        return ret

    def __lt__(self, other):
        if self.order == other.order:
            return self.doc < other.doc
        return self.order < other.order

    def __repr__(self):
        return 'OleItem: doc=%s, order=%d' % (repr(self.doc), self.order)


class RecordItem(build.OleItem, WritableItem):
    order = 9
    typename = 'RECORD'

    def __init__(self, typeInfo, typeAttr, doc=None, bForUser=1):
        build.OleItem.__init__(self, doc)
        self.clsid = typeAttr[0]

    def WriteClass(self, generator):
        pass


def WriteAliasesForItem(item, aliasItems, stream):
    for alias in aliasItems.values():
        if item.doc and alias.aliasDoc and alias.aliasDoc[0] == item.doc[0]:
            alias.WriteAliasItem(aliasItems, stream)


class AliasItem(build.OleItem, WritableItem):
    order = 2
    typename = 'ALIAS'

    def __init__(self, typeinfo, attr, doc=None, bForUser=1):
        build.OleItem.__init__(self, doc)
        ai = attr[14]
        self.attr = attr
        if type(ai) == type(()) and type(ai[1]) == type(0):
            href = ai[1]
            alinfo = typeinfo.GetRefTypeInfo(href)
            self.aliasDoc = alinfo.GetDocumentation(-1)
            self.aliasAttr = alinfo.GetTypeAttr()
        else:
            self.aliasDoc = None
            self.aliasAttr = None

    def WriteAliasItem(self, aliasDict, stream):
        if self.bWritten:
            return
            if self.aliasDoc:
                depName = self.aliasDoc[0]
                if depName in aliasDict:
                    aliasDict[depName].WriteAliasItem(aliasDict, stream)
                print((self.doc[0] + ' = ' + depName), file=stream)
        else:
            ai = self.attr[14]
            if type(ai) == type(0):
                try:
                    typeStr = mapVTToTypeString[ai]
                    print(('# %s=%s' % (self.doc[0], typeStr)), file=stream)
                except KeyError:
                    print((self.doc[0] + " = None # Can't convert alias info " + str(ai)), file=stream)

        print(file=stream)
        self.bWritten = 1


class EnumerationItem(build.OleItem, WritableItem):
    order = 1
    typename = 'ENUMERATION'

    def __init__(self, typeinfo, attr, doc=None, bForUser=1):
        build.OleItem.__init__(self, doc)
        self.clsid = attr[0]
        self.mapVars = {}
        typeFlags = attr[11]
        self.hidden = typeFlags & pythoncom.TYPEFLAG_FHIDDEN or typeFlags & pythoncom.TYPEFLAG_FRESTRICTED
        for j in range(attr[7]):
            vdesc = typeinfo.GetVarDesc(j)
            name = typeinfo.GetNames(vdesc[0])[0]
            self.mapVars[name] = build.MapEntry(vdesc)

    def WriteEnumerationItems(self, stream):
        num = 0
        enumName = self.doc[0]
        names = list(self.mapVars.keys())
        names.sort()
        for name in names:
            entry = self.mapVars[name]
            vdesc = entry.desc
            if vdesc[4] == pythoncom.VAR_CONST:
                val = vdesc[1]
                use = repr(val)
                try:
                    compile(use, '<makepy>', 'eval')
                except SyntaxError:
                    use = use.replace('"', "'")
                    use = '"' + use + '"' + ' # This VARIANT type cannot be converted automatically'
                else:
                    print(('\t%-30s=%-10s # from enum %s' % (
                     build.MakePublicAttributeName(name, True), use, enumName)),
                      file=stream)
                    num += 1
            return num


class VTableItem(build.VTableItem, WritableItem):
    order = 4

    def WriteClass(self, generator):
        self.WriteVTableMap(generator)
        self.bWritten = 1

    def WriteVTableMap(self, generator):
        stream = generator.file
        print(('%s_vtables_dispatch_ = %d' % (self.python_name, self.bIsDispatch)), file=stream)
        print(('%s_vtables_ = [' % (self.python_name,)), file=stream)
        for v in self.vtableFuncs:
            names, dispid, desc = v
            arg_desc = desc[2]
            arg_reprs = []
            item_num = 0
            print('\t((', end=' ', file=stream)
            for name in names:
                print((repr(name)), ',', end=' ', file=stream)
                item_num = item_num + 1
                if item_num % 5 == 0:
                    print('\n\t\t\t', end=' ', file=stream)
                print(('), %d, (%r, %r, [' % (dispid, desc[0], desc[1])), end=' ', file=stream)
                for arg in arg_desc:
                    item_num = item_num + 1
                    if item_num % 5 == 0:
                        print('\n\t\t\t', end=' ', file=stream)
                    else:
                        defval = build.MakeDefaultArgRepr(arg)
                        if arg[3] is None:
                            arg3_repr = None
                        else:
                            arg3_repr = repr(arg[3])
                    print((repr((arg[0], arg[1], defval, arg3_repr))), ',', end=' ', file=stream)
                else:
                    print('],', end=' ', file=stream)
                    for d in desc[3:]:
                        print((repr(d)), ',', end=' ', file=stream)
                    else:
                        print(')),', file=stream)

            else:
                print(']', file=stream)
                print(file=stream)


class DispatchItem(build.DispatchItem, WritableItem):
    order = 3

    def __init__(self, typeinfo, attr, doc=None):
        build.DispatchItem.__init__(self, typeinfo, attr, doc)
        self.type_attr = attr
        self.coclass_clsid = None

    def WriteClass(self, generator):
        if not self.bIsDispatch:
            if not self.type_attr.typekind == pythoncom.TKIND_DISPATCH:
                return
        elif self.bIsSink:
            self.WriteEventSinkClassHeader(generator)
            self.WriteCallbackClassBody(generator)
        else:
            self.WriteClassHeader(generator)
            self.WriteClassBody(generator)
        print(file=(generator.file))
        self.bWritten = 1

    def WriteClassHeader(self, generator):
        generator.checkWriteDispatchBaseClass()
        doc = self.doc
        stream = generator.file
        print(('class ' + self.python_name + '(DispatchBaseClass):'), file=stream)
        if doc[1]:
            print(('\t' + build._makeDocString(doc[1])), file=stream)
        try:
            progId = pythoncom.ProgIDFromCLSID(self.clsid)
            print(("\t# This class is creatable by the name '%s'" % progId), file=stream)
        except pythoncom.com_error:
            pass
        else:
            print(('\tCLSID = ' + repr(self.clsid)), file=stream)
            if self.coclass_clsid is None:
                print('\tcoclass_clsid = None', file=stream)
            else:
                print(('\tcoclass_clsid = ' + repr(self.coclass_clsid)), file=stream)
            print(file=stream)
            self.bWritten = 1

    def WriteEventSinkClassHeader(self, generator):
        generator.checkWriteEventBaseClass()
        doc = self.doc
        stream = generator.file
        print(('class ' + self.python_name + ':'), file=stream)
        if doc[1]:
            print(('\t' + build._makeDocString(doc[1])), file=stream)
        try:
            progId = pythoncom.ProgIDFromCLSID(self.clsid)
            print(("\t# This class is creatable by the name '%s'" % progId), file=stream)
        except pythoncom.com_error:
            pass
        else:
            print(('\tCLSID = CLSID_Sink = ' + repr(self.clsid)), file=stream)
            if self.coclass_clsid is None:
                print('\tcoclass_clsid = None', file=stream)
            else:
                print(('\tcoclass_clsid = ' + repr(self.coclass_clsid)), file=stream)
            print('\t_public_methods_ = [] # For COM Server support', file=stream)
            WriteSinkEventMap(self, stream)
            print(file=stream)
            print('\tdef __init__(self, oobj = None):', file=stream)
            print('\t\tif oobj is None:', file=stream)
            print('\t\t\tself._olecp = None', file=stream)
            print('\t\telse:', file=stream)
            print('\t\t\timport win32com.server.util', file=stream)
            print('\t\t\tfrom win32com.server.policy import EventHandlerPolicy', file=stream)
            print('\t\t\tcpc=oobj._oleobj_.QueryInterface(pythoncom.IID_IConnectionPointContainer)', file=stream)
            print('\t\t\tcp=cpc.FindConnectionPoint(self.CLSID_Sink)', file=stream)
            print('\t\t\tcookie=cp.Advise(win32com.server.util.wrap(self, usePolicy=EventHandlerPolicy))', file=stream)
            print('\t\t\tself._olecp,self._olecp_cookie = cp,cookie', file=stream)
            print('\tdef __del__(self):', file=stream)
            print('\t\ttry:', file=stream)
            print('\t\t\tself.close()', file=stream)
            print('\t\texcept pythoncom.com_error:', file=stream)
            print('\t\t\tpass', file=stream)
            print('\tdef close(self):', file=stream)
            print('\t\tif self._olecp is not None:', file=stream)
            print('\t\t\tcp,cookie,self._olecp,self._olecp_cookie = self._olecp,self._olecp_cookie,None,None', file=stream)
            print('\t\t\tcp.Unadvise(cookie)', file=stream)
            print('\tdef _query_interface_(self, iid):', file=stream)
            print('\t\timport win32com.server.util', file=stream)
            print('\t\tif iid==self.CLSID_Sink: return win32com.server.util.wrap(self)', file=stream)
            print(file=stream)
            self.bWritten = 1

    def WriteCallbackClassBody(self, generator):
        stream = generator.file
        print('\t# Event Handlers', file=stream)
        print('\t# If you create handlers, they should have the following prototypes:', file=stream)
        for name, entry in list(self.propMapGet.items()) + list(self.propMapPut.items()) + list(self.mapFuncs.items()):
            fdesc = entry.desc
            methName = MakeEventMethodName(entry.names[0])
            print(('#\tdef ' + methName + '(self' + build.BuildCallList(fdesc, (entry.names), 'defaultNamedOptArg', 'defaultNamedNotOptArg', 'defaultUnnamedArg', 'pythoncom.Missing', is_comment=True) + '):'), file=stream)
            if entry.doc:
                if entry.doc[1]:
                    print(('#\t\t' + build._makeDocString(entry.doc[1])), file=stream)
                print(file=stream)
                self.bWritten = 1

    def WriteClassBody--- This code section failed: ---

 L. 365         0  LOAD_FAST                'generator'
                2  LOAD_ATTR                file
                4  STORE_FAST               'stream'

 L. 367         6  LOAD_GLOBAL              list
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                mapFuncs
               12  LOAD_METHOD              keys
               14  CALL_METHOD_0         0  ''
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'names'

 L. 368        20  LOAD_FAST                'names'
               22  LOAD_METHOD              sort
               24  CALL_METHOD_0         0  ''
               26  POP_TOP          

 L. 369        28  LOAD_CONST               None
               30  LOAD_CONST               None
               32  LOAD_CONST               None
               34  LOAD_CONST               None
               36  LOAD_CONST               ('count', 'item', 'value', '_newenum')
               38  BUILD_CONST_KEY_MAP_4     4 
               40  STORE_FAST               'specialItems'

 L. 370        42  LOAD_CONST               None
               44  STORE_FAST               'itemCount'

 L. 371        46  LOAD_FAST                'names'
               48  GET_ITER         
             50_0  COME_FROM           230  '230'
            50_52  FOR_ITER            330  'to 330'
               54  STORE_FAST               'name'

 L. 372        56  LOAD_FAST                'self'
               58  LOAD_ATTR                mapFuncs
               60  LOAD_FAST                'name'
               62  BINARY_SUBSCR    
               64  STORE_FAST               'entry'

 L. 376        66  LOAD_FAST                'entry'
               68  LOAD_ATTR                desc
               70  LOAD_CONST               0
               72  BINARY_SUBSCR    
               74  STORE_FAST               'dispid'

 L. 377        76  LOAD_FAST                'entry'
               78  LOAD_ATTR                desc
               80  LOAD_CONST               9
               82  BINARY_SUBSCR    
               84  LOAD_GLOBAL              pythoncom
               86  LOAD_ATTR                FUNCFLAG_FRESTRICTED
               88  BINARY_AND       
               90  POP_JUMP_IF_FALSE   104  'to 104'

 L. 378        92  LOAD_FAST                'dispid'
               94  LOAD_GLOBAL              pythoncom
               96  LOAD_ATTR                DISPID_NEWENUM
               98  COMPARE_OP               !=

 L. 377       100  POP_JUMP_IF_FALSE   104  'to 104'

 L. 379       102  JUMP_BACK            50  'to 50'
            104_0  COME_FROM           100  '100'
            104_1  COME_FROM            90  '90'

 L. 381       104  LOAD_FAST                'entry'
              106  LOAD_ATTR                desc
              108  LOAD_CONST               3
              110  BINARY_SUBSCR    
              112  LOAD_GLOBAL              pythoncom
              114  LOAD_ATTR                FUNC_DISPATCH
              116  COMPARE_OP               !=
              118  POP_JUMP_IF_FALSE   122  'to 122'

 L. 382       120  JUMP_BACK            50  'to 50'
            122_0  COME_FROM           118  '118'

 L. 383       122  LOAD_FAST                'dispid'
              124  LOAD_GLOBAL              pythoncom
              126  LOAD_ATTR                DISPID_VALUE
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE   138  'to 138'

 L. 384       132  LOAD_STR                 'value'
              134  STORE_FAST               'lkey'
              136  JUMP_FORWARD        180  'to 180'
            138_0  COME_FROM           130  '130'

 L. 385       138  LOAD_FAST                'dispid'
              140  LOAD_GLOBAL              pythoncom
              142  LOAD_ATTR                DISPID_NEWENUM
              144  COMPARE_OP               ==
              146  POP_JUMP_IF_FALSE   172  'to 172'

 L. 386       148  LOAD_FAST                'entry'
              150  LOAD_FAST                'entry'
              152  LOAD_ATTR                desc
              154  LOAD_CONST               4
              156  BINARY_SUBSCR    
              158  LOAD_CONST               None
              160  BUILD_TUPLE_3         3 
              162  LOAD_FAST                'specialItems'
              164  LOAD_STR                 '_newenum'
              166  STORE_SUBSCR     

 L. 387       168  JUMP_BACK            50  'to 50'
              170  JUMP_FORWARD        180  'to 180'
            172_0  COME_FROM           146  '146'

 L. 389       172  LOAD_FAST                'name'
              174  LOAD_METHOD              lower
              176  CALL_METHOD_0         0  ''
              178  STORE_FAST               'lkey'
            180_0  COME_FROM           170  '170'
            180_1  COME_FROM           136  '136'

 L. 390       180  LOAD_FAST                'lkey'
              182  LOAD_FAST                'specialItems'
              184  COMPARE_OP               in
              186  POP_JUMP_IF_FALSE   220  'to 220'
              188  LOAD_FAST                'specialItems'
              190  LOAD_FAST                'lkey'
              192  BINARY_SUBSCR    
              194  LOAD_CONST               None
              196  COMPARE_OP               is
              198  POP_JUMP_IF_FALSE   220  'to 220'

 L. 391       200  LOAD_FAST                'entry'
              202  LOAD_FAST                'entry'
              204  LOAD_ATTR                desc
              206  LOAD_CONST               4
              208  BINARY_SUBSCR    
              210  LOAD_CONST               None
              212  BUILD_TUPLE_3         3 
              214  LOAD_FAST                'specialItems'
              216  LOAD_FAST                'lkey'
              218  STORE_SUBSCR     
            220_0  COME_FROM           198  '198'
            220_1  COME_FROM           186  '186'

 L. 392       220  LOAD_FAST                'generator'
              222  LOAD_ATTR                bBuildHidden
              224  POP_JUMP_IF_TRUE    232  'to 232'
              226  LOAD_FAST                'entry'
              228  LOAD_ATTR                hidden
              230  POP_JUMP_IF_TRUE     50  'to 50'
            232_0  COME_FROM           224  '224'

 L. 393       232  LOAD_FAST                'entry'
              234  LOAD_METHOD              GetResultName
              236  CALL_METHOD_0         0  ''
          238_240  POP_JUMP_IF_FALSE   262  'to 262'

 L. 394       242  LOAD_GLOBAL              print
              244  LOAD_STR                 '\t# Result is of type '
              246  LOAD_FAST                'entry'
              248  LOAD_METHOD              GetResultName
              250  CALL_METHOD_0         0  ''
              252  BINARY_ADD       
              254  LOAD_FAST                'stream'
              256  LOAD_CONST               ('file',)
              258  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              260  POP_TOP          
            262_0  COME_FROM           238  '238'

 L. 395       262  LOAD_FAST                'entry'
              264  LOAD_ATTR                wasProperty
          266_268  POP_JUMP_IF_FALSE   286  'to 286'

 L. 396       270  LOAD_GLOBAL              print
              272  LOAD_STR                 '\t# The method %s is actually a property, but must be used as a method to correctly pass the arguments'
              274  LOAD_FAST                'name'
              276  BINARY_MODULO    
              278  LOAD_FAST                'stream'
              280  LOAD_CONST               ('file',)
              282  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              284  POP_TOP          
            286_0  COME_FROM           266  '266'

 L. 397       286  LOAD_FAST                'self'
              288  LOAD_METHOD              MakeFuncMethod
              290  LOAD_FAST                'entry'
              292  LOAD_GLOBAL              build
              294  LOAD_METHOD              MakePublicAttributeName
              296  LOAD_FAST                'name'
              298  CALL_METHOD_1         1  ''
              300  CALL_METHOD_2         2  ''
              302  STORE_FAST               'ret'

 L. 398       304  LOAD_FAST                'ret'
              306  GET_ITER         
              308  FOR_ITER            328  'to 328'
              310  STORE_FAST               'line'

 L. 399       312  LOAD_GLOBAL              print
              314  LOAD_FAST                'line'
              316  LOAD_FAST                'stream'
              318  LOAD_CONST               ('file',)
              320  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              322  POP_TOP          
          324_326  JUMP_BACK           308  'to 308'
              328  JUMP_BACK            50  'to 50'

 L. 400       330  LOAD_GLOBAL              print
              332  LOAD_STR                 '\t_prop_map_get_ = {'
              334  LOAD_FAST                'stream'
              336  LOAD_CONST               ('file',)
              338  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              340  POP_TOP          

 L. 401       342  LOAD_GLOBAL              list
              344  LOAD_FAST                'self'
              346  LOAD_ATTR                propMap
              348  LOAD_METHOD              keys
              350  CALL_METHOD_0         0  ''
              352  CALL_FUNCTION_1       1  ''
              354  STORE_FAST               'names'

 L. 401       356  LOAD_FAST                'names'
              358  LOAD_METHOD              sort
              360  CALL_METHOD_0         0  ''
              362  POP_TOP          

 L. 402       364  LOAD_FAST                'names'
              366  GET_ITER         
            368_0  COME_FROM           396  '396'
          368_370  FOR_ITER            636  'to 636'
              372  STORE_FAST               'key'

 L. 403       374  LOAD_FAST                'self'
              376  LOAD_ATTR                propMap
              378  LOAD_FAST                'key'
              380  BINARY_SUBSCR    
              382  STORE_FAST               'entry'

 L. 404       384  LOAD_FAST                'generator'
              386  LOAD_ATTR                bBuildHidden
          388_390  POP_JUMP_IF_TRUE    400  'to 400'
              392  LOAD_FAST                'entry'
              394  LOAD_ATTR                hidden
          396_398  POP_JUMP_IF_TRUE    368  'to 368'
            400_0  COME_FROM           388  '388'

 L. 405       400  LOAD_FAST                'entry'
              402  LOAD_METHOD              GetResultName
              404  CALL_METHOD_0         0  ''
              406  STORE_FAST               'resultName'

 L. 406       408  LOAD_FAST                'resultName'
          410_412  POP_JUMP_IF_FALSE   434  'to 434'

 L. 407       414  LOAD_GLOBAL              print
              416  LOAD_STR                 "\t\t# Property '%s' is an object of type '%s'"
              418  LOAD_FAST                'key'
              420  LOAD_FAST                'resultName'
              422  BUILD_TUPLE_2         2 
              424  BINARY_MODULO    
              426  LOAD_FAST                'stream'
              428  LOAD_CONST               ('file',)
              430  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              432  POP_TOP          
            434_0  COME_FROM           410  '410'

 L. 408       434  LOAD_FAST                'key'
              436  LOAD_METHOD              lower
              438  CALL_METHOD_0         0  ''
              440  STORE_FAST               'lkey'

 L. 409       442  LOAD_FAST                'entry'
              444  LOAD_ATTR                desc
              446  STORE_FAST               'details'

 L. 410       448  LOAD_FAST                'details'
              450  LOAD_CONST               2
              452  BINARY_SUBSCR    
              454  STORE_FAST               'resultDesc'

 L. 411       456  LOAD_CONST               ()
              458  STORE_FAST               'argDesc'

 L. 412       460  LOAD_GLOBAL              MakeMapLineEntry
              462  LOAD_FAST                'details'
              464  LOAD_CONST               0
              466  BINARY_SUBSCR    
              468  LOAD_GLOBAL              pythoncom
              470  LOAD_ATTR                DISPATCH_PROPERTYGET
              472  LOAD_FAST                'resultDesc'
              474  LOAD_FAST                'argDesc'
              476  LOAD_FAST                'key'
              478  LOAD_FAST                'entry'
              480  LOAD_METHOD              GetResultCLSIDStr
              482  CALL_METHOD_0         0  ''
              484  CALL_FUNCTION_6       6  ''
              486  STORE_FAST               'mapEntry'

 L. 414       488  LOAD_FAST                'entry'
              490  LOAD_ATTR                desc
              492  LOAD_CONST               0
              494  BINARY_SUBSCR    
              496  LOAD_GLOBAL              pythoncom
              498  LOAD_ATTR                DISPID_VALUE
              500  COMPARE_OP               ==
          502_504  POP_JUMP_IF_FALSE   512  'to 512'

 L. 415       506  LOAD_STR                 'value'
              508  STORE_FAST               'lkey'
              510  JUMP_FORWARD        544  'to 544'
            512_0  COME_FROM           502  '502'

 L. 416       512  LOAD_FAST                'entry'
              514  LOAD_ATTR                desc
              516  LOAD_CONST               0
              518  BINARY_SUBSCR    
              520  LOAD_GLOBAL              pythoncom
              522  LOAD_ATTR                DISPID_NEWENUM
              524  COMPARE_OP               ==
          526_528  POP_JUMP_IF_FALSE   536  'to 536'

 L. 417       530  LOAD_STR                 '_newenum'
              532  STORE_FAST               'lkey'
              534  JUMP_FORWARD        544  'to 544'
            536_0  COME_FROM           526  '526'

 L. 419       536  LOAD_FAST                'key'
              538  LOAD_METHOD              lower
              540  CALL_METHOD_0         0  ''
              542  STORE_FAST               'lkey'
            544_0  COME_FROM           534  '534'
            544_1  COME_FROM           510  '510'

 L. 420       544  LOAD_FAST                'lkey'
              546  LOAD_FAST                'specialItems'
              548  COMPARE_OP               in
          550_552  POP_JUMP_IF_FALSE   606  'to 606'
              554  LOAD_FAST                'specialItems'
              556  LOAD_FAST                'lkey'
              558  BINARY_SUBSCR    
              560  LOAD_CONST               None
              562  COMPARE_OP               is
          564_566  POP_JUMP_IF_FALSE   606  'to 606'

 L. 421       568  LOAD_FAST                'entry'
              570  LOAD_GLOBAL              pythoncom
              572  LOAD_ATTR                DISPATCH_PROPERTYGET
              574  LOAD_FAST                'mapEntry'
              576  BUILD_TUPLE_3         3 
              578  LOAD_FAST                'specialItems'
              580  LOAD_FAST                'lkey'
              582  STORE_SUBSCR     

 L. 424       584  LOAD_FAST                'entry'
              586  LOAD_ATTR                desc
              588  LOAD_CONST               0
              590  BINARY_SUBSCR    
              592  LOAD_GLOBAL              pythoncom
              594  LOAD_ATTR                DISPID_NEWENUM
              596  COMPARE_OP               ==
          598_600  POP_JUMP_IF_FALSE   606  'to 606'

 L. 425   602_604  JUMP_BACK           368  'to 368'
            606_0  COME_FROM           598  '598'
            606_1  COME_FROM           564  '564'
            606_2  COME_FROM           550  '550'

 L. 427       606  LOAD_GLOBAL              print
              608  LOAD_STR                 '\t\t"%s": %s,'
              610  LOAD_GLOBAL              build
              612  LOAD_METHOD              MakePublicAttributeName
              614  LOAD_FAST                'key'
              616  CALL_METHOD_1         1  ''
              618  LOAD_FAST                'mapEntry'
              620  BUILD_TUPLE_2         2 
              622  BINARY_MODULO    
              624  LOAD_FAST                'stream'
              626  LOAD_CONST               ('file',)
              628  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              630  POP_TOP          
          632_634  JUMP_BACK           368  'to 368'

 L. 428       636  LOAD_GLOBAL              list
              638  LOAD_FAST                'self'
              640  LOAD_ATTR                propMapGet
              642  LOAD_METHOD              keys
              644  CALL_METHOD_0         0  ''
              646  CALL_FUNCTION_1       1  ''
              648  STORE_FAST               'names'

 L. 428       650  LOAD_FAST                'names'
              652  LOAD_METHOD              sort
              654  CALL_METHOD_0         0  ''
              656  POP_TOP          

 L. 429       658  LOAD_FAST                'names'
              660  GET_ITER         
            662_0  COME_FROM           690  '690'
          662_664  FOR_ITER            934  'to 934'
              666  STORE_FAST               'key'

 L. 430       668  LOAD_FAST                'self'
              670  LOAD_ATTR                propMapGet
              672  LOAD_FAST                'key'
              674  BINARY_SUBSCR    
              676  STORE_FAST               'entry'

 L. 431       678  LOAD_FAST                'generator'
              680  LOAD_ATTR                bBuildHidden
          682_684  POP_JUMP_IF_TRUE    694  'to 694'
              686  LOAD_FAST                'entry'
              688  LOAD_ATTR                hidden
          690_692  POP_JUMP_IF_TRUE    662  'to 662'
            694_0  COME_FROM           682  '682'

 L. 432       694  LOAD_FAST                'entry'
              696  LOAD_METHOD              GetResultName
              698  CALL_METHOD_0         0  ''
          700_702  POP_JUMP_IF_FALSE   728  'to 728'

 L. 433       704  LOAD_GLOBAL              print
              706  LOAD_STR                 "\t\t# Method '%s' returns object of type '%s'"
              708  LOAD_FAST                'key'
              710  LOAD_FAST                'entry'
              712  LOAD_METHOD              GetResultName
              714  CALL_METHOD_0         0  ''
              716  BUILD_TUPLE_2         2 
              718  BINARY_MODULO    
              720  LOAD_FAST                'stream'
              722  LOAD_CONST               ('file',)
              724  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              726  POP_TOP          
            728_0  COME_FROM           700  '700'

 L. 434       728  LOAD_FAST                'entry'
              730  LOAD_ATTR                desc
              732  STORE_FAST               'details'

 L. 435       734  LOAD_FAST                'key'
              736  LOAD_METHOD              lower
              738  CALL_METHOD_0         0  ''
              740  STORE_FAST               'lkey'

 L. 436       742  LOAD_FAST                'details'
              744  LOAD_CONST               2
              746  BINARY_SUBSCR    
              748  STORE_FAST               'argDesc'

 L. 437       750  LOAD_FAST                'details'
              752  LOAD_CONST               8
              754  BINARY_SUBSCR    
              756  STORE_FAST               'resultDesc'

 L. 438       758  LOAD_GLOBAL              MakeMapLineEntry
              760  LOAD_FAST                'details'
              762  LOAD_CONST               0
              764  BINARY_SUBSCR    
              766  LOAD_GLOBAL              pythoncom
              768  LOAD_ATTR                DISPATCH_PROPERTYGET
              770  LOAD_FAST                'resultDesc'
              772  LOAD_FAST                'argDesc'
              774  LOAD_FAST                'key'
              776  LOAD_FAST                'entry'
              778  LOAD_METHOD              GetResultCLSIDStr
              780  CALL_METHOD_0         0  ''
              782  CALL_FUNCTION_6       6  ''
              784  STORE_FAST               'mapEntry'

 L. 439       786  LOAD_FAST                'entry'
              788  LOAD_ATTR                desc
              790  LOAD_CONST               0
              792  BINARY_SUBSCR    
              794  LOAD_GLOBAL              pythoncom
              796  LOAD_ATTR                DISPID_VALUE
              798  COMPARE_OP               ==
          800_802  POP_JUMP_IF_FALSE   810  'to 810'

 L. 440       804  LOAD_STR                 'value'
              806  STORE_FAST               'lkey'
              808  JUMP_FORWARD        842  'to 842'
            810_0  COME_FROM           800  '800'

 L. 441       810  LOAD_FAST                'entry'
              812  LOAD_ATTR                desc
              814  LOAD_CONST               0
              816  BINARY_SUBSCR    
              818  LOAD_GLOBAL              pythoncom
              820  LOAD_ATTR                DISPID_NEWENUM
              822  COMPARE_OP               ==
          824_826  POP_JUMP_IF_FALSE   834  'to 834'

 L. 442       828  LOAD_STR                 '_newenum'
              830  STORE_FAST               'lkey'
              832  JUMP_FORWARD        842  'to 842'
            834_0  COME_FROM           824  '824'

 L. 444       834  LOAD_FAST                'key'
              836  LOAD_METHOD              lower
              838  CALL_METHOD_0         0  ''
              840  STORE_FAST               'lkey'
            842_0  COME_FROM           832  '832'
            842_1  COME_FROM           808  '808'

 L. 445       842  LOAD_FAST                'lkey'
              844  LOAD_FAST                'specialItems'
              846  COMPARE_OP               in
          848_850  POP_JUMP_IF_FALSE   904  'to 904'
              852  LOAD_FAST                'specialItems'
              854  LOAD_FAST                'lkey'
              856  BINARY_SUBSCR    
              858  LOAD_CONST               None
              860  COMPARE_OP               is
          862_864  POP_JUMP_IF_FALSE   904  'to 904'

 L. 446       866  LOAD_FAST                'entry'
              868  LOAD_GLOBAL              pythoncom
              870  LOAD_ATTR                DISPATCH_PROPERTYGET
              872  LOAD_FAST                'mapEntry'
              874  BUILD_TUPLE_3         3 
              876  LOAD_FAST                'specialItems'
              878  LOAD_FAST                'lkey'
              880  STORE_SUBSCR     

 L. 449       882  LOAD_FAST                'entry'
              884  LOAD_ATTR                desc
              886  LOAD_CONST               0
              888  BINARY_SUBSCR    
              890  LOAD_GLOBAL              pythoncom
              892  LOAD_ATTR                DISPID_NEWENUM
              894  COMPARE_OP               ==
          896_898  POP_JUMP_IF_FALSE   904  'to 904'

 L. 450   900_902  JUMP_BACK           662  'to 662'
            904_0  COME_FROM           896  '896'
            904_1  COME_FROM           862  '862'
            904_2  COME_FROM           848  '848'

 L. 451       904  LOAD_GLOBAL              print
              906  LOAD_STR                 '\t\t"%s": %s,'
              908  LOAD_GLOBAL              build
              910  LOAD_METHOD              MakePublicAttributeName
              912  LOAD_FAST                'key'
              914  CALL_METHOD_1         1  ''
              916  LOAD_FAST                'mapEntry'
              918  BUILD_TUPLE_2         2 
              920  BINARY_MODULO    
              922  LOAD_FAST                'stream'
              924  LOAD_CONST               ('file',)
              926  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              928  POP_TOP          
          930_932  JUMP_BACK           662  'to 662'

 L. 453       934  LOAD_GLOBAL              print
              936  LOAD_STR                 '\t}'
              938  LOAD_FAST                'stream'
              940  LOAD_CONST               ('file',)
              942  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              944  POP_TOP          

 L. 455       946  LOAD_GLOBAL              print
              948  LOAD_STR                 '\t_prop_map_put_ = {'
              950  LOAD_FAST                'stream'
              952  LOAD_CONST               ('file',)
              954  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              956  POP_TOP          

 L. 457       958  LOAD_GLOBAL              list
              960  LOAD_FAST                'self'
              962  LOAD_ATTR                propMap
              964  LOAD_METHOD              keys
              966  CALL_METHOD_0         0  ''
              968  CALL_FUNCTION_1       1  ''
              970  STORE_FAST               'names'

 L. 457       972  LOAD_FAST                'names'
              974  LOAD_METHOD              sort
              976  CALL_METHOD_0         0  ''
              978  POP_TOP          

 L. 458       980  LOAD_FAST                'names'
              982  GET_ITER         
            984_0  COME_FROM          1010  '1010'
              984  FOR_ITER           1106  'to 1106'
              986  STORE_FAST               'key'

 L. 459       988  LOAD_FAST                'self'
              990  LOAD_ATTR                propMap
              992  LOAD_FAST                'key'
              994  BINARY_SUBSCR    
              996  STORE_FAST               'entry'

 L. 460       998  LOAD_FAST                'generator'
             1000  LOAD_ATTR                bBuildHidden
         1002_1004  POP_JUMP_IF_TRUE   1014  'to 1014'
             1006  LOAD_FAST                'entry'
             1008  LOAD_ATTR                hidden
         1010_1012  POP_JUMP_IF_TRUE    984  'to 984'
           1014_0  COME_FROM          1002  '1002'

 L. 461      1014  LOAD_FAST                'key'
             1016  LOAD_METHOD              lower
             1018  CALL_METHOD_0         0  ''
             1020  STORE_FAST               'lkey'

 L. 462      1022  LOAD_FAST                'entry'
             1024  LOAD_ATTR                desc
             1026  STORE_FAST               'details'

 L. 464      1028  LOAD_GLOBAL              build
             1030  LOAD_METHOD              MakeDefaultArgRepr
             1032  LOAD_FAST                'details'
             1034  LOAD_CONST               2
             1036  BINARY_SUBSCR    
             1038  CALL_METHOD_1         1  ''
             1040  STORE_FAST               'defArgDesc'

 L. 465      1042  LOAD_FAST                'defArgDesc'
             1044  LOAD_CONST               None
             1046  COMPARE_OP               is
         1048_1050  POP_JUMP_IF_FALSE  1058  'to 1058'

 L. 466      1052  LOAD_STR                 ''
             1054  STORE_FAST               'defArgDesc'
             1056  JUMP_FORWARD       1066  'to 1066'
           1058_0  COME_FROM          1048  '1048'

 L. 468      1058  LOAD_FAST                'defArgDesc'
             1060  LOAD_STR                 ','
             1062  BINARY_ADD       
             1064  STORE_FAST               'defArgDesc'
           1066_0  COME_FROM          1056  '1056'

 L. 469      1066  LOAD_GLOBAL              print
             1068  LOAD_STR                 '\t\t"%s" : ((%s, LCID, %d, 0),(%s)),'
             1070  LOAD_GLOBAL              build
             1072  LOAD_METHOD              MakePublicAttributeName
             1074  LOAD_FAST                'key'
             1076  CALL_METHOD_1         1  ''
             1078  LOAD_FAST                'details'
             1080  LOAD_CONST               0
             1082  BINARY_SUBSCR    
             1084  LOAD_GLOBAL              pythoncom
             1086  LOAD_ATTR                DISPATCH_PROPERTYPUT
             1088  LOAD_FAST                'defArgDesc'
             1090  BUILD_TUPLE_4         4 
             1092  BINARY_MODULO    
             1094  LOAD_FAST                'stream'
             1096  LOAD_CONST               ('file',)
             1098  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1100  POP_TOP          
         1102_1104  JUMP_BACK           984  'to 984'

 L. 471      1106  LOAD_GLOBAL              list
             1108  LOAD_FAST                'self'
             1110  LOAD_ATTR                propMapPut
             1112  LOAD_METHOD              keys
             1114  CALL_METHOD_0         0  ''
             1116  CALL_FUNCTION_1       1  ''
             1118  STORE_FAST               'names'

 L. 471      1120  LOAD_FAST                'names'
             1122  LOAD_METHOD              sort
             1124  CALL_METHOD_0         0  ''
             1126  POP_TOP          

 L. 472      1128  LOAD_FAST                'names'
             1130  GET_ITER         
           1132_0  COME_FROM          1158  '1158'
             1132  FOR_ITER           1222  'to 1222'
             1134  STORE_FAST               'key'

 L. 473      1136  LOAD_FAST                'self'
             1138  LOAD_ATTR                propMapPut
             1140  LOAD_FAST                'key'
             1142  BINARY_SUBSCR    
             1144  STORE_FAST               'entry'

 L. 474      1146  LOAD_FAST                'generator'
             1148  LOAD_ATTR                bBuildHidden
         1150_1152  POP_JUMP_IF_TRUE   1162  'to 1162'
             1154  LOAD_FAST                'entry'
             1156  LOAD_ATTR                hidden
         1158_1160  POP_JUMP_IF_TRUE   1132  'to 1132'
           1162_0  COME_FROM          1150  '1150'

 L. 475      1162  LOAD_FAST                'entry'
             1164  LOAD_ATTR                desc
             1166  STORE_FAST               'details'

 L. 476      1168  LOAD_GLOBAL              MakeDefaultArgsForPropertyPut
             1170  LOAD_FAST                'details'
             1172  LOAD_CONST               2
             1174  BINARY_SUBSCR    
             1176  CALL_FUNCTION_1       1  ''
             1178  STORE_FAST               'defArgDesc'

 L. 477      1180  LOAD_GLOBAL              print
             1182  LOAD_STR                 '\t\t"%s": ((%s, LCID, %d, 0),%s),'
             1184  LOAD_GLOBAL              build
             1186  LOAD_METHOD              MakePublicAttributeName
             1188  LOAD_FAST                'key'
             1190  CALL_METHOD_1         1  ''
             1192  LOAD_FAST                'details'
             1194  LOAD_CONST               0
             1196  BINARY_SUBSCR    
             1198  LOAD_FAST                'details'
             1200  LOAD_CONST               4
             1202  BINARY_SUBSCR    
             1204  LOAD_FAST                'defArgDesc'
             1206  BUILD_TUPLE_4         4 
             1208  BINARY_MODULO    
             1210  LOAD_FAST                'stream'
             1212  LOAD_CONST               ('file',)
             1214  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1216  POP_TOP          
         1218_1220  JUMP_BACK          1132  'to 1132'

 L. 478      1222  LOAD_GLOBAL              print
             1224  LOAD_STR                 '\t}'
             1226  LOAD_FAST                'stream'
             1228  LOAD_CONST               ('file',)
             1230  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1232  POP_TOP          

 L. 480      1234  LOAD_FAST                'specialItems'
             1236  LOAD_STR                 'value'
             1238  BINARY_SUBSCR    
         1240_1242  POP_JUMP_IF_FALSE  1496  'to 1496'

 L. 481      1244  LOAD_FAST                'specialItems'
             1246  LOAD_STR                 'value'
             1248  BINARY_SUBSCR    
             1250  UNPACK_SEQUENCE_3     3 
             1252  STORE_FAST               'entry'
             1254  STORE_FAST               'invoketype'
             1256  STORE_FAST               'propArgs'

 L. 482      1258  LOAD_FAST                'propArgs'
             1260  LOAD_CONST               None
             1262  COMPARE_OP               is
         1264_1266  POP_JUMP_IF_FALSE  1286  'to 1286'

 L. 483      1268  LOAD_STR                 'method'
             1270  STORE_FAST               'typename'

 L. 484      1272  LOAD_FAST                'self'
             1274  LOAD_METHOD              MakeFuncMethod
             1276  LOAD_FAST                'entry'
             1278  LOAD_STR                 '__call__'
             1280  CALL_METHOD_2         2  ''
             1282  STORE_FAST               'ret'
             1284  JUMP_FORWARD       1300  'to 1300'
           1286_0  COME_FROM          1264  '1264'

 L. 486      1286  LOAD_STR                 'property'
             1288  STORE_FAST               'typename'

 L. 487      1290  LOAD_STR                 '\tdef __call__(self):\n\t\treturn self._ApplyTypes_(*%s)'
             1292  LOAD_FAST                'propArgs'
             1294  BINARY_MODULO    
             1296  BUILD_LIST_1          1 
             1298  STORE_FAST               'ret'
           1300_0  COME_FROM          1284  '1284'

 L. 488      1300  LOAD_GLOBAL              print
             1302  LOAD_STR                 "\t# Default %s for this class is '%s'"
             1304  LOAD_FAST                'typename'
             1306  LOAD_FAST                'entry'
             1308  LOAD_ATTR                names
             1310  LOAD_CONST               0
             1312  BINARY_SUBSCR    
             1314  BUILD_TUPLE_2         2 
             1316  BINARY_MODULO    
             1318  LOAD_FAST                'stream'
             1320  LOAD_CONST               ('file',)
             1322  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1324  POP_TOP          

 L. 489      1326  LOAD_FAST                'ret'
             1328  GET_ITER         
             1330  FOR_ITER           1350  'to 1350'
             1332  STORE_FAST               'line'

 L. 490      1334  LOAD_GLOBAL              print
             1336  LOAD_FAST                'line'
             1338  LOAD_FAST                'stream'
             1340  LOAD_CONST               ('file',)
             1342  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1344  POP_TOP          
         1346_1348  JUMP_BACK          1330  'to 1330'

 L. 491      1350  LOAD_GLOBAL              sys
             1352  LOAD_ATTR                version_info
             1354  LOAD_CONST               (3, 0)
             1356  COMPARE_OP               >
         1358_1360  POP_JUMP_IF_FALSE  1388  'to 1388'

 L. 492      1362  LOAD_GLOBAL              print
             1364  LOAD_STR                 '\tdef __str__(self, *args):'
             1366  LOAD_FAST                'stream'
             1368  LOAD_CONST               ('file',)
             1370  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1372  POP_TOP          

 L. 493      1374  LOAD_GLOBAL              print
             1376  LOAD_STR                 '\t\treturn str(self.__call__(*args))'
             1378  LOAD_FAST                'stream'
             1380  LOAD_CONST               ('file',)
             1382  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1384  POP_TOP          
             1386  JUMP_FORWARD       1472  'to 1472'
           1388_0  COME_FROM          1358  '1358'

 L. 495      1388  LOAD_GLOBAL              print
             1390  LOAD_STR                 '\tdef __unicode__(self, *args):'
             1392  LOAD_FAST                'stream'
             1394  LOAD_CONST               ('file',)
             1396  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1398  POP_TOP          

 L. 496      1400  LOAD_GLOBAL              print
             1402  LOAD_STR                 '\t\ttry:'
             1404  LOAD_FAST                'stream'
             1406  LOAD_CONST               ('file',)
             1408  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1410  POP_TOP          

 L. 497      1412  LOAD_GLOBAL              print
             1414  LOAD_STR                 '\t\t\treturn unicode(self.__call__(*args))'
             1416  LOAD_FAST                'stream'
             1418  LOAD_CONST               ('file',)
             1420  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1422  POP_TOP          

 L. 498      1424  LOAD_GLOBAL              print
             1426  LOAD_STR                 '\t\texcept pythoncom.com_error:'
             1428  LOAD_FAST                'stream'
             1430  LOAD_CONST               ('file',)
             1432  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1434  POP_TOP          

 L. 499      1436  LOAD_GLOBAL              print
             1438  LOAD_STR                 '\t\t\treturn repr(self)'
             1440  LOAD_FAST                'stream'
             1442  LOAD_CONST               ('file',)
             1444  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1446  POP_TOP          

 L. 500      1448  LOAD_GLOBAL              print
             1450  LOAD_STR                 '\tdef __str__(self, *args):'
             1452  LOAD_FAST                'stream'
             1454  LOAD_CONST               ('file',)
             1456  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1458  POP_TOP          

 L. 501      1460  LOAD_GLOBAL              print
             1462  LOAD_STR                 '\t\treturn str(self.__unicode__(*args))'
             1464  LOAD_FAST                'stream'
             1466  LOAD_CONST               ('file',)
             1468  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1470  POP_TOP          
           1472_0  COME_FROM          1386  '1386'

 L. 502      1472  LOAD_GLOBAL              print
             1474  LOAD_STR                 '\tdef __int__(self, *args):'
             1476  LOAD_FAST                'stream'
             1478  LOAD_CONST               ('file',)
             1480  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1482  POP_TOP          

 L. 503      1484  LOAD_GLOBAL              print
             1486  LOAD_STR                 '\t\treturn int(self.__call__(*args))'
             1488  LOAD_FAST                'stream'
             1490  LOAD_CONST               ('file',)
             1492  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1494  POP_TOP          
           1496_0  COME_FROM          1240  '1240'

 L. 509      1496  LOAD_FAST                'specialItems'
             1498  LOAD_STR                 '_newenum'
             1500  BINARY_SUBSCR    
         1502_1504  POP_JUMP_IF_FALSE  1540  'to 1540'

 L. 510      1506  LOAD_FAST                'specialItems'
             1508  LOAD_STR                 '_newenum'
             1510  BINARY_SUBSCR    
             1512  UNPACK_SEQUENCE_3     3 
             1514  STORE_FAST               'enumEntry'
             1516  STORE_FAST               'invoketype'
             1518  STORE_FAST               'propArgs'

 L. 511      1520  LOAD_FAST                'enumEntry'
             1522  LOAD_ATTR                desc
             1524  LOAD_CONST               4
             1526  BINARY_SUBSCR    
             1528  STORE_FAST               'invkind'

 L. 514      1530  LOAD_FAST                'enumEntry'
             1532  LOAD_METHOD              GetResultCLSIDStr
             1534  CALL_METHOD_0         0  ''
             1536  STORE_FAST               'resultCLSID'
             1538  JUMP_FORWARD       1556  'to 1556'
           1540_0  COME_FROM          1502  '1502'

 L. 516      1540  LOAD_GLOBAL              pythoncom
             1542  LOAD_ATTR                DISPATCH_METHOD
             1544  LOAD_GLOBAL              pythoncom
             1546  LOAD_ATTR                DISPATCH_PROPERTYGET
             1548  BINARY_OR        
             1550  STORE_FAST               'invkind'

 L. 517      1552  LOAD_STR                 'None'
             1554  STORE_FAST               'resultCLSID'
           1556_0  COME_FROM          1538  '1538'

 L. 519      1556  LOAD_FAST                'resultCLSID'
             1558  LOAD_STR                 'None'
             1560  COMPARE_OP               ==
         1562_1564  POP_JUMP_IF_FALSE  1592  'to 1592'
             1566  LOAD_STR                 'Item'
             1568  LOAD_FAST                'self'
             1570  LOAD_ATTR                mapFuncs
             1572  COMPARE_OP               in
         1574_1576  POP_JUMP_IF_FALSE  1592  'to 1592'

 L. 520      1578  LOAD_FAST                'self'
             1580  LOAD_ATTR                mapFuncs
             1582  LOAD_STR                 'Item'
             1584  BINARY_SUBSCR    
             1586  LOAD_METHOD              GetResultCLSIDStr
             1588  CALL_METHOD_0         0  ''
             1590  STORE_FAST               'resultCLSID'
           1592_0  COME_FROM          1574  '1574'
           1592_1  COME_FROM          1562  '1562'

 L. 521      1592  LOAD_GLOBAL              print
             1594  LOAD_STR                 '\tdef __iter__(self):'
             1596  LOAD_FAST                'stream'
             1598  LOAD_CONST               ('file',)
             1600  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1602  POP_TOP          

 L. 522      1604  LOAD_GLOBAL              print
             1606  LOAD_STR                 '\t\t"Return a Python iterator for this object"'
             1608  LOAD_FAST                'stream'
             1610  LOAD_CONST               ('file',)
             1612  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1614  POP_TOP          

 L. 523      1616  LOAD_GLOBAL              print
             1618  LOAD_STR                 '\t\ttry:'
             1620  LOAD_FAST                'stream'
             1622  LOAD_CONST               ('file',)
             1624  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1626  POP_TOP          

 L. 524      1628  LOAD_GLOBAL              print
             1630  LOAD_STR                 '\t\t\tob = self._oleobj_.InvokeTypes(%d,LCID,%d,(13, 10),())'
             1632  LOAD_GLOBAL              pythoncom
             1634  LOAD_ATTR                DISPID_NEWENUM
             1636  LOAD_FAST                'invkind'
             1638  BUILD_TUPLE_2         2 
             1640  BINARY_MODULO    
             1642  LOAD_FAST                'stream'
             1644  LOAD_CONST               ('file',)
             1646  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1648  POP_TOP          

 L. 525      1650  LOAD_GLOBAL              print
             1652  LOAD_STR                 '\t\texcept pythoncom.error:'
             1654  LOAD_FAST                'stream'
             1656  LOAD_CONST               ('file',)
             1658  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1660  POP_TOP          

 L. 526      1662  LOAD_GLOBAL              print
             1664  LOAD_STR                 '\t\t\traise TypeError("This object does not support enumeration")'
             1666  LOAD_FAST                'stream'
             1668  LOAD_CONST               ('file',)
             1670  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1672  POP_TOP          

 L. 528      1674  LOAD_GLOBAL              print
             1676  LOAD_STR                 '\t\treturn win32com.client.util.Iterator(ob, %s)'
             1678  LOAD_FAST                'resultCLSID'
             1680  BINARY_MODULO    
             1682  LOAD_FAST                'stream'
             1684  LOAD_CONST               ('file',)
             1686  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1688  POP_TOP          

 L. 530      1690  LOAD_FAST                'specialItems'
             1692  LOAD_STR                 'item'
             1694  BINARY_SUBSCR    
         1696_1698  POP_JUMP_IF_FALSE  1798  'to 1798'

 L. 531      1700  LOAD_FAST                'specialItems'
             1702  LOAD_STR                 'item'
             1704  BINARY_SUBSCR    
             1706  UNPACK_SEQUENCE_3     3 
             1708  STORE_FAST               'entry'
             1710  STORE_FAST               'invoketype'
             1712  STORE_FAST               'propArgs'

 L. 532      1714  LOAD_FAST                'entry'
             1716  LOAD_METHOD              GetResultCLSIDStr
             1718  CALL_METHOD_0         0  ''
             1720  STORE_FAST               'resultCLSID'

 L. 533      1722  LOAD_GLOBAL              print
             1724  LOAD_STR                 '\t#This class has Item property/method which allows indexed access with the object[key] syntax.'
             1726  LOAD_FAST                'stream'
             1728  LOAD_CONST               ('file',)
             1730  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1732  POP_TOP          

 L. 534      1734  LOAD_GLOBAL              print
             1736  LOAD_STR                 '\t#Some objects will accept a string or other type of key in addition to integers.'
             1738  LOAD_FAST                'stream'
             1740  LOAD_CONST               ('file',)
             1742  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1744  POP_TOP          

 L. 535      1746  LOAD_GLOBAL              print
             1748  LOAD_STR                 '\t#Note that many Office objects do not use zero-based indexing.'
             1750  LOAD_FAST                'stream'
             1752  LOAD_CONST               ('file',)
             1754  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1756  POP_TOP          

 L. 536      1758  LOAD_GLOBAL              print
             1760  LOAD_STR                 '\tdef __getitem__(self, key):'
             1762  LOAD_FAST                'stream'
             1764  LOAD_CONST               ('file',)
             1766  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1768  POP_TOP          

 L. 537      1770  LOAD_GLOBAL              print
             1772  LOAD_STR                 '\t\treturn self._get_good_object_(self._oleobj_.Invoke(*(%d, LCID, %d, 1, key)), "Item", %s)'

 L. 538      1774  LOAD_FAST                'entry'
             1776  LOAD_ATTR                desc
             1778  LOAD_CONST               0
             1780  BINARY_SUBSCR    
             1782  LOAD_FAST                'invoketype'
             1784  LOAD_FAST                'resultCLSID'
             1786  BUILD_TUPLE_3         3 

 L. 537      1788  BINARY_MODULO    

 L. 538      1790  LOAD_FAST                'stream'

 L. 537      1792  LOAD_CONST               ('file',)
             1794  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1796  POP_TOP          
           1798_0  COME_FROM          1696  '1696'

 L. 540      1798  LOAD_FAST                'specialItems'
             1800  LOAD_STR                 'count'
             1802  BINARY_SUBSCR    
         1804_1806  POP_JUMP_IF_FALSE  1940  'to 1940'

 L. 541      1808  LOAD_FAST                'specialItems'
             1810  LOAD_STR                 'count'
             1812  BINARY_SUBSCR    
             1814  UNPACK_SEQUENCE_3     3 
             1816  STORE_FAST               'entry'
             1818  STORE_FAST               'invoketype'
             1820  STORE_FAST               'propArgs'

 L. 542      1822  LOAD_FAST                'propArgs'
             1824  LOAD_CONST               None
             1826  COMPARE_OP               is
         1828_1830  POP_JUMP_IF_FALSE  1850  'to 1850'

 L. 543      1832  LOAD_STR                 'method'
             1834  STORE_FAST               'typename'

 L. 544      1836  LOAD_FAST                'self'
             1838  LOAD_METHOD              MakeFuncMethod
             1840  LOAD_FAST                'entry'
             1842  LOAD_STR                 '__len__'
             1844  CALL_METHOD_2         2  ''
             1846  STORE_FAST               'ret'
             1848  JUMP_FORWARD       1864  'to 1864'
           1850_0  COME_FROM          1828  '1828'

 L. 546      1850  LOAD_STR                 'property'
             1852  STORE_FAST               'typename'

 L. 547      1854  LOAD_STR                 '\tdef __len__(self):\n\t\treturn self._ApplyTypes_(*%s)'
             1856  LOAD_FAST                'propArgs'
             1858  BINARY_MODULO    
             1860  BUILD_LIST_1          1 
             1862  STORE_FAST               'ret'
           1864_0  COME_FROM          1848  '1848'

 L. 548      1864  LOAD_GLOBAL              print
             1866  LOAD_STR                 '\t#This class has Count() %s - allow len(ob) to provide this'
             1868  LOAD_FAST                'typename'
             1870  BINARY_MODULO    
             1872  LOAD_FAST                'stream'
             1874  LOAD_CONST               ('file',)
             1876  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1878  POP_TOP          

 L. 549      1880  LOAD_FAST                'ret'
             1882  GET_ITER         
             1884  FOR_ITER           1904  'to 1904'
             1886  STORE_FAST               'line'

 L. 550      1888  LOAD_GLOBAL              print
             1890  LOAD_FAST                'line'
             1892  LOAD_FAST                'stream'
             1894  LOAD_CONST               ('file',)
             1896  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1898  POP_TOP          
         1900_1902  JUMP_BACK          1884  'to 1884'

 L. 552      1904  LOAD_GLOBAL              print
             1906  LOAD_STR                 "\t#This class has a __len__ - this is needed so 'if object:' always returns TRUE."
             1908  LOAD_FAST                'stream'
             1910  LOAD_CONST               ('file',)
             1912  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1914  POP_TOP          

 L. 553      1916  LOAD_GLOBAL              print
             1918  LOAD_STR                 '\tdef __nonzero__(self):'
             1920  LOAD_FAST                'stream'
             1922  LOAD_CONST               ('file',)
             1924  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1926  POP_TOP          

 L. 554      1928  LOAD_GLOBAL              print
             1930  LOAD_STR                 '\t\treturn True'
             1932  LOAD_FAST                'stream'
             1934  LOAD_CONST               ('file',)
             1936  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1938  POP_TOP          
           1940_0  COME_FROM          1804  '1804'

Parse error at or near `JUMP_FORWARD' instruction at offset 170


class CoClassItem(build.OleItem, WritableItem):
    order = 5
    typename = 'COCLASS'

    def __init__(self, typeinfo, attr, doc=None, sources=[], interfaces=[], bForUser=1):
        build.OleItem.__init__(self, doc)
        self.clsid = attr[0]
        self.sources = sources
        self.interfaces = interfaces
        self.bIsDispatch = 1

    def WriteClass(self, generator):
        generator.checkWriteCoClassBaseClass()
        doc = self.doc
        stream = generator.file
        if generator.generate_type == GEN_DEMAND_CHILD:
            referenced_items = []
            for ref, flag in self.sources:
                referenced_items.append(ref)
            else:
                for ref, flag in self.interfaces:
                    referenced_items.append(ref)
                else:
                    print('import sys', file=stream)
                    for ref in referenced_items:
                        print(("__import__('%s.%s')" % (generator.base_mod_name, ref.python_name)), file=stream)
                        print(("%s = sys.modules['%s.%s'].%s" % (ref.python_name, generator.base_mod_name, ref.python_name, ref.python_name)), file=stream)
                        ref.bWritten = 1

        try:
            progId = pythoncom.ProgIDFromCLSID(self.clsid)
            print(("# This CoClass is known by the name '%s'" % progId), file=stream)
        except pythoncom.com_error:
            pass
        else:
            print(('class %s(CoClassBaseClass): # A CoClass' % self.python_name), file=stream)
            if doc:
                if doc[1]:
                    print(('\t# ' + doc[1]), file=stream)
            print(('\tCLSID = %r' % (self.clsid,)), file=stream)
            print('\tcoclass_sources = [', file=stream)
            defItem = None
        for item, flag in self.sources:
            if flag & pythoncom.IMPLTYPEFLAG_FDEFAULT:
                defItem = item
            elif item.bWritten:
                key = item.python_name
            else:
                key = repr(str(item.clsid))
            print(('\t\t%s,' % key), file=stream)
        else:
            print('\t]', file=stream)
            if defItem:
                if defItem.bWritten:
                    defName = defItem.python_name
                else:
                    defName = repr(str(defItem.clsid))
                print(('\tdefault_source = %s' % (defName,)), file=stream)
            print('\tcoclass_interfaces = [', file=stream)
            defItem = None
            for item, flag in self.interfaces:
                if flag & pythoncom.IMPLTYPEFLAG_FDEFAULT:
                    defItem = item
                elif item.bWritten:
                    key = item.python_name
                else:
                    key = repr(str(item.clsid))
                print(('\t\t%s,' % (key,)), file=stream)
            else:
                print('\t]', file=stream)
                if defItem:
                    if defItem.bWritten:
                        defName = defItem.python_name
                    else:
                        defName = repr(str(defItem.clsid))
                    print(('\tdefault_interface = %s' % (defName,)), file=stream)
                self.bWritten = 1
                print(file=stream)


class GeneratorProgress:

    def __init__(self):
        pass

    def Starting(self, tlb_desc):
        """Called when the process starts.
        """
        self.tlb_desc = tlb_desc

    def Finished(self):
        """Called when the process is complete.
        """
        pass

    def SetDescription(self, desc, maxticks=None):
        """We are entering a major step.  If maxticks, then this
        is how many ticks we expect to make until finished
        """
        pass

    def Tick(self, desc=None):
        """Minor progress step.  Can provide new description if necessary
        """
        pass

    def VerboseProgress(self, desc):
        """Verbose/Debugging output.
        """
        pass

    def LogWarning(self, desc):
        """If a warning is generated
        """
        pass

    def LogBeginGenerate(self, filename):
        pass

    def Close(self):
        pass


class Generator:

    def __init__(self, typelib, sourceFilename, progressObject, bBuildHidden=1, bUnicodeToString=None):
        assert bUnicodeToString is None, 'this is deprecated and will go away'
        self.bHaveWrittenDispatchBaseClass = 0
        self.bHaveWrittenCoClassBaseClass = 0
        self.bHaveWrittenEventBaseClass = 0
        self.typelib = typelib
        self.sourceFilename = sourceFilename
        self.bBuildHidden = bBuildHidden
        self.progress = progressObject
        self.file = None

    def CollectOleItemInfosFromType(self):
        ret = []
        for i in range(self.typelib.GetTypeInfoCount()):
            info = self.typelib.GetTypeInfo(i)
            infotype = self.typelib.GetTypeInfoType(i)
            doc = self.typelib.GetDocumentation(i)
            attr = info.GetTypeAttr()
            ret.append((info, infotype, doc, attr))
        else:
            return ret

    def _Build_CoClass--- This code section failed: ---

 L. 676         0  LOAD_FAST                'type_info_tuple'
                2  UNPACK_SEQUENCE_4     4 
                4  STORE_FAST               'info'
                6  STORE_FAST               'infotype'
                8  STORE_FAST               'doc'
               10  STORE_FAST               'attr'

 L. 678        12  BUILD_LIST_0          0 
               14  STORE_FAST               'child_infos'

 L. 679        16  LOAD_GLOBAL              range
               18  LOAD_FAST                'attr'
               20  LOAD_CONST               8
               22  BINARY_SUBSCR    
               24  CALL_FUNCTION_1       1  ''
               26  GET_ITER         
               28  FOR_ITER            130  'to 130'
               30  STORE_FAST               'j'

 L. 680        32  LOAD_FAST                'info'
               34  LOAD_METHOD              GetImplTypeFlags
               36  LOAD_FAST                'j'
               38  CALL_METHOD_1         1  ''
               40  STORE_FAST               'flags'

 L. 681        42  SETUP_FINALLY        64  'to 64'

 L. 682        44  LOAD_FAST                'info'
               46  LOAD_METHOD              GetRefTypeInfo
               48  LOAD_FAST                'info'
               50  LOAD_METHOD              GetRefTypeOfImplType
               52  LOAD_FAST                'j'
               54  CALL_METHOD_1         1  ''
               56  CALL_METHOD_1         1  ''
               58  STORE_FAST               'refType'
               60  POP_BLOCK        
               62  JUMP_FORWARD         90  'to 90'
             64_0  COME_FROM_FINALLY    42  '42'

 L. 683        64  DUP_TOP          
               66  LOAD_GLOBAL              pythoncom
               68  LOAD_ATTR                com_error
               70  COMPARE_OP               exception-match
               72  POP_JUMP_IF_FALSE    88  'to 88'
               74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          

 L. 685        80  POP_EXCEPT       
               82  JUMP_BACK            28  'to 28'
               84  POP_EXCEPT       
               86  JUMP_FORWARD         90  'to 90'
             88_0  COME_FROM            72  '72'
               88  END_FINALLY      
             90_0  COME_FROM            86  '86'
             90_1  COME_FROM            62  '62'

 L. 686        90  LOAD_FAST                'refType'
               92  LOAD_METHOD              GetTypeAttr
               94  CALL_METHOD_0         0  ''
               96  STORE_FAST               'refAttr'

 L. 687        98  LOAD_FAST                'child_infos'
              100  LOAD_METHOD              append
              102  LOAD_FAST                'info'
              104  LOAD_FAST                'refAttr'
              106  LOAD_ATTR                typekind
              108  LOAD_FAST                'refType'
              110  LOAD_FAST                'refType'
              112  LOAD_METHOD              GetDocumentation
              114  LOAD_CONST               -1
              116  CALL_METHOD_1         1  ''
              118  LOAD_FAST                'refAttr'
              120  LOAD_FAST                'flags'
              122  BUILD_TUPLE_6         6 
              124  CALL_METHOD_1         1  ''
              126  POP_TOP          
              128  JUMP_BACK            28  'to 28'

 L. 690       130  LOAD_GLOBAL              CoClassItem
              132  LOAD_FAST                'info'
              134  LOAD_FAST                'attr'
              136  LOAD_FAST                'doc'
              138  CALL_FUNCTION_3       3  ''
              140  STORE_FAST               'newItem'

 L. 691       142  LOAD_FAST                'newItem'
              144  LOAD_FAST                'child_infos'
              146  BUILD_TUPLE_2         2 
              148  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 84

    def _Build_CoClassChildren(self, coclass, coclass_info, oleItems, vtableItems):
        sources = {}
        interfaces = {}
        for info, info_type, refType, doc, refAttr, flags in coclass_info:
            if not refAttr.typekind == pythoncom.TKIND_DISPATCH:
                if refAttr.typekind == pythoncom.TKIND_INTERFACE:
                    if refAttr[11] & pythoncom.TYPEFLAG_FDISPATCHABLE:
                        clsid = refAttr[0]
                        if clsid in oleItems:
                            dispItem = oleItems[clsid]
                        else:
                            dispItem = DispatchItem(refType, refAttr, doc)
                            oleItems[dispItem.clsid] = dispItem
                        dispItem.coclass_clsid = coclass.clsid
                        if flags & pythoncom.IMPLTYPEFLAG_FSOURCE:
                            dispItem.bIsSink = 1
                            sources[dispItem.clsid] = (dispItem, flags)
                        else:
                            interfaces[dispItem.clsid] = (
                             dispItem, flags)
                    if clsid not in vtableItems:
                        if refAttr[11] & pythoncom.TYPEFLAG_FDUAL:
                            refType = refType.GetRefTypeInfo(refType.GetRefTypeOfImplType(-1))
                            refAttr = refType.GetTypeAttr()
                            assert refAttr.typekind == pythoncom.TKIND_INTERFACE, 'must be interface bynow!'
                            vtableItem = VTableItem(refType, refAttr, doc)
                            vtableItems[clsid] = vtableItem
                        coclass.sources = list(sources.values())
                        coclass.interfaces = list(interfaces.values())

    def _Build_Interface(self, type_info_tuple):
        info, infotype, doc, attr = type_info_tuple
        oleItem = vtableItem = None
        if (infotype == pythoncom.TKIND_DISPATCH or infotype) == pythoncom.TKIND_INTERFACE:
            if attr[11] & pythoncom.TYPEFLAG_FDISPATCHABLE:
                oleItem = DispatchItem(info, attr, doc)
                if attr.wTypeFlags & pythoncom.TYPEFLAG_FDUAL:
                    refhtype = info.GetRefTypeOfImplType(-1)
                    info = info.GetRefTypeInfo(refhtype)
                    attr = info.GetTypeAttr()
                    infotype = pythoncom.TKIND_INTERFACE
                else:
                    infotype = None
        assert infotype in (None, pythoncom.TKIND_INTERFACE), 'Must be a real interface at this point'
        if infotype == pythoncom.TKIND_INTERFACE:
            vtableItem = VTableItem(info, attr, doc)
        return (
         oleItem, vtableItem)

    def BuildOleItemsFromType(self):
        assert self.bBuildHidden, 'This code doesnt look at the hidden flag - I thought everyone set it true!?!?!'
        oleItems = {}
        enumItems = {}
        recordItems = {}
        vtableItems = {}
        for type_info_tuple in self.CollectOleItemInfosFromType():
            info, infotype, doc, attr = type_info_tuple
            clsid = attr[0]
            if infotype == pythoncom.TKIND_ENUM or infotype == pythoncom.TKIND_MODULE:
                newItem = EnumerationItem(info, attr, doc)
                enumItems[newItem.doc[0]] = newItem
            elif infotype in (pythoncom.TKIND_DISPATCH, pythoncom.TKIND_INTERFACE):
                if clsid not in oleItems:
                    oleItem, vtableItem = self._Build_Interface(type_info_tuple)
                    oleItems[clsid] = oleItem
                    if vtableItem is not None:
                        vtableItems[clsid] = vtableItem
                elif infotype == pythoncom.TKIND_RECORD or infotype == pythoncom.TKIND_UNION:
                    newItem = RecordItem(info, attr, doc)
                    recordItems[newItem.clsid] = newItem
                elif infotype == pythoncom.TKIND_ALIAS:
                    continue
            elif infotype == pythoncom.TKIND_COCLASS:
                newItem, child_infos = self._Build_CoClass(type_info_tuple)
                self._Build_CoClassChildren(newItem, child_infos, oleItems, vtableItems)
                oleItems[newItem.clsid] = newItem
            else:
                self.progress.LogWarning('Unknown TKIND found: %d' % infotype)
        else:
            return (
             oleItems, enumItems, recordItems, vtableItems)

    def open_writer(self, filename, encoding='mbcs'):
        try:
            os.unlink(filename)
        except os.error:
            pass
        else:
            filename = filename + '.temp'
            if sys.version_info > (3, 0):
                ret = open(filename, 'wt', encoding=encoding)
            else:
                import codecs
                ret = codecs.open(filename, 'w', encoding)
            return ret

    def finish_writer(self, filename, f, worked):
        f.close()
        if worked:
            os.rename(filename + '.temp', filename)
        else:
            os.unlink(filename + '.temp')

    def generate(self, file, is_for_demand=0):
        if is_for_demand:
            self.generate_type = GEN_DEMAND_BASE
        else:
            self.generate_type = GEN_FULL
        self.file = file
        self.do_generate()
        self.file = None
        self.progress.Finished()

    def do_gen_file_header(self):
        la = self.typelib.GetLibAttr()
        moduleDoc = self.typelib.GetDocumentation(-1)
        docDesc = ''
        if moduleDoc[1]:
            docDesc = moduleDoc[1]
        self.bHaveWrittenDispatchBaseClass = 0
        self.bHaveWrittenCoClassBaseClass = 0
        self.bHaveWrittenEventBaseClass = 0
        assert self.file.encoding, self.file
        encoding = self.file.encoding
        print(('# -*- coding: %s -*-' % (encoding,)), file=(self.file))
        print(('# Created by makepy.py version %s' % (makepy_version,)), file=(self.file))
        print(('# By python version %s' % (
         sys.version.replace('\n', '-'),)),
          file=(self.file))
        if self.sourceFilename:
            print(("# From type library '%s'" % (os.path.split(self.sourceFilename)[1],)), file=(self.file))
        print(('# On %s' % time.ctime(time.time())), file=(self.file))
        print((build._makeDocString(docDesc)), file=(self.file))
        print('makepy_version =', (repr(makepy_version)), file=(self.file))
        print(('python_version = 0x%x' % (sys.hexversion,)), file=(self.file))
        print(file=(self.file))
        print('import win32com.client.CLSIDToClass, pythoncom, pywintypes', file=(self.file))
        print('import win32com.client.util', file=(self.file))
        print('from pywintypes import IID', file=(self.file))
        print('from win32com.client import Dispatch', file=(self.file))
        print(file=(self.file))
        print('# The following 3 lines may need tweaking for the particular server', file=(self.file))
        print('# Candidates are pythoncom.Missing, .Empty and .ArgNotFound', file=(self.file))
        print('defaultNamedOptArg=pythoncom.Empty', file=(self.file))
        print('defaultNamedNotOptArg=pythoncom.Empty', file=(self.file))
        print('defaultUnnamedArg=pythoncom.Empty', file=(self.file))
        print(file=(self.file))
        print(('CLSID = ' + repr(la[0])), file=(self.file))
        print(('MajorVersion = ' + str(la[3])), file=(self.file))
        print(('MinorVersion = ' + str(la[4])), file=(self.file))
        print(('LibraryFlags = ' + str(la[5])), file=(self.file))
        print(('LCID = ' + hex(la[1])), file=(self.file))
        print(file=(self.file))

    def do_generate(self):
        moduleDoc = self.typelib.GetDocumentation(-1)
        stream = self.file
        docDesc = ''
        if moduleDoc[1]:
            docDesc = moduleDoc[1]
        else:
            self.progress.Starting(docDesc)
            self.progress.SetDescription('Building definitions from type library...')
            self.do_gen_file_header()
            oleItems, enumItems, recordItems, vtableItems = self.BuildOleItemsFromType()
            self.progress.SetDescription('Generating...', len(oleItems) + len(enumItems) + len(vtableItems))
            if enumItems:
                print('class constants:', file=stream)
                items = list(enumItems.values())
                items.sort()
                num_written = 0
                for oleitem in items:
                    num_written += oleitem.WriteEnumerationItems(stream)
                    self.progress.Tick()
                else:
                    if not num_written:
                        print('\tpass', file=stream)
                    print(file=stream)

            if self.generate_type == GEN_FULL:
                items = [l for l in oleItems.values() if l is not None]
                items.sort()
                for oleitem in items:
                    self.progress.Tick()
                    oleitem.WriteClass(self)
                else:
                    items = list(vtableItems.values())
                    items.sort()
                    for oleitem in items:
                        self.progress.Tick()
                        oleitem.WriteClass(self)

            else:
                self.progress.Tick(len(oleItems) + len(vtableItems))
        print('RecordMap = {', file=stream)
        for record in recordItems.values():
            if record.clsid == pythoncom.IID_NULL:
                print(("\t###%s: %s, # Record disabled because it doesn't have a non-null GUID" % (repr(record.doc[0]), repr(str(record.clsid)))), file=stream)
            else:
                print(('\t%s: %s,' % (repr(record.doc[0]), repr(str(record.clsid)))), file=stream)
        else:
            print('}', file=stream)
            print(file=stream)
            if self.generate_type == GEN_FULL:
                print('CLSIDToClassMap = {', file=stream)
                for item in oleItems.values():
                    if item is not None:
                        if item.bWritten:
                            print(("\t'%s' : %s," % (str(item.clsid), item.python_name)), file=stream)
                        print('}', file=stream)
                        print('CLSIDToPackageMap = {}', file=stream)
                        print('win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )', file=stream)
                        print('VTablesToPackageMap = {}', file=stream)
                        print('VTablesToClassMap = {', file=stream)
                        for item in vtableItems.values():
                            print(("\t'%s' : '%s'," % (item.clsid, item.python_name)), file=stream)
                        else:
                            print('}', file=stream)
                            print(file=stream)

            else:
                print('CLSIDToClassMap = {}', file=stream)
                print('CLSIDToPackageMap = {', file=stream)
                for item in oleItems.values():
                    if item is not None:
                        print(("\t'%s' : %s," % (str(item.clsid), repr(item.python_name))), file=stream)
                    print('}', file=stream)
                    print('VTablesToClassMap = {}', file=stream)
                    print('VTablesToPackageMap = {', file=stream)
                    for item in vtableItems.values():
                        print(("\t'%s' : '%s'," % (item.clsid, item.python_name)), file=stream)
                    else:
                        print('}', file=stream)
                        print(file=stream)

            print(file=stream)
            map = {}
            for item in oleItems.values():
                if item is not None:
                    map[item.python_name] = isinstance(item, CoClassItem) or item.clsid

        for item in vtableItems.values():
            map[item.python_name] = item.clsid
        else:
            print('NamesToIIDMap = {', file=stream)
            for name, iid in map.items():
                print(("\t'%s' : '%s'," % (name, iid)), file=stream)
            else:
                print('}', file=stream)
                print(file=stream)
                if enumItems:
                    print('win32com.client.constants.__dicts__.append(constants.__dict__)', file=stream)
                print(file=stream)

    def generate_child(self, child, dir):
        """Generate a single child.  May force a few children to be built as we generate deps"""
        self.generate_type = GEN_DEMAND_CHILD
        la = self.typelib.GetLibAttr()
        lcid = la[1]
        clsid = la[0]
        major = la[3]
        minor = la[4]
        self.base_mod_name = 'win32com.gen_py.' + str(clsid)[1:-1] + 'x%sx%sx%s' % (lcid, major, minor)
        try:
            oleItems = {}
            vtableItems = {}
            infos = self.CollectOleItemInfosFromType()
            found = 0
            for type_info_tuple in infos:
                info, infotype, doc, attr = type_info_tuple
                if infotype == pythoncom.TKIND_COCLASS:
                    coClassItem, child_infos = self._Build_CoClass(type_info_tuple)
                    found = build.MakePublicAttributeName(doc[0]) == child
                    if not found:
                        for info, info_type, refType, doc, refAttr, flags in child_infos:
                            if build.MakePublicAttributeName(doc[0]) == child:
                                found = 1
                                break

            else:
                if found:
                    oleItems[coClassItem.clsid] = coClassItem
                    self._Build_CoClassChildren(coClassItem, child_infos, oleItems, vtableItems)
                    break

            for type_info_tuple in found or infos:
                info, infotype, doc, attr = type_info_tuple
                if infotype in (pythoncom.TKIND_INTERFACE, pythoncom.TKIND_DISPATCH) and build.MakePublicAttributeName(doc[0]) == child:
                    found = 1
                    oleItem, vtableItem = self._Build_Interface(type_info_tuple)
                    oleItems[clsid] = oleItem
                    if vtableItem is not None:
                        vtableItems[clsid] = vtableItem
            else:
                assert found, "Cant find the '%s' interface in the CoClasses, or the interfaces" % (child,)
                items = {}

            for key, value in oleItems.items():
                items[key] = (
                 value, None)
            else:
                for key, value in vtableItems.items():
                    existing = items.get(key, None)
                    if existing is not None:
                        new_val = (
                         existing[0], value)
                    else:
                        new_val = (
                         None, value)
                    items[key] = new_val
                else:
                    self.progress.SetDescription('Generating...', len(items))
                    for oleitem, vtableitem in items.values():
                        an_item = oleitem or vtableitem
                        if self.file:
                            raise AssertionError('already have a file?')
                        out_name = os.path.join(dir, an_item.python_name) + '.py'
                        worked = False
                        self.file = self.open_writer(out_name)
                        try:
                            if oleitem is not None:
                                self.do_gen_child_item(oleitem)
                            if vtableitem is not None:
                                self.do_gen_child_item(vtableitem)
                            self.progress.Tick()
                            worked = True
                        finally:
                            self.finish_writer(out_name, self.file, worked)
                            self.file = None

        finally:
            self.progress.Finished()

    def do_gen_child_item(self, oleitem):
        moduleDoc = self.typelib.GetDocumentation(-1)
        docDesc = ''
        if moduleDoc[1]:
            docDesc = moduleDoc[1]
        self.progress.Starting(docDesc)
        self.progress.SetDescription('Building definitions from type library...')
        self.do_gen_file_header()
        oleitem.WriteClass(self)
        if oleitem.bWritten:
            print(('win32com.client.CLSIDToClass.RegisterCLSID( "%s", %s )' % (oleitem.clsid, oleitem.python_name)), file=(self.file))

    def checkWriteDispatchBaseClass(self):
        if not self.bHaveWrittenDispatchBaseClass:
            print('from win32com.client import DispatchBaseClass', file=(self.file))
            self.bHaveWrittenDispatchBaseClass = 1

    def checkWriteCoClassBaseClass(self):
        if not self.bHaveWrittenCoClassBaseClass:
            print('from win32com.client import CoClassBaseClass', file=(self.file))
            self.bHaveWrittenCoClassBaseClass = 1

    def checkWriteEventBaseClass(self):
        if not self.bHaveWrittenEventBaseClass:
            self.bHaveWrittenEventBaseClass = 1


if __name__ == '__main__':
    print('This is a worker module.  Please use makepy to generate Python files.')