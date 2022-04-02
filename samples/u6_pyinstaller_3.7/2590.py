# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: comtypes\tools\codegenerator.py
import os, io, keyword
from comtypes.tools import typedesc
import comtypes.client, comtypes.client._generate
version = '$Rev$'[6:-2]
__warn_on_munge__ = True

class lcid(object):

    def __repr__(self):
        return '_lcid'


lcid = lcid()

class dispid(object):

    def __init__(self, memid):
        self.memid = memid

    def __repr__(self):
        return 'dispid(%s)' % self.memid


class helpstring(object):

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return 'helpstring(%r)' % self.text


ctypes_names = {'unsigned char':'c_ubyte', 
 'signed char':'c_byte', 
 'char':'c_char', 
 'wchar_t':'c_wchar', 
 'short unsigned int':'c_ushort', 
 'short int':'c_short', 
 'long unsigned int':'c_ulong', 
 'long int':'c_long', 
 'long signed int':'c_long', 
 'unsigned int':'c_uint', 
 'int':'c_int', 
 'long long unsigned int':'c_ulonglong', 
 'long long int':'c_longlong', 
 'double':'c_double', 
 'float':'c_float', 
 'void':'None'}

def get_real_type(tp):
    if type(tp) is typedesc.Typedef:
        return get_real_type(tp.typ)
    if isinstance(tp, typedesc.CvQualifiedType):
        return get_real_type(tp.typ)
    return tp


ASSUME_STRINGS = True

def _calc_packing(struct, fields, pack, isStruct):
    if struct.size is None:
        return -1
        if struct.name in dont_assert_size:
            return
        if struct.bases:
            size = struct.bases[0].size
            total_align = struct.bases[0].align
    else:
        size = 0
        total_align = 8
    for i, f in enumerate(fields):
        if f.bits:
            return -2
        else:
            s, a = storage(f.typ)
            if pack is not None:
                a = min(pack, a)
            if size % a:
                size += a - size % a
            if isStruct:
                if size != f.offset:
                    raise PackingError('field %s offset (%s/%s)' % (f.name, size, f.offset))
                size += s
            else:
                size = max(size, s)
        total_align = max(total_align, a)

    if total_align != struct.align:
        raise PackingError('total alignment (%s/%s)' % (total_align, struct.align))
    a = total_align
    if pack is not None:
        a = min(pack, a)
    if size % a:
        size += a - size % a
    if size != struct.size:
        raise PackingError('total size (%s/%s)' % (size, struct.size))


def calc_packing(struct, fields):
    isStruct = isinstance(struct, typedesc.Structure)
    for pack in (None, 128, 64, 32, 16, 8):
        try:
            _calc_packing(struct, fields, pack, isStruct)
        except PackingError as details:
            try:
                continue
            finally:
                details = None
                del details

        else:
            if pack is None:
                return
            return pack / 8

    raise PackingError('PACKING FAILED: %s' % details)


class PackingError(Exception):
    pass


try:
    set
except NameError:
    from sets import Set as set

dont_assert_size = set([
 '__si_class_type_info_pseudo',
 '__class_type_info_pseudo'])

def storage(t):
    if isinstance(t, typedesc.Typedef):
        return storage(t.typ)
    if isinstance(t, typedesc.ArrayType):
        s, a = storage(t.typ)
        return (s * (int(t.max) - int(t.min) + 1), a)
    return (
     int(t.size), int(t.align))


class Generator(object):

    def __init__(self, ofi, known_symbols=None):
        self._externals = {}
        self.output = ofi
        self.stream = io.StringIO()
        self.imports = io.StringIO()
        self.known_symbols = known_symbols or {}
        self.done = set()
        self.names = set()

    def generate(self, item):
        if item in self.done:
            return
        elif isinstance(item, typedesc.StructureHead):
            name = getattr(item.struct, 'name', None)
        else:
            name = getattr(item, 'name', None)
        if name in self.known_symbols:
            mod = self.known_symbols[name]
            print(('from %s import %s' % (mod, name)), file=(self.imports))
            self.done.add(item)
            if isinstance(item, typedesc.Structure):
                self.done.add(item.get_head())
                self.done.add(item.get_body())
            return
        mth = getattr(self, type(item).__name__)
        self.done.add(item)
        mth(item)

    def generate_all(self, items):
        for item in items:
            self.generate(item)

    def _make_relative_path(self, path1, path2):
        """path1 and path2 are pathnames.
        Return path1 as a relative path to path2, if possible.
        """
        path1 = os.path.abspath(path1)
        path2 = os.path.abspath(path2)
        common = os.path.commonprefix([os.path.normcase(path1),
         os.path.normcase(path2)])
        if not os.path.isdir(common):
            return path1
        else:
            return common.endswith('\\') or path1
        if not os.path.isdir(path2):
            path2 = os.path.dirname(path2)
        path1 = path1[len(common):]
        path2 = path2[len(common):]
        parts2 = path2.split('\\')
        return '..\\' * len(parts2) + path1

    def generate_code(self, items, filename=None):
        self.filename = filename
        if filename is not None:
            print('# -*- coding: mbcs -*-', file=(self.output))
            if os.path.isabs(filename):
                print(('typelib_path = %r' % filename), file=(self.output))
            else:
                if not os.path.dirname(filename):
                    os.path.isfile(filename) or print(('typelib_path = %r' % filename), file=(self.output))
                else:
                    path = self._make_relative_path(filename, comtypes.gen.__path__[0])
                    print('import os', file=(self.output))
                    print('typelib_path = os.path.normpath(', file=(self.output))
                    print('    os.path.abspath(os.path.join(os.path.dirname(__file__),', file=(self.output))
                    print(('                                 %r)))' % path), file=(self.output))
                    p = os.path.normpath(os.path.abspath(os.path.join(comtypes.gen.__path__[0], path)))
                    assert os.path.isfile(p)
        print('_lcid = 0 # change this if required', file=(self.imports))
        print('from ctypes import *', file=(self.imports))
        items = set(items)
        loops = 0
        while items:
            loops += 1
            self.more = set()
            self.generate_all(items)
            items |= self.more
            items -= self.done

        self.output.write(self.imports.getvalue())
        self.output.write('\n\n')
        self.output.write(self.stream.getvalue())
        import textwrap
        wrapper = textwrap.TextWrapper(subsequent_indent='           ', break_long_words=False)
        text = '__all__ = [ %s]' % ', '.join([repr(str(n)) for n in self.names])
        for line in wrapper.wrap(text):
            print(line, file=(self.output))

        print(('from comtypes import _check_version; _check_version(%r)' % version), file=(self.output))
        return loops

    def type_name(self, t, generate=True):
        if isinstance(t, typedesc.SAFEARRAYType):
            return '_midlSAFEARRAY(%s)' % self.type_name(t.typ)
        if isinstance(t, typedesc.Typedef):
            return t.name
        if isinstance(t, typedesc.PointerType):
            if ASSUME_STRINGS:
                x = get_real_type(t.typ)
                if isinstance(x, typedesc.FundamentalType):
                    if x.name == 'char':
                        self.need_STRING()
                        return 'STRING'
                    if x.name == 'wchar_t':
                        self.need_WSTRING()
                        return 'WSTRING'
            result = 'POINTER(%s)' % self.type_name(t.typ, generate)
            if result.startswith('POINTER(WINFUNCTYPE'):
                return result[len('POINTER('):-1]
            if result.startswith('POINTER(CFUNCTYPE'):
                return result[len('POINTER('):-1]
            if result == 'POINTER(None)':
                return 'c_void_p'
            return result
        if isinstance(t, typedesc.ArrayType):
            return '%s * %s' % (self.type_name(t.typ, generate), int(t.max) + 1)
        if isinstance(t, typedesc.FunctionType):
            args = [self.type_name(x, generate) for x in [t.returns] + list(t.iterArgTypes())]
            if '__stdcall__' in t.attributes:
                return 'WINFUNCTYPE(%s)' % ', '.join(args)
            return 'CFUNCTYPE(%s)' % ', '.join(args)
        else:
            if isinstance(t, typedesc.CvQualifiedType):
                return '%s' % self.type_name(t.typ, generate)
            if isinstance(t, typedesc.FundamentalType):
                return ctypes_names[t.name]
            if isinstance(t, typedesc.Structure):
                return t.name
            if isinstance(t, typedesc.Enumeration):
                if t.name:
                    return t.name
                return 'c_int'
            return t.name

    def need_VARIANT_imports(self, value):
        text = repr(value)
        if 'Decimal(' in text:
            print('from decimal import Decimal', file=(self.imports))
        if 'datetime.datetime(' in text:
            print('import datetime', file=(self.imports))

    _STRING_defined = False

    def need_STRING(self):
        if self._STRING_defined:
            return
        print('STRING = c_char_p', file=(self.imports))
        self._STRING_defined = True

    _WSTRING_defined = False

    def need_WSTRING(self):
        if self._WSTRING_defined:
            return
        print('WSTRING = c_wchar_p', file=(self.imports))
        self._WSTRING_defined = True

    _OPENARRAYS_defined = False

    def need_OPENARRAYS(self):
        if self._OPENARRAYS_defined:
            return
        print('OPENARRAY = POINTER(c_ubyte) # hack, see comtypes/tools/codegenerator.py', file=(self.imports))
        self._OPENARRAYS_defined = True

    _arraytypes = 0

    def ArrayType(self, tp):
        self._arraytypes += 1
        self.generate(get_real_type(tp.typ))
        self.generate(tp.typ)

    _enumvalues = 0

    def EnumValue(self, tp):
        value = int(tp.value)
        if keyword.iskeyword(tp.name):
            if __warn_on_munge__:
                print('# Fixing keyword as EnumValue for %s' % tp.name)
            tp.name += '_'
        print(('%s = %d' % (tp.name, value)), file=(self.stream))
        self.names.add(tp.name)
        self._enumvalues += 1

    _enumtypes = 0

    def Enumeration(self, tp):
        self._enumtypes += 1
        print(file=(self.stream))
        if tp.name:
            print(("# values for enumeration '%s'" % tp.name), file=(self.stream))
        else:
            print('# values for unnamed enumeration', file=(self.stream))
        for item in tp.values:
            self.generate(item)

        if tp.name:
            print(('%s = c_int # enum' % tp.name), file=(self.stream))
            self.names.add(tp.name)

    _GUID_defined = False

    def need_GUID(self):
        if self._GUID_defined:
            return
        self._GUID_defined = True
        modname = self.known_symbols.get('GUID')
        if modname:
            print(('from %s import GUID' % modname), file=(self.imports))

    _typedefs = 0

    def Typedef(self, tp):
        self._typedefs += 1
        if type(tp.typ) in (typedesc.Structure, typedesc.Union):
            self.generate(tp.typ.get_head())
            self.more.add(tp.typ)
        else:
            self.generate(tp.typ)
        if self.type_name(tp.typ) in self.known_symbols:
            stream = self.imports
        else:
            stream = self.stream
        if tp.name != self.type_name(tp.typ):
            print(('%s = %s' % (
             tp.name, self.type_name(tp.typ))),
              file=stream)
        self.names.add(tp.name)

    def FundamentalType(self, item):
        pass

    def StructureHead(self, head):
        for struct in head.struct.bases:
            self.generate(struct.get_head())
            self.more.add(struct)

        if head.struct.location:
            print(('# %s %s' % head.struct.location), file=(self.stream))
        basenames = [self.type_name(b) for b in head.struct.bases]
        if basenames:
            self.need_GUID()
            method_names = [m.name for m in head.struct.members if type(m) is typedesc.Method]
            print(('class %s(%s):' % (head.struct.name, ', '.join(basenames))), file=(self.stream))
            print("    _iid_ = GUID('{}') # please look up iid and fill in!", file=(self.stream))
            if 'Enum' in method_names:
                print('    def __iter__(self):', file=(self.stream))
                print('        return self.Enum()', file=(self.stream))
            else:
                if method_names == 'Next Skip Reset Clone'.split():
                    print('    def __iter__(self):', file=(self.stream))
                    print('        return self', file=(self.stream))
                    print(file=(self.stream))
                    print('    def next(self):', file=(self.stream))
                    print('         arr, fetched = self.Next(1)', file=(self.stream))
                    print('         if fetched == 0:', file=(self.stream))
                    print('             raise StopIteration', file=(self.stream))
                    print('         return arr[0]', file=(self.stream))
        else:
            methods = [m for m in head.struct.members if type(m) is typedesc.Method]
            if methods:
                print("assert 0, 'cannot generate code for IUnknown'", file=(self.stream))
                print(('class %s(_com_interface):' % head.struct.name), file=(self.stream))
                print('    pass', file=(self.stream))
            else:
                if type(head.struct) == typedesc.Structure:
                    print(('class %s(Structure):' % head.struct.name), file=(self.stream))
                    if hasattr(head.struct, '_recordinfo_'):
                        print(('    _recordinfo_ = %r' % (head.struct._recordinfo_,)), file=(self.stream))
                    else:
                        print('    pass', file=(self.stream))
                else:
                    if type(head.struct) == typedesc.Union:
                        print(('class %s(Union):' % head.struct.name), file=(self.stream))
                        print('    pass', file=(self.stream))
                    self.names.add(head.struct.name)

    _structures = 0

    def Structure(self, struct):
        self._structures += 1
        self.generate(struct.get_head())
        self.generate(struct.get_body())

    Union = Structure

    def StructureBody--- This code section failed: ---

 L. 458         0  BUILD_LIST_0          0 
                2  STORE_FAST               'fields'

 L. 459         4  BUILD_LIST_0          0 
                6  STORE_FAST               'methods'

 L. 460         8  SETUP_LOOP          162  'to 162'
               10  LOAD_FAST                'body'
               12  LOAD_ATTR                struct
               14  LOAD_ATTR                members
               16  GET_ITER         
             18_0  COME_FROM           156  '156'
               18  FOR_ITER            160  'to 160'
               20  STORE_FAST               'm'

 L. 461        22  LOAD_GLOBAL              type
               24  LOAD_FAST                'm'
               26  CALL_FUNCTION_1       1  '1 positional argument'
               28  LOAD_GLOBAL              typedesc
               30  LOAD_ATTR                Field
               32  COMPARE_OP               is
               34  POP_JUMP_IF_FALSE    92  'to 92'

 L. 462        36  LOAD_FAST                'fields'
               38  LOAD_METHOD              append
               40  LOAD_FAST                'm'
               42  CALL_METHOD_1         1  '1 positional argument'
               44  POP_TOP          

 L. 463        46  LOAD_GLOBAL              type
               48  LOAD_FAST                'm'
               50  LOAD_ATTR                typ
               52  CALL_FUNCTION_1       1  '1 positional argument'
               54  LOAD_GLOBAL              typedesc
               56  LOAD_ATTR                Typedef
               58  COMPARE_OP               is
               60  POP_JUMP_IF_FALSE    78  'to 78'

 L. 464        62  LOAD_FAST                'self'
               64  LOAD_METHOD              generate
               66  LOAD_GLOBAL              get_real_type
               68  LOAD_FAST                'm'
               70  LOAD_ATTR                typ
               72  CALL_FUNCTION_1       1  '1 positional argument'
               74  CALL_METHOD_1         1  '1 positional argument'
               76  POP_TOP          
             78_0  COME_FROM            60  '60'

 L. 465        78  LOAD_FAST                'self'
               80  LOAD_METHOD              generate
               82  LOAD_FAST                'm'
               84  LOAD_ATTR                typ
               86  CALL_METHOD_1         1  '1 positional argument'
               88  POP_TOP          
               90  JUMP_BACK            18  'to 18'
             92_0  COME_FROM            34  '34'

 L. 466        92  LOAD_GLOBAL              type
               94  LOAD_FAST                'm'
               96  CALL_FUNCTION_1       1  '1 positional argument'
               98  LOAD_GLOBAL              typedesc
              100  LOAD_ATTR                Method
              102  COMPARE_OP               is
              104  POP_JUMP_IF_FALSE   144  'to 144'

 L. 467       106  LOAD_FAST                'methods'
              108  LOAD_METHOD              append
              110  LOAD_FAST                'm'
              112  CALL_METHOD_1         1  '1 positional argument'
              114  POP_TOP          

 L. 468       116  LOAD_FAST                'self'
              118  LOAD_METHOD              generate
              120  LOAD_FAST                'm'
              122  LOAD_ATTR                returns
              124  CALL_METHOD_1         1  '1 positional argument'
              126  POP_TOP          

 L. 469       128  LOAD_FAST                'self'
              130  LOAD_METHOD              generate_all
              132  LOAD_FAST                'm'
              134  LOAD_METHOD              iterArgTypes
              136  CALL_METHOD_0         0  '0 positional arguments'
              138  CALL_METHOD_1         1  '1 positional argument'
              140  POP_TOP          
              142  JUMP_BACK            18  'to 18'
            144_0  COME_FROM           104  '104'

 L. 470       144  LOAD_GLOBAL              type
              146  LOAD_FAST                'm'
              148  CALL_FUNCTION_1       1  '1 positional argument'
              150  LOAD_GLOBAL              typedesc
              152  LOAD_ATTR                Constructor
              154  COMPARE_OP               is
              156  POP_JUMP_IF_FALSE    18  'to 18'

 L. 471       158  JUMP_BACK            18  'to 18'
              160  POP_BLOCK        
            162_0  COME_FROM_LOOP        8  '8'

 L. 475       162  LOAD_FAST                'methods'
          164_166  POP_JUMP_IF_TRUE    310  'to 310'

 L. 476       168  SETUP_EXCEPT        220  'to 220'

 L. 477       170  LOAD_GLOBAL              calc_packing
              172  LOAD_FAST                'body'
              174  LOAD_ATTR                struct
              176  LOAD_FAST                'fields'
              178  CALL_FUNCTION_2       2  '2 positional arguments'
              180  STORE_FAST               'pack'

 L. 478       182  LOAD_FAST                'pack'
              184  LOAD_CONST               None
              186  COMPARE_OP               is-not
              188  POP_JUMP_IF_FALSE   216  'to 216'

 L. 479       190  LOAD_GLOBAL              print
              192  LOAD_STR                 '%s._pack_ = %s'
              194  LOAD_FAST                'body'
              196  LOAD_ATTR                struct
              198  LOAD_ATTR                name
              200  LOAD_FAST                'pack'
              202  BUILD_TUPLE_2         2 
              204  BINARY_MODULO    
              206  LOAD_FAST                'self'
              208  LOAD_ATTR                stream
              210  LOAD_CONST               ('file',)
              212  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              214  POP_TOP          
            216_0  COME_FROM           188  '188'
              216  POP_BLOCK        
              218  JUMP_FORWARD        310  'to 310'
            220_0  COME_FROM_EXCEPT    168  '168'

 L. 480       220  DUP_TOP          
              222  LOAD_GLOBAL              PackingError
              224  COMPARE_OP               exception-match
          226_228  POP_JUMP_IF_FALSE   308  'to 308'
              230  POP_TOP          
              232  STORE_FAST               'details'
              234  POP_TOP          
              236  SETUP_FINALLY       296  'to 296'

 L. 482       238  LOAD_CONST               0
              240  LOAD_CONST               None
              242  IMPORT_NAME              warnings
              244  STORE_FAST               'warnings'

 L. 483       246  LOAD_STR                 'Structure %s: %s'
              248  LOAD_FAST                'body'
              250  LOAD_ATTR                struct
              252  LOAD_ATTR                name
              254  LOAD_FAST                'details'
              256  BUILD_TUPLE_2         2 
              258  BINARY_MODULO    
              260  STORE_FAST               'message'

 L. 484       262  LOAD_FAST                'warnings'
              264  LOAD_METHOD              warn
              266  LOAD_FAST                'message'
              268  LOAD_GLOBAL              UserWarning
              270  CALL_METHOD_2         2  '2 positional arguments'
              272  POP_TOP          

 L. 485       274  LOAD_GLOBAL              print
              276  LOAD_STR                 '# WARNING: %s'
              278  LOAD_FAST                'details'
              280  BINARY_MODULO    
              282  LOAD_FAST                'self'
              284  LOAD_ATTR                stream
              286  LOAD_CONST               ('file',)
              288  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              290  POP_TOP          
              292  POP_BLOCK        
              294  LOAD_CONST               None
            296_0  COME_FROM_FINALLY   236  '236'
              296  LOAD_CONST               None
              298  STORE_FAST               'details'
              300  DELETE_FAST              'details'
              302  END_FINALLY      
              304  POP_EXCEPT       
              306  JUMP_FORWARD        310  'to 310'
            308_0  COME_FROM           226  '226'
              308  END_FINALLY      
            310_0  COME_FROM           306  '306'
            310_1  COME_FROM           218  '218'
            310_2  COME_FROM           164  '164'

 L. 487       310  LOAD_FAST                'fields'
          312_314  POP_JUMP_IF_FALSE   770  'to 770'

 L. 488       316  LOAD_FAST                'body'
              318  LOAD_ATTR                struct
              320  LOAD_ATTR                bases
          322_324  POP_JUMP_IF_FALSE   370  'to 370'

 L. 489       326  LOAD_GLOBAL              len
              328  LOAD_FAST                'body'
              330  LOAD_ATTR                struct
              332  LOAD_ATTR                bases
              334  CALL_FUNCTION_1       1  '1 positional argument'
              336  LOAD_CONST               1
              338  COMPARE_OP               ==
          340_342  POP_JUMP_IF_TRUE    348  'to 348'
              344  LOAD_ASSERT              AssertionError
              346  RAISE_VARARGS_1       1  'exception instance'
            348_0  COME_FROM           340  '340'

 L. 490       348  LOAD_FAST                'self'
              350  LOAD_METHOD              generate
              352  LOAD_FAST                'body'
              354  LOAD_ATTR                struct
              356  LOAD_ATTR                bases
              358  LOAD_CONST               0
              360  BINARY_SUBSCR    
              362  LOAD_METHOD              get_body
              364  CALL_METHOD_0         0  '0 positional arguments'
              366  CALL_METHOD_1         1  '1 positional argument'
              368  POP_TOP          
            370_0  COME_FROM           322  '322'

 L. 494       370  SETUP_LOOP          398  'to 398'
              372  LOAD_FAST                'fields'
              374  GET_ITER         
              376  FOR_ITER            396  'to 396'
              378  STORE_FAST               'f'

 L. 495       380  LOAD_FAST                'self'
              382  LOAD_METHOD              type_name
              384  LOAD_FAST                'f'
              386  LOAD_ATTR                typ
              388  CALL_METHOD_1         1  '1 positional argument'
              390  POP_TOP          
          392_394  JUMP_BACK           376  'to 376'
              396  POP_BLOCK        
            398_0  COME_FROM_LOOP      370  '370'

 L. 496       398  LOAD_GLOBAL              print
              400  LOAD_STR                 '%s._fields_ = ['
              402  LOAD_FAST                'body'
              404  LOAD_ATTR                struct
              406  LOAD_ATTR                name
              408  BINARY_MODULO    
              410  LOAD_FAST                'self'
              412  LOAD_ATTR                stream
              414  LOAD_CONST               ('file',)
              416  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              418  POP_TOP          

 L. 497       420  LOAD_FAST                'body'
              422  LOAD_ATTR                struct
              424  LOAD_ATTR                location
          426_428  POP_JUMP_IF_FALSE   452  'to 452'

 L. 498       430  LOAD_GLOBAL              print
              432  LOAD_STR                 '    # %s %s'
              434  LOAD_FAST                'body'
              436  LOAD_ATTR                struct
              438  LOAD_ATTR                location
              440  BINARY_MODULO    
              442  LOAD_FAST                'self'
              444  LOAD_ATTR                stream
              446  LOAD_CONST               ('file',)
              448  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              450  POP_TOP          
            452_0  COME_FROM           426  '426'

 L. 500       452  LOAD_CONST               0
              454  STORE_FAST               'unnamed_index'

 L. 501       456  SETUP_LOOP          612  'to 612'
              458  LOAD_FAST                'fields'
              460  GET_ITER         
              462  FOR_ITER            610  'to 610'
              464  STORE_FAST               'f'

 L. 502       466  LOAD_FAST                'f'
              468  LOAD_ATTR                name
          470_472  POP_JUMP_IF_TRUE    522  'to 522'

 L. 503       474  LOAD_FAST                'unnamed_index'
          476_478  POP_JUMP_IF_FALSE   490  'to 490'

 L. 504       480  LOAD_STR                 '_%d'
              482  LOAD_FAST                'unnamed_index'
              484  BINARY_MODULO    
              486  STORE_FAST               'fieldname'
              488  JUMP_FORWARD        494  'to 494'
            490_0  COME_FROM           476  '476'

 L. 506       490  LOAD_STR                 '_'
              492  STORE_FAST               'fieldname'
            494_0  COME_FROM           488  '488'

 L. 507       494  LOAD_FAST                'unnamed_index'
              496  LOAD_CONST               1
              498  INPLACE_ADD      
              500  STORE_FAST               'unnamed_index'

 L. 508       502  LOAD_GLOBAL              print
              504  LOAD_STR                 "    # Unnamed field renamed to '%s'"
              506  LOAD_FAST                'fieldname'
              508  BINARY_MODULO    
              510  LOAD_FAST                'self'
              512  LOAD_ATTR                stream
              514  LOAD_CONST               ('file',)
              516  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              518  POP_TOP          
              520  JUMP_FORWARD        528  'to 528'
            522_0  COME_FROM           470  '470'

 L. 510       522  LOAD_FAST                'f'
              524  LOAD_ATTR                name
              526  STORE_FAST               'fieldname'
            528_0  COME_FROM           520  '520'

 L. 511       528  LOAD_FAST                'f'
              530  LOAD_ATTR                bits
              532  LOAD_CONST               None
              534  COMPARE_OP               is
          536_538  POP_JUMP_IF_FALSE   572  'to 572'

 L. 512       540  LOAD_GLOBAL              print
              542  LOAD_STR                 "    ('%s', %s),"
              544  LOAD_FAST                'fieldname'
              546  LOAD_FAST                'self'
              548  LOAD_METHOD              type_name
              550  LOAD_FAST                'f'
              552  LOAD_ATTR                typ
              554  CALL_METHOD_1         1  '1 positional argument'
              556  BUILD_TUPLE_2         2 
              558  BINARY_MODULO    
              560  LOAD_FAST                'self'
              562  LOAD_ATTR                stream
              564  LOAD_CONST               ('file',)
              566  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              568  POP_TOP          
              570  JUMP_BACK           462  'to 462'
            572_0  COME_FROM           536  '536'

 L. 514       572  LOAD_GLOBAL              print
              574  LOAD_STR                 "    ('%s', %s, %s),"
              576  LOAD_FAST                'fieldname'
              578  LOAD_FAST                'self'
              580  LOAD_METHOD              type_name
              582  LOAD_FAST                'f'
              584  LOAD_ATTR                typ
              586  CALL_METHOD_1         1  '1 positional argument'
              588  LOAD_FAST                'f'
              590  LOAD_ATTR                bits
              592  BUILD_TUPLE_3         3 
              594  BINARY_MODULO    
              596  LOAD_FAST                'self'
              598  LOAD_ATTR                stream
              600  LOAD_CONST               ('file',)
              602  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              604  POP_TOP          
          606_608  JUMP_BACK           462  'to 462'
              610  POP_BLOCK        
            612_0  COME_FROM_LOOP      456  '456'

 L. 515       612  LOAD_GLOBAL              print
              614  LOAD_STR                 ']'
              616  LOAD_FAST                'self'
              618  LOAD_ATTR                stream
              620  LOAD_CONST               ('file',)
              622  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              624  POP_TOP          

 L. 517       626  LOAD_FAST                'body'
              628  LOAD_ATTR                struct
              630  LOAD_ATTR                size
              632  LOAD_CONST               None
              634  COMPARE_OP               is
          636_638  POP_JUMP_IF_FALSE   668  'to 668'

 L. 518       640  LOAD_STR                 '# The size provided by the typelib is incorrect.\n# The size and alignment check for %s is skipped.'
              642  STORE_FAST               'msg'

 L. 520       644  LOAD_GLOBAL              print
              646  LOAD_FAST                'msg'
              648  LOAD_FAST                'body'
              650  LOAD_ATTR                struct
              652  LOAD_ATTR                name
              654  BINARY_MODULO    
              656  LOAD_FAST                'self'
              658  LOAD_ATTR                stream
              660  LOAD_CONST               ('file',)
              662  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              664  POP_TOP          
              666  JUMP_FORWARD        770  'to 770'
            668_0  COME_FROM           636  '636'

 L. 521       668  LOAD_FAST                'body'
              670  LOAD_ATTR                struct
              672  LOAD_ATTR                name
              674  LOAD_GLOBAL              dont_assert_size
              676  COMPARE_OP               not-in
          678_680  POP_JUMP_IF_FALSE   770  'to 770'

 L. 522       682  LOAD_FAST                'body'
              684  LOAD_ATTR                struct
              686  LOAD_ATTR                size
              688  LOAD_CONST               8
              690  BINARY_FLOOR_DIVIDE
              692  STORE_FAST               'size'

 L. 523       694  LOAD_GLOBAL              print
              696  LOAD_STR                 'assert sizeof(%s) == %s, sizeof(%s)'

 L. 524       698  LOAD_FAST                'body'
              700  LOAD_ATTR                struct
              702  LOAD_ATTR                name
              704  LOAD_FAST                'size'
              706  LOAD_FAST                'body'
              708  LOAD_ATTR                struct
              710  LOAD_ATTR                name
              712  BUILD_TUPLE_3         3 
              714  BINARY_MODULO    
              716  LOAD_FAST                'self'
              718  LOAD_ATTR                stream
              720  LOAD_CONST               ('file',)
              722  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              724  POP_TOP          

 L. 525       726  LOAD_FAST                'body'
              728  LOAD_ATTR                struct
              730  LOAD_ATTR                align
              732  LOAD_CONST               8
              734  BINARY_FLOOR_DIVIDE
              736  STORE_FAST               'align'

 L. 526       738  LOAD_GLOBAL              print
              740  LOAD_STR                 'assert alignment(%s) == %s, alignment(%s)'

 L. 527       742  LOAD_FAST                'body'
              744  LOAD_ATTR                struct
              746  LOAD_ATTR                name
              748  LOAD_FAST                'align'
              750  LOAD_FAST                'body'
              752  LOAD_ATTR                struct
              754  LOAD_ATTR                name
              756  BUILD_TUPLE_3         3 
              758  BINARY_MODULO    
              760  LOAD_FAST                'self'
              762  LOAD_ATTR                stream
              764  LOAD_CONST               ('file',)
              766  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              768  POP_TOP          
            770_0  COME_FROM           678  '678'
            770_1  COME_FROM           666  '666'
            770_2  COME_FROM           312  '312'

 L. 529       770  LOAD_FAST                'methods'
          772_774  POP_JUMP_IF_FALSE  1044  'to 1044'

 L. 530       776  LOAD_FAST                'self'
              778  LOAD_METHOD              need_COMMETHOD
              780  CALL_METHOD_0         0  '0 positional arguments'
              782  POP_TOP          

 L. 534       784  SETUP_LOOP          842  'to 842'
              786  LOAD_FAST                'methods'
              788  GET_ITER         
              790  FOR_ITER            840  'to 840'
              792  STORE_FAST               'm'

 L. 535       794  LOAD_FAST                'self'
              796  LOAD_METHOD              type_name
              798  LOAD_FAST                'm'
              800  LOAD_ATTR                returns
              802  CALL_METHOD_1         1  '1 positional argument'
              804  POP_TOP          

 L. 536       806  SETUP_LOOP          836  'to 836'
              808  LOAD_FAST                'm'
              810  LOAD_METHOD              iterArgTypes
              812  CALL_METHOD_0         0  '0 positional arguments'
              814  GET_ITER         
              816  FOR_ITER            834  'to 834'
              818  STORE_FAST               'a'

 L. 537       820  LOAD_FAST                'self'
              822  LOAD_METHOD              type_name
              824  LOAD_FAST                'a'
              826  CALL_METHOD_1         1  '1 positional argument'
              828  POP_TOP          
          830_832  JUMP_BACK           816  'to 816'
              834  POP_BLOCK        
            836_0  COME_FROM_LOOP      806  '806'
          836_838  JUMP_BACK           790  'to 790'
              840  POP_BLOCK        
            842_0  COME_FROM_LOOP      784  '784'

 L. 538       842  LOAD_GLOBAL              print
              844  LOAD_STR                 '%s._methods_ = ['
              846  LOAD_FAST                'body'
              848  LOAD_ATTR                struct
              850  LOAD_ATTR                name
              852  BINARY_MODULO    
              854  LOAD_FAST                'self'
              856  LOAD_ATTR                stream
              858  LOAD_CONST               ('file',)
              860  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              862  POP_TOP          

 L. 539       864  LOAD_FAST                'body'
              866  LOAD_ATTR                struct
              868  LOAD_ATTR                location
          870_872  POP_JUMP_IF_FALSE   896  'to 896'

 L. 540       874  LOAD_GLOBAL              print
              876  LOAD_STR                 '# %s %s'
              878  LOAD_FAST                'body'
              880  LOAD_ATTR                struct
              882  LOAD_ATTR                location
              884  BINARY_MODULO    
              886  LOAD_FAST                'self'
              888  LOAD_ATTR                stream
              890  LOAD_CONST               ('file',)
              892  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              894  POP_TOP          
            896_0  COME_FROM           870  '870'

 L. 542       896  SETUP_LOOP         1030  'to 1030'
              898  LOAD_FAST                'methods'
              900  GET_ITER         
              902  FOR_ITER           1028  'to 1028'
              904  STORE_FAST               'm'

 L. 543       906  LOAD_FAST                'm'
              908  LOAD_ATTR                location
          910_912  POP_JUMP_IF_FALSE   934  'to 934'

 L. 544       914  LOAD_GLOBAL              print
              916  LOAD_STR                 '    # %s %s'
              918  LOAD_FAST                'm'
              920  LOAD_ATTR                location
              922  BINARY_MODULO    
              924  LOAD_FAST                'self'
              926  LOAD_ATTR                stream
              928  LOAD_CONST               ('file',)
              930  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              932  POP_TOP          
            934_0  COME_FROM           910  '910'

 L. 545       934  LOAD_GLOBAL              print
              936  LOAD_STR                 "    COMMETHOD([], %s, '%s',"

 L. 546       938  LOAD_FAST                'self'
              940  LOAD_METHOD              type_name
              942  LOAD_FAST                'm'
              944  LOAD_ATTR                returns
              946  CALL_METHOD_1         1  '1 positional argument'

 L. 547       948  LOAD_FAST                'm'
              950  LOAD_ATTR                name
              952  BUILD_TUPLE_2         2 
              954  BINARY_MODULO    
              956  LOAD_FAST                'self'
              958  LOAD_ATTR                stream
              960  LOAD_CONST               ('file',)
              962  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              964  POP_TOP          

 L. 548       966  SETUP_LOOP         1024  'to 1024'
              968  LOAD_FAST                'm'
              970  LOAD_METHOD              iterArgTypes
              972  CALL_METHOD_0         0  '0 positional arguments'
              974  GET_ITER         
              976  FOR_ITER           1022  'to 1022'
              978  STORE_FAST               'a'

 L. 549       980  LOAD_GLOBAL              print
              982  LOAD_STR                 '               ( [], %s, ),'
              984  LOAD_FAST                'self'
              986  LOAD_METHOD              type_name
              988  LOAD_FAST                'a'
              990  CALL_METHOD_1         1  '1 positional argument'
              992  BINARY_MODULO    
              994  LOAD_FAST                'self'
              996  LOAD_ATTR                stream
              998  LOAD_CONST               ('file',)
             1000  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1002  POP_TOP          

 L. 550      1004  LOAD_GLOBAL              print
             1006  LOAD_STR                 '             ),'
             1008  LOAD_FAST                'self'
             1010  LOAD_ATTR                stream
             1012  LOAD_CONST               ('file',)
             1014  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1016  POP_TOP          
         1018_1020  JUMP_BACK           976  'to 976'
             1022  POP_BLOCK        
           1024_0  COME_FROM_LOOP      966  '966'
         1024_1026  JUMP_BACK           902  'to 902'
             1028  POP_BLOCK        
           1030_0  COME_FROM_LOOP      896  '896'

 L. 551      1030  LOAD_GLOBAL              print
             1032  LOAD_STR                 ']'
             1034  LOAD_FAST                'self'
             1036  LOAD_ATTR                stream
             1038  LOAD_CONST               ('file',)
             1040  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1042  POP_TOP          
           1044_0  COME_FROM           772  '772'

Parse error at or near `POP_BLOCK' instruction at offset 160

    _midlSAFEARRAY_defined = False

    def need_midlSAFEARRAY(self):
        if self._midlSAFEARRAY_defined:
            return
        print('from comtypes.automation import _midlSAFEARRAY', file=(self.imports))
        self._midlSAFEARRAY_defined = True

    _CoClass_defined = False

    def need_CoClass(self):
        if self._CoClass_defined:
            return
        print('from comtypes import CoClass', file=(self.imports))
        self._CoClass_defined = True

    _dispid_defined = False

    def need_dispid(self):
        if self._dispid_defined:
            return
        print('from comtypes import dispid', file=(self.imports))
        self._dispid_defined = True

    _COMMETHOD_defined = False

    def need_COMMETHOD(self):
        if self._COMMETHOD_defined:
            return
        print('from comtypes import helpstring', file=(self.imports))
        print('from comtypes import COMMETHOD', file=(self.imports))
        self._COMMETHOD_defined = True

    _DISPMETHOD_defined = False

    def need_DISPMETHOD(self):
        if self._DISPMETHOD_defined:
            return
        print('from comtypes import DISPMETHOD, DISPPROPERTY, helpstring', file=(self.imports))
        self._DISPMETHOD_defined = True

    def TypeLib(self, lib):
        print('class Library(object):', file=(self.stream))
        if lib.doc:
            print(('    %r' % lib.doc), file=(self.stream))
        if lib.name:
            print(('    name = %r' % lib.name), file=(self.stream))
        print(('    _reg_typelib_ = (%r, %r, %r)' % (lib.guid, lib.major, lib.minor)), file=(self.stream))
        print(file=(self.stream))

    def External(self, ext):
        libdesc = str(ext.tlib.GetLibAttr())
        if libdesc in self._externals:
            modname = self._externals[libdesc]
            ext.name = '%s.%s' % (modname, ext.symbol_name)
            return
        modname = comtypes.client._generate._name_module(ext.tlib)
        ext.name = '%s.%s' % (modname, ext.symbol_name)
        self._externals[libdesc] = modname
        print('import', modname, file=(self.imports))
        comtypes.client.GetModule(ext.tlib)

    def Constant(self, tp):
        print(('%s = %r # Constant %s' % (tp.name,
         tp.value,
         self.type_name(tp.typ, False))),
          file=(self.stream))
        self.names.add(tp.name)

    def SAFEARRAYType(self, sa):
        self.generate(sa.typ)
        self.need_midlSAFEARRAY()

    _pointertypes = 0

    def PointerType(self, tp):
        self._pointertypes += 1
        if type(tp.typ) is typedesc.ComInterface:
            self.generate(tp.typ.get_head())
            self.more.add(tp.typ)
        else:
            if type(tp.typ) is typedesc.PointerType:
                self.generate(tp.typ)
            else:
                if type(tp.typ) in (typedesc.Union, typedesc.Structure):
                    self.generate(tp.typ.get_head())
                    self.more.add(tp.typ)
                else:
                    if type(tp.typ) is typedesc.Typedef:
                        self.generate(tp.typ)
                    else:
                        self.generate(tp.typ)

    def CoClass(self, coclass):
        self.need_GUID()
        self.need_CoClass()
        print(('class %s(CoClass):' % coclass.name), file=(self.stream))
        doc = getattr(coclass, 'doc', None)
        if doc:
            print(('    %r' % doc), file=(self.stream))
        print(('    _reg_clsid_ = GUID(%r)' % coclass.clsid), file=(self.stream))
        print(('    _idlflags_ = %s' % coclass.idlflags), file=(self.stream))
        if self.filename is not None:
            print('    _typelib_path_ = typelib_path', file=(self.stream))
        libid = coclass.tlibattr.guid
        wMajor, wMinor = coclass.tlibattr.wMajorVerNum, coclass.tlibattr.wMinorVerNum
        print(('    _reg_typelib_ = (%r, %s, %s)' % (str(libid), wMajor, wMinor)), file=(self.stream))
        for itf, idlflags in coclass.interfaces:
            self.generate(itf.get_head())

        implemented = []
        sources = []
        for item in coclass.interfaces:
            if item[1] & 2:
                where = sources
            else:
                where = implemented
            if item[1] & 1:
                where.insert(0, item[0].name)
            else:
                where.append(item[0].name)

        if implemented:
            print(('%s._com_interfaces_ = [%s]' % (coclass.name, ', '.join(implemented))), file=(self.stream))
        if sources:
            print(('%s._outgoing_interfaces_ = [%s]' % (coclass.name, ', '.join(sources))), file=(self.stream))
        print(file=(self.stream))
        self.names.add(coclass.name)

    def ComInterface(self, itf):
        self.generate(itf.get_head())
        self.generate(itf.get_body())
        self.names.add(itf.name)

    def _is_enuminterface(self, itf):
        if not itf.name.startswith('IEnum'):
            return False
        member_names = [mth.name for mth in itf.members]
        for name in ('Next', 'Skip', 'Reset', 'Clone'):
            if name not in member_names:
                return False

        return True

    def ComInterfaceHead(self, head):
        if head.itf.name in self.known_symbols:
            return
        base = head.itf.base
        if head.itf.base is None:
            return
        self.generate(base.get_head())
        self.more.add(base)
        basename = self.type_name(head.itf.base)
        self.need_GUID()
        print(('class %s(%s):' % (head.itf.name, basename)), file=(self.stream))
        print('    _case_insensitive_ = True', file=(self.stream))
        doc = getattr(head.itf, 'doc', None)
        if doc:
            print(('    %r' % doc), file=(self.stream))
        print(('    _iid_ = GUID(%r)' % head.itf.iid), file=(self.stream))
        print(('    _idlflags_ = %s' % head.itf.idlflags), file=(self.stream))
        if self._is_enuminterface(head.itf):
            print('    def __iter__(self):', file=(self.stream))
            print('        return self', file=(self.stream))
            print(file=(self.stream))
            print('    def next(self):', file=(self.stream))
            print('        item, fetched = self.Next(1)', file=(self.stream))
            print('        if fetched:', file=(self.stream))
            print('            return item', file=(self.stream))
            print('        raise StopIteration', file=(self.stream))
            print(file=(self.stream))
            print('    def __getitem__(self, index):', file=(self.stream))
            print('        self.Reset()', file=(self.stream))
            print('        self.Skip(index)', file=(self.stream))
            print('        item, fetched = self.Next(1)', file=(self.stream))
            print('        if fetched:', file=(self.stream))
            print('            return item', file=(self.stream))
            print('        raise IndexError(index)', file=(self.stream))
            print(file=(self.stream))

    def ComInterfaceBody(self, body):
        self.generate(body.itf.base)
        for m in body.itf.members:
            for a in m.arguments:
                self.generate(a[0])

            self.generate(m.returns)

        self.need_COMMETHOD()
        self.need_dispid()
        print(('%s._methods_ = [' % body.itf.name), file=(self.stream))
        for m in body.itf.members:
            if isinstance(m, typedesc.ComMethod):
                self.make_ComMethod(m, 'dual' in body.itf.idlflags)
            else:
                raise TypeError("what's this?")

        print(']', file=(self.stream))
        print('################################################################', file=(self.stream))
        print(('## code template for %s implementation' % body.itf.name), file=(self.stream))
        print(('##class %s_Impl(object):' % body.itf.name), file=(self.stream))
        methods = {}
        for m in body.itf.members:
            if isinstance(m, typedesc.ComMethod):
                inargs = [a[1] or '<unnamed>' for a in m.arguments if 'out' not in a[2]]
                outargs = [a[1] or '<unnamed>' for a in m.arguments if 'out' in a[2]]
                if 'propget' in m.idlflags:
                    methods.setdefault(m.name, [0, inargs, outargs, m.doc])[0] |= 1
                elif 'propput' in m.idlflags:
                    methods.setdefault(m.name, [0, inargs[:-1], inargs[-1:], m.doc])[0] |= 2
                else:
                    methods[m.name] = [
                     0, inargs, outargs, m.doc]

        for name, (typ, inargs, outargs, doc) in methods.items():
            if typ == 0:
                print(('##    def %s(%s):' % (name, ', '.join(['self'] + inargs))), file=(self.stream))
                print(('##        %r' % (doc or '-no docstring-')), file=(self.stream))
                print(('##        #return %s' % ', '.join(outargs)), file=(self.stream))
            else:
                if typ == 1:
                    print('##    @property', file=(self.stream))
                    print(('##    def %s(%s):' % (name, ', '.join(['self'] + inargs))), file=(self.stream))
                    print(('##        %r' % (doc or '-no docstring-')), file=(self.stream))
                    print(('##        #return %s' % ', '.join(outargs)), file=(self.stream))
                else:
                    if typ == 2:
                        print(('##    def _set(%s):' % ', '.join(['self'] + inargs + outargs)), file=(self.stream))
                        print(('##        %r' % (doc or '-no docstring-')), file=(self.stream))
                        print(('##    %s = property(fset = _set, doc = _set.__doc__)' % name), file=(self.stream))
                    else:
                        if typ == 3:
                            print(('##    def _get(%s):' % ', '.join(['self'] + inargs)), file=(self.stream))
                            print(('##        %r' % (doc or '-no docstring-')), file=(self.stream))
                            print(('##        #return %s' % ', '.join(outargs)), file=(self.stream))
                            print(('##    def _set(%s):' % ', '.join(['self'] + inargs + outargs)), file=(self.stream))
                            print(('##        %r' % (doc or '-no docstring-')), file=(self.stream))
                            print(('##    %s = property(_get, _set, doc = _set.__doc__)' % name), file=(self.stream))
                        else:
                            raise RuntimeError('BUG')
            print('##', file=(self.stream))

        print(file=(self.stream))

    def DispInterface(self, itf):
        self.generate(itf.get_head())
        self.generate(itf.get_body())
        self.names.add(itf.name)

    def DispInterfaceHead(self, head):
        self.generate(head.itf.base)
        basename = self.type_name(head.itf.base)
        self.need_GUID()
        print(('class %s(%s):' % (head.itf.name, basename)), file=(self.stream))
        print('    _case_insensitive_ = True', file=(self.stream))
        doc = getattr(head.itf, 'doc', None)
        if doc:
            print(('    %r' % doc), file=(self.stream))
        print(('    _iid_ = GUID(%r)' % head.itf.iid), file=(self.stream))
        print(('    _idlflags_ = %s' % head.itf.idlflags), file=(self.stream))
        print('    _methods_ = []', file=(self.stream))

    def DispInterfaceBody(self, body):
        for m in body.itf.members:
            if isinstance(m, typedesc.DispMethod):
                for a in m.arguments:
                    self.generate(a[0])

                self.generate(m.returns)
            elif isinstance(m, typedesc.DispProperty):
                self.generate(m.typ)
            else:
                raise TypeError(m)

        self.need_dispid()
        self.need_DISPMETHOD()
        print(('%s._disp_methods_ = [' % body.itf.name), file=(self.stream))
        for m in body.itf.members:
            if isinstance(m, typedesc.DispMethod):
                self.make_DispMethod(m)
            elif isinstance(m, typedesc.DispProperty):
                self.make_DispProperty(m)
            else:
                raise TypeError(m)

        print(']', file=(self.stream))

    def make_ComMethod(self, m, isdual):
        if isdual:
            idlflags = [
             dispid(m.memid)] + m.idlflags
        else:
            idlflags = m.idlflags
        if m.doc:
            idlflags.insert(1, helpstring(m.doc))
        else:
            code = "    COMMETHOD(%r, %s, '%s'" % (
             idlflags,
             self.type_name(m.returns),
             m.name)
            if not m.arguments:
                print(('%s),' % code), file=(self.stream))
            else:
                print(('%s,' % code), file=(self.stream))
                self.stream.write('              ')
                arglist = []
                for typ, name, idlflags, default in m.arguments:
                    type_name = self.type_name(typ)
                    if isinstance(typ, typedesc.ComInterface):
                        self.need_OPENARRAYS()
                        type_name = 'OPENARRAY'
                        if 'in' not in idlflags:
                            idlflags.append('in')
                    if 'lcid' in idlflags:
                        default = lcid
                    if default is not None:
                        self.need_VARIANT_imports(default)
                        arglist.append("( %r, %s, '%s', %r )" % (
                         idlflags,
                         type_name,
                         name,
                         default))
                    else:
                        arglist.append("( %r, %s, '%s' )" % (
                         idlflags,
                         type_name,
                         name))

                self.stream.write(',\n              '.join(arglist))
                print('),', file=(self.stream))

    def make_DispMethod(self, m):
        idlflags = [
         dispid(m.dispid)] + m.idlflags
        if m.doc:
            idlflags.insert(1, helpstring(m.doc))
        else:
            code = "    DISPMETHOD(%r, %s, '%s'" % (
             idlflags,
             self.type_name(m.returns),
             m.name)
            if not m.arguments:
                print(('%s),' % code), file=(self.stream))
            else:
                print(('%s,' % code), file=(self.stream))
                self.stream.write('               ')
                arglist = []
                for typ, name, idlflags, default in m.arguments:
                    self.need_VARIANT_imports(default)
                    if default is not None:
                        arglist.append("( %r, %s, '%s', %r )" % (
                         idlflags,
                         self.type_name(typ),
                         name,
                         default))
                    else:
                        arglist.append("( %r, %s, '%s' )" % (
                         idlflags,
                         self.type_name(typ),
                         name))

                self.stream.write(',\n               '.join(arglist))
                print('),', file=(self.stream))

    def make_DispProperty(self, prop):
        idlflags = [
         dispid(prop.dispid)] + prop.idlflags
        if prop.doc:
            idlflags.insert(1, helpstring(prop.doc))
        print(("    DISPPROPERTY(%r, %s, '%s')," % (
         idlflags,
         self.type_name(prop.typ),
         prop.name)),
          file=(self.stream))


if __name__ == '__main__':
    from . import tlbparser
    tlbparser.main()