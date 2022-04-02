# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
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

def MakeDefaultArgsForPropertyPut--- This code section failed: ---

 L.  61         0  BUILD_LIST_0          0 
                2  STORE_FAST               'ret'

 L.  62         4  LOAD_FAST                'argsDesc'
                6  LOAD_CONST               1
                8  LOAD_CONST               None
               10  BUILD_SLICE_2         2 
               12  BINARY_SUBSCR    
               14  GET_ITER         
               16  FOR_ITER             54  'to 54'
               18  STORE_FAST               'desc'

 L.  63        20  LOAD_GLOBAL              build
               22  LOAD_METHOD              MakeDefaultArgRepr
               24  LOAD_FAST                'desc'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'default'

 L.  64        30  LOAD_FAST                'default'
               32  LOAD_CONST               None
               34  <117>                 0  ''
               36  POP_JUMP_IF_FALSE    42  'to 42'

 L.  65        38  POP_TOP          
               40  BREAK_LOOP           54  'to 54'
             42_0  COME_FROM            36  '36'

 L.  66        42  LOAD_FAST                'ret'
               44  LOAD_METHOD              append
               46  LOAD_FAST                'default'
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          
               52  JUMP_BACK            16  'to 16'

 L.  67        54  LOAD_GLOBAL              tuple
               56  LOAD_FAST                'ret'
               58  CALL_FUNCTION_1       1  ''
               60  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 34


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
        print(('\t\t%9d : "%s",' % (fdesc.memid, MakeEventMethodName(entry.names[0]))), file=stream)
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
            alinfo = typeinfo.GetRefTypeInfohref
            self.aliasDoc = alinfo.GetDocumentation(-1)
            self.aliasAttr = alinfo.GetTypeAttr()
        else:
            self.aliasDoc = None
            self.aliasAttr = None

    def WriteAliasItem--- This code section failed: ---

 L. 154         0  LOAD_FAST                'self'
                2  LOAD_ATTR                bWritten
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L. 155         6  LOAD_CONST               None
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 157        10  LOAD_FAST                'self'
               12  LOAD_ATTR                aliasDoc
               14  POP_JUMP_IF_FALSE    78  'to 78'

 L. 158        16  LOAD_FAST                'self'
               18  LOAD_ATTR                aliasDoc
               20  LOAD_CONST               0
               22  BINARY_SUBSCR    
               24  STORE_FAST               'depName'

 L. 159        26  LOAD_FAST                'depName'
               28  LOAD_FAST                'aliasDict'
               30  <118>                 0  ''
               32  POP_JUMP_IF_FALSE    50  'to 50'

 L. 160        34  LOAD_FAST                'aliasDict'
               36  LOAD_FAST                'depName'
               38  BINARY_SUBSCR    
               40  LOAD_METHOD              WriteAliasItem
               42  LOAD_FAST                'aliasDict'
               44  LOAD_FAST                'stream'
               46  CALL_METHOD_2         2  ''
               48  POP_TOP          
             50_0  COME_FROM            32  '32'

 L. 161        50  LOAD_GLOBAL              print
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                doc
               56  LOAD_CONST               0
               58  BINARY_SUBSCR    
               60  LOAD_STR                 ' = '
               62  BINARY_ADD       
               64  LOAD_FAST                'depName'
               66  BINARY_ADD       
               68  LOAD_FAST                'stream'
               70  LOAD_CONST               ('file',)
               72  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               74  POP_TOP          
               76  JUMP_FORWARD        192  'to 192'
             78_0  COME_FROM            14  '14'

 L. 163        78  LOAD_FAST                'self'
               80  LOAD_ATTR                attr
               82  LOAD_CONST               14
               84  BINARY_SUBSCR    
               86  STORE_FAST               'ai'

 L. 164        88  LOAD_GLOBAL              type
               90  LOAD_FAST                'ai'
               92  CALL_FUNCTION_1       1  ''
               94  LOAD_GLOBAL              type
               96  LOAD_CONST               0
               98  CALL_FUNCTION_1       1  ''
              100  COMPARE_OP               ==
              102  POP_JUMP_IF_FALSE   192  'to 192'

 L. 165       104  SETUP_FINALLY       144  'to 144'

 L. 166       106  LOAD_GLOBAL              mapVTToTypeString
              108  LOAD_FAST                'ai'
              110  BINARY_SUBSCR    
              112  STORE_FAST               'typeStr'

 L. 167       114  LOAD_GLOBAL              print
              116  LOAD_STR                 '# %s=%s'
              118  LOAD_FAST                'self'
              120  LOAD_ATTR                doc
              122  LOAD_CONST               0
              124  BINARY_SUBSCR    
              126  LOAD_FAST                'typeStr'
              128  BUILD_TUPLE_2         2 
              130  BINARY_MODULO    
              132  LOAD_FAST                'stream'
              134  LOAD_CONST               ('file',)
              136  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              138  POP_TOP          
              140  POP_BLOCK        
              142  JUMP_FORWARD        192  'to 192'
            144_0  COME_FROM_FINALLY   104  '104'

 L. 168       144  DUP_TOP          
              146  LOAD_GLOBAL              KeyError
              148  <121>               190  ''
              150  POP_TOP          
              152  POP_TOP          
              154  POP_TOP          

 L. 169       156  LOAD_GLOBAL              print
              158  LOAD_FAST                'self'
              160  LOAD_ATTR                doc
              162  LOAD_CONST               0
              164  BINARY_SUBSCR    
              166  LOAD_STR                 " = None # Can't convert alias info "
              168  BINARY_ADD       
              170  LOAD_GLOBAL              str
              172  LOAD_FAST                'ai'
              174  CALL_FUNCTION_1       1  ''
              176  BINARY_ADD       
              178  LOAD_FAST                'stream'
              180  LOAD_CONST               ('file',)
              182  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              184  POP_TOP          
              186  POP_EXCEPT       
              188  JUMP_FORWARD        192  'to 192'
              190  <48>             
            192_0  COME_FROM           188  '188'
            192_1  COME_FROM           142  '142'
            192_2  COME_FROM           102  '102'
            192_3  COME_FROM            76  '76'

 L. 170       192  LOAD_GLOBAL              print
              194  LOAD_FAST                'stream'
              196  LOAD_CONST               ('file',)
              198  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              200  POP_TOP          

 L. 171       202  LOAD_CONST               1
              204  LOAD_FAST                'self'
              206  STORE_ATTR               bWritten

Parse error at or near `<118>' instruction at offset 30


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
            vdesc = typeinfo.GetVarDescj
            name = typeinfo.GetNamesvdesc[0][0]
            self.mapVars[name] = build.MapEntryvdesc

    def WriteEnumerationItems--- This code section failed: ---

 L. 197         0  LOAD_CONST               0
                2  STORE_FAST               'num'

 L. 198         4  LOAD_FAST                'self'
                6  LOAD_ATTR                doc
                8  LOAD_CONST               0
               10  BINARY_SUBSCR    
               12  STORE_FAST               'enumName'

 L. 200        14  LOAD_GLOBAL              list
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                mapVars
               20  LOAD_METHOD              keys
               22  CALL_METHOD_0         0  ''
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'names'

 L. 201        28  LOAD_FAST                'names'
               30  LOAD_METHOD              sort
               32  CALL_METHOD_0         0  ''
               34  POP_TOP          

 L. 202        36  LOAD_FAST                'names'
               38  GET_ITER         
             40_0  COME_FROM            72  '72'
               40  FOR_ITER            194  'to 194'
               42  STORE_FAST               'name'

 L. 203        44  LOAD_FAST                'self'
               46  LOAD_ATTR                mapVars
               48  LOAD_FAST                'name'
               50  BINARY_SUBSCR    
               52  STORE_FAST               'entry'

 L. 204        54  LOAD_FAST                'entry'
               56  LOAD_ATTR                desc
               58  STORE_FAST               'vdesc'

 L. 205        60  LOAD_FAST                'vdesc'
               62  LOAD_CONST               4
               64  BINARY_SUBSCR    
               66  LOAD_GLOBAL              pythoncom
               68  LOAD_ATTR                VAR_CONST
               70  COMPARE_OP               ==
               72  POP_JUMP_IF_FALSE    40  'to 40'

 L. 206        74  LOAD_FAST                'vdesc'
               76  LOAD_CONST               1
               78  BINARY_SUBSCR    
               80  STORE_FAST               'val'

 L. 208        82  LOAD_GLOBAL              repr
               84  LOAD_FAST                'val'
               86  CALL_FUNCTION_1       1  ''
               88  STORE_FAST               'use'

 L. 212        90  SETUP_FINALLY       108  'to 108'

 L. 213        92  LOAD_GLOBAL              compile
               94  LOAD_FAST                'use'
               96  LOAD_STR                 '<makepy>'
               98  LOAD_STR                 'eval'
              100  CALL_FUNCTION_3       3  ''
              102  POP_TOP          
              104  POP_BLOCK        
              106  JUMP_FORWARD        154  'to 154'
            108_0  COME_FROM_FINALLY    90  '90'

 L. 214       108  DUP_TOP          
              110  LOAD_GLOBAL              SyntaxError
              112  <121>               152  ''
              114  POP_TOP          
              116  POP_TOP          
              118  POP_TOP          

 L. 217       120  LOAD_FAST                'use'
              122  LOAD_METHOD              replace
              124  LOAD_STR                 '"'
              126  LOAD_STR                 "'"
              128  CALL_METHOD_2         2  ''
              130  STORE_FAST               'use'

 L. 218       132  LOAD_STR                 '"'
              134  LOAD_FAST                'use'
              136  BINARY_ADD       
              138  LOAD_STR                 '"'
              140  BINARY_ADD       
              142  LOAD_STR                 ' # This VARIANT type cannot be converted automatically'
              144  BINARY_ADD       
              146  STORE_FAST               'use'
              148  POP_EXCEPT       
              150  JUMP_FORWARD        154  'to 154'
              152  <48>             
            154_0  COME_FROM           150  '150'
            154_1  COME_FROM           106  '106'

 L. 219       154  LOAD_GLOBAL              print
              156  LOAD_STR                 '\t%-30s=%-10s # from enum %s'

 L. 220       158  LOAD_GLOBAL              build
              160  LOAD_METHOD              MakePublicAttributeName
              162  LOAD_FAST                'name'
              164  LOAD_CONST               True
              166  CALL_METHOD_2         2  ''
              168  LOAD_FAST                'use'
              170  LOAD_FAST                'enumName'
              172  BUILD_TUPLE_3         3 

 L. 219       174  BINARY_MODULO    

 L. 220       176  LOAD_FAST                'stream'

 L. 219       178  LOAD_CONST               ('file',)
              180  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              182  POP_TOP          

 L. 221       184  LOAD_FAST                'num'
              186  LOAD_CONST               1
              188  INPLACE_ADD      
              190  STORE_FAST               'num'
              192  JUMP_BACK            40  'to 40'

 L. 222       194  LOAD_FAST                'num'
              196  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 112


class VTableItem(build.VTableItem, WritableItem):
    order = 4

    def WriteClass(self, generator):
        self.WriteVTableMapgenerator
        self.bWritten = 1

    def WriteVTableMap--- This code section failed: ---

 L. 232         0  LOAD_FAST                'generator'
                2  LOAD_ATTR                file
                4  STORE_FAST               'stream'

 L. 233         6  LOAD_GLOBAL              print
                8  LOAD_STR                 '%s_vtables_dispatch_ = %d'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                python_name
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                bIsDispatch
               18  BUILD_TUPLE_2         2 
               20  BINARY_MODULO    
               22  LOAD_FAST                'stream'
               24  LOAD_CONST               ('file',)
               26  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               28  POP_TOP          

 L. 234        30  LOAD_GLOBAL              print
               32  LOAD_STR                 '%s_vtables_ = ['
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                python_name
               38  BUILD_TUPLE_1         1 
               40  BINARY_MODULO    
               42  LOAD_FAST                'stream'
               44  LOAD_CONST               ('file',)
               46  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               48  POP_TOP          

 L. 235        50  LOAD_FAST                'self'
               52  LOAD_ATTR                vtableFuncs
               54  GET_ITER         
            56_58  FOR_ITER            508  'to 508'
               60  STORE_FAST               'v'

 L. 236        62  LOAD_FAST                'v'
               64  UNPACK_SEQUENCE_3     3 
               66  STORE_FAST               'names'
               68  STORE_FAST               'dispid'
               70  STORE_FAST               'desc'

 L. 237        72  LOAD_FAST                'desc'
               74  LOAD_ATTR                desckind
               76  LOAD_GLOBAL              pythoncom
               78  LOAD_ATTR                DESCKIND_FUNCDESC
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_TRUE     88  'to 88'
               84  <74>             
               86  RAISE_VARARGS_1       1  'exception instance'
             88_0  COME_FROM            82  '82'

 L. 238        88  BUILD_LIST_0          0 
               90  STORE_FAST               'arg_reprs'

 L. 240        92  LOAD_CONST               0
               94  STORE_FAST               'item_num'

 L. 241        96  LOAD_GLOBAL              print
               98  LOAD_STR                 '\t(('
              100  LOAD_STR                 ' '
              102  LOAD_FAST                'stream'
              104  LOAD_CONST               ('end', 'file')
              106  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              108  POP_TOP          

 L. 242       110  LOAD_FAST                'names'
              112  GET_ITER         
            114_0  COME_FROM           156  '156'
              114  FOR_ITER            174  'to 174'
              116  STORE_FAST               'name'

 L. 243       118  LOAD_GLOBAL              print
              120  LOAD_GLOBAL              repr
              122  LOAD_FAST                'name'
              124  CALL_FUNCTION_1       1  ''
              126  LOAD_STR                 ','
              128  LOAD_STR                 ' '
              130  LOAD_FAST                'stream'
              132  LOAD_CONST               ('end', 'file')
              134  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              136  POP_TOP          

 L. 244       138  LOAD_FAST                'item_num'
              140  LOAD_CONST               1
              142  BINARY_ADD       
              144  STORE_FAST               'item_num'

 L. 245       146  LOAD_FAST                'item_num'
              148  LOAD_CONST               5
              150  BINARY_MODULO    
              152  LOAD_CONST               0
              154  COMPARE_OP               ==
              156  POP_JUMP_IF_FALSE   114  'to 114'

 L. 246       158  LOAD_GLOBAL              print
              160  LOAD_STR                 '\n\t\t\t'
              162  LOAD_STR                 ' '
              164  LOAD_FAST                'stream'
              166  LOAD_CONST               ('end', 'file')
              168  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              170  POP_TOP          
              172  JUMP_BACK           114  'to 114'

 L. 247       174  LOAD_GLOBAL              print
              176  LOAD_STR                 '), %d, (%r, %r, ['
              178  LOAD_FAST                'dispid'
              180  LOAD_FAST                'desc'
              182  LOAD_ATTR                memid
              184  LOAD_FAST                'desc'
              186  LOAD_ATTR                scodeArray
              188  BUILD_TUPLE_3         3 
              190  BINARY_MODULO    
              192  LOAD_STR                 ' '
              194  LOAD_FAST                'stream'
              196  LOAD_CONST               ('end', 'file')
              198  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              200  POP_TOP          

 L. 248       202  LOAD_FAST                'desc'
              204  LOAD_ATTR                args
              206  GET_ITER         
              208  FOR_ITER            326  'to 326'
              210  STORE_FAST               'arg'

 L. 249       212  LOAD_FAST                'item_num'
              214  LOAD_CONST               1
              216  BINARY_ADD       
              218  STORE_FAST               'item_num'

 L. 250       220  LOAD_FAST                'item_num'
              222  LOAD_CONST               5
              224  BINARY_MODULO    
              226  LOAD_CONST               0
              228  COMPARE_OP               ==
              230  POP_JUMP_IF_FALSE   246  'to 246'

 L. 251       232  LOAD_GLOBAL              print
              234  LOAD_STR                 '\n\t\t\t'
              236  LOAD_STR                 ' '
              238  LOAD_FAST                'stream'
              240  LOAD_CONST               ('end', 'file')
              242  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              244  POP_TOP          
            246_0  COME_FROM           230  '230'

 L. 252       246  LOAD_GLOBAL              build
              248  LOAD_METHOD              MakeDefaultArgRepr
              250  LOAD_FAST                'arg'
              252  CALL_METHOD_1         1  ''
              254  STORE_FAST               'defval'

 L. 253       256  LOAD_FAST                'arg'
              258  LOAD_CONST               3
              260  BINARY_SUBSCR    
              262  LOAD_CONST               None
              264  <117>                 0  ''
          266_268  POP_JUMP_IF_FALSE   276  'to 276'

 L. 254       270  LOAD_CONST               None
              272  STORE_FAST               'arg3_repr'
              274  JUMP_FORWARD        288  'to 288'
            276_0  COME_FROM           266  '266'

 L. 256       276  LOAD_GLOBAL              repr
              278  LOAD_FAST                'arg'
              280  LOAD_CONST               3
              282  BINARY_SUBSCR    
              284  CALL_FUNCTION_1       1  ''
              286  STORE_FAST               'arg3_repr'
            288_0  COME_FROM           274  '274'

 L. 257       288  LOAD_GLOBAL              print
              290  LOAD_GLOBAL              repr
              292  LOAD_FAST                'arg'
              294  LOAD_CONST               0
              296  BINARY_SUBSCR    
              298  LOAD_FAST                'arg'
              300  LOAD_CONST               1
              302  BINARY_SUBSCR    
              304  LOAD_FAST                'defval'
              306  LOAD_FAST                'arg3_repr'
              308  BUILD_TUPLE_4         4 
              310  CALL_FUNCTION_1       1  ''
              312  LOAD_STR                 ','
              314  LOAD_STR                 ' '
              316  LOAD_FAST                'stream'
              318  LOAD_CONST               ('end', 'file')
              320  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              322  POP_TOP          
              324  JUMP_BACK           208  'to 208'

 L. 258       326  LOAD_GLOBAL              print
              328  LOAD_STR                 '],'
              330  LOAD_STR                 ' '
              332  LOAD_FAST                'stream'
              334  LOAD_CONST               ('end', 'file')
              336  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              338  POP_TOP          

 L. 259       340  LOAD_GLOBAL              print
              342  LOAD_GLOBAL              repr
              344  LOAD_FAST                'desc'
              346  LOAD_ATTR                funckind
              348  CALL_FUNCTION_1       1  ''
              350  LOAD_STR                 ','
              352  LOAD_STR                 ' '
              354  LOAD_FAST                'stream'
              356  LOAD_CONST               ('end', 'file')
              358  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              360  POP_TOP          

 L. 260       362  LOAD_GLOBAL              print
              364  LOAD_GLOBAL              repr
              366  LOAD_FAST                'desc'
              368  LOAD_ATTR                invkind
              370  CALL_FUNCTION_1       1  ''
              372  LOAD_STR                 ','
              374  LOAD_STR                 ' '
              376  LOAD_FAST                'stream'
              378  LOAD_CONST               ('end', 'file')
              380  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              382  POP_TOP          

 L. 261       384  LOAD_GLOBAL              print
              386  LOAD_GLOBAL              repr
              388  LOAD_FAST                'desc'
              390  LOAD_ATTR                callconv
              392  CALL_FUNCTION_1       1  ''
              394  LOAD_STR                 ','
              396  LOAD_STR                 ' '
              398  LOAD_FAST                'stream'
              400  LOAD_CONST               ('end', 'file')
              402  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              404  POP_TOP          

 L. 262       406  LOAD_GLOBAL              print
              408  LOAD_GLOBAL              repr
              410  LOAD_FAST                'desc'
              412  LOAD_ATTR                cParamsOpt
              414  CALL_FUNCTION_1       1  ''
              416  LOAD_STR                 ','
              418  LOAD_STR                 ' '
              420  LOAD_FAST                'stream'
              422  LOAD_CONST               ('end', 'file')
              424  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              426  POP_TOP          

 L. 263       428  LOAD_GLOBAL              print
              430  LOAD_GLOBAL              repr
              432  LOAD_FAST                'desc'
              434  LOAD_ATTR                oVft
              436  CALL_FUNCTION_1       1  ''
              438  LOAD_STR                 ','
              440  LOAD_STR                 ' '
              442  LOAD_FAST                'stream'
              444  LOAD_CONST               ('end', 'file')
              446  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              448  POP_TOP          

 L. 264       450  LOAD_GLOBAL              print
              452  LOAD_GLOBAL              repr
              454  LOAD_FAST                'desc'
              456  LOAD_ATTR                rettype
              458  CALL_FUNCTION_1       1  ''
              460  LOAD_STR                 ','
              462  LOAD_STR                 ' '
              464  LOAD_FAST                'stream'
              466  LOAD_CONST               ('end', 'file')
              468  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              470  POP_TOP          

 L. 265       472  LOAD_GLOBAL              print
              474  LOAD_GLOBAL              repr
              476  LOAD_FAST                'desc'
              478  LOAD_ATTR                wFuncFlags
              480  CALL_FUNCTION_1       1  ''
              482  LOAD_STR                 ','
              484  LOAD_STR                 ' '
              486  LOAD_FAST                'stream'
              488  LOAD_CONST               ('end', 'file')
              490  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              492  POP_TOP          

 L. 266       494  LOAD_GLOBAL              print
              496  LOAD_STR                 ')),'
              498  LOAD_FAST                'stream'
              500  LOAD_CONST               ('file',)
              502  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              504  POP_TOP          
              506  JUMP_BACK            56  'to 56'

 L. 267       508  LOAD_GLOBAL              print
              510  LOAD_STR                 ']'
              512  LOAD_FAST                'stream'
              514  LOAD_CONST               ('file',)
              516  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              518  POP_TOP          

 L. 268       520  LOAD_GLOBAL              print
              522  LOAD_FAST                'stream'
              524  LOAD_CONST               ('file',)
              526  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              528  POP_TOP          

Parse error at or near `<74>' instruction at offset 84


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
            self.WriteEventSinkClassHeadergenerator
            self.WriteCallbackClassBodygenerator
        else:
            self.WriteClassHeadergenerator
            self.WriteClassBodygenerator
        print(file=(generator.file))
        self.bWritten = 1

    def WriteClassHeader--- This code section failed: ---

 L. 293         0  LOAD_FAST                'generator'
                2  LOAD_METHOD              checkWriteDispatchBaseClass
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 294         8  LOAD_FAST                'self'
               10  LOAD_ATTR                doc
               12  STORE_FAST               'doc'

 L. 295        14  LOAD_FAST                'generator'
               16  LOAD_ATTR                file
               18  STORE_FAST               'stream'

 L. 296        20  LOAD_GLOBAL              print
               22  LOAD_STR                 'class '
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                python_name
               28  BINARY_ADD       
               30  LOAD_STR                 '(DispatchBaseClass):'
               32  BINARY_ADD       
               34  LOAD_FAST                'stream'
               36  LOAD_CONST               ('file',)
               38  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               40  POP_TOP          

 L. 297        42  LOAD_FAST                'doc'
               44  LOAD_CONST               1
               46  BINARY_SUBSCR    
               48  POP_JUMP_IF_FALSE    76  'to 76'
               50  LOAD_GLOBAL              print
               52  LOAD_STR                 '\t'
               54  LOAD_GLOBAL              build
               56  LOAD_METHOD              _makeDocString
               58  LOAD_FAST                'doc'
               60  LOAD_CONST               1
               62  BINARY_SUBSCR    
               64  CALL_METHOD_1         1  ''
               66  BINARY_ADD       
               68  LOAD_FAST                'stream'
               70  LOAD_CONST               ('file',)
               72  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               74  POP_TOP          
             76_0  COME_FROM            48  '48'

 L. 298        76  SETUP_FINALLY       110  'to 110'

 L. 299        78  LOAD_GLOBAL              pythoncom
               80  LOAD_METHOD              ProgIDFromCLSID
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                clsid
               86  CALL_METHOD_1         1  ''
               88  STORE_FAST               'progId'

 L. 300        90  LOAD_GLOBAL              print
               92  LOAD_STR                 "\t# This class is creatable by the name '%s'"
               94  LOAD_FAST                'progId'
               96  BINARY_MODULO    
               98  LOAD_FAST                'stream'
              100  LOAD_CONST               ('file',)
              102  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              104  POP_TOP          
              106  POP_BLOCK        
              108  JUMP_FORWARD        130  'to 130'
            110_0  COME_FROM_FINALLY    76  '76'

 L. 301       110  DUP_TOP          
              112  LOAD_GLOBAL              pythoncom
              114  LOAD_ATTR                com_error
              116  <121>               128  ''
              118  POP_TOP          
              120  POP_TOP          
              122  POP_TOP          

 L. 302       124  POP_EXCEPT       
              126  JUMP_FORWARD        130  'to 130'
              128  <48>             
            130_0  COME_FROM           126  '126'
            130_1  COME_FROM           108  '108'

 L. 303       130  LOAD_GLOBAL              print
              132  LOAD_STR                 '\tCLSID = '
              134  LOAD_GLOBAL              repr
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                clsid
              140  CALL_FUNCTION_1       1  ''
              142  BINARY_ADD       
              144  LOAD_FAST                'stream'
              146  LOAD_CONST               ('file',)
              148  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              150  POP_TOP          

 L. 304       152  LOAD_FAST                'self'
              154  LOAD_ATTR                coclass_clsid
              156  LOAD_CONST               None
              158  <117>                 0  ''
              160  POP_JUMP_IF_FALSE   176  'to 176'

 L. 305       162  LOAD_GLOBAL              print
              164  LOAD_STR                 '\tcoclass_clsid = None'
              166  LOAD_FAST                'stream'
              168  LOAD_CONST               ('file',)
              170  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              172  POP_TOP          
              174  JUMP_FORWARD        198  'to 198'
            176_0  COME_FROM           160  '160'

 L. 307       176  LOAD_GLOBAL              print
              178  LOAD_STR                 '\tcoclass_clsid = '
              180  LOAD_GLOBAL              repr
              182  LOAD_FAST                'self'
              184  LOAD_ATTR                coclass_clsid
              186  CALL_FUNCTION_1       1  ''
              188  BINARY_ADD       
              190  LOAD_FAST                'stream'
              192  LOAD_CONST               ('file',)
              194  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              196  POP_TOP          
            198_0  COME_FROM           174  '174'

 L. 308       198  LOAD_GLOBAL              print
              200  LOAD_FAST                'stream'
              202  LOAD_CONST               ('file',)
              204  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              206  POP_TOP          

 L. 309       208  LOAD_CONST               1
              210  LOAD_FAST                'self'
              212  STORE_ATTR               bWritten

Parse error at or near `<121>' instruction at offset 116

    def WriteEventSinkClassHeader--- This code section failed: ---

 L. 312         0  LOAD_FAST                'generator'
                2  LOAD_METHOD              checkWriteEventBaseClass
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 313         8  LOAD_FAST                'self'
               10  LOAD_ATTR                doc
               12  STORE_FAST               'doc'

 L. 314        14  LOAD_FAST                'generator'
               16  LOAD_ATTR                file
               18  STORE_FAST               'stream'

 L. 315        20  LOAD_GLOBAL              print
               22  LOAD_STR                 'class '
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                python_name
               28  BINARY_ADD       
               30  LOAD_STR                 ':'
               32  BINARY_ADD       
               34  LOAD_FAST                'stream'
               36  LOAD_CONST               ('file',)
               38  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               40  POP_TOP          

 L. 316        42  LOAD_FAST                'doc'
               44  LOAD_CONST               1
               46  BINARY_SUBSCR    
               48  POP_JUMP_IF_FALSE    76  'to 76'
               50  LOAD_GLOBAL              print
               52  LOAD_STR                 '\t'
               54  LOAD_GLOBAL              build
               56  LOAD_METHOD              _makeDocString
               58  LOAD_FAST                'doc'
               60  LOAD_CONST               1
               62  BINARY_SUBSCR    
               64  CALL_METHOD_1         1  ''
               66  BINARY_ADD       
               68  LOAD_FAST                'stream'
               70  LOAD_CONST               ('file',)
               72  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               74  POP_TOP          
             76_0  COME_FROM            48  '48'

 L. 317        76  SETUP_FINALLY       110  'to 110'

 L. 318        78  LOAD_GLOBAL              pythoncom
               80  LOAD_METHOD              ProgIDFromCLSID
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                clsid
               86  CALL_METHOD_1         1  ''
               88  STORE_FAST               'progId'

 L. 319        90  LOAD_GLOBAL              print
               92  LOAD_STR                 "\t# This class is creatable by the name '%s'"
               94  LOAD_FAST                'progId'
               96  BINARY_MODULO    
               98  LOAD_FAST                'stream'
              100  LOAD_CONST               ('file',)
              102  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              104  POP_TOP          
              106  POP_BLOCK        
              108  JUMP_FORWARD        130  'to 130'
            110_0  COME_FROM_FINALLY    76  '76'

 L. 320       110  DUP_TOP          
              112  LOAD_GLOBAL              pythoncom
              114  LOAD_ATTR                com_error
              116  <121>               128  ''
              118  POP_TOP          
              120  POP_TOP          
              122  POP_TOP          

 L. 321       124  POP_EXCEPT       
              126  JUMP_FORWARD        130  'to 130'
              128  <48>             
            130_0  COME_FROM           126  '126'
            130_1  COME_FROM           108  '108'

 L. 322       130  LOAD_GLOBAL              print
              132  LOAD_STR                 '\tCLSID = CLSID_Sink = '
              134  LOAD_GLOBAL              repr
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                clsid
              140  CALL_FUNCTION_1       1  ''
              142  BINARY_ADD       
              144  LOAD_FAST                'stream'
              146  LOAD_CONST               ('file',)
              148  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              150  POP_TOP          

 L. 323       152  LOAD_FAST                'self'
              154  LOAD_ATTR                coclass_clsid
              156  LOAD_CONST               None
              158  <117>                 0  ''
              160  POP_JUMP_IF_FALSE   176  'to 176'

 L. 324       162  LOAD_GLOBAL              print
              164  LOAD_STR                 '\tcoclass_clsid = None'
              166  LOAD_FAST                'stream'
              168  LOAD_CONST               ('file',)
              170  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              172  POP_TOP          
              174  JUMP_FORWARD        198  'to 198'
            176_0  COME_FROM           160  '160'

 L. 326       176  LOAD_GLOBAL              print
              178  LOAD_STR                 '\tcoclass_clsid = '
              180  LOAD_GLOBAL              repr
              182  LOAD_FAST                'self'
              184  LOAD_ATTR                coclass_clsid
              186  CALL_FUNCTION_1       1  ''
              188  BINARY_ADD       
              190  LOAD_FAST                'stream'
              192  LOAD_CONST               ('file',)
              194  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              196  POP_TOP          
            198_0  COME_FROM           174  '174'

 L. 327       198  LOAD_GLOBAL              print
              200  LOAD_STR                 '\t_public_methods_ = [] # For COM Server support'
              202  LOAD_FAST                'stream'
              204  LOAD_CONST               ('file',)
              206  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              208  POP_TOP          

 L. 328       210  LOAD_GLOBAL              WriteSinkEventMap
              212  LOAD_FAST                'self'
              214  LOAD_FAST                'stream'
              216  CALL_FUNCTION_2       2  ''
              218  POP_TOP          

 L. 329       220  LOAD_GLOBAL              print
              222  LOAD_FAST                'stream'
              224  LOAD_CONST               ('file',)
              226  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              228  POP_TOP          

 L. 330       230  LOAD_GLOBAL              print
              232  LOAD_STR                 '\tdef __init__(self, oobj = None):'
              234  LOAD_FAST                'stream'
              236  LOAD_CONST               ('file',)
              238  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              240  POP_TOP          

 L. 331       242  LOAD_GLOBAL              print
              244  LOAD_STR                 '\t\tif oobj is None:'
              246  LOAD_FAST                'stream'
              248  LOAD_CONST               ('file',)
              250  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              252  POP_TOP          

 L. 332       254  LOAD_GLOBAL              print
              256  LOAD_STR                 '\t\t\tself._olecp = None'
              258  LOAD_FAST                'stream'
              260  LOAD_CONST               ('file',)
              262  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              264  POP_TOP          

 L. 333       266  LOAD_GLOBAL              print
              268  LOAD_STR                 '\t\telse:'
              270  LOAD_FAST                'stream'
              272  LOAD_CONST               ('file',)
              274  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              276  POP_TOP          

 L. 334       278  LOAD_GLOBAL              print
              280  LOAD_STR                 '\t\t\timport win32com.server.util'
              282  LOAD_FAST                'stream'
              284  LOAD_CONST               ('file',)
              286  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              288  POP_TOP          

 L. 335       290  LOAD_GLOBAL              print
              292  LOAD_STR                 '\t\t\tfrom win32com.server.policy import EventHandlerPolicy'
              294  LOAD_FAST                'stream'
              296  LOAD_CONST               ('file',)
              298  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              300  POP_TOP          

 L. 336       302  LOAD_GLOBAL              print
              304  LOAD_STR                 '\t\t\tcpc=oobj._oleobj_.QueryInterface(pythoncom.IID_IConnectionPointContainer)'
              306  LOAD_FAST                'stream'
              308  LOAD_CONST               ('file',)
              310  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              312  POP_TOP          

 L. 337       314  LOAD_GLOBAL              print
              316  LOAD_STR                 '\t\t\tcp=cpc.FindConnectionPoint(self.CLSID_Sink)'
              318  LOAD_FAST                'stream'
              320  LOAD_CONST               ('file',)
              322  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              324  POP_TOP          

 L. 338       326  LOAD_GLOBAL              print
              328  LOAD_STR                 '\t\t\tcookie=cp.Advise(win32com.server.util.wrap(self, usePolicy=EventHandlerPolicy))'
              330  LOAD_FAST                'stream'
              332  LOAD_CONST               ('file',)
              334  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              336  POP_TOP          

 L. 339       338  LOAD_GLOBAL              print
              340  LOAD_STR                 '\t\t\tself._olecp,self._olecp_cookie = cp,cookie'
              342  LOAD_FAST                'stream'
              344  LOAD_CONST               ('file',)
              346  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              348  POP_TOP          

 L. 340       350  LOAD_GLOBAL              print
              352  LOAD_STR                 '\tdef __del__(self):'
              354  LOAD_FAST                'stream'
              356  LOAD_CONST               ('file',)
              358  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              360  POP_TOP          

 L. 341       362  LOAD_GLOBAL              print
              364  LOAD_STR                 '\t\ttry:'
              366  LOAD_FAST                'stream'
              368  LOAD_CONST               ('file',)
              370  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              372  POP_TOP          

 L. 342       374  LOAD_GLOBAL              print
              376  LOAD_STR                 '\t\t\tself.close()'
              378  LOAD_FAST                'stream'
              380  LOAD_CONST               ('file',)
              382  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              384  POP_TOP          

 L. 343       386  LOAD_GLOBAL              print
              388  LOAD_STR                 '\t\texcept pythoncom.com_error:'
              390  LOAD_FAST                'stream'
              392  LOAD_CONST               ('file',)
              394  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              396  POP_TOP          

 L. 344       398  LOAD_GLOBAL              print
              400  LOAD_STR                 '\t\t\tpass'
              402  LOAD_FAST                'stream'
              404  LOAD_CONST               ('file',)
              406  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              408  POP_TOP          

 L. 345       410  LOAD_GLOBAL              print
              412  LOAD_STR                 '\tdef close(self):'
              414  LOAD_FAST                'stream'
              416  LOAD_CONST               ('file',)
              418  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              420  POP_TOP          

 L. 346       422  LOAD_GLOBAL              print
              424  LOAD_STR                 '\t\tif self._olecp is not None:'
              426  LOAD_FAST                'stream'
              428  LOAD_CONST               ('file',)
              430  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              432  POP_TOP          

 L. 347       434  LOAD_GLOBAL              print
              436  LOAD_STR                 '\t\t\tcp,cookie,self._olecp,self._olecp_cookie = self._olecp,self._olecp_cookie,None,None'
              438  LOAD_FAST                'stream'
              440  LOAD_CONST               ('file',)
              442  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              444  POP_TOP          

 L. 348       446  LOAD_GLOBAL              print
              448  LOAD_STR                 '\t\t\tcp.Unadvise(cookie)'
              450  LOAD_FAST                'stream'
              452  LOAD_CONST               ('file',)
              454  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              456  POP_TOP          

 L. 349       458  LOAD_GLOBAL              print
              460  LOAD_STR                 '\tdef _query_interface_(self, iid):'
              462  LOAD_FAST                'stream'
              464  LOAD_CONST               ('file',)
              466  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              468  POP_TOP          

 L. 350       470  LOAD_GLOBAL              print
              472  LOAD_STR                 '\t\timport win32com.server.util'
              474  LOAD_FAST                'stream'
              476  LOAD_CONST               ('file',)
              478  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              480  POP_TOP          

 L. 351       482  LOAD_GLOBAL              print
              484  LOAD_STR                 '\t\tif iid==self.CLSID_Sink: return win32com.server.util.wrap(self)'
              486  LOAD_FAST                'stream'
              488  LOAD_CONST               ('file',)
              490  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              492  POP_TOP          

 L. 352       494  LOAD_GLOBAL              print
              496  LOAD_FAST                'stream'
              498  LOAD_CONST               ('file',)
              500  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              502  POP_TOP          

 L. 353       504  LOAD_CONST               1
              506  LOAD_FAST                'self'
              508  STORE_ATTR               bWritten

Parse error at or near `<121>' instruction at offset 116

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
                    print(('#\t\t' + build._makeDocStringentry.doc[1]), file=stream)
                print(file=stream)
                self.bWritten = 1

    def WriteClassBody--- This code section failed: ---

 L. 369         0  LOAD_FAST                'generator'
                2  LOAD_ATTR                file
                4  STORE_FAST               'stream'

 L. 371         6  LOAD_GLOBAL              list
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                mapFuncs
               12  LOAD_METHOD              keys
               14  CALL_METHOD_0         0  ''
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'names'

 L. 372        20  LOAD_FAST                'names'
               22  LOAD_METHOD              sort
               24  CALL_METHOD_0         0  ''
               26  POP_TOP          

 L. 373        28  LOAD_CONST               None
               30  LOAD_CONST               None
               32  LOAD_CONST               None
               34  LOAD_CONST               None
               36  LOAD_CONST               ('count', 'item', 'value', '_newenum')
               38  BUILD_CONST_KEY_MAP_4     4 
               40  STORE_FAST               'specialItems'

 L. 374        42  LOAD_CONST               None
               44  STORE_FAST               'itemCount'

 L. 375        46  LOAD_FAST                'names'
               48  GET_ITER         
             50_0  COME_FROM           238  '238'
            50_52  FOR_ITER            338  'to 338'
               54  STORE_FAST               'name'

 L. 376        56  LOAD_FAST                'self'
               58  LOAD_ATTR                mapFuncs
               60  LOAD_FAST                'name'
               62  BINARY_SUBSCR    
               64  STORE_FAST               'entry'

 L. 377        66  LOAD_FAST                'entry'
               68  LOAD_ATTR                desc
               70  LOAD_ATTR                desckind
               72  LOAD_GLOBAL              pythoncom
               74  LOAD_ATTR                DESCKIND_FUNCDESC
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_TRUE     84  'to 84'
               80  <74>             
               82  RAISE_VARARGS_1       1  'exception instance'
             84_0  COME_FROM            78  '78'

 L. 381        84  LOAD_FAST                'entry'
               86  LOAD_ATTR                desc
               88  LOAD_ATTR                memid
               90  STORE_FAST               'dispid'

 L. 382        92  LOAD_FAST                'entry'
               94  LOAD_ATTR                desc
               96  LOAD_ATTR                wFuncFlags
               98  LOAD_GLOBAL              pythoncom
              100  LOAD_ATTR                FUNCFLAG_FRESTRICTED
              102  BINARY_AND       
              104  POP_JUMP_IF_FALSE   118  'to 118'

 L. 383       106  LOAD_FAST                'dispid'
              108  LOAD_GLOBAL              pythoncom
              110  LOAD_ATTR                DISPID_NEWENUM
              112  COMPARE_OP               !=

 L. 382       114  POP_JUMP_IF_FALSE   118  'to 118'

 L. 384       116  JUMP_BACK            50  'to 50'
            118_0  COME_FROM           114  '114'
            118_1  COME_FROM           104  '104'

 L. 386       118  LOAD_FAST                'entry'
              120  LOAD_ATTR                desc
              122  LOAD_ATTR                funckind
              124  LOAD_GLOBAL              pythoncom
              126  LOAD_ATTR                FUNC_DISPATCH
              128  COMPARE_OP               !=
              130  POP_JUMP_IF_FALSE   134  'to 134'

 L. 387       132  JUMP_BACK            50  'to 50'
            134_0  COME_FROM           130  '130'

 L. 388       134  LOAD_FAST                'dispid'
              136  LOAD_GLOBAL              pythoncom
              138  LOAD_ATTR                DISPID_VALUE
              140  COMPARE_OP               ==
              142  POP_JUMP_IF_FALSE   150  'to 150'

 L. 389       144  LOAD_STR                 'value'
              146  STORE_FAST               'lkey'
              148  JUMP_FORWARD        190  'to 190'
            150_0  COME_FROM           142  '142'

 L. 390       150  LOAD_FAST                'dispid'
              152  LOAD_GLOBAL              pythoncom
              154  LOAD_ATTR                DISPID_NEWENUM
              156  COMPARE_OP               ==
              158  POP_JUMP_IF_FALSE   182  'to 182'

 L. 391       160  LOAD_FAST                'entry'
              162  LOAD_FAST                'entry'
              164  LOAD_ATTR                desc
              166  LOAD_ATTR                invkind
              168  LOAD_CONST               None
              170  BUILD_TUPLE_3         3 
              172  LOAD_FAST                'specialItems'
              174  LOAD_STR                 '_newenum'
              176  STORE_SUBSCR     

 L. 392       178  JUMP_BACK            50  'to 50'
              180  JUMP_FORWARD        190  'to 190'
            182_0  COME_FROM           158  '158'

 L. 394       182  LOAD_FAST                'name'
              184  LOAD_METHOD              lower
              186  CALL_METHOD_0         0  ''
              188  STORE_FAST               'lkey'
            190_0  COME_FROM           180  '180'
            190_1  COME_FROM           148  '148'

 L. 395       190  LOAD_FAST                'lkey'
              192  LOAD_FAST                'specialItems'
              194  <118>                 0  ''
              196  POP_JUMP_IF_FALSE   228  'to 228'
              198  LOAD_FAST                'specialItems'
              200  LOAD_FAST                'lkey'
              202  BINARY_SUBSCR    
              204  LOAD_CONST               None
              206  <117>                 0  ''
              208  POP_JUMP_IF_FALSE   228  'to 228'

 L. 396       210  LOAD_FAST                'entry'
              212  LOAD_FAST                'entry'
              214  LOAD_ATTR                desc
              216  LOAD_ATTR                invkind
              218  LOAD_CONST               None
              220  BUILD_TUPLE_3         3 
              222  LOAD_FAST                'specialItems'
              224  LOAD_FAST                'lkey'
              226  STORE_SUBSCR     
            228_0  COME_FROM           208  '208'
            228_1  COME_FROM           196  '196'

 L. 397       228  LOAD_FAST                'generator'
              230  LOAD_ATTR                bBuildHidden
              232  POP_JUMP_IF_TRUE    240  'to 240'
              234  LOAD_FAST                'entry'
              236  LOAD_ATTR                hidden
              238  POP_JUMP_IF_TRUE     50  'to 50'
            240_0  COME_FROM           232  '232'

 L. 398       240  LOAD_FAST                'entry'
              242  LOAD_METHOD              GetResultName
              244  CALL_METHOD_0         0  ''
          246_248  POP_JUMP_IF_FALSE   270  'to 270'

 L. 399       250  LOAD_GLOBAL              print
              252  LOAD_STR                 '\t# Result is of type '
              254  LOAD_FAST                'entry'
              256  LOAD_METHOD              GetResultName
              258  CALL_METHOD_0         0  ''
              260  BINARY_ADD       
              262  LOAD_FAST                'stream'
              264  LOAD_CONST               ('file',)
              266  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              268  POP_TOP          
            270_0  COME_FROM           246  '246'

 L. 400       270  LOAD_FAST                'entry'
              272  LOAD_ATTR                wasProperty
          274_276  POP_JUMP_IF_FALSE   294  'to 294'

 L. 401       278  LOAD_GLOBAL              print
              280  LOAD_STR                 '\t# The method %s is actually a property, but must be used as a method to correctly pass the arguments'
              282  LOAD_FAST                'name'
              284  BINARY_MODULO    
              286  LOAD_FAST                'stream'
              288  LOAD_CONST               ('file',)
              290  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              292  POP_TOP          
            294_0  COME_FROM           274  '274'

 L. 402       294  LOAD_FAST                'self'
              296  LOAD_METHOD              MakeFuncMethod
              298  LOAD_FAST                'entry'
              300  LOAD_GLOBAL              build
              302  LOAD_METHOD              MakePublicAttributeName
              304  LOAD_FAST                'name'
              306  CALL_METHOD_1         1  ''
              308  CALL_METHOD_2         2  ''
              310  STORE_FAST               'ret'

 L. 403       312  LOAD_FAST                'ret'
              314  GET_ITER         
              316  FOR_ITER            336  'to 336'
              318  STORE_FAST               'line'

 L. 404       320  LOAD_GLOBAL              print
              322  LOAD_FAST                'line'
              324  LOAD_FAST                'stream'
              326  LOAD_CONST               ('file',)
              328  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              330  POP_TOP          
          332_334  JUMP_BACK           316  'to 316'
              336  JUMP_BACK            50  'to 50'

 L. 405       338  LOAD_GLOBAL              print
              340  LOAD_STR                 '\t_prop_map_get_ = {'
              342  LOAD_FAST                'stream'
              344  LOAD_CONST               ('file',)
              346  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              348  POP_TOP          

 L. 406       350  LOAD_GLOBAL              list
              352  LOAD_FAST                'self'
              354  LOAD_ATTR                propMap
              356  LOAD_METHOD              keys
              358  CALL_METHOD_0         0  ''
              360  CALL_FUNCTION_1       1  ''
              362  STORE_FAST               'names'
              364  LOAD_FAST                'names'
              366  LOAD_METHOD              sort
              368  CALL_METHOD_0         0  ''
              370  POP_TOP          

 L. 407       372  LOAD_FAST                'names'
              374  GET_ITER         
            376_0  COME_FROM           402  '402'
              376  FOR_ITER            628  'to 628'
              378  STORE_FAST               'key'

 L. 408       380  LOAD_FAST                'self'
              382  LOAD_ATTR                propMap
              384  LOAD_FAST                'key'
              386  BINARY_SUBSCR    
              388  STORE_FAST               'entry'

 L. 409       390  LOAD_FAST                'generator'
              392  LOAD_ATTR                bBuildHidden
          394_396  POP_JUMP_IF_TRUE    406  'to 406'
              398  LOAD_FAST                'entry'
              400  LOAD_ATTR                hidden
          402_404  POP_JUMP_IF_TRUE    376  'to 376'
            406_0  COME_FROM           394  '394'

 L. 410       406  LOAD_FAST                'entry'
              408  LOAD_METHOD              GetResultName
              410  CALL_METHOD_0         0  ''
              412  STORE_FAST               'resultName'

 L. 411       414  LOAD_FAST                'resultName'
          416_418  POP_JUMP_IF_FALSE   440  'to 440'

 L. 412       420  LOAD_GLOBAL              print
              422  LOAD_STR                 "\t\t# Property '%s' is an object of type '%s'"
              424  LOAD_FAST                'key'
              426  LOAD_FAST                'resultName'
              428  BUILD_TUPLE_2         2 
              430  BINARY_MODULO    
              432  LOAD_FAST                'stream'
              434  LOAD_CONST               ('file',)
              436  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              438  POP_TOP          
            440_0  COME_FROM           416  '416'

 L. 413       440  LOAD_FAST                'key'
              442  LOAD_METHOD              lower
              444  CALL_METHOD_0         0  ''
              446  STORE_FAST               'lkey'

 L. 414       448  LOAD_FAST                'entry'
              450  LOAD_ATTR                desc
              452  STORE_FAST               'details'

 L. 415       454  LOAD_FAST                'details'
              456  LOAD_CONST               2
              458  BINARY_SUBSCR    
              460  STORE_FAST               'resultDesc'

 L. 416       462  LOAD_CONST               ()
              464  STORE_FAST               'argDesc'

 L. 417       466  LOAD_GLOBAL              MakeMapLineEntry
              468  LOAD_FAST                'details'
              470  LOAD_ATTR                memid
              472  LOAD_GLOBAL              pythoncom
              474  LOAD_ATTR                DISPATCH_PROPERTYGET
              476  LOAD_FAST                'resultDesc'
              478  LOAD_FAST                'argDesc'
              480  LOAD_FAST                'key'
              482  LOAD_FAST                'entry'
              484  LOAD_METHOD              GetResultCLSIDStr
              486  CALL_METHOD_0         0  ''
              488  CALL_FUNCTION_6       6  ''
              490  STORE_FAST               'mapEntry'

 L. 419       492  LOAD_FAST                'details'
              494  LOAD_ATTR                memid
              496  LOAD_GLOBAL              pythoncom
              498  LOAD_ATTR                DISPID_VALUE
              500  COMPARE_OP               ==
          502_504  POP_JUMP_IF_FALSE   512  'to 512'

 L. 420       506  LOAD_STR                 'value'
              508  STORE_FAST               'lkey'
              510  JUMP_FORWARD        540  'to 540'
            512_0  COME_FROM           502  '502'

 L. 421       512  LOAD_FAST                'details'
              514  LOAD_ATTR                memid
              516  LOAD_GLOBAL              pythoncom
              518  LOAD_ATTR                DISPID_NEWENUM
              520  COMPARE_OP               ==
          522_524  POP_JUMP_IF_FALSE   532  'to 532'

 L. 422       526  LOAD_STR                 '_newenum'
              528  STORE_FAST               'lkey'
              530  JUMP_FORWARD        540  'to 540'
            532_0  COME_FROM           522  '522'

 L. 424       532  LOAD_FAST                'key'
              534  LOAD_METHOD              lower
              536  CALL_METHOD_0         0  ''
              538  STORE_FAST               'lkey'
            540_0  COME_FROM           530  '530'
            540_1  COME_FROM           510  '510'

 L. 425       540  LOAD_FAST                'lkey'
              542  LOAD_FAST                'specialItems'
              544  <118>                 0  ''
          546_548  POP_JUMP_IF_FALSE   598  'to 598'
              550  LOAD_FAST                'specialItems'
              552  LOAD_FAST                'lkey'
              554  BINARY_SUBSCR    
              556  LOAD_CONST               None
              558  <117>                 0  ''
          560_562  POP_JUMP_IF_FALSE   598  'to 598'

 L. 426       564  LOAD_FAST                'entry'
              566  LOAD_GLOBAL              pythoncom
              568  LOAD_ATTR                DISPATCH_PROPERTYGET
              570  LOAD_FAST                'mapEntry'
              572  BUILD_TUPLE_3         3 
              574  LOAD_FAST                'specialItems'
              576  LOAD_FAST                'lkey'
              578  STORE_SUBSCR     

 L. 429       580  LOAD_FAST                'details'
              582  LOAD_ATTR                memid
              584  LOAD_GLOBAL              pythoncom
              586  LOAD_ATTR                DISPID_NEWENUM
              588  COMPARE_OP               ==
          590_592  POP_JUMP_IF_FALSE   598  'to 598'

 L. 430   594_596  JUMP_BACK           376  'to 376'
            598_0  COME_FROM           590  '590'
            598_1  COME_FROM           560  '560'
            598_2  COME_FROM           546  '546'

 L. 432       598  LOAD_GLOBAL              print
              600  LOAD_STR                 '\t\t"%s": %s,'
              602  LOAD_GLOBAL              build
              604  LOAD_METHOD              MakePublicAttributeName
              606  LOAD_FAST                'key'
              608  CALL_METHOD_1         1  ''
              610  LOAD_FAST                'mapEntry'
              612  BUILD_TUPLE_2         2 
              614  BINARY_MODULO    
              616  LOAD_FAST                'stream'
              618  LOAD_CONST               ('file',)
              620  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              622  POP_TOP          
          624_626  JUMP_BACK           376  'to 376'

 L. 433       628  LOAD_GLOBAL              list
              630  LOAD_FAST                'self'
              632  LOAD_ATTR                propMapGet
              634  LOAD_METHOD              keys
              636  CALL_METHOD_0         0  ''
              638  CALL_FUNCTION_1       1  ''
              640  STORE_FAST               'names'
              642  LOAD_FAST                'names'
              644  LOAD_METHOD              sort
              646  CALL_METHOD_0         0  ''
              648  POP_TOP          

 L. 434       650  LOAD_FAST                'names'
              652  GET_ITER         
            654_0  COME_FROM           682  '682'
          654_656  FOR_ITER            932  'to 932'
              658  STORE_FAST               'key'

 L. 435       660  LOAD_FAST                'self'
              662  LOAD_ATTR                propMapGet
              664  LOAD_FAST                'key'
              666  BINARY_SUBSCR    
              668  STORE_FAST               'entry'

 L. 436       670  LOAD_FAST                'generator'
              672  LOAD_ATTR                bBuildHidden
          674_676  POP_JUMP_IF_TRUE    686  'to 686'
              678  LOAD_FAST                'entry'
              680  LOAD_ATTR                hidden
          682_684  POP_JUMP_IF_TRUE    654  'to 654'
            686_0  COME_FROM           674  '674'

 L. 437       686  LOAD_FAST                'entry'
              688  LOAD_METHOD              GetResultName
              690  CALL_METHOD_0         0  ''
          692_694  POP_JUMP_IF_FALSE   720  'to 720'

 L. 438       696  LOAD_GLOBAL              print
              698  LOAD_STR                 "\t\t# Method '%s' returns object of type '%s'"
              700  LOAD_FAST                'key'
              702  LOAD_FAST                'entry'
              704  LOAD_METHOD              GetResultName
              706  CALL_METHOD_0         0  ''
              708  BUILD_TUPLE_2         2 
              710  BINARY_MODULO    
              712  LOAD_FAST                'stream'
              714  LOAD_CONST               ('file',)
              716  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              718  POP_TOP          
            720_0  COME_FROM           692  '692'

 L. 439       720  LOAD_FAST                'entry'
              722  LOAD_ATTR                desc
              724  STORE_FAST               'details'

 L. 440       726  LOAD_FAST                'details'
              728  LOAD_ATTR                desckind
              730  LOAD_GLOBAL              pythoncom
              732  LOAD_ATTR                DESCKIND_FUNCDESC
              734  COMPARE_OP               ==
          736_738  POP_JUMP_IF_TRUE    744  'to 744'
              740  <74>             
              742  RAISE_VARARGS_1       1  'exception instance'
            744_0  COME_FROM           736  '736'

 L. 441       744  LOAD_FAST                'key'
              746  LOAD_METHOD              lower
              748  CALL_METHOD_0         0  ''
              750  STORE_FAST               'lkey'

 L. 442       752  LOAD_FAST                'details'
              754  LOAD_CONST               2
              756  BINARY_SUBSCR    
              758  STORE_FAST               'argDesc'

 L. 443       760  LOAD_FAST                'details'
              762  LOAD_CONST               8
              764  BINARY_SUBSCR    
              766  STORE_FAST               'resultDesc'

 L. 444       768  LOAD_GLOBAL              MakeMapLineEntry
              770  LOAD_FAST                'details'
              772  LOAD_CONST               0
              774  BINARY_SUBSCR    
              776  LOAD_GLOBAL              pythoncom
              778  LOAD_ATTR                DISPATCH_PROPERTYGET
              780  LOAD_FAST                'resultDesc'
              782  LOAD_FAST                'argDesc'
              784  LOAD_FAST                'key'
              786  LOAD_FAST                'entry'
              788  LOAD_METHOD              GetResultCLSIDStr
              790  CALL_METHOD_0         0  ''
              792  CALL_FUNCTION_6       6  ''
              794  STORE_FAST               'mapEntry'

 L. 445       796  LOAD_FAST                'details'
              798  LOAD_ATTR                memid
              800  LOAD_GLOBAL              pythoncom
              802  LOAD_ATTR                DISPID_VALUE
              804  COMPARE_OP               ==
          806_808  POP_JUMP_IF_FALSE   816  'to 816'

 L. 446       810  LOAD_STR                 'value'
              812  STORE_FAST               'lkey'
              814  JUMP_FORWARD        844  'to 844'
            816_0  COME_FROM           806  '806'

 L. 447       816  LOAD_FAST                'details'
              818  LOAD_ATTR                memid
              820  LOAD_GLOBAL              pythoncom
              822  LOAD_ATTR                DISPID_NEWENUM
              824  COMPARE_OP               ==
          826_828  POP_JUMP_IF_FALSE   836  'to 836'

 L. 448       830  LOAD_STR                 '_newenum'
              832  STORE_FAST               'lkey'
              834  JUMP_FORWARD        844  'to 844'
            836_0  COME_FROM           826  '826'

 L. 450       836  LOAD_FAST                'key'
              838  LOAD_METHOD              lower
              840  CALL_METHOD_0         0  ''
              842  STORE_FAST               'lkey'
            844_0  COME_FROM           834  '834'
            844_1  COME_FROM           814  '814'

 L. 451       844  LOAD_FAST                'lkey'
              846  LOAD_FAST                'specialItems'
              848  <118>                 0  ''
          850_852  POP_JUMP_IF_FALSE   902  'to 902'
              854  LOAD_FAST                'specialItems'
              856  LOAD_FAST                'lkey'
              858  BINARY_SUBSCR    
              860  LOAD_CONST               None
              862  <117>                 0  ''
          864_866  POP_JUMP_IF_FALSE   902  'to 902'

 L. 452       868  LOAD_FAST                'entry'
              870  LOAD_GLOBAL              pythoncom
              872  LOAD_ATTR                DISPATCH_PROPERTYGET
              874  LOAD_FAST                'mapEntry'
              876  BUILD_TUPLE_3         3 
              878  LOAD_FAST                'specialItems'
              880  LOAD_FAST                'lkey'
              882  STORE_SUBSCR     

 L. 455       884  LOAD_FAST                'details'
              886  LOAD_ATTR                memid
              888  LOAD_GLOBAL              pythoncom
              890  LOAD_ATTR                DISPID_NEWENUM
              892  COMPARE_OP               ==
          894_896  POP_JUMP_IF_FALSE   902  'to 902'

 L. 456   898_900  JUMP_BACK           654  'to 654'
            902_0  COME_FROM           894  '894'
            902_1  COME_FROM           864  '864'
            902_2  COME_FROM           850  '850'

 L. 457       902  LOAD_GLOBAL              print
              904  LOAD_STR                 '\t\t"%s": %s,'
              906  LOAD_GLOBAL              build
              908  LOAD_METHOD              MakePublicAttributeName
              910  LOAD_FAST                'key'
              912  CALL_METHOD_1         1  ''
              914  LOAD_FAST                'mapEntry'
              916  BUILD_TUPLE_2         2 
              918  BINARY_MODULO    
              920  LOAD_FAST                'stream'
              922  LOAD_CONST               ('file',)
              924  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              926  POP_TOP          
          928_930  JUMP_BACK           654  'to 654'

 L. 459       932  LOAD_GLOBAL              print
              934  LOAD_STR                 '\t}'
              936  LOAD_FAST                'stream'
              938  LOAD_CONST               ('file',)
              940  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              942  POP_TOP          

 L. 461       944  LOAD_GLOBAL              print
              946  LOAD_STR                 '\t_prop_map_put_ = {'
              948  LOAD_FAST                'stream'
              950  LOAD_CONST               ('file',)
              952  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              954  POP_TOP          

 L. 463       956  LOAD_GLOBAL              list
              958  LOAD_FAST                'self'
              960  LOAD_ATTR                propMap
              962  LOAD_METHOD              keys
              964  CALL_METHOD_0         0  ''
              966  CALL_FUNCTION_1       1  ''
              968  STORE_FAST               'names'
              970  LOAD_FAST                'names'
              972  LOAD_METHOD              sort
              974  CALL_METHOD_0         0  ''
              976  POP_TOP          

 L. 464       978  LOAD_FAST                'names'
              980  GET_ITER         
            982_0  COME_FROM          1008  '1008'
              982  FOR_ITER           1104  'to 1104'
              984  STORE_FAST               'key'

 L. 465       986  LOAD_FAST                'self'
              988  LOAD_ATTR                propMap
              990  LOAD_FAST                'key'
              992  BINARY_SUBSCR    
              994  STORE_FAST               'entry'

 L. 466       996  LOAD_FAST                'generator'
              998  LOAD_ATTR                bBuildHidden
         1000_1002  POP_JUMP_IF_TRUE   1012  'to 1012'
             1004  LOAD_FAST                'entry'
             1006  LOAD_ATTR                hidden
         1008_1010  POP_JUMP_IF_TRUE    982  'to 982'
           1012_0  COME_FROM          1000  '1000'

 L. 467      1012  LOAD_FAST                'key'
             1014  LOAD_METHOD              lower
             1016  CALL_METHOD_0         0  ''
             1018  STORE_FAST               'lkey'

 L. 468      1020  LOAD_FAST                'entry'
             1022  LOAD_ATTR                desc
             1024  STORE_FAST               'details'

 L. 470      1026  LOAD_GLOBAL              build
             1028  LOAD_METHOD              MakeDefaultArgRepr
             1030  LOAD_FAST                'details'
             1032  LOAD_CONST               2
             1034  BINARY_SUBSCR    
             1036  CALL_METHOD_1         1  ''
             1038  STORE_FAST               'defArgDesc'

 L. 471      1040  LOAD_FAST                'defArgDesc'
             1042  LOAD_CONST               None
             1044  <117>                 0  ''
         1046_1048  POP_JUMP_IF_FALSE  1056  'to 1056'

 L. 472      1050  LOAD_STR                 ''
             1052  STORE_FAST               'defArgDesc'
             1054  JUMP_FORWARD       1064  'to 1064'
           1056_0  COME_FROM          1046  '1046'

 L. 474      1056  LOAD_FAST                'defArgDesc'
             1058  LOAD_STR                 ','
             1060  BINARY_ADD       
             1062  STORE_FAST               'defArgDesc'
           1064_0  COME_FROM          1054  '1054'

 L. 475      1064  LOAD_GLOBAL              print
             1066  LOAD_STR                 '\t\t"%s" : ((%s, LCID, %d, 0),(%s)),'
             1068  LOAD_GLOBAL              build
             1070  LOAD_METHOD              MakePublicAttributeName
             1072  LOAD_FAST                'key'
             1074  CALL_METHOD_1         1  ''
             1076  LOAD_FAST                'details'
             1078  LOAD_CONST               0
             1080  BINARY_SUBSCR    
             1082  LOAD_GLOBAL              pythoncom
             1084  LOAD_ATTR                DISPATCH_PROPERTYPUT
             1086  LOAD_FAST                'defArgDesc'
             1088  BUILD_TUPLE_4         4 
             1090  BINARY_MODULO    
             1092  LOAD_FAST                'stream'
             1094  LOAD_CONST               ('file',)
             1096  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1098  POP_TOP          
         1100_1102  JUMP_BACK           982  'to 982'

 L. 477      1104  LOAD_GLOBAL              list
             1106  LOAD_FAST                'self'
             1108  LOAD_ATTR                propMapPut
             1110  LOAD_METHOD              keys
             1112  CALL_METHOD_0         0  ''
             1114  CALL_FUNCTION_1       1  ''
             1116  STORE_FAST               'names'
             1118  LOAD_FAST                'names'
             1120  LOAD_METHOD              sort
             1122  CALL_METHOD_0         0  ''
             1124  POP_TOP          

 L. 478      1126  LOAD_FAST                'names'
             1128  GET_ITER         
           1130_0  COME_FROM          1156  '1156'
             1130  FOR_ITER           1220  'to 1220'
             1132  STORE_FAST               'key'

 L. 479      1134  LOAD_FAST                'self'
             1136  LOAD_ATTR                propMapPut
             1138  LOAD_FAST                'key'
             1140  BINARY_SUBSCR    
             1142  STORE_FAST               'entry'

 L. 480      1144  LOAD_FAST                'generator'
             1146  LOAD_ATTR                bBuildHidden
         1148_1150  POP_JUMP_IF_TRUE   1160  'to 1160'
             1152  LOAD_FAST                'entry'
             1154  LOAD_ATTR                hidden
         1156_1158  POP_JUMP_IF_TRUE   1130  'to 1130'
           1160_0  COME_FROM          1148  '1148'

 L. 481      1160  LOAD_FAST                'entry'
             1162  LOAD_ATTR                desc
             1164  STORE_FAST               'details'

 L. 482      1166  LOAD_GLOBAL              MakeDefaultArgsForPropertyPut
             1168  LOAD_FAST                'details'
             1170  LOAD_CONST               2
             1172  BINARY_SUBSCR    
             1174  CALL_FUNCTION_1       1  ''
             1176  STORE_FAST               'defArgDesc'

 L. 483      1178  LOAD_GLOBAL              print
             1180  LOAD_STR                 '\t\t"%s": ((%s, LCID, %d, 0),%s),'
             1182  LOAD_GLOBAL              build
             1184  LOAD_METHOD              MakePublicAttributeName
             1186  LOAD_FAST                'key'
             1188  CALL_METHOD_1         1  ''
             1190  LOAD_FAST                'details'
             1192  LOAD_CONST               0
             1194  BINARY_SUBSCR    
             1196  LOAD_FAST                'details'
             1198  LOAD_CONST               4
             1200  BINARY_SUBSCR    
             1202  LOAD_FAST                'defArgDesc'
             1204  BUILD_TUPLE_4         4 
             1206  BINARY_MODULO    
             1208  LOAD_FAST                'stream'
             1210  LOAD_CONST               ('file',)
             1212  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1214  POP_TOP          
         1216_1218  JUMP_BACK          1130  'to 1130'

 L. 484      1220  LOAD_GLOBAL              print
             1222  LOAD_STR                 '\t}'
             1224  LOAD_FAST                'stream'
             1226  LOAD_CONST               ('file',)
             1228  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1230  POP_TOP          

 L. 486      1232  LOAD_FAST                'specialItems'
             1234  LOAD_STR                 'value'
             1236  BINARY_SUBSCR    
         1238_1240  POP_JUMP_IF_FALSE  1396  'to 1396'

 L. 487      1242  LOAD_FAST                'specialItems'
             1244  LOAD_STR                 'value'
             1246  BINARY_SUBSCR    
             1248  UNPACK_SEQUENCE_3     3 
             1250  STORE_FAST               'entry'
             1252  STORE_FAST               'invoketype'
             1254  STORE_FAST               'propArgs'

 L. 488      1256  LOAD_FAST                'propArgs'
             1258  LOAD_CONST               None
             1260  <117>                 0  ''
         1262_1264  POP_JUMP_IF_FALSE  1284  'to 1284'

 L. 489      1266  LOAD_STR                 'method'
             1268  STORE_FAST               'typename'

 L. 490      1270  LOAD_FAST                'self'
             1272  LOAD_METHOD              MakeFuncMethod
             1274  LOAD_FAST                'entry'
             1276  LOAD_STR                 '__call__'
             1278  CALL_METHOD_2         2  ''
             1280  STORE_FAST               'ret'
             1282  JUMP_FORWARD       1298  'to 1298'
           1284_0  COME_FROM          1262  '1262'

 L. 492      1284  LOAD_STR                 'property'
             1286  STORE_FAST               'typename'

 L. 493      1288  LOAD_STR                 '\tdef __call__(self):\n\t\treturn self._ApplyTypes_(*%s)'
             1290  LOAD_FAST                'propArgs'
             1292  BINARY_MODULO    
             1294  BUILD_LIST_1          1 
             1296  STORE_FAST               'ret'
           1298_0  COME_FROM          1282  '1282'

 L. 494      1298  LOAD_GLOBAL              print
             1300  LOAD_STR                 "\t# Default %s for this class is '%s'"
             1302  LOAD_FAST                'typename'
             1304  LOAD_FAST                'entry'
             1306  LOAD_ATTR                names
             1308  LOAD_CONST               0
             1310  BINARY_SUBSCR    
             1312  BUILD_TUPLE_2         2 
             1314  BINARY_MODULO    
             1316  LOAD_FAST                'stream'
             1318  LOAD_CONST               ('file',)
             1320  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1322  POP_TOP          

 L. 495      1324  LOAD_FAST                'ret'
             1326  GET_ITER         
             1328  FOR_ITER           1348  'to 1348'
             1330  STORE_FAST               'line'

 L. 496      1332  LOAD_GLOBAL              print
             1334  LOAD_FAST                'line'
             1336  LOAD_FAST                'stream'
             1338  LOAD_CONST               ('file',)
             1340  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1342  POP_TOP          
         1344_1346  JUMP_BACK          1328  'to 1328'

 L. 497      1348  LOAD_GLOBAL              print
             1350  LOAD_STR                 '\tdef __str__(self, *args):'
             1352  LOAD_FAST                'stream'
             1354  LOAD_CONST               ('file',)
             1356  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1358  POP_TOP          

 L. 498      1360  LOAD_GLOBAL              print
             1362  LOAD_STR                 '\t\treturn str(self.__call__(*args))'
             1364  LOAD_FAST                'stream'
             1366  LOAD_CONST               ('file',)
             1368  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1370  POP_TOP          

 L. 499      1372  LOAD_GLOBAL              print
             1374  LOAD_STR                 '\tdef __int__(self, *args):'
             1376  LOAD_FAST                'stream'
             1378  LOAD_CONST               ('file',)
             1380  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1382  POP_TOP          

 L. 500      1384  LOAD_GLOBAL              print
             1386  LOAD_STR                 '\t\treturn int(self.__call__(*args))'
             1388  LOAD_FAST                'stream'
             1390  LOAD_CONST               ('file',)
             1392  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1394  POP_TOP          
           1396_0  COME_FROM          1238  '1238'

 L. 506      1396  LOAD_FAST                'specialItems'
             1398  LOAD_STR                 '_newenum'
             1400  BINARY_SUBSCR    
         1402_1404  POP_JUMP_IF_FALSE  1458  'to 1458'

 L. 507      1406  LOAD_FAST                'specialItems'
             1408  LOAD_STR                 '_newenum'
             1410  BINARY_SUBSCR    
             1412  UNPACK_SEQUENCE_3     3 
             1414  STORE_FAST               'enumEntry'
             1416  STORE_FAST               'invoketype'
             1418  STORE_FAST               'propArgs'

 L. 508      1420  LOAD_FAST                'enumEntry'
             1422  LOAD_ATTR                desc
             1424  LOAD_ATTR                desckind
             1426  LOAD_GLOBAL              pythoncom
             1428  LOAD_ATTR                DESCKIND_FUNCDESC
             1430  COMPARE_OP               ==
         1432_1434  POP_JUMP_IF_TRUE   1440  'to 1440'
             1436  <74>             
             1438  RAISE_VARARGS_1       1  'exception instance'
           1440_0  COME_FROM          1432  '1432'

 L. 509      1440  LOAD_FAST                'enumEntry'
             1442  LOAD_ATTR                desc
             1444  LOAD_ATTR                invkind
             1446  STORE_FAST               'invkind'

 L. 512      1448  LOAD_FAST                'enumEntry'
             1450  LOAD_METHOD              GetResultCLSIDStr
             1452  CALL_METHOD_0         0  ''
             1454  STORE_FAST               'resultCLSID'
             1456  JUMP_FORWARD       1474  'to 1474'
           1458_0  COME_FROM          1402  '1402'

 L. 514      1458  LOAD_GLOBAL              pythoncom
             1460  LOAD_ATTR                DISPATCH_METHOD
             1462  LOAD_GLOBAL              pythoncom
             1464  LOAD_ATTR                DISPATCH_PROPERTYGET
             1466  BINARY_OR        
             1468  STORE_FAST               'invkind'

 L. 515      1470  LOAD_STR                 'None'
             1472  STORE_FAST               'resultCLSID'
           1474_0  COME_FROM          1456  '1456'

 L. 517      1474  LOAD_FAST                'resultCLSID'
             1476  LOAD_STR                 'None'
             1478  COMPARE_OP               ==
         1480_1482  POP_JUMP_IF_FALSE  1510  'to 1510'
             1484  LOAD_STR                 'Item'
             1486  LOAD_FAST                'self'
             1488  LOAD_ATTR                mapFuncs
             1490  <118>                 0  ''
         1492_1494  POP_JUMP_IF_FALSE  1510  'to 1510'

 L. 518      1496  LOAD_FAST                'self'
             1498  LOAD_ATTR                mapFuncs
             1500  LOAD_STR                 'Item'
             1502  BINARY_SUBSCR    
             1504  LOAD_METHOD              GetResultCLSIDStr
             1506  CALL_METHOD_0         0  ''
             1508  STORE_FAST               'resultCLSID'
           1510_0  COME_FROM          1492  '1492'
           1510_1  COME_FROM          1480  '1480'

 L. 519      1510  LOAD_GLOBAL              print
             1512  LOAD_STR                 '\tdef __iter__(self):'
             1514  LOAD_FAST                'stream'
             1516  LOAD_CONST               ('file',)
             1518  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1520  POP_TOP          

 L. 520      1522  LOAD_GLOBAL              print
             1524  LOAD_STR                 '\t\t"Return a Python iterator for this object"'
             1526  LOAD_FAST                'stream'
             1528  LOAD_CONST               ('file',)
             1530  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1532  POP_TOP          

 L. 521      1534  LOAD_GLOBAL              print
             1536  LOAD_STR                 '\t\ttry:'
             1538  LOAD_FAST                'stream'
             1540  LOAD_CONST               ('file',)
             1542  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1544  POP_TOP          

 L. 522      1546  LOAD_GLOBAL              print
             1548  LOAD_STR                 '\t\t\tob = self._oleobj_.InvokeTypes(%d,LCID,%d,(13, 10),())'
             1550  LOAD_GLOBAL              pythoncom
             1552  LOAD_ATTR                DISPID_NEWENUM
             1554  LOAD_FAST                'invkind'
             1556  BUILD_TUPLE_2         2 
             1558  BINARY_MODULO    
             1560  LOAD_FAST                'stream'
             1562  LOAD_CONST               ('file',)
             1564  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1566  POP_TOP          

 L. 523      1568  LOAD_GLOBAL              print
             1570  LOAD_STR                 '\t\texcept pythoncom.error:'
             1572  LOAD_FAST                'stream'
             1574  LOAD_CONST               ('file',)
             1576  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1578  POP_TOP          

 L. 524      1580  LOAD_GLOBAL              print
             1582  LOAD_STR                 '\t\t\traise TypeError("This object does not support enumeration")'
             1584  LOAD_FAST                'stream'
             1586  LOAD_CONST               ('file',)
             1588  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1590  POP_TOP          

 L. 526      1592  LOAD_GLOBAL              print
             1594  LOAD_STR                 '\t\treturn win32com.client.util.Iterator(ob, %s)'
             1596  LOAD_FAST                'resultCLSID'
             1598  BINARY_MODULO    
             1600  LOAD_FAST                'stream'
             1602  LOAD_CONST               ('file',)
             1604  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1606  POP_TOP          

 L. 528      1608  LOAD_FAST                'specialItems'
             1610  LOAD_STR                 'item'
             1612  BINARY_SUBSCR    
         1614_1616  POP_JUMP_IF_FALSE  1714  'to 1714'

 L. 529      1618  LOAD_FAST                'specialItems'
             1620  LOAD_STR                 'item'
             1622  BINARY_SUBSCR    
             1624  UNPACK_SEQUENCE_3     3 
             1626  STORE_FAST               'entry'
             1628  STORE_FAST               'invoketype'
             1630  STORE_FAST               'propArgs'

 L. 530      1632  LOAD_FAST                'entry'
             1634  LOAD_METHOD              GetResultCLSIDStr
             1636  CALL_METHOD_0         0  ''
             1638  STORE_FAST               'resultCLSID'

 L. 531      1640  LOAD_GLOBAL              print
             1642  LOAD_STR                 '\t#This class has Item property/method which allows indexed access with the object[key] syntax.'
             1644  LOAD_FAST                'stream'
             1646  LOAD_CONST               ('file',)
             1648  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1650  POP_TOP          

 L. 532      1652  LOAD_GLOBAL              print
             1654  LOAD_STR                 '\t#Some objects will accept a string or other type of key in addition to integers.'
             1656  LOAD_FAST                'stream'
             1658  LOAD_CONST               ('file',)
             1660  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1662  POP_TOP          

 L. 533      1664  LOAD_GLOBAL              print
             1666  LOAD_STR                 '\t#Note that many Office objects do not use zero-based indexing.'
             1668  LOAD_FAST                'stream'
             1670  LOAD_CONST               ('file',)
             1672  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1674  POP_TOP          

 L. 534      1676  LOAD_GLOBAL              print
             1678  LOAD_STR                 '\tdef __getitem__(self, key):'
             1680  LOAD_FAST                'stream'
             1682  LOAD_CONST               ('file',)
             1684  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1686  POP_TOP          

 L. 535      1688  LOAD_GLOBAL              print
             1690  LOAD_STR                 '\t\treturn self._get_good_object_(self._oleobj_.Invoke(*(%d, LCID, %d, 1, key)), "Item", %s)'

 L. 536      1692  LOAD_FAST                'entry'
             1694  LOAD_ATTR                desc
             1696  LOAD_ATTR                memid
             1698  LOAD_FAST                'invoketype'
             1700  LOAD_FAST                'resultCLSID'
             1702  BUILD_TUPLE_3         3 

 L. 535      1704  BINARY_MODULO    

 L. 536      1706  LOAD_FAST                'stream'

 L. 535      1708  LOAD_CONST               ('file',)
             1710  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1712  POP_TOP          
           1714_0  COME_FROM          1614  '1614'

 L. 538      1714  LOAD_FAST                'specialItems'
             1716  LOAD_STR                 'count'
             1718  BINARY_SUBSCR    
         1720_1722  POP_JUMP_IF_FALSE  1856  'to 1856'

 L. 539      1724  LOAD_FAST                'specialItems'
             1726  LOAD_STR                 'count'
             1728  BINARY_SUBSCR    
             1730  UNPACK_SEQUENCE_3     3 
             1732  STORE_FAST               'entry'
             1734  STORE_FAST               'invoketype'
             1736  STORE_FAST               'propArgs'

 L. 540      1738  LOAD_FAST                'propArgs'
             1740  LOAD_CONST               None
             1742  <117>                 0  ''
         1744_1746  POP_JUMP_IF_FALSE  1766  'to 1766'

 L. 541      1748  LOAD_STR                 'method'
             1750  STORE_FAST               'typename'

 L. 542      1752  LOAD_FAST                'self'
             1754  LOAD_METHOD              MakeFuncMethod
             1756  LOAD_FAST                'entry'
             1758  LOAD_STR                 '__len__'
             1760  CALL_METHOD_2         2  ''
             1762  STORE_FAST               'ret'
             1764  JUMP_FORWARD       1780  'to 1780'
           1766_0  COME_FROM          1744  '1744'

 L. 544      1766  LOAD_STR                 'property'
             1768  STORE_FAST               'typename'

 L. 545      1770  LOAD_STR                 '\tdef __len__(self):\n\t\treturn self._ApplyTypes_(*%s)'
             1772  LOAD_FAST                'propArgs'
             1774  BINARY_MODULO    
             1776  BUILD_LIST_1          1 
             1778  STORE_FAST               'ret'
           1780_0  COME_FROM          1764  '1764'

 L. 546      1780  LOAD_GLOBAL              print
             1782  LOAD_STR                 '\t#This class has Count() %s - allow len(ob) to provide this'
             1784  LOAD_FAST                'typename'
             1786  BINARY_MODULO    
             1788  LOAD_FAST                'stream'
             1790  LOAD_CONST               ('file',)
             1792  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1794  POP_TOP          

 L. 547      1796  LOAD_FAST                'ret'
             1798  GET_ITER         
             1800  FOR_ITER           1820  'to 1820'
             1802  STORE_FAST               'line'

 L. 548      1804  LOAD_GLOBAL              print
             1806  LOAD_FAST                'line'
             1808  LOAD_FAST                'stream'
             1810  LOAD_CONST               ('file',)
             1812  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1814  POP_TOP          
         1816_1818  JUMP_BACK          1800  'to 1800'

 L. 550      1820  LOAD_GLOBAL              print
             1822  LOAD_STR                 "\t#This class has a __len__ - this is needed so 'if object:' always returns TRUE."
             1824  LOAD_FAST                'stream'
             1826  LOAD_CONST               ('file',)
             1828  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1830  POP_TOP          

 L. 551      1832  LOAD_GLOBAL              print
             1834  LOAD_STR                 '\tdef __nonzero__(self):'
             1836  LOAD_FAST                'stream'
             1838  LOAD_CONST               ('file',)
             1840  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1842  POP_TOP          

 L. 552      1844  LOAD_GLOBAL              print
             1846  LOAD_STR                 '\t\treturn True'
             1848  LOAD_FAST                'stream'
             1850  LOAD_CONST               ('file',)
             1852  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1854  POP_TOP          
           1856_0  COME_FROM          1720  '1720'

Parse error at or near `<74>' instruction at offset 80


class CoClassItem(build.OleItem, WritableItem):
    order = 5
    typename = 'COCLASS'

    def __init__(self, typeinfo, attr, doc=None, sources=[], interfaces=[], bForUser=1):
        build.OleItem.__init__(self, doc)
        self.clsid = attr[0]
        self.sources = sources
        self.interfaces = interfaces
        self.bIsDispatch = 1

    def WriteClass--- This code section failed: ---

 L. 566         0  LOAD_FAST                'generator'
                2  LOAD_METHOD              checkWriteCoClassBaseClass
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 567         8  LOAD_FAST                'self'
               10  LOAD_ATTR                doc
               12  STORE_FAST               'doc'

 L. 568        14  LOAD_FAST                'generator'
               16  LOAD_ATTR                file
               18  STORE_FAST               'stream'

 L. 569        20  LOAD_FAST                'generator'
               22  LOAD_ATTR                generate_type
               24  LOAD_GLOBAL              GEN_DEMAND_CHILD
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_FALSE   170  'to 170'

 L. 571        30  BUILD_LIST_0          0 
               32  STORE_FAST               'referenced_items'

 L. 572        34  LOAD_FAST                'self'
               36  LOAD_ATTR                sources
               38  GET_ITER         
               40  FOR_ITER             60  'to 60'
               42  UNPACK_SEQUENCE_2     2 
               44  STORE_FAST               'ref'
               46  STORE_FAST               'flag'

 L. 573        48  LOAD_FAST                'referenced_items'
               50  LOAD_METHOD              append
               52  LOAD_FAST                'ref'
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          
               58  JUMP_BACK            40  'to 40'

 L. 574        60  LOAD_FAST                'self'
               62  LOAD_ATTR                interfaces
               64  GET_ITER         
               66  FOR_ITER             86  'to 86'
               68  UNPACK_SEQUENCE_2     2 
               70  STORE_FAST               'ref'
               72  STORE_FAST               'flag'

 L. 575        74  LOAD_FAST                'referenced_items'
               76  LOAD_METHOD              append
               78  LOAD_FAST                'ref'
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          
               84  JUMP_BACK            66  'to 66'

 L. 576        86  LOAD_GLOBAL              print
               88  LOAD_STR                 'import sys'
               90  LOAD_FAST                'stream'
               92  LOAD_CONST               ('file',)
               94  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               96  POP_TOP          

 L. 577        98  LOAD_FAST                'referenced_items'
              100  GET_ITER         
              102  FOR_ITER            170  'to 170'
              104  STORE_FAST               'ref'

 L. 578       106  LOAD_GLOBAL              print
              108  LOAD_STR                 "__import__('%s.%s')"
              110  LOAD_FAST                'generator'
              112  LOAD_ATTR                base_mod_name
              114  LOAD_FAST                'ref'
              116  LOAD_ATTR                python_name
              118  BUILD_TUPLE_2         2 
              120  BINARY_MODULO    
              122  LOAD_FAST                'stream'
              124  LOAD_CONST               ('file',)
              126  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              128  POP_TOP          

 L. 579       130  LOAD_GLOBAL              print
              132  LOAD_STR                 "%s = sys.modules['%s.%s'].%s"
              134  LOAD_FAST                'ref'
              136  LOAD_ATTR                python_name
              138  LOAD_FAST                'generator'
              140  LOAD_ATTR                base_mod_name
              142  LOAD_FAST                'ref'
              144  LOAD_ATTR                python_name
              146  LOAD_FAST                'ref'
              148  LOAD_ATTR                python_name
              150  BUILD_TUPLE_4         4 
              152  BINARY_MODULO    
              154  LOAD_FAST                'stream'
              156  LOAD_CONST               ('file',)
              158  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              160  POP_TOP          

 L. 581       162  LOAD_CONST               1
              164  LOAD_FAST                'ref'
              166  STORE_ATTR               bWritten
              168  JUMP_BACK           102  'to 102'
            170_0  COME_FROM            28  '28'

 L. 582       170  SETUP_FINALLY       204  'to 204'

 L. 583       172  LOAD_GLOBAL              pythoncom
              174  LOAD_METHOD              ProgIDFromCLSID
              176  LOAD_FAST                'self'
              178  LOAD_ATTR                clsid
              180  CALL_METHOD_1         1  ''
              182  STORE_FAST               'progId'

 L. 584       184  LOAD_GLOBAL              print
              186  LOAD_STR                 "# This CoClass is known by the name '%s'"
              188  LOAD_FAST                'progId'
              190  BINARY_MODULO    
              192  LOAD_FAST                'stream'
              194  LOAD_CONST               ('file',)
              196  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              198  POP_TOP          
              200  POP_BLOCK        
              202  JUMP_FORWARD        224  'to 224'
            204_0  COME_FROM_FINALLY   170  '170'

 L. 585       204  DUP_TOP          
              206  LOAD_GLOBAL              pythoncom
              208  LOAD_ATTR                com_error
              210  <121>               222  ''
              212  POP_TOP          
              214  POP_TOP          
              216  POP_TOP          

 L. 586       218  POP_EXCEPT       
              220  JUMP_FORWARD        224  'to 224'
              222  <48>             
            224_0  COME_FROM           220  '220'
            224_1  COME_FROM           202  '202'

 L. 587       224  LOAD_GLOBAL              print
              226  LOAD_STR                 'class %s(CoClassBaseClass): # A CoClass'
              228  LOAD_FAST                'self'
              230  LOAD_ATTR                python_name
              232  BINARY_MODULO    
              234  LOAD_FAST                'stream'
              236  LOAD_CONST               ('file',)
              238  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              240  POP_TOP          

 L. 588       242  LOAD_FAST                'doc'
          244_246  POP_JUMP_IF_FALSE   278  'to 278'
              248  LOAD_FAST                'doc'
              250  LOAD_CONST               1
              252  BINARY_SUBSCR    
          254_256  POP_JUMP_IF_FALSE   278  'to 278'
              258  LOAD_GLOBAL              print
              260  LOAD_STR                 '\t# '
              262  LOAD_FAST                'doc'
              264  LOAD_CONST               1
              266  BINARY_SUBSCR    
              268  BINARY_ADD       
              270  LOAD_FAST                'stream'
              272  LOAD_CONST               ('file',)
              274  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              276  POP_TOP          
            278_0  COME_FROM           254  '254'
            278_1  COME_FROM           244  '244'

 L. 589       278  LOAD_GLOBAL              print
              280  LOAD_STR                 '\tCLSID = %r'
              282  LOAD_FAST                'self'
              284  LOAD_ATTR                clsid
              286  BUILD_TUPLE_1         1 
              288  BINARY_MODULO    
              290  LOAD_FAST                'stream'
              292  LOAD_CONST               ('file',)
              294  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              296  POP_TOP          

 L. 590       298  LOAD_GLOBAL              print
              300  LOAD_STR                 '\tcoclass_sources = ['
              302  LOAD_FAST                'stream'
              304  LOAD_CONST               ('file',)
              306  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              308  POP_TOP          

 L. 591       310  LOAD_CONST               None
              312  STORE_FAST               'defItem'

 L. 592       314  LOAD_FAST                'self'
              316  LOAD_ATTR                sources
              318  GET_ITER         
              320  FOR_ITER            394  'to 394'
              322  UNPACK_SEQUENCE_2     2 
              324  STORE_FAST               'item'
              326  STORE_FAST               'flag'

 L. 593       328  LOAD_FAST                'flag'
              330  LOAD_GLOBAL              pythoncom
              332  LOAD_ATTR                IMPLTYPEFLAG_FDEFAULT
              334  BINARY_AND       
          336_338  POP_JUMP_IF_FALSE   344  'to 344'

 L. 594       340  LOAD_FAST                'item'
              342  STORE_FAST               'defItem'
            344_0  COME_FROM           336  '336'

 L. 597       344  LOAD_FAST                'item'
              346  LOAD_ATTR                bWritten
          348_350  POP_JUMP_IF_FALSE   360  'to 360'
              352  LOAD_FAST                'item'
              354  LOAD_ATTR                python_name
              356  STORE_FAST               'key'
              358  JUMP_FORWARD        374  'to 374'
            360_0  COME_FROM           348  '348'

 L. 598       360  LOAD_GLOBAL              repr
              362  LOAD_GLOBAL              str
              364  LOAD_FAST                'item'
              366  LOAD_ATTR                clsid
              368  CALL_FUNCTION_1       1  ''
              370  CALL_FUNCTION_1       1  ''
              372  STORE_FAST               'key'
            374_0  COME_FROM           358  '358'

 L. 599       374  LOAD_GLOBAL              print
              376  LOAD_STR                 '\t\t%s,'
              378  LOAD_FAST                'key'
              380  BINARY_MODULO    
              382  LOAD_FAST                'stream'
              384  LOAD_CONST               ('file',)
              386  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              388  POP_TOP          
          390_392  JUMP_BACK           320  'to 320'

 L. 600       394  LOAD_GLOBAL              print
              396  LOAD_STR                 '\t]'
              398  LOAD_FAST                'stream'
              400  LOAD_CONST               ('file',)
              402  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              404  POP_TOP          

 L. 601       406  LOAD_FAST                'defItem'
          408_410  POP_JUMP_IF_FALSE   460  'to 460'

 L. 602       412  LOAD_FAST                'defItem'
              414  LOAD_ATTR                bWritten
          416_418  POP_JUMP_IF_FALSE   428  'to 428'
              420  LOAD_FAST                'defItem'
              422  LOAD_ATTR                python_name
              424  STORE_FAST               'defName'
              426  JUMP_FORWARD        442  'to 442'
            428_0  COME_FROM           416  '416'

 L. 603       428  LOAD_GLOBAL              repr
              430  LOAD_GLOBAL              str
              432  LOAD_FAST                'defItem'
              434  LOAD_ATTR                clsid
              436  CALL_FUNCTION_1       1  ''
              438  CALL_FUNCTION_1       1  ''
              440  STORE_FAST               'defName'
            442_0  COME_FROM           426  '426'

 L. 604       442  LOAD_GLOBAL              print
              444  LOAD_STR                 '\tdefault_source = %s'
              446  LOAD_FAST                'defName'
              448  BUILD_TUPLE_1         1 
              450  BINARY_MODULO    
              452  LOAD_FAST                'stream'
              454  LOAD_CONST               ('file',)
              456  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              458  POP_TOP          
            460_0  COME_FROM           408  '408'

 L. 605       460  LOAD_GLOBAL              print
              462  LOAD_STR                 '\tcoclass_interfaces = ['
              464  LOAD_FAST                'stream'
              466  LOAD_CONST               ('file',)
              468  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              470  POP_TOP          

 L. 606       472  LOAD_CONST               None
              474  STORE_FAST               'defItem'

 L. 607       476  LOAD_FAST                'self'
              478  LOAD_ATTR                interfaces
              480  GET_ITER         
              482  FOR_ITER            558  'to 558'
              484  UNPACK_SEQUENCE_2     2 
              486  STORE_FAST               'item'
              488  STORE_FAST               'flag'

 L. 608       490  LOAD_FAST                'flag'
              492  LOAD_GLOBAL              pythoncom
              494  LOAD_ATTR                IMPLTYPEFLAG_FDEFAULT
              496  BINARY_AND       
          498_500  POP_JUMP_IF_FALSE   506  'to 506'

 L. 609       502  LOAD_FAST                'item'
              504  STORE_FAST               'defItem'
            506_0  COME_FROM           498  '498'

 L. 611       506  LOAD_FAST                'item'
              508  LOAD_ATTR                bWritten
          510_512  POP_JUMP_IF_FALSE   522  'to 522'
              514  LOAD_FAST                'item'
              516  LOAD_ATTR                python_name
              518  STORE_FAST               'key'
              520  JUMP_FORWARD        536  'to 536'
            522_0  COME_FROM           510  '510'

 L. 612       522  LOAD_GLOBAL              repr
              524  LOAD_GLOBAL              str
              526  LOAD_FAST                'item'
              528  LOAD_ATTR                clsid
              530  CALL_FUNCTION_1       1  ''
              532  CALL_FUNCTION_1       1  ''
              534  STORE_FAST               'key'
            536_0  COME_FROM           520  '520'

 L. 613       536  LOAD_GLOBAL              print
              538  LOAD_STR                 '\t\t%s,'
              540  LOAD_FAST                'key'
              542  BUILD_TUPLE_1         1 
              544  BINARY_MODULO    
              546  LOAD_FAST                'stream'
              548  LOAD_CONST               ('file',)
              550  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              552  POP_TOP          
          554_556  JUMP_BACK           482  'to 482'

 L. 614       558  LOAD_GLOBAL              print
              560  LOAD_STR                 '\t]'
              562  LOAD_FAST                'stream'
              564  LOAD_CONST               ('file',)
              566  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              568  POP_TOP          

 L. 615       570  LOAD_FAST                'defItem'
          572_574  POP_JUMP_IF_FALSE   624  'to 624'

 L. 616       576  LOAD_FAST                'defItem'
              578  LOAD_ATTR                bWritten
          580_582  POP_JUMP_IF_FALSE   592  'to 592'
              584  LOAD_FAST                'defItem'
              586  LOAD_ATTR                python_name
              588  STORE_FAST               'defName'
              590  JUMP_FORWARD        606  'to 606'
            592_0  COME_FROM           580  '580'

 L. 617       592  LOAD_GLOBAL              repr
              594  LOAD_GLOBAL              str
              596  LOAD_FAST                'defItem'
              598  LOAD_ATTR                clsid
              600  CALL_FUNCTION_1       1  ''
              602  CALL_FUNCTION_1       1  ''
              604  STORE_FAST               'defName'
            606_0  COME_FROM           590  '590'

 L. 618       606  LOAD_GLOBAL              print
              608  LOAD_STR                 '\tdefault_interface = %s'
              610  LOAD_FAST                'defName'
              612  BUILD_TUPLE_1         1 
              614  BINARY_MODULO    
              616  LOAD_FAST                'stream'
              618  LOAD_CONST               ('file',)
              620  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              622  POP_TOP          
            624_0  COME_FROM           572  '572'

 L. 619       624  LOAD_CONST               1
              626  LOAD_FAST                'self'
              628  STORE_ATTR               bWritten

 L. 620       630  LOAD_GLOBAL              print
              632  LOAD_FAST                'stream'
              634  LOAD_CONST               ('file',)
              636  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              638  POP_TOP          

Parse error at or near `<121>' instruction at offset 210


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

    def __init__--- This code section failed: ---

 L. 652         0  LOAD_FAST                'bUnicodeToString'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  <74>             
               10  LOAD_STR                 'this is deprecated and will go away'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 653        16  LOAD_CONST               0
               18  LOAD_FAST                'self'
               20  STORE_ATTR               bHaveWrittenDispatchBaseClass

 L. 654        22  LOAD_CONST               0
               24  LOAD_FAST                'self'
               26  STORE_ATTR               bHaveWrittenCoClassBaseClass

 L. 655        28  LOAD_CONST               0
               30  LOAD_FAST                'self'
               32  STORE_ATTR               bHaveWrittenEventBaseClass

 L. 656        34  LOAD_FAST                'typelib'
               36  LOAD_FAST                'self'
               38  STORE_ATTR               typelib

 L. 657        40  LOAD_FAST                'sourceFilename'
               42  LOAD_FAST                'self'
               44  STORE_ATTR               sourceFilename

 L. 658        46  LOAD_FAST                'bBuildHidden'
               48  LOAD_FAST                'self'
               50  STORE_ATTR               bBuildHidden

 L. 659        52  LOAD_FAST                'progressObject'
               54  LOAD_FAST                'self'
               56  STORE_ATTR               progress

 L. 661        58  LOAD_CONST               None
               60  LOAD_FAST                'self'
               62  STORE_ATTR               file

Parse error at or near `None' instruction at offset -1

    def CollectOleItemInfosFromType(self):
        ret = []
        for i in range(self.typelib.GetTypeInfoCount()):
            info = self.typelib.GetTypeInfoi
            infotype = self.typelib.GetTypeInfoTypei
            doc = self.typelib.GetDocumentationi
            attr = info.GetTypeAttr()
            ret.append(info, infotype, doc, attr)
        else:
            return ret

    def _Build_CoClass--- This code section failed: ---

 L. 674         0  LOAD_FAST                'type_info_tuple'
                2  UNPACK_SEQUENCE_4     4 
                4  STORE_FAST               'info'
                6  STORE_FAST               'infotype'
                8  STORE_FAST               'doc'
               10  STORE_FAST               'attr'

 L. 676        12  BUILD_LIST_0          0 
               14  STORE_FAST               'child_infos'

 L. 677        16  LOAD_GLOBAL              range
               18  LOAD_FAST                'attr'
               20  LOAD_CONST               8
               22  BINARY_SUBSCR    
               24  CALL_FUNCTION_1       1  ''
               26  GET_ITER         
               28  FOR_ITER            128  'to 128'
               30  STORE_FAST               'j'

 L. 678        32  LOAD_FAST                'info'
               34  LOAD_METHOD              GetImplTypeFlags
               36  LOAD_FAST                'j'
               38  CALL_METHOD_1         1  ''
               40  STORE_FAST               'flags'

 L. 679        42  SETUP_FINALLY        64  'to 64'

 L. 680        44  LOAD_FAST                'info'
               46  LOAD_METHOD              GetRefTypeInfo
               48  LOAD_FAST                'info'
               50  LOAD_METHOD              GetRefTypeOfImplType
               52  LOAD_FAST                'j'
               54  CALL_METHOD_1         1  ''
               56  CALL_METHOD_1         1  ''
               58  STORE_FAST               'refType'
               60  POP_BLOCK        
               62  JUMP_FORWARD         88  'to 88'
             64_0  COME_FROM_FINALLY    42  '42'

 L. 681        64  DUP_TOP          
               66  LOAD_GLOBAL              pythoncom
               68  LOAD_ATTR                com_error
               70  <121>                86  ''
               72  POP_TOP          
               74  POP_TOP          
               76  POP_TOP          

 L. 683        78  POP_EXCEPT       
               80  JUMP_BACK            28  'to 28'
               82  POP_EXCEPT       
               84  JUMP_FORWARD         88  'to 88'
               86  <48>             
             88_0  COME_FROM            84  '84'
             88_1  COME_FROM            62  '62'

 L. 684        88  LOAD_FAST                'refType'
               90  LOAD_METHOD              GetTypeAttr
               92  CALL_METHOD_0         0  ''
               94  STORE_FAST               'refAttr'

 L. 685        96  LOAD_FAST                'child_infos'
               98  LOAD_METHOD              append
              100  LOAD_FAST                'info'
              102  LOAD_FAST                'refAttr'
              104  LOAD_ATTR                typekind
              106  LOAD_FAST                'refType'
              108  LOAD_FAST                'refType'
              110  LOAD_METHOD              GetDocumentation
              112  LOAD_CONST               -1
              114  CALL_METHOD_1         1  ''
              116  LOAD_FAST                'refAttr'
              118  LOAD_FAST                'flags'
              120  BUILD_TUPLE_6         6 
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          
              126  JUMP_BACK            28  'to 28'

 L. 688       128  LOAD_GLOBAL              CoClassItem
              130  LOAD_FAST                'info'
              132  LOAD_FAST                'attr'
              134  LOAD_FAST                'doc'
              136  CALL_FUNCTION_3       3  ''
              138  STORE_FAST               'newItem'

 L. 689       140  LOAD_FAST                'newItem'
              142  LOAD_FAST                'child_infos'
              144  BUILD_TUPLE_2         2 
              146  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 70

    def _Build_CoClassChildren--- This code section failed: ---

 L. 692         0  BUILD_MAP_0           0 
                2  STORE_FAST               'sources'

 L. 693         4  BUILD_MAP_0           0 
                6  STORE_FAST               'interfaces'

 L. 694         8  LOAD_FAST                'coclass_info'
               10  GET_ITER         
             12_0  COME_FROM           188  '188'
             12_1  COME_FROM           174  '174'
             12_2  COME_FROM            64  '64'
             12_3  COME_FROM            50  '50'
               12  FOR_ITER            256  'to 256'
               14  UNPACK_SEQUENCE_6     6 
               16  STORE_FAST               'info'
               18  STORE_FAST               'info_type'
               20  STORE_FAST               'refType'
               22  STORE_FAST               'doc'
               24  STORE_FAST               'refAttr'
               26  STORE_FAST               'flags'

 L. 696        28  LOAD_FAST                'refAttr'
               30  LOAD_ATTR                typekind
               32  LOAD_GLOBAL              pythoncom
               34  LOAD_ATTR                TKIND_DISPATCH
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_TRUE     66  'to 66'

 L. 697        40  LOAD_FAST                'refAttr'
               42  LOAD_ATTR                typekind
               44  LOAD_GLOBAL              pythoncom
               46  LOAD_ATTR                TKIND_INTERFACE
               48  COMPARE_OP               ==

 L. 696        50  POP_JUMP_IF_FALSE    12  'to 12'

 L. 697        52  LOAD_FAST                'refAttr'
               54  LOAD_CONST               11
               56  BINARY_SUBSCR    
               58  LOAD_GLOBAL              pythoncom
               60  LOAD_ATTR                TYPEFLAG_FDISPATCHABLE
               62  BINARY_AND       

 L. 696        64  POP_JUMP_IF_FALSE    12  'to 12'
             66_0  COME_FROM            38  '38'

 L. 698        66  LOAD_FAST                'refAttr'
               68  LOAD_CONST               0
               70  BINARY_SUBSCR    
               72  STORE_FAST               'clsid'

 L. 699        74  LOAD_FAST                'clsid'
               76  LOAD_FAST                'oleItems'
               78  <118>                 0  ''
               80  POP_JUMP_IF_FALSE    92  'to 92'

 L. 700        82  LOAD_FAST                'oleItems'
               84  LOAD_FAST                'clsid'
               86  BINARY_SUBSCR    
               88  STORE_FAST               'dispItem'
               90  JUMP_FORWARD        114  'to 114'
             92_0  COME_FROM            80  '80'

 L. 702        92  LOAD_GLOBAL              DispatchItem
               94  LOAD_FAST                'refType'
               96  LOAD_FAST                'refAttr'
               98  LOAD_FAST                'doc'
              100  CALL_FUNCTION_3       3  ''
              102  STORE_FAST               'dispItem'

 L. 703       104  LOAD_FAST                'dispItem'
              106  LOAD_FAST                'oleItems'
              108  LOAD_FAST                'dispItem'
              110  LOAD_ATTR                clsid
              112  STORE_SUBSCR     
            114_0  COME_FROM            90  '90'

 L. 704       114  LOAD_FAST                'coclass'
              116  LOAD_ATTR                clsid
              118  LOAD_FAST                'dispItem'
              120  STORE_ATTR               coclass_clsid

 L. 705       122  LOAD_FAST                'flags'
              124  LOAD_GLOBAL              pythoncom
              126  LOAD_ATTR                IMPLTYPEFLAG_FSOURCE
              128  BINARY_AND       
              130  POP_JUMP_IF_FALSE   154  'to 154'

 L. 706       132  LOAD_CONST               1
              134  LOAD_FAST                'dispItem'
              136  STORE_ATTR               bIsSink

 L. 707       138  LOAD_FAST                'dispItem'
              140  LOAD_FAST                'flags'
              142  BUILD_TUPLE_2         2 
              144  LOAD_FAST                'sources'
              146  LOAD_FAST                'dispItem'
              148  LOAD_ATTR                clsid
              150  STORE_SUBSCR     
              152  JUMP_FORWARD        168  'to 168'
            154_0  COME_FROM           130  '130'

 L. 709       154  LOAD_FAST                'dispItem'
              156  LOAD_FAST                'flags'
              158  BUILD_TUPLE_2         2 
              160  LOAD_FAST                'interfaces'
              162  LOAD_FAST                'dispItem'
              164  LOAD_ATTR                clsid
              166  STORE_SUBSCR     
            168_0  COME_FROM           152  '152'

 L. 711       168  LOAD_FAST                'clsid'
              170  LOAD_FAST                'vtableItems'
              172  <118>                 1  ''
              174  POP_JUMP_IF_FALSE    12  'to 12'
              176  LOAD_FAST                'refAttr'
              178  LOAD_CONST               11
              180  BINARY_SUBSCR    
              182  LOAD_GLOBAL              pythoncom
              184  LOAD_ATTR                TYPEFLAG_FDUAL
              186  BINARY_AND       
              188  POP_JUMP_IF_FALSE    12  'to 12'

 L. 712       190  LOAD_FAST                'refType'
              192  LOAD_METHOD              GetRefTypeInfo
              194  LOAD_FAST                'refType'
              196  LOAD_METHOD              GetRefTypeOfImplType
              198  LOAD_CONST               -1
              200  CALL_METHOD_1         1  ''
              202  CALL_METHOD_1         1  ''
              204  STORE_FAST               'refType'

 L. 713       206  LOAD_FAST                'refType'
              208  LOAD_METHOD              GetTypeAttr
              210  CALL_METHOD_0         0  ''
              212  STORE_FAST               'refAttr'

 L. 714       214  LOAD_FAST                'refAttr'
              216  LOAD_ATTR                typekind
              218  LOAD_GLOBAL              pythoncom
              220  LOAD_ATTR                TKIND_INTERFACE
              222  COMPARE_OP               ==
              224  POP_JUMP_IF_TRUE    234  'to 234'
              226  <74>             
              228  LOAD_STR                 'must be interface bynow!'
              230  CALL_FUNCTION_1       1  ''
              232  RAISE_VARARGS_1       1  'exception instance'
            234_0  COME_FROM           224  '224'

 L. 715       234  LOAD_GLOBAL              VTableItem
              236  LOAD_FAST                'refType'
              238  LOAD_FAST                'refAttr'
              240  LOAD_FAST                'doc'
              242  CALL_FUNCTION_3       3  ''
              244  STORE_FAST               'vtableItem'

 L. 716       246  LOAD_FAST                'vtableItem'
              248  LOAD_FAST                'vtableItems'
              250  LOAD_FAST                'clsid'
              252  STORE_SUBSCR     
              254  JUMP_BACK            12  'to 12'

 L. 717       256  LOAD_GLOBAL              list
              258  LOAD_FAST                'sources'
              260  LOAD_METHOD              values
              262  CALL_METHOD_0         0  ''
              264  CALL_FUNCTION_1       1  ''
              266  LOAD_FAST                'coclass'
              268  STORE_ATTR               sources

 L. 718       270  LOAD_GLOBAL              list
              272  LOAD_FAST                'interfaces'
              274  LOAD_METHOD              values
              276  CALL_METHOD_0         0  ''
              278  CALL_FUNCTION_1       1  ''
              280  LOAD_FAST                'coclass'
              282  STORE_ATTR               interfaces

Parse error at or near `<118>' instruction at offset 78

    def _Build_Interface--- This code section failed: ---

 L. 721         0  LOAD_FAST                'type_info_tuple'
                2  UNPACK_SEQUENCE_4     4 
                4  STORE_FAST               'info'
                6  STORE_FAST               'infotype'
                8  STORE_FAST               'doc'
               10  STORE_FAST               'attr'

 L. 722        12  LOAD_CONST               None
               14  DUP_TOP          
               16  STORE_FAST               'oleItem'
               18  STORE_FAST               'vtableItem'

 L. 723        20  LOAD_FAST                'infotype'
               22  LOAD_GLOBAL              pythoncom
               24  LOAD_ATTR                TKIND_DISPATCH
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_TRUE     54  'to 54'

 L. 724        30  LOAD_FAST                'infotype'
               32  LOAD_GLOBAL              pythoncom
               34  LOAD_ATTR                TKIND_INTERFACE
               36  COMPARE_OP               ==

 L. 723        38  POP_JUMP_IF_FALSE   118  'to 118'

 L. 724        40  LOAD_FAST                'attr'
               42  LOAD_CONST               11
               44  BINARY_SUBSCR    
               46  LOAD_GLOBAL              pythoncom
               48  LOAD_ATTR                TYPEFLAG_FDISPATCHABLE
               50  BINARY_AND       

 L. 723        52  POP_JUMP_IF_FALSE   118  'to 118'
             54_0  COME_FROM            28  '28'

 L. 725        54  LOAD_GLOBAL              DispatchItem
               56  LOAD_FAST                'info'
               58  LOAD_FAST                'attr'
               60  LOAD_FAST                'doc'
               62  CALL_FUNCTION_3       3  ''
               64  STORE_FAST               'oleItem'

 L. 727        66  LOAD_FAST                'attr'
               68  LOAD_ATTR                wTypeFlags
               70  LOAD_GLOBAL              pythoncom
               72  LOAD_ATTR                TYPEFLAG_FDUAL
               74  BINARY_AND       
               76  POP_JUMP_IF_FALSE   114  'to 114'

 L. 729        78  LOAD_FAST                'info'
               80  LOAD_METHOD              GetRefTypeOfImplType
               82  LOAD_CONST               -1
               84  CALL_METHOD_1         1  ''
               86  STORE_FAST               'refhtype'

 L. 730        88  LOAD_FAST                'info'
               90  LOAD_METHOD              GetRefTypeInfo
               92  LOAD_FAST                'refhtype'
               94  CALL_METHOD_1         1  ''
               96  STORE_FAST               'info'

 L. 731        98  LOAD_FAST                'info'
              100  LOAD_METHOD              GetTypeAttr
              102  CALL_METHOD_0         0  ''
              104  STORE_FAST               'attr'

 L. 732       106  LOAD_GLOBAL              pythoncom
              108  LOAD_ATTR                TKIND_INTERFACE
              110  STORE_FAST               'infotype'
              112  JUMP_FORWARD        118  'to 118'
            114_0  COME_FROM            76  '76'

 L. 734       114  LOAD_CONST               None
              116  STORE_FAST               'infotype'
            118_0  COME_FROM           112  '112'
            118_1  COME_FROM            52  '52'
            118_2  COME_FROM            38  '38'

 L. 735       118  LOAD_FAST                'infotype'
              120  LOAD_CONST               None
              122  LOAD_GLOBAL              pythoncom
              124  LOAD_ATTR                TKIND_INTERFACE
              126  BUILD_TUPLE_2         2 
              128  <118>                 0  ''
              130  POP_JUMP_IF_TRUE    140  'to 140'
              132  <74>             
              134  LOAD_STR                 'Must be a real interface at this point'
              136  CALL_FUNCTION_1       1  ''
              138  RAISE_VARARGS_1       1  'exception instance'
            140_0  COME_FROM           130  '130'

 L. 736       140  LOAD_FAST                'infotype'
              142  LOAD_GLOBAL              pythoncom
              144  LOAD_ATTR                TKIND_INTERFACE
              146  COMPARE_OP               ==
              148  POP_JUMP_IF_FALSE   162  'to 162'

 L. 737       150  LOAD_GLOBAL              VTableItem
              152  LOAD_FAST                'info'
              154  LOAD_FAST                'attr'
              156  LOAD_FAST                'doc'
              158  CALL_FUNCTION_3       3  ''
              160  STORE_FAST               'vtableItem'
            162_0  COME_FROM           148  '148'

 L. 738       162  LOAD_FAST                'oleItem'
              164  LOAD_FAST                'vtableItem'
              166  BUILD_TUPLE_2         2 
              168  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 128

    def BuildOleItemsFromType--- This code section failed: ---

 L. 741         0  LOAD_FAST                'self'
                2  LOAD_ATTR                bBuildHidden
                4  POP_JUMP_IF_TRUE     14  'to 14'
                6  <74>             
                8  LOAD_STR                 'This code doesnt look at the hidden flag - I thought everyone set it true!?!?!'
               10  CALL_FUNCTION_1       1  ''
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             4  '4'

 L. 742        14  BUILD_MAP_0           0 
               16  STORE_FAST               'oleItems'

 L. 743        18  BUILD_MAP_0           0 
               20  STORE_FAST               'enumItems'

 L. 744        22  BUILD_MAP_0           0 
               24  STORE_FAST               'recordItems'

 L. 745        26  BUILD_MAP_0           0 
               28  STORE_FAST               'vtableItems'

 L. 747        30  LOAD_FAST                'self'
               32  LOAD_METHOD              CollectOleItemInfosFromType
               34  CALL_METHOD_0         0  ''
               36  GET_ITER         
            38_40  FOR_ITER            306  'to 306'
               42  STORE_FAST               'type_info_tuple'

 L. 748        44  LOAD_FAST                'type_info_tuple'
               46  UNPACK_SEQUENCE_4     4 
               48  STORE_FAST               'info'
               50  STORE_FAST               'infotype'
               52  STORE_FAST               'doc'
               54  STORE_FAST               'attr'

 L. 749        56  LOAD_FAST                'attr'
               58  LOAD_CONST               0
               60  BINARY_SUBSCR    
               62  STORE_FAST               'clsid'

 L. 750        64  LOAD_FAST                'infotype'
               66  LOAD_GLOBAL              pythoncom
               68  LOAD_ATTR                TKIND_ENUM
               70  COMPARE_OP               ==
               72  POP_JUMP_IF_TRUE     84  'to 84'
               74  LOAD_FAST                'infotype'
               76  LOAD_GLOBAL              pythoncom
               78  LOAD_ATTR                TKIND_MODULE
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_FALSE   112  'to 112'
             84_0  COME_FROM            72  '72'

 L. 751        84  LOAD_GLOBAL              EnumerationItem
               86  LOAD_FAST                'info'
               88  LOAD_FAST                'attr'
               90  LOAD_FAST                'doc'
               92  CALL_FUNCTION_3       3  ''
               94  STORE_FAST               'newItem'

 L. 752        96  LOAD_FAST                'newItem'
               98  LOAD_FAST                'enumItems'
              100  LOAD_FAST                'newItem'
              102  LOAD_ATTR                doc
              104  LOAD_CONST               0
              106  BINARY_SUBSCR    
              108  STORE_SUBSCR     
              110  JUMP_BACK            38  'to 38'
            112_0  COME_FROM            82  '82'

 L. 755       112  LOAD_FAST                'infotype'
              114  LOAD_GLOBAL              pythoncom
              116  LOAD_ATTR                TKIND_DISPATCH
              118  LOAD_GLOBAL              pythoncom
              120  LOAD_ATTR                TKIND_INTERFACE
              122  BUILD_TUPLE_2         2 
              124  <118>                 0  ''
              126  POP_JUMP_IF_FALSE   176  'to 176'

 L. 756       128  LOAD_FAST                'clsid'
              130  LOAD_FAST                'oleItems'
              132  <118>                 1  ''
              134  POP_JUMP_IF_FALSE   174  'to 174'

 L. 757       136  LOAD_FAST                'self'
              138  LOAD_METHOD              _Build_Interface
              140  LOAD_FAST                'type_info_tuple'
              142  CALL_METHOD_1         1  ''
              144  UNPACK_SEQUENCE_2     2 
              146  STORE_FAST               'oleItem'
              148  STORE_FAST               'vtableItem'

 L. 758       150  LOAD_FAST                'oleItem'
              152  LOAD_FAST                'oleItems'
              154  LOAD_FAST                'clsid'
              156  STORE_SUBSCR     

 L. 759       158  LOAD_FAST                'vtableItem'
              160  LOAD_CONST               None
              162  <117>                 1  ''
              164  POP_JUMP_IF_FALSE   174  'to 174'

 L. 760       166  LOAD_FAST                'vtableItem'
              168  LOAD_FAST                'vtableItems'
              170  LOAD_FAST                'clsid'
              172  STORE_SUBSCR     
            174_0  COME_FROM           164  '164'
            174_1  COME_FROM           134  '134'
              174  JUMP_BACK            38  'to 38'
            176_0  COME_FROM           126  '126'

 L. 761       176  LOAD_FAST                'infotype'
              178  LOAD_GLOBAL              pythoncom
              180  LOAD_ATTR                TKIND_RECORD
              182  COMPARE_OP               ==
              184  POP_JUMP_IF_TRUE    196  'to 196'
              186  LOAD_FAST                'infotype'
              188  LOAD_GLOBAL              pythoncom
              190  LOAD_ATTR                TKIND_UNION
              192  COMPARE_OP               ==
              194  POP_JUMP_IF_FALSE   220  'to 220'
            196_0  COME_FROM           184  '184'

 L. 762       196  LOAD_GLOBAL              RecordItem
              198  LOAD_FAST                'info'
              200  LOAD_FAST                'attr'
              202  LOAD_FAST                'doc'
              204  CALL_FUNCTION_3       3  ''
              206  STORE_FAST               'newItem'

 L. 763       208  LOAD_FAST                'newItem'
              210  LOAD_FAST                'recordItems'
              212  LOAD_FAST                'newItem'
              214  LOAD_ATTR                clsid
              216  STORE_SUBSCR     
              218  JUMP_BACK            38  'to 38'
            220_0  COME_FROM           194  '194'

 L. 764       220  LOAD_FAST                'infotype'
              222  LOAD_GLOBAL              pythoncom
              224  LOAD_ATTR                TKIND_ALIAS
              226  COMPARE_OP               ==
              228  POP_JUMP_IF_FALSE   234  'to 234'

 L. 766       230  CONTINUE             38  'to 38'
              232  JUMP_BACK            38  'to 38'
            234_0  COME_FROM           228  '228'

 L. 767       234  LOAD_FAST                'infotype'
              236  LOAD_GLOBAL              pythoncom
              238  LOAD_ATTR                TKIND_COCLASS
              240  COMPARE_OP               ==
          242_244  POP_JUMP_IF_FALSE   288  'to 288'

 L. 768       246  LOAD_FAST                'self'
              248  LOAD_METHOD              _Build_CoClass
              250  LOAD_FAST                'type_info_tuple'
              252  CALL_METHOD_1         1  ''
              254  UNPACK_SEQUENCE_2     2 
              256  STORE_FAST               'newItem'
              258  STORE_FAST               'child_infos'

 L. 769       260  LOAD_FAST                'self'
              262  LOAD_METHOD              _Build_CoClassChildren
              264  LOAD_FAST                'newItem'
              266  LOAD_FAST                'child_infos'
              268  LOAD_FAST                'oleItems'
              270  LOAD_FAST                'vtableItems'
              272  CALL_METHOD_4         4  ''
              274  POP_TOP          

 L. 770       276  LOAD_FAST                'newItem'
              278  LOAD_FAST                'oleItems'
              280  LOAD_FAST                'newItem'
              282  LOAD_ATTR                clsid
              284  STORE_SUBSCR     
              286  JUMP_BACK            38  'to 38'
            288_0  COME_FROM           242  '242'

 L. 772       288  LOAD_FAST                'self'
              290  LOAD_ATTR                progress
              292  LOAD_METHOD              LogWarning
              294  LOAD_STR                 'Unknown TKIND found: %d'
              296  LOAD_FAST                'infotype'
              298  BINARY_MODULO    
              300  CALL_METHOD_1         1  ''
              302  POP_TOP          
              304  JUMP_BACK            38  'to 38'

 L. 774       306  LOAD_FAST                'oleItems'
              308  LOAD_FAST                'enumItems'
              310  LOAD_FAST                'recordItems'
              312  LOAD_FAST                'vtableItems'
              314  BUILD_TUPLE_4         4 
              316  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def open_writer(self, filename, encoding='mbcs'):
        temp_filename = self.get_temp_filenamefilename
        return open(temp_filename, 'wt', encoding=encoding)

    def finish_writer--- This code section failed: ---

 L. 789         0  LOAD_FAST                'f'
                2  LOAD_METHOD              close
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 790         8  SETUP_FINALLY        24  'to 24'

 L. 791        10  LOAD_GLOBAL              os
               12  LOAD_METHOD              unlink
               14  LOAD_FAST                'filename'
               16  CALL_METHOD_1         1  ''
               18  POP_TOP          
               20  POP_BLOCK        
               22  JUMP_FORWARD         44  'to 44'
             24_0  COME_FROM_FINALLY     8  '8'

 L. 792        24  DUP_TOP          
               26  LOAD_GLOBAL              os
               28  LOAD_ATTR                error
               30  <121>                42  ''
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 793        38  POP_EXCEPT       
               40  JUMP_FORWARD         44  'to 44'
               42  <48>             
             44_0  COME_FROM            40  '40'
             44_1  COME_FROM            22  '22'

 L. 794        44  LOAD_FAST                'self'
               46  LOAD_METHOD              get_temp_filename
               48  LOAD_FAST                'filename'
               50  CALL_METHOD_1         1  ''
               52  STORE_FAST               'temp_filename'

 L. 795        54  LOAD_FAST                'worked'
               56  POP_JUMP_IF_FALSE   146  'to 146'

 L. 796        58  SETUP_FINALLY        76  'to 76'

 L. 797        60  LOAD_GLOBAL              os
               62  LOAD_METHOD              rename
               64  LOAD_FAST                'temp_filename'
               66  LOAD_FAST                'filename'
               68  CALL_METHOD_2         2  ''
               70  POP_TOP          
               72  POP_BLOCK        
               74  JUMP_ABSOLUTE       156  'to 156'
             76_0  COME_FROM_FINALLY    58  '58'

 L. 798        76  DUP_TOP          
               78  LOAD_GLOBAL              os
               80  LOAD_ATTR                error
               82  <121>               142  ''
               84  POP_TOP          
               86  POP_TOP          
               88  POP_TOP          

 L. 812        90  SETUP_FINALLY       106  'to 106'

 L. 813        92  LOAD_GLOBAL              os
               94  LOAD_METHOD              unlink
               96  LOAD_FAST                'filename'
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          
              102  POP_BLOCK        
              104  JUMP_FORWARD        126  'to 126'
            106_0  COME_FROM_FINALLY    90  '90'

 L. 814       106  DUP_TOP          
              108  LOAD_GLOBAL              os
              110  LOAD_ATTR                error
              112  <121>               124  ''
              114  POP_TOP          
              116  POP_TOP          
              118  POP_TOP          

 L. 815       120  POP_EXCEPT       
              122  JUMP_FORWARD        126  'to 126'
              124  <48>             
            126_0  COME_FROM           122  '122'
            126_1  COME_FROM           104  '104'

 L. 816       126  LOAD_GLOBAL              os
              128  LOAD_METHOD              rename
              130  LOAD_FAST                'temp_filename'
              132  LOAD_FAST                'filename'
              134  CALL_METHOD_2         2  ''
              136  POP_TOP          
              138  POP_EXCEPT       
              140  JUMP_ABSOLUTE       156  'to 156'
              142  <48>             
              144  JUMP_FORWARD        156  'to 156'
            146_0  COME_FROM            56  '56'

 L. 818       146  LOAD_GLOBAL              os
              148  LOAD_METHOD              unlink
              150  LOAD_FAST                'temp_filename'
              152  CALL_METHOD_1         1  ''
              154  POP_TOP          
            156_0  COME_FROM_EXCEPT_CLAUSE   144  '144'
            156_1  COME_FROM_EXCEPT_CLAUSE   140  '140'

Parse error at or near `<121>' instruction at offset 30

    def get_temp_filename(self, filename):
        return '%s.%d.temp' % (filename, os.getpid())

    def generate(self, file, is_for_demand=0):
        if is_for_demand:
            self.generate_type = GEN_DEMAND_BASE
        else:
            self.generate_type = GEN_FULL
        self.file = file
        self.do_generate()
        self.file = None
        self.progress.Finished()

    def do_gen_file_header--- This code section failed: ---

 L. 834         0  LOAD_FAST                'self'
                2  LOAD_ATTR                typelib
                4  LOAD_METHOD              GetLibAttr
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'la'

 L. 835        10  LOAD_FAST                'self'
               12  LOAD_ATTR                typelib
               14  LOAD_METHOD              GetDocumentation
               16  LOAD_CONST               -1
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'moduleDoc'

 L. 836        22  LOAD_STR                 ''
               24  STORE_FAST               'docDesc'

 L. 837        26  LOAD_FAST                'moduleDoc'
               28  LOAD_CONST               1
               30  BINARY_SUBSCR    
               32  POP_JUMP_IF_FALSE    42  'to 42'

 L. 838        34  LOAD_FAST                'moduleDoc'
               36  LOAD_CONST               1
               38  BINARY_SUBSCR    
               40  STORE_FAST               'docDesc'
             42_0  COME_FROM            32  '32'

 L. 841        42  LOAD_CONST               0
               44  LOAD_FAST                'self'
               46  STORE_ATTR               bHaveWrittenDispatchBaseClass

 L. 842        48  LOAD_CONST               0
               50  LOAD_FAST                'self'
               52  STORE_ATTR               bHaveWrittenCoClassBaseClass

 L. 843        54  LOAD_CONST               0
               56  LOAD_FAST                'self'
               58  STORE_ATTR               bHaveWrittenEventBaseClass

 L. 847        60  LOAD_FAST                'self'
               62  LOAD_ATTR                file
               64  LOAD_ATTR                encoding
               66  POP_JUMP_IF_TRUE     78  'to 78'
               68  <74>             
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                file
               74  CALL_FUNCTION_1       1  ''
               76  RAISE_VARARGS_1       1  'exception instance'
             78_0  COME_FROM            66  '66'

 L. 848        78  LOAD_FAST                'self'
               80  LOAD_ATTR                file
               82  LOAD_ATTR                encoding
               84  STORE_FAST               'encoding'

 L. 850        86  LOAD_GLOBAL              print
               88  LOAD_STR                 '# -*- coding: %s -*-'
               90  LOAD_FAST                'encoding'
               92  BUILD_TUPLE_1         1 
               94  BINARY_MODULO    
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                file
              100  LOAD_CONST               ('file',)
              102  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              104  POP_TOP          

 L. 851       106  LOAD_GLOBAL              print
              108  LOAD_STR                 '# Created by makepy.py version %s'
              110  LOAD_GLOBAL              makepy_version
              112  BUILD_TUPLE_1         1 
              114  BINARY_MODULO    
              116  LOAD_FAST                'self'
              118  LOAD_ATTR                file
              120  LOAD_CONST               ('file',)
              122  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              124  POP_TOP          

 L. 852       126  LOAD_GLOBAL              print
              128  LOAD_STR                 '# By python version %s'

 L. 853       130  LOAD_GLOBAL              sys
              132  LOAD_ATTR                version
              134  LOAD_METHOD              replace
              136  LOAD_STR                 '\n'
              138  LOAD_STR                 '-'
              140  CALL_METHOD_2         2  ''
              142  BUILD_TUPLE_1         1 

 L. 852       144  BINARY_MODULO    

 L. 853       146  LOAD_FAST                'self'
              148  LOAD_ATTR                file

 L. 852       150  LOAD_CONST               ('file',)
              152  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              154  POP_TOP          

 L. 854       156  LOAD_FAST                'self'
              158  LOAD_ATTR                sourceFilename
              160  POP_JUMP_IF_FALSE   196  'to 196'

 L. 855       162  LOAD_GLOBAL              print
              164  LOAD_STR                 "# From type library '%s'"
              166  LOAD_GLOBAL              os
              168  LOAD_ATTR                path
              170  LOAD_METHOD              split
              172  LOAD_FAST                'self'
              174  LOAD_ATTR                sourceFilename
              176  CALL_METHOD_1         1  ''
              178  LOAD_CONST               1
              180  BINARY_SUBSCR    
              182  BUILD_TUPLE_1         1 
              184  BINARY_MODULO    
              186  LOAD_FAST                'self'
              188  LOAD_ATTR                file
              190  LOAD_CONST               ('file',)
              192  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              194  POP_TOP          
            196_0  COME_FROM           160  '160'

 L. 856       196  LOAD_GLOBAL              print
              198  LOAD_STR                 '# On %s'
              200  LOAD_GLOBAL              time
              202  LOAD_METHOD              ctime
              204  LOAD_GLOBAL              time
              206  LOAD_METHOD              time
              208  CALL_METHOD_0         0  ''
              210  CALL_METHOD_1         1  ''
              212  BINARY_MODULO    
              214  LOAD_FAST                'self'
              216  LOAD_ATTR                file
              218  LOAD_CONST               ('file',)
              220  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              222  POP_TOP          

 L. 858       224  LOAD_GLOBAL              print
              226  LOAD_GLOBAL              build
              228  LOAD_METHOD              _makeDocString
              230  LOAD_FAST                'docDesc'
              232  CALL_METHOD_1         1  ''
              234  LOAD_FAST                'self'
              236  LOAD_ATTR                file
              238  LOAD_CONST               ('file',)
              240  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              242  POP_TOP          

 L. 860       244  LOAD_GLOBAL              print
              246  LOAD_STR                 'makepy_version ='
              248  LOAD_GLOBAL              repr
              250  LOAD_GLOBAL              makepy_version
              252  CALL_FUNCTION_1       1  ''
              254  LOAD_FAST                'self'
              256  LOAD_ATTR                file
              258  LOAD_CONST               ('file',)
              260  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              262  POP_TOP          

 L. 861       264  LOAD_GLOBAL              print
              266  LOAD_STR                 'python_version = 0x%x'
              268  LOAD_GLOBAL              sys
              270  LOAD_ATTR                hexversion
              272  BUILD_TUPLE_1         1 
              274  BINARY_MODULO    
              276  LOAD_FAST                'self'
              278  LOAD_ATTR                file
              280  LOAD_CONST               ('file',)
              282  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              284  POP_TOP          

 L. 862       286  LOAD_GLOBAL              print
              288  LOAD_FAST                'self'
              290  LOAD_ATTR                file
              292  LOAD_CONST               ('file',)
              294  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              296  POP_TOP          

 L. 863       298  LOAD_GLOBAL              print
              300  LOAD_STR                 'import win32com.client.CLSIDToClass, pythoncom, pywintypes'
              302  LOAD_FAST                'self'
              304  LOAD_ATTR                file
              306  LOAD_CONST               ('file',)
              308  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              310  POP_TOP          

 L. 864       312  LOAD_GLOBAL              print
              314  LOAD_STR                 'import win32com.client.util'
              316  LOAD_FAST                'self'
              318  LOAD_ATTR                file
              320  LOAD_CONST               ('file',)
              322  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              324  POP_TOP          

 L. 865       326  LOAD_GLOBAL              print
              328  LOAD_STR                 'from pywintypes import IID'
              330  LOAD_FAST                'self'
              332  LOAD_ATTR                file
              334  LOAD_CONST               ('file',)
              336  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              338  POP_TOP          

 L. 866       340  LOAD_GLOBAL              print
              342  LOAD_STR                 'from win32com.client import Dispatch'
              344  LOAD_FAST                'self'
              346  LOAD_ATTR                file
              348  LOAD_CONST               ('file',)
              350  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              352  POP_TOP          

 L. 867       354  LOAD_GLOBAL              print
              356  LOAD_FAST                'self'
              358  LOAD_ATTR                file
              360  LOAD_CONST               ('file',)
              362  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              364  POP_TOP          

 L. 868       366  LOAD_GLOBAL              print
              368  LOAD_STR                 '# The following 3 lines may need tweaking for the particular server'
              370  LOAD_FAST                'self'
              372  LOAD_ATTR                file
              374  LOAD_CONST               ('file',)
              376  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              378  POP_TOP          

 L. 869       380  LOAD_GLOBAL              print
              382  LOAD_STR                 '# Candidates are pythoncom.Missing, .Empty and .ArgNotFound'
              384  LOAD_FAST                'self'
              386  LOAD_ATTR                file
              388  LOAD_CONST               ('file',)
              390  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              392  POP_TOP          

 L. 870       394  LOAD_GLOBAL              print
              396  LOAD_STR                 'defaultNamedOptArg=pythoncom.Empty'
              398  LOAD_FAST                'self'
              400  LOAD_ATTR                file
              402  LOAD_CONST               ('file',)
              404  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              406  POP_TOP          

 L. 871       408  LOAD_GLOBAL              print
              410  LOAD_STR                 'defaultNamedNotOptArg=pythoncom.Empty'
              412  LOAD_FAST                'self'
              414  LOAD_ATTR                file
              416  LOAD_CONST               ('file',)
              418  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              420  POP_TOP          

 L. 872       422  LOAD_GLOBAL              print
              424  LOAD_STR                 'defaultUnnamedArg=pythoncom.Empty'
              426  LOAD_FAST                'self'
              428  LOAD_ATTR                file
              430  LOAD_CONST               ('file',)
              432  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              434  POP_TOP          

 L. 873       436  LOAD_GLOBAL              print
              438  LOAD_FAST                'self'
              440  LOAD_ATTR                file
              442  LOAD_CONST               ('file',)
              444  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              446  POP_TOP          

 L. 874       448  LOAD_GLOBAL              print
              450  LOAD_STR                 'CLSID = '
              452  LOAD_GLOBAL              repr
              454  LOAD_FAST                'la'
              456  LOAD_CONST               0
              458  BINARY_SUBSCR    
              460  CALL_FUNCTION_1       1  ''
              462  BINARY_ADD       
              464  LOAD_FAST                'self'
              466  LOAD_ATTR                file
              468  LOAD_CONST               ('file',)
              470  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              472  POP_TOP          

 L. 875       474  LOAD_GLOBAL              print
              476  LOAD_STR                 'MajorVersion = '
              478  LOAD_GLOBAL              str
              480  LOAD_FAST                'la'
              482  LOAD_CONST               3
              484  BINARY_SUBSCR    
              486  CALL_FUNCTION_1       1  ''
              488  BINARY_ADD       
              490  LOAD_FAST                'self'
              492  LOAD_ATTR                file
              494  LOAD_CONST               ('file',)
              496  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              498  POP_TOP          

 L. 876       500  LOAD_GLOBAL              print
              502  LOAD_STR                 'MinorVersion = '
              504  LOAD_GLOBAL              str
              506  LOAD_FAST                'la'
              508  LOAD_CONST               4
              510  BINARY_SUBSCR    
              512  CALL_FUNCTION_1       1  ''
              514  BINARY_ADD       
              516  LOAD_FAST                'self'
              518  LOAD_ATTR                file
              520  LOAD_CONST               ('file',)
              522  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              524  POP_TOP          

 L. 877       526  LOAD_GLOBAL              print
              528  LOAD_STR                 'LibraryFlags = '
              530  LOAD_GLOBAL              str
              532  LOAD_FAST                'la'
              534  LOAD_CONST               5
              536  BINARY_SUBSCR    
              538  CALL_FUNCTION_1       1  ''
              540  BINARY_ADD       
              542  LOAD_FAST                'self'
              544  LOAD_ATTR                file
              546  LOAD_CONST               ('file',)
              548  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              550  POP_TOP          

 L. 878       552  LOAD_GLOBAL              print
              554  LOAD_STR                 'LCID = '
              556  LOAD_GLOBAL              hex
              558  LOAD_FAST                'la'
              560  LOAD_CONST               1
              562  BINARY_SUBSCR    
              564  CALL_FUNCTION_1       1  ''
              566  BINARY_ADD       
              568  LOAD_FAST                'self'
              570  LOAD_ATTR                file
              572  LOAD_CONST               ('file',)
              574  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              576  POP_TOP          

 L. 879       578  LOAD_GLOBAL              print
              580  LOAD_FAST                'self'
              582  LOAD_ATTR                file
              584  LOAD_CONST               ('file',)
              586  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              588  POP_TOP          

Parse error at or near `<74>' instruction at offset 68

    def do_generate--- This code section failed: ---

 L. 882         0  LOAD_FAST                'self'
                2  LOAD_ATTR                typelib
                4  LOAD_METHOD              GetDocumentation
                6  LOAD_CONST               -1
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'moduleDoc'

 L. 883        12  LOAD_FAST                'self'
               14  LOAD_ATTR                file
               16  STORE_FAST               'stream'

 L. 884        18  LOAD_STR                 ''
               20  STORE_FAST               'docDesc'

 L. 885        22  LOAD_FAST                'moduleDoc'
               24  LOAD_CONST               1
               26  BINARY_SUBSCR    
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L. 886        30  LOAD_FAST                'moduleDoc'
               32  LOAD_CONST               1
               34  BINARY_SUBSCR    
               36  STORE_FAST               'docDesc'
             38_0  COME_FROM            28  '28'

 L. 887        38  LOAD_FAST                'self'
               40  LOAD_ATTR                progress
               42  LOAD_METHOD              Starting
               44  LOAD_FAST                'docDesc'
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          

 L. 888        50  LOAD_FAST                'self'
               52  LOAD_ATTR                progress
               54  LOAD_METHOD              SetDescription
               56  LOAD_STR                 'Building definitions from type library...'
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          

 L. 890        62  LOAD_FAST                'self'
               64  LOAD_METHOD              do_gen_file_header
               66  CALL_METHOD_0         0  ''
               68  POP_TOP          

 L. 892        70  LOAD_FAST                'self'
               72  LOAD_METHOD              BuildOleItemsFromType
               74  CALL_METHOD_0         0  ''
               76  UNPACK_SEQUENCE_4     4 
               78  STORE_FAST               'oleItems'
               80  STORE_FAST               'enumItems'
               82  STORE_FAST               'recordItems'
               84  STORE_FAST               'vtableItems'

 L. 894        86  LOAD_FAST                'self'
               88  LOAD_ATTR                progress
               90  LOAD_METHOD              SetDescription
               92  LOAD_STR                 'Generating...'
               94  LOAD_GLOBAL              len
               96  LOAD_FAST                'oleItems'
               98  CALL_FUNCTION_1       1  ''
              100  LOAD_GLOBAL              len
              102  LOAD_FAST                'enumItems'
              104  CALL_FUNCTION_1       1  ''
              106  BINARY_ADD       
              108  LOAD_GLOBAL              len
              110  LOAD_FAST                'vtableItems'
              112  CALL_FUNCTION_1       1  ''
              114  BINARY_ADD       
              116  CALL_METHOD_2         2  ''
              118  POP_TOP          

 L. 897       120  LOAD_FAST                'enumItems'
              122  POP_JUMP_IF_FALSE   220  'to 220'

 L. 898       124  LOAD_GLOBAL              print
              126  LOAD_STR                 'class constants:'
              128  LOAD_FAST                'stream'
              130  LOAD_CONST               ('file',)
              132  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              134  POP_TOP          

 L. 899       136  LOAD_GLOBAL              list
              138  LOAD_FAST                'enumItems'
              140  LOAD_METHOD              values
              142  CALL_METHOD_0         0  ''
              144  CALL_FUNCTION_1       1  ''
              146  STORE_FAST               'items'

 L. 900       148  LOAD_FAST                'items'
              150  LOAD_METHOD              sort
              152  CALL_METHOD_0         0  ''
              154  POP_TOP          

 L. 901       156  LOAD_CONST               0
              158  STORE_FAST               'num_written'

 L. 902       160  LOAD_FAST                'items'
              162  GET_ITER         
              164  FOR_ITER            194  'to 194'
              166  STORE_FAST               'oleitem'

 L. 903       168  LOAD_FAST                'num_written'
              170  LOAD_FAST                'oleitem'
              172  LOAD_METHOD              WriteEnumerationItems
              174  LOAD_FAST                'stream'
              176  CALL_METHOD_1         1  ''
              178  INPLACE_ADD      
              180  STORE_FAST               'num_written'

 L. 904       182  LOAD_FAST                'self'
              184  LOAD_ATTR                progress
              186  LOAD_METHOD              Tick
              188  CALL_METHOD_0         0  ''
              190  POP_TOP          
              192  JUMP_BACK           164  'to 164'

 L. 905       194  LOAD_FAST                'num_written'
              196  POP_JUMP_IF_TRUE    210  'to 210'

 L. 906       198  LOAD_GLOBAL              print
              200  LOAD_STR                 '\tpass'
              202  LOAD_FAST                'stream'
              204  LOAD_CONST               ('file',)
              206  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              208  POP_TOP          
            210_0  COME_FROM           196  '196'

 L. 907       210  LOAD_GLOBAL              print
              212  LOAD_FAST                'stream'
              214  LOAD_CONST               ('file',)
              216  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              218  POP_TOP          
            220_0  COME_FROM           122  '122'

 L. 909       220  LOAD_FAST                'self'
              222  LOAD_ATTR                generate_type
              224  LOAD_GLOBAL              GEN_FULL
              226  COMPARE_OP               ==
          228_230  POP_JUMP_IF_FALSE   344  'to 344'

 L. 910       232  LOAD_LISTCOMP            '<code_object <listcomp>>'
              234  LOAD_STR                 'Generator.do_generate.<locals>.<listcomp>'
              236  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              238  LOAD_FAST                'oleItems'
              240  LOAD_METHOD              values
              242  CALL_METHOD_0         0  ''
              244  GET_ITER         
              246  CALL_FUNCTION_1       1  ''
              248  STORE_FAST               'items'

 L. 911       250  LOAD_FAST                'items'
              252  LOAD_METHOD              sort
              254  CALL_METHOD_0         0  ''
              256  POP_TOP          

 L. 912       258  LOAD_FAST                'items'
              260  GET_ITER         
              262  FOR_ITER            290  'to 290'
              264  STORE_FAST               'oleitem'

 L. 913       266  LOAD_FAST                'self'
              268  LOAD_ATTR                progress
              270  LOAD_METHOD              Tick
              272  CALL_METHOD_0         0  ''
              274  POP_TOP          

 L. 914       276  LOAD_FAST                'oleitem'
              278  LOAD_METHOD              WriteClass
              280  LOAD_FAST                'self'
              282  CALL_METHOD_1         1  ''
              284  POP_TOP          
          286_288  JUMP_BACK           262  'to 262'

 L. 916       290  LOAD_GLOBAL              list
              292  LOAD_FAST                'vtableItems'
              294  LOAD_METHOD              values
              296  CALL_METHOD_0         0  ''
              298  CALL_FUNCTION_1       1  ''
              300  STORE_FAST               'items'

 L. 917       302  LOAD_FAST                'items'
              304  LOAD_METHOD              sort
              306  CALL_METHOD_0         0  ''
              308  POP_TOP          

 L. 918       310  LOAD_FAST                'items'
              312  GET_ITER         
              314  FOR_ITER            342  'to 342'
              316  STORE_FAST               'oleitem'

 L. 919       318  LOAD_FAST                'self'
              320  LOAD_ATTR                progress
              322  LOAD_METHOD              Tick
              324  CALL_METHOD_0         0  ''
              326  POP_TOP          

 L. 920       328  LOAD_FAST                'oleitem'
              330  LOAD_METHOD              WriteClass
              332  LOAD_FAST                'self'
              334  CALL_METHOD_1         1  ''
              336  POP_TOP          
          338_340  JUMP_BACK           314  'to 314'
              342  JUMP_FORWARD        368  'to 368'
            344_0  COME_FROM           228  '228'

 L. 922       344  LOAD_FAST                'self'
              346  LOAD_ATTR                progress
              348  LOAD_METHOD              Tick
              350  LOAD_GLOBAL              len
              352  LOAD_FAST                'oleItems'
              354  CALL_FUNCTION_1       1  ''
              356  LOAD_GLOBAL              len
              358  LOAD_FAST                'vtableItems'
              360  CALL_FUNCTION_1       1  ''
              362  BINARY_ADD       
              364  CALL_METHOD_1         1  ''
              366  POP_TOP          
            368_0  COME_FROM           342  '342'

 L. 924       368  LOAD_GLOBAL              print
              370  LOAD_STR                 'RecordMap = {'
              372  LOAD_FAST                'stream'
              374  LOAD_CONST               ('file',)
              376  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              378  POP_TOP          

 L. 925       380  LOAD_FAST                'recordItems'
              382  LOAD_METHOD              values
              384  CALL_METHOD_0         0  ''
              386  GET_ITER         
              388  FOR_ITER            492  'to 492'
              390  STORE_FAST               'record'

 L. 926       392  LOAD_FAST                'record'
              394  LOAD_ATTR                clsid
              396  LOAD_GLOBAL              pythoncom
              398  LOAD_ATTR                IID_NULL
              400  COMPARE_OP               ==
          402_404  POP_JUMP_IF_FALSE   448  'to 448'

 L. 927       406  LOAD_GLOBAL              print
              408  LOAD_STR                 "\t###%s: %s, # Record disabled because it doesn't have a non-null GUID"
              410  LOAD_GLOBAL              repr
              412  LOAD_FAST                'record'
              414  LOAD_ATTR                doc
              416  LOAD_CONST               0
              418  BINARY_SUBSCR    
              420  CALL_FUNCTION_1       1  ''
              422  LOAD_GLOBAL              repr
              424  LOAD_GLOBAL              str
              426  LOAD_FAST                'record'
              428  LOAD_ATTR                clsid
              430  CALL_FUNCTION_1       1  ''
              432  CALL_FUNCTION_1       1  ''
              434  BUILD_TUPLE_2         2 
              436  BINARY_MODULO    
              438  LOAD_FAST                'stream'
              440  LOAD_CONST               ('file',)
              442  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              444  POP_TOP          
              446  JUMP_BACK           388  'to 388'
            448_0  COME_FROM           402  '402'

 L. 929       448  LOAD_GLOBAL              print
              450  LOAD_STR                 '\t%s: %s,'
              452  LOAD_GLOBAL              repr
              454  LOAD_FAST                'record'
              456  LOAD_ATTR                doc
              458  LOAD_CONST               0
              460  BINARY_SUBSCR    
              462  CALL_FUNCTION_1       1  ''
              464  LOAD_GLOBAL              repr
              466  LOAD_GLOBAL              str
              468  LOAD_FAST                'record'
              470  LOAD_ATTR                clsid
              472  CALL_FUNCTION_1       1  ''
              474  CALL_FUNCTION_1       1  ''
              476  BUILD_TUPLE_2         2 
              478  BINARY_MODULO    
              480  LOAD_FAST                'stream'
              482  LOAD_CONST               ('file',)
              484  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              486  POP_TOP          
          488_490  JUMP_BACK           388  'to 388'

 L. 930       492  LOAD_GLOBAL              print
              494  LOAD_STR                 '}'
              496  LOAD_FAST                'stream'
              498  LOAD_CONST               ('file',)
              500  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              502  POP_TOP          

 L. 931       504  LOAD_GLOBAL              print
              506  LOAD_FAST                'stream'
              508  LOAD_CONST               ('file',)
              510  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              512  POP_TOP          

 L. 934       514  LOAD_FAST                'self'
              516  LOAD_ATTR                generate_type
              518  LOAD_GLOBAL              GEN_FULL
              520  COMPARE_OP               ==
          522_524  POP_JUMP_IF_FALSE   724  'to 724'

 L. 935       526  LOAD_GLOBAL              print
              528  LOAD_STR                 'CLSIDToClassMap = {'
              530  LOAD_FAST                'stream'
              532  LOAD_CONST               ('file',)
              534  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              536  POP_TOP          

 L. 936       538  LOAD_FAST                'oleItems'
              540  LOAD_METHOD              values
              542  CALL_METHOD_0         0  ''
              544  GET_ITER         
            546_0  COME_FROM           564  '564'
            546_1  COME_FROM           556  '556'
              546  FOR_ITER            600  'to 600'
              548  STORE_FAST               'item'

 L. 937       550  LOAD_FAST                'item'
              552  LOAD_CONST               None
              554  <117>                 1  ''
          556_558  POP_JUMP_IF_FALSE   546  'to 546'
              560  LOAD_FAST                'item'
              562  LOAD_ATTR                bWritten
          564_566  POP_JUMP_IF_FALSE   546  'to 546'

 L. 938       568  LOAD_GLOBAL              print
              570  LOAD_STR                 "\t'%s' : %s,"
              572  LOAD_GLOBAL              str
              574  LOAD_FAST                'item'
              576  LOAD_ATTR                clsid
              578  CALL_FUNCTION_1       1  ''
              580  LOAD_FAST                'item'
              582  LOAD_ATTR                python_name
              584  BUILD_TUPLE_2         2 
              586  BINARY_MODULO    
              588  LOAD_FAST                'stream'
              590  LOAD_CONST               ('file',)
              592  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              594  POP_TOP          
          596_598  JUMP_BACK           546  'to 546'

 L. 939       600  LOAD_GLOBAL              print
              602  LOAD_STR                 '}'
              604  LOAD_FAST                'stream'
              606  LOAD_CONST               ('file',)
              608  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              610  POP_TOP          

 L. 940       612  LOAD_GLOBAL              print
              614  LOAD_STR                 'CLSIDToPackageMap = {}'
              616  LOAD_FAST                'stream'
              618  LOAD_CONST               ('file',)
              620  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              622  POP_TOP          

 L. 941       624  LOAD_GLOBAL              print
              626  LOAD_STR                 'win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )'
              628  LOAD_FAST                'stream'
              630  LOAD_CONST               ('file',)
              632  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              634  POP_TOP          

 L. 942       636  LOAD_GLOBAL              print
              638  LOAD_STR                 'VTablesToPackageMap = {}'
              640  LOAD_FAST                'stream'
              642  LOAD_CONST               ('file',)
              644  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              646  POP_TOP          

 L. 943       648  LOAD_GLOBAL              print
              650  LOAD_STR                 'VTablesToClassMap = {'
              652  LOAD_FAST                'stream'
              654  LOAD_CONST               ('file',)
              656  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              658  POP_TOP          

 L. 944       660  LOAD_FAST                'vtableItems'
              662  LOAD_METHOD              values
              664  CALL_METHOD_0         0  ''
              666  GET_ITER         
              668  FOR_ITER            700  'to 700'
              670  STORE_FAST               'item'

 L. 945       672  LOAD_GLOBAL              print
              674  LOAD_STR                 "\t'%s' : '%s',"
              676  LOAD_FAST                'item'
              678  LOAD_ATTR                clsid
              680  LOAD_FAST                'item'
              682  LOAD_ATTR                python_name
              684  BUILD_TUPLE_2         2 
              686  BINARY_MODULO    
              688  LOAD_FAST                'stream'
              690  LOAD_CONST               ('file',)
              692  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              694  POP_TOP          
          696_698  JUMP_BACK           668  'to 668'

 L. 946       700  LOAD_GLOBAL              print
              702  LOAD_STR                 '}'
              704  LOAD_FAST                'stream'
              706  LOAD_CONST               ('file',)
              708  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              710  POP_TOP          

 L. 947       712  LOAD_GLOBAL              print
              714  LOAD_FAST                'stream'
              716  LOAD_CONST               ('file',)
              718  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              720  POP_TOP          
              722  JUMP_FORWARD        904  'to 904'
            724_0  COME_FROM           522  '522'

 L. 950       724  LOAD_GLOBAL              print
              726  LOAD_STR                 'CLSIDToClassMap = {}'
              728  LOAD_FAST                'stream'
              730  LOAD_CONST               ('file',)
              732  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              734  POP_TOP          

 L. 951       736  LOAD_GLOBAL              print
              738  LOAD_STR                 'CLSIDToPackageMap = {'
              740  LOAD_FAST                'stream'
              742  LOAD_CONST               ('file',)
              744  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              746  POP_TOP          

 L. 952       748  LOAD_FAST                'oleItems'
              750  LOAD_METHOD              values
              752  CALL_METHOD_0         0  ''
              754  GET_ITER         
            756_0  COME_FROM           766  '766'
              756  FOR_ITER            806  'to 806'
              758  STORE_FAST               'item'

 L. 953       760  LOAD_FAST                'item'
              762  LOAD_CONST               None
              764  <117>                 1  ''
          766_768  POP_JUMP_IF_FALSE   756  'to 756'

 L. 954       770  LOAD_GLOBAL              print
              772  LOAD_STR                 "\t'%s' : %s,"
              774  LOAD_GLOBAL              str
              776  LOAD_FAST                'item'
              778  LOAD_ATTR                clsid
              780  CALL_FUNCTION_1       1  ''
              782  LOAD_GLOBAL              repr
              784  LOAD_FAST                'item'
              786  LOAD_ATTR                python_name
              788  CALL_FUNCTION_1       1  ''
              790  BUILD_TUPLE_2         2 
              792  BINARY_MODULO    
              794  LOAD_FAST                'stream'
              796  LOAD_CONST               ('file',)
              798  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              800  POP_TOP          
          802_804  JUMP_BACK           756  'to 756'

 L. 955       806  LOAD_GLOBAL              print
              808  LOAD_STR                 '}'
              810  LOAD_FAST                'stream'
              812  LOAD_CONST               ('file',)
              814  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              816  POP_TOP          

 L. 956       818  LOAD_GLOBAL              print
              820  LOAD_STR                 'VTablesToClassMap = {}'
              822  LOAD_FAST                'stream'
              824  LOAD_CONST               ('file',)
              826  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              828  POP_TOP          

 L. 957       830  LOAD_GLOBAL              print
              832  LOAD_STR                 'VTablesToPackageMap = {'
              834  LOAD_FAST                'stream'
              836  LOAD_CONST               ('file',)
              838  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              840  POP_TOP          

 L. 958       842  LOAD_FAST                'vtableItems'
              844  LOAD_METHOD              values
              846  CALL_METHOD_0         0  ''
              848  GET_ITER         
              850  FOR_ITER            882  'to 882'
              852  STORE_FAST               'item'

 L. 959       854  LOAD_GLOBAL              print
              856  LOAD_STR                 "\t'%s' : '%s',"
              858  LOAD_FAST                'item'
              860  LOAD_ATTR                clsid
              862  LOAD_FAST                'item'
              864  LOAD_ATTR                python_name
              866  BUILD_TUPLE_2         2 
              868  BINARY_MODULO    
              870  LOAD_FAST                'stream'
              872  LOAD_CONST               ('file',)
              874  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              876  POP_TOP          
          878_880  JUMP_BACK           850  'to 850'

 L. 960       882  LOAD_GLOBAL              print
              884  LOAD_STR                 '}'
              886  LOAD_FAST                'stream'
              888  LOAD_CONST               ('file',)
              890  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              892  POP_TOP          

 L. 961       894  LOAD_GLOBAL              print
              896  LOAD_FAST                'stream'
              898  LOAD_CONST               ('file',)
              900  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              902  POP_TOP          
            904_0  COME_FROM           722  '722'

 L. 963       904  LOAD_GLOBAL              print
              906  LOAD_FAST                'stream'
              908  LOAD_CONST               ('file',)
              910  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              912  POP_TOP          

 L. 965       914  BUILD_MAP_0           0 
              916  STORE_FAST               'map'

 L. 966       918  LOAD_FAST                'oleItems'
              920  LOAD_METHOD              values
              922  CALL_METHOD_0         0  ''
              924  GET_ITER         
            926_0  COME_FROM           948  '948'
            926_1  COME_FROM           936  '936'
              926  FOR_ITER            968  'to 968'
              928  STORE_FAST               'item'

 L. 967       930  LOAD_FAST                'item'
              932  LOAD_CONST               None
              934  <117>                 1  ''
          936_938  POP_JUMP_IF_FALSE   926  'to 926'
              940  LOAD_GLOBAL              isinstance
              942  LOAD_FAST                'item'
              944  LOAD_GLOBAL              CoClassItem
              946  CALL_FUNCTION_2       2  ''
          948_950  POP_JUMP_IF_TRUE    926  'to 926'

 L. 968       952  LOAD_FAST                'item'
              954  LOAD_ATTR                clsid
              956  LOAD_FAST                'map'
              958  LOAD_FAST                'item'
              960  LOAD_ATTR                python_name
              962  STORE_SUBSCR     
          964_966  JUMP_BACK           926  'to 926'

 L. 969       968  LOAD_FAST                'vtableItems'
              970  LOAD_METHOD              values
              972  CALL_METHOD_0         0  ''
              974  GET_ITER         
              976  FOR_ITER            996  'to 996'
              978  STORE_FAST               'item'

 L. 970       980  LOAD_FAST                'item'
              982  LOAD_ATTR                clsid
              984  LOAD_FAST                'map'
              986  LOAD_FAST                'item'
              988  LOAD_ATTR                python_name
              990  STORE_SUBSCR     
          992_994  JUMP_BACK           976  'to 976'

 L. 972       996  LOAD_GLOBAL              print
              998  LOAD_STR                 'NamesToIIDMap = {'
             1000  LOAD_FAST                'stream'
             1002  LOAD_CONST               ('file',)
             1004  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1006  POP_TOP          

 L. 973      1008  LOAD_FAST                'map'
             1010  LOAD_METHOD              items
             1012  CALL_METHOD_0         0  ''
             1014  GET_ITER         
             1016  FOR_ITER           1048  'to 1048'
             1018  UNPACK_SEQUENCE_2     2 
             1020  STORE_FAST               'name'
             1022  STORE_FAST               'iid'

 L. 974      1024  LOAD_GLOBAL              print
             1026  LOAD_STR                 "\t'%s' : '%s',"
             1028  LOAD_FAST                'name'
             1030  LOAD_FAST                'iid'
             1032  BUILD_TUPLE_2         2 
             1034  BINARY_MODULO    
             1036  LOAD_FAST                'stream'
             1038  LOAD_CONST               ('file',)
             1040  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1042  POP_TOP          
         1044_1046  JUMP_BACK          1016  'to 1016'

 L. 975      1048  LOAD_GLOBAL              print
             1050  LOAD_STR                 '}'
             1052  LOAD_FAST                'stream'
             1054  LOAD_CONST               ('file',)
             1056  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1058  POP_TOP          

 L. 976      1060  LOAD_GLOBAL              print
             1062  LOAD_FAST                'stream'
             1064  LOAD_CONST               ('file',)
             1066  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1068  POP_TOP          

 L. 978      1070  LOAD_FAST                'enumItems'
         1072_1074  POP_JUMP_IF_FALSE  1088  'to 1088'

 L. 979      1076  LOAD_GLOBAL              print
             1078  LOAD_STR                 'win32com.client.constants.__dicts__.append(constants.__dict__)'
             1080  LOAD_FAST                'stream'
             1082  LOAD_CONST               ('file',)
             1084  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1086  POP_TOP          
           1088_0  COME_FROM          1072  '1072'

 L. 980      1088  LOAD_GLOBAL              print
             1090  LOAD_FAST                'stream'
             1092  LOAD_CONST               ('file',)
             1094  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1096  POP_TOP          

Parse error at or near `<117>' instruction at offset 554

    def generate_child--- This code section failed: ---

 L. 984         0  LOAD_GLOBAL              GEN_DEMAND_CHILD
                2  LOAD_FAST                'self'
                4  STORE_ATTR               generate_type

 L. 986         6  LOAD_FAST                'self'
                8  LOAD_ATTR                typelib
               10  LOAD_METHOD              GetLibAttr
               12  CALL_METHOD_0         0  ''
               14  STORE_FAST               'la'

 L. 987        16  LOAD_FAST                'la'
               18  LOAD_CONST               1
               20  BINARY_SUBSCR    
               22  STORE_FAST               'lcid'

 L. 988        24  LOAD_FAST                'la'
               26  LOAD_CONST               0
               28  BINARY_SUBSCR    
               30  STORE_FAST               'clsid'

 L. 989        32  LOAD_FAST                'la'
               34  LOAD_CONST               3
               36  BINARY_SUBSCR    
               38  STORE_FAST               'major'

 L. 990        40  LOAD_FAST                'la'
               42  LOAD_CONST               4
               44  BINARY_SUBSCR    
               46  STORE_FAST               'minor'

 L. 991        48  LOAD_STR                 'win32com.gen_py.'
               50  LOAD_GLOBAL              str
               52  LOAD_FAST                'clsid'
               54  CALL_FUNCTION_1       1  ''
               56  LOAD_CONST               1
               58  LOAD_CONST               -1
               60  BUILD_SLICE_2         2 
               62  BINARY_SUBSCR    
               64  BINARY_ADD       
               66  LOAD_STR                 'x%sx%sx%s'
               68  LOAD_FAST                'lcid'
               70  LOAD_FAST                'major'
               72  LOAD_FAST                'minor'
               74  BUILD_TUPLE_3         3 
               76  BINARY_MODULO    
               78  BINARY_ADD       
               80  LOAD_FAST                'self'
               82  STORE_ATTR               base_mod_name

 L. 992     84_86  SETUP_FINALLY       720  'to 720'

 L. 997        88  BUILD_MAP_0           0 
               90  STORE_FAST               'oleItems'

 L. 998        92  BUILD_MAP_0           0 
               94  STORE_FAST               'vtableItems'

 L. 999        96  LOAD_FAST                'self'
               98  LOAD_METHOD              CollectOleItemInfosFromType
              100  CALL_METHOD_0         0  ''
              102  STORE_FAST               'infos'

 L.1000       104  LOAD_CONST               0
              106  STORE_FAST               'found'

 L.1001       108  LOAD_FAST                'infos'
              110  GET_ITER         
            112_0  COME_FROM           224  '224'
            112_1  COME_FROM           136  '136'
              112  FOR_ITER            260  'to 260'
              114  STORE_FAST               'type_info_tuple'

 L.1002       116  LOAD_FAST                'type_info_tuple'
              118  UNPACK_SEQUENCE_4     4 
              120  STORE_FAST               'info'
              122  STORE_FAST               'infotype'
              124  STORE_FAST               'doc'
              126  STORE_FAST               'attr'

 L.1003       128  LOAD_FAST                'infotype'
              130  LOAD_GLOBAL              pythoncom
              132  LOAD_ATTR                TKIND_COCLASS
              134  COMPARE_OP               ==
              136  POP_JUMP_IF_FALSE   112  'to 112'

 L.1004       138  LOAD_FAST                'self'
              140  LOAD_METHOD              _Build_CoClass
              142  LOAD_FAST                'type_info_tuple'
              144  CALL_METHOD_1         1  ''
              146  UNPACK_SEQUENCE_2     2 
              148  STORE_FAST               'coClassItem'
              150  STORE_FAST               'child_infos'

 L.1005       152  LOAD_GLOBAL              build
              154  LOAD_METHOD              MakePublicAttributeName
              156  LOAD_FAST                'doc'
              158  LOAD_CONST               0
              160  BINARY_SUBSCR    
              162  CALL_METHOD_1         1  ''
              164  LOAD_FAST                'child'
              166  COMPARE_OP               ==
              168  STORE_FAST               'found'

 L.1006       170  LOAD_FAST                'found'
              172  POP_JUMP_IF_TRUE    222  'to 222'

 L.1008       174  LOAD_FAST                'child_infos'
              176  GET_ITER         
            178_0  COME_FROM           210  '210'
              178  FOR_ITER            222  'to 222'
              180  UNPACK_SEQUENCE_6     6 
              182  STORE_FAST               'info'
              184  STORE_FAST               'info_type'
              186  STORE_FAST               'refType'
              188  STORE_FAST               'doc'
              190  STORE_FAST               'refAttr'
              192  STORE_FAST               'flags'

 L.1009       194  LOAD_GLOBAL              build
              196  LOAD_METHOD              MakePublicAttributeName
              198  LOAD_FAST                'doc'
              200  LOAD_CONST               0
              202  BINARY_SUBSCR    
              204  CALL_METHOD_1         1  ''
              206  LOAD_FAST                'child'
              208  COMPARE_OP               ==
              210  POP_JUMP_IF_FALSE   178  'to 178'

 L.1010       212  LOAD_CONST               1
              214  STORE_FAST               'found'

 L.1011       216  POP_TOP          
              218  BREAK_LOOP          222  'to 222'
              220  JUMP_BACK           178  'to 178'
            222_0  COME_FROM           172  '172'

 L.1012       222  LOAD_FAST                'found'
              224  POP_JUMP_IF_FALSE   112  'to 112'

 L.1013       226  LOAD_FAST                'coClassItem'
              228  LOAD_FAST                'oleItems'
              230  LOAD_FAST                'coClassItem'
              232  LOAD_ATTR                clsid
              234  STORE_SUBSCR     

 L.1014       236  LOAD_FAST                'self'
              238  LOAD_METHOD              _Build_CoClassChildren
              240  LOAD_FAST                'coClassItem'
              242  LOAD_FAST                'child_infos'
              244  LOAD_FAST                'oleItems'
              246  LOAD_FAST                'vtableItems'
              248  CALL_METHOD_4         4  ''
              250  POP_TOP          

 L.1015       252  POP_TOP          
          254_256  BREAK_LOOP          260  'to 260'
              258  JUMP_BACK           112  'to 112'

 L.1016       260  LOAD_FAST                'found'
          262_264  POP_JUMP_IF_TRUE    372  'to 372'

 L.1018       266  LOAD_FAST                'infos'
              268  GET_ITER         
            270_0  COME_FROM           356  '356'
            270_1  COME_FROM           320  '320'
            270_2  COME_FROM           300  '300'
              270  FOR_ITER            372  'to 372'
              272  STORE_FAST               'type_info_tuple'

 L.1019       274  LOAD_FAST                'type_info_tuple'
              276  UNPACK_SEQUENCE_4     4 
              278  STORE_FAST               'info'
              280  STORE_FAST               'infotype'
              282  STORE_FAST               'doc'
              284  STORE_FAST               'attr'

 L.1020       286  LOAD_FAST                'infotype'
              288  LOAD_GLOBAL              pythoncom
              290  LOAD_ATTR                TKIND_INTERFACE
              292  LOAD_GLOBAL              pythoncom
              294  LOAD_ATTR                TKIND_DISPATCH
              296  BUILD_TUPLE_2         2 
              298  <118>                 0  ''
          300_302  POP_JUMP_IF_FALSE   270  'to 270'

 L.1021       304  LOAD_GLOBAL              build
              306  LOAD_METHOD              MakePublicAttributeName
              308  LOAD_FAST                'doc'
              310  LOAD_CONST               0
              312  BINARY_SUBSCR    
              314  CALL_METHOD_1         1  ''
              316  LOAD_FAST                'child'
              318  COMPARE_OP               ==
          320_322  POP_JUMP_IF_FALSE   270  'to 270'

 L.1022       324  LOAD_CONST               1
              326  STORE_FAST               'found'

 L.1023       328  LOAD_FAST                'self'
              330  LOAD_METHOD              _Build_Interface
              332  LOAD_FAST                'type_info_tuple'
              334  CALL_METHOD_1         1  ''
              336  UNPACK_SEQUENCE_2     2 
              338  STORE_FAST               'oleItem'
              340  STORE_FAST               'vtableItem'

 L.1024       342  LOAD_FAST                'oleItem'
              344  LOAD_FAST                'oleItems'
              346  LOAD_FAST                'clsid'
              348  STORE_SUBSCR     

 L.1025       350  LOAD_FAST                'vtableItem'
              352  LOAD_CONST               None
              354  <117>                 1  ''
          356_358  POP_JUMP_IF_FALSE   270  'to 270'

 L.1026       360  LOAD_FAST                'vtableItem'
              362  LOAD_FAST                'vtableItems'
              364  LOAD_FAST                'clsid'
              366  STORE_SUBSCR     
          368_370  JUMP_BACK           270  'to 270'
            372_0  COME_FROM           262  '262'

 L.1028       372  LOAD_FAST                'found'
          374_376  POP_JUMP_IF_TRUE    392  'to 392'
              378  <74>             
              380  LOAD_STR                 "Cant find the '%s' interface in the CoClasses, or the interfaces"
              382  LOAD_FAST                'child'
              384  BUILD_TUPLE_1         1 
              386  BINARY_MODULO    
              388  CALL_FUNCTION_1       1  ''
              390  RAISE_VARARGS_1       1  'exception instance'
            392_0  COME_FROM           374  '374'

 L.1030       392  BUILD_MAP_0           0 
              394  STORE_FAST               'items'

 L.1031       396  LOAD_FAST                'oleItems'
              398  LOAD_METHOD              items
              400  CALL_METHOD_0         0  ''
              402  GET_ITER         
              404  FOR_ITER            428  'to 428'
              406  UNPACK_SEQUENCE_2     2 
              408  STORE_FAST               'key'
              410  STORE_FAST               'value'

 L.1032       412  LOAD_FAST                'value'
              414  LOAD_CONST               None
              416  BUILD_TUPLE_2         2 
              418  LOAD_FAST                'items'
              420  LOAD_FAST                'key'
              422  STORE_SUBSCR     
          424_426  JUMP_BACK           404  'to 404'

 L.1033       428  LOAD_FAST                'vtableItems'
              430  LOAD_METHOD              items
              432  CALL_METHOD_0         0  ''
              434  GET_ITER         
              436  FOR_ITER            500  'to 500'
              438  UNPACK_SEQUENCE_2     2 
              440  STORE_FAST               'key'
              442  STORE_FAST               'value'

 L.1034       444  LOAD_FAST                'items'
              446  LOAD_METHOD              get
              448  LOAD_FAST                'key'
              450  LOAD_CONST               None
              452  CALL_METHOD_2         2  ''
              454  STORE_FAST               'existing'

 L.1035       456  LOAD_FAST                'existing'
              458  LOAD_CONST               None
              460  <117>                 1  ''
          462_464  POP_JUMP_IF_FALSE   480  'to 480'

 L.1036       466  LOAD_FAST                'existing'
              468  LOAD_CONST               0
              470  BINARY_SUBSCR    
              472  LOAD_FAST                'value'
              474  BUILD_TUPLE_2         2 
              476  STORE_FAST               'new_val'
              478  JUMP_FORWARD        488  'to 488'
            480_0  COME_FROM           462  '462'

 L.1038       480  LOAD_CONST               None
              482  LOAD_FAST                'value'
              484  BUILD_TUPLE_2         2 
              486  STORE_FAST               'new_val'
            488_0  COME_FROM           478  '478'

 L.1039       488  LOAD_FAST                'new_val'
              490  LOAD_FAST                'items'
              492  LOAD_FAST                'key'
              494  STORE_SUBSCR     
          496_498  JUMP_BACK           436  'to 436'

 L.1041       500  LOAD_FAST                'self'
              502  LOAD_ATTR                progress
              504  LOAD_METHOD              SetDescription
              506  LOAD_STR                 'Generating...'
              508  LOAD_GLOBAL              len
              510  LOAD_FAST                'items'
              512  CALL_FUNCTION_1       1  ''
              514  CALL_METHOD_2         2  ''
              516  POP_TOP          

 L.1042       518  LOAD_FAST                'items'
              520  LOAD_METHOD              values
              522  CALL_METHOD_0         0  ''
              524  GET_ITER         
              526  FOR_ITER            706  'to 706'
              528  UNPACK_SEQUENCE_2     2 
              530  STORE_FAST               'oleitem'
              532  STORE_FAST               'vtableitem'

 L.1043       534  LOAD_FAST                'oleitem'
          536_538  JUMP_IF_TRUE_OR_POP   542  'to 542'
              540  LOAD_FAST                'vtableitem'
            542_0  COME_FROM           536  '536'
              542  STORE_FAST               'an_item'

 L.1044       544  LOAD_FAST                'self'
              546  LOAD_ATTR                file
          548_550  POP_JUMP_IF_FALSE   560  'to 560'
              552  <74>             
              554  LOAD_STR                 'already have a file?'
              556  CALL_FUNCTION_1       1  ''
              558  RAISE_VARARGS_1       1  'exception instance'
            560_0  COME_FROM           548  '548'

 L.1047       560  LOAD_GLOBAL              os
              562  LOAD_ATTR                path
              564  LOAD_METHOD              join
              566  LOAD_FAST                'dir'
              568  LOAD_FAST                'an_item'
              570  LOAD_ATTR                python_name
              572  CALL_METHOD_2         2  ''
              574  LOAD_STR                 '.py'
              576  BINARY_ADD       
              578  STORE_FAST               'out_name'

 L.1048       580  LOAD_CONST               False
              582  STORE_FAST               'worked'

 L.1049       584  LOAD_FAST                'self'
              586  LOAD_METHOD              open_writer
              588  LOAD_FAST                'out_name'
              590  CALL_METHOD_1         1  ''
              592  LOAD_FAST                'self'
              594  STORE_ATTR               file

 L.1050       596  SETUP_FINALLY       678  'to 678'

 L.1051       598  LOAD_FAST                'oleitem'
              600  LOAD_CONST               None
              602  <117>                 1  ''
          604_606  POP_JUMP_IF_FALSE   618  'to 618'

 L.1052       608  LOAD_FAST                'self'
              610  LOAD_METHOD              do_gen_child_item
              612  LOAD_FAST                'oleitem'
              614  CALL_METHOD_1         1  ''
              616  POP_TOP          
            618_0  COME_FROM           604  '604'

 L.1053       618  LOAD_FAST                'vtableitem'
              620  LOAD_CONST               None
              622  <117>                 1  ''
          624_626  POP_JUMP_IF_FALSE   638  'to 638'

 L.1054       628  LOAD_FAST                'self'
              630  LOAD_METHOD              do_gen_child_item
              632  LOAD_FAST                'vtableitem'
              634  CALL_METHOD_1         1  ''
              636  POP_TOP          
            638_0  COME_FROM           624  '624'

 L.1055       638  LOAD_FAST                'self'
              640  LOAD_ATTR                progress
              642  LOAD_METHOD              Tick
              644  CALL_METHOD_0         0  ''
              646  POP_TOP          

 L.1056       648  LOAD_CONST               True
              650  STORE_FAST               'worked'
              652  POP_BLOCK        

 L.1058       654  LOAD_FAST                'self'
              656  LOAD_METHOD              finish_writer
              658  LOAD_FAST                'out_name'
              660  LOAD_FAST                'self'
              662  LOAD_ATTR                file
              664  LOAD_FAST                'worked'
              666  CALL_METHOD_3         3  ''
              668  POP_TOP          

 L.1059       670  LOAD_CONST               None
              672  LOAD_FAST                'self'
              674  STORE_ATTR               file
              676  JUMP_BACK           526  'to 526'
            678_0  COME_FROM_FINALLY   596  '596'

 L.1058       678  LOAD_FAST                'self'
              680  LOAD_METHOD              finish_writer
              682  LOAD_FAST                'out_name'
              684  LOAD_FAST                'self'
              686  LOAD_ATTR                file
              688  LOAD_FAST                'worked'
              690  CALL_METHOD_3         3  ''
              692  POP_TOP          

 L.1059       694  LOAD_CONST               None
              696  LOAD_FAST                'self'
              698  STORE_ATTR               file
              700  <48>             
          702_704  JUMP_BACK           526  'to 526'
              706  POP_BLOCK        

 L.1061       708  LOAD_FAST                'self'
              710  LOAD_ATTR                progress
              712  LOAD_METHOD              Finished
              714  CALL_METHOD_0         0  ''
              716  POP_TOP          
              718  JUMP_FORWARD        732  'to 732'
            720_0  COME_FROM_FINALLY    84  '84'
              720  LOAD_FAST                'self'
              722  LOAD_ATTR                progress
              724  LOAD_METHOD              Finished
              726  CALL_METHOD_0         0  ''
              728  POP_TOP          
              730  <48>             
            732_0  COME_FROM           718  '718'

Parse error at or near `<118>' instruction at offset 298

    def do_gen_child_item(self, oleitem):
        moduleDoc = self.typelib.GetDocumentation(-1)
        docDesc = ''
        if moduleDoc[1]:
            docDesc = moduleDoc[1]
        self.progress.StartingdocDesc
        self.progress.SetDescription'Building definitions from type library...'
        self.do_gen_file_header()
        oleitem.WriteClassself
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