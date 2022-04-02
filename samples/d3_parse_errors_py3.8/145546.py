# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: cffi\cparser.py
from . import model
from .commontypes import COMMON_TYPES, resolve_common_type
from .error import FFIError, CDefError
try:
    from . import _pycparser as pycparser
except ImportError:
    import pycparser
else:
    import weakref, re, sys
    try:
        if sys.version_info < (3, ):
            import thread as _thread
        else:
            import _thread
        lock = _thread.allocate_lock()
    except ImportError:
        lock = None
    else:

        def _workaround_for_static_import_finders():
            import pycparser.yacctab, pycparser.lextab


        CDEF_SOURCE_STRING = '<cdef source string>'
        _r_comment = re.compile('/\\*.*?\\*/|//([^\\n\\\\]|\\\\.)*?$', re.DOTALL | re.MULTILINE)
        _r_define = re.compile('^\\s*#\\s*define\\s+([A-Za-z_][A-Za-z_0-9]*)\\b((?:[^\\n\\\\]|\\\\.)*?)$', re.DOTALL | re.MULTILINE)
        _r_partial_enum = re.compile('=\\s*\\.\\.\\.\\s*[,}]|\\.\\.\\.\\s*\\}')
        _r_enum_dotdotdot = re.compile('__dotdotdot\\d+__$')
        _r_partial_array = re.compile('\\[\\s*\\.\\.\\.\\s*\\]')
        _r_words = re.compile('\\w+|\\S')
        _parser_cache = None
        _r_int_literal = re.compile('-?0?x?[0-9a-f]+[lu]*$', re.IGNORECASE)
        _r_stdcall1 = re.compile('\\b(__stdcall|WINAPI)\\b')
        _r_stdcall2 = re.compile('[(]\\s*(__stdcall|WINAPI)\\b')
        _r_cdecl = re.compile('\\b__cdecl\\b')
        _r_extern_python = re.compile('\\bextern\\s*"(Python|Python\\s*\\+\\s*C|C\\s*\\+\\s*Python)"\\s*.')
        _r_star_const_space = re.compile('[*]\\s*((const|volatile|restrict)\\b\\s*)+')
        _r_int_dotdotdot = re.compile('(\\b(int|long|short|signed|unsigned|char)\\s*)+\\.\\.\\.')
        _r_float_dotdotdot = re.compile('\\b(double|float)\\s*\\.\\.\\.')

        def _get_parser():
            global _parser_cache
            if _parser_cache is None:
                _parser_cache = pycparser.CParser()
            return _parser_cache


        def _workaround_for_old_pycparser(csource):
            parts = []
            while True:
                match = _r_star_const_space.search(csource)
                if not match:
                    pass
                else:
                    parts.append(csource[:match.start()])
                    parts.append('(')
                    closing = ')'
                    parts.append(match.group())
                    endpos = match.end()
                if csource.startswith('*', endpos):
                    parts.append('(')
                    closing += ')'
                else:
                    level = 0
                    i = endpos
                    while True:
                        if i < len(csource):
                            c = csource[i]
                            if c == '(':
                                level += 1
                        else:
                            pass
                        if c == ')':
                            if level == 0:
                                pass
                            else:
                                level -= 1
                        else:
                            level == 0 if c in ',;=' else i += 1

                    csource = csource[endpos:i] + closing + csource[i:]

            parts.append(csource)
            return ''.join(parts)


        def _preprocess_extern_python(csource):
            parts = []
            while True:
                match = _r_extern_python.search(csource)
                if not match:
                    pass
                else:
                    endpos = match.end() - 1
                    parts.append(csource[:match.start()])
                    if 'C' in match.group(1):
                        parts.append('void __cffi_extern_python_plus_c_start; ')
                    else:
                        parts.append('void __cffi_extern_python_start; ')
                    if csource[endpos] == '{':
                        closing = csource.find('}', endpos)
                        if closing < 0:
                            raise CDefError('\'extern "Python" {\': no \'}\' found')
                        if csource.find('{', endpos + 1, closing) >= 0:
                            raise NotImplementedError('cannot use { } inside a block \'extern "Python" { ... }\'')
                        parts.append(csource[endpos + 1:closing])
                        csource = csource[closing + 1:]
                    else:
                        semicolon = csource.find(';', endpos)
                        if semicolon < 0:
                            raise CDefError('\'extern "Python": no \';\' found')
                        parts.append(csource[endpos:semicolon + 1])
                        csource = csource[semicolon + 1:]
                    parts.append(' void __cffi_extern_python_stop;')

            parts.append(csource)
            return ''.join(parts)


        def _warn_for_string_literal--- This code section failed: ---

 L. 148         0  LOAD_STR                 '"'
                2  LOAD_FAST                'csource'
                4  COMPARE_OP               not-in
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 149         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 150        12  LOAD_FAST                'csource'
               14  LOAD_METHOD              splitlines
               16  CALL_METHOD_0         0  ''
               18  GET_ITER         
             20_0  COME_FROM            68  '68'
             20_1  COME_FROM            44  '44'
             20_2  COME_FROM            30  '30'
               20  FOR_ITER             70  'to 70'
               22  STORE_FAST               'line'

 L. 151        24  LOAD_STR                 '"'
               26  LOAD_FAST                'line'
               28  COMPARE_OP               in
               30  POP_JUMP_IF_FALSE_BACK    20  'to 20'
               32  LOAD_FAST                'line'
               34  LOAD_METHOD              lstrip
               36  CALL_METHOD_0         0  ''
               38  LOAD_METHOD              startswith
               40  LOAD_STR                 '#'
               42  CALL_METHOD_1         1  ''
               44  POP_JUMP_IF_TRUE_BACK    20  'to 20'

 L. 152        46  LOAD_CONST               0
               48  LOAD_CONST               None
               50  IMPORT_NAME              warnings
               52  STORE_FAST               'warnings'

 L. 153        54  LOAD_FAST                'warnings'
               56  LOAD_METHOD              warn
               58  LOAD_STR                 'String literal found in cdef() or type source. String literals are ignored here, but you should remove them anyway because some character sequences confuse pre-parsing.'
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          

 L. 157        64  POP_TOP          
               66  BREAK_LOOP           70  'to 70'
               68  JUMP_BACK            20  'to 20'
             70_0  COME_FROM            66  '66'
             70_1  COME_FROM            20  '20'

Parse error at or near `COME_FROM' instruction at offset 70_0


        def _warn_for_non_extern_non_static_global_variable(decl):
            if not decl.storage:
                import warnings
                warnings.warn("Global variable '%s' in cdef(): for consistency with C it should have a storage class specifier (usually 'extern')" % (
                 decl.name,))


        def _preprocess(csource):
            csource = _r_comment.sub(' ', csource)
            macros = {}
            for match in _r_define.finditer(csource):
                macroname, macrovalue = match.groups()
                macrovalue = macrovalue.replace('\\\n', '').strip()
                macros[macroname] = macrovalue
            else:
                csource = _r_define.sub('', csource)
                if pycparser.__version__ < '2.14':
                    csource = _workaround_for_old_pycparser(csource)
                csource = _r_stdcall2.sub(' volatile volatile const(', csource)
                csource = _r_stdcall1.sub(' volatile volatile const ', csource)
                csource = _r_cdecl.sub(' ', csource)
                csource = _preprocess_extern_python(csource)
                _warn_for_string_literal(csource)
                csource = _r_partial_array.sub('[__dotdotdotarray__]', csource)
                matches = list(_r_partial_enum.finditer(csource))
                for number, match in enumerate(reversed(matches)):
                    p = match.start()
                    if csource[p] == '=':
                        p2 = csource.find('...', p, match.end())
                        if not p2 > p:
                            raise AssertionError
                        else:
                            csource = '%s,__dotdotdot%d__ %s' % (csource[:p], number,
                             csource[p2 + 3:])
                    else:
                        assert csource[p:p + 3] == '...'
                        csource = '%s __dotdotdot%d__ %s' % (csource[:p], number,
                         csource[p + 3:])
                else:
                    csource = _r_int_dotdotdot.sub(' __dotdotdotint__ ', csource)
                    csource = _r_float_dotdotdot.sub(' __dotdotdotfloat__ ', csource)
                    return (
                     csource.replace('...', ' __dotdotdot__ '), macros)


        def _common_type_names(csource):
            look_for_words = set(COMMON_TYPES)
            look_for_words.add(';')
            look_for_words.add(',')
            look_for_words.add('(')
            look_for_words.add(')')
            look_for_words.add('typedef')
            words_used = set()
            is_typedef = False
            paren = 0
            previous_word = ''
            for word in _r_words.findall(csource):
                if word in look_for_words:
                    if word == ';':
                        if is_typedef:
                            words_used.discard(previous_word)
                            look_for_words.discard(previous_word)
                            is_typedef = False
                    elif word == 'typedef':
                        is_typedef = True
                        paren = 0
                    elif word == '(':
                        paren += 1
                    elif word == ')':
                        paren -= 1
                    elif word == ',':
                        if not is_typedef or paren == 0:
                            words_used.discard(previous_word)
                            look_for_words.discard(previous_word)
                    else:
                        words_used.add(word)
                previous_word = word
            else:
                return words_used


        class Parser(object):

            def __init__(self):
                self._declarations = {}
                self._included_declarations = set()
                self._anonymous_counter = 0
                self._structnode2type = weakref.WeakKeyDictionary()
                self._options = {}
                self._int_constants = {}
                self._recomplete = []
                self._uses_new_feature = None

            def _parse(self, csource):
                csource, macros = _preprocess(csource)
                ctn = _common_type_names(csource)
                typenames = []
                for name in sorted(self._declarations):
                    if name.startswith('typedef '):
                        name = name[8:]
                        typenames.append(name)
                        ctn.discard(name)
                else:
                    typenames += sorted(ctn)
                    csourcelines = []
                    csourcelines.append('# 1 "<cdef automatic initialization code>"')
                    for typename in typenames:
                        csourcelines.append('typedef int %s;' % typename)
                    else:
                        csourcelines.append('typedef int __dotdotdotint__, __dotdotdotfloat__, __dotdotdot__;')
                        csourcelines.append('# 1 "%s"' % (CDEF_SOURCE_STRING,))
                        csourcelines.append(csource)
                        fullcsource = '\n'.join(csourcelines)
                        if lock is not None:
                            lock.acquire()
                        try:
                            try:
                                ast = _get_parser().parse(fullcsource)
                            except pycparser.c_parser.ParseError as e:
                                try:
                                    self.convert_pycparser_error(e, csource)
                                finally:
                                    e = None
                                    del e

                        finally:
                            if lock is not None:
                                lock.release()

                        return (ast, macros, csource)

            def _convert_pycparser_error(self, e, csource):
                line = None
                msg = str(e)
                match = re.match('%s:(\\d+):' % (CDEF_SOURCE_STRING,), msg)
                if match:
                    linenum = int(match.group(1), 10)
                    csourcelines = csource.splitlines()
                    if 1 <= linenum <= len(csourcelines):
                        line = csourcelines[(linenum - 1)]
                return line

            def convert_pycparser_error(self, e, csource):
                line = self._convert_pycparser_error(e, csource)
                msg = str(e)
                if line:
                    msg = 'cannot parse "%s"\n%s' % (line.strip(), msg)
                else:
                    msg = 'parse error\n%s' % (msg,)
                raise CDefError(msg)

            def parse(self, csource, override=False, packed=False, pack=None, dllexport=False):
                if packed:
                    if packed != True:
                        raise ValueError("'packed' should be False or True; use 'pack' to give another value")
                    if pack:
                        raise ValueError("cannot give both 'pack' and 'packed'")
                    pack = 1
                elif pack:
                    if pack & pack - 1:
                        raise ValueError("'pack' must be a power of two, not %r" % (
                         pack,))
                else:
                    pack = 0
                prev_options = self._options
                try:
                    self._options = {'override':override, 
                     'packed':pack, 
                     'dllexport':dllexport}
                    self._internal_parse(csource)
                finally:
                    self._options = prev_options

            def _internal_parse(self, csource):
                ast, macros, csource = self._parse(csource)
                self._process_macros(macros)
                iterator = iter(ast.ext)
                for decl in iterator:
                    if decl.name == '__dotdotdot__':
                        break
                else:
                    assert 0
                    current_decl = None
                    try:
                        self._inside_extern_python = '__cffi_extern_python_stop'
                        for decl in iterator:
                            current_decl = decl
                            if isinstance(decl, pycparser.c_ast.Decl):
                                self._parse_decl(decl)
                            else:
                                if isinstance(decl, pycparser.c_ast.Typedef):
                                    if not decl.name:
                                        raise CDefError('typedef does not declare any name', decl)
                                    else:
                                        quals = 0
                                        if isinstance(decl.type.type, pycparser.c_ast.IdentifierType) and decl.type.type.names[(-1)].startswith('__dotdotdot'):
                                            realtype = self._get_unknown_type(decl)
                                        elif isinstance(decl.type, pycparser.c_ast.PtrDecl)and isinstance(decl.type.type, pycparser.c_ast.TypeDecl) and isinstance(decl.type.type, pycparser.c_ast.TypeDecl) and decl.type.type.type.names[(-1)].startswith('__dotdotdot'):
                                            realtype = self._get_unknown_ptr_type(decl)
                                        else:
                                            realtype, quals = self._get_type_and_quals((decl.type),
                                              name=(decl.name), partial_length_ok=True)
                                        self._declare(('typedef ' + decl.name), realtype, quals=quals)
                                else:
                                    if decl.__class__.__name__ == 'Pragma':
                                        pass
                                    else:
                                        raise CDefError('unexpected <%s>: this construct is valid C but not valid in cdef()' % decl.__class__.__name__, decl)

                    except CDefError as e:
                        try:
                            if len(e.args) == 1:
                                e.args = e.args + (current_decl,)
                            raise
                        finally:
                            e = None
                            del e

                    except FFIError as e:
                        try:
                            msg = self._convert_pycparser_error(e, csource)
                            if msg:
                                e.args = (
                                 e.args[0] + '\n    *** Err: %s' % msg,)
                            raise
                        finally:
                            e = None
                            del e

            def _add_constants(self, key, val):
                if key in self._int_constants:
                    if self._int_constants[key] == val:
                        return
                    raise FFIError('multiple declarations of constant: %s' % (key,))
                self._int_constants[key] = val

            def _add_integer_constant(self, name, int_str):
                int_str = int_str.lower().rstrip('ul')
                neg = int_str.startswith('-')
                if neg:
                    int_str = int_str[1:]
                if not int_str.startswith('0') or int_str != '0':
                    if not int_str.startswith('0x'):
                        int_str = '0o' + int_str[1:]
                    pyvalue = int(int_str, 0)
                    if neg:
                        pyvalue = -pyvalue
                self._add_constants(name, pyvalue)
                self._declare('macro ' + name, pyvalue)

            def _process_macros(self, macros):
                for key, value in macros.items():
                    value = value.strip()
                    if _r_int_literal.match(value):
                        self._add_integer_constant(key, value)
                    else:
                        if value == '...':
                            self._declare('macro ' + key, value)
                        else:
                            raise CDefError('only supports one of the following syntax:\n  #define %s ...     (literally dot-dot-dot)\n  #define %s NUMBER  (with NUMBER an integer constant, decimal/hex/octal)\ngot:\n  #define %s %s' % (
                             key, key, key, value))

            def _declare_function(self, tp, quals, decl):
                tp = self._get_type_pointer(tp, quals)
                if self._options.get('dllexport'):
                    tag = 'dllexport_python '
                elif self._inside_extern_python == '__cffi_extern_python_start':
                    tag = 'extern_python '
                elif self._inside_extern_python == '__cffi_extern_python_plus_c_start':
                    tag = 'extern_python_plus_c '
                else:
                    tag = 'function '
                self._declare(tag + decl.name, tp)

            def _parse_decl(self, decl):
                node = decl.type
                if isinstance(node, pycparser.c_ast.FuncDecl):
                    tp, quals = self._get_type_and_quals(node, name=(decl.name))
                    assert isinstance(tp, model.RawFunctionType)
                    self._declare_function(tp, quals, decl)
                else:
                    if isinstance(node, pycparser.c_ast.Struct):
                        self._get_struct_union_enum_type('struct', node)
                    elif isinstance(node, pycparser.c_ast.Union):
                        self._get_struct_union_enum_type('union', node)
                    elif isinstance(node, pycparser.c_ast.Enum):
                        self._get_struct_union_enum_type('enum', node)
                    elif not decl.name:
                        raise CDefError('construct does not declare any variable', decl)
                    if decl.name:
                        tp, quals = self._get_type_and_quals(node, partial_length_ok=True)
                        if tp.is_raw_function:
                            self._declare_function(tp, quals, decl)
                        elif tp.is_integer_type()and hasattr(decl, 'init') and hasattr(decl, 'init') and _r_int_literal.match(decl.init.value):
                            self._add_integer_constant(decl.name, decl.init.value)
                        elif tp.is_integer_type()and isinstance(decl.init, pycparser.c_ast.UnaryOp)and decl.init.op == '-' and isinstance(decl.init, pycparser.c_ast.UnaryOp) and _r_int_literal.match(decl.init.expr.value):
                            self._add_integer_constant(decl.name, '-' + decl.init.expr.value)
                        elif tp is model.void_type and decl.name.startswith('__cffi_extern_python_'):
                            self._inside_extern_python = decl.name
                        else:
                            if self._inside_extern_python != '__cffi_extern_python_stop':
                                raise CDefError('cannot declare constants or variables with \'extern "Python"\'')
                            if quals & model.Q_CONST and not tp.is_array_type:
                                self._declare(('constant ' + decl.name), tp, quals=quals)
                            else:
                                _warn_for_non_extern_non_static_global_variable(decl)
                                self._declare(('variable ' + decl.name), tp, quals=quals)

            def parse_type(self, cdecl):
                return self.parse_type_and_quals(cdecl)[0]

            def parse_type_and_quals(self, cdecl):
                ast, macros = self._parse('void __dummy(\n%s\n);' % cdecl)[:2]
                assert not macros
                exprnode = ast.ext[(-1)].type.args.params[0]
                if isinstance(exprnode, pycparser.c_ast.ID):
                    raise CDefError("unknown identifier '%s'" % (exprnode.name,))
                return self._get_type_and_quals(exprnode.type)

            def _declare(self, name, obj, included=False, quals=0):
                if name in self._declarations:
                    prevobj, prevquals = self._declarations[name]
                    if prevobj is obj:
                        if prevquals == quals:
                            return
                    if not self._options.get('override'):
                        raise FFIError('multiple declarations of %s (for interactive usage, try cdef(xx, override=True))' % (
                         name,))
                    assert '__dotdotdot__' not in name.split()
                    self._declarations[name] = (obj, quals)
                    if included:
                        self._included_declarations.add(obj)

            def _extract_quals(self, type):
                quals = 0
                if isinstance(type, (pycparser.c_ast.TypeDecl,
                 pycparser.c_ast.PtrDecl)):
                    if 'const' in type.quals:
                        quals |= model.Q_CONST
                    if 'volatile' in type.quals:
                        quals |= model.Q_VOLATILE
                    if 'restrict' in type.quals:
                        quals |= model.Q_RESTRICT
                return quals

            def _get_type_pointer(self, type, quals, declname=None):
                if isinstance(type, model.RawFunctionType):
                    return type.as_function_pointer()
                if isinstance(type, model.StructOrUnionOrEnum):
                    if type.name.startswith('$'):
                        if type.name[1:].isdigit():
                            if type.forcename is None:
                                if declname is not None:
                                    return model.NamedPointerType(type, declname, quals)
                return model.PointerType(type, quals)

            def _get_type_and_quals--- This code section failed: ---

 L. 567         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'typenode'
                4  LOAD_GLOBAL              pycparser
                6  LOAD_ATTR                c_ast
                8  LOAD_ATTR                TypeDecl
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_FALSE   116  'to 116'

 L. 568        14  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'typenode'
               18  LOAD_ATTR                type
               20  LOAD_GLOBAL              pycparser
               22  LOAD_ATTR                c_ast
               24  LOAD_ATTR                IdentifierType
               26  CALL_FUNCTION_2       2  ''

 L. 567        28  POP_JUMP_IF_FALSE   116  'to 116'

 L. 569        30  LOAD_GLOBAL              len
               32  LOAD_FAST                'typenode'
               34  LOAD_ATTR                type
               36  LOAD_ATTR                names
               38  CALL_FUNCTION_1       1  ''
               40  LOAD_CONST               1
               42  COMPARE_OP               ==

 L. 567        44  POP_JUMP_IF_FALSE   116  'to 116'

 L. 570        46  LOAD_STR                 'typedef '
               48  LOAD_FAST                'typenode'
               50  LOAD_ATTR                type
               52  LOAD_ATTR                names
               54  LOAD_CONST               0
               56  BINARY_SUBSCR    
               58  BINARY_ADD       
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                _declarations
               64  COMPARE_OP               in

 L. 567        66  POP_JUMP_IF_FALSE   116  'to 116'

 L. 571        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _declarations
               72  LOAD_STR                 'typedef '
               74  LOAD_FAST                'typenode'
               76  LOAD_ATTR                type
               78  LOAD_ATTR                names
               80  LOAD_CONST               0
               82  BINARY_SUBSCR    
               84  BINARY_ADD       
               86  BINARY_SUBSCR    
               88  UNPACK_SEQUENCE_2     2 
               90  STORE_FAST               'tp'
               92  STORE_FAST               'quals'

 L. 572        94  LOAD_FAST                'quals'
               96  LOAD_FAST                'self'
               98  LOAD_METHOD              _extract_quals
              100  LOAD_FAST                'typenode'
              102  CALL_METHOD_1         1  ''
              104  INPLACE_OR       
              106  STORE_FAST               'quals'

 L. 573       108  LOAD_FAST                'tp'
              110  LOAD_FAST                'quals'
              112  BUILD_TUPLE_2         2 
              114  RETURN_VALUE     
            116_0  COME_FROM            66  '66'
            116_1  COME_FROM            44  '44'
            116_2  COME_FROM            28  '28'
            116_3  COME_FROM            12  '12'

 L. 575       116  LOAD_GLOBAL              isinstance
              118  LOAD_FAST                'typenode'
              120  LOAD_GLOBAL              pycparser
              122  LOAD_ATTR                c_ast
              124  LOAD_ATTR                ArrayDecl
              126  CALL_FUNCTION_2       2  ''
              128  POP_JUMP_IF_FALSE   198  'to 198'

 L. 577       130  LOAD_FAST                'typenode'
              132  LOAD_ATTR                dim
              134  LOAD_CONST               None
              136  COMPARE_OP               is
              138  POP_JUMP_IF_FALSE   146  'to 146'

 L. 578       140  LOAD_CONST               None
              142  STORE_FAST               'length'
              144  JUMP_FORWARD        162  'to 162'
            146_0  COME_FROM           138  '138'

 L. 580       146  LOAD_FAST                'self'
              148  LOAD_ATTR                _parse_constant

 L. 581       150  LOAD_FAST                'typenode'
              152  LOAD_ATTR                dim

 L. 581       154  LOAD_FAST                'partial_length_ok'

 L. 580       156  LOAD_CONST               ('partial_length_ok',)
              158  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              160  STORE_FAST               'length'
            162_0  COME_FROM           144  '144'

 L. 582       162  LOAD_FAST                'self'
              164  LOAD_ATTR                _get_type_and_quals
              166  LOAD_FAST                'typenode'
              168  LOAD_ATTR                type

 L. 583       170  LOAD_FAST                'partial_length_ok'

 L. 582       172  LOAD_CONST               ('partial_length_ok',)
              174  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              176  UNPACK_SEQUENCE_2     2 
              178  STORE_FAST               'tp'
              180  STORE_FAST               'quals'

 L. 584       182  LOAD_GLOBAL              model
              184  LOAD_METHOD              ArrayType
              186  LOAD_FAST                'tp'
              188  LOAD_FAST                'length'
              190  CALL_METHOD_2         2  ''
              192  LOAD_FAST                'quals'
              194  BUILD_TUPLE_2         2 
              196  RETURN_VALUE     
            198_0  COME_FROM           128  '128'

 L. 586       198  LOAD_GLOBAL              isinstance
              200  LOAD_FAST                'typenode'
              202  LOAD_GLOBAL              pycparser
              204  LOAD_ATTR                c_ast
              206  LOAD_ATTR                PtrDecl
              208  CALL_FUNCTION_2       2  ''
          210_212  POP_JUMP_IF_FALSE   264  'to 264'

 L. 588       214  LOAD_FAST                'self'
              216  LOAD_METHOD              _get_type_and_quals
              218  LOAD_FAST                'typenode'
              220  LOAD_ATTR                type
              222  CALL_METHOD_1         1  ''
              224  UNPACK_SEQUENCE_2     2 
              226  STORE_FAST               'itemtype'
              228  STORE_FAST               'itemquals'

 L. 589       230  LOAD_FAST                'self'
              232  LOAD_ATTR                _get_type_pointer
              234  LOAD_FAST                'itemtype'
              236  LOAD_FAST                'itemquals'
              238  LOAD_FAST                'name'
              240  LOAD_CONST               ('declname',)
              242  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              244  STORE_FAST               'tp'

 L. 590       246  LOAD_FAST                'self'
              248  LOAD_METHOD              _extract_quals
              250  LOAD_FAST                'typenode'
              252  CALL_METHOD_1         1  ''
              254  STORE_FAST               'quals'

 L. 591       256  LOAD_FAST                'tp'
              258  LOAD_FAST                'quals'
              260  BUILD_TUPLE_2         2 
              262  RETURN_VALUE     
            264_0  COME_FROM           210  '210'

 L. 593       264  LOAD_GLOBAL              isinstance
              266  LOAD_FAST                'typenode'
              268  LOAD_GLOBAL              pycparser
              270  LOAD_ATTR                c_ast
              272  LOAD_ATTR                TypeDecl
              274  CALL_FUNCTION_2       2  ''
          276_278  POP_JUMP_IF_FALSE   702  'to 702'

 L. 594       280  LOAD_FAST                'self'
              282  LOAD_METHOD              _extract_quals
              284  LOAD_FAST                'typenode'
              286  CALL_METHOD_1         1  ''
              288  STORE_FAST               'quals'

 L. 595       290  LOAD_FAST                'typenode'
              292  LOAD_ATTR                type
              294  STORE_FAST               'type'

 L. 596       296  LOAD_GLOBAL              isinstance
              298  LOAD_FAST                'type'
              300  LOAD_GLOBAL              pycparser
              302  LOAD_ATTR                c_ast
              304  LOAD_ATTR                IdentifierType
              306  CALL_FUNCTION_2       2  ''
          308_310  POP_JUMP_IF_FALSE   588  'to 588'

 L. 599       312  LOAD_GLOBAL              list
              314  LOAD_FAST                'type'
              316  LOAD_ATTR                names
              318  CALL_FUNCTION_1       1  ''
              320  STORE_FAST               'names'

 L. 600       322  LOAD_FAST                'names'
              324  LOAD_STR                 'signed'
              326  LOAD_STR                 'char'
              328  BUILD_LIST_2          2 
              330  COMPARE_OP               !=
          332_334  POP_JUMP_IF_FALSE   506  'to 506'

 L. 601       336  BUILD_MAP_0           0 
              338  STORE_FAST               'prefixes'
            340_0  COME_FROM           396  '396'
            340_1  COME_FROM           390  '390'

 L. 602       340  LOAD_FAST                'names'
          342_344  POP_JUMP_IF_FALSE   400  'to 400'

 L. 603       346  LOAD_FAST                'names'
              348  LOAD_CONST               0
              350  BINARY_SUBSCR    
              352  STORE_FAST               'name'

 L. 604       354  LOAD_FAST                'name'
              356  LOAD_CONST               ('short', 'long', 'signed', 'unsigned')
              358  COMPARE_OP               in
          360_362  POP_JUMP_IF_FALSE   400  'to 400'

 L. 605       364  LOAD_FAST                'prefixes'
              366  LOAD_METHOD              get
              368  LOAD_FAST                'name'
              370  LOAD_CONST               0
              372  CALL_METHOD_2         2  ''
              374  LOAD_CONST               1
              376  BINARY_ADD       
              378  LOAD_FAST                'prefixes'
              380  LOAD_FAST                'name'
              382  STORE_SUBSCR     

 L. 606       384  LOAD_FAST                'names'
              386  LOAD_CONST               0
              388  DELETE_SUBSCR    
              390  JUMP_BACK           340  'to 340'

 L. 608   392_394  JUMP_FORWARD        400  'to 400'
          396_398  JUMP_BACK           340  'to 340'
            400_0  COME_FROM           392  '392'
            400_1  COME_FROM           360  '360'
            400_2  COME_FROM           342  '342'

 L. 610       400  BUILD_LIST_0          0 
              402  STORE_FAST               'newnames'

 L. 611       404  LOAD_CONST               ('unsigned', 'short', 'long')
              406  GET_ITER         
            408_0  COME_FROM           446  '446'
              408  FOR_ITER            450  'to 450'
              410  STORE_FAST               'prefix'

 L. 612       412  LOAD_GLOBAL              range
              414  LOAD_FAST                'prefixes'
              416  LOAD_METHOD              get
              418  LOAD_FAST                'prefix'
              420  LOAD_CONST               0
              422  CALL_METHOD_2         2  ''
              424  CALL_FUNCTION_1       1  ''
              426  GET_ITER         
            428_0  COME_FROM           442  '442'
              428  FOR_ITER            446  'to 446'
              430  STORE_FAST               'i'

 L. 613       432  LOAD_FAST                'newnames'
              434  LOAD_METHOD              append
              436  LOAD_FAST                'prefix'
              438  CALL_METHOD_1         1  ''
              440  POP_TOP          
          442_444  JUMP_BACK           428  'to 428'
            446_0  COME_FROM           428  '428'
          446_448  JUMP_BACK           408  'to 408'
            450_0  COME_FROM           408  '408'

 L. 614       450  LOAD_FAST                'names'
          452_454  POP_JUMP_IF_TRUE    462  'to 462'

 L. 615       456  LOAD_STR                 'int'
              458  BUILD_LIST_1          1 
              460  STORE_FAST               'names'
            462_0  COME_FROM           452  '452'

 L. 616       462  LOAD_FAST                'names'
              464  LOAD_STR                 'int'
              466  BUILD_LIST_1          1 
              468  COMPARE_OP               ==
          470_472  POP_JUMP_IF_FALSE   498  'to 498'

 L. 617       474  LOAD_STR                 'short'
              476  LOAD_FAST                'prefixes'
              478  COMPARE_OP               in
          480_482  POP_JUMP_IF_TRUE    494  'to 494'
              484  LOAD_STR                 'long'
              486  LOAD_FAST                'prefixes'
              488  COMPARE_OP               in
          490_492  POP_JUMP_IF_FALSE   498  'to 498'
            494_0  COME_FROM           480  '480'

 L. 618       494  BUILD_LIST_0          0 
              496  STORE_FAST               'names'
            498_0  COME_FROM           490  '490'
            498_1  COME_FROM           470  '470'

 L. 619       498  LOAD_FAST                'newnames'
              500  LOAD_FAST                'names'
              502  BINARY_ADD       
              504  STORE_FAST               'names'
            506_0  COME_FROM           332  '332'

 L. 620       506  LOAD_STR                 ' '
              508  LOAD_METHOD              join
              510  LOAD_FAST                'names'
              512  CALL_METHOD_1         1  ''
              514  STORE_FAST               'ident'

 L. 621       516  LOAD_FAST                'ident'
              518  LOAD_STR                 'void'
              520  COMPARE_OP               ==
          522_524  POP_JUMP_IF_FALSE   536  'to 536'

 L. 622       526  LOAD_GLOBAL              model
              528  LOAD_ATTR                void_type
              530  LOAD_FAST                'quals'
              532  BUILD_TUPLE_2         2 
              534  RETURN_VALUE     
            536_0  COME_FROM           522  '522'

 L. 623       536  LOAD_FAST                'ident'
              538  LOAD_STR                 '__dotdotdot__'
              540  COMPARE_OP               ==
          542_544  POP_JUMP_IF_FALSE   562  'to 562'

 L. 624       546  LOAD_GLOBAL              FFIError
              548  LOAD_STR                 ':%d: bad usage of "..."'

 L. 625       550  LOAD_FAST                'typenode'
              552  LOAD_ATTR                coord
              554  LOAD_ATTR                line

 L. 624       556  BINARY_MODULO    
              558  CALL_FUNCTION_1       1  ''
              560  RAISE_VARARGS_1       1  'exception instance'
            562_0  COME_FROM           542  '542'

 L. 626       562  LOAD_GLOBAL              resolve_common_type
              564  LOAD_FAST                'self'
              566  LOAD_FAST                'ident'
              568  CALL_FUNCTION_2       2  ''
              570  UNPACK_SEQUENCE_2     2 
              572  STORE_FAST               'tp0'
              574  STORE_FAST               'quals0'

 L. 627       576  LOAD_FAST                'tp0'
              578  LOAD_FAST                'quals'
              580  LOAD_FAST                'quals0'
              582  BINARY_OR        
              584  BUILD_TUPLE_2         2 
              586  RETURN_VALUE     
            588_0  COME_FROM           308  '308'

 L. 629       588  LOAD_GLOBAL              isinstance
              590  LOAD_FAST                'type'
              592  LOAD_GLOBAL              pycparser
              594  LOAD_ATTR                c_ast
              596  LOAD_ATTR                Struct
              598  CALL_FUNCTION_2       2  ''
          600_602  POP_JUMP_IF_FALSE   626  'to 626'

 L. 631       604  LOAD_FAST                'self'
              606  LOAD_METHOD              _get_struct_union_enum_type
              608  LOAD_STR                 'struct'
              610  LOAD_FAST                'type'
              612  LOAD_FAST                'name'
              614  CALL_METHOD_3         3  ''
              616  STORE_FAST               'tp'

 L. 632       618  LOAD_FAST                'tp'
              620  LOAD_FAST                'quals'
              622  BUILD_TUPLE_2         2 
              624  RETURN_VALUE     
            626_0  COME_FROM           600  '600'

 L. 634       626  LOAD_GLOBAL              isinstance
              628  LOAD_FAST                'type'
              630  LOAD_GLOBAL              pycparser
              632  LOAD_ATTR                c_ast
              634  LOAD_ATTR                Union
              636  CALL_FUNCTION_2       2  ''
          638_640  POP_JUMP_IF_FALSE   664  'to 664'

 L. 636       642  LOAD_FAST                'self'
              644  LOAD_METHOD              _get_struct_union_enum_type
              646  LOAD_STR                 'union'
              648  LOAD_FAST                'type'
              650  LOAD_FAST                'name'
              652  CALL_METHOD_3         3  ''
              654  STORE_FAST               'tp'

 L. 637       656  LOAD_FAST                'tp'
              658  LOAD_FAST                'quals'
              660  BUILD_TUPLE_2         2 
              662  RETURN_VALUE     
            664_0  COME_FROM           638  '638'

 L. 639       664  LOAD_GLOBAL              isinstance
              666  LOAD_FAST                'type'
              668  LOAD_GLOBAL              pycparser
              670  LOAD_ATTR                c_ast
              672  LOAD_ATTR                Enum
              674  CALL_FUNCTION_2       2  ''
          676_678  POP_JUMP_IF_FALSE   702  'to 702'

 L. 641       680  LOAD_FAST                'self'
              682  LOAD_METHOD              _get_struct_union_enum_type
              684  LOAD_STR                 'enum'
              686  LOAD_FAST                'type'
              688  LOAD_FAST                'name'
              690  CALL_METHOD_3         3  ''
              692  STORE_FAST               'tp'

 L. 642       694  LOAD_FAST                'tp'
              696  LOAD_FAST                'quals'
              698  BUILD_TUPLE_2         2 
              700  RETURN_VALUE     
            702_0  COME_FROM           676  '676'
            702_1  COME_FROM           276  '276'

 L. 644       702  LOAD_GLOBAL              isinstance
              704  LOAD_FAST                'typenode'
              706  LOAD_GLOBAL              pycparser
              708  LOAD_ATTR                c_ast
              710  LOAD_ATTR                FuncDecl
              712  CALL_FUNCTION_2       2  ''
          714_716  POP_JUMP_IF_FALSE   734  'to 734'

 L. 646       718  LOAD_FAST                'self'
              720  LOAD_METHOD              _parse_function_type
              722  LOAD_FAST                'typenode'
              724  LOAD_FAST                'name'
              726  CALL_METHOD_2         2  ''
              728  LOAD_CONST               0
              730  BUILD_TUPLE_2         2 
              732  RETURN_VALUE     
            734_0  COME_FROM           714  '714'

 L. 649       734  LOAD_GLOBAL              isinstance
              736  LOAD_FAST                'typenode'
              738  LOAD_GLOBAL              pycparser
              740  LOAD_ATTR                c_ast
              742  LOAD_ATTR                Struct
              744  CALL_FUNCTION_2       2  ''
          746_748  POP_JUMP_IF_FALSE   772  'to 772'

 L. 650       750  LOAD_FAST                'self'
              752  LOAD_ATTR                _get_struct_union_enum_type
              754  LOAD_STR                 'struct'
              756  LOAD_FAST                'typenode'
              758  LOAD_FAST                'name'

 L. 651       760  LOAD_CONST               True

 L. 650       762  LOAD_CONST               ('nested',)
              764  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 651       766  LOAD_CONST               0

 L. 650       768  BUILD_TUPLE_2         2 
              770  RETURN_VALUE     
            772_0  COME_FROM           746  '746'

 L. 652       772  LOAD_GLOBAL              isinstance
              774  LOAD_FAST                'typenode'
              776  LOAD_GLOBAL              pycparser
              778  LOAD_ATTR                c_ast
              780  LOAD_ATTR                Union
              782  CALL_FUNCTION_2       2  ''
          784_786  POP_JUMP_IF_FALSE   810  'to 810'

 L. 653       788  LOAD_FAST                'self'
              790  LOAD_ATTR                _get_struct_union_enum_type
              792  LOAD_STR                 'union'
              794  LOAD_FAST                'typenode'
              796  LOAD_FAST                'name'

 L. 654       798  LOAD_CONST               True

 L. 653       800  LOAD_CONST               ('nested',)
              802  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 654       804  LOAD_CONST               0

 L. 653       806  BUILD_TUPLE_2         2 
              808  RETURN_VALUE     
            810_0  COME_FROM           784  '784'

 L. 656       810  LOAD_GLOBAL              FFIError
              812  LOAD_STR                 ':%d: bad or unsupported type declaration'

 L. 657       814  LOAD_FAST                'typenode'
              816  LOAD_ATTR                coord
              818  LOAD_ATTR                line

 L. 656       820  BINARY_MODULO    
              822  CALL_FUNCTION_1       1  ''
              824  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `CALL_FUNCTION_1' instruction at offset 822

            def _parse_function_type(self, typenode, funcname=None):
                params = list(getattr(typenode.args, 'params', []))
                for i, arg in enumerate(params):
                    if not hasattr(arg, 'type'):
                        raise CDefError("%s arg %d: unknown type '%s' (if you meant to use the old C syntax of giving untyped arguments, it is not supported)" % (
                         funcname or 'in expression', i + 1,
                         getattr(arg, 'name', '?')))
                else:
                    ellipsis = len(params) > 0 and isinstance(params[(-1)].type, pycparser.c_ast.TypeDecl) and isinstance(params[(-1)].type.type, pycparser.c_ast.IdentifierType) and params[(-1)].type.type.names == ['__dotdotdot__']
                    if ellipsis:
                        params.pop()
                        if not params:
                            raise CDefError("%s: a function with only '(...)' as argument is not correct C" % (funcname or 'in expression'))
                        args = [(self._as_func_arg)(*self._get_type_and_quals(argdeclnode.type)) for argdeclnode in params]
                        if not ellipsis:
                            if args == [model.void_type]:
                                args = []
                        result, quals = self._get_type_and_quals(typenode.type)
                        abi = None
                        if hasattr(typenode.type, 'quals'):
                            if typenode.type.quals[-3:] == ['volatile', 'volatile', 'const']:
                                abi = '__stdcall'
                        return model.RawFunctionType(tuple(args), result, ellipsis, abi)

            def _as_func_arg(self, type, quals):
                if isinstance(type, model.ArrayType):
                    return model.PointerType(type.item, quals)
                if isinstance(type, model.RawFunctionType):
                    return type.as_function_pointer()
                return type

            def _get_struct_union_enum_type--- This code section failed: ---

 L. 711         0  SETUP_FINALLY        14  'to 14'

 L. 712         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _structnode2type
                6  LOAD_FAST                'type'
                8  BINARY_SUBSCR    
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 713        14  DUP_TOP          
               16  LOAD_GLOBAL              KeyError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    32  'to 32'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 714        28  POP_EXCEPT       
               30  JUMP_FORWARD         34  'to 34'
             32_0  COME_FROM            20  '20'
               32  END_FINALLY      
             34_0  COME_FROM            30  '30'

 L. 724        34  LOAD_FAST                'name'
               36  STORE_FAST               'force_name'

 L. 725        38  LOAD_FAST                'type'
               40  LOAD_ATTR                name
               42  STORE_FAST               'name'

 L. 728        44  LOAD_FAST                'name'
               46  LOAD_CONST               None
               48  COMPARE_OP               is
               50  POP_JUMP_IF_FALSE   100  'to 100'

 L. 731        52  LOAD_FAST                'force_name'
               54  LOAD_CONST               None
               56  COMPARE_OP               is-not
               58  POP_JUMP_IF_FALSE    70  'to 70'

 L. 732        60  LOAD_STR                 '$%s'
               62  LOAD_FAST                'force_name'
               64  BINARY_MODULO    
               66  STORE_FAST               'explicit_name'
               68  JUMP_FORWARD         94  'to 94'
             70_0  COME_FROM            58  '58'

 L. 734        70  LOAD_FAST                'self'
               72  DUP_TOP          
               74  LOAD_ATTR                _anonymous_counter
               76  LOAD_CONST               1
               78  INPLACE_ADD      
               80  ROT_TWO          
               82  STORE_ATTR               _anonymous_counter

 L. 735        84  LOAD_STR                 '$%d'
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                _anonymous_counter
               90  BINARY_MODULO    
               92  STORE_FAST               'explicit_name'
             94_0  COME_FROM            68  '68'

 L. 736        94  LOAD_CONST               None
               96  STORE_FAST               'tp'
               98  JUMP_FORWARD        134  'to 134'
            100_0  COME_FROM            50  '50'

 L. 738       100  LOAD_FAST                'name'
              102  STORE_FAST               'explicit_name'

 L. 739       104  LOAD_STR                 '%s %s'
              106  LOAD_FAST                'kind'
              108  LOAD_FAST                'name'
              110  BUILD_TUPLE_2         2 
              112  BINARY_MODULO    
              114  STORE_FAST               'key'

 L. 740       116  LOAD_FAST                'self'
              118  LOAD_ATTR                _declarations
              120  LOAD_METHOD              get
              122  LOAD_FAST                'key'
              124  LOAD_CONST               (None, None)
              126  CALL_METHOD_2         2  ''
              128  UNPACK_SEQUENCE_2     2 
              130  STORE_FAST               'tp'
              132  STORE_FAST               '_'
            134_0  COME_FROM            98  '98'

 L. 742       134  LOAD_FAST                'tp'
              136  LOAD_CONST               None
              138  COMPARE_OP               is
          140_142  POP_JUMP_IF_FALSE   274  'to 274'

 L. 743       144  LOAD_FAST                'kind'
              146  LOAD_STR                 'struct'
              148  COMPARE_OP               ==
              150  POP_JUMP_IF_FALSE   170  'to 170'

 L. 744       152  LOAD_GLOBAL              model
              154  LOAD_METHOD              StructType
              156  LOAD_FAST                'explicit_name'
              158  LOAD_CONST               None
              160  LOAD_CONST               None
              162  LOAD_CONST               None
              164  CALL_METHOD_4         4  ''
              166  STORE_FAST               'tp'
              168  JUMP_FORWARD        250  'to 250'
            170_0  COME_FROM           150  '150'

 L. 745       170  LOAD_FAST                'kind'
              172  LOAD_STR                 'union'
              174  COMPARE_OP               ==
              176  POP_JUMP_IF_FALSE   196  'to 196'

 L. 746       178  LOAD_GLOBAL              model
              180  LOAD_METHOD              UnionType
              182  LOAD_FAST                'explicit_name'
              184  LOAD_CONST               None
              186  LOAD_CONST               None
              188  LOAD_CONST               None
              190  CALL_METHOD_4         4  ''
              192  STORE_FAST               'tp'
              194  JUMP_FORWARD        250  'to 250'
            196_0  COME_FROM           176  '176'

 L. 747       196  LOAD_FAST                'kind'
              198  LOAD_STR                 'enum'
              200  COMPARE_OP               ==
              202  POP_JUMP_IF_FALSE   236  'to 236'

 L. 748       204  LOAD_FAST                'explicit_name'
              206  LOAD_STR                 '__dotdotdot__'
              208  COMPARE_OP               ==
              210  POP_JUMP_IF_FALSE   220  'to 220'

 L. 749       212  LOAD_GLOBAL              CDefError
              214  LOAD_STR                 'Enums cannot be declared with ...'
              216  CALL_FUNCTION_1       1  ''
              218  RAISE_VARARGS_1       1  'exception instance'
            220_0  COME_FROM           210  '210'

 L. 750       220  LOAD_FAST                'self'
              222  LOAD_METHOD              _build_enum_type
              224  LOAD_FAST                'explicit_name'
              226  LOAD_FAST                'type'
              228  LOAD_ATTR                values
              230  CALL_METHOD_2         2  ''
              232  STORE_FAST               'tp'
              234  JUMP_FORWARD        250  'to 250'
            236_0  COME_FROM           202  '202'

 L. 752       236  LOAD_GLOBAL              AssertionError
              238  LOAD_STR                 'kind = %r'
              240  LOAD_FAST                'kind'
              242  BUILD_TUPLE_1         1 
              244  BINARY_MODULO    
              246  CALL_FUNCTION_1       1  ''
              248  RAISE_VARARGS_1       1  'exception instance'
            250_0  COME_FROM           234  '234'
            250_1  COME_FROM           194  '194'
            250_2  COME_FROM           168  '168'

 L. 753       250  LOAD_FAST                'name'
              252  LOAD_CONST               None
              254  COMPARE_OP               is-not
          256_258  POP_JUMP_IF_FALSE   308  'to 308'

 L. 754       260  LOAD_FAST                'self'
              262  LOAD_METHOD              _declare
              264  LOAD_FAST                'key'
              266  LOAD_FAST                'tp'
              268  CALL_METHOD_2         2  ''
              270  POP_TOP          
              272  JUMP_FORWARD        308  'to 308'
            274_0  COME_FROM           140  '140'

 L. 756       274  LOAD_FAST                'kind'
              276  LOAD_STR                 'enum'
              278  COMPARE_OP               ==
          280_282  POP_JUMP_IF_FALSE   308  'to 308'
              284  LOAD_FAST                'type'
              286  LOAD_ATTR                values
              288  LOAD_CONST               None
              290  COMPARE_OP               is-not
          292_294  POP_JUMP_IF_FALSE   308  'to 308'

 L. 757       296  LOAD_GLOBAL              NotImplementedError

 L. 758       298  LOAD_STR                 "enum %s: the '{}' declaration should appear on the first time the enum is mentioned, not later"

 L. 759       300  LOAD_FAST                'explicit_name'

 L. 758       302  BINARY_MODULO    

 L. 757       304  CALL_FUNCTION_1       1  ''
              306  RAISE_VARARGS_1       1  'exception instance'
            308_0  COME_FROM           292  '292'
            308_1  COME_FROM           280  '280'
            308_2  COME_FROM           272  '272'
            308_3  COME_FROM           256  '256'

 L. 760       308  LOAD_FAST                'tp'
              310  LOAD_ATTR                forcename
          312_314  POP_JUMP_IF_TRUE    326  'to 326'

 L. 761       316  LOAD_FAST                'tp'
              318  LOAD_METHOD              force_the_name
              320  LOAD_FAST                'force_name'
              322  CALL_METHOD_1         1  ''
              324  POP_TOP          
            326_0  COME_FROM           312  '312'

 L. 762       326  LOAD_FAST                'tp'
              328  LOAD_ATTR                forcename
          330_332  POP_JUMP_IF_FALSE   364  'to 364'
              334  LOAD_STR                 '$'
              336  LOAD_FAST                'tp'
              338  LOAD_ATTR                name
              340  COMPARE_OP               in
          342_344  POP_JUMP_IF_FALSE   364  'to 364'

 L. 763       346  LOAD_FAST                'self'
              348  LOAD_METHOD              _declare
              350  LOAD_STR                 'anonymous %s'
              352  LOAD_FAST                'tp'
              354  LOAD_ATTR                forcename
              356  BINARY_MODULO    
              358  LOAD_FAST                'tp'
              360  CALL_METHOD_2         2  ''
              362  POP_TOP          
            364_0  COME_FROM           342  '342'
            364_1  COME_FROM           330  '330'

 L. 765       364  LOAD_FAST                'tp'
              366  LOAD_FAST                'self'
              368  LOAD_ATTR                _structnode2type
              370  LOAD_FAST                'type'
              372  STORE_SUBSCR     

 L. 768       374  LOAD_FAST                'kind'
              376  LOAD_STR                 'enum'
              378  COMPARE_OP               ==
          380_382  POP_JUMP_IF_FALSE   388  'to 388'

 L. 769       384  LOAD_FAST                'tp'
              386  RETURN_VALUE     
            388_0  COME_FROM           380  '380'

 L. 774       388  LOAD_FAST                'type'
              390  LOAD_ATTR                decls
              392  LOAD_CONST               None
              394  COMPARE_OP               is
          396_398  POP_JUMP_IF_FALSE   404  'to 404'

 L. 775       400  LOAD_FAST                'tp'
              402  RETURN_VALUE     
            404_0  COME_FROM           396  '396'

 L. 777       404  LOAD_FAST                'tp'
              406  LOAD_ATTR                fldnames
              408  LOAD_CONST               None
              410  COMPARE_OP               is-not
          412_414  POP_JUMP_IF_FALSE   428  'to 428'

 L. 778       416  LOAD_GLOBAL              CDefError
              418  LOAD_STR                 'duplicate declaration of struct %s'
              420  LOAD_FAST                'name'
              422  BINARY_MODULO    
              424  CALL_FUNCTION_1       1  ''
              426  RAISE_VARARGS_1       1  'exception instance'
            428_0  COME_FROM           412  '412'

 L. 779       428  BUILD_LIST_0          0 
              430  STORE_FAST               'fldnames'

 L. 780       432  BUILD_LIST_0          0 
              434  STORE_FAST               'fldtypes'

 L. 781       436  BUILD_LIST_0          0 
              438  STORE_FAST               'fldbitsize'

 L. 782       440  BUILD_LIST_0          0 
              442  STORE_FAST               'fldquals'

 L. 783       444  LOAD_FAST                'type'
              446  LOAD_ATTR                decls
              448  GET_ITER         
            450_0  COME_FROM           666  '666'
            450_1  COME_FROM           504  '504'
              450  FOR_ITER            670  'to 670'
              452  STORE_FAST               'decl'

 L. 784       454  LOAD_GLOBAL              isinstance
              456  LOAD_FAST                'decl'
              458  LOAD_ATTR                type
              460  LOAD_GLOBAL              pycparser
              462  LOAD_ATTR                c_ast
              464  LOAD_ATTR                IdentifierType
              466  CALL_FUNCTION_2       2  ''
          468_470  POP_JUMP_IF_FALSE   508  'to 508'

 L. 785       472  LOAD_STR                 ''
              474  LOAD_METHOD              join
              476  LOAD_FAST                'decl'
              478  LOAD_ATTR                type
              480  LOAD_ATTR                names
              482  CALL_METHOD_1         1  ''
              484  LOAD_STR                 '__dotdotdot__'
              486  COMPARE_OP               ==

 L. 784   488_490  POP_JUMP_IF_FALSE   508  'to 508'

 L. 789       492  LOAD_FAST                'self'
              494  LOAD_METHOD              _make_partial
              496  LOAD_FAST                'tp'
              498  LOAD_FAST                'nested'
              500  CALL_METHOD_2         2  ''
              502  POP_TOP          

 L. 790   504_506  JUMP_BACK           450  'to 450'
            508_0  COME_FROM           488  '488'
            508_1  COME_FROM           468  '468'

 L. 791       508  LOAD_FAST                'decl'
              510  LOAD_ATTR                bitsize
              512  LOAD_CONST               None
              514  COMPARE_OP               is
          516_518  POP_JUMP_IF_FALSE   526  'to 526'

 L. 792       520  LOAD_CONST               -1
              522  STORE_FAST               'bitsize'
              524  JUMP_FORWARD        538  'to 538'
            526_0  COME_FROM           516  '516'

 L. 794       526  LOAD_FAST                'self'
              528  LOAD_METHOD              _parse_constant
              530  LOAD_FAST                'decl'
              532  LOAD_ATTR                bitsize
              534  CALL_METHOD_1         1  ''
              536  STORE_FAST               'bitsize'
            538_0  COME_FROM           524  '524'

 L. 795       538  LOAD_CONST               False
              540  LOAD_FAST                'self'
              542  STORE_ATTR               _partial_length

 L. 796       544  LOAD_FAST                'self'
              546  LOAD_ATTR                _get_type_and_quals
              548  LOAD_FAST                'decl'
              550  LOAD_ATTR                type

 L. 797       552  LOAD_CONST               True

 L. 796       554  LOAD_CONST               ('partial_length_ok',)
              556  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              558  UNPACK_SEQUENCE_2     2 
              560  STORE_FAST               'type'
              562  STORE_FAST               'fqual'

 L. 798       564  LOAD_FAST                'self'
              566  LOAD_ATTR                _partial_length
          568_570  POP_JUMP_IF_FALSE   584  'to 584'

 L. 799       572  LOAD_FAST                'self'
              574  LOAD_METHOD              _make_partial
              576  LOAD_FAST                'tp'
              578  LOAD_FAST                'nested'
              580  CALL_METHOD_2         2  ''
              582  POP_TOP          
            584_0  COME_FROM           568  '568'

 L. 800       584  LOAD_GLOBAL              isinstance
              586  LOAD_FAST                'type'
              588  LOAD_GLOBAL              model
              590  LOAD_ATTR                StructType
              592  CALL_FUNCTION_2       2  ''
          594_596  POP_JUMP_IF_FALSE   618  'to 618'
              598  LOAD_FAST                'type'
              600  LOAD_ATTR                partial
          602_604  POP_JUMP_IF_FALSE   618  'to 618'

 L. 801       606  LOAD_FAST                'self'
              608  LOAD_METHOD              _make_partial
              610  LOAD_FAST                'tp'
              612  LOAD_FAST                'nested'
              614  CALL_METHOD_2         2  ''
              616  POP_TOP          
            618_0  COME_FROM           602  '602'
            618_1  COME_FROM           594  '594'

 L. 802       618  LOAD_FAST                'fldnames'
              620  LOAD_METHOD              append
              622  LOAD_FAST                'decl'
              624  LOAD_ATTR                name
          626_628  JUMP_IF_TRUE_OR_POP   632  'to 632'
              630  LOAD_STR                 ''
            632_0  COME_FROM           626  '626'
              632  CALL_METHOD_1         1  ''
              634  POP_TOP          

 L. 803       636  LOAD_FAST                'fldtypes'
              638  LOAD_METHOD              append
              640  LOAD_FAST                'type'
              642  CALL_METHOD_1         1  ''
              644  POP_TOP          

 L. 804       646  LOAD_FAST                'fldbitsize'
              648  LOAD_METHOD              append
              650  LOAD_FAST                'bitsize'
              652  CALL_METHOD_1         1  ''
              654  POP_TOP          

 L. 805       656  LOAD_FAST                'fldquals'
              658  LOAD_METHOD              append
              660  LOAD_FAST                'fqual'
              662  CALL_METHOD_1         1  ''
              664  POP_TOP          
          666_668  JUMP_BACK           450  'to 450'
            670_0  COME_FROM           450  '450'

 L. 806       670  LOAD_GLOBAL              tuple
              672  LOAD_FAST                'fldnames'
              674  CALL_FUNCTION_1       1  ''
              676  LOAD_FAST                'tp'
              678  STORE_ATTR               fldnames

 L. 807       680  LOAD_GLOBAL              tuple
              682  LOAD_FAST                'fldtypes'
              684  CALL_FUNCTION_1       1  ''
              686  LOAD_FAST                'tp'
              688  STORE_ATTR               fldtypes

 L. 808       690  LOAD_GLOBAL              tuple
              692  LOAD_FAST                'fldbitsize'
              694  CALL_FUNCTION_1       1  ''
              696  LOAD_FAST                'tp'
              698  STORE_ATTR               fldbitsize

 L. 809       700  LOAD_GLOBAL              tuple
              702  LOAD_FAST                'fldquals'
              704  CALL_FUNCTION_1       1  ''
              706  LOAD_FAST                'tp'
              708  STORE_ATTR               fldquals

 L. 810       710  LOAD_FAST                'fldbitsize'
              712  LOAD_CONST               -1
              714  BUILD_LIST_1          1 
              716  LOAD_GLOBAL              len
              718  LOAD_FAST                'fldbitsize'
              720  CALL_FUNCTION_1       1  ''
              722  BINARY_MULTIPLY  
              724  COMPARE_OP               !=
          726_728  POP_JUMP_IF_FALSE   766  'to 766'

 L. 811       730  LOAD_GLOBAL              isinstance
              732  LOAD_FAST                'tp'
              734  LOAD_GLOBAL              model
              736  LOAD_ATTR                StructType
              738  CALL_FUNCTION_2       2  ''
          740_742  POP_JUMP_IF_FALSE   766  'to 766'
              744  LOAD_FAST                'tp'
              746  LOAD_ATTR                partial
          748_750  POP_JUMP_IF_FALSE   766  'to 766'

 L. 812       752  LOAD_GLOBAL              NotImplementedError
              754  LOAD_STR                 "%s: using both bitfields and '...;'"

 L. 813       756  LOAD_FAST                'tp'
              758  BUILD_TUPLE_1         1 

 L. 812       760  BINARY_MODULO    
              762  CALL_FUNCTION_1       1  ''
              764  RAISE_VARARGS_1       1  'exception instance'
            766_0  COME_FROM           748  '748'
            766_1  COME_FROM           740  '740'
            766_2  COME_FROM           726  '726'

 L. 814       766  LOAD_FAST                'self'
              768  LOAD_ATTR                _options
              770  LOAD_METHOD              get
              772  LOAD_STR                 'packed'
              774  CALL_METHOD_1         1  ''
              776  LOAD_FAST                'tp'
              778  STORE_ATTR               packed

 L. 815       780  LOAD_FAST                'tp'
              782  LOAD_ATTR                completed
          784_786  POP_JUMP_IF_FALSE   806  'to 806'

 L. 816       788  LOAD_CONST               0
              790  LOAD_FAST                'tp'
              792  STORE_ATTR               completed

 L. 817       794  LOAD_FAST                'self'
              796  LOAD_ATTR                _recomplete
              798  LOAD_METHOD              append
              800  LOAD_FAST                'tp'
              802  CALL_METHOD_1         1  ''
              804  POP_TOP          
            806_0  COME_FROM           784  '784'

 L. 818       806  LOAD_FAST                'tp'
              808  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 32_0

            def _make_partial(self, tp, nested):
                if not isinstance(tp, model.StructOrUnion):
                    raise CDefError('%s cannot be partial' % (tp,))
                if not tp.has_c_name():
                    if not nested:
                        raise NotImplementedError('%s is partial but has no C name' % (tp,))
                tp.partial = True

            def _parse_constant(self, exprnode, partial_length_ok=False):
                if isinstance(exprnode, pycparser.c_ast.Constant):
                    s = exprnode.value
                    if '0' <= s[0] <= '9':
                        s = s.rstrip('uUlL')
                        try:
                            if s.startswith('0'):
                                return int(s, 8)
                            return int(s, 10)
                        except ValueError:
                            if len(s) > 1:
                                if s.lower()[0:2] == '0x':
                                    return int(s, 16)
                                if s.lower()[0:2] == '0b':
                                    return int(s, 2)
                        else:
                            raise CDefError('invalid constant %r' % (s,))
                    elif not s[0] == "'" or s[(-1)] == "'":
                        if len(s) == 3 or (len(s) == 4 and s[1] == '\\'):
                            return ord(s[(-2)])
                        raise CDefError('invalid constant %r' % (s,))
                if isinstance(exprnode, pycparser.c_ast.UnaryOp):
                    if exprnode.op == '+':
                        return self._parse_constant(exprnode.expr)
                if isinstance(exprnode, pycparser.c_ast.UnaryOp):
                    if exprnode.op == '-':
                        return -self._parse_constant(exprnode.expr)
                if isinstance(exprnode, pycparser.c_ast.ID):
                    if exprnode.name in self._int_constants:
                        return self._int_constants[exprnode.name]
                if isinstance(exprnode, pycparser.c_ast.ID):
                    if exprnode.name == '__dotdotdotarray__':
                        if partial_length_ok:
                            self._partial_length = True
                            return '...'
                        raise FFIError(":%d: unsupported '[...]' here, cannot derive the actual array length in this context" % exprnode.coord.line)
                if isinstance(exprnode, pycparser.c_ast.BinaryOp):
                    left = self._parse_constant(exprnode.left)
                    right = self._parse_constant(exprnode.right)
                    if exprnode.op == '+':
                        return left + right
                    if exprnode.op == '-':
                        return left - right
                    if exprnode.op == '*':
                        return left * right
                    if exprnode.op == '/':
                        return self._c_div(left, right)
                    if exprnode.op == '%':
                        return left - self._c_div(left, right) * right
                    if exprnode.op == '<<':
                        return left << right
                    if exprnode.op == '>>':
                        return left >> right
                    if exprnode.op == '&':
                        return left & right
                    if exprnode.op == '|':
                        return left | right
                    if exprnode.op == '^':
                        return left ^ right
                raise FFIError(':%d: unsupported expression: expected a simple numeric constant' % exprnode.coord.line)

            def _c_div(self, a, b):
                result = a // b
                if (a < 0) ^ (b < 0):
                    if a % b != 0:
                        result += 1
                return result

            def _build_enum_type(self, explicit_name, decls):
                if decls is not None:
                    partial = False
                    enumerators = []
                    enumvalues = []
                    nextenumvalue = 0
                    for enum in decls.enumerators:
                        if _r_enum_dotdotdot.match(enum.name):
                            partial = True
                        else:
                            if enum.value is not None:
                                nextenumvalue = self._parse_constant(enum.value)
                            enumerators.append(enum.name)
                            enumvalues.append(nextenumvalue)
                            self._add_constants(enum.name, nextenumvalue)
                            nextenumvalue += 1
                    else:
                        enumerators = tuple(enumerators)
                        enumvalues = tuple(enumvalues)
                        tp = model.EnumType(explicit_name, enumerators, enumvalues)
                        tp.partial = partial

                else:
                    tp = model.EnumType(explicit_name, (), ())
                return tp

            def include(self, other):
                for name, (tp, quals) in other._declarations.items():
                    if name.startswith('anonymous $enum_$'):
                        pass
                    else:
                        kind = name.split(' ', 1)[0]
                        if kind in ('struct', 'union', 'enum', 'anonymous', 'typedef'):
                            self._declare(name, tp, included=True, quals=quals)
                else:
                    for k, v in other._int_constants.items():
                        self._add_constants(k, v)

            def _get_unknown_type(self, decl):
                typenames = decl.type.type.names
                if typenames == ['__dotdotdot__']:
                    return model.unknown_type(decl.name)
                if typenames == ['__dotdotdotint__']:
                    if self._uses_new_feature is None:
                        self._uses_new_feature = "'typedef int... %s'" % decl.name
                    return model.UnknownIntegerType(decl.name)
                if typenames == ['__dotdotdotfloat__']:
                    if self._uses_new_feature is None:
                        self._uses_new_feature = "'typedef float... %s'" % decl.name
                    return model.UnknownFloatType(decl.name)
                raise FFIError(':%d: unsupported usage of "..." in typedef' % decl.coord.line)

            def _get_unknown_ptr_type(self, decl):
                if decl.type.type.type.names == ['__dotdotdot__']:
                    return model.unknown_ptr_type(decl.name)
                raise FFIError(':%d: unsupported usage of "..." in typedef' % decl.coord.line)