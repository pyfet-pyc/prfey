# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pycparser\c_parser.py
import re
from .ply import yacc
from . import c_ast
from .c_lexer import CLexer
from .plyparser import PLYParser, Coord, ParseError, parameterized, template
from .ast_transforms import fix_switch_cases

@template
class CParser(PLYParser):

    def __init__(self, lex_optimize=True, lexer=CLexer, lextab='pycparser.lextab', yacc_optimize=True, yacctab='pycparser.yacctab', yacc_debug=False, taboutputdir=''):
        """ Create a new CParser.

            Some arguments for controlling the debug/optimization
            level of the parser are provided. The defaults are
            tuned for release/performance mode.
            The simple rules for using them are:
            *) When tweaking CParser/CLexer, set these to False
            *) When releasing a stable parser, set to True

            lex_optimize:
                Set to False when you're modifying the lexer.
                Otherwise, changes in the lexer won't be used, if
                some lextab.py file exists.
                When releasing with a stable lexer, set to True
                to save the re-generation of the lexer table on
                each run.

            lexer:
                Set this parameter to define the lexer to use if
                you're not using the default CLexer.

            lextab:
                Points to the lex table that's used for optimized
                mode. Only if you're modifying the lexer and want
                some tests to avoid re-generating the table, make
                this point to a local lex table file (that's been
                earlier generated with lex_optimize=True)

            yacc_optimize:
                Set to False when you're modifying the parser.
                Otherwise, changes in the parser won't be used, if
                some parsetab.py file exists.
                When releasing with a stable parser, set to True
                to save the re-generation of the parser table on
                each run.

            yacctab:
                Points to the yacc table that's used for optimized
                mode. Only if you're modifying the parser, make
                this point to a local yacc table file

            yacc_debug:
                Generate a parser.out file that explains how yacc
                built the parsing table from the grammar.

            taboutputdir:
                Set this parameter to control the location of generated
                lextab and yacctab files.
        """
        self.clex = lexer(error_func=(self._lex_error_func),
          on_lbrace_func=(self._lex_on_lbrace_func),
          on_rbrace_func=(self._lex_on_rbrace_func),
          type_lookup_func=(self._lex_type_lookup_func))
        self.clex.build(optimize=lex_optimize,
          lextab=lextab,
          outputdir=taboutputdir)
        self.tokens = self.clex.tokens
        rules_with_opt = [
         'abstract_declarator',
         'assignment_expression',
         'declaration_list',
         'declaration_specifiers_no_type',
         'designation',
         'expression',
         'identifier_list',
         'init_declarator_list',
         'id_init_declarator_list',
         'initializer_list',
         'parameter_type_list',
         'block_item_list',
         'type_qualifier_list',
         'struct_declarator_list']
        for rule in rules_with_opt:
            self._create_opt_rule(rule)
        else:
            self.cparser = yacc.yacc(module=self,
              start='translation_unit_or_empty',
              debug=yacc_debug,
              optimize=yacc_optimize,
              tabmodule=yacctab,
              outputdir=taboutputdir)
            self._scope_stack = [
             dict()]
            self._last_yielded_token = None

    def parse(self, text, filename='', debuglevel=0):
        """ Parses C code and returns an AST.

            text:
                A string containing the C source code

            filename:
                Name of the file being parsed (for meaningful
                error messages)

            debuglevel:
                Debug level to yacc
        """
        self.clex.filename = filename
        self.clex.reset_lineno()
        self._scope_stack = [dict()]
        self._last_yielded_token = None
        return self.cparser.parse(input=text,
          lexer=(self.clex),
          debug=debuglevel)

    def _push_scope(self):
        self._scope_stack.append(dict())

    def _pop_scope(self):
        assert len(self._scope_stack) > 1
        self._scope_stack.pop()

    def _add_typedef_name(self, name, coord):
        """ Add a new typedef name (ie a TYPEID) to the current scope
        """
        if not self._scope_stack[(-1)].get(name, True):
            self._parse_error('Typedef %r previously declared as non-typedef in this scope' % name, coord)
        self._scope_stack[(-1)][name] = True

    def _add_identifier(self, name, coord):
        """ Add a new object, function, or enum member name (ie an ID) to the
            current scope
        """
        if self._scope_stack[(-1)].get(name, False):
            self._parse_error('Non-typedef %r previously declared as typedef in this scope' % name, coord)
        self._scope_stack[(-1)][name] = False

    def _is_type_in_scope(self, name):
        """ Is *name* a typedef-name in the current scope?
        """
        for scope in reversed(self._scope_stack):
            in_scope = scope.get(name)
            if in_scope is not None:
                return in_scope
            return False

    def _lex_error_func(self, msg, line, column):
        self._parse_error(msg, self._coord(line, column))

    def _lex_on_lbrace_func(self):
        self._push_scope()

    def _lex_on_rbrace_func(self):
        self._pop_scope()

    def _lex_type_lookup_func(self, name):
        """ Looks up types that were previously defined with
            typedef.
            Passed to the lexer for recognizing identifiers that
            are types.
        """
        is_type = self._is_type_in_scope(name)
        return is_type

    def _get_yacc_lookahead_token(self):
        """ We need access to yacc's lookahead token in certain cases.
            This is the last token yacc requested from the lexer, so we
            ask the lexer.
        """
        return self.clex.last_token

    def _type_modify_decl(self, decl, modifier):
        """ Tacks a type modifier on a declarator, and returns
            the modified declarator.

            Note: the declarator and modifier may be modified
        """
        modifier_head = modifier
        modifier_tail = modifier
        while modifier_tail.type:
            modifier_tail = modifier_tail.type

        if isinstance(decl, c_ast.TypeDecl):
            modifier_tail.type = decl
            return modifier
        else:
            decl_tail = decl
            while True:
                if not isinstance(decl_tail.type, c_ast.TypeDecl):
                    decl_tail = decl_tail.type

        modifier_tail.type = decl_tail.type
        decl_tail.type = modifier_head
        return decl

    def _fix_decl_name_type(self, decl, typename):
        """ Fixes a declaration. Modifies decl.
        """
        type = decl
        while not isinstance(type, c_ast.TypeDecl):
            type = type.type

        decl.name = type.declname
        type.quals = decl.quals
        for tn in typename:
            if not isinstance(tn, c_ast.IdentifierType):
                if len(typename) > 1:
                    self._parse_error('Invalid multiple types specified', tn.coord)
                else:
                    type.type = tn
                    return decl
            if not typename:
                if not isinstance(decl.type, c_ast.FuncDecl):
                    self._parse_error('Missing type in declaration', decl.coord)
                type.type = c_ast.IdentifierType([
                 'int'],
                  coord=(decl.coord))
            else:
                type.type = c_ast.IdentifierType([name for id in typename for name in id.names],
                  coord=(typename[0].coord))
            return decl

    def _add_declaration_specifier(self, declspec, newspec, kind, append=False):
        """ Declaration specifiers are represented by a dictionary
            with the entries:
            * qual: a list of type qualifiers
            * storage: a list of storage type qualifiers
            * type: a list of type specifiers
            * function: a list of function specifiers

            This method is given a declaration specifier, and a
            new specifier of a given kind.
            If `append` is True, the new specifier is added to the end of
            the specifiers list, otherwise it's added at the beginning.
            Returns the declaration specifier, with the new
            specifier incorporated.
        """
        spec = declspec or dict(qual=[], storage=[], type=[], function=[])
        if append:
            spec[kind].append(newspec)
        else:
            spec[kind].insert(0, newspec)
        return spec

    def _build_declarations--- This code section failed: ---

 L. 381         0  LOAD_STR                 'typedef'
                2  LOAD_FAST                'spec'
                4  LOAD_STR                 'storage'
                6  BINARY_SUBSCR    
                8  COMPARE_OP               in
               10  STORE_FAST               'is_typedef'

 L. 382        12  BUILD_LIST_0          0 
               14  STORE_FAST               'declarations'

 L. 386        16  LOAD_FAST                'decls'
               18  LOAD_CONST               0
               20  BINARY_SUBSCR    
               22  LOAD_METHOD              get
               24  LOAD_STR                 'bitsize'
               26  CALL_METHOD_1         1  ''
               28  LOAD_CONST               None
               30  COMPARE_OP               is-not
               32  POP_JUMP_IF_FALSE    38  'to 38'

 L. 387     34_36  JUMP_FORWARD        338  'to 338'
             38_0  COME_FROM            32  '32'

 L. 394        38  LOAD_FAST                'decls'
               40  LOAD_CONST               0
               42  BINARY_SUBSCR    
               44  LOAD_STR                 'decl'
               46  BINARY_SUBSCR    
               48  LOAD_CONST               None
               50  COMPARE_OP               is
               52  POP_JUMP_IF_FALSE   228  'to 228'

 L. 395        54  LOAD_GLOBAL              len
               56  LOAD_FAST                'spec'
               58  LOAD_STR                 'type'
               60  BINARY_SUBSCR    
               62  CALL_FUNCTION_1       1  ''
               64  LOAD_CONST               2
               66  COMPARE_OP               <
               68  POP_JUMP_IF_TRUE    116  'to 116'
               70  LOAD_GLOBAL              len
               72  LOAD_FAST                'spec'
               74  LOAD_STR                 'type'
               76  BINARY_SUBSCR    
               78  LOAD_CONST               -1
               80  BINARY_SUBSCR    
               82  LOAD_ATTR                names
               84  CALL_FUNCTION_1       1  ''
               86  LOAD_CONST               1
               88  COMPARE_OP               !=
               90  POP_JUMP_IF_TRUE    116  'to 116'

 L. 396        92  LOAD_FAST                'self'
               94  LOAD_METHOD              _is_type_in_scope
               96  LOAD_FAST                'spec'
               98  LOAD_STR                 'type'
              100  BINARY_SUBSCR    
              102  LOAD_CONST               -1
              104  BINARY_SUBSCR    
              106  LOAD_ATTR                names
              108  LOAD_CONST               0
              110  BINARY_SUBSCR    
              112  CALL_METHOD_1         1  ''

 L. 395       114  POP_JUMP_IF_TRUE    166  'to 166'
            116_0  COME_FROM            90  '90'
            116_1  COME_FROM            68  '68'

 L. 397       116  LOAD_STR                 '?'
              118  STORE_FAST               'coord'

 L. 398       120  LOAD_FAST                'spec'
              122  LOAD_STR                 'type'
              124  BINARY_SUBSCR    
              126  GET_ITER         
            128_0  COME_FROM           140  '140'
              128  FOR_ITER            154  'to 154'
              130  STORE_FAST               't'

 L. 399       132  LOAD_GLOBAL              hasattr
              134  LOAD_FAST                't'
              136  LOAD_STR                 'coord'
              138  CALL_FUNCTION_2       2  ''
              140  POP_JUMP_IF_FALSE   128  'to 128'

 L. 400       142  LOAD_FAST                't'
              144  LOAD_ATTR                coord
              146  STORE_FAST               'coord'

 L. 401       148  POP_TOP          
              150  BREAK_LOOP          154  'to 154'
              152  JUMP_BACK           128  'to 128'

 L. 402       154  LOAD_FAST                'self'
              156  LOAD_METHOD              _parse_error
              158  LOAD_STR                 'Invalid declaration'
              160  LOAD_FAST                'coord'
              162  CALL_METHOD_2         2  ''
              164  POP_TOP          
            166_0  COME_FROM           114  '114'

 L. 405       166  LOAD_GLOBAL              c_ast
              168  LOAD_ATTR                TypeDecl

 L. 406       170  LOAD_FAST                'spec'
              172  LOAD_STR                 'type'
              174  BINARY_SUBSCR    
              176  LOAD_CONST               -1
              178  BINARY_SUBSCR    
              180  LOAD_ATTR                names
              182  LOAD_CONST               0
              184  BINARY_SUBSCR    

 L. 407       186  LOAD_CONST               None

 L. 408       188  LOAD_CONST               None

 L. 409       190  LOAD_FAST                'spec'
              192  LOAD_STR                 'type'
              194  BINARY_SUBSCR    
              196  LOAD_CONST               -1
              198  BINARY_SUBSCR    
              200  LOAD_ATTR                coord

 L. 405       202  LOAD_CONST               ('declname', 'type', 'quals', 'coord')
              204  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              206  LOAD_FAST                'decls'
              208  LOAD_CONST               0
              210  BINARY_SUBSCR    
              212  LOAD_STR                 'decl'
              214  STORE_SUBSCR     

 L. 411       216  LOAD_FAST                'spec'
              218  LOAD_STR                 'type'
              220  BINARY_SUBSCR    
              222  LOAD_CONST               -1
              224  DELETE_SUBSCR    
              226  JUMP_FORWARD        338  'to 338'
            228_0  COME_FROM            52  '52'

 L. 416       228  LOAD_GLOBAL              isinstance
              230  LOAD_FAST                'decls'
              232  LOAD_CONST               0
              234  BINARY_SUBSCR    
              236  LOAD_STR                 'decl'
              238  BINARY_SUBSCR    

 L. 417       240  LOAD_GLOBAL              c_ast
              242  LOAD_ATTR                Struct
              244  LOAD_GLOBAL              c_ast
              246  LOAD_ATTR                Union
              248  LOAD_GLOBAL              c_ast
              250  LOAD_ATTR                IdentifierType
              252  BUILD_TUPLE_3         3 

 L. 416       254  CALL_FUNCTION_2       2  ''
          256_258  POP_JUMP_IF_TRUE    338  'to 338'

 L. 418       260  LOAD_FAST                'decls'
              262  LOAD_CONST               0
              264  BINARY_SUBSCR    
              266  LOAD_STR                 'decl'
              268  BINARY_SUBSCR    
              270  STORE_FAST               'decls_0_tail'

 L. 419       272  LOAD_GLOBAL              isinstance
              274  LOAD_FAST                'decls_0_tail'
              276  LOAD_GLOBAL              c_ast
              278  LOAD_ATTR                TypeDecl
              280  CALL_FUNCTION_2       2  ''
          282_284  POP_JUMP_IF_TRUE    296  'to 296'

 L. 420       286  LOAD_FAST                'decls_0_tail'
              288  LOAD_ATTR                type
              290  STORE_FAST               'decls_0_tail'
          292_294  JUMP_BACK           272  'to 272'
            296_0  COME_FROM           282  '282'

 L. 421       296  LOAD_FAST                'decls_0_tail'
              298  LOAD_ATTR                declname
              300  LOAD_CONST               None
              302  COMPARE_OP               is
          304_306  POP_JUMP_IF_FALSE   338  'to 338'

 L. 422       308  LOAD_FAST                'spec'
              310  LOAD_STR                 'type'
              312  BINARY_SUBSCR    
              314  LOAD_CONST               -1
              316  BINARY_SUBSCR    
              318  LOAD_ATTR                names
              320  LOAD_CONST               0
              322  BINARY_SUBSCR    
              324  LOAD_FAST                'decls_0_tail'
              326  STORE_ATTR               declname

 L. 423       328  LOAD_FAST                'spec'
              330  LOAD_STR                 'type'
              332  BINARY_SUBSCR    
              334  LOAD_CONST               -1
              336  DELETE_SUBSCR    
            338_0  COME_FROM           304  '304'
            338_1  COME_FROM           256  '256'
            338_2  COME_FROM           226  '226'
            338_3  COME_FROM            34  '34'

 L. 425       338  LOAD_FAST                'decls'
              340  GET_ITER         
              342  FOR_ITER            578  'to 578'
              344  STORE_FAST               'decl'

 L. 426       346  LOAD_FAST                'decl'
              348  LOAD_STR                 'decl'
              350  BINARY_SUBSCR    
              352  LOAD_CONST               None
              354  COMPARE_OP               is-not
          356_358  POP_JUMP_IF_TRUE    364  'to 364'
              360  LOAD_ASSERT              AssertionError
              362  RAISE_VARARGS_1       1  'exception instance'
            364_0  COME_FROM           356  '356'

 L. 427       364  LOAD_FAST                'is_typedef'
          366_368  POP_JUMP_IF_FALSE   410  'to 410'

 L. 428       370  LOAD_GLOBAL              c_ast
              372  LOAD_ATTR                Typedef

 L. 429       374  LOAD_CONST               None

 L. 430       376  LOAD_FAST                'spec'
              378  LOAD_STR                 'qual'
              380  BINARY_SUBSCR    

 L. 431       382  LOAD_FAST                'spec'
              384  LOAD_STR                 'storage'
              386  BINARY_SUBSCR    

 L. 432       388  LOAD_FAST                'decl'
              390  LOAD_STR                 'decl'
              392  BINARY_SUBSCR    

 L. 433       394  LOAD_FAST                'decl'
              396  LOAD_STR                 'decl'
              398  BINARY_SUBSCR    
              400  LOAD_ATTR                coord

 L. 428       402  LOAD_CONST               ('name', 'quals', 'storage', 'type', 'coord')
              404  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              406  STORE_FAST               'declaration'
              408  JUMP_FORWARD        470  'to 470'
            410_0  COME_FROM           366  '366'

 L. 435       410  LOAD_GLOBAL              c_ast
              412  LOAD_ATTR                Decl

 L. 436       414  LOAD_CONST               None

 L. 437       416  LOAD_FAST                'spec'
              418  LOAD_STR                 'qual'
              420  BINARY_SUBSCR    

 L. 438       422  LOAD_FAST                'spec'
              424  LOAD_STR                 'storage'
              426  BINARY_SUBSCR    

 L. 439       428  LOAD_FAST                'spec'
              430  LOAD_STR                 'function'
              432  BINARY_SUBSCR    

 L. 440       434  LOAD_FAST                'decl'
              436  LOAD_STR                 'decl'
              438  BINARY_SUBSCR    

 L. 441       440  LOAD_FAST                'decl'
              442  LOAD_METHOD              get
              444  LOAD_STR                 'init'
              446  CALL_METHOD_1         1  ''

 L. 442       448  LOAD_FAST                'decl'
              450  LOAD_METHOD              get
              452  LOAD_STR                 'bitsize'
              454  CALL_METHOD_1         1  ''

 L. 443       456  LOAD_FAST                'decl'
              458  LOAD_STR                 'decl'
              460  BINARY_SUBSCR    
              462  LOAD_ATTR                coord

 L. 435       464  LOAD_CONST               ('name', 'quals', 'storage', 'funcspec', 'type', 'init', 'bitsize', 'coord')
              466  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
              468  STORE_FAST               'declaration'
            470_0  COME_FROM           408  '408'

 L. 445       470  LOAD_GLOBAL              isinstance
              472  LOAD_FAST                'declaration'
              474  LOAD_ATTR                type

 L. 446       476  LOAD_GLOBAL              c_ast
              478  LOAD_ATTR                Struct
              480  LOAD_GLOBAL              c_ast
              482  LOAD_ATTR                Union
              484  LOAD_GLOBAL              c_ast
              486  LOAD_ATTR                IdentifierType
              488  BUILD_TUPLE_3         3 

 L. 445       490  CALL_FUNCTION_2       2  ''
          492_494  POP_JUMP_IF_FALSE   502  'to 502'

 L. 447       496  LOAD_FAST                'declaration'
              498  STORE_FAST               'fixed_decl'
              500  JUMP_FORWARD        518  'to 518'
            502_0  COME_FROM           492  '492'

 L. 449       502  LOAD_FAST                'self'
              504  LOAD_METHOD              _fix_decl_name_type
              506  LOAD_FAST                'declaration'
              508  LOAD_FAST                'spec'
              510  LOAD_STR                 'type'
              512  BINARY_SUBSCR    
              514  CALL_METHOD_2         2  ''
              516  STORE_FAST               'fixed_decl'
            518_0  COME_FROM           500  '500'

 L. 454       518  LOAD_FAST                'typedef_namespace'
          520_522  POP_JUMP_IF_FALSE   564  'to 564'

 L. 455       524  LOAD_FAST                'is_typedef'
          526_528  POP_JUMP_IF_FALSE   548  'to 548'

 L. 456       530  LOAD_FAST                'self'
              532  LOAD_METHOD              _add_typedef_name
              534  LOAD_FAST                'fixed_decl'
              536  LOAD_ATTR                name
              538  LOAD_FAST                'fixed_decl'
              540  LOAD_ATTR                coord
              542  CALL_METHOD_2         2  ''
              544  POP_TOP          
              546  JUMP_FORWARD        564  'to 564'
            548_0  COME_FROM           526  '526'

 L. 458       548  LOAD_FAST                'self'
              550  LOAD_METHOD              _add_identifier
              552  LOAD_FAST                'fixed_decl'
              554  LOAD_ATTR                name
              556  LOAD_FAST                'fixed_decl'
              558  LOAD_ATTR                coord
              560  CALL_METHOD_2         2  ''
              562  POP_TOP          
            564_0  COME_FROM           546  '546'
            564_1  COME_FROM           520  '520'

 L. 460       564  LOAD_FAST                'declarations'
              566  LOAD_METHOD              append
              568  LOAD_FAST                'fixed_decl'
              570  CALL_METHOD_1         1  ''
              572  POP_TOP          
          574_576  JUMP_BACK           342  'to 342'

 L. 462       578  LOAD_FAST                'declarations'
              580  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 226

    def _build_function_definition(self, spec, decl, param_decls, body):
        """ Builds a function definition.
        """
        assert 'typedef' not in spec['storage']
        declaration = self._build_declarations(spec=spec,
          decls=[
         dict(decl=decl, init=None)],
          typedef_namespace=True)[0]
        return c_ast.FuncDef(decl=declaration,
          param_decls=param_decls,
          body=body,
          coord=(decl.coord))

    def _select_struct_union_class(self, token):
        """ Given a token (either STRUCT or UNION), selects the
            appropriate AST class.
        """
        if token == 'struct':
            return c_ast.Struct
        return c_ast.Union

    precedence = (('left', 'LOR'), ('left', 'LAND'), ('left', 'OR'), ('left', 'XOR'),
                  ('left', 'AND'), ('left', 'EQ', 'NE'), ('left', 'GT', 'GE', 'LT', 'LE'),
                  ('left', 'RSHIFT', 'LSHIFT'), ('left', 'PLUS', 'MINUS'), ('left', 'TIMES', 'DIVIDE', 'MOD'))

    def p_translation_unit_or_empty(self, p):
        """ translation_unit_or_empty   : translation_unit
                                        | empty
        """
        if p[1] is None:
            p[0] = c_ast.FileAST([])
        else:
            p[0] = c_ast.FileAST(p[1])

    def p_translation_unit_1(self, p):
        """ translation_unit    : external_declaration
        """
        p[0] = p[1]

    def p_translation_unit_2(self, p):
        """ translation_unit    : translation_unit external_declaration
        """
        if p[2] is not None:
            p[1].extend(p[2])
        p[0] = p[1]

    def p_external_declaration_1(self, p):
        """ external_declaration    : function_definition
        """
        p[0] = [
         p[1]]

    def p_external_declaration_2(self, p):
        """ external_declaration    : declaration
        """
        p[0] = p[1]

    def p_external_declaration_3(self, p):
        """ external_declaration    : pp_directive
                                    | pppragma_directive
        """
        p[0] = [
         p[1]]

    def p_external_declaration_4(self, p):
        """ external_declaration    : SEMI
        """
        p[0] = None

    def p_pp_directive(self, p):
        """ pp_directive  : PPHASH
        """
        self._parse_error('Directives not supported yet', self._token_coord(p, 1))

    def p_pppragma_directive(self, p):
        """ pppragma_directive      : PPPRAGMA
                                    | PPPRAGMA PPPRAGMASTR
        """
        if len(p) == 3:
            p[0] = c_ast.Pragma(p[2], self._token_coord(p, 2))
        else:
            p[0] = c_ast.Pragma('', self._token_coord(p, 1))

    def p_function_definition_1(self, p):
        """ function_definition : id_declarator declaration_list_opt compound_statement
        """
        spec = dict(qual=[], storage=[], type=[
         c_ast.IdentifierType(['int'], coord=(self._token_coord(p, 1)))],
          function=[])
        p[0] = self._build_function_definition(spec=spec,
          decl=(p[1]),
          param_decls=(p[2]),
          body=(p[3]))

    def p_function_definition_2(self, p):
        """ function_definition : declaration_specifiers id_declarator declaration_list_opt compound_statement
        """
        spec = p[1]
        p[0] = self._build_function_definition(spec=spec,
          decl=(p[2]),
          param_decls=(p[3]),
          body=(p[4]))

    def p_statement(self, p):
        """ statement   : labeled_statement
                        | expression_statement
                        | compound_statement
                        | selection_statement
                        | iteration_statement
                        | jump_statement
                        | pppragma_directive
        """
        p[0] = p[1]

    def p_pragmacomp_or_statement(self, p):
        """ pragmacomp_or_statement     : pppragma_directive statement
                                        | statement
        """
        if isinstance(p[1], c_ast.Pragma) and len(p) == 3:
            p[0] = c_ast.Compound(block_items=[
             p[1], p[2]],
              coord=(self._token_coord(p, 1)))
        else:
            p[0] = p[1]

    def p_decl_body(self, p):
        """ decl_body : declaration_specifiers init_declarator_list_opt
                      | declaration_specifiers_no_type id_init_declarator_list_opt
        """
        spec = p[1]
        if p[2] is None:
            ty = spec['type']
            s_u_or_e = (c_ast.Struct, c_ast.Union, c_ast.Enum)
            if len(ty) == 1 and isinstance(ty[0], s_u_or_e):
                decls = [
                 c_ast.Decl(name=None,
                   quals=(spec['qual']),
                   storage=(spec['storage']),
                   funcspec=(spec['function']),
                   type=(ty[0]),
                   init=None,
                   bitsize=None,
                   coord=(ty[0].coord))]
            else:
                decls = self._build_declarations(spec=spec,
                  decls=[
                 dict(decl=None, init=None)],
                  typedef_namespace=True)
        else:
            decls = self._build_declarations(spec=spec,
              decls=(p[2]),
              typedef_namespace=True)
        p[0] = decls

    def p_declaration(self, p):
        """ declaration : decl_body SEMI
        """
        p[0] = p[1]

    def p_declaration_list(self, p):
        """ declaration_list    : declaration
                                | declaration_list declaration
        """
        p[0] = p[1] if len(p) == 2 else p[1] + p[2]

    def p_declaration_specifiers_no_type_1(self, p):
        """ declaration_specifiers_no_type  : type_qualifier declaration_specifiers_no_type_opt
        """
        p[0] = self._add_declaration_specifier(p[2], p[1], 'qual')

    def p_declaration_specifiers_no_type_2(self, p):
        """ declaration_specifiers_no_type  : storage_class_specifier declaration_specifiers_no_type_opt
        """
        p[0] = self._add_declaration_specifier(p[2], p[1], 'storage')

    def p_declaration_specifiers_no_type_3(self, p):
        """ declaration_specifiers_no_type  : function_specifier declaration_specifiers_no_type_opt
        """
        p[0] = self._add_declaration_specifier(p[2], p[1], 'function')

    def p_declaration_specifiers_1(self, p):
        """ declaration_specifiers  : declaration_specifiers type_qualifier
        """
        p[0] = self._add_declaration_specifier((p[1]), (p[2]), 'qual', append=True)

    def p_declaration_specifiers_2(self, p):
        """ declaration_specifiers  : declaration_specifiers storage_class_specifier
        """
        p[0] = self._add_declaration_specifier((p[1]), (p[2]), 'storage', append=True)

    def p_declaration_specifiers_3(self, p):
        """ declaration_specifiers  : declaration_specifiers function_specifier
        """
        p[0] = self._add_declaration_specifier((p[1]), (p[2]), 'function', append=True)

    def p_declaration_specifiers_4(self, p):
        """ declaration_specifiers  : declaration_specifiers type_specifier_no_typeid
        """
        p[0] = self._add_declaration_specifier((p[1]), (p[2]), 'type', append=True)

    def p_declaration_specifiers_5(self, p):
        """ declaration_specifiers  : type_specifier
        """
        p[0] = self._add_declaration_specifier(None, p[1], 'type')

    def p_declaration_specifiers_6(self, p):
        """ declaration_specifiers  : declaration_specifiers_no_type type_specifier
        """
        p[0] = self._add_declaration_specifier((p[1]), (p[2]), 'type', append=True)

    def p_storage_class_specifier(self, p):
        """ storage_class_specifier : AUTO
                                    | REGISTER
                                    | STATIC
                                    | EXTERN
                                    | TYPEDEF
        """
        p[0] = p[1]

    def p_function_specifier(self, p):
        """ function_specifier  : INLINE
        """
        p[0] = p[1]

    def p_type_specifier_no_typeid(self, p):
        """ type_specifier_no_typeid  : VOID
                                      | _BOOL
                                      | CHAR
                                      | SHORT
                                      | INT
                                      | LONG
                                      | FLOAT
                                      | DOUBLE
                                      | _COMPLEX
                                      | SIGNED
                                      | UNSIGNED
                                      | __INT128
        """
        p[0] = c_ast.IdentifierType([p[1]], coord=(self._token_coord(p, 1)))

    def p_type_specifier(self, p):
        """ type_specifier  : typedef_name
                            | enum_specifier
                            | struct_or_union_specifier
                            | type_specifier_no_typeid
        """
        p[0] = p[1]

    def p_type_qualifier(self, p):
        """ type_qualifier  : CONST
                            | RESTRICT
                            | VOLATILE
        """
        p[0] = p[1]

    def p_init_declarator_list(self, p):
        """ init_declarator_list    : init_declarator
                                    | init_declarator_list COMMA init_declarator
        """
        p[0] = p[1] + [p[3]] if len(p) == 4 else [p[1]]

    def p_init_declarator(self, p):
        """ init_declarator : declarator
                            | declarator EQUALS initializer
        """
        p[0] = dict(decl=(p[1]), init=(p[3] if len(p) > 2 else None))

    def p_id_init_declarator_list(self, p):
        """ id_init_declarator_list    : id_init_declarator
                                       | id_init_declarator_list COMMA init_declarator
        """
        p[0] = p[1] + [p[3]] if len(p) == 4 else [p[1]]

    def p_id_init_declarator(self, p):
        """ id_init_declarator : id_declarator
                               | id_declarator EQUALS initializer
        """
        p[0] = dict(decl=(p[1]), init=(p[3] if len(p) > 2 else None))

    def p_specifier_qualifier_list_1(self, p):
        """ specifier_qualifier_list    : specifier_qualifier_list type_specifier_no_typeid
        """
        p[0] = self._add_declaration_specifier((p[1]), (p[2]), 'type', append=True)

    def p_specifier_qualifier_list_2(self, p):
        """ specifier_qualifier_list    : specifier_qualifier_list type_qualifier
        """
        p[0] = self._add_declaration_specifier((p[1]), (p[2]), 'qual', append=True)

    def p_specifier_qualifier_list_3(self, p):
        """ specifier_qualifier_list  : type_specifier
        """
        p[0] = self._add_declaration_specifier(None, p[1], 'type')

    def p_specifier_qualifier_list_4(self, p):
        """ specifier_qualifier_list  : type_qualifier_list type_specifier
        """
        spec = dict(qual=(p[1]), storage=[], type=[], function=[])
        p[0] = self._add_declaration_specifier(spec, (p[2]), 'type', append=True)

    def p_struct_or_union_specifier_1(self, p):
        """ struct_or_union_specifier   : struct_or_union ID
                                        | struct_or_union TYPEID
        """
        klass = self._select_struct_union_class(p[1])
        p[0] = klass(name=(p[2]),
          decls=None,
          coord=(self._token_coord(p, 2)))

    def p_struct_or_union_specifier_2(self, p):
        """ struct_or_union_specifier : struct_or_union brace_open struct_declaration_list brace_close
                                      | struct_or_union brace_open brace_close
        """
        klass = self._select_struct_union_class(p[1])
        if len(p) == 4:
            p[0] = klass(name=None,
              decls=[],
              coord=(self._token_coord(p, 2)))
        else:
            p[0] = klass(name=None,
              decls=(p[3]),
              coord=(self._token_coord(p, 2)))

    def p_struct_or_union_specifier_3(self, p):
        """ struct_or_union_specifier   : struct_or_union ID brace_open struct_declaration_list brace_close
                                        | struct_or_union ID brace_open brace_close
                                        | struct_or_union TYPEID brace_open struct_declaration_list brace_close
                                        | struct_or_union TYPEID brace_open brace_close
        """
        klass = self._select_struct_union_class(p[1])
        if len(p) == 5:
            p[0] = klass(name=(p[2]),
              decls=[],
              coord=(self._token_coord(p, 2)))
        else:
            p[0] = klass(name=(p[2]),
              decls=(p[4]),
              coord=(self._token_coord(p, 2)))

    def p_struct_or_union(self, p):
        """ struct_or_union : STRUCT
                            | UNION
        """
        p[0] = p[1]

    def p_struct_declaration_list(self, p):
        """ struct_declaration_list     : struct_declaration
                                        | struct_declaration_list struct_declaration
        """
        if len(p) == 2:
            p[0] = p[1] or []
        else:
            p[0] = p[1] + (p[2] or [])

    def p_struct_declaration_1(self, p):
        """ struct_declaration : specifier_qualifier_list struct_declarator_list_opt SEMI
        """
        spec = p[1]
        if not 'typedef' not in spec['storage']:
            raise AssertionError
        elif p[2] is not None:
            decls = self._build_declarations(spec=spec,
              decls=(p[2]))
        else:
            if len(spec['type']) == 1:
                node = spec['type'][0]
                if isinstance(node, c_ast.Node):
                    decl_type = node
                else:
                    decl_type = c_ast.IdentifierType(node)
                decls = self._build_declarations(spec=spec,
                  decls=[
                 dict(decl=decl_type)])
            else:
                decls = self._build_declarations(spec=spec,
                  decls=[
                 dict(decl=None, init=None)])
        p[0] = decls

    def p_struct_declaration_2(self, p):
        """ struct_declaration : SEMI
        """
        p[0] = None

    def p_struct_declaration_3(self, p):
        """ struct_declaration : pppragma_directive
        """
        p[0] = [
         p[1]]

    def p_struct_declarator_list(self, p):
        """ struct_declarator_list  : struct_declarator
                                    | struct_declarator_list COMMA struct_declarator
        """
        p[0] = p[1] + [p[3]] if len(p) == 4 else [p[1]]

    def p_struct_declarator_1(self, p):
        """ struct_declarator : declarator
        """
        p[0] = {'decl':p[1], 
         'bitsize':None}

    def p_struct_declarator_2(self, p):
        """ struct_declarator   : declarator COLON constant_expression
                                | COLON constant_expression
        """
        if len(p) > 3:
            p[0] = {'decl':p[1], 
             'bitsize':p[3]}
        else:
            p[0] = {'decl':c_ast.TypeDecl(None, None, None), 
             'bitsize':p[2]}

    def p_enum_specifier_1(self, p):
        """ enum_specifier  : ENUM ID
                            | ENUM TYPEID
        """
        p[0] = c_ast.Enum(p[2], None, self._token_coord(p, 1))

    def p_enum_specifier_2(self, p):
        """ enum_specifier  : ENUM brace_open enumerator_list brace_close
        """
        p[0] = c_ast.Enum(None, p[3], self._token_coord(p, 1))

    def p_enum_specifier_3(self, p):
        """ enum_specifier  : ENUM ID brace_open enumerator_list brace_close
                            | ENUM TYPEID brace_open enumerator_list brace_close
        """
        p[0] = c_ast.Enum(p[2], p[4], self._token_coord(p, 1))

    def p_enumerator_list(self, p):
        """ enumerator_list : enumerator
                            | enumerator_list COMMA
                            | enumerator_list COMMA enumerator
        """
        if len(p) == 2:
            p[0] = c_ast.EnumeratorList([p[1]], p[1].coord)
        else:
            if len(p) == 3:
                p[0] = p[1]
            else:
                p[1].enumerators.append(p[3])
                p[0] = p[1]

    def p_enumerator(self, p):
        """ enumerator  : ID
                        | ID EQUALS constant_expression
        """
        if len(p) == 2:
            enumerator = c_ast.Enumerator(p[1], None, self._token_coord(p, 1))
        else:
            enumerator = c_ast.Enumerator(p[1], p[3], self._token_coord(p, 1))
        self._add_identifier(enumerator.name, enumerator.coord)
        p[0] = enumerator

    def p_declarator(self, p):
        """ declarator  : id_declarator
                        | typeid_declarator
        """
        p[0] = p[1]

    @parameterized(('id', 'ID'), ('typeid', 'TYPEID'), ('typeid_noparen', 'TYPEID'))
    def p_xxx_declarator_1(self, p):
        """ xxx_declarator  : direct_xxx_declarator
        """
        p[0] = p[1]

    @parameterized(('id', 'ID'), ('typeid', 'TYPEID'), ('typeid_noparen', 'TYPEID'))
    def p_xxx_declarator_2(self, p):
        """ xxx_declarator  : pointer direct_xxx_declarator
        """
        p[0] = self._type_modify_decl(p[2], p[1])

    @parameterized(('id', 'ID'), ('typeid', 'TYPEID'), ('typeid_noparen', 'TYPEID'))
    def p_direct_xxx_declarator_1(self, p):
        """ direct_xxx_declarator   : yyy
        """
        p[0] = c_ast.TypeDecl(declname=(p[1]),
          type=None,
          quals=None,
          coord=(self._token_coord(p, 1)))

    @parameterized(('id', 'ID'), ('typeid', 'TYPEID'))
    def p_direct_xxx_declarator_2(self, p):
        """ direct_xxx_declarator   : LPAREN xxx_declarator RPAREN
        """
        p[0] = p[2]

    @parameterized(('id', 'ID'), ('typeid', 'TYPEID'), ('typeid_noparen', 'TYPEID'))
    def p_direct_xxx_declarator_3(self, p):
        """ direct_xxx_declarator   : direct_xxx_declarator LBRACKET type_qualifier_list_opt assignment_expression_opt RBRACKET
        """
        quals = (p[3] if len(p) > 5 else []) or []
        arr = c_ast.ArrayDecl(type=None,
          dim=(p[4] if len(p) > 5 else p[3]),
          dim_quals=quals,
          coord=(p[1].coord))
        p[0] = self._type_modify_decl(decl=(p[1]), modifier=arr)

    @parameterized(('id', 'ID'), ('typeid', 'TYPEID'), ('typeid_noparen', 'TYPEID'))
    def p_direct_xxx_declarator_4(self, p):
        """ direct_xxx_declarator   : direct_xxx_declarator LBRACKET STATIC type_qualifier_list_opt assignment_expression RBRACKET
                                    | direct_xxx_declarator LBRACKET type_qualifier_list STATIC assignment_expression RBRACKET
        """
        listed_quals = [item if isinstance(item, list) else [item] for item in (p[3], p[4])]
        dim_quals = [qual for sublist in listed_quals for qual in sublist if qual is not None]
        arr = c_ast.ArrayDecl(type=None,
          dim=(p[5]),
          dim_quals=dim_quals,
          coord=(p[1].coord))
        p[0] = self._type_modify_decl(decl=(p[1]), modifier=arr)

    @parameterized(('id', 'ID'), ('typeid', 'TYPEID'), ('typeid_noparen', 'TYPEID'))
    def p_direct_xxx_declarator_5(self, p):
        """ direct_xxx_declarator   : direct_xxx_declarator LBRACKET type_qualifier_list_opt TIMES RBRACKET
        """
        arr = c_ast.ArrayDecl(type=None,
          dim=(c_ast.ID(p[4], self._token_coord(p, 4))),
          dim_quals=(p[3] if p[3] != None else []),
          coord=(p[1].coord))
        p[0] = self._type_modify_decl(decl=(p[1]), modifier=arr)

    @parameterized(('id', 'ID'), ('typeid', 'TYPEID'), ('typeid_noparen', 'TYPEID'))
    def p_direct_xxx_declarator_6--- This code section failed: ---

 L.1176         0  LOAD_GLOBAL              c_ast
                2  LOAD_ATTR                FuncDecl

 L.1177         4  LOAD_FAST                'p'
                6  LOAD_CONST               3
                8  BINARY_SUBSCR    

 L.1178        10  LOAD_CONST               None

 L.1179        12  LOAD_FAST                'p'
               14  LOAD_CONST               1
               16  BINARY_SUBSCR    
               18  LOAD_ATTR                coord

 L.1176        20  LOAD_CONST               ('args', 'type', 'coord')
               22  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               24  STORE_FAST               'func'

 L.1192        26  LOAD_FAST                'self'
               28  LOAD_METHOD              _get_yacc_lookahead_token
               30  CALL_METHOD_0         0  ''
               32  LOAD_ATTR                type
               34  LOAD_STR                 'LBRACE'
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE    96  'to 96'

 L.1193        40  LOAD_FAST                'func'
               42  LOAD_ATTR                args
               44  LOAD_CONST               None
               46  COMPARE_OP               is-not
               48  POP_JUMP_IF_FALSE    96  'to 96'

 L.1194        50  LOAD_FAST                'func'
               52  LOAD_ATTR                args
               54  LOAD_ATTR                params
               56  GET_ITER         
               58  FOR_ITER             96  'to 96'
               60  STORE_FAST               'param'

 L.1195        62  LOAD_GLOBAL              isinstance
               64  LOAD_FAST                'param'
               66  LOAD_GLOBAL              c_ast
               68  LOAD_ATTR                EllipsisParam
               70  CALL_FUNCTION_2       2  ''
               72  POP_JUMP_IF_FALSE    78  'to 78'

 L.1195        74  POP_TOP          
               76  JUMP_ABSOLUTE        96  'to 96'
             78_0  COME_FROM            72  '72'

 L.1196        78  LOAD_FAST                'self'
               80  LOAD_METHOD              _add_identifier
               82  LOAD_FAST                'param'
               84  LOAD_ATTR                name
               86  LOAD_FAST                'param'
               88  LOAD_ATTR                coord
               90  CALL_METHOD_2         2  ''
               92  POP_TOP          
               94  JUMP_BACK            58  'to 58'
             96_0  COME_FROM            48  '48'
             96_1  COME_FROM            38  '38'

 L.1198        96  LOAD_FAST                'self'
               98  LOAD_ATTR                _type_modify_decl
              100  LOAD_FAST                'p'
              102  LOAD_CONST               1
              104  BINARY_SUBSCR    
              106  LOAD_FAST                'func'
              108  LOAD_CONST               ('decl', 'modifier')
              110  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              112  LOAD_FAST                'p'
              114  LOAD_CONST               0
              116  STORE_SUBSCR     

Parse error at or near `LOAD_CONST' instruction at offset 114

    def p_pointer(self, p):
        """ pointer : TIMES type_qualifier_list_opt
                    | TIMES type_qualifier_list_opt pointer
        """
        coord = self._token_coord(p, 1)
        nested_type = c_ast.PtrDecl(quals=(p[2] or []), type=None, coord=coord)
        if len(p) > 3:
            tail_type = p[3]
            while tail_type.type is not None:
                tail_type = tail_type.type

            tail_type.type = nested_type
            p[0] = p[3]
        else:
            p[0] = nested_type

    def p_type_qualifier_list(self, p):
        """ type_qualifier_list : type_qualifier
                                | type_qualifier_list type_qualifier
        """
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

    def p_parameter_type_list(self, p):
        """ parameter_type_list : parameter_list
                                | parameter_list COMMA ELLIPSIS
        """
        if len(p) > 2:
            p[1].params.append(c_ast.EllipsisParam(self._token_coord(p, 3)))
        p[0] = p[1]

    def p_parameter_list(self, p):
        """ parameter_list  : parameter_declaration
                            | parameter_list COMMA parameter_declaration
        """
        if len(p) == 2:
            p[0] = c_ast.ParamList([p[1]], p[1].coord)
        else:
            p[1].params.append(p[3])
            p[0] = p[1]

    def p_parameter_declaration_1(self, p):
        """ parameter_declaration   : declaration_specifiers id_declarator
                                    | declaration_specifiers typeid_noparen_declarator
        """
        spec = p[1]
        if not spec['type']:
            spec['type'] = [c_ast.IdentifierType(['int'], coord=(self._token_coord(p, 1)))]
        p[0] = self._build_declarations(spec=spec,
          decls=[
         dict(decl=(p[2]))])[0]

    def p_parameter_declaration_2(self, p):
        """ parameter_declaration   : declaration_specifiers abstract_declarator_opt
        """
        spec = p[1]
        if not spec['type']:
            spec['type'] = [c_ast.IdentifierType(['int'], coord=(self._token_coord(p, 1)))]
        if len(spec['type']) > 1 and len(spec['type'][(-1)].names) == 1 and self._is_type_in_scope(spec['type'][(-1)].names[0]):
            decl = self._build_declarations(spec=spec,
              decls=[
             dict(decl=(p[2]), init=None)])[0]
        else:
            decl = c_ast.Typename(name='',
              quals=(spec['qual']),
              type=(p[2] or c_ast.TypeDecl(None, None, None)),
              coord=(self._token_coord(p, 2)))
            typename = spec['type']
            decl = self._fix_decl_name_type(decl, typename)
        p[0] = decl

    def p_identifier_list(self, p):
        """ identifier_list : identifier
                            | identifier_list COMMA identifier
        """
        if len(p) == 2:
            p[0] = c_ast.ParamList([p[1]], p[1].coord)
        else:
            p[1].params.append(p[3])
            p[0] = p[1]

    def p_initializer_1(self, p):
        """ initializer : assignment_expression
        """
        p[0] = p[1]

    def p_initializer_2(self, p):
        """ initializer : brace_open initializer_list_opt brace_close
                        | brace_open initializer_list COMMA brace_close
        """
        if p[2] is None:
            p[0] = c_ast.InitList([], self._token_coord(p, 1))
        else:
            p[0] = p[2]

    def p_initializer_list(self, p):
        """ initializer_list    : designation_opt initializer
                                | initializer_list COMMA designation_opt initializer
        """
        if len(p) == 3:
            init = p[2] if p[1] is None else c_ast.NamedInitializer(p[1], p[2])
            p[0] = c_ast.InitList([init], p[2].coord)
        else:
            init = p[4] if p[3] is None else c_ast.NamedInitializer(p[3], p[4])
            p[1].exprs.append(init)
            p[0] = p[1]

    def p_designation(self, p):
        """ designation : designator_list EQUALS
        """
        p[0] = p[1]

    def p_designator_list(self, p):
        """ designator_list : designator
                            | designator_list designator
        """
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

    def p_designator(self, p):
        """ designator  : LBRACKET constant_expression RBRACKET
                        | PERIOD identifier
        """
        p[0] = p[2]

    def p_type_name(self, p):
        """ type_name   : specifier_qualifier_list abstract_declarator_opt
        """
        typename = c_ast.Typename(name='',
          quals=(p[1]['qual']),
          type=(p[2] or c_ast.TypeDecl(None, None, None)),
          coord=(self._token_coord(p, 2)))
        p[0] = self._fix_decl_name_type(typename, p[1]['type'])

    def p_abstract_declarator_1(self, p):
        """ abstract_declarator     : pointer
        """
        dummytype = c_ast.TypeDecl(None, None, None)
        p[0] = self._type_modify_decl(decl=dummytype,
          modifier=(p[1]))

    def p_abstract_declarator_2(self, p):
        """ abstract_declarator     : pointer direct_abstract_declarator
        """
        p[0] = self._type_modify_decl(p[2], p[1])

    def p_abstract_declarator_3(self, p):
        """ abstract_declarator     : direct_abstract_declarator
        """
        p[0] = p[1]

    def p_direct_abstract_declarator_1(self, p):
        """ direct_abstract_declarator  : LPAREN abstract_declarator RPAREN """
        p[0] = p[2]

    def p_direct_abstract_declarator_2(self, p):
        """ direct_abstract_declarator  : direct_abstract_declarator LBRACKET assignment_expression_opt RBRACKET
        """
        arr = c_ast.ArrayDecl(type=None,
          dim=(p[3]),
          dim_quals=[],
          coord=(p[1].coord))
        p[0] = self._type_modify_decl(decl=(p[1]), modifier=arr)

    def p_direct_abstract_declarator_3(self, p):
        """ direct_abstract_declarator  : LBRACKET assignment_expression_opt RBRACKET
        """
        p[0] = c_ast.ArrayDecl(type=(c_ast.TypeDecl(None, None, None)),
          dim=(p[2]),
          dim_quals=[],
          coord=(self._token_coord(p, 1)))

    def p_direct_abstract_declarator_4(self, p):
        """ direct_abstract_declarator  : direct_abstract_declarator LBRACKET TIMES RBRACKET
        """
        arr = c_ast.ArrayDecl(type=None,
          dim=(c_ast.ID(p[3], self._token_coord(p, 3))),
          dim_quals=[],
          coord=(p[1].coord))
        p[0] = self._type_modify_decl(decl=(p[1]), modifier=arr)

    def p_direct_abstract_declarator_5(self, p):
        """ direct_abstract_declarator  : LBRACKET TIMES RBRACKET
        """
        p[0] = c_ast.ArrayDecl(type=(c_ast.TypeDecl(None, None, None)),
          dim=(c_ast.ID(p[3], self._token_coord(p, 3))),
          dim_quals=[],
          coord=(self._token_coord(p, 1)))

    def p_direct_abstract_declarator_6(self, p):
        """ direct_abstract_declarator  : direct_abstract_declarator LPAREN parameter_type_list_opt RPAREN
        """
        func = c_ast.FuncDecl(args=(p[3]),
          type=None,
          coord=(p[1].coord))
        p[0] = self._type_modify_decl(decl=(p[1]), modifier=func)

    def p_direct_abstract_declarator_7(self, p):
        """ direct_abstract_declarator  : LPAREN parameter_type_list_opt RPAREN
        """
        p[0] = c_ast.FuncDecl(args=(p[2]),
          type=(c_ast.TypeDecl(None, None, None)),
          coord=(self._token_coord(p, 1)))

    def p_block_item(self, p):
        """ block_item  : declaration
                        | statement
        """
        p[0] = p[1] if isinstance(p[1], list) else [p[1]]

    def p_block_item_list(self, p):
        """ block_item_list : block_item
                            | block_item_list block_item
        """
        p[0] = p[1] if (len(p) == 2 or p[2] == [None]) else (p[1] + p[2])

    def p_compound_statement_1(self, p):
        """ compound_statement : brace_open block_item_list_opt brace_close """
        p[0] = c_ast.Compound(block_items=(p[2]),
          coord=(self._token_coord(p, 1)))

    def p_labeled_statement_1(self, p):
        """ labeled_statement : ID COLON pragmacomp_or_statement """
        p[0] = c_ast.Label(p[1], p[3], self._token_coord(p, 1))

    def p_labeled_statement_2(self, p):
        """ labeled_statement : CASE constant_expression COLON pragmacomp_or_statement """
        p[0] = c_ast.Case(p[2], [p[4]], self._token_coord(p, 1))

    def p_labeled_statement_3(self, p):
        """ labeled_statement : DEFAULT COLON pragmacomp_or_statement """
        p[0] = c_ast.Default([p[3]], self._token_coord(p, 1))

    def p_selection_statement_1(self, p):
        """ selection_statement : IF LPAREN expression RPAREN pragmacomp_or_statement """
        p[0] = c_ast.If(p[3], p[5], None, self._token_coord(p, 1))

    def p_selection_statement_2(self, p):
        """ selection_statement : IF LPAREN expression RPAREN statement ELSE pragmacomp_or_statement """
        p[0] = c_ast.If(p[3], p[5], p[7], self._token_coord(p, 1))

    def p_selection_statement_3(self, p):
        """ selection_statement : SWITCH LPAREN expression RPAREN pragmacomp_or_statement """
        p[0] = fix_switch_cases(c_ast.Switch(p[3], p[5], self._token_coord(p, 1)))

    def p_iteration_statement_1(self, p):
        """ iteration_statement : WHILE LPAREN expression RPAREN pragmacomp_or_statement """
        p[0] = c_ast.While(p[3], p[5], self._token_coord(p, 1))

    def p_iteration_statement_2(self, p):
        """ iteration_statement : DO pragmacomp_or_statement WHILE LPAREN expression RPAREN SEMI """
        p[0] = c_ast.DoWhile(p[5], p[2], self._token_coord(p, 1))

    def p_iteration_statement_3(self, p):
        """ iteration_statement : FOR LPAREN expression_opt SEMI expression_opt SEMI expression_opt RPAREN pragmacomp_or_statement """
        p[0] = c_ast.For(p[3], p[5], p[7], p[9], self._token_coord(p, 1))

    def p_iteration_statement_4(self, p):
        """ iteration_statement : FOR LPAREN declaration expression_opt SEMI expression_opt RPAREN pragmacomp_or_statement """
        p[0] = c_ast.For(c_ast.DeclList(p[3], self._token_coord(p, 1)), p[4], p[6], p[8], self._token_coord(p, 1))

    def p_jump_statement_1(self, p):
        """ jump_statement  : GOTO ID SEMI """
        p[0] = c_ast.Goto(p[2], self._token_coord(p, 1))

    def p_jump_statement_2(self, p):
        """ jump_statement  : BREAK SEMI """
        p[0] = c_ast.Break(self._token_coord(p, 1))

    def p_jump_statement_3(self, p):
        """ jump_statement  : CONTINUE SEMI """
        p[0] = c_ast.Continue(self._token_coord(p, 1))

    def p_jump_statement_4(self, p):
        """ jump_statement  : RETURN expression SEMI
                            | RETURN SEMI
        """
        p[0] = c_ast.Return(p[2] if len(p) == 4 else None, self._token_coord(p, 1))

    def p_expression_statement(self, p):
        """ expression_statement : expression_opt SEMI """
        if p[1] is None:
            p[0] = c_ast.EmptyStatement(self._token_coord(p, 2))
        else:
            p[0] = p[1]

    def p_expression(self, p):
        """ expression  : assignment_expression
                        | expression COMMA assignment_expression
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            if not isinstance(p[1], c_ast.ExprList):
                p[1] = c_ast.ExprList([p[1]], p[1].coord)
            p[1].exprs.append(p[3])
            p[0] = p[1]

    def p_typedef_name(self, p):
        """ typedef_name : TYPEID """
        p[0] = c_ast.IdentifierType([p[1]], coord=(self._token_coord(p, 1)))

    def p_assignment_expression(self, p):
        """ assignment_expression   : conditional_expression
                                    | unary_expression assignment_operator assignment_expression
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = c_ast.Assignment(p[2], p[1], p[3], p[1].coord)

    def p_assignment_operator(self, p):
        """ assignment_operator : EQUALS
                                | XOREQUAL
                                | TIMESEQUAL
                                | DIVEQUAL
                                | MODEQUAL
                                | PLUSEQUAL
                                | MINUSEQUAL
                                | LSHIFTEQUAL
                                | RSHIFTEQUAL
                                | ANDEQUAL
                                | OREQUAL
        """
        p[0] = p[1]

    def p_constant_expression(self, p):
        """ constant_expression : conditional_expression """
        p[0] = p[1]

    def p_conditional_expression(self, p):
        """ conditional_expression  : binary_expression
                                    | binary_expression CONDOP expression COLON conditional_expression
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = c_ast.TernaryOp(p[1], p[3], p[5], p[1].coord)

    def p_binary_expression(self, p):
        """ binary_expression   : cast_expression
                                | binary_expression TIMES binary_expression
                                | binary_expression DIVIDE binary_expression
                                | binary_expression MOD binary_expression
                                | binary_expression PLUS binary_expression
                                | binary_expression MINUS binary_expression
                                | binary_expression RSHIFT binary_expression
                                | binary_expression LSHIFT binary_expression
                                | binary_expression LT binary_expression
                                | binary_expression LE binary_expression
                                | binary_expression GE binary_expression
                                | binary_expression GT binary_expression
                                | binary_expression EQ binary_expression
                                | binary_expression NE binary_expression
                                | binary_expression AND binary_expression
                                | binary_expression OR binary_expression
                                | binary_expression XOR binary_expression
                                | binary_expression LAND binary_expression
                                | binary_expression LOR binary_expression
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = c_ast.BinaryOp(p[2], p[1], p[3], p[1].coord)

    def p_cast_expression_1(self, p):
        """ cast_expression : unary_expression """
        p[0] = p[1]

    def p_cast_expression_2(self, p):
        """ cast_expression : LPAREN type_name RPAREN cast_expression """
        p[0] = c_ast.Cast(p[2], p[4], self._token_coord(p, 1))

    def p_unary_expression_1(self, p):
        """ unary_expression    : postfix_expression """
        p[0] = p[1]

    def p_unary_expression_2(self, p):
        """ unary_expression    : PLUSPLUS unary_expression
                                | MINUSMINUS unary_expression
                                | unary_operator cast_expression
        """
        p[0] = c_ast.UnaryOp(p[1], p[2], p[2].coord)

    def p_unary_expression_3(self, p):
        """ unary_expression    : SIZEOF unary_expression
                                | SIZEOF LPAREN type_name RPAREN
        """
        p[0] = c_ast.UnaryOp(p[1], p[2] if len(p) == 3 else p[3], self._token_coord(p, 1))

    def p_unary_operator(self, p):
        """ unary_operator  : AND
                            | TIMES
                            | PLUS
                            | MINUS
                            | NOT
                            | LNOT
        """
        p[0] = p[1]

    def p_postfix_expression_1(self, p):
        """ postfix_expression  : primary_expression """
        p[0] = p[1]

    def p_postfix_expression_2(self, p):
        """ postfix_expression  : postfix_expression LBRACKET expression RBRACKET """
        p[0] = c_ast.ArrayRef(p[1], p[3], p[1].coord)

    def p_postfix_expression_3(self, p):
        """ postfix_expression  : postfix_expression LPAREN argument_expression_list RPAREN
                                | postfix_expression LPAREN RPAREN
        """
        p[0] = c_ast.FuncCall(p[1], p[3] if len(p) == 5 else None, p[1].coord)

    def p_postfix_expression_4(self, p):
        """ postfix_expression  : postfix_expression PERIOD ID
                                | postfix_expression PERIOD TYPEID
                                | postfix_expression ARROW ID
                                | postfix_expression ARROW TYPEID
        """
        field = c_ast.ID(p[3], self._token_coord(p, 3))
        p[0] = c_ast.StructRef(p[1], p[2], field, p[1].coord)

    def p_postfix_expression_5(self, p):
        """ postfix_expression  : postfix_expression PLUSPLUS
                                | postfix_expression MINUSMINUS
        """
        p[0] = c_ast.UnaryOp('p' + p[2], p[1], p[1].coord)

    def p_postfix_expression_6(self, p):
        """ postfix_expression  : LPAREN type_name RPAREN brace_open initializer_list brace_close
                                | LPAREN type_name RPAREN brace_open initializer_list COMMA brace_close
        """
        p[0] = c_ast.CompoundLiteral(p[2], p[5])

    def p_primary_expression_1(self, p):
        """ primary_expression  : identifier """
        p[0] = p[1]

    def p_primary_expression_2(self, p):
        """ primary_expression  : constant """
        p[0] = p[1]

    def p_primary_expression_3(self, p):
        """ primary_expression  : unified_string_literal
                                | unified_wstring_literal
        """
        p[0] = p[1]

    def p_primary_expression_4(self, p):
        """ primary_expression  : LPAREN expression RPAREN """
        p[0] = p[2]

    def p_primary_expression_5(self, p):
        """ primary_expression  : OFFSETOF LPAREN type_name COMMA offsetof_member_designator RPAREN
        """
        coord = self._token_coord(p, 1)
        p[0] = c_ast.FuncCall(c_ast.ID(p[1], coord), c_ast.ExprList([p[3], p[5]], coord), coord)

    def p_offsetof_member_designator(self, p):
        """ offsetof_member_designator : identifier
                                         | offsetof_member_designator PERIOD identifier
                                         | offsetof_member_designator LBRACKET expression RBRACKET
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            if len(p) == 4:
                field = c_ast.ID(p[3], self._token_coord(p, 3))
                p[0] = c_ast.StructRef(p[1], p[2], field, p[1].coord)
            else:
                if len(p) == 5:
                    p[0] = c_ast.ArrayRef(p[1], p[3], p[1].coord)
                else:
                    raise NotImplementedError('Unexpected parsing state. len(p): %u' % len(p))

    def p_argument_expression_list(self, p):
        """ argument_expression_list    : assignment_expression
                                        | argument_expression_list COMMA assignment_expression
        """
        if len(p) == 2:
            p[0] = c_ast.ExprList([p[1]], p[1].coord)
        else:
            p[1].exprs.append(p[3])
            p[0] = p[1]

    def p_identifier(self, p):
        """ identifier  : ID """
        p[0] = c_ast.ID(p[1], self._token_coord(p, 1))

    def p_constant_1(self, p):
        """ constant    : INT_CONST_DEC
                        | INT_CONST_OCT
                        | INT_CONST_HEX
                        | INT_CONST_BIN
        """
        p[0] = c_ast.Constant('int', p[1], self._token_coord(p, 1))

    def p_constant_2(self, p):
        """ constant    : FLOAT_CONST
                        | HEX_FLOAT_CONST
        """
        if 'x' in p[1].lower():
            t = 'float'
        else:
            if p[1][(-1)] in ('f', 'F'):
                t = 'float'
            else:
                if p[1][(-1)] in ('l', 'L'):
                    t = 'long double'
                else:
                    t = 'double'
        p[0] = c_ast.Constant(t, p[1], self._token_coord(p, 1))

    def p_constant_3(self, p):
        """ constant    : CHAR_CONST
                        | WCHAR_CONST
        """
        p[0] = c_ast.Constant('char', p[1], self._token_coord(p, 1))

    def p_unified_string_literal(self, p):
        """ unified_string_literal  : STRING_LITERAL
                                    | unified_string_literal STRING_LITERAL
        """
        if len(p) == 2:
            p[0] = c_ast.Constant('string', p[1], self._token_coord(p, 1))
        else:
            p[1].value = p[1].value[:-1] + p[2][1:]
            p[0] = p[1]

    def p_unified_wstring_literal(self, p):
        """ unified_wstring_literal : WSTRING_LITERAL
                                    | unified_wstring_literal WSTRING_LITERAL
        """
        if len(p) == 2:
            p[0] = c_ast.Constant('string', p[1], self._token_coord(p, 1))
        else:
            p[1].value = p[1].value.rstrip()[:-1] + p[2][2:]
            p[0] = p[1]

    def p_brace_open(self, p):
        """ brace_open  :   LBRACE
        """
        p[0] = p[1]
        p.set_lineno(0, p.lineno(1))

    def p_brace_close(self, p):
        """ brace_close :   RBRACE
        """
        p[0] = p[1]
        p.set_lineno(0, p.lineno(1))

    def p_empty(self, p):
        """empty : """
        p[0] = None

    def p_error(self, p):
        if p:
            self._parse_error('before: %s' % p.value, self._coord(lineno=(p.lineno), column=(self.clex.find_tok_column(p))))
        else:
            self._parse_error('At end of input', self.clex.filename)