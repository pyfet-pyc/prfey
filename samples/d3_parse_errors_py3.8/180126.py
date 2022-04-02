# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: comtypes\tools\codegenerator.py
import os, io, keyword, ctypes
from comtypes.tools import typedesc
import comtypes, comtypes.client, comtypes.client._generate
version = comtypes.__version__
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
    else:
        if total_align != struct.align:
            raise PackingError('total alignment (%s/%s)' % (total_align, struct.align))
        a = total_align
        if pack is not None:
            a = min(pack, a)
        if size % a:
            size += a - size % a
        if size != struct.size:
            raise PackingError('total size (%s/%s)' % (size, struct.size))


def calc_packing--- This code section failed: ---

 L. 116         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'struct'
                4  LOAD_GLOBAL              typedesc
                6  LOAD_ATTR                Structure
                8  CALL_FUNCTION_2       2  ''
               10  STORE_FAST               'isStruct'

 L. 117        12  LOAD_CONST               (None, 128, 64, 32, 16, 8)
               14  GET_ITER         
             16_0  COME_FROM           108  '108'
             16_1  COME_FROM            78  '78'
             16_2  COME_FROM            62  '62'
               16  FOR_ITER            110  'to 110'
               18  STORE_FAST               'pack'

 L. 118        20  SETUP_FINALLY        40  'to 40'

 L. 119        22  LOAD_GLOBAL              _calc_packing
               24  LOAD_FAST                'struct'
               26  LOAD_FAST                'fields'
               28  LOAD_FAST                'pack'
               30  LOAD_FAST                'isStruct'
               32  CALL_FUNCTION_4       4  ''
               34  POP_TOP          
               36  POP_BLOCK        
               38  JUMP_FORWARD         82  'to 82'
             40_0  COME_FROM_FINALLY    20  '20'

 L. 120        40  DUP_TOP          
               42  LOAD_GLOBAL              PackingError
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE    80  'to 80'
               48  POP_TOP          
               50  STORE_FAST               'details'
               52  POP_TOP          
               54  SETUP_FINALLY        68  'to 68'

 L. 121        56  POP_BLOCK        
               58  POP_EXCEPT       
               60  CALL_FINALLY         68  'to 68'
               62  JUMP_BACK            16  'to 16'
               64  POP_BLOCK        
               66  BEGIN_FINALLY    
             68_0  COME_FROM            60  '60'
             68_1  COME_FROM_FINALLY    54  '54'
               68  LOAD_CONST               None
               70  STORE_FAST               'details'
               72  DELETE_FAST              'details'
               74  END_FINALLY      
               76  POP_EXCEPT       
               78  JUMP_BACK            16  'to 16'
             80_0  COME_FROM            46  '46'
               80  END_FINALLY      
             82_0  COME_FROM            38  '38'

 L. 123        82  LOAD_FAST                'pack'
               84  LOAD_CONST               None
               86  COMPARE_OP               is
               88  POP_JUMP_IF_FALSE    96  'to 96'

 L. 124        90  POP_TOP          
               92  LOAD_CONST               None
               94  RETURN_VALUE     
             96_0  COME_FROM            88  '88'

 L. 125        96  LOAD_FAST                'pack'
               98  LOAD_CONST               8
              100  BINARY_TRUE_DIVIDE
              102  ROT_TWO          
              104  POP_TOP          
              106  RETURN_VALUE     
              108  JUMP_BACK            16  'to 16'
            110_0  COME_FROM            16  '16'

 L. 126       110  LOAD_GLOBAL              PackingError
              112  LOAD_STR                 'PACKING FAILED: %s'
              114  LOAD_FAST                'details'
              116  BINARY_MODULO    
              118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `JUMP_BACK' instruction at offset 62


class PackingError(Exception):
    pass


try:
    set
except NameError:
    from sets import Set as set
else:
    dont_assert_size = set([
     '__si_class_type_info_pseudo',
     '__class_type_info_pseudo'])

    def storage(t):
        if isinstance(t, typedesc.Typedef):
            return storage(t.typ)
        if isinstance(t, typedesc.ArrayType):
            s, a = storage(t.typ)
            return (
             s * (int(t.max) - int(t.min) + 1), a)
        return (int(t.size), int(t.align))


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
            if isinstance(item, typedesc.StructureHead):
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
            if not common.endswith('\\'):
                return path1
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
                        pass
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
                while True:
                    if items:
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
            else:
                tlib_mtime = None
                if self.filename is not None:
                    loaded_typelib = comtypes.typeinfo.LoadTypeLib(self.filename)
                    full_filename = comtypes.tools.tlbparser.get_tlib_filename(loaded_typelib)
                    if full_filename is None:
                        tlib_mtime = 0
                    else:
                        tlib_mtime = os.stat(full_filename).st_mtime
                print(('from comtypes import _check_version; _check_version(%r, %f)' % (version, tlib_mtime)), file=(self.output))
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
            else:
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
            else:
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
                    elif method_names == 'Next Skip Reset Clone'.split():
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
                    elif type(head.struct) == typedesc.Structure:
                        print(('class %s(Structure):' % head.struct.name), file=(self.stream))
                        if hasattr(head.struct, '_recordinfo_'):
                            print(('    _recordinfo_ = %r' % (head.struct._recordinfo_,)), file=(self.stream))
                        else:
                            print('    pass', file=(self.stream))
                    elif type(head.struct) == typedesc.Union:
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

 L. 474         0  BUILD_LIST_0          0 
                2  STORE_FAST               'fields'

 L. 475         4  BUILD_LIST_0          0 
                6  STORE_FAST               'methods'

 L. 476         8  LOAD_FAST                'body'
               10  LOAD_ATTR                struct
               12  LOAD_ATTR                members
               14  GET_ITER         
             16_0  COME_FROM           156  '156'
             16_1  COME_FROM           154  '154'
             16_2  COME_FROM           140  '140'
             16_3  COME_FROM            88  '88'
               16  FOR_ITER            158  'to 158'
               18  STORE_FAST               'm'

 L. 477        20  LOAD_GLOBAL              type
               22  LOAD_FAST                'm'
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_GLOBAL              typedesc
               28  LOAD_ATTR                Field
               30  COMPARE_OP               is
               32  POP_JUMP_IF_FALSE    90  'to 90'

 L. 478        34  LOAD_FAST                'fields'
               36  LOAD_METHOD              append
               38  LOAD_FAST                'm'
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          

 L. 479        44  LOAD_GLOBAL              type
               46  LOAD_FAST                'm'
               48  LOAD_ATTR                typ
               50  CALL_FUNCTION_1       1  ''
               52  LOAD_GLOBAL              typedesc
               54  LOAD_ATTR                Typedef
               56  COMPARE_OP               is
               58  POP_JUMP_IF_FALSE    76  'to 76'

 L. 480        60  LOAD_FAST                'self'
               62  LOAD_METHOD              generate
               64  LOAD_GLOBAL              get_real_type
               66  LOAD_FAST                'm'
               68  LOAD_ATTR                typ
               70  CALL_FUNCTION_1       1  ''
               72  CALL_METHOD_1         1  ''
               74  POP_TOP          
             76_0  COME_FROM            58  '58'

 L. 481        76  LOAD_FAST                'self'
               78  LOAD_METHOD              generate
               80  LOAD_FAST                'm'
               82  LOAD_ATTR                typ
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          
               88  JUMP_BACK            16  'to 16'
             90_0  COME_FROM            32  '32'

 L. 482        90  LOAD_GLOBAL              type
               92  LOAD_FAST                'm'
               94  CALL_FUNCTION_1       1  ''
               96  LOAD_GLOBAL              typedesc
               98  LOAD_ATTR                Method
              100  COMPARE_OP               is
              102  POP_JUMP_IF_FALSE   142  'to 142'

 L. 483       104  LOAD_FAST                'methods'
              106  LOAD_METHOD              append
              108  LOAD_FAST                'm'
              110  CALL_METHOD_1         1  ''
              112  POP_TOP          

 L. 484       114  LOAD_FAST                'self'
              116  LOAD_METHOD              generate
              118  LOAD_FAST                'm'
              120  LOAD_ATTR                returns
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          

 L. 485       126  LOAD_FAST                'self'
              128  LOAD_METHOD              generate_all
              130  LOAD_FAST                'm'
              132  LOAD_METHOD              iterArgTypes
              134  CALL_METHOD_0         0  ''
              136  CALL_METHOD_1         1  ''
              138  POP_TOP          
              140  JUMP_BACK            16  'to 16'
            142_0  COME_FROM           102  '102'

 L. 486       142  LOAD_GLOBAL              type
              144  LOAD_FAST                'm'
              146  CALL_FUNCTION_1       1  ''
              148  LOAD_GLOBAL              typedesc
              150  LOAD_ATTR                Constructor
              152  COMPARE_OP               is
              154  POP_JUMP_IF_FALSE_BACK    16  'to 16'

 L. 487       156  JUMP_BACK            16  'to 16'
            158_0  COME_FROM            16  '16'

 L. 491       158  LOAD_FAST                'methods'
          160_162  POP_JUMP_IF_TRUE    306  'to 306'

 L. 492       164  SETUP_FINALLY       216  'to 216'

 L. 493       166  LOAD_GLOBAL              calc_packing
              168  LOAD_FAST                'body'
              170  LOAD_ATTR                struct
              172  LOAD_FAST                'fields'
              174  CALL_FUNCTION_2       2  ''
              176  STORE_FAST               'pack'

 L. 494       178  LOAD_FAST                'pack'
              180  LOAD_CONST               None
              182  COMPARE_OP               is-not
              184  POP_JUMP_IF_FALSE   212  'to 212'

 L. 495       186  LOAD_GLOBAL              print
              188  LOAD_STR                 '%s._pack_ = %s'
              190  LOAD_FAST                'body'
              192  LOAD_ATTR                struct
              194  LOAD_ATTR                name
              196  LOAD_FAST                'pack'
              198  BUILD_TUPLE_2         2 
              200  BINARY_MODULO    
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                stream
              206  LOAD_CONST               ('file',)
              208  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              210  POP_TOP          
            212_0  COME_FROM           184  '184'
              212  POP_BLOCK        
              214  JUMP_FORWARD        306  'to 306'
            216_0  COME_FROM_FINALLY   164  '164'

 L. 496       216  DUP_TOP          
              218  LOAD_GLOBAL              PackingError
              220  COMPARE_OP               exception-match
          222_224  POP_JUMP_IF_FALSE   304  'to 304'
              226  POP_TOP          
              228  STORE_FAST               'details'
              230  POP_TOP          
              232  SETUP_FINALLY       292  'to 292'

 L. 498       234  LOAD_CONST               0
              236  LOAD_CONST               None
              238  IMPORT_NAME              warnings
              240  STORE_FAST               'warnings'

 L. 499       242  LOAD_STR                 'Structure %s: %s'
              244  LOAD_FAST                'body'
              246  LOAD_ATTR                struct
              248  LOAD_ATTR                name
              250  LOAD_FAST                'details'
              252  BUILD_TUPLE_2         2 
              254  BINARY_MODULO    
              256  STORE_FAST               'message'

 L. 500       258  LOAD_FAST                'warnings'
              260  LOAD_METHOD              warn
              262  LOAD_FAST                'message'
              264  LOAD_GLOBAL              UserWarning
              266  CALL_METHOD_2         2  ''
              268  POP_TOP          

 L. 501       270  LOAD_GLOBAL              print
              272  LOAD_STR                 '# WARNING: %s'
              274  LOAD_FAST                'details'
              276  BINARY_MODULO    
              278  LOAD_FAST                'self'
              280  LOAD_ATTR                stream
              282  LOAD_CONST               ('file',)
              284  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              286  POP_TOP          
              288  POP_BLOCK        
              290  BEGIN_FINALLY    
            292_0  COME_FROM_FINALLY   232  '232'
              292  LOAD_CONST               None
              294  STORE_FAST               'details'
              296  DELETE_FAST              'details'
              298  END_FINALLY      
              300  POP_EXCEPT       
              302  JUMP_FORWARD        306  'to 306'
            304_0  COME_FROM           222  '222'
              304  END_FINALLY      
            306_0  COME_FROM           302  '302'
            306_1  COME_FROM           214  '214'
            306_2  COME_FROM           160  '160'

 L. 503       306  LOAD_FAST                'fields'
          308_310  POP_JUMP_IF_FALSE   758  'to 758'

 L. 504       312  LOAD_FAST                'body'
              314  LOAD_ATTR                struct
              316  LOAD_ATTR                bases
          318_320  POP_JUMP_IF_FALSE   366  'to 366'

 L. 505       322  LOAD_GLOBAL              len
              324  LOAD_FAST                'body'
              326  LOAD_ATTR                struct
              328  LOAD_ATTR                bases
              330  CALL_FUNCTION_1       1  ''
              332  LOAD_CONST               1
              334  COMPARE_OP               ==
          336_338  POP_JUMP_IF_TRUE    344  'to 344'
              340  LOAD_ASSERT              AssertionError
              342  RAISE_VARARGS_1       1  'exception instance'
            344_0  COME_FROM           336  '336'

 L. 506       344  LOAD_FAST                'self'
              346  LOAD_METHOD              generate
              348  LOAD_FAST                'body'
              350  LOAD_ATTR                struct
              352  LOAD_ATTR                bases
              354  LOAD_CONST               0
              356  BINARY_SUBSCR    
              358  LOAD_METHOD              get_body
              360  CALL_METHOD_0         0  ''
              362  CALL_METHOD_1         1  ''
              364  POP_TOP          
            366_0  COME_FROM           318  '318'

 L. 510       366  LOAD_FAST                'fields'
              368  GET_ITER         
            370_0  COME_FROM           386  '386'
              370  FOR_ITER            390  'to 390'
              372  STORE_FAST               'f'

 L. 511       374  LOAD_FAST                'self'
              376  LOAD_METHOD              type_name
              378  LOAD_FAST                'f'
              380  LOAD_ATTR                typ
              382  CALL_METHOD_1         1  ''
              384  POP_TOP          
          386_388  JUMP_BACK           370  'to 370'
            390_0  COME_FROM           370  '370'

 L. 512       390  LOAD_GLOBAL              print
              392  LOAD_STR                 '%s._fields_ = ['
              394  LOAD_FAST                'body'
              396  LOAD_ATTR                struct
              398  LOAD_ATTR                name
              400  BINARY_MODULO    
              402  LOAD_FAST                'self'
              404  LOAD_ATTR                stream
              406  LOAD_CONST               ('file',)
              408  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              410  POP_TOP          

 L. 513       412  LOAD_FAST                'body'
              414  LOAD_ATTR                struct
              416  LOAD_ATTR                location
          418_420  POP_JUMP_IF_FALSE   444  'to 444'

 L. 514       422  LOAD_GLOBAL              print
              424  LOAD_STR                 '    # %s %s'
              426  LOAD_FAST                'body'
              428  LOAD_ATTR                struct
              430  LOAD_ATTR                location
              432  BINARY_MODULO    
              434  LOAD_FAST                'self'
              436  LOAD_ATTR                stream
              438  LOAD_CONST               ('file',)
              440  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              442  POP_TOP          
            444_0  COME_FROM           418  '418'

 L. 516       444  LOAD_CONST               0
              446  STORE_FAST               'unnamed_index'

 L. 517       448  LOAD_FAST                'fields'
              450  GET_ITER         
            452_0  COME_FROM           596  '596'
            452_1  COME_FROM           560  '560'
              452  FOR_ITER            600  'to 600'
              454  STORE_FAST               'f'

 L. 518       456  LOAD_FAST                'f'
              458  LOAD_ATTR                name
          460_462  POP_JUMP_IF_TRUE    512  'to 512'

 L. 519       464  LOAD_FAST                'unnamed_index'
          466_468  POP_JUMP_IF_FALSE   480  'to 480'

 L. 520       470  LOAD_STR                 '_%d'
              472  LOAD_FAST                'unnamed_index'
              474  BINARY_MODULO    
              476  STORE_FAST               'fieldname'
              478  JUMP_FORWARD        484  'to 484'
            480_0  COME_FROM           466  '466'

 L. 522       480  LOAD_STR                 '_'
              482  STORE_FAST               'fieldname'
            484_0  COME_FROM           478  '478'

 L. 523       484  LOAD_FAST                'unnamed_index'
              486  LOAD_CONST               1
              488  INPLACE_ADD      
              490  STORE_FAST               'unnamed_index'

 L. 524       492  LOAD_GLOBAL              print
              494  LOAD_STR                 "    # Unnamed field renamed to '%s'"
              496  LOAD_FAST                'fieldname'
              498  BINARY_MODULO    
              500  LOAD_FAST                'self'
              502  LOAD_ATTR                stream
              504  LOAD_CONST               ('file',)
              506  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              508  POP_TOP          
              510  JUMP_FORWARD        518  'to 518'
            512_0  COME_FROM           460  '460'

 L. 526       512  LOAD_FAST                'f'
              514  LOAD_ATTR                name
              516  STORE_FAST               'fieldname'
            518_0  COME_FROM           510  '510'

 L. 527       518  LOAD_FAST                'f'
              520  LOAD_ATTR                bits
              522  LOAD_CONST               None
              524  COMPARE_OP               is
          526_528  POP_JUMP_IF_FALSE   562  'to 562'

 L. 528       530  LOAD_GLOBAL              print
              532  LOAD_STR                 "    ('%s', %s),"
              534  LOAD_FAST                'fieldname'
              536  LOAD_FAST                'self'
              538  LOAD_METHOD              type_name
              540  LOAD_FAST                'f'
              542  LOAD_ATTR                typ
              544  CALL_METHOD_1         1  ''
              546  BUILD_TUPLE_2         2 
              548  BINARY_MODULO    
              550  LOAD_FAST                'self'
              552  LOAD_ATTR                stream
              554  LOAD_CONST               ('file',)
              556  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              558  POP_TOP          
              560  JUMP_BACK           452  'to 452'
            562_0  COME_FROM           526  '526'

 L. 530       562  LOAD_GLOBAL              print
              564  LOAD_STR                 "    ('%s', %s, %s),"
              566  LOAD_FAST                'fieldname'
              568  LOAD_FAST                'self'
              570  LOAD_METHOD              type_name
              572  LOAD_FAST                'f'
              574  LOAD_ATTR                typ
              576  CALL_METHOD_1         1  ''
              578  LOAD_FAST                'f'
              580  LOAD_ATTR                bits
              582  BUILD_TUPLE_3         3 
              584  BINARY_MODULO    
              586  LOAD_FAST                'self'
              588  LOAD_ATTR                stream
              590  LOAD_CONST               ('file',)
              592  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              594  POP_TOP          
          596_598  JUMP_BACK           452  'to 452'
            600_0  COME_FROM           452  '452'

 L. 531       600  LOAD_GLOBAL              print
              602  LOAD_STR                 ']'
              604  LOAD_FAST                'self'
              606  LOAD_ATTR                stream
              608  LOAD_CONST               ('file',)
              610  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              612  POP_TOP          

 L. 533       614  LOAD_FAST                'body'
              616  LOAD_ATTR                struct
              618  LOAD_ATTR                size
              620  LOAD_CONST               None
              622  COMPARE_OP               is
          624_626  POP_JUMP_IF_FALSE   656  'to 656'

 L. 534       628  LOAD_STR                 '# The size provided by the typelib is incorrect.\n# The size and alignment check for %s is skipped.'
              630  STORE_FAST               'msg'

 L. 536       632  LOAD_GLOBAL              print
              634  LOAD_FAST                'msg'
              636  LOAD_FAST                'body'
              638  LOAD_ATTR                struct
              640  LOAD_ATTR                name
              642  BINARY_MODULO    
              644  LOAD_FAST                'self'
              646  LOAD_ATTR                stream
              648  LOAD_CONST               ('file',)
              650  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              652  POP_TOP          
              654  JUMP_FORWARD        758  'to 758'
            656_0  COME_FROM           624  '624'

 L. 537       656  LOAD_FAST                'body'
              658  LOAD_ATTR                struct
              660  LOAD_ATTR                name
              662  LOAD_GLOBAL              dont_assert_size
              664  COMPARE_OP               not-in
          666_668  POP_JUMP_IF_FALSE   758  'to 758'

 L. 538       670  LOAD_FAST                'body'
              672  LOAD_ATTR                struct
              674  LOAD_ATTR                size
              676  LOAD_CONST               8
              678  BINARY_FLOOR_DIVIDE
              680  STORE_FAST               'size'

 L. 539       682  LOAD_GLOBAL              print
              684  LOAD_STR                 'assert sizeof(%s) == %s, sizeof(%s)'

 L. 540       686  LOAD_FAST                'body'
              688  LOAD_ATTR                struct
              690  LOAD_ATTR                name
              692  LOAD_FAST                'size'
              694  LOAD_FAST                'body'
              696  LOAD_ATTR                struct
              698  LOAD_ATTR                name
              700  BUILD_TUPLE_3         3 

 L. 539       702  BINARY_MODULO    

 L. 540       704  LOAD_FAST                'self'
              706  LOAD_ATTR                stream

 L. 539       708  LOAD_CONST               ('file',)
              710  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              712  POP_TOP          

 L. 541       714  LOAD_FAST                'body'
              716  LOAD_ATTR                struct
              718  LOAD_ATTR                align
              720  LOAD_CONST               8
              722  BINARY_FLOOR_DIVIDE
              724  STORE_FAST               'align'

 L. 542       726  LOAD_GLOBAL              print
              728  LOAD_STR                 'assert alignment(%s) == %s, alignment(%s)'

 L. 543       730  LOAD_FAST                'body'
              732  LOAD_ATTR                struct
              734  LOAD_ATTR                name
              736  LOAD_FAST                'align'
              738  LOAD_FAST                'body'
              740  LOAD_ATTR                struct
              742  LOAD_ATTR                name
              744  BUILD_TUPLE_3         3 

 L. 542       746  BINARY_MODULO    

 L. 543       748  LOAD_FAST                'self'
              750  LOAD_ATTR                stream

 L. 542       752  LOAD_CONST               ('file',)
              754  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              756  POP_TOP          
            758_0  COME_FROM           666  '666'
            758_1  COME_FROM           654  '654'
            758_2  COME_FROM           308  '308'

 L. 545       758  LOAD_FAST                'methods'
          760_762  POP_JUMP_IF_FALSE  1016  'to 1016'

 L. 546       764  LOAD_FAST                'self'
              766  LOAD_METHOD              need_COMMETHOD
              768  CALL_METHOD_0         0  ''
              770  POP_TOP          

 L. 550       772  LOAD_FAST                'methods'
              774  GET_ITER         
            776_0  COME_FROM           818  '818'
              776  FOR_ITER            822  'to 822'
              778  STORE_FAST               'm'

 L. 551       780  LOAD_FAST                'self'
              782  LOAD_METHOD              type_name
              784  LOAD_FAST                'm'
              786  LOAD_ATTR                returns
              788  CALL_METHOD_1         1  ''
              790  POP_TOP          

 L. 552       792  LOAD_FAST                'm'
              794  LOAD_METHOD              iterArgTypes
              796  CALL_METHOD_0         0  ''
              798  GET_ITER         
            800_0  COME_FROM           814  '814'
              800  FOR_ITER            818  'to 818'
              802  STORE_FAST               'a'

 L. 553       804  LOAD_FAST                'self'
              806  LOAD_METHOD              type_name
              808  LOAD_FAST                'a'
              810  CALL_METHOD_1         1  ''
              812  POP_TOP          
          814_816  JUMP_BACK           800  'to 800'
            818_0  COME_FROM           800  '800'
          818_820  JUMP_BACK           776  'to 776'
            822_0  COME_FROM           776  '776'

 L. 554       822  LOAD_GLOBAL              print
              824  LOAD_STR                 '%s._methods_ = ['
              826  LOAD_FAST                'body'
              828  LOAD_ATTR                struct
              830  LOAD_ATTR                name
              832  BINARY_MODULO    
              834  LOAD_FAST                'self'
              836  LOAD_ATTR                stream
              838  LOAD_CONST               ('file',)
              840  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              842  POP_TOP          

 L. 555       844  LOAD_FAST                'body'
              846  LOAD_ATTR                struct
              848  LOAD_ATTR                location
          850_852  POP_JUMP_IF_FALSE   876  'to 876'

 L. 556       854  LOAD_GLOBAL              print
              856  LOAD_STR                 '# %s %s'
              858  LOAD_FAST                'body'
              860  LOAD_ATTR                struct
              862  LOAD_ATTR                location
              864  BINARY_MODULO    
              866  LOAD_FAST                'self'
              868  LOAD_ATTR                stream
              870  LOAD_CONST               ('file',)
              872  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              874  POP_TOP          
            876_0  COME_FROM           850  '850'

 L. 558       876  LOAD_FAST                'methods'
              878  GET_ITER         
            880_0  COME_FROM           998  '998'
              880  FOR_ITER           1002  'to 1002'
              882  STORE_FAST               'm'

 L. 559       884  LOAD_FAST                'm'
              886  LOAD_ATTR                location
          888_890  POP_JUMP_IF_FALSE   912  'to 912'

 L. 560       892  LOAD_GLOBAL              print
              894  LOAD_STR                 '    # %s %s'
              896  LOAD_FAST                'm'
              898  LOAD_ATTR                location
              900  BINARY_MODULO    
              902  LOAD_FAST                'self'
              904  LOAD_ATTR                stream
              906  LOAD_CONST               ('file',)
              908  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              910  POP_TOP          
            912_0  COME_FROM           888  '888'

 L. 561       912  LOAD_GLOBAL              print
              914  LOAD_STR                 "    COMMETHOD([], %s, '%s',"

 L. 562       916  LOAD_FAST                'self'
              918  LOAD_METHOD              type_name
              920  LOAD_FAST                'm'
              922  LOAD_ATTR                returns
              924  CALL_METHOD_1         1  ''

 L. 563       926  LOAD_FAST                'm'
              928  LOAD_ATTR                name

 L. 561       930  BUILD_TUPLE_2         2 
              932  BINARY_MODULO    

 L. 563       934  LOAD_FAST                'self'
              936  LOAD_ATTR                stream

 L. 561       938  LOAD_CONST               ('file',)
              940  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              942  POP_TOP          

 L. 564       944  LOAD_FAST                'm'
              946  LOAD_METHOD              iterArgTypes
              948  CALL_METHOD_0         0  ''
              950  GET_ITER         
            952_0  COME_FROM           994  '994'
              952  FOR_ITER            998  'to 998'
              954  STORE_FAST               'a'

 L. 565       956  LOAD_GLOBAL              print
              958  LOAD_STR                 '               ( [], %s, ),'
              960  LOAD_FAST                'self'
              962  LOAD_METHOD              type_name
              964  LOAD_FAST                'a'
              966  CALL_METHOD_1         1  ''
              968  BINARY_MODULO    
              970  LOAD_FAST                'self'
              972  LOAD_ATTR                stream
              974  LOAD_CONST               ('file',)
              976  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              978  POP_TOP          

 L. 566       980  LOAD_GLOBAL              print
              982  LOAD_STR                 '             ),'
              984  LOAD_FAST                'self'
              986  LOAD_ATTR                stream
              988  LOAD_CONST               ('file',)
              990  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              992  POP_TOP          
          994_996  JUMP_BACK           952  'to 952'
            998_0  COME_FROM           952  '952'
         998_1000  JUMP_BACK           880  'to 880'
           1002_0  COME_FROM           880  '880'

 L. 567      1002  LOAD_GLOBAL              print
             1004  LOAD_STR                 ']'
             1006  LOAD_FAST                'self'
             1008  LOAD_ATTR                stream
             1010  LOAD_CONST               ('file',)
             1012  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1014  POP_TOP          
           1016_0  COME_FROM           760  '760'

Parse error at or near `JUMP_BACK' instruction at offset 156

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
            elif type(tp.typ) is typedesc.PointerType:
                self.generate(tp.typ)
            elif type(tp.typ) in (typedesc.Union, typedesc.Structure):
                self.generate(tp.typ.get_head())
                self.more.add(tp.typ)
            elif type(tp.typ) is typedesc.Typedef:
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
            else:
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
                else:
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
            else:
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
                else:
                    self.generate(m.returns)

            else:
                self.need_COMMETHOD()
                self.need_dispid()
                print(('%s._methods_ = [' % body.itf.name), file=(self.stream))
                for m in body.itf.members:
                    if isinstance(m, typedesc.ComMethod):
                        self.make_ComMethod(m, 'dual' in body.itf.idlflags)
                    else:
                        raise TypeError("what's this?")
                else:
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
                            else:
                                if 'propput' in m.idlflags:
                                    methods.setdefault(m.name, [0, inargs[:-1], inargs[-1:], m.doc])[0] |= 2
                                else:
                                    methods[m.name] = [
                                     0, inargs, outargs, m.doc]
                    else:
                        for name, (typ, inargs, outargs, doc) in methods.items():
                            if typ == 0:
                                print(('##    def %s(%s):' % (name, ', '.join(['self'] + inargs))), file=(self.stream))
                                print(('##        %r' % (doc or '-no docstring-')), file=(self.stream))
                                print(('##        #return %s' % ', '.join(outargs)), file=(self.stream))
                            elif typ == 1:
                                print('##    @property', file=(self.stream))
                                print(('##    def %s(%s):' % (name, ', '.join(['self'] + inargs))), file=(self.stream))
                                print(('##        %r' % (doc or '-no docstring-')), file=(self.stream))
                                print(('##        #return %s' % ', '.join(outargs)), file=(self.stream))
                            elif typ == 2:
                                print(('##    def _set(%s):' % ', '.join(['self'] + inargs + outargs)), file=(self.stream))
                                print(('##        %r' % (doc or '-no docstring-')), file=(self.stream))
                                print(('##    %s = property(fset = _set, doc = _set.__doc__)' % name), file=(self.stream))
                            elif typ == 3:
                                print(('##    def _get(%s):' % ', '.join(['self'] + inargs)), file=(self.stream))
                                print(('##        %r' % (doc or '-no docstring-')), file=(self.stream))
                                print(('##        #return %s' % ', '.join(outargs)), file=(self.stream))
                                print(('##    def _set(%s):' % ', '.join(['self'] + inargs + outargs)), file=(self.stream))
                                print(('##        %r' % (doc or '-no docstring-')), file=(self.stream))
                                print(('##    %s = property(_get, _set, doc = _set.__doc__)' % name), file=(self.stream))
                            else:
                                raise RuntimeError('BUG')
                            print('##', file=(self.stream))
                        else:
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
                    else:
                        self.generate(m.returns)

                else:
                    if isinstance(m, typedesc.DispProperty):
                        self.generate(m.typ)
                    else:
                        raise TypeError(m)
            else:
                self.need_dispid()
                self.need_DISPMETHOD()
                print(('%s._disp_methods_ = [' % body.itf.name), file=(self.stream))
                for m in body.itf.members:
                    if isinstance(m, typedesc.DispMethod):
                        self.make_DispMethod(m)
                    else:
                        if isinstance(m, typedesc.DispProperty):
                            self.make_DispProperty(m)
                        else:
                            raise TypeError(m)
                else:
                    print(']', file=(self.stream))

        def make_ComMethod(self, m, isdual):
            if isdual:
                idlflags = [
                 dispid(m.memid)] + m.idlflags
            else:
                idlflags = m.idlflags
            if m.doc:
                idlflags.insert(1, helpstring(m.doc))
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