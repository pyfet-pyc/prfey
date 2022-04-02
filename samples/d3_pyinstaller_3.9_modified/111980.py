# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: pycparser\c_lexer.py
import re, sys
from .ply import lex
from ply.lex import TOKEN

class CLexer(object):
    __doc__ = ' A lexer for the C language. After building it, set the\n        input text with input(), and call token() to get new\n        tokens.\n\n        The public attribute filename can be set to an initial\n        filename, but the lexer will update it upon #line\n        directives.\n    '

    def __init__(self, error_func, on_lbrace_func, on_rbrace_func, type_lookup_func):
        """ Create a new Lexer.

            error_func:
                An error function. Will be called with an error
                message, line and column as arguments, in case of
                an error during lexing.

            on_lbrace_func, on_rbrace_func:
                Called when an LBRACE or RBRACE is encountered
                (likely to push/pop type_lookup_func's scope)

            type_lookup_func:
                A type lookup function. Given a string, it must
                return True IFF this string is a name of a type
                that was defined with a typedef earlier.
        """
        self.error_func = error_func
        self.on_lbrace_func = on_lbrace_func
        self.on_rbrace_func = on_rbrace_func
        self.type_lookup_func = type_lookup_func
        self.filename = ''
        self.last_token = None
        self.line_pattern = re.compile('([ \\t]*line\\W)|([ \\t]*\\d+)')
        self.pragma_pattern = re.compile('[ \\t]*pragma\\W')

    def build--- This code section failed: ---

 L.  66         0  LOAD_GLOBAL              lex
                2  LOAD_ATTR                lex
                4  BUILD_TUPLE_0         0 
                6  LOAD_STR                 'object'
                8  LOAD_FAST                'self'
               10  BUILD_MAP_1           1 
               12  LOAD_FAST                'kwargs'
               14  <164>                 1  ''
               16  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               18  LOAD_FAST                'self'
               20  STORE_ATTR               lexer

Parse error at or near `None' instruction at offset -1

    def reset_lineno(self):
        """ Resets the internal line number counter of the lexer.
        """
        self.lexer.lineno = 1

    def input(self, text):
        self.lexer.input(text)

    def token(self):
        self.last_token = self.lexer.token()
        return self.last_token

    def find_tok_column(self, token):
        """ Find the column of the token in its line.
        """
        last_cr = self.lexer.lexdata.rfind('\n', 0, token.lexpos)
        return token.lexpos - last_cr

    def _error(self, msg, token):
        location = self._make_tok_location(token)
        self.error_func(msg, location[0], location[1])
        self.lexer.skip(1)

    def _make_tok_location(self, token):
        return (
         token.lineno, self.find_tok_column(token))

    keywords = ('_BOOL', '_COMPLEX', 'AUTO', 'BREAK', 'CASE', 'CHAR', 'CONST', 'CONTINUE',
                'DEFAULT', 'DO', 'DOUBLE', 'ELSE', 'ENUM', 'EXTERN', 'FLOAT', 'FOR',
                'GOTO', 'IF', 'INLINE', 'INT', 'LONG', 'REGISTER', 'OFFSETOF', 'RESTRICT',
                'RETURN', 'SHORT', 'SIGNED', 'SIZEOF', 'STATIC', 'STRUCT', 'SWITCH',
                'TYPEDEF', 'UNION', 'UNSIGNED', 'VOID', 'VOLATILE', 'WHILE', '__INT128')
    keyword_map = {}
    for keyword in keywords:
        if keyword == '_BOOL':
            keyword_map['_Bool'] = keyword
        else:
            if keyword == '_COMPLEX':
                keyword_map['_Complex'] = keyword
            else:
                keyword_map[keyword.lower()] = keyword
    else:
        tokens = keywords + ('ID', 'TYPEID', 'INT_CONST_DEC', 'INT_CONST_OCT', 'INT_CONST_HEX',
                             'INT_CONST_BIN', 'INT_CONST_CHAR', 'FLOAT_CONST', 'HEX_FLOAT_CONST',
                             'CHAR_CONST', 'WCHAR_CONST', 'STRING_LITERAL', 'WSTRING_LITERAL',
                             'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD', 'OR', 'AND',
                             'NOT', 'XOR', 'LSHIFT', 'RSHIFT', 'LOR', 'LAND', 'LNOT',
                             'LT', 'LE', 'GT', 'GE', 'EQ', 'NE', 'EQUALS', 'TIMESEQUAL',
                             'DIVEQUAL', 'MODEQUAL', 'PLUSEQUAL', 'MINUSEQUAL', 'LSHIFTEQUAL',
                             'RSHIFTEQUAL', 'ANDEQUAL', 'XOREQUAL', 'OREQUAL', 'PLUSPLUS',
                             'MINUSMINUS', 'ARROW', 'CONDOP', 'LPAREN', 'RPAREN',
                             'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 'COMMA',
                             'PERIOD', 'SEMI', 'COLON', 'ELLIPSIS', 'PPHASH', 'PPPRAGMA',
                             'PPPRAGMASTR')
        identifier = '[a-zA-Z_$][0-9a-zA-Z_$]*'
        hex_prefix = '0[xX]'
        hex_digits = '[0-9a-fA-F]+'
        bin_prefix = '0[bB]'
        bin_digits = '[01]+'
        integer_suffix_opt = '(([uU]ll)|([uU]LL)|(ll[uU]?)|(LL[uU]?)|([uU][lL])|([lL][uU]?)|[uU])?'
        decimal_constant = '(0' + integer_suffix_opt + ')|([1-9][0-9]*' + integer_suffix_opt + ')'
        octal_constant = '0[0-7]*' + integer_suffix_opt
        hex_constant = hex_prefix + hex_digits + integer_suffix_opt
        bin_constant = bin_prefix + bin_digits + integer_suffix_opt
        bad_octal_constant = '0[0-7]*[89]'
        simple_escape = '([a-wyzA-Z._~!=&\\^\\-\\\\?\'"]|x(?![0-9a-fA-F]))'
        decimal_escape = '(\\d+)(?!\\d)'
        hex_escape = '(x[0-9a-fA-F]+)(?![0-9a-fA-F])'
        bad_escape = '([\\\\][^a-zA-Z._~^!=&\\^\\-\\\\?\'"x0-9])'
        escape_sequence = '(\\\\(' + simple_escape + '|' + decimal_escape + '|' + hex_escape + '))'
        escape_sequence_start_in_string = '(\\\\[0-9a-zA-Z._~!=&\\^\\-\\\\?\'"])'
        cconst_char = "([^'\\\\\\n]|" + escape_sequence + ')'
        char_const = "'" + cconst_char + "'"
        wchar_const = 'L' + char_const
        multicharacter_constant = "'" + cconst_char + "{2,4}'"
        unmatched_quote = "('" + cconst_char + "*\\n)|('" + cconst_char + '*$)'
        bad_char_const = "('" + cconst_char + "[^'\n]+')|('')|('" + bad_escape + "[^'\\n]*')"
        string_char = '([^"\\\\\\n]|' + escape_sequence_start_in_string + ')'
        string_literal = '"' + string_char + '*"'
        wstring_literal = 'L' + string_literal
        bad_string_literal = '"' + string_char + '*' + bad_escape + string_char + '*"'
        exponent_part = '([eE][-+]?[0-9]+)'
        fractional_constant = '([0-9]*\\.[0-9]+)|([0-9]+\\.)'
        floating_constant = '((((' + fractional_constant + ')' + exponent_part + '?)|([0-9]+' + exponent_part + '))[FfLl]?)'
        binary_exponent_part = '([pP][+-]?[0-9]+)'
        hex_fractional_constant = '(((' + hex_digits + ')?\\.' + hex_digits + ')|(' + hex_digits + '\\.))'
        hex_floating_constant = '(' + hex_prefix + '(' + hex_digits + '|' + hex_fractional_constant + ')' + binary_exponent_part + '[FfLl]?)'
        states = (('ppline', 'exclusive'), ('pppragma', 'exclusive'))

        def t_PPHASH(self, t):
            r"""[ \t]*\#"""
            if self.line_pattern.match((t.lexer.lexdata), pos=(t.lexer.lexpos)):
                t.lexer.begin('ppline')
                self.pp_line = self.pp_filename = None
            elif self.pragma_pattern.match((t.lexer.lexdata), pos=(t.lexer.lexpos)):
                t.lexer.begin('pppragma')
            else:
                t.type = 'PPHASH'
                return t

        @TOKEN(string_literal)
        def t_ppline_FILENAME--- This code section failed: ---

 L. 289         0  LOAD_FAST                'self'
                2  LOAD_ATTR                pp_line
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L. 290        10  LOAD_FAST                'self'
               12  LOAD_METHOD              _error
               14  LOAD_STR                 'filename before line number in #line'
               16  LOAD_FAST                't'
               18  CALL_METHOD_2         2  ''
               20  POP_TOP          
               22  JUMP_FORWARD         44  'to 44'
             24_0  COME_FROM             8  '8'

 L. 292        24  LOAD_FAST                't'
               26  LOAD_ATTR                value
               28  LOAD_METHOD              lstrip
               30  LOAD_STR                 '"'
               32  CALL_METHOD_1         1  ''
               34  LOAD_METHOD              rstrip
               36  LOAD_STR                 '"'
               38  CALL_METHOD_1         1  ''
               40  LOAD_FAST                'self'
               42  STORE_ATTR               pp_filename
             44_0  COME_FROM            22  '22'

Parse error at or near `None' instruction at offset -1

        @TOKEN(decimal_constant)
        def t_ppline_LINE_NUMBER--- This code section failed: ---

 L. 296         0  LOAD_FAST                'self'
                2  LOAD_ATTR                pp_line
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L. 297        10  LOAD_FAST                't'
               12  LOAD_ATTR                value
               14  LOAD_FAST                'self'
               16  STORE_ATTR               pp_line
               18  JUMP_FORWARD         20  'to 20'
             20_0  COME_FROM            18  '18'
             20_1  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

        def t_ppline_NEWLINE--- This code section failed: ---

 L. 305         0  LOAD_FAST                'self'
                2  LOAD_ATTR                pp_line
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L. 306        10  LOAD_FAST                'self'
               12  LOAD_METHOD              _error
               14  LOAD_STR                 'line number missing in #line'
               16  LOAD_FAST                't'
               18  CALL_METHOD_2         2  ''
               20  POP_TOP          
               22  JUMP_FORWARD         56  'to 56'
             24_0  COME_FROM             8  '8'

 L. 308        24  LOAD_GLOBAL              int
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                pp_line
               30  CALL_FUNCTION_1       1  ''
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                lexer
               36  STORE_ATTR               lineno

 L. 310        38  LOAD_FAST                'self'
               40  LOAD_ATTR                pp_filename
               42  LOAD_CONST               None
               44  <117>                 1  ''
               46  POP_JUMP_IF_FALSE    56  'to 56'

 L. 311        48  LOAD_FAST                'self'
               50  LOAD_ATTR                pp_filename
               52  LOAD_FAST                'self'
               54  STORE_ATTR               filename
             56_0  COME_FROM            46  '46'
             56_1  COME_FROM            22  '22'

 L. 313        56  LOAD_FAST                't'
               58  LOAD_ATTR                lexer
               60  LOAD_METHOD              begin
               62  LOAD_STR                 'INITIAL'
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          

Parse error at or near `None' instruction at offset -1

        def t_ppline_PPLINE(self, t):
            """line"""
            pass

        t_ppline_ignore = ' \t'

        def t_ppline_error(self, t):
            self._error'invalid #line directive't

        def t_pppragma_NEWLINE(self, t):
            r"""\n"""
            t.lexer.lineno += 1
            t.lexer.begin('INITIAL')

        def t_pppragma_PPPRAGMA(self, t):
            """pragma"""
            return t

        t_pppragma_ignore = ' \t'

        def t_pppragma_STR(self, t):
            """.+"""
            t.type = 'PPPRAGMASTR'
            return t

        def t_pppragma_error(self, t):
            self._error'invalid #pragma directive't

        t_ignore = ' \t'

        def t_NEWLINE(self, t):
            r"""\n+"""
            t.lexer.lineno += t.value.count('\n')

        t_PLUS = '\\+'
        t_MINUS = '-'
        t_TIMES = '\\*'
        t_DIVIDE = '/'
        t_MOD = '%'
        t_OR = '\\|'
        t_AND = '&'
        t_NOT = '~'
        t_XOR = '\\^'
        t_LSHIFT = '<<'
        t_RSHIFT = '>>'
        t_LOR = '\\|\\|'
        t_LAND = '&&'
        t_LNOT = '!'
        t_LT = '<'
        t_GT = '>'
        t_LE = '<='
        t_GE = '>='
        t_EQ = '=='
        t_NE = '!='
        t_EQUALS = '='
        t_TIMESEQUAL = '\\*='
        t_DIVEQUAL = '/='
        t_MODEQUAL = '%='
        t_PLUSEQUAL = '\\+='
        t_MINUSEQUAL = '-='
        t_LSHIFTEQUAL = '<<='
        t_RSHIFTEQUAL = '>>='
        t_ANDEQUAL = '&='
        t_OREQUAL = '\\|='
        t_XOREQUAL = '\\^='
        t_PLUSPLUS = '\\+\\+'
        t_MINUSMINUS = '--'
        t_ARROW = '->'
        t_CONDOP = '\\?'
        t_LPAREN = '\\('
        t_RPAREN = '\\)'
        t_LBRACKET = '\\['
        t_RBRACKET = '\\]'
        t_COMMA = ','
        t_PERIOD = '\\.'
        t_SEMI = ';'
        t_COLON = ':'
        t_ELLIPSIS = '\\.\\.\\.'

        @TOKEN('\\{')
        def t_LBRACE(self, t):
            self.on_lbrace_func()
            return t

        @TOKEN('\\}')
        def t_RBRACE(self, t):
            self.on_rbrace_func()
            return t

        t_STRING_LITERAL = string_literal

        @TOKEN(floating_constant)
        def t_FLOAT_CONST(self, t):
            return t

        @TOKEN(hex_floating_constant)
        def t_HEX_FLOAT_CONST(self, t):
            return t

        @TOKEN(hex_constant)
        def t_INT_CONST_HEX(self, t):
            return t

        @TOKEN(bin_constant)
        def t_INT_CONST_BIN(self, t):
            return t

        @TOKEN(bad_octal_constant)
        def t_BAD_CONST_OCT(self, t):
            msg = 'Invalid octal constant'
            self._errormsgt

        @TOKEN(octal_constant)
        def t_INT_CONST_OCT(self, t):
            return t

        @TOKEN(decimal_constant)
        def t_INT_CONST_DEC(self, t):
            return t

        @TOKEN(multicharacter_constant)
        def t_INT_CONST_CHAR(self, t):
            return t

        @TOKEN(char_const)
        def t_CHAR_CONST(self, t):
            return t

        @TOKEN(wchar_const)
        def t_WCHAR_CONST(self, t):
            return t

        @TOKEN(unmatched_quote)
        def t_UNMATCHED_QUOTE(self, t):
            msg = "Unmatched '"
            self._errormsgt

        @TOKEN(bad_char_const)
        def t_BAD_CHAR_CONST(self, t):
            msg = 'Invalid char constant %s' % t.value
            self._errormsgt

        @TOKEN(wstring_literal)
        def t_WSTRING_LITERAL(self, t):
            return t

        @TOKEN(bad_string_literal)
        def t_BAD_STRING_LITERAL(self, t):
            msg = 'String contains invalid escape code'
            self._errormsgt

        @TOKEN(identifier)
        def t_ID(self, t):
            t.type = self.keyword_map.gett.value'ID'
            if t.type == 'ID':
                if self.type_lookup_func(t.value):
                    t.type = 'TYPEID'
            return t

        def t_error(self, t):
            msg = 'Illegal character %s' % repr(t.value[0])
            self._errormsgt