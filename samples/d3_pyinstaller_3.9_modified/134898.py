# decompyle3 version 3.7.5
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
             16_0  COME_FROM            52  '52'
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
             54_0  COME_FROM            40  '40'
             54_1  COME_FROM            16  '16'

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
        if item.doc:
            if alias.aliasDoc:
                if alias.aliasDoc[0] == item.doc[0]:
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
             40_0  COME_FROM           192  '192'
             40_1  COME_FROM            72  '72'
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
               72  POP_JUMP_IF_FALSE_BACK    40  'to 40'

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
            194_0  COME_FROM            40  '40'

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
             56_0  COME_FROM           386  '386'
            56_58  FOR_ITER            388  'to 388'
               60  STORE_FAST               'v'

 L. 236        62  LOAD_FAST                'v'
               64  UNPACK_SEQUENCE_3     3 
               66  STORE_FAST               'names'
               68  STORE_FAST               'dispid'
               70  STORE_FAST               'desc'

 L. 237        72  LOAD_FAST                'desc'
               74  LOAD_CONST               2
               76  BINARY_SUBSCR    
               78  STORE_FAST               'arg_desc'

 L. 239        80  BUILD_LIST_0          0 
               82  STORE_FAST               'arg_reprs'

 L. 241        84  LOAD_CONST               0
               86  STORE_FAST               'item_num'

 L. 242        88  LOAD_GLOBAL              print
               90  LOAD_STR                 '\t(('
               92  LOAD_STR                 ' '
               94  LOAD_FAST                'stream'
               96  LOAD_CONST               ('end', 'file')
               98  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              100  POP_TOP          

 L. 243       102  LOAD_FAST                'names'
              104  GET_ITER         
            106_0  COME_FROM           164  '164'
            106_1  COME_FROM           148  '148'
              106  FOR_ITER            166  'to 166'
              108  STORE_FAST               'name'

 L. 244       110  LOAD_GLOBAL              print
              112  LOAD_GLOBAL              repr
              114  LOAD_FAST                'name'
              116  CALL_FUNCTION_1       1  ''
              118  LOAD_STR                 ','
              120  LOAD_STR                 ' '
              122  LOAD_FAST                'stream'
              124  LOAD_CONST               ('end', 'file')
              126  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              128  POP_TOP          

 L. 245       130  LOAD_FAST                'item_num'
              132  LOAD_CONST               1
              134  BINARY_ADD       
              136  STORE_FAST               'item_num'

 L. 246       138  LOAD_FAST                'item_num'
              140  LOAD_CONST               5
              142  BINARY_MODULO    
              144  LOAD_CONST               0
              146  COMPARE_OP               ==
              148  POP_JUMP_IF_FALSE_BACK   106  'to 106'

 L. 247       150  LOAD_GLOBAL              print
              152  LOAD_STR                 '\n\t\t\t'
              154  LOAD_STR                 ' '
              156  LOAD_FAST                'stream'
              158  LOAD_CONST               ('end', 'file')
              160  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              162  POP_TOP          
              164  JUMP_BACK           106  'to 106'
            166_0  COME_FROM           106  '106'

 L. 248       166  LOAD_GLOBAL              print
              168  LOAD_STR                 '), %d, (%r, %r, ['
              170  LOAD_FAST                'dispid'
              172  LOAD_FAST                'desc'
              174  LOAD_CONST               0
              176  BINARY_SUBSCR    
              178  LOAD_FAST                'desc'
              180  LOAD_CONST               1
              182  BINARY_SUBSCR    
              184  BUILD_TUPLE_3         3 
              186  BINARY_MODULO    
              188  LOAD_STR                 ' '
              190  LOAD_FAST                'stream'
              192  LOAD_CONST               ('end', 'file')
              194  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              196  POP_TOP          

 L. 249       198  LOAD_FAST                'arg_desc'
              200  GET_ITER         
            202_0  COME_FROM           318  '318'
              202  FOR_ITER            320  'to 320'
              204  STORE_FAST               'arg'

 L. 250       206  LOAD_FAST                'item_num'
              208  LOAD_CONST               1
              210  BINARY_ADD       
              212  STORE_FAST               'item_num'

 L. 251       214  LOAD_FAST                'item_num'
              216  LOAD_CONST               5
              218  BINARY_MODULO    
              220  LOAD_CONST               0
              222  COMPARE_OP               ==
              224  POP_JUMP_IF_FALSE   240  'to 240'

 L. 252       226  LOAD_GLOBAL              print
              228  LOAD_STR                 '\n\t\t\t'
              230  LOAD_STR                 ' '
              232  LOAD_FAST                'stream'
              234  LOAD_CONST               ('end', 'file')
              236  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              238  POP_TOP          
            240_0  COME_FROM           224  '224'

 L. 253       240  LOAD_GLOBAL              build
              242  LOAD_METHOD              MakeDefaultArgRepr
              244  LOAD_FAST                'arg'
              246  CALL_METHOD_1         1  ''
              248  STORE_FAST               'defval'

 L. 254       250  LOAD_FAST                'arg'
              252  LOAD_CONST               3
              254  BINARY_SUBSCR    
              256  LOAD_CONST               None
              258  <117>                 0  ''
          260_262  POP_JUMP_IF_FALSE   270  'to 270'

 L. 255       264  LOAD_CONST               None
              266  STORE_FAST               'arg3_repr'
              268  JUMP_FORWARD        282  'to 282'
            270_0  COME_FROM           260  '260'

 L. 257       270  LOAD_GLOBAL              repr
              272  LOAD_FAST                'arg'
              274  LOAD_CONST               3
              276  BINARY_SUBSCR    
              278  CALL_FUNCTION_1       1  ''
              280  STORE_FAST               'arg3_repr'
            282_0  COME_FROM           268  '268'

 L. 258       282  LOAD_GLOBAL              print
              284  LOAD_GLOBAL              repr
              286  LOAD_FAST                'arg'
              288  LOAD_CONST               0
              290  BINARY_SUBSCR    
              292  LOAD_FAST                'arg'
              294  LOAD_CONST               1
              296  BINARY_SUBSCR    
              298  LOAD_FAST                'defval'
              300  LOAD_FAST                'arg3_repr'
              302  BUILD_TUPLE_4         4 
              304  CALL_FUNCTION_1       1  ''
              306  LOAD_STR                 ','
              308  LOAD_STR                 ' '
              310  LOAD_FAST                'stream'
              312  LOAD_CONST               ('end', 'file')
              314  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              316  POP_TOP          
              318  JUMP_BACK           202  'to 202'
            320_0  COME_FROM           202  '202'

 L. 259       320  LOAD_GLOBAL              print
              322  LOAD_STR                 '],'
              324  LOAD_STR                 ' '
              326  LOAD_FAST                'stream'
              328  LOAD_CONST               ('end', 'file')
              330  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              332  POP_TOP          

 L. 260       334  LOAD_FAST                'desc'
              336  LOAD_CONST               3
              338  LOAD_CONST               None
              340  BUILD_SLICE_2         2 
              342  BINARY_SUBSCR    
              344  GET_ITER         
            346_0  COME_FROM           370  '370'
              346  FOR_ITER            374  'to 374'
              348  STORE_FAST               'd'

 L. 261       350  LOAD_GLOBAL              print
              352  LOAD_GLOBAL              repr
              354  LOAD_FAST                'd'
              356  CALL_FUNCTION_1       1  ''
              358  LOAD_STR                 ','
              360  LOAD_STR                 ' '
              362  LOAD_FAST                'stream'
              364  LOAD_CONST               ('end', 'file')
              366  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              368  POP_TOP          
          370_372  JUMP_BACK           346  'to 346'
            374_0  COME_FROM           346  '346'

 L. 262       374  LOAD_GLOBAL              print
              376  LOAD_STR                 ')),'
              378  LOAD_FAST                'stream'
              380  LOAD_CONST               ('file',)
              382  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              384  POP_TOP          
              386  JUMP_BACK            56  'to 56'
            388_0  COME_FROM            56  '56'

 L. 263       388  LOAD_GLOBAL              print
              390  LOAD_STR                 ']'
              392  LOAD_FAST                'stream'
              394  LOAD_CONST               ('file',)
              396  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              398  POP_TOP          

 L. 264       400  LOAD_GLOBAL              print
              402  LOAD_FAST                'stream'
              404  LOAD_CONST               ('file',)
              406  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              408  POP_TOP          

Parse error at or near `<117>' instruction at offset 258


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
        if self.bIsSink:
            self.WriteEventSinkClassHeadergenerator
            self.WriteCallbackClassBodygenerator
        else:
            self.WriteClassHeadergenerator
            self.WriteClassBodygenerator
        print(file=(generator.file))
        self.bWritten = 1

    def WriteClassHeader--- This code section failed: ---

 L. 289         0  LOAD_FAST                'generator'
                2  LOAD_METHOD              checkWriteDispatchBaseClass
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 290         8  LOAD_FAST                'self'
               10  LOAD_ATTR                doc
               12  STORE_FAST               'doc'

 L. 291        14  LOAD_FAST                'generator'
               16  LOAD_ATTR                file
               18  STORE_FAST               'stream'

 L. 292        20  LOAD_GLOBAL              print
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

 L. 293        42  LOAD_FAST                'doc'
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

 L. 294        76  SETUP_FINALLY       110  'to 110'

 L. 295        78  LOAD_GLOBAL              pythoncom
               80  LOAD_METHOD              ProgIDFromCLSID
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                clsid
               86  CALL_METHOD_1         1  ''
               88  STORE_FAST               'progId'

 L. 296        90  LOAD_GLOBAL              print
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

 L. 297       110  DUP_TOP          
              112  LOAD_GLOBAL              pythoncom
              114  LOAD_ATTR                com_error
              116  <121>               128  ''
              118  POP_TOP          
              120  POP_TOP          
              122  POP_TOP          

 L. 298       124  POP_EXCEPT       
              126  JUMP_FORWARD        130  'to 130'
              128  <48>             
            130_0  COME_FROM           126  '126'
            130_1  COME_FROM           108  '108'

 L. 299       130  LOAD_GLOBAL              print
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

 L. 300       152  LOAD_FAST                'self'
              154  LOAD_ATTR                coclass_clsid
              156  LOAD_CONST               None
              158  <117>                 0  ''
              160  POP_JUMP_IF_FALSE   176  'to 176'

 L. 301       162  LOAD_GLOBAL              print
              164  LOAD_STR                 '\tcoclass_clsid = None'
              166  LOAD_FAST                'stream'
              168  LOAD_CONST               ('file',)
              170  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              172  POP_TOP          
              174  JUMP_FORWARD        198  'to 198'
            176_0  COME_FROM           160  '160'

 L. 303       176  LOAD_GLOBAL              print
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

 L. 304       198  LOAD_GLOBAL              print
              200  LOAD_FAST                'stream'
              202  LOAD_CONST               ('file',)
              204  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              206  POP_TOP          

 L. 305       208  LOAD_CONST               1
              210  LOAD_FAST                'self'
              212  STORE_ATTR               bWritten

Parse error at or near `<121>' instruction at offset 116

    def WriteEventSinkClassHeader--- This code section failed: ---

 L. 308         0  LOAD_FAST                'generator'
                2  LOAD_METHOD              checkWriteEventBaseClass
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 309         8  LOAD_FAST                'self'
               10  LOAD_ATTR                doc
               12  STORE_FAST               'doc'

 L. 310        14  LOAD_FAST                'generator'
               16  LOAD_ATTR                file
               18  STORE_FAST               'stream'

 L. 311        20  LOAD_GLOBAL              print
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

 L. 312        42  LOAD_FAST                'doc'
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

 L. 313        76  SETUP_FINALLY       110  'to 110'

 L. 314        78  LOAD_GLOBAL              pythoncom
               80  LOAD_METHOD              ProgIDFromCLSID
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                clsid
               86  CALL_METHOD_1         1  ''
               88  STORE_FAST               'progId'

 L. 315        90  LOAD_GLOBAL              print
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

 L. 316       110  DUP_TOP          
              112  LOAD_GLOBAL              pythoncom
              114  LOAD_ATTR                com_error
              116  <121>               128  ''
              118  POP_TOP          
              120  POP_TOP          
              122  POP_TOP          

 L. 317       124  POP_EXCEPT       
              126  JUMP_FORWARD        130  'to 130'
              128  <48>             
            130_0  COME_FROM           126  '126'
            130_1  COME_FROM           108  '108'

 L. 318       130  LOAD_GLOBAL              print
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

 L. 319       152  LOAD_FAST                'self'
              154  LOAD_ATTR                coclass_clsid
              156  LOAD_CONST               None
              158  <117>                 0  ''
              160  POP_JUMP_IF_FALSE   176  'to 176'

 L. 320       162  LOAD_GLOBAL              print
              164  LOAD_STR                 '\tcoclass_clsid = None'
              166  LOAD_FAST                'stream'
              168  LOAD_CONST               ('file',)
              170  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              172  POP_TOP          
              174  JUMP_FORWARD        198  'to 198'
            176_0  COME_FROM           160  '160'

 L. 322       176  LOAD_GLOBAL              print
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

 L. 323       198  LOAD_GLOBAL              print
              200  LOAD_STR                 '\t_public_methods_ = [] # For COM Server support'
              202  LOAD_FAST                'stream'
              204  LOAD_CONST               ('file',)
              206  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              208  POP_TOP          

 L. 324       210  LOAD_GLOBAL              WriteSinkEventMap
              212  LOAD_FAST                'self'
              214  LOAD_FAST                'stream'
              216  CALL_FUNCTION_2       2  ''
              218  POP_TOP          

 L. 325       220  LOAD_GLOBAL              print
              222  LOAD_FAST                'stream'
              224  LOAD_CONST               ('file',)
              226  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              228  POP_TOP          

 L. 326       230  LOAD_GLOBAL              print
              232  LOAD_STR                 '\tdef __init__(self, oobj = None):'
              234  LOAD_FAST                'stream'
              236  LOAD_CONST               ('file',)
              238  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              240  POP_TOP          

 L. 327       242  LOAD_GLOBAL              print
              244  LOAD_STR                 '\t\tif oobj is None:'
              246  LOAD_FAST                'stream'
              248  LOAD_CONST               ('file',)
              250  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              252  POP_TOP          

 L. 328       254  LOAD_GLOBAL              print
              256  LOAD_STR                 '\t\t\tself._olecp = None'
              258  LOAD_FAST                'stream'
              260  LOAD_CONST               ('file',)
              262  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              264  POP_TOP          

 L. 329       266  LOAD_GLOBAL              print
              268  LOAD_STR                 '\t\telse:'
              270  LOAD_FAST                'stream'
              272  LOAD_CONST               ('file',)
              274  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              276  POP_TOP          

 L. 330       278  LOAD_GLOBAL              print
              280  LOAD_STR                 '\t\t\timport win32com.server.util'
              282  LOAD_FAST                'stream'
              284  LOAD_CONST               ('file',)
              286  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              288  POP_TOP          

 L. 331       290  LOAD_GLOBAL              print
              292  LOAD_STR                 '\t\t\tfrom win32com.server.policy import EventHandlerPolicy'
              294  LOAD_FAST                'stream'
              296  LOAD_CONST               ('file',)
              298  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              300  POP_TOP          

 L. 332       302  LOAD_GLOBAL              print
              304  LOAD_STR                 '\t\t\tcpc=oobj._oleobj_.QueryInterface(pythoncom.IID_IConnectionPointContainer)'
              306  LOAD_FAST                'stream'
              308  LOAD_CONST               ('file',)
              310  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              312  POP_TOP          

 L. 333       314  LOAD_GLOBAL              print
              316  LOAD_STR                 '\t\t\tcp=cpc.FindConnectionPoint(self.CLSID_Sink)'
              318  LOAD_FAST                'stream'
              320  LOAD_CONST               ('file',)
              322  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              324  POP_TOP          

 L. 334       326  LOAD_GLOBAL              print
              328  LOAD_STR                 '\t\t\tcookie=cp.Advise(win32com.server.util.wrap(self, usePolicy=EventHandlerPolicy))'
              330  LOAD_FAST                'stream'
              332  LOAD_CONST               ('file',)
              334  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              336  POP_TOP          

 L. 335       338  LOAD_GLOBAL              print
              340  LOAD_STR                 '\t\t\tself._olecp,self._olecp_cookie = cp,cookie'
              342  LOAD_FAST                'stream'
              344  LOAD_CONST               ('file',)
              346  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              348  POP_TOP          

 L. 336       350  LOAD_GLOBAL              print
              352  LOAD_STR                 '\tdef __del__(self):'
              354  LOAD_FAST                'stream'
              356  LOAD_CONST               ('file',)
              358  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              360  POP_TOP          

 L. 337       362  LOAD_GLOBAL              print
              364  LOAD_STR                 '\t\ttry:'
              366  LOAD_FAST                'stream'
              368  LOAD_CONST               ('file',)
              370  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              372  POP_TOP          

 L. 338       374  LOAD_GLOBAL              print
              376  LOAD_STR                 '\t\t\tself.close()'
              378  LOAD_FAST                'stream'
              380  LOAD_CONST               ('file',)
              382  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              384  POP_TOP          

 L. 339       386  LOAD_GLOBAL              print
              388  LOAD_STR                 '\t\texcept pythoncom.com_error:'
              390  LOAD_FAST                'stream'
              392  LOAD_CONST               ('file',)
              394  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              396  POP_TOP          

 L. 340       398  LOAD_GLOBAL              print
              400  LOAD_STR                 '\t\t\tpass'
              402  LOAD_FAST                'stream'
              404  LOAD_CONST               ('file',)
              406  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              408  POP_TOP          

 L. 341       410  LOAD_GLOBAL              print
              412  LOAD_STR                 '\tdef close(self):'
              414  LOAD_FAST                'stream'
              416  LOAD_CONST               ('file',)
              418  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              420  POP_TOP          

 L. 342       422  LOAD_GLOBAL              print
              424  LOAD_STR                 '\t\tif self._olecp is not None:'
              426  LOAD_FAST                'stream'
              428  LOAD_CONST               ('file',)
              430  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              432  POP_TOP          

 L. 343       434  LOAD_GLOBAL              print
              436  LOAD_STR                 '\t\t\tcp,cookie,self._olecp,self._olecp_cookie = self._olecp,self._olecp_cookie,None,None'
              438  LOAD_FAST                'stream'
              440  LOAD_CONST               ('file',)
              442  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              444  POP_TOP          

 L. 344       446  LOAD_GLOBAL              print
              448  LOAD_STR                 '\t\t\tcp.Unadvise(cookie)'
              450  LOAD_FAST                'stream'
              452  LOAD_CONST               ('file',)
              454  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              456  POP_TOP          

 L. 345       458  LOAD_GLOBAL              print
              460  LOAD_STR                 '\tdef _query_interface_(self, iid):'
              462  LOAD_FAST                'stream'
              464  LOAD_CONST               ('file',)
              466  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              468  POP_TOP          

 L. 346       470  LOAD_GLOBAL              print
              472  LOAD_STR                 '\t\timport win32com.server.util'
              474  LOAD_FAST                'stream'
              476  LOAD_CONST               ('file',)
              478  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              480  POP_TOP          

 L. 347       482  LOAD_GLOBAL              print
              484  LOAD_STR                 '\t\tif iid==self.CLSID_Sink: return win32com.server.util.wrap(self)'
              486  LOAD_FAST                'stream'
              488  LOAD_CONST               ('file',)
              490  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              492  POP_TOP          

 L. 348       494  LOAD_GLOBAL              print
              496  LOAD_FAST                'stream'
              498  LOAD_CONST               ('file',)
              500  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              502  POP_TOP          

 L. 349       504  LOAD_CONST               1
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
        else:
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
             50_0  COME_FROM           328  '328'
             50_1  COME_FROM           230  '230'
             50_2  COME_FROM           168  '168'
             50_3  COME_FROM           120  '120'
             50_4  COME_FROM           102  '102'
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
              184  <118>                 0  ''
              186  POP_JUMP_IF_FALSE   220  'to 220'
              188  LOAD_FAST                'specialItems'
              190  LOAD_FAST                'lkey'
              192  BINARY_SUBSCR    
              194  LOAD_CONST               None
              196  <117>                 0  ''
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
              230  POP_JUMP_IF_TRUE_BACK    50  'to 50'
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
            308_0  COME_FROM           324  '324'
              308  FOR_ITER            328  'to 328'
              310  STORE_FAST               'line'

 L. 399       312  LOAD_GLOBAL              print
              314  LOAD_FAST                'line'
              316  LOAD_FAST                'stream'
              318  LOAD_CONST               ('file',)
              320  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              322  POP_TOP          
          324_326  JUMP_BACK           308  'to 308'
            328_0  COME_FROM           308  '308'
              328  JUMP_BACK            50  'to 50'
            330_0  COME_FROM            50  '50'

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
              356  LOAD_FAST                'names'
              358  LOAD_METHOD              sort
              360  CALL_METHOD_0         0  ''
              362  POP_TOP          

 L. 402       364  LOAD_FAST                'names'
              366  GET_ITER         
            368_0  COME_FROM           632  '632'
            368_1  COME_FROM           602  '602'
            368_2  COME_FROM           396  '396'
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
          396_398  POP_JUMP_IF_TRUE_BACK   368  'to 368'
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
              548  <118>                 0  ''
          550_552  POP_JUMP_IF_FALSE   606  'to 606'
              554  LOAD_FAST                'specialItems'
              556  LOAD_FAST                'lkey'
              558  BINARY_SUBSCR    
              560  LOAD_CONST               None
              562  <117>                 0  ''
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
            636_0  COME_FROM           368  '368'

 L. 428       636  LOAD_GLOBAL              list
              638  LOAD_FAST                'self'
              640  LOAD_ATTR                propMapGet
              642  LOAD_METHOD              keys
              644  CALL_METHOD_0         0  ''
              646  CALL_FUNCTION_1       1  ''
              648  STORE_FAST               'names'
              650  LOAD_FAST                'names'
              652  LOAD_METHOD              sort
              654  CALL_METHOD_0         0  ''
              656  POP_TOP          

 L. 429       658  LOAD_FAST                'names'
              660  GET_ITER         
            662_0  COME_FROM           930  '930'
            662_1  COME_FROM           900  '900'
            662_2  COME_FROM           690  '690'
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
          690_692  POP_JUMP_IF_TRUE_BACK   662  'to 662'
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
              846  <118>                 0  ''
          848_850  POP_JUMP_IF_FALSE   904  'to 904'
              852  LOAD_FAST                'specialItems'
              854  LOAD_FAST                'lkey'
              856  BINARY_SUBSCR    
              858  LOAD_CONST               None
              860  <117>                 0  ''
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
            934_0  COME_FROM           662  '662'

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
              972  LOAD_FAST                'names'
              974  LOAD_METHOD              sort
              976  CALL_METHOD_0         0  ''
              978  POP_TOP          

 L. 458       980  LOAD_FAST                'names'
              982  GET_ITER         
            984_0  COME_FROM          1102  '1102'
            984_1  COME_FROM          1010  '1010'
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
         1010_1012  POP_JUMP_IF_TRUE_BACK   984  'to 984'
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
             1046  <117>                 0  ''
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
           1106_0  COME_FROM           984  '984'

 L. 471      1106  LOAD_GLOBAL              list
             1108  LOAD_FAST                'self'
             1110  LOAD_ATTR                propMapPut
             1112  LOAD_METHOD              keys
             1114  CALL_METHOD_0         0  ''
             1116  CALL_FUNCTION_1       1  ''
             1118  STORE_FAST               'names'
             1120  LOAD_FAST                'names'
             1122  LOAD_METHOD              sort
             1124  CALL_METHOD_0         0  ''
             1126  POP_TOP          

 L. 472      1128  LOAD_FAST                'names'
             1130  GET_ITER         
           1132_0  COME_FROM          1218  '1218'
           1132_1  COME_FROM          1158  '1158'
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
         1158_1160  POP_JUMP_IF_TRUE_BACK  1132  'to 1132'
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
           1222_0  COME_FROM          1132  '1132'

 L. 478      1222  LOAD_GLOBAL              print
             1224  LOAD_STR                 '\t}'
             1226  LOAD_FAST                'stream'
             1228  LOAD_CONST               ('file',)
             1230  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1232  POP_TOP          

 L. 480      1234  LOAD_FAST                'specialItems'
             1236  LOAD_STR                 'value'
             1238  BINARY_SUBSCR    
         1240_1242  POP_JUMP_IF_FALSE  1398  'to 1398'

 L. 481      1244  LOAD_FAST                'specialItems'
             1246  LOAD_STR                 'value'
             1248  BINARY_SUBSCR    
             1250  UNPACK_SEQUENCE_3     3 
             1252  STORE_FAST               'entry'
             1254  STORE_FAST               'invoketype'
             1256  STORE_FAST               'propArgs'

 L. 482      1258  LOAD_FAST                'propArgs'
             1260  LOAD_CONST               None
             1262  <117>                 0  ''
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
           1330_0  COME_FROM          1346  '1346'
             1330  FOR_ITER           1350  'to 1350'
             1332  STORE_FAST               'line'

 L. 490      1334  LOAD_GLOBAL              print
             1336  LOAD_FAST                'line'
             1338  LOAD_FAST                'stream'
             1340  LOAD_CONST               ('file',)
             1342  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1344  POP_TOP          
         1346_1348  JUMP_BACK          1330  'to 1330'
           1350_0  COME_FROM          1330  '1330'

 L. 491      1350  LOAD_GLOBAL              print
             1352  LOAD_STR                 '\tdef __str__(self, *args):'
             1354  LOAD_FAST                'stream'
             1356  LOAD_CONST               ('file',)
             1358  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1360  POP_TOP          

 L. 492      1362  LOAD_GLOBAL              print
             1364  LOAD_STR                 '\t\treturn str(self.__call__(*args))'
             1366  LOAD_FAST                'stream'
             1368  LOAD_CONST               ('file',)
             1370  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1372  POP_TOP          

 L. 493      1374  LOAD_GLOBAL              print
             1376  LOAD_STR                 '\tdef __int__(self, *args):'
             1378  LOAD_FAST                'stream'
             1380  LOAD_CONST               ('file',)
             1382  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1384  POP_TOP          

 L. 494      1386  LOAD_GLOBAL              print
             1388  LOAD_STR                 '\t\treturn int(self.__call__(*args))'
             1390  LOAD_FAST                'stream'
             1392  LOAD_CONST               ('file',)
             1394  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1396  POP_TOP          
           1398_0  COME_FROM          1240  '1240'

 L. 500      1398  LOAD_FAST                'specialItems'
             1400  LOAD_STR                 '_newenum'
             1402  BINARY_SUBSCR    
         1404_1406  POP_JUMP_IF_FALSE  1442  'to 1442'

 L. 501      1408  LOAD_FAST                'specialItems'
             1410  LOAD_STR                 '_newenum'
             1412  BINARY_SUBSCR    
             1414  UNPACK_SEQUENCE_3     3 
             1416  STORE_FAST               'enumEntry'
             1418  STORE_FAST               'invoketype'
             1420  STORE_FAST               'propArgs'

 L. 502      1422  LOAD_FAST                'enumEntry'
             1424  LOAD_ATTR                desc
             1426  LOAD_CONST               4
             1428  BINARY_SUBSCR    
             1430  STORE_FAST               'invkind'

 L. 505      1432  LOAD_FAST                'enumEntry'
             1434  LOAD_METHOD              GetResultCLSIDStr
             1436  CALL_METHOD_0         0  ''
             1438  STORE_FAST               'resultCLSID'
             1440  JUMP_FORWARD       1458  'to 1458'
           1442_0  COME_FROM          1404  '1404'

 L. 507      1442  LOAD_GLOBAL              pythoncom
             1444  LOAD_ATTR                DISPATCH_METHOD
             1446  LOAD_GLOBAL              pythoncom
             1448  LOAD_ATTR                DISPATCH_PROPERTYGET
             1450  BINARY_OR        
             1452  STORE_FAST               'invkind'

 L. 508      1454  LOAD_STR                 'None'
             1456  STORE_FAST               'resultCLSID'
           1458_0  COME_FROM          1440  '1440'

 L. 510      1458  LOAD_FAST                'resultCLSID'
             1460  LOAD_STR                 'None'
             1462  COMPARE_OP               ==
         1464_1466  POP_JUMP_IF_FALSE  1494  'to 1494'
             1468  LOAD_STR                 'Item'
             1470  LOAD_FAST                'self'
             1472  LOAD_ATTR                mapFuncs
             1474  <118>                 0  ''
         1476_1478  POP_JUMP_IF_FALSE  1494  'to 1494'

 L. 511      1480  LOAD_FAST                'self'
             1482  LOAD_ATTR                mapFuncs
             1484  LOAD_STR                 'Item'
             1486  BINARY_SUBSCR    
             1488  LOAD_METHOD              GetResultCLSIDStr
             1490  CALL_METHOD_0         0  ''
             1492  STORE_FAST               'resultCLSID'
           1494_0  COME_FROM          1476  '1476'
           1494_1  COME_FROM          1464  '1464'

 L. 512      1494  LOAD_GLOBAL              print
             1496  LOAD_STR                 '\tdef __iter__(self):'
             1498  LOAD_FAST                'stream'
             1500  LOAD_CONST               ('file',)
             1502  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1504  POP_TOP          

 L. 513      1506  LOAD_GLOBAL              print
             1508  LOAD_STR                 '\t\t"Return a Python iterator for this object"'
             1510  LOAD_FAST                'stream'
             1512  LOAD_CONST               ('file',)
             1514  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1516  POP_TOP          

 L. 514      1518  LOAD_GLOBAL              print
             1520  LOAD_STR                 '\t\ttry:'
             1522  LOAD_FAST                'stream'
             1524  LOAD_CONST               ('file',)
             1526  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1528  POP_TOP          

 L. 515      1530  LOAD_GLOBAL              print
             1532  LOAD_STR                 '\t\t\tob = self._oleobj_.InvokeTypes(%d,LCID,%d,(13, 10),())'
             1534  LOAD_GLOBAL              pythoncom
             1536  LOAD_ATTR                DISPID_NEWENUM
             1538  LOAD_FAST                'invkind'
             1540  BUILD_TUPLE_2         2 
             1542  BINARY_MODULO    
             1544  LOAD_FAST                'stream'
             1546  LOAD_CONST               ('file',)
             1548  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1550  POP_TOP          

 L. 516      1552  LOAD_GLOBAL              print
             1554  LOAD_STR                 '\t\texcept pythoncom.error:'
             1556  LOAD_FAST                'stream'
             1558  LOAD_CONST               ('file',)
             1560  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1562  POP_TOP          

 L. 517      1564  LOAD_GLOBAL              print
             1566  LOAD_STR                 '\t\t\traise TypeError("This object does not support enumeration")'
             1568  LOAD_FAST                'stream'
             1570  LOAD_CONST               ('file',)
             1572  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1574  POP_TOP          

 L. 519      1576  LOAD_GLOBAL              print
             1578  LOAD_STR                 '\t\treturn win32com.client.util.Iterator(ob, %s)'
             1580  LOAD_FAST                'resultCLSID'
             1582  BINARY_MODULO    
             1584  LOAD_FAST                'stream'
             1586  LOAD_CONST               ('file',)
             1588  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1590  POP_TOP          

 L. 521      1592  LOAD_FAST                'specialItems'
             1594  LOAD_STR                 'item'
             1596  BINARY_SUBSCR    
         1598_1600  POP_JUMP_IF_FALSE  1700  'to 1700'

 L. 522      1602  LOAD_FAST                'specialItems'
             1604  LOAD_STR                 'item'
             1606  BINARY_SUBSCR    
             1608  UNPACK_SEQUENCE_3     3 
             1610  STORE_FAST               'entry'
             1612  STORE_FAST               'invoketype'
             1614  STORE_FAST               'propArgs'

 L. 523      1616  LOAD_FAST                'entry'
             1618  LOAD_METHOD              GetResultCLSIDStr
             1620  CALL_METHOD_0         0  ''
             1622  STORE_FAST               'resultCLSID'

 L. 524      1624  LOAD_GLOBAL              print
             1626  LOAD_STR                 '\t#This class has Item property/method which allows indexed access with the object[key] syntax.'
             1628  LOAD_FAST                'stream'
             1630  LOAD_CONST               ('file',)
             1632  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1634  POP_TOP          

 L. 525      1636  LOAD_GLOBAL              print
             1638  LOAD_STR                 '\t#Some objects will accept a string or other type of key in addition to integers.'
             1640  LOAD_FAST                'stream'
             1642  LOAD_CONST               ('file',)
             1644  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1646  POP_TOP          

 L. 526      1648  LOAD_GLOBAL              print
             1650  LOAD_STR                 '\t#Note that many Office objects do not use zero-based indexing.'
             1652  LOAD_FAST                'stream'
             1654  LOAD_CONST               ('file',)
             1656  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1658  POP_TOP          

 L. 527      1660  LOAD_GLOBAL              print
             1662  LOAD_STR                 '\tdef __getitem__(self, key):'
             1664  LOAD_FAST                'stream'
             1666  LOAD_CONST               ('file',)
             1668  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1670  POP_TOP          

 L. 528      1672  LOAD_GLOBAL              print
             1674  LOAD_STR                 '\t\treturn self._get_good_object_(self._oleobj_.Invoke(*(%d, LCID, %d, 1, key)), "Item", %s)'

 L. 529      1676  LOAD_FAST                'entry'
             1678  LOAD_ATTR                desc
             1680  LOAD_CONST               0
             1682  BINARY_SUBSCR    
             1684  LOAD_FAST                'invoketype'
             1686  LOAD_FAST                'resultCLSID'
             1688  BUILD_TUPLE_3         3 

 L. 528      1690  BINARY_MODULO    

 L. 529      1692  LOAD_FAST                'stream'

 L. 528      1694  LOAD_CONST               ('file',)
             1696  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1698  POP_TOP          
           1700_0  COME_FROM          1598  '1598'

 L. 531      1700  LOAD_FAST                'specialItems'
             1702  LOAD_STR                 'count'
             1704  BINARY_SUBSCR    
         1706_1708  POP_JUMP_IF_FALSE  1842  'to 1842'

 L. 532      1710  LOAD_FAST                'specialItems'
             1712  LOAD_STR                 'count'
             1714  BINARY_SUBSCR    
             1716  UNPACK_SEQUENCE_3     3 
             1718  STORE_FAST               'entry'
             1720  STORE_FAST               'invoketype'
             1722  STORE_FAST               'propArgs'

 L. 533      1724  LOAD_FAST                'propArgs'
             1726  LOAD_CONST               None
             1728  <117>                 0  ''
         1730_1732  POP_JUMP_IF_FALSE  1752  'to 1752'

 L. 534      1734  LOAD_STR                 'method'
             1736  STORE_FAST               'typename'

 L. 535      1738  LOAD_FAST                'self'
             1740  LOAD_METHOD              MakeFuncMethod
             1742  LOAD_FAST                'entry'
             1744  LOAD_STR                 '__len__'
             1746  CALL_METHOD_2         2  ''
             1748  STORE_FAST               'ret'
             1750  JUMP_FORWARD       1766  'to 1766'
           1752_0  COME_FROM          1730  '1730'

 L. 537      1752  LOAD_STR                 'property'
             1754  STORE_FAST               'typename'

 L. 538      1756  LOAD_STR                 '\tdef __len__(self):\n\t\treturn self._ApplyTypes_(*%s)'
             1758  LOAD_FAST                'propArgs'
             1760  BINARY_MODULO    
             1762  BUILD_LIST_1          1 
             1764  STORE_FAST               'ret'
           1766_0  COME_FROM          1750  '1750'

 L. 539      1766  LOAD_GLOBAL              print
             1768  LOAD_STR                 '\t#This class has Count() %s - allow len(ob) to provide this'
             1770  LOAD_FAST                'typename'
             1772  BINARY_MODULO    
             1774  LOAD_FAST                'stream'
             1776  LOAD_CONST               ('file',)
             1778  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1780  POP_TOP          

 L. 540      1782  LOAD_FAST                'ret'
             1784  GET_ITER         
           1786_0  COME_FROM          1802  '1802'
             1786  FOR_ITER           1806  'to 1806'
             1788  STORE_FAST               'line'

 L. 541      1790  LOAD_GLOBAL              print
             1792  LOAD_FAST                'line'
             1794  LOAD_FAST                'stream'
             1796  LOAD_CONST               ('file',)
             1798  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1800  POP_TOP          
         1802_1804  JUMP_BACK          1786  'to 1786'
           1806_0  COME_FROM          1786  '1786'

 L. 543      1806  LOAD_GLOBAL              print
             1808  LOAD_STR                 "\t#This class has a __len__ - this is needed so 'if object:' always returns TRUE."
             1810  LOAD_FAST                'stream'
             1812  LOAD_CONST               ('file',)
             1814  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1816  POP_TOP          

 L. 544      1818  LOAD_GLOBAL              print
             1820  LOAD_STR                 '\tdef __nonzero__(self):'
             1822  LOAD_FAST                'stream'
             1824  LOAD_CONST               ('file',)
             1826  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1828  POP_TOP          

 L. 545      1830  LOAD_GLOBAL              print
             1832  LOAD_STR                 '\t\treturn True'
             1834  LOAD_FAST                'stream'
             1836  LOAD_CONST               ('file',)
             1838  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1840  POP_TOP          
           1842_0  COME_FROM          1706  '1706'

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

    def WriteClass--- This code section failed: ---

 L. 559         0  LOAD_FAST                'generator'
                2  LOAD_METHOD              checkWriteCoClassBaseClass
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 560         8  LOAD_FAST                'self'
               10  LOAD_ATTR                doc
               12  STORE_FAST               'doc'

 L. 561        14  LOAD_FAST                'generator'
               16  LOAD_ATTR                file
               18  STORE_FAST               'stream'

 L. 562        20  LOAD_FAST                'generator'
               22  LOAD_ATTR                generate_type
               24  LOAD_GLOBAL              GEN_DEMAND_CHILD
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_FALSE   170  'to 170'

 L. 564        30  BUILD_LIST_0          0 
               32  STORE_FAST               'referenced_items'

 L. 565        34  LOAD_FAST                'self'
               36  LOAD_ATTR                sources
               38  GET_ITER         
             40_0  COME_FROM            58  '58'
               40  FOR_ITER             60  'to 60'
               42  UNPACK_SEQUENCE_2     2 
               44  STORE_FAST               'ref'
               46  STORE_FAST               'flag'

 L. 566        48  LOAD_FAST                'referenced_items'
               50  LOAD_METHOD              append
               52  LOAD_FAST                'ref'
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          
               58  JUMP_BACK            40  'to 40'
             60_0  COME_FROM            40  '40'

 L. 567        60  LOAD_FAST                'self'
               62  LOAD_ATTR                interfaces
               64  GET_ITER         
             66_0  COME_FROM            84  '84'
               66  FOR_ITER             86  'to 86'
               68  UNPACK_SEQUENCE_2     2 
               70  STORE_FAST               'ref'
               72  STORE_FAST               'flag'

 L. 568        74  LOAD_FAST                'referenced_items'
               76  LOAD_METHOD              append
               78  LOAD_FAST                'ref'
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          
               84  JUMP_BACK            66  'to 66'
             86_0  COME_FROM            66  '66'

 L. 569        86  LOAD_GLOBAL              print
               88  LOAD_STR                 'import sys'
               90  LOAD_FAST                'stream'
               92  LOAD_CONST               ('file',)
               94  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               96  POP_TOP          

 L. 570        98  LOAD_FAST                'referenced_items'
              100  GET_ITER         
            102_0  COME_FROM           168  '168'
              102  FOR_ITER            170  'to 170'
              104  STORE_FAST               'ref'

 L. 571       106  LOAD_GLOBAL              print
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

 L. 572       130  LOAD_GLOBAL              print
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

 L. 574       162  LOAD_CONST               1
              164  LOAD_FAST                'ref'
              166  STORE_ATTR               bWritten
              168  JUMP_BACK           102  'to 102'
            170_0  COME_FROM           102  '102'
            170_1  COME_FROM            28  '28'

 L. 575       170  SETUP_FINALLY       204  'to 204'

 L. 576       172  LOAD_GLOBAL              pythoncom
              174  LOAD_METHOD              ProgIDFromCLSID
              176  LOAD_FAST                'self'
              178  LOAD_ATTR                clsid
              180  CALL_METHOD_1         1  ''
              182  STORE_FAST               'progId'

 L. 577       184  LOAD_GLOBAL              print
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

 L. 578       204  DUP_TOP          
              206  LOAD_GLOBAL              pythoncom
              208  LOAD_ATTR                com_error
              210  <121>               222  ''
              212  POP_TOP          
              214  POP_TOP          
              216  POP_TOP          

 L. 579       218  POP_EXCEPT       
              220  JUMP_FORWARD        224  'to 224'
              222  <48>             
            224_0  COME_FROM           220  '220'
            224_1  COME_FROM           202  '202'

 L. 580       224  LOAD_GLOBAL              print
              226  LOAD_STR                 'class %s(CoClassBaseClass): # A CoClass'
              228  LOAD_FAST                'self'
              230  LOAD_ATTR                python_name
              232  BINARY_MODULO    
              234  LOAD_FAST                'stream'
              236  LOAD_CONST               ('file',)
              238  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              240  POP_TOP          

 L. 581       242  LOAD_FAST                'doc'
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

 L. 582       278  LOAD_GLOBAL              print
              280  LOAD_STR                 '\tCLSID = %r'
              282  LOAD_FAST                'self'
              284  LOAD_ATTR                clsid
              286  BUILD_TUPLE_1         1 
              288  BINARY_MODULO    
              290  LOAD_FAST                'stream'
              292  LOAD_CONST               ('file',)
              294  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              296  POP_TOP          

 L. 583       298  LOAD_GLOBAL              print
              300  LOAD_STR                 '\tcoclass_sources = ['
              302  LOAD_FAST                'stream'
              304  LOAD_CONST               ('file',)
              306  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              308  POP_TOP          

 L. 584       310  LOAD_CONST               None
              312  STORE_FAST               'defItem'

 L. 585       314  LOAD_FAST                'self'
              316  LOAD_ATTR                sources
              318  GET_ITER         
            320_0  COME_FROM           390  '390'
              320  FOR_ITER            394  'to 394'
              322  UNPACK_SEQUENCE_2     2 
              324  STORE_FAST               'item'
              326  STORE_FAST               'flag'

 L. 586       328  LOAD_FAST                'flag'
              330  LOAD_GLOBAL              pythoncom
              332  LOAD_ATTR                IMPLTYPEFLAG_FDEFAULT
              334  BINARY_AND       
          336_338  POP_JUMP_IF_FALSE   344  'to 344'

 L. 587       340  LOAD_FAST                'item'
              342  STORE_FAST               'defItem'
            344_0  COME_FROM           336  '336'

 L. 590       344  LOAD_FAST                'item'
              346  LOAD_ATTR                bWritten
          348_350  POP_JUMP_IF_FALSE   360  'to 360'
              352  LOAD_FAST                'item'
              354  LOAD_ATTR                python_name
              356  STORE_FAST               'key'
              358  JUMP_FORWARD        374  'to 374'
            360_0  COME_FROM           348  '348'

 L. 591       360  LOAD_GLOBAL              repr
              362  LOAD_GLOBAL              str
              364  LOAD_FAST                'item'
              366  LOAD_ATTR                clsid
              368  CALL_FUNCTION_1       1  ''
              370  CALL_FUNCTION_1       1  ''
              372  STORE_FAST               'key'
            374_0  COME_FROM           358  '358'

 L. 592       374  LOAD_GLOBAL              print
              376  LOAD_STR                 '\t\t%s,'
              378  LOAD_FAST                'key'
              380  BINARY_MODULO    
              382  LOAD_FAST                'stream'
              384  LOAD_CONST               ('file',)
              386  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              388  POP_TOP          
          390_392  JUMP_BACK           320  'to 320'
            394_0  COME_FROM           320  '320'

 L. 593       394  LOAD_GLOBAL              print
              396  LOAD_STR                 '\t]'
              398  LOAD_FAST                'stream'
              400  LOAD_CONST               ('file',)
              402  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              404  POP_TOP          

 L. 594       406  LOAD_FAST                'defItem'
          408_410  POP_JUMP_IF_FALSE   460  'to 460'

 L. 595       412  LOAD_FAST                'defItem'
              414  LOAD_ATTR                bWritten
          416_418  POP_JUMP_IF_FALSE   428  'to 428'
              420  LOAD_FAST                'defItem'
              422  LOAD_ATTR                python_name
              424  STORE_FAST               'defName'
              426  JUMP_FORWARD        442  'to 442'
            428_0  COME_FROM           416  '416'

 L. 596       428  LOAD_GLOBAL              repr
              430  LOAD_GLOBAL              str
              432  LOAD_FAST                'defItem'
              434  LOAD_ATTR                clsid
              436  CALL_FUNCTION_1       1  ''
              438  CALL_FUNCTION_1       1  ''
              440  STORE_FAST               'defName'
            442_0  COME_FROM           426  '426'

 L. 597       442  LOAD_GLOBAL              print
              444  LOAD_STR                 '\tdefault_source = %s'
              446  LOAD_FAST                'defName'
              448  BUILD_TUPLE_1         1 
              450  BINARY_MODULO    
              452  LOAD_FAST                'stream'
              454  LOAD_CONST               ('file',)
              456  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              458  POP_TOP          
            460_0  COME_FROM           408  '408'

 L. 598       460  LOAD_GLOBAL              print
              462  LOAD_STR                 '\tcoclass_interfaces = ['
              464  LOAD_FAST                'stream'
              466  LOAD_CONST               ('file',)
              468  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              470  POP_TOP          

 L. 599       472  LOAD_CONST               None
              474  STORE_FAST               'defItem'

 L. 600       476  LOAD_FAST                'self'
              478  LOAD_ATTR                interfaces
              480  GET_ITER         
            482_0  COME_FROM           554  '554'
              482  FOR_ITER            558  'to 558'
              484  UNPACK_SEQUENCE_2     2 
              486  STORE_FAST               'item'
              488  STORE_FAST               'flag'

 L. 601       490  LOAD_FAST                'flag'
              492  LOAD_GLOBAL              pythoncom
              494  LOAD_ATTR                IMPLTYPEFLAG_FDEFAULT
              496  BINARY_AND       
          498_500  POP_JUMP_IF_FALSE   506  'to 506'

 L. 602       502  LOAD_FAST                'item'
              504  STORE_FAST               'defItem'
            506_0  COME_FROM           498  '498'

 L. 604       506  LOAD_FAST                'item'
              508  LOAD_ATTR                bWritten
          510_512  POP_JUMP_IF_FALSE   522  'to 522'
              514  LOAD_FAST                'item'
              516  LOAD_ATTR                python_name
              518  STORE_FAST               'key'
              520  JUMP_FORWARD        536  'to 536'
            522_0  COME_FROM           510  '510'

 L. 605       522  LOAD_GLOBAL              repr
              524  LOAD_GLOBAL              str
              526  LOAD_FAST                'item'
              528  LOAD_ATTR                clsid
              530  CALL_FUNCTION_1       1  ''
              532  CALL_FUNCTION_1       1  ''
              534  STORE_FAST               'key'
            536_0  COME_FROM           520  '520'

 L. 606       536  LOAD_GLOBAL              print
              538  LOAD_STR                 '\t\t%s,'
              540  LOAD_FAST                'key'
              542  BUILD_TUPLE_1         1 
              544  BINARY_MODULO    
              546  LOAD_FAST                'stream'
              548  LOAD_CONST               ('file',)
              550  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              552  POP_TOP          
          554_556  JUMP_BACK           482  'to 482'
            558_0  COME_FROM           482  '482'

 L. 607       558  LOAD_GLOBAL              print
              560  LOAD_STR                 '\t]'
              562  LOAD_FAST                'stream'
              564  LOAD_CONST               ('file',)
              566  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              568  POP_TOP          

 L. 608       570  LOAD_FAST                'defItem'
          572_574  POP_JUMP_IF_FALSE   624  'to 624'

 L. 609       576  LOAD_FAST                'defItem'
              578  LOAD_ATTR                bWritten
          580_582  POP_JUMP_IF_FALSE   592  'to 592'
              584  LOAD_FAST                'defItem'
              586  LOAD_ATTR                python_name
              588  STORE_FAST               'defName'
              590  JUMP_FORWARD        606  'to 606'
            592_0  COME_FROM           580  '580'

 L. 610       592  LOAD_GLOBAL              repr
              594  LOAD_GLOBAL              str
              596  LOAD_FAST                'defItem'
              598  LOAD_ATTR                clsid
              600  CALL_FUNCTION_1       1  ''
              602  CALL_FUNCTION_1       1  ''
              604  STORE_FAST               'defName'
            606_0  COME_FROM           590  '590'

 L. 611       606  LOAD_GLOBAL              print
              608  LOAD_STR                 '\tdefault_interface = %s'
              610  LOAD_FAST                'defName'
              612  BUILD_TUPLE_1         1 
              614  BINARY_MODULO    
              616  LOAD_FAST                'stream'
              618  LOAD_CONST               ('file',)
              620  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              622  POP_TOP          
            624_0  COME_FROM           572  '572'

 L. 612       624  LOAD_CONST               1
              626  LOAD_FAST                'self'
              628  STORE_ATTR               bWritten

 L. 613       630  LOAD_GLOBAL              print
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

 L. 645         0  LOAD_FAST                'bUnicodeToString'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  <74>             
               10  LOAD_STR                 'this is deprecated and will go away'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 646        16  LOAD_CONST               0
               18  LOAD_FAST                'self'
               20  STORE_ATTR               bHaveWrittenDispatchBaseClass

 L. 647        22  LOAD_CONST               0
               24  LOAD_FAST                'self'
               26  STORE_ATTR               bHaveWrittenCoClassBaseClass

 L. 648        28  LOAD_CONST               0
               30  LOAD_FAST                'self'
               32  STORE_ATTR               bHaveWrittenEventBaseClass

 L. 649        34  LOAD_FAST                'typelib'
               36  LOAD_FAST                'self'
               38  STORE_ATTR               typelib

 L. 650        40  LOAD_FAST                'sourceFilename'
               42  LOAD_FAST                'self'
               44  STORE_ATTR               sourceFilename

 L. 651        46  LOAD_FAST                'bBuildHidden'
               48  LOAD_FAST                'self'
               50  STORE_ATTR               bBuildHidden

 L. 652        52  LOAD_FAST                'progressObject'
               54  LOAD_FAST                'self'
               56  STORE_ATTR               progress

 L. 654        58  LOAD_CONST               None
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

 L. 667         0  LOAD_FAST                'type_info_tuple'
                2  UNPACK_SEQUENCE_4     4 
                4  STORE_FAST               'info'
                6  STORE_FAST               'infotype'
                8  STORE_FAST               'doc'
               10  STORE_FAST               'attr'

 L. 669        12  BUILD_LIST_0          0 
               14  STORE_FAST               'child_infos'

 L. 670        16  LOAD_GLOBAL              range
               18  LOAD_FAST                'attr'
               20  LOAD_CONST               8
               22  BINARY_SUBSCR    
               24  CALL_FUNCTION_1       1  ''
               26  GET_ITER         
             28_0  COME_FROM           126  '126'
             28_1  COME_FROM            80  '80'
               28  FOR_ITER            128  'to 128'
               30  STORE_FAST               'j'

 L. 671        32  LOAD_FAST                'info'
               34  LOAD_METHOD              GetImplTypeFlags
               36  LOAD_FAST                'j'
               38  CALL_METHOD_1         1  ''
               40  STORE_FAST               'flags'

 L. 672        42  SETUP_FINALLY        64  'to 64'

 L. 673        44  LOAD_FAST                'info'
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

 L. 674        64  DUP_TOP          
               66  LOAD_GLOBAL              pythoncom
               68  LOAD_ATTR                com_error
               70  <121>                86  ''
               72  POP_TOP          
               74  POP_TOP          
               76  POP_TOP          

 L. 676        78  POP_EXCEPT       
               80  JUMP_BACK            28  'to 28'
               82  POP_EXCEPT       
               84  JUMP_FORWARD         88  'to 88'
               86  <48>             
             88_0  COME_FROM            84  '84'
             88_1  COME_FROM            62  '62'

 L. 677        88  LOAD_FAST                'refType'
               90  LOAD_METHOD              GetTypeAttr
               92  CALL_METHOD_0         0  ''
               94  STORE_FAST               'refAttr'

 L. 678        96  LOAD_FAST                'child_infos'
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
            128_0  COME_FROM            28  '28'

 L. 681       128  LOAD_GLOBAL              CoClassItem
              130  LOAD_FAST                'info'
              132  LOAD_FAST                'attr'
              134  LOAD_FAST                'doc'
              136  CALL_FUNCTION_3       3  ''
              138  STORE_FAST               'newItem'

 L. 682       140  LOAD_FAST                'newItem'
              142  LOAD_FAST                'child_infos'
              144  BUILD_TUPLE_2         2 
              146  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 70

    def _Build_CoClassChildren--- This code section failed: ---

 L. 685         0  BUILD_MAP_0           0 
                2  STORE_FAST               'sources'

 L. 686         4  BUILD_MAP_0           0 
                6  STORE_FAST               'interfaces'

 L. 687         8  LOAD_FAST                'coclass_info'
               10  GET_ITER         
             12_0  COME_FROM           254  '254'
             12_1  COME_FROM           188  '188'
             12_2  COME_FROM           174  '174'
             12_3  COME_FROM            64  '64'
             12_4  COME_FROM            50  '50'
               12  FOR_ITER            256  'to 256'
               14  UNPACK_SEQUENCE_6     6 
               16  STORE_FAST               'info'
               18  STORE_FAST               'info_type'
               20  STORE_FAST               'refType'
               22  STORE_FAST               'doc'
               24  STORE_FAST               'refAttr'
               26  STORE_FAST               'flags'

 L. 689        28  LOAD_FAST                'refAttr'
               30  LOAD_ATTR                typekind
               32  LOAD_GLOBAL              pythoncom
               34  LOAD_ATTR                TKIND_DISPATCH
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_TRUE     66  'to 66'

 L. 690        40  LOAD_FAST                'refAttr'
               42  LOAD_ATTR                typekind
               44  LOAD_GLOBAL              pythoncom
               46  LOAD_ATTR                TKIND_INTERFACE
               48  COMPARE_OP               ==

 L. 689        50  POP_JUMP_IF_FALSE_BACK    12  'to 12'

 L. 690        52  LOAD_FAST                'refAttr'
               54  LOAD_CONST               11
               56  BINARY_SUBSCR    
               58  LOAD_GLOBAL              pythoncom
               60  LOAD_ATTR                TYPEFLAG_FDISPATCHABLE
               62  BINARY_AND       

 L. 689        64  POP_JUMP_IF_FALSE_BACK    12  'to 12'
             66_0  COME_FROM            38  '38'

 L. 691        66  LOAD_FAST                'refAttr'
               68  LOAD_CONST               0
               70  BINARY_SUBSCR    
               72  STORE_FAST               'clsid'

 L. 692        74  LOAD_FAST                'clsid'
               76  LOAD_FAST                'oleItems'
               78  <118>                 0  ''
               80  POP_JUMP_IF_FALSE    92  'to 92'

 L. 693        82  LOAD_FAST                'oleItems'
               84  LOAD_FAST                'clsid'
               86  BINARY_SUBSCR    
               88  STORE_FAST               'dispItem'
               90  JUMP_FORWARD        114  'to 114'
             92_0  COME_FROM            80  '80'

 L. 695        92  LOAD_GLOBAL              DispatchItem
               94  LOAD_FAST                'refType'
               96  LOAD_FAST                'refAttr'
               98  LOAD_FAST                'doc'
              100  CALL_FUNCTION_3       3  ''
              102  STORE_FAST               'dispItem'

 L. 696       104  LOAD_FAST                'dispItem'
              106  LOAD_FAST                'oleItems'
              108  LOAD_FAST                'dispItem'
              110  LOAD_ATTR                clsid
              112  STORE_SUBSCR     
            114_0  COME_FROM            90  '90'

 L. 697       114  LOAD_FAST                'coclass'
              116  LOAD_ATTR                clsid
              118  LOAD_FAST                'dispItem'
              120  STORE_ATTR               coclass_clsid

 L. 698       122  LOAD_FAST                'flags'
              124  LOAD_GLOBAL              pythoncom
              126  LOAD_ATTR                IMPLTYPEFLAG_FSOURCE
              128  BINARY_AND       
              130  POP_JUMP_IF_FALSE   154  'to 154'

 L. 699       132  LOAD_CONST               1
              134  LOAD_FAST                'dispItem'
              136  STORE_ATTR               bIsSink

 L. 700       138  LOAD_FAST                'dispItem'
              140  LOAD_FAST                'flags'
              142  BUILD_TUPLE_2         2 
              144  LOAD_FAST                'sources'
              146  LOAD_FAST                'dispItem'
              148  LOAD_ATTR                clsid
              150  STORE_SUBSCR     
              152  JUMP_FORWARD        168  'to 168'
            154_0  COME_FROM           130  '130'

 L. 702       154  LOAD_FAST                'dispItem'
              156  LOAD_FAST                'flags'
              158  BUILD_TUPLE_2         2 
              160  LOAD_FAST                'interfaces'
              162  LOAD_FAST                'dispItem'
              164  LOAD_ATTR                clsid
              166  STORE_SUBSCR     
            168_0  COME_FROM           152  '152'

 L. 704       168  LOAD_FAST                'clsid'
              170  LOAD_FAST                'vtableItems'
              172  <118>                 1  ''
              174  POP_JUMP_IF_FALSE_BACK    12  'to 12'
              176  LOAD_FAST                'refAttr'
              178  LOAD_CONST               11
              180  BINARY_SUBSCR    
              182  LOAD_GLOBAL              pythoncom
              184  LOAD_ATTR                TYPEFLAG_FDUAL
              186  BINARY_AND       
              188  POP_JUMP_IF_FALSE_BACK    12  'to 12'

 L. 705       190  LOAD_FAST                'refType'
              192  LOAD_METHOD              GetRefTypeInfo
              194  LOAD_FAST                'refType'
              196  LOAD_METHOD              GetRefTypeOfImplType
              198  LOAD_CONST               -1
              200  CALL_METHOD_1         1  ''
              202  CALL_METHOD_1         1  ''
              204  STORE_FAST               'refType'

 L. 706       206  LOAD_FAST                'refType'
              208  LOAD_METHOD              GetTypeAttr
              210  CALL_METHOD_0         0  ''
              212  STORE_FAST               'refAttr'

 L. 707       214  LOAD_FAST                'refAttr'
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

 L. 708       234  LOAD_GLOBAL              VTableItem
              236  LOAD_FAST                'refType'
              238  LOAD_FAST                'refAttr'
              240  LOAD_FAST                'doc'
              242  CALL_FUNCTION_3       3  ''
              244  STORE_FAST               'vtableItem'

 L. 709       246  LOAD_FAST                'vtableItem'
              248  LOAD_FAST                'vtableItems'
              250  LOAD_FAST                'clsid'
              252  STORE_SUBSCR     
              254  JUMP_BACK            12  'to 12'
            256_0  COME_FROM            12  '12'

 L. 710       256  LOAD_GLOBAL              list
              258  LOAD_FAST                'sources'
              260  LOAD_METHOD              values
              262  CALL_METHOD_0         0  ''
              264  CALL_FUNCTION_1       1  ''
              266  LOAD_FAST                'coclass'
              268  STORE_ATTR               sources

 L. 711       270  LOAD_GLOBAL              list
              272  LOAD_FAST                'interfaces'
              274  LOAD_METHOD              values
              276  CALL_METHOD_0         0  ''
              278  CALL_FUNCTION_1       1  ''
              280  LOAD_FAST                'coclass'
              282  STORE_ATTR               interfaces

Parse error at or near `<118>' instruction at offset 78

    def _Build_Interface--- This code section failed: ---

 L. 714         0  LOAD_FAST                'type_info_tuple'
                2  UNPACK_SEQUENCE_4     4 
                4  STORE_FAST               'info'
                6  STORE_FAST               'infotype'
                8  STORE_FAST               'doc'
               10  STORE_FAST               'attr'

 L. 715        12  LOAD_CONST               None
               14  DUP_TOP          
               16  STORE_FAST               'oleItem'
               18  STORE_FAST               'vtableItem'

 L. 716        20  LOAD_FAST                'infotype'
               22  LOAD_GLOBAL              pythoncom
               24  LOAD_ATTR                TKIND_DISPATCH
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_TRUE     54  'to 54'

 L. 717        30  LOAD_FAST                'infotype'
               32  LOAD_GLOBAL              pythoncom
               34  LOAD_ATTR                TKIND_INTERFACE
               36  COMPARE_OP               ==

 L. 716        38  POP_JUMP_IF_FALSE   118  'to 118'

 L. 717        40  LOAD_FAST                'attr'
               42  LOAD_CONST               11
               44  BINARY_SUBSCR    
               46  LOAD_GLOBAL              pythoncom
               48  LOAD_ATTR                TYPEFLAG_FDISPATCHABLE
               50  BINARY_AND       

 L. 716        52  POP_JUMP_IF_FALSE   118  'to 118'
             54_0  COME_FROM            28  '28'

 L. 718        54  LOAD_GLOBAL              DispatchItem
               56  LOAD_FAST                'info'
               58  LOAD_FAST                'attr'
               60  LOAD_FAST                'doc'
               62  CALL_FUNCTION_3       3  ''
               64  STORE_FAST               'oleItem'

 L. 720        66  LOAD_FAST                'attr'
               68  LOAD_ATTR                wTypeFlags
               70  LOAD_GLOBAL              pythoncom
               72  LOAD_ATTR                TYPEFLAG_FDUAL
               74  BINARY_AND       
               76  POP_JUMP_IF_FALSE   114  'to 114'

 L. 722        78  LOAD_FAST                'info'
               80  LOAD_METHOD              GetRefTypeOfImplType
               82  LOAD_CONST               -1
               84  CALL_METHOD_1         1  ''
               86  STORE_FAST               'refhtype'

 L. 723        88  LOAD_FAST                'info'
               90  LOAD_METHOD              GetRefTypeInfo
               92  LOAD_FAST                'refhtype'
               94  CALL_METHOD_1         1  ''
               96  STORE_FAST               'info'

 L. 724        98  LOAD_FAST                'info'
              100  LOAD_METHOD              GetTypeAttr
              102  CALL_METHOD_0         0  ''
              104  STORE_FAST               'attr'

 L. 725       106  LOAD_GLOBAL              pythoncom
              108  LOAD_ATTR                TKIND_INTERFACE
              110  STORE_FAST               'infotype'
              112  JUMP_FORWARD        118  'to 118'
            114_0  COME_FROM            76  '76'

 L. 727       114  LOAD_CONST               None
              116  STORE_FAST               'infotype'
            118_0  COME_FROM           112  '112'
            118_1  COME_FROM            52  '52'
            118_2  COME_FROM            38  '38'

 L. 728       118  LOAD_FAST                'infotype'
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

 L. 729       140  LOAD_FAST                'infotype'
              142  LOAD_GLOBAL              pythoncom
              144  LOAD_ATTR                TKIND_INTERFACE
              146  COMPARE_OP               ==
              148  POP_JUMP_IF_FALSE   162  'to 162'

 L. 730       150  LOAD_GLOBAL              VTableItem
              152  LOAD_FAST                'info'
              154  LOAD_FAST                'attr'
              156  LOAD_FAST                'doc'
              158  CALL_FUNCTION_3       3  ''
              160  STORE_FAST               'vtableItem'
            162_0  COME_FROM           148  '148'

 L. 731       162  LOAD_FAST                'oleItem'
              164  LOAD_FAST                'vtableItem'
              166  BUILD_TUPLE_2         2 
              168  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 128

    def BuildOleItemsFromType--- This code section failed: ---

 L. 734         0  LOAD_FAST                'self'
                2  LOAD_ATTR                bBuildHidden
                4  POP_JUMP_IF_TRUE     14  'to 14'
                6  <74>             
                8  LOAD_STR                 'This code doesnt look at the hidden flag - I thought everyone set it true!?!?!'
               10  CALL_FUNCTION_1       1  ''
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             4  '4'

 L. 735        14  BUILD_MAP_0           0 
               16  STORE_FAST               'oleItems'

 L. 736        18  BUILD_MAP_0           0 
               20  STORE_FAST               'enumItems'

 L. 737        22  BUILD_MAP_0           0 
               24  STORE_FAST               'recordItems'

 L. 738        26  BUILD_MAP_0           0 
               28  STORE_FAST               'vtableItems'

 L. 740        30  LOAD_FAST                'self'
               32  LOAD_METHOD              CollectOleItemInfosFromType
               34  CALL_METHOD_0         0  ''
               36  GET_ITER         
             38_0  COME_FROM           304  '304'
             38_1  COME_FROM           286  '286'
             38_2  COME_FROM           232  '232'
             38_3  COME_FROM           230  '230'
             38_4  COME_FROM           218  '218'
             38_5  COME_FROM           174  '174'
             38_6  COME_FROM           110  '110'
            38_40  FOR_ITER            306  'to 306'
               42  STORE_FAST               'type_info_tuple'

 L. 741        44  LOAD_FAST                'type_info_tuple'
               46  UNPACK_SEQUENCE_4     4 
               48  STORE_FAST               'info'
               50  STORE_FAST               'infotype'
               52  STORE_FAST               'doc'
               54  STORE_FAST               'attr'

 L. 742        56  LOAD_FAST                'attr'
               58  LOAD_CONST               0
               60  BINARY_SUBSCR    
               62  STORE_FAST               'clsid'

 L. 743        64  LOAD_FAST                'infotype'
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

 L. 744        84  LOAD_GLOBAL              EnumerationItem
               86  LOAD_FAST                'info'
               88  LOAD_FAST                'attr'
               90  LOAD_FAST                'doc'
               92  CALL_FUNCTION_3       3  ''
               94  STORE_FAST               'newItem'

 L. 745        96  LOAD_FAST                'newItem'
               98  LOAD_FAST                'enumItems'
              100  LOAD_FAST                'newItem'
              102  LOAD_ATTR                doc
              104  LOAD_CONST               0
              106  BINARY_SUBSCR    
              108  STORE_SUBSCR     
              110  JUMP_BACK            38  'to 38'
            112_0  COME_FROM            82  '82'

 L. 748       112  LOAD_FAST                'infotype'
              114  LOAD_GLOBAL              pythoncom
              116  LOAD_ATTR                TKIND_DISPATCH
              118  LOAD_GLOBAL              pythoncom
              120  LOAD_ATTR                TKIND_INTERFACE
              122  BUILD_TUPLE_2         2 
              124  <118>                 0  ''
              126  POP_JUMP_IF_FALSE   176  'to 176'

 L. 749       128  LOAD_FAST                'clsid'
              130  LOAD_FAST                'oleItems'
              132  <118>                 1  ''
              134  POP_JUMP_IF_FALSE   174  'to 174'

 L. 750       136  LOAD_FAST                'self'
              138  LOAD_METHOD              _Build_Interface
              140  LOAD_FAST                'type_info_tuple'
              142  CALL_METHOD_1         1  ''
              144  UNPACK_SEQUENCE_2     2 
              146  STORE_FAST               'oleItem'
              148  STORE_FAST               'vtableItem'

 L. 751       150  LOAD_FAST                'oleItem'
              152  LOAD_FAST                'oleItems'
              154  LOAD_FAST                'clsid'
              156  STORE_SUBSCR     

 L. 752       158  LOAD_FAST                'vtableItem'
              160  LOAD_CONST               None
              162  <117>                 1  ''
              164  POP_JUMP_IF_FALSE   174  'to 174'

 L. 753       166  LOAD_FAST                'vtableItem'
              168  LOAD_FAST                'vtableItems'
              170  LOAD_FAST                'clsid'
              172  STORE_SUBSCR     
            174_0  COME_FROM           164  '164'
            174_1  COME_FROM           134  '134'
              174  JUMP_BACK            38  'to 38'
            176_0  COME_FROM           126  '126'

 L. 754       176  LOAD_FAST                'infotype'
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

 L. 755       196  LOAD_GLOBAL              RecordItem
              198  LOAD_FAST                'info'
              200  LOAD_FAST                'attr'
              202  LOAD_FAST                'doc'
              204  CALL_FUNCTION_3       3  ''
              206  STORE_FAST               'newItem'

 L. 756       208  LOAD_FAST                'newItem'
              210  LOAD_FAST                'recordItems'
              212  LOAD_FAST                'newItem'
              214  LOAD_ATTR                clsid
              216  STORE_SUBSCR     
              218  JUMP_BACK            38  'to 38'
            220_0  COME_FROM           194  '194'

 L. 757       220  LOAD_FAST                'infotype'
              222  LOAD_GLOBAL              pythoncom
              224  LOAD_ATTR                TKIND_ALIAS
              226  COMPARE_OP               ==
              228  POP_JUMP_IF_FALSE   234  'to 234'

 L. 759       230  CONTINUE             38  'to 38'
              232  JUMP_BACK            38  'to 38'
            234_0  COME_FROM           228  '228'

 L. 760       234  LOAD_FAST                'infotype'
              236  LOAD_GLOBAL              pythoncom
              238  LOAD_ATTR                TKIND_COCLASS
              240  COMPARE_OP               ==
          242_244  POP_JUMP_IF_FALSE   288  'to 288'

 L. 761       246  LOAD_FAST                'self'
              248  LOAD_METHOD              _Build_CoClass
              250  LOAD_FAST                'type_info_tuple'
              252  CALL_METHOD_1         1  ''
              254  UNPACK_SEQUENCE_2     2 
              256  STORE_FAST               'newItem'
              258  STORE_FAST               'child_infos'

 L. 762       260  LOAD_FAST                'self'
              262  LOAD_METHOD              _Build_CoClassChildren
              264  LOAD_FAST                'newItem'
              266  LOAD_FAST                'child_infos'
              268  LOAD_FAST                'oleItems'
              270  LOAD_FAST                'vtableItems'
              272  CALL_METHOD_4         4  ''
              274  POP_TOP          

 L. 763       276  LOAD_FAST                'newItem'
              278  LOAD_FAST                'oleItems'
              280  LOAD_FAST                'newItem'
              282  LOAD_ATTR                clsid
              284  STORE_SUBSCR     
              286  JUMP_BACK            38  'to 38'
            288_0  COME_FROM           242  '242'

 L. 765       288  LOAD_FAST                'self'
              290  LOAD_ATTR                progress
              292  LOAD_METHOD              LogWarning
              294  LOAD_STR                 'Unknown TKIND found: %d'
              296  LOAD_FAST                'infotype'
              298  BINARY_MODULO    
              300  CALL_METHOD_1         1  ''
              302  POP_TOP          
              304  JUMP_BACK            38  'to 38'
            306_0  COME_FROM            38  '38'

 L. 767       306  LOAD_FAST                'oleItems'
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

 L. 782         0  LOAD_FAST                'f'
                2  LOAD_METHOD              close
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 783         8  SETUP_FINALLY        24  'to 24'

 L. 784        10  LOAD_GLOBAL              os
               12  LOAD_METHOD              unlink
               14  LOAD_FAST                'filename'
               16  CALL_METHOD_1         1  ''
               18  POP_TOP          
               20  POP_BLOCK        
               22  JUMP_FORWARD         44  'to 44'
             24_0  COME_FROM_FINALLY     8  '8'

 L. 785        24  DUP_TOP          
               26  LOAD_GLOBAL              os
               28  LOAD_ATTR                error
               30  <121>                42  ''
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 786        38  POP_EXCEPT       
               40  JUMP_FORWARD         44  'to 44'
               42  <48>             
             44_0  COME_FROM            40  '40'
             44_1  COME_FROM            22  '22'

 L. 787        44  LOAD_FAST                'self'
               46  LOAD_METHOD              get_temp_filename
               48  LOAD_FAST                'filename'
               50  CALL_METHOD_1         1  ''
               52  STORE_FAST               'temp_filename'

 L. 788        54  LOAD_FAST                'worked'
               56  POP_JUMP_IF_FALSE   146  'to 146'

 L. 789        58  SETUP_FINALLY        76  'to 76'

 L. 790        60  LOAD_GLOBAL              os
               62  LOAD_METHOD              rename
               64  LOAD_FAST                'temp_filename'
               66  LOAD_FAST                'filename'
               68  CALL_METHOD_2         2  ''
               70  POP_TOP          
               72  POP_BLOCK        
               74  JUMP_FORWARD        156  'to 156'
             76_0  COME_FROM_FINALLY    58  '58'

 L. 791        76  DUP_TOP          
               78  LOAD_GLOBAL              os
               80  LOAD_ATTR                error
               82  <121>               142  ''
               84  POP_TOP          
               86  POP_TOP          
               88  POP_TOP          

 L. 805        90  SETUP_FINALLY       106  'to 106'

 L. 806        92  LOAD_GLOBAL              os
               94  LOAD_METHOD              unlink
               96  LOAD_FAST                'filename'
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          
              102  POP_BLOCK        
              104  JUMP_FORWARD        126  'to 126'
            106_0  COME_FROM_FINALLY    90  '90'

 L. 807       106  DUP_TOP          
              108  LOAD_GLOBAL              os
              110  LOAD_ATTR                error
              112  <121>               124  ''
              114  POP_TOP          
              116  POP_TOP          
              118  POP_TOP          

 L. 808       120  POP_EXCEPT       
              122  JUMP_FORWARD        126  'to 126'
              124  <48>             
            126_0  COME_FROM           122  '122'
            126_1  COME_FROM           104  '104'

 L. 809       126  LOAD_GLOBAL              os
              128  LOAD_METHOD              rename
              130  LOAD_FAST                'temp_filename'
              132  LOAD_FAST                'filename'
              134  CALL_METHOD_2         2  ''
              136  POP_TOP          
              138  POP_EXCEPT       
              140  JUMP_FORWARD        156  'to 156'
              142  <48>             
              144  JUMP_FORWARD        156  'to 156'
            146_0  COME_FROM            56  '56'

 L. 811       146  LOAD_GLOBAL              os
              148  LOAD_METHOD              unlink
              150  LOAD_FAST                'temp_filename'
              152  CALL_METHOD_1         1  ''
              154  POP_TOP          
            156_0  COME_FROM           144  '144'
            156_1  COME_FROM           140  '140'
            156_2  COME_FROM            74  '74'

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

 L. 827         0  LOAD_FAST                'self'
                2  LOAD_ATTR                typelib
                4  LOAD_METHOD              GetLibAttr
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'la'

 L. 828        10  LOAD_FAST                'self'
               12  LOAD_ATTR                typelib
               14  LOAD_METHOD              GetDocumentation
               16  LOAD_CONST               -1
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'moduleDoc'

 L. 829        22  LOAD_STR                 ''
               24  STORE_FAST               'docDesc'

 L. 830        26  LOAD_FAST                'moduleDoc'
               28  LOAD_CONST               1
               30  BINARY_SUBSCR    
               32  POP_JUMP_IF_FALSE    42  'to 42'

 L. 831        34  LOAD_FAST                'moduleDoc'
               36  LOAD_CONST               1
               38  BINARY_SUBSCR    
               40  STORE_FAST               'docDesc'
             42_0  COME_FROM            32  '32'

 L. 834        42  LOAD_CONST               0
               44  LOAD_FAST                'self'
               46  STORE_ATTR               bHaveWrittenDispatchBaseClass

 L. 835        48  LOAD_CONST               0
               50  LOAD_FAST                'self'
               52  STORE_ATTR               bHaveWrittenCoClassBaseClass

 L. 836        54  LOAD_CONST               0
               56  LOAD_FAST                'self'
               58  STORE_ATTR               bHaveWrittenEventBaseClass

 L. 840        60  LOAD_FAST                'self'
               62  LOAD_ATTR                file
               64  LOAD_ATTR                encoding
               66  POP_JUMP_IF_TRUE     78  'to 78'
               68  <74>             
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                file
               74  CALL_FUNCTION_1       1  ''
               76  RAISE_VARARGS_1       1  'exception instance'
             78_0  COME_FROM            66  '66'

 L. 841        78  LOAD_FAST                'self'
               80  LOAD_ATTR                file
               82  LOAD_ATTR                encoding
               84  STORE_FAST               'encoding'

 L. 843        86  LOAD_GLOBAL              print
               88  LOAD_STR                 '# -*- coding: %s -*-'
               90  LOAD_FAST                'encoding'
               92  BUILD_TUPLE_1         1 
               94  BINARY_MODULO    
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                file
              100  LOAD_CONST               ('file',)
              102  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              104  POP_TOP          

 L. 844       106  LOAD_GLOBAL              print
              108  LOAD_STR                 '# Created by makepy.py version %s'
              110  LOAD_GLOBAL              makepy_version
              112  BUILD_TUPLE_1         1 
              114  BINARY_MODULO    
              116  LOAD_FAST                'self'
              118  LOAD_ATTR                file
              120  LOAD_CONST               ('file',)
              122  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              124  POP_TOP          

 L. 845       126  LOAD_GLOBAL              print
              128  LOAD_STR                 '# By python version %s'

 L. 846       130  LOAD_GLOBAL              sys
              132  LOAD_ATTR                version
              134  LOAD_METHOD              replace
              136  LOAD_STR                 '\n'
              138  LOAD_STR                 '-'
              140  CALL_METHOD_2         2  ''
              142  BUILD_TUPLE_1         1 

 L. 845       144  BINARY_MODULO    

 L. 846       146  LOAD_FAST                'self'
              148  LOAD_ATTR                file

 L. 845       150  LOAD_CONST               ('file',)
              152  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              154  POP_TOP          

 L. 847       156  LOAD_FAST                'self'
              158  LOAD_ATTR                sourceFilename
              160  POP_JUMP_IF_FALSE   196  'to 196'

 L. 848       162  LOAD_GLOBAL              print
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

 L. 849       196  LOAD_GLOBAL              print
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

 L. 851       224  LOAD_GLOBAL              print
              226  LOAD_GLOBAL              build
              228  LOAD_METHOD              _makeDocString
              230  LOAD_FAST                'docDesc'
              232  CALL_METHOD_1         1  ''
              234  LOAD_FAST                'self'
              236  LOAD_ATTR                file
              238  LOAD_CONST               ('file',)
              240  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              242  POP_TOP          

 L. 853       244  LOAD_GLOBAL              print
              246  LOAD_STR                 'makepy_version ='
              248  LOAD_GLOBAL              repr
              250  LOAD_GLOBAL              makepy_version
              252  CALL_FUNCTION_1       1  ''
              254  LOAD_FAST                'self'
              256  LOAD_ATTR                file
              258  LOAD_CONST               ('file',)
              260  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              262  POP_TOP          

 L. 854       264  LOAD_GLOBAL              print
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

 L. 855       286  LOAD_GLOBAL              print
              288  LOAD_FAST                'self'
              290  LOAD_ATTR                file
              292  LOAD_CONST               ('file',)
              294  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              296  POP_TOP          

 L. 856       298  LOAD_GLOBAL              print
              300  LOAD_STR                 'import win32com.client.CLSIDToClass, pythoncom, pywintypes'
              302  LOAD_FAST                'self'
              304  LOAD_ATTR                file
              306  LOAD_CONST               ('file',)
              308  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              310  POP_TOP          

 L. 857       312  LOAD_GLOBAL              print
              314  LOAD_STR                 'import win32com.client.util'
              316  LOAD_FAST                'self'
              318  LOAD_ATTR                file
              320  LOAD_CONST               ('file',)
              322  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              324  POP_TOP          

 L. 858       326  LOAD_GLOBAL              print
              328  LOAD_STR                 'from pywintypes import IID'
              330  LOAD_FAST                'self'
              332  LOAD_ATTR                file
              334  LOAD_CONST               ('file',)
              336  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              338  POP_TOP          

 L. 859       340  LOAD_GLOBAL              print
              342  LOAD_STR                 'from win32com.client import Dispatch'
              344  LOAD_FAST                'self'
              346  LOAD_ATTR                file
              348  LOAD_CONST               ('file',)
              350  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              352  POP_TOP          

 L. 860       354  LOAD_GLOBAL              print
              356  LOAD_FAST                'self'
              358  LOAD_ATTR                file
              360  LOAD_CONST               ('file',)
              362  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              364  POP_TOP          

 L. 861       366  LOAD_GLOBAL              print
              368  LOAD_STR                 '# The following 3 lines may need tweaking for the particular server'
              370  LOAD_FAST                'self'
              372  LOAD_ATTR                file
              374  LOAD_CONST               ('file',)
              376  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              378  POP_TOP          

 L. 862       380  LOAD_GLOBAL              print
              382  LOAD_STR                 '# Candidates are pythoncom.Missing, .Empty and .ArgNotFound'
              384  LOAD_FAST                'self'
              386  LOAD_ATTR                file
              388  LOAD_CONST               ('file',)
              390  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              392  POP_TOP          

 L. 863       394  LOAD_GLOBAL              print
              396  LOAD_STR                 'defaultNamedOptArg=pythoncom.Empty'
              398  LOAD_FAST                'self'
              400  LOAD_ATTR                file
              402  LOAD_CONST               ('file',)
              404  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              406  POP_TOP          

 L. 864       408  LOAD_GLOBAL              print
              410  LOAD_STR                 'defaultNamedNotOptArg=pythoncom.Empty'
              412  LOAD_FAST                'self'
              414  LOAD_ATTR                file
              416  LOAD_CONST               ('file',)
              418  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              420  POP_TOP          

 L. 865       422  LOAD_GLOBAL              print
              424  LOAD_STR                 'defaultUnnamedArg=pythoncom.Empty'
              426  LOAD_FAST                'self'
              428  LOAD_ATTR                file
              430  LOAD_CONST               ('file',)
              432  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              434  POP_TOP          

 L. 866       436  LOAD_GLOBAL              print
              438  LOAD_FAST                'self'
              440  LOAD_ATTR                file
              442  LOAD_CONST               ('file',)
              444  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              446  POP_TOP          

 L. 867       448  LOAD_GLOBAL              print
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

 L. 868       474  LOAD_GLOBAL              print
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

 L. 869       500  LOAD_GLOBAL              print
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

 L. 870       526  LOAD_GLOBAL              print
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

 L. 871       552  LOAD_GLOBAL              print
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

 L. 872       578  LOAD_GLOBAL              print
              580  LOAD_FAST                'self'
              582  LOAD_ATTR                file
              584  LOAD_CONST               ('file',)
              586  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              588  POP_TOP          

Parse error at or near `<74>' instruction at offset 68

    def do_generate--- This code section failed: ---

 L. 875         0  LOAD_FAST                'self'
                2  LOAD_ATTR                typelib
                4  LOAD_METHOD              GetDocumentation
                6  LOAD_CONST               -1
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'moduleDoc'

 L. 876        12  LOAD_FAST                'self'
               14  LOAD_ATTR                file
               16  STORE_FAST               'stream'

 L. 877        18  LOAD_STR                 ''
               20  STORE_FAST               'docDesc'

 L. 878        22  LOAD_FAST                'moduleDoc'
               24  LOAD_CONST               1
               26  BINARY_SUBSCR    
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L. 879        30  LOAD_FAST                'moduleDoc'
               32  LOAD_CONST               1
               34  BINARY_SUBSCR    
               36  STORE_FAST               'docDesc'
             38_0  COME_FROM            28  '28'

 L. 880        38  LOAD_FAST                'self'
               40  LOAD_ATTR                progress
               42  LOAD_METHOD              Starting
               44  LOAD_FAST                'docDesc'
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          

 L. 881        50  LOAD_FAST                'self'
               52  LOAD_ATTR                progress
               54  LOAD_METHOD              SetDescription
               56  LOAD_STR                 'Building definitions from type library...'
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          

 L. 883        62  LOAD_FAST                'self'
               64  LOAD_METHOD              do_gen_file_header
               66  CALL_METHOD_0         0  ''
               68  POP_TOP          

 L. 885        70  LOAD_FAST                'self'
               72  LOAD_METHOD              BuildOleItemsFromType
               74  CALL_METHOD_0         0  ''
               76  UNPACK_SEQUENCE_4     4 
               78  STORE_FAST               'oleItems'
               80  STORE_FAST               'enumItems'
               82  STORE_FAST               'recordItems'
               84  STORE_FAST               'vtableItems'

 L. 887        86  LOAD_FAST                'self'
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

 L. 890       120  LOAD_FAST                'enumItems'
              122  POP_JUMP_IF_FALSE   220  'to 220'

 L. 891       124  LOAD_GLOBAL              print
              126  LOAD_STR                 'class constants:'
              128  LOAD_FAST                'stream'
              130  LOAD_CONST               ('file',)
              132  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              134  POP_TOP          

 L. 892       136  LOAD_GLOBAL              list
              138  LOAD_FAST                'enumItems'
              140  LOAD_METHOD              values
              142  CALL_METHOD_0         0  ''
              144  CALL_FUNCTION_1       1  ''
              146  STORE_FAST               'items'

 L. 893       148  LOAD_FAST                'items'
              150  LOAD_METHOD              sort
              152  CALL_METHOD_0         0  ''
              154  POP_TOP          

 L. 894       156  LOAD_CONST               0
              158  STORE_FAST               'num_written'

 L. 895       160  LOAD_FAST                'items'
              162  GET_ITER         
            164_0  COME_FROM           192  '192'
              164  FOR_ITER            194  'to 194'
              166  STORE_FAST               'oleitem'

 L. 896       168  LOAD_FAST                'num_written'
              170  LOAD_FAST                'oleitem'
              172  LOAD_METHOD              WriteEnumerationItems
              174  LOAD_FAST                'stream'
              176  CALL_METHOD_1         1  ''
              178  INPLACE_ADD      
              180  STORE_FAST               'num_written'

 L. 897       182  LOAD_FAST                'self'
              184  LOAD_ATTR                progress
              186  LOAD_METHOD              Tick
              188  CALL_METHOD_0         0  ''
              190  POP_TOP          
              192  JUMP_BACK           164  'to 164'
            194_0  COME_FROM           164  '164'

 L. 898       194  LOAD_FAST                'num_written'
              196  POP_JUMP_IF_TRUE    210  'to 210'

 L. 899       198  LOAD_GLOBAL              print
              200  LOAD_STR                 '\tpass'
              202  LOAD_FAST                'stream'
              204  LOAD_CONST               ('file',)
              206  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              208  POP_TOP          
            210_0  COME_FROM           196  '196'

 L. 900       210  LOAD_GLOBAL              print
              212  LOAD_FAST                'stream'
              214  LOAD_CONST               ('file',)
              216  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              218  POP_TOP          
            220_0  COME_FROM           122  '122'

 L. 902       220  LOAD_FAST                'self'
              222  LOAD_ATTR                generate_type
              224  LOAD_GLOBAL              GEN_FULL
              226  COMPARE_OP               ==
          228_230  POP_JUMP_IF_FALSE   344  'to 344'

 L. 903       232  LOAD_LISTCOMP            '<code_object <listcomp>>'
              234  LOAD_STR                 'Generator.do_generate.<locals>.<listcomp>'
              236  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              238  LOAD_FAST                'oleItems'
              240  LOAD_METHOD              values
              242  CALL_METHOD_0         0  ''
              244  GET_ITER         
              246  CALL_FUNCTION_1       1  ''
              248  STORE_FAST               'items'

 L. 904       250  LOAD_FAST                'items'
              252  LOAD_METHOD              sort
              254  CALL_METHOD_0         0  ''
              256  POP_TOP          

 L. 905       258  LOAD_FAST                'items'
              260  GET_ITER         
            262_0  COME_FROM           286  '286'
              262  FOR_ITER            290  'to 290'
              264  STORE_FAST               'oleitem'

 L. 906       266  LOAD_FAST                'self'
              268  LOAD_ATTR                progress
              270  LOAD_METHOD              Tick
              272  CALL_METHOD_0         0  ''
              274  POP_TOP          

 L. 907       276  LOAD_FAST                'oleitem'
              278  LOAD_METHOD              WriteClass
              280  LOAD_FAST                'self'
              282  CALL_METHOD_1         1  ''
              284  POP_TOP          
          286_288  JUMP_BACK           262  'to 262'
            290_0  COME_FROM           262  '262'

 L. 909       290  LOAD_GLOBAL              list
              292  LOAD_FAST                'vtableItems'
              294  LOAD_METHOD              values
              296  CALL_METHOD_0         0  ''
              298  CALL_FUNCTION_1       1  ''
              300  STORE_FAST               'items'

 L. 910       302  LOAD_FAST                'items'
              304  LOAD_METHOD              sort
              306  CALL_METHOD_0         0  ''
              308  POP_TOP          

 L. 911       310  LOAD_FAST                'items'
              312  GET_ITER         
            314_0  COME_FROM           338  '338'
              314  FOR_ITER            342  'to 342'
              316  STORE_FAST               'oleitem'

 L. 912       318  LOAD_FAST                'self'
              320  LOAD_ATTR                progress
              322  LOAD_METHOD              Tick
              324  CALL_METHOD_0         0  ''
              326  POP_TOP          

 L. 913       328  LOAD_FAST                'oleitem'
              330  LOAD_METHOD              WriteClass
              332  LOAD_FAST                'self'
              334  CALL_METHOD_1         1  ''
              336  POP_TOP          
          338_340  JUMP_BACK           314  'to 314'
            342_0  COME_FROM           314  '314'
              342  JUMP_FORWARD        368  'to 368'
            344_0  COME_FROM           228  '228'

 L. 915       344  LOAD_FAST                'self'
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

 L. 917       368  LOAD_GLOBAL              print
              370  LOAD_STR                 'RecordMap = {'
              372  LOAD_FAST                'stream'
              374  LOAD_CONST               ('file',)
              376  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              378  POP_TOP          

 L. 918       380  LOAD_FAST                'recordItems'
              382  LOAD_METHOD              values
              384  CALL_METHOD_0         0  ''
              386  GET_ITER         
            388_0  COME_FROM           488  '488'
            388_1  COME_FROM           446  '446'
              388  FOR_ITER            492  'to 492'
              390  STORE_FAST               'record'

 L. 919       392  LOAD_FAST                'record'
              394  LOAD_ATTR                clsid
              396  LOAD_GLOBAL              pythoncom
              398  LOAD_ATTR                IID_NULL
              400  COMPARE_OP               ==
          402_404  POP_JUMP_IF_FALSE   448  'to 448'

 L. 920       406  LOAD_GLOBAL              print
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

 L. 922       448  LOAD_GLOBAL              print
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
            492_0  COME_FROM           388  '388'

 L. 923       492  LOAD_GLOBAL              print
              494  LOAD_STR                 '}'
              496  LOAD_FAST                'stream'
              498  LOAD_CONST               ('file',)
              500  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              502  POP_TOP          

 L. 924       504  LOAD_GLOBAL              print
              506  LOAD_FAST                'stream'
              508  LOAD_CONST               ('file',)
              510  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              512  POP_TOP          

 L. 927       514  LOAD_FAST                'self'
              516  LOAD_ATTR                generate_type
              518  LOAD_GLOBAL              GEN_FULL
              520  COMPARE_OP               ==
          522_524  POP_JUMP_IF_FALSE   724  'to 724'

 L. 928       526  LOAD_GLOBAL              print
              528  LOAD_STR                 'CLSIDToClassMap = {'
              530  LOAD_FAST                'stream'
              532  LOAD_CONST               ('file',)
              534  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              536  POP_TOP          

 L. 929       538  LOAD_FAST                'oleItems'
              540  LOAD_METHOD              values
              542  CALL_METHOD_0         0  ''
              544  GET_ITER         
            546_0  COME_FROM           596  '596'
            546_1  COME_FROM           564  '564'
            546_2  COME_FROM           556  '556'
              546  FOR_ITER            600  'to 600'
              548  STORE_FAST               'item'

 L. 930       550  LOAD_FAST                'item'
              552  LOAD_CONST               None
              554  <117>                 1  ''
          556_558  POP_JUMP_IF_FALSE_BACK   546  'to 546'
              560  LOAD_FAST                'item'
              562  LOAD_ATTR                bWritten
          564_566  POP_JUMP_IF_FALSE_BACK   546  'to 546'

 L. 931       568  LOAD_GLOBAL              print
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
            600_0  COME_FROM           546  '546'

 L. 932       600  LOAD_GLOBAL              print
              602  LOAD_STR                 '}'
              604  LOAD_FAST                'stream'
              606  LOAD_CONST               ('file',)
              608  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              610  POP_TOP          

 L. 933       612  LOAD_GLOBAL              print
              614  LOAD_STR                 'CLSIDToPackageMap = {}'
              616  LOAD_FAST                'stream'
              618  LOAD_CONST               ('file',)
              620  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              622  POP_TOP          

 L. 934       624  LOAD_GLOBAL              print
              626  LOAD_STR                 'win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )'
              628  LOAD_FAST                'stream'
              630  LOAD_CONST               ('file',)
              632  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              634  POP_TOP          

 L. 935       636  LOAD_GLOBAL              print
              638  LOAD_STR                 'VTablesToPackageMap = {}'
              640  LOAD_FAST                'stream'
              642  LOAD_CONST               ('file',)
              644  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              646  POP_TOP          

 L. 936       648  LOAD_GLOBAL              print
              650  LOAD_STR                 'VTablesToClassMap = {'
              652  LOAD_FAST                'stream'
              654  LOAD_CONST               ('file',)
              656  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              658  POP_TOP          

 L. 937       660  LOAD_FAST                'vtableItems'
              662  LOAD_METHOD              values
              664  CALL_METHOD_0         0  ''
              666  GET_ITER         
            668_0  COME_FROM           696  '696'
              668  FOR_ITER            700  'to 700'
              670  STORE_FAST               'item'

 L. 938       672  LOAD_GLOBAL              print
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
            700_0  COME_FROM           668  '668'

 L. 939       700  LOAD_GLOBAL              print
              702  LOAD_STR                 '}'
              704  LOAD_FAST                'stream'
              706  LOAD_CONST               ('file',)
              708  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              710  POP_TOP          

 L. 940       712  LOAD_GLOBAL              print
              714  LOAD_FAST                'stream'
              716  LOAD_CONST               ('file',)
              718  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              720  POP_TOP          
              722  JUMP_FORWARD        904  'to 904'
            724_0  COME_FROM           522  '522'

 L. 943       724  LOAD_GLOBAL              print
              726  LOAD_STR                 'CLSIDToClassMap = {}'
              728  LOAD_FAST                'stream'
              730  LOAD_CONST               ('file',)
              732  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              734  POP_TOP          

 L. 944       736  LOAD_GLOBAL              print
              738  LOAD_STR                 'CLSIDToPackageMap = {'
              740  LOAD_FAST                'stream'
              742  LOAD_CONST               ('file',)
              744  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              746  POP_TOP          

 L. 945       748  LOAD_FAST                'oleItems'
              750  LOAD_METHOD              values
              752  CALL_METHOD_0         0  ''
              754  GET_ITER         
            756_0  COME_FROM           802  '802'
            756_1  COME_FROM           766  '766'
              756  FOR_ITER            806  'to 806'
              758  STORE_FAST               'item'

 L. 946       760  LOAD_FAST                'item'
              762  LOAD_CONST               None
              764  <117>                 1  ''
          766_768  POP_JUMP_IF_FALSE_BACK   756  'to 756'

 L. 947       770  LOAD_GLOBAL              print
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
            806_0  COME_FROM           756  '756'

 L. 948       806  LOAD_GLOBAL              print
              808  LOAD_STR                 '}'
              810  LOAD_FAST                'stream'
              812  LOAD_CONST               ('file',)
              814  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              816  POP_TOP          

 L. 949       818  LOAD_GLOBAL              print
              820  LOAD_STR                 'VTablesToClassMap = {}'
              822  LOAD_FAST                'stream'
              824  LOAD_CONST               ('file',)
              826  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              828  POP_TOP          

 L. 950       830  LOAD_GLOBAL              print
              832  LOAD_STR                 'VTablesToPackageMap = {'
              834  LOAD_FAST                'stream'
              836  LOAD_CONST               ('file',)
              838  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              840  POP_TOP          

 L. 951       842  LOAD_FAST                'vtableItems'
              844  LOAD_METHOD              values
              846  CALL_METHOD_0         0  ''
              848  GET_ITER         
            850_0  COME_FROM           878  '878'
              850  FOR_ITER            882  'to 882'
              852  STORE_FAST               'item'

 L. 952       854  LOAD_GLOBAL              print
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
            882_0  COME_FROM           850  '850'

 L. 953       882  LOAD_GLOBAL              print
              884  LOAD_STR                 '}'
              886  LOAD_FAST                'stream'
              888  LOAD_CONST               ('file',)
              890  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              892  POP_TOP          

 L. 954       894  LOAD_GLOBAL              print
              896  LOAD_FAST                'stream'
              898  LOAD_CONST               ('file',)
              900  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              902  POP_TOP          
            904_0  COME_FROM           722  '722'

 L. 956       904  LOAD_GLOBAL              print
              906  LOAD_FAST                'stream'
              908  LOAD_CONST               ('file',)
              910  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              912  POP_TOP          

 L. 958       914  BUILD_MAP_0           0 
              916  STORE_FAST               'map'

 L. 959       918  LOAD_FAST                'oleItems'
              920  LOAD_METHOD              values
              922  CALL_METHOD_0         0  ''
              924  GET_ITER         
            926_0  COME_FROM           964  '964'
            926_1  COME_FROM           948  '948'
            926_2  COME_FROM           936  '936'
              926  FOR_ITER            968  'to 968'
              928  STORE_FAST               'item'

 L. 960       930  LOAD_FAST                'item'
              932  LOAD_CONST               None
              934  <117>                 1  ''
          936_938  POP_JUMP_IF_FALSE_BACK   926  'to 926'
              940  LOAD_GLOBAL              isinstance
              942  LOAD_FAST                'item'
              944  LOAD_GLOBAL              CoClassItem
              946  CALL_FUNCTION_2       2  ''
          948_950  POP_JUMP_IF_TRUE_BACK   926  'to 926'

 L. 961       952  LOAD_FAST                'item'
              954  LOAD_ATTR                clsid
              956  LOAD_FAST                'map'
              958  LOAD_FAST                'item'
              960  LOAD_ATTR                python_name
              962  STORE_SUBSCR     
          964_966  JUMP_BACK           926  'to 926'
            968_0  COME_FROM           926  '926'

 L. 962       968  LOAD_FAST                'vtableItems'
              970  LOAD_METHOD              values
              972  CALL_METHOD_0         0  ''
              974  GET_ITER         
            976_0  COME_FROM           992  '992'
              976  FOR_ITER            996  'to 996'
              978  STORE_FAST               'item'

 L. 963       980  LOAD_FAST                'item'
              982  LOAD_ATTR                clsid
              984  LOAD_FAST                'map'
              986  LOAD_FAST                'item'
              988  LOAD_ATTR                python_name
              990  STORE_SUBSCR     
          992_994  JUMP_BACK           976  'to 976'
            996_0  COME_FROM           976  '976'

 L. 965       996  LOAD_GLOBAL              print
              998  LOAD_STR                 'NamesToIIDMap = {'
             1000  LOAD_FAST                'stream'
             1002  LOAD_CONST               ('file',)
             1004  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1006  POP_TOP          

 L. 966      1008  LOAD_FAST                'map'
             1010  LOAD_METHOD              items
             1012  CALL_METHOD_0         0  ''
             1014  GET_ITER         
           1016_0  COME_FROM          1044  '1044'
             1016  FOR_ITER           1048  'to 1048'
             1018  UNPACK_SEQUENCE_2     2 
             1020  STORE_FAST               'name'
             1022  STORE_FAST               'iid'

 L. 967      1024  LOAD_GLOBAL              print
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
           1048_0  COME_FROM          1016  '1016'

 L. 968      1048  LOAD_GLOBAL              print
             1050  LOAD_STR                 '}'
             1052  LOAD_FAST                'stream'
             1054  LOAD_CONST               ('file',)
             1056  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1058  POP_TOP          

 L. 969      1060  LOAD_GLOBAL              print
             1062  LOAD_FAST                'stream'
             1064  LOAD_CONST               ('file',)
             1066  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1068  POP_TOP          

 L. 971      1070  LOAD_FAST                'enumItems'
         1072_1074  POP_JUMP_IF_FALSE  1088  'to 1088'

 L. 972      1076  LOAD_GLOBAL              print
             1078  LOAD_STR                 'win32com.client.constants.__dicts__.append(constants.__dict__)'
             1080  LOAD_FAST                'stream'
             1082  LOAD_CONST               ('file',)
             1084  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1086  POP_TOP          
           1088_0  COME_FROM          1072  '1072'

 L. 973      1088  LOAD_GLOBAL              print
             1090  LOAD_FAST                'stream'
             1092  LOAD_CONST               ('file',)
             1094  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1096  POP_TOP          

Parse error at or near `<117>' instruction at offset 554

    def generate_child--- This code section failed: ---

 L. 977         0  LOAD_GLOBAL              GEN_DEMAND_CHILD
                2  LOAD_FAST                'self'
                4  STORE_ATTR               generate_type

 L. 979         6  LOAD_FAST                'self'
                8  LOAD_ATTR                typelib
               10  LOAD_METHOD              GetLibAttr
               12  CALL_METHOD_0         0  ''
               14  STORE_FAST               'la'

 L. 980        16  LOAD_FAST                'la'
               18  LOAD_CONST               1
               20  BINARY_SUBSCR    
               22  STORE_FAST               'lcid'

 L. 981        24  LOAD_FAST                'la'
               26  LOAD_CONST               0
               28  BINARY_SUBSCR    
               30  STORE_FAST               'clsid'

 L. 982        32  LOAD_FAST                'la'
               34  LOAD_CONST               3
               36  BINARY_SUBSCR    
               38  STORE_FAST               'major'

 L. 983        40  LOAD_FAST                'la'
               42  LOAD_CONST               4
               44  BINARY_SUBSCR    
               46  STORE_FAST               'minor'

 L. 984        48  LOAD_STR                 'win32com.gen_py.'
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

 L. 985     84_86  SETUP_FINALLY       720  'to 720'

 L. 990        88  BUILD_MAP_0           0 
               90  STORE_FAST               'oleItems'

 L. 991        92  BUILD_MAP_0           0 
               94  STORE_FAST               'vtableItems'

 L. 992        96  LOAD_FAST                'self'
               98  LOAD_METHOD              CollectOleItemInfosFromType
              100  CALL_METHOD_0         0  ''
              102  STORE_FAST               'infos'

 L. 993       104  LOAD_CONST               0
              106  STORE_FAST               'found'

 L. 994       108  LOAD_FAST                'infos'
              110  GET_ITER         
            112_0  COME_FROM           258  '258'
            112_1  COME_FROM           224  '224'
            112_2  COME_FROM           136  '136'
              112  FOR_ITER            260  'to 260'
              114  STORE_FAST               'type_info_tuple'

 L. 995       116  LOAD_FAST                'type_info_tuple'
              118  UNPACK_SEQUENCE_4     4 
              120  STORE_FAST               'info'
              122  STORE_FAST               'infotype'
              124  STORE_FAST               'doc'
              126  STORE_FAST               'attr'

 L. 996       128  LOAD_FAST                'infotype'
              130  LOAD_GLOBAL              pythoncom
              132  LOAD_ATTR                TKIND_COCLASS
              134  COMPARE_OP               ==
              136  POP_JUMP_IF_FALSE_BACK   112  'to 112'

 L. 997       138  LOAD_FAST                'self'
              140  LOAD_METHOD              _Build_CoClass
              142  LOAD_FAST                'type_info_tuple'
              144  CALL_METHOD_1         1  ''
              146  UNPACK_SEQUENCE_2     2 
              148  STORE_FAST               'coClassItem'
              150  STORE_FAST               'child_infos'

 L. 998       152  LOAD_GLOBAL              build
              154  LOAD_METHOD              MakePublicAttributeName
              156  LOAD_FAST                'doc'
              158  LOAD_CONST               0
              160  BINARY_SUBSCR    
              162  CALL_METHOD_1         1  ''
              164  LOAD_FAST                'child'
              166  COMPARE_OP               ==
              168  STORE_FAST               'found'

 L. 999       170  LOAD_FAST                'found'
              172  POP_JUMP_IF_TRUE    222  'to 222'

 L.1001       174  LOAD_FAST                'child_infos'
              176  GET_ITER         
            178_0  COME_FROM           220  '220'
            178_1  COME_FROM           210  '210'
              178  FOR_ITER            222  'to 222'
              180  UNPACK_SEQUENCE_6     6 
              182  STORE_FAST               'info'
              184  STORE_FAST               'info_type'
              186  STORE_FAST               'refType'
              188  STORE_FAST               'doc'
              190  STORE_FAST               'refAttr'
              192  STORE_FAST               'flags'

 L.1002       194  LOAD_GLOBAL              build
              196  LOAD_METHOD              MakePublicAttributeName
              198  LOAD_FAST                'doc'
              200  LOAD_CONST               0
              202  BINARY_SUBSCR    
              204  CALL_METHOD_1         1  ''
              206  LOAD_FAST                'child'
              208  COMPARE_OP               ==
              210  POP_JUMP_IF_FALSE_BACK   178  'to 178'

 L.1003       212  LOAD_CONST               1
              214  STORE_FAST               'found'

 L.1004       216  POP_TOP          
              218  BREAK_LOOP          222  'to 222'
              220  JUMP_BACK           178  'to 178'
            222_0  COME_FROM           218  '218'
            222_1  COME_FROM           178  '178'
            222_2  COME_FROM           172  '172'

 L.1005       222  LOAD_FAST                'found'
              224  POP_JUMP_IF_FALSE_BACK   112  'to 112'

 L.1006       226  LOAD_FAST                'coClassItem'
              228  LOAD_FAST                'oleItems'
              230  LOAD_FAST                'coClassItem'
              232  LOAD_ATTR                clsid
              234  STORE_SUBSCR     

 L.1007       236  LOAD_FAST                'self'
              238  LOAD_METHOD              _Build_CoClassChildren
              240  LOAD_FAST                'coClassItem'
              242  LOAD_FAST                'child_infos'
              244  LOAD_FAST                'oleItems'
              246  LOAD_FAST                'vtableItems'
              248  CALL_METHOD_4         4  ''
              250  POP_TOP          

 L.1008       252  POP_TOP          
          254_256  BREAK_LOOP          260  'to 260'
              258  JUMP_BACK           112  'to 112'
            260_0  COME_FROM           254  '254'
            260_1  COME_FROM           112  '112'

 L.1009       260  LOAD_FAST                'found'
          262_264  POP_JUMP_IF_TRUE    372  'to 372'

 L.1011       266  LOAD_FAST                'infos'
              268  GET_ITER         
            270_0  COME_FROM           368  '368'
            270_1  COME_FROM           356  '356'
            270_2  COME_FROM           320  '320'
            270_3  COME_FROM           300  '300'
              270  FOR_ITER            372  'to 372'
              272  STORE_FAST               'type_info_tuple'

 L.1012       274  LOAD_FAST                'type_info_tuple'
              276  UNPACK_SEQUENCE_4     4 
              278  STORE_FAST               'info'
              280  STORE_FAST               'infotype'
              282  STORE_FAST               'doc'
              284  STORE_FAST               'attr'

 L.1013       286  LOAD_FAST                'infotype'
              288  LOAD_GLOBAL              pythoncom
              290  LOAD_ATTR                TKIND_INTERFACE
              292  LOAD_GLOBAL              pythoncom
              294  LOAD_ATTR                TKIND_DISPATCH
              296  BUILD_TUPLE_2         2 
              298  <118>                 0  ''
          300_302  POP_JUMP_IF_FALSE_BACK   270  'to 270'

 L.1014       304  LOAD_GLOBAL              build
              306  LOAD_METHOD              MakePublicAttributeName
              308  LOAD_FAST                'doc'
              310  LOAD_CONST               0
              312  BINARY_SUBSCR    
              314  CALL_METHOD_1         1  ''
              316  LOAD_FAST                'child'
              318  COMPARE_OP               ==
          320_322  POP_JUMP_IF_FALSE_BACK   270  'to 270'

 L.1015       324  LOAD_CONST               1
              326  STORE_FAST               'found'

 L.1016       328  LOAD_FAST                'self'
              330  LOAD_METHOD              _Build_Interface
              332  LOAD_FAST                'type_info_tuple'
              334  CALL_METHOD_1         1  ''
              336  UNPACK_SEQUENCE_2     2 
              338  STORE_FAST               'oleItem'
              340  STORE_FAST               'vtableItem'

 L.1017       342  LOAD_FAST                'oleItem'
              344  LOAD_FAST                'oleItems'
              346  LOAD_FAST                'clsid'
              348  STORE_SUBSCR     

 L.1018       350  LOAD_FAST                'vtableItem'
              352  LOAD_CONST               None
              354  <117>                 1  ''
          356_358  POP_JUMP_IF_FALSE_BACK   270  'to 270'

 L.1019       360  LOAD_FAST                'vtableItem'
              362  LOAD_FAST                'vtableItems'
              364  LOAD_FAST                'clsid'
              366  STORE_SUBSCR     
          368_370  JUMP_BACK           270  'to 270'
            372_0  COME_FROM           270  '270'
            372_1  COME_FROM           262  '262'

 L.1021       372  LOAD_FAST                'found'
          374_376  POP_JUMP_IF_TRUE    392  'to 392'
              378  <74>             
              380  LOAD_STR                 "Cant find the '%s' interface in the CoClasses, or the interfaces"
              382  LOAD_FAST                'child'
              384  BUILD_TUPLE_1         1 
              386  BINARY_MODULO    
              388  CALL_FUNCTION_1       1  ''
              390  RAISE_VARARGS_1       1  'exception instance'
            392_0  COME_FROM           374  '374'

 L.1023       392  BUILD_MAP_0           0 
              394  STORE_FAST               'items'

 L.1024       396  LOAD_FAST                'oleItems'
              398  LOAD_METHOD              items
              400  CALL_METHOD_0         0  ''
              402  GET_ITER         
            404_0  COME_FROM           424  '424'
              404  FOR_ITER            428  'to 428'
              406  UNPACK_SEQUENCE_2     2 
              408  STORE_FAST               'key'
              410  STORE_FAST               'value'

 L.1025       412  LOAD_FAST                'value'
              414  LOAD_CONST               None
              416  BUILD_TUPLE_2         2 
              418  LOAD_FAST                'items'
              420  LOAD_FAST                'key'
              422  STORE_SUBSCR     
          424_426  JUMP_BACK           404  'to 404'
            428_0  COME_FROM           404  '404'

 L.1026       428  LOAD_FAST                'vtableItems'
              430  LOAD_METHOD              items
              432  CALL_METHOD_0         0  ''
              434  GET_ITER         
            436_0  COME_FROM           496  '496'
              436  FOR_ITER            500  'to 500'
              438  UNPACK_SEQUENCE_2     2 
              440  STORE_FAST               'key'
              442  STORE_FAST               'value'

 L.1027       444  LOAD_FAST                'items'
              446  LOAD_METHOD              get
              448  LOAD_FAST                'key'
              450  LOAD_CONST               None
              452  CALL_METHOD_2         2  ''
              454  STORE_FAST               'existing'

 L.1028       456  LOAD_FAST                'existing'
              458  LOAD_CONST               None
              460  <117>                 1  ''
          462_464  POP_JUMP_IF_FALSE   480  'to 480'

 L.1029       466  LOAD_FAST                'existing'
              468  LOAD_CONST               0
              470  BINARY_SUBSCR    
              472  LOAD_FAST                'value'
              474  BUILD_TUPLE_2         2 
              476  STORE_FAST               'new_val'
              478  JUMP_FORWARD        488  'to 488'
            480_0  COME_FROM           462  '462'

 L.1031       480  LOAD_CONST               None
              482  LOAD_FAST                'value'
              484  BUILD_TUPLE_2         2 
              486  STORE_FAST               'new_val'
            488_0  COME_FROM           478  '478'

 L.1032       488  LOAD_FAST                'new_val'
              490  LOAD_FAST                'items'
              492  LOAD_FAST                'key'
              494  STORE_SUBSCR     
          496_498  JUMP_BACK           436  'to 436'
            500_0  COME_FROM           436  '436'

 L.1034       500  LOAD_FAST                'self'
              502  LOAD_ATTR                progress
              504  LOAD_METHOD              SetDescription
              506  LOAD_STR                 'Generating...'
              508  LOAD_GLOBAL              len
              510  LOAD_FAST                'items'
              512  CALL_FUNCTION_1       1  ''
              514  CALL_METHOD_2         2  ''
              516  POP_TOP          

 L.1035       518  LOAD_FAST                'items'
              520  LOAD_METHOD              values
              522  CALL_METHOD_0         0  ''
              524  GET_ITER         
            526_0  COME_FROM           702  '702'
            526_1  COME_FROM           676  '676'
              526  FOR_ITER            706  'to 706'
              528  UNPACK_SEQUENCE_2     2 
              530  STORE_FAST               'oleitem'
              532  STORE_FAST               'vtableitem'

 L.1036       534  LOAD_FAST                'oleitem'
          536_538  JUMP_IF_TRUE_OR_POP   542  'to 542'
              540  LOAD_FAST                'vtableitem'
            542_0  COME_FROM           536  '536'
              542  STORE_FAST               'an_item'

 L.1037       544  LOAD_FAST                'self'
              546  LOAD_ATTR                file
          548_550  POP_JUMP_IF_FALSE   560  'to 560'
              552  <74>             
              554  LOAD_STR                 'already have a file?'
              556  CALL_FUNCTION_1       1  ''
              558  RAISE_VARARGS_1       1  'exception instance'
            560_0  COME_FROM           548  '548'

 L.1040       560  LOAD_GLOBAL              os
              562  LOAD_ATTR                path
              564  LOAD_METHOD              join
              566  LOAD_FAST                'dir'
              568  LOAD_FAST                'an_item'
              570  LOAD_ATTR                python_name
              572  CALL_METHOD_2         2  ''
              574  LOAD_STR                 '.py'
              576  BINARY_ADD       
              578  STORE_FAST               'out_name'

 L.1041       580  LOAD_CONST               False
              582  STORE_FAST               'worked'

 L.1042       584  LOAD_FAST                'self'
              586  LOAD_METHOD              open_writer
              588  LOAD_FAST                'out_name'
              590  CALL_METHOD_1         1  ''
              592  LOAD_FAST                'self'
              594  STORE_ATTR               file

 L.1043       596  SETUP_FINALLY       678  'to 678'

 L.1044       598  LOAD_FAST                'oleitem'
              600  LOAD_CONST               None
              602  <117>                 1  ''
          604_606  POP_JUMP_IF_FALSE   618  'to 618'

 L.1045       608  LOAD_FAST                'self'
              610  LOAD_METHOD              do_gen_child_item
              612  LOAD_FAST                'oleitem'
              614  CALL_METHOD_1         1  ''
              616  POP_TOP          
            618_0  COME_FROM           604  '604'

 L.1046       618  LOAD_FAST                'vtableitem'
              620  LOAD_CONST               None
              622  <117>                 1  ''
          624_626  POP_JUMP_IF_FALSE   638  'to 638'

 L.1047       628  LOAD_FAST                'self'
              630  LOAD_METHOD              do_gen_child_item
              632  LOAD_FAST                'vtableitem'
              634  CALL_METHOD_1         1  ''
              636  POP_TOP          
            638_0  COME_FROM           624  '624'

 L.1048       638  LOAD_FAST                'self'
              640  LOAD_ATTR                progress
              642  LOAD_METHOD              Tick
              644  CALL_METHOD_0         0  ''
              646  POP_TOP          

 L.1049       648  LOAD_CONST               True
              650  STORE_FAST               'worked'
              652  POP_BLOCK        

 L.1051       654  LOAD_FAST                'self'
              656  LOAD_METHOD              finish_writer
              658  LOAD_FAST                'out_name'
              660  LOAD_FAST                'self'
              662  LOAD_ATTR                file
              664  LOAD_FAST                'worked'
              666  CALL_METHOD_3         3  ''
              668  POP_TOP          

 L.1052       670  LOAD_CONST               None
              672  LOAD_FAST                'self'
              674  STORE_ATTR               file
              676  JUMP_BACK           526  'to 526'
            678_0  COME_FROM_FINALLY   596  '596'

 L.1051       678  LOAD_FAST                'self'
              680  LOAD_METHOD              finish_writer
              682  LOAD_FAST                'out_name'
              684  LOAD_FAST                'self'
              686  LOAD_ATTR                file
              688  LOAD_FAST                'worked'
              690  CALL_METHOD_3         3  ''
              692  POP_TOP          

 L.1052       694  LOAD_CONST               None
              696  LOAD_FAST                'self'
              698  STORE_ATTR               file
              700  <48>             
          702_704  JUMP_BACK           526  'to 526'
            706_0  COME_FROM           526  '526'
              706  POP_BLOCK        

 L.1054       708  LOAD_FAST                'self'
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