# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: pycparser\plyparser.py
import warnings

class Coord(object):
    __doc__ = ' Coordinates of a syntactic element. Consists of:\n            - File name\n            - Line number\n            - (optional) column number, for the Lexer\n    '
    __slots__ = ('file', 'line', 'column', '__weakref__')

    def __init__(self, file, line, column=None):
        self.file = file
        self.line = line
        self.column = column

    def __str__(self):
        str = '%s:%s' % (self.file, self.line)
        if self.column:
            str += ':%s' % self.column
        return str


class ParseError(Exception):
    pass


class PLYParser(object):

    def _create_opt_rule(self, rulename):
        """ Given a rule name, creates an optional ply.yacc rule
            for it. The name of the optional rule is
            <rulename>_opt
        """
        optname = rulename + '_opt'

        def optrule(self, p):
            p[0] = p[1]

        optrule.__doc__ = '%s : empty\n| %s' % (optname, rulename)
        optrule.__name__ = 'p_%s' % optname
        setattr(self.__class__, optrule.__name__, optrule)

    def _coord(self, lineno, column=None):
        return Coord(file=(self.clex.filename),
          line=lineno,
          column=column)

    def _token_coord(self, p, token_idx):
        """ Returns the coordinates for the YaccProduction objet 'p' indexed
            with 'token_idx'. The coordinate includes the 'lineno' and
            'column'. Both follow the lex semantic, starting from 1.
        """
        last_cr = p.lexer.lexer.lexdata.rfind('\n', 0, p.lexpos(token_idx))
        if last_cr < 0:
            last_cr = -1
        column = p.lexpos(token_idx) - last_cr
        return self._coord(p.lineno(token_idx), column)

    def _parse_error(self, msg, coord):
        raise ParseError('%s: %s' % (coord, msg))


def parameterized(*params):
    """ Decorator to create parameterized rules.

    Parameterized rule methods must be named starting with 'p_' and contain
    'xxx', and their docstrings may contain 'xxx' and 'yyy'. These will be
    replaced by the given parameter tuples. For example, ``p_xxx_rule()`` with
    docstring 'xxx_rule  : yyy' when decorated with
    ``@parameterized(('id', 'ID'))`` produces ``p_id_rule()`` with the docstring
    'id_rule  : ID'. Using multiple tuples produces multiple rules.
    """

    def decorate(rule_func):
        rule_func._params = params
        return rule_func

    return decorate


def template--- This code section failed: ---

 L.  91         0  LOAD_CONST               False
                2  STORE_FAST               'issued_nodoc_warning'

 L.  92         4  LOAD_GLOBAL              dir
                6  LOAD_FAST                'cls'
                8  CALL_FUNCTION_1       1  ''
               10  GET_ITER         
             12_0  COME_FROM           102  '102'
             12_1  COME_FROM            80  '80'
             12_2  COME_FROM            76  '76'
             12_3  COME_FROM            44  '44'
             12_4  COME_FROM            24  '24'
               12  FOR_ITER            104  'to 104'
               14  STORE_FAST               'attr_name'

 L.  93        16  LOAD_FAST                'attr_name'
               18  LOAD_METHOD              startswith
               20  LOAD_STR                 'p_'
               22  CALL_METHOD_1         1  ''
               24  POP_JUMP_IF_FALSE_BACK    12  'to 12'

 L.  94        26  LOAD_GLOBAL              getattr
               28  LOAD_FAST                'cls'
               30  LOAD_FAST                'attr_name'
               32  CALL_FUNCTION_2       2  ''
               34  STORE_FAST               'method'

 L.  95        36  LOAD_GLOBAL              hasattr
               38  LOAD_FAST                'method'
               40  LOAD_STR                 '_params'
               42  CALL_FUNCTION_2       2  ''
               44  POP_JUMP_IF_FALSE_BACK    12  'to 12'

 L.  97        46  LOAD_GLOBAL              delattr
               48  LOAD_FAST                'cls'
               50  LOAD_FAST                'attr_name'
               52  CALL_FUNCTION_2       2  ''
               54  POP_TOP          

 L. 105        56  LOAD_FAST                'method'
               58  LOAD_ATTR                __doc__
               60  LOAD_CONST               None
               62  <117>                 1  ''
               64  POP_JUMP_IF_FALSE    78  'to 78'

 L. 106        66  LOAD_GLOBAL              _create_param_rules
               68  LOAD_FAST                'cls'
               70  LOAD_FAST                'method'
               72  CALL_FUNCTION_2       2  ''
               74  POP_TOP          
               76  JUMP_BACK            12  'to 12'
             78_0  COME_FROM            64  '64'

 L. 107        78  LOAD_FAST                'issued_nodoc_warning'
               80  POP_JUMP_IF_TRUE_BACK    12  'to 12'

 L. 108        82  LOAD_GLOBAL              warnings
               84  LOAD_ATTR                warn

 L. 109        86  LOAD_STR                 'parsing methods must have __doc__ for pycparser to work properly'

 L. 110        88  LOAD_GLOBAL              RuntimeWarning

 L. 111        90  LOAD_CONST               2

 L. 108        92  LOAD_CONST               ('stacklevel',)
               94  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               96  POP_TOP          

 L. 112        98  LOAD_CONST               True
              100  STORE_FAST               'issued_nodoc_warning'
              102  JUMP_BACK            12  'to 12'
            104_0  COME_FROM            12  '12'

 L. 113       104  LOAD_FAST                'cls'
              106  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 62


def _create_param_rules(cls, func):
    """ Create ply.yacc rules based on a parameterized rule function

    Generates new methods (one per each pair of parameters) based on the
    template rule function `func`, and attaches them to `cls`. The rule
    function's parameters must be accessible via its `_params` attribute.
    """
    for xxx, yyy in func._params:

        def param_rule(self, p):
            funcselfp

        param_rule.__doc__ = func.__doc__.replace('xxx', xxx).replace('yyy', yyy)
        param_rule.__name__ = func.__name__.replace('xxx', xxx)
        setattr(cls, param_rule.__name__, param_rule)