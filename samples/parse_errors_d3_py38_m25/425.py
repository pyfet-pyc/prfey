# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: gettext.py
"""Internationalization and localization support.

This module provides internationalization (I18N) and localization (L10N)
support for your Python programs by providing an interface to the GNU gettext
message catalog library.

I18N refers to the operation by which a program is made aware of multiple
languages.  L10N refers to the adaptation of your program, once
internationalized, to the local language and cultural habits.

"""
import locale, os, re, sys
__all__ = [
 'NullTranslations', 'GNUTranslations', 'Catalog',
 'find', 'translation', 'install', 'textdomain', 'bindtextdomain',
 'bind_textdomain_codeset',
 'dgettext', 'dngettext', 'gettext', 'lgettext', 'ldgettext',
 'ldngettext', 'lngettext', 'ngettext',
 'pgettext', 'dpgettext', 'npgettext', 'dnpgettext']
_default_localedir = os.path.join(sys.base_prefix, 'share', 'locale')
_token_pattern = re.compile('\n        (?P<WHITESPACES>[ \\t]+)                    | # spaces and horizontal tabs\n        (?P<NUMBER>[0-9]+\\b)                       | # decimal integer\n        (?P<NAME>n\\b)                              | # only n is allowed\n        (?P<PARENTHESIS>[()])                      |\n        (?P<OPERATOR>[-*/%+?:]|[><!]=?|==|&&|\\|\\|) | # !, *, /, %, +, -, <, >,\n                                                     # <=, >=, ==, !=, &&, ||,\n                                                     # ? :\n                                                     # unary and bitwise ops\n                                                     # not allowed\n        (?P<INVALID>\\w+|.)                           # invalid token\n    ', re.VERBOSE | re.DOTALL)

def _tokenize(plural):
    for mo in re.finditer(_token_pattern, plural):
        kind = mo.lastgroup
        if kind == 'WHITESPACES':
            pass
        else:
            value = mo.group(kind)
            if kind == 'INVALID':
                raise ValueError('invalid token in plural form: %s' % value)
            yield value
    else:
        yield ''


def _error(value):
    if value:
        return ValueError('unexpected token in plural form: %s' % value)
    return ValueError('unexpected end of plural form')


_binary_ops = (('||',), ('&&',), ('==', '!='), ('<', '>', '<=', '>='), ('+', '-'),
               ('*', '/', '%'))
_binary_ops = {i:op for i, ops in enumerate(_binary_ops, 1) for op in ops}
_c2py_ops = {'||':'or',  '&&':'and',  '/':'//'}

def _parse(tokens, priority=-1):
    result = ''
    nexttok = next(tokens)
    while True:
        if nexttok == '!':
            result += 'not '
            nexttok = next(tokens)

    if nexttok == '(':
        sub, nexttok = _parse(tokens)
        result = '%s(%s)' % (result, sub)
        if nexttok != ')':
            raise ValueError('unbalanced parenthesis in plural form')
    else:
        pass
    if nexttok == 'n':
        result = '%s%s' % (result, nexttok)
    else:
        try:
            value = int(nexttok, 10)
        except ValueError:
            raise _error(nexttok) from None
        else:
            result = '%s%d' % (result, value)
    nexttok = next(tokens)
    j = 100
    while True:
        if nexttok in _binary_ops:
            i = _binary_ops[nexttok]
            if i < priority:
                pass
            else:
                if i in (3, 4):
                    if j in (3, 4):
                        result = '(%s)' % result
                op = _c2py_ops.get(nexttok, nexttok)
                right, nexttok = _parse(tokens, i + 1)
                result = '%s %s %s' % (result, op, right)
                j = i

    if j == priority == 4:
        result = '(%s)' % result
    if nexttok == '?':
        if priority <= 0:
            if_true, nexttok = _parse(tokens, 0)
            if nexttok != ':':
                raise _error(nexttok)
            if_false, nexttok = _parse(tokens)
            result = '%s if %s else %s' % (if_true, result, if_false)
            if priority == 0:
                result = '(%s)' % result
    return (
     result, nexttok)


def _as_int(n):
    try:
        i = round(n)
    except TypeError:
        raise TypeError('Plural value must be an integer, got %s' % (
         n.__class__.__name__,)) from None
    else:
        import warnings
        warnings.warn('Plural value must be an integer, got %s' % (
         n.__class__.__name__,), DeprecationWarning, 4)
        return n


def c2py(plural):
    """Gets a C expression as used in PO files for plural forms and returns a
    Python function that implements an equivalent expression.
    """
    if len(plural) > 1000:
        raise ValueError('plural form expression is too long')
    try:
        result, nexttok = _parse(_tokenize(plural))
        if nexttok:
            raise _error(nexttok)
        depth = 0
        for c in result:
            if c == '(':
                depth += 1
                if depth > 20:
                    raise ValueError('plural form expression is too complex')
            else:
                if c == ')':
                    depth -= 1

        ns = {'_as_int': _as_int}
        exec('if True:\n            def func(n):\n                if not isinstance(n, int):\n                    n = _as_int(n)\n                return int(%s)\n            ' % result, ns)
        return ns['func']
    except RecursionError:
        raise ValueError('plural form expression is too complex')


def _expand_lang(loc):
    loc = locale.normalize(loc)
    COMPONENT_CODESET = 1
    COMPONENT_TERRITORY = 2
    COMPONENT_MODIFIER = 4
    mask = 0
    pos = loc.find('@')
    if pos >= 0:
        modifier = loc[pos:]
        loc = loc[:pos]
        mask |= COMPONENT_MODIFIER
    else:
        modifier = ''
    pos = loc.find('.')
    if pos >= 0:
        codeset = loc[pos:]
        loc = loc[:pos]
        mask |= COMPONENT_CODESET
    else:
        codeset = ''
    pos = loc.find('_')
    if pos >= 0:
        territory = loc[pos:]
        loc = loc[:pos]
        mask |= COMPONENT_TERRITORY
    else:
        territory = ''
    language = loc
    ret = []
    for i in range(mask + 1):
        if not i & ~mask:
            val = language
            if i & COMPONENT_TERRITORY:
                val += territory
            else:
                if i & COMPONENT_CODESET:
                    val += codeset
                if i & COMPONENT_MODIFIER:
                    val += modifier
                ret.append(val)
    else:
        ret.reverse()
        return ret


class NullTranslations:

    def __init__(self, fp=None):
        self._info = {}
        self._charset = None
        self._output_charset = None
        self._fallback = None
        if fp is not None:
            self._parse(fp)

    def _parse(self, fp):
        pass

    def add_fallback(self, fallback):
        if self._fallback:
            self._fallback.add_fallback(fallback)
        else:
            self._fallback = fallback

    def gettext(self, message):
        if self._fallback:
            return self._fallback.gettext(message)
        return message

    def lgettext(self, message):
        import warnings
        warnings.warn('lgettext() is deprecated, use gettext() instead', DeprecationWarning, 2)
        if self._fallback:
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore', '.*\\blgettext\\b.*', DeprecationWarning)
                return self._fallback.lgettext(message)
        if self._output_charset:
            return message.encode(self._output_charset)
        return message.encode(locale.getpreferredencoding())

    def ngettext(self, msgid1, msgid2, n):
        if self._fallback:
            return self._fallback.ngettext(msgid1, msgid2, n)
        if n == 1:
            return msgid1
        return msgid2

    def lngettext(self, msgid1, msgid2, n):
        import warnings
        warnings.warn('lngettext() is deprecated, use ngettext() instead', DeprecationWarning, 2)
        if self._fallback:
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore', '.*\\blngettext\\b.*', DeprecationWarning)
                return self._fallback.lngettext(msgid1, msgid2, n)
        if n == 1:
            tmsg = msgid1
        else:
            tmsg = msgid2
        if self._output_charset:
            return tmsg.encode(self._output_charset)
        return tmsg.encode(locale.getpreferredencoding())

    def pgettext(self, context, message):
        if self._fallback:
            return self._fallback.pgettext(context, message)
        return message

    def npgettext(self, context, msgid1, msgid2, n):
        if self._fallback:
            return self._fallback.npgettext(context, msgid1, msgid2, n)
        if n == 1:
            return msgid1
        return msgid2

    def info(self):
        return self._info

    def charset(self):
        return self._charset

    def output_charset(self):
        import warnings
        warnings.warn('output_charset() is deprecated', DeprecationWarning, 2)
        return self._output_charset

    def set_output_charset(self, charset):
        import warnings
        warnings.warn('set_output_charset() is deprecated', DeprecationWarning, 2)
        self._output_charset = charset

    def install(self, names=None):
        import builtins
        builtins.__dict__['_'] = self.gettext
        if names is not None:
            allowed = {
             'gettext', 'lgettext', 'lngettext',
             'ngettext', 'npgettext', 'pgettext'}
            for name in allowed & set(names):
                builtins.__dict__[name] = getattr(self, name)


class GNUTranslations(NullTranslations):
    LE_MAGIC = 2500072158
    BE_MAGIC = 3725722773
    CONTEXT = '%s\x04%s'
    VERSIONS = (0, 1)

    def _get_versions(self, version):
        """Returns a tuple of major version, minor version"""
        return (
         version >> 16, version & 65535)

    def _parse--- This code section failed: ---

 L. 376         0  LOAD_CONST               0
                2  LOAD_CONST               ('unpack',)
                4  IMPORT_NAME              struct
                6  IMPORT_FROM              unpack
                8  STORE_FAST               'unpack'
               10  POP_TOP          

 L. 377        12  LOAD_GLOBAL              getattr
               14  LOAD_FAST                'fp'
               16  LOAD_STR                 'name'
               18  LOAD_STR                 ''
               20  CALL_FUNCTION_3       3  ''
               22  STORE_FAST               'filename'

 L. 380        24  BUILD_MAP_0           0 
               26  DUP_TOP          
               28  LOAD_FAST                'self'
               30  STORE_ATTR               _catalog
               32  STORE_FAST               'catalog'

 L. 381        34  LOAD_LAMBDA              '<code_object <lambda>>'
               36  LOAD_STR                 'GNUTranslations._parse.<locals>.<lambda>'
               38  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               40  LOAD_FAST                'self'
               42  STORE_ATTR               plural

 L. 382        44  LOAD_FAST                'fp'
               46  LOAD_METHOD              read
               48  CALL_METHOD_0         0  ''
               50  STORE_FAST               'buf'

 L. 383        52  LOAD_GLOBAL              len
               54  LOAD_FAST                'buf'
               56  CALL_FUNCTION_1       1  ''
               58  STORE_FAST               'buflen'

 L. 385        60  LOAD_FAST                'unpack'
               62  LOAD_STR                 '<I'
               64  LOAD_FAST                'buf'
               66  LOAD_CONST               None
               68  LOAD_CONST               4
               70  BUILD_SLICE_2         2 
               72  BINARY_SUBSCR    
               74  CALL_FUNCTION_2       2  ''
               76  LOAD_CONST               0
               78  BINARY_SUBSCR    
               80  STORE_FAST               'magic'

 L. 386        82  LOAD_FAST                'magic'
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                LE_MAGIC
               88  COMPARE_OP               ==
               90  POP_JUMP_IF_FALSE   124  'to 124'

 L. 387        92  LOAD_FAST                'unpack'
               94  LOAD_STR                 '<4I'
               96  LOAD_FAST                'buf'
               98  LOAD_CONST               4
              100  LOAD_CONST               20
              102  BUILD_SLICE_2         2 
              104  BINARY_SUBSCR    
              106  CALL_FUNCTION_2       2  ''
              108  UNPACK_SEQUENCE_4     4 
              110  STORE_FAST               'version'
              112  STORE_FAST               'msgcount'
              114  STORE_FAST               'masteridx'
              116  STORE_FAST               'transidx'

 L. 388       118  LOAD_STR                 '<II'
              120  STORE_FAST               'ii'
              122  JUMP_FORWARD        178  'to 178'
            124_0  COME_FROM            90  '90'

 L. 389       124  LOAD_FAST                'magic'
              126  LOAD_FAST                'self'
              128  LOAD_ATTR                BE_MAGIC
              130  COMPARE_OP               ==
              132  POP_JUMP_IF_FALSE   166  'to 166'

 L. 390       134  LOAD_FAST                'unpack'
              136  LOAD_STR                 '>4I'
              138  LOAD_FAST                'buf'
              140  LOAD_CONST               4
              142  LOAD_CONST               20
              144  BUILD_SLICE_2         2 
              146  BINARY_SUBSCR    
              148  CALL_FUNCTION_2       2  ''
              150  UNPACK_SEQUENCE_4     4 
              152  STORE_FAST               'version'
              154  STORE_FAST               'msgcount'
              156  STORE_FAST               'masteridx'
              158  STORE_FAST               'transidx'

 L. 391       160  LOAD_STR                 '>II'
              162  STORE_FAST               'ii'
              164  JUMP_FORWARD        178  'to 178'
            166_0  COME_FROM           132  '132'

 L. 393       166  LOAD_GLOBAL              OSError
              168  LOAD_CONST               0
              170  LOAD_STR                 'Bad magic number'
              172  LOAD_FAST                'filename'
              174  CALL_FUNCTION_3       3  ''
              176  RAISE_VARARGS_1       1  'exception instance'
            178_0  COME_FROM           164  '164'
            178_1  COME_FROM           122  '122'

 L. 395       178  LOAD_FAST                'self'
              180  LOAD_METHOD              _get_versions
              182  LOAD_FAST                'version'
              184  CALL_METHOD_1         1  ''
              186  UNPACK_SEQUENCE_2     2 
              188  STORE_FAST               'major_version'
              190  STORE_FAST               'minor_version'

 L. 397       192  LOAD_FAST                'major_version'
              194  LOAD_FAST                'self'
              196  LOAD_ATTR                VERSIONS
              198  COMPARE_OP               not-in
              200  POP_JUMP_IF_FALSE   222  'to 222'

 L. 398       202  LOAD_GLOBAL              OSError
              204  LOAD_CONST               0
              206  LOAD_STR                 'Bad version number '
              208  LOAD_GLOBAL              str
              210  LOAD_FAST                'major_version'
              212  CALL_FUNCTION_1       1  ''
              214  BINARY_ADD       
              216  LOAD_FAST                'filename'
              218  CALL_FUNCTION_3       3  ''
              220  RAISE_VARARGS_1       1  'exception instance'
            222_0  COME_FROM           200  '200'

 L. 402       222  LOAD_GLOBAL              range
              224  LOAD_CONST               0
              226  LOAD_FAST                'msgcount'
              228  CALL_FUNCTION_2       2  ''
              230  GET_ITER         
            232_0  COME_FROM           752  '752'
          232_234  FOR_ITER            754  'to 754'
              236  STORE_FAST               'i'

 L. 403       238  LOAD_FAST                'unpack'
              240  LOAD_FAST                'ii'
              242  LOAD_FAST                'buf'
              244  LOAD_FAST                'masteridx'
              246  LOAD_FAST                'masteridx'
              248  LOAD_CONST               8
              250  BINARY_ADD       
              252  BUILD_SLICE_2         2 
              254  BINARY_SUBSCR    
              256  CALL_FUNCTION_2       2  ''
              258  UNPACK_SEQUENCE_2     2 
              260  STORE_FAST               'mlen'
              262  STORE_FAST               'moff'

 L. 404       264  LOAD_FAST                'moff'
              266  LOAD_FAST                'mlen'
              268  BINARY_ADD       
              270  STORE_FAST               'mend'

 L. 405       272  LOAD_FAST                'unpack'
              274  LOAD_FAST                'ii'
              276  LOAD_FAST                'buf'
              278  LOAD_FAST                'transidx'
              280  LOAD_FAST                'transidx'
              282  LOAD_CONST               8
              284  BINARY_ADD       
              286  BUILD_SLICE_2         2 
              288  BINARY_SUBSCR    
              290  CALL_FUNCTION_2       2  ''
              292  UNPACK_SEQUENCE_2     2 
              294  STORE_FAST               'tlen'
              296  STORE_FAST               'toff'

 L. 406       298  LOAD_FAST                'toff'
              300  LOAD_FAST                'tlen'
              302  BINARY_ADD       
              304  STORE_FAST               'tend'

 L. 407       306  LOAD_FAST                'mend'
              308  LOAD_FAST                'buflen'
              310  COMPARE_OP               <
          312_314  POP_JUMP_IF_FALSE   352  'to 352'
              316  LOAD_FAST                'tend'
              318  LOAD_FAST                'buflen'
              320  COMPARE_OP               <
          322_324  POP_JUMP_IF_FALSE   352  'to 352'

 L. 408       326  LOAD_FAST                'buf'
              328  LOAD_FAST                'moff'
              330  LOAD_FAST                'mend'
              332  BUILD_SLICE_2         2 
              334  BINARY_SUBSCR    
              336  STORE_FAST               'msg'

 L. 409       338  LOAD_FAST                'buf'
              340  LOAD_FAST                'toff'
              342  LOAD_FAST                'tend'
              344  BUILD_SLICE_2         2 
              346  BINARY_SUBSCR    
              348  STORE_FAST               'tmsg'
              350  JUMP_FORWARD        364  'to 364'
            352_0  COME_FROM           322  '322'
            352_1  COME_FROM           312  '312'

 L. 411       352  LOAD_GLOBAL              OSError
              354  LOAD_CONST               0
              356  LOAD_STR                 'File is corrupt'
              358  LOAD_FAST                'filename'
              360  CALL_FUNCTION_3       3  ''
              362  RAISE_VARARGS_1       1  'exception instance'
            364_0  COME_FROM           350  '350'

 L. 413       364  LOAD_FAST                'mlen'
              366  LOAD_CONST               0
              368  COMPARE_OP               ==
          370_372  POP_JUMP_IF_FALSE   620  'to 620'

 L. 415       374  LOAD_CONST               None
              376  STORE_FAST               'lastk'

 L. 416       378  LOAD_FAST                'tmsg'
              380  LOAD_METHOD              split
              382  LOAD_CONST               b'\n'
              384  CALL_METHOD_1         1  ''
              386  GET_ITER         
            388_0  COME_FROM           616  '616'
            388_1  COME_FROM           574  '574'
            388_2  COME_FROM           566  '566'
            388_3  COME_FROM           438  '438'
            388_4  COME_FROM           410  '410'
              388  FOR_ITER            620  'to 620'
              390  STORE_FAST               'b_item'

 L. 417       392  LOAD_FAST                'b_item'
              394  LOAD_METHOD              decode
              396  CALL_METHOD_0         0  ''
              398  LOAD_METHOD              strip
              400  CALL_METHOD_0         0  ''
              402  STORE_FAST               'item'

 L. 418       404  LOAD_FAST                'item'
          406_408  POP_JUMP_IF_TRUE    414  'to 414'

 L. 419   410_412  JUMP_BACK           388  'to 388'
            414_0  COME_FROM           406  '406'

 L. 421       414  LOAD_FAST                'item'
              416  LOAD_METHOD              startswith
              418  LOAD_STR                 '#-#-#-#-#'
              420  CALL_METHOD_1         1  ''
          422_424  POP_JUMP_IF_FALSE   442  'to 442'
              426  LOAD_FAST                'item'
              428  LOAD_METHOD              endswith
              430  LOAD_STR                 '#-#-#-#-#'
              432  CALL_METHOD_1         1  ''
          434_436  POP_JUMP_IF_FALSE   442  'to 442'

 L. 422   438_440  JUMP_BACK           388  'to 388'
            442_0  COME_FROM           434  '434'
            442_1  COME_FROM           422  '422'

 L. 423       442  LOAD_CONST               None
              444  DUP_TOP          
              446  STORE_FAST               'k'
              448  STORE_FAST               'v'

 L. 424       450  LOAD_STR                 ':'
              452  LOAD_FAST                'item'
              454  COMPARE_OP               in
          456_458  POP_JUMP_IF_FALSE   512  'to 512'

 L. 425       460  LOAD_FAST                'item'
              462  LOAD_METHOD              split
              464  LOAD_STR                 ':'
              466  LOAD_CONST               1
              468  CALL_METHOD_2         2  ''
              470  UNPACK_SEQUENCE_2     2 
              472  STORE_FAST               'k'
              474  STORE_FAST               'v'

 L. 426       476  LOAD_FAST                'k'
              478  LOAD_METHOD              strip
              480  CALL_METHOD_0         0  ''
              482  LOAD_METHOD              lower
              484  CALL_METHOD_0         0  ''
              486  STORE_FAST               'k'

 L. 427       488  LOAD_FAST                'v'
              490  LOAD_METHOD              strip
              492  CALL_METHOD_0         0  ''
              494  STORE_FAST               'v'

 L. 428       496  LOAD_FAST                'v'
              498  LOAD_FAST                'self'
              500  LOAD_ATTR                _info
              502  LOAD_FAST                'k'
              504  STORE_SUBSCR     

 L. 429       506  LOAD_FAST                'k'
              508  STORE_FAST               'lastk'
              510  JUMP_FORWARD        540  'to 540'
            512_0  COME_FROM           456  '456'

 L. 430       512  LOAD_FAST                'lastk'
          514_516  POP_JUMP_IF_FALSE   540  'to 540'

 L. 431       518  LOAD_FAST                'self'
              520  LOAD_ATTR                _info
              522  LOAD_FAST                'lastk'
              524  DUP_TOP_TWO      
              526  BINARY_SUBSCR    
              528  LOAD_STR                 '\n'
              530  LOAD_FAST                'item'
              532  BINARY_ADD       
              534  INPLACE_ADD      
              536  ROT_THREE        
              538  STORE_SUBSCR     
            540_0  COME_FROM           514  '514'
            540_1  COME_FROM           510  '510'

 L. 432       540  LOAD_FAST                'k'
              542  LOAD_STR                 'content-type'
              544  COMPARE_OP               ==
          546_548  POP_JUMP_IF_FALSE   568  'to 568'

 L. 433       550  LOAD_FAST                'v'
              552  LOAD_METHOD              split
              554  LOAD_STR                 'charset='
              556  CALL_METHOD_1         1  ''
              558  LOAD_CONST               1
              560  BINARY_SUBSCR    
              562  LOAD_FAST                'self'
              564  STORE_ATTR               _charset
              566  JUMP_BACK           388  'to 388'
            568_0  COME_FROM           546  '546'

 L. 434       568  LOAD_FAST                'k'
              570  LOAD_STR                 'plural-forms'
              572  COMPARE_OP               ==
          574_576  POP_JUMP_IF_FALSE_BACK   388  'to 388'

 L. 435       578  LOAD_FAST                'v'
              580  LOAD_METHOD              split
              582  LOAD_STR                 ';'
              584  CALL_METHOD_1         1  ''
              586  STORE_FAST               'v'

 L. 436       588  LOAD_FAST                'v'
              590  LOAD_CONST               1
              592  BINARY_SUBSCR    
              594  LOAD_METHOD              split
              596  LOAD_STR                 'plural='
              598  CALL_METHOD_1         1  ''
              600  LOAD_CONST               1
              602  BINARY_SUBSCR    
              604  STORE_FAST               'plural'

 L. 437       606  LOAD_GLOBAL              c2py
              608  LOAD_FAST                'plural'
              610  CALL_FUNCTION_1       1  ''
              612  LOAD_FAST                'self'
              614  STORE_ATTR               plural
          616_618  JUMP_BACK           388  'to 388'
            620_0  COME_FROM           388  '388'
            620_1  COME_FROM           370  '370'

 L. 447       620  LOAD_FAST                'self'
              622  LOAD_ATTR                _charset
          624_626  JUMP_IF_TRUE_OR_POP   630  'to 630'
              628  LOAD_STR                 'ascii'
            630_0  COME_FROM           624  '624'
              630  STORE_FAST               'charset'

 L. 448       632  LOAD_CONST               b'\x00'
              634  LOAD_FAST                'msg'
              636  COMPARE_OP               in
          638_640  POP_JUMP_IF_FALSE   716  'to 716'

 L. 450       642  LOAD_FAST                'msg'
              644  LOAD_METHOD              split
              646  LOAD_CONST               b'\x00'
              648  CALL_METHOD_1         1  ''
              650  UNPACK_SEQUENCE_2     2 
              652  STORE_FAST               'msgid1'
              654  STORE_FAST               'msgid2'

 L. 451       656  LOAD_FAST                'tmsg'
              658  LOAD_METHOD              split
              660  LOAD_CONST               b'\x00'
              662  CALL_METHOD_1         1  ''
              664  STORE_FAST               'tmsg'

 L. 452       666  LOAD_GLOBAL              str
              668  LOAD_FAST                'msgid1'
              670  LOAD_FAST                'charset'
              672  CALL_FUNCTION_2       2  ''
              674  STORE_FAST               'msgid1'

 L. 453       676  LOAD_GLOBAL              enumerate
              678  LOAD_FAST                'tmsg'
              680  CALL_FUNCTION_1       1  ''
              682  GET_ITER         
            684_0  COME_FROM           710  '710'
              684  FOR_ITER            714  'to 714'
              686  UNPACK_SEQUENCE_2     2 
              688  STORE_FAST               'i'
              690  STORE_FAST               'x'

 L. 454       692  LOAD_GLOBAL              str
              694  LOAD_FAST                'x'
              696  LOAD_FAST                'charset'
              698  CALL_FUNCTION_2       2  ''
              700  LOAD_FAST                'catalog'
              702  LOAD_FAST                'msgid1'
              704  LOAD_FAST                'i'
              706  BUILD_TUPLE_2         2 
              708  STORE_SUBSCR     
          710_712  JUMP_BACK           684  'to 684'
            714_0  COME_FROM           684  '684'
              714  JUMP_FORWARD        736  'to 736'
            716_0  COME_FROM           638  '638'

 L. 456       716  LOAD_GLOBAL              str
              718  LOAD_FAST                'tmsg'
              720  LOAD_FAST                'charset'
              722  CALL_FUNCTION_2       2  ''
              724  LOAD_FAST                'catalog'
              726  LOAD_GLOBAL              str
              728  LOAD_FAST                'msg'
              730  LOAD_FAST                'charset'
              732  CALL_FUNCTION_2       2  ''
              734  STORE_SUBSCR     
            736_0  COME_FROM           714  '714'

 L. 458       736  LOAD_FAST                'masteridx'
              738  LOAD_CONST               8
              740  INPLACE_ADD      
              742  STORE_FAST               'masteridx'

 L. 459       744  LOAD_FAST                'transidx'
              746  LOAD_CONST               8
              748  INPLACE_ADD      
              750  STORE_FAST               'transidx'
              752  JUMP_BACK           232  'to 232'
            754_0  COME_FROM           232  '232'

Parse error at or near `JUMP_BACK' instruction at offset 752

    def lgettext(self, message):
        import warnings
        warnings.warn('lgettext() is deprecated, use gettext() instead', DeprecationWarning, 2)
        missing = object()
        tmsg = self._catalog.get(message, missing)
        if tmsg is missing:
            if self._fallback:
                return self._fallback.lgettext(message)
            tmsg = message
        if self._output_charset:
            return tmsg.encode(self._output_charset)
        return tmsg.encode(locale.getpreferredencoding())

    def lngettext(self, msgid1, msgid2, n):
        import warnings
        warnings.warn('lngettext() is deprecated, use ngettext() instead', DeprecationWarning, 2)
        try:
            tmsg = self._catalog[(msgid1, self.plural(n))]
        except KeyError:
            if self._fallback:
                return self._fallback.lngettext(msgid1, msgid2, n)
            elif n == 1:
                tmsg = msgid1
            else:
                tmsg = msgid2
        else:
            if self._output_charset:
                return tmsg.encode(self._output_charset)
            else:
                return tmsg.encode(locale.getpreferredencoding())

    def gettext(self, message):
        missing = object()
        tmsg = self._catalog.get(message, missing)
        if tmsg is missing:
            if self._fallback:
                return self._fallback.gettext(message)
            return message
        return tmsg

    def ngettext(self, msgid1, msgid2, n):
        try:
            tmsg = self._catalog[(msgid1, self.plural(n))]
        except KeyError:
            if self._fallback:
                return self._fallback.ngettext(msgid1, msgid2, n)
            elif n == 1:
                tmsg = msgid1
            else:
                tmsg = msgid2
        else:
            return tmsg

    def pgettext(self, context, message):
        ctxt_msg_id = self.CONTEXT % (context, message)
        missing = object()
        tmsg = self._catalog.get(ctxt_msg_id, missing)
        if tmsg is missing:
            if self._fallback:
                return self._fallback.pgettext(context, message)
            return message
        return tmsg

    def npgettext(self, context, msgid1, msgid2, n):
        ctxt_msg_id = self.CONTEXT % (context, msgid1)
        try:
            tmsg = self._catalog[(ctxt_msg_id, self.plural(n))]
        except KeyError:
            if self._fallback:
                return self._fallback.npgettext(context, msgid1, msgid2, n)
            elif n == 1:
                tmsg = msgid1
            else:
                tmsg = msgid2
        else:
            return tmsg


def find(domain, localedir=None, languages=None, all=False):
    if localedir is None:
        localedir = _default_localedir
    if languages is None:
        languages = []
        for envar in ('LANGUAGE', 'LC_ALL', 'LC_MESSAGES', 'LANG'):
            val = os.environ.get(envar)
            if val:
                languages = val.split(':')
                break
        else:
            if 'C' not in languages:
                languages.append('C')

    nelangs = []
    for lang in languages:
        for nelang in _expand_lang(lang):
            if nelang not in nelangs:
                nelangs.append(nelang)

    else:
        if all:
            result = []
        else:
            result = None
        for lang in nelangs:
            if lang == 'C':
                break
            else:
                mofile = os.path.join(localedir, lang, 'LC_MESSAGES', '%s.mo' % domain)
            if os.path.exists(mofile):
                if all:
                    result.append(mofile)
                else:
                    return mofile
        else:
            return result


_translations = {}
_unspecified = [
 'unspecified']

def translation(domain, localedir=None, languages=None, class_=None, fallback=False, codeset=_unspecified):
    if class_ is None:
        class_ = GNUTranslations
    mofiles = find(domain, localedir, languages, all=True)
    if not mofiles:
        if fallback:
            return NullTranslations()
        from errno import ENOENT
        raise FileNotFoundError(ENOENT, 'No translation file found for domain', domain)
    result = None
    for mofile in mofiles:
        key = (
         class_, os.path.abspath(mofile))
        t = _translations.get(key)
        if t is None:
            with open(mofile, 'rb') as fp:
                t = _translations.setdefault(key, class_(fp))
        import copy
        t = copy.copy(t)
        if codeset is not _unspecified:
            import warnings
            warnings.warn('parameter codeset is deprecated', DeprecationWarning, 2)
            if codeset:
                with warnings.catch_warnings():
                    warnings.filterwarnings('ignore', '.*\\bset_output_charset\\b.*', DeprecationWarning)
                    t.set_output_charset(codeset)
        if result is None:
            result = t
        else:
            result.add_fallback(t)
    else:
        return result


def install(domain, localedir=None, codeset=_unspecified, names=None):
    t = translation(domain, localedir, fallback=True, codeset=codeset)
    t.install(names)


_localedirs = {}
_localecodesets = {}
_current_domain = 'messages'

def textdomain(domain=None):
    global _current_domain
    if domain is not None:
        _current_domain = domain
    return _current_domain


def bindtextdomain(domain, localedir=None):
    global _localedirs
    if localedir is not None:
        _localedirs[domain] = localedir
    return _localedirs.get(domain, _default_localedir)


def bind_textdomain_codeset(domain, codeset=None):
    global _localecodesets
    import warnings
    warnings.warn('bind_textdomain_codeset() is deprecated', DeprecationWarning, 2)
    if codeset is not None:
        _localecodesets[domain] = codeset
    return _localecodesets.get(domain)


def dgettext(domain, message):
    try:
        t = translation(domain, _localedirs.get(domain, None))
    except OSError:
        return message
    else:
        return t.gettext(message)


def ldgettext(domain, message):
    import warnings
    warnings.warn('ldgettext() is deprecated, use dgettext() instead', DeprecationWarning, 2)
    codeset = _localecodesets.get(domain)
    try:
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', '.*\\bparameter codeset\\b.*', DeprecationWarning)
            t = translation(domain, (_localedirs.get(domain, None)), codeset=codeset)
    except OSError:
        return message.encode(codeset or locale.getpreferredencoding())
    else:
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', '.*\\blgettext\\b.*', DeprecationWarning)
            return t.lgettext(message)


def dngettext(domain, msgid1, msgid2, n):
    try:
        t = translation(domain, _localedirs.get(domain, None))
    except OSError:
        if n == 1:
            return msgid1
        else:
            return msgid2
    else:
        return t.ngettext(msgid1, msgid2, n)


def ldngettext(domain, msgid1, msgid2, n):
    import warnings
    warnings.warn('ldngettext() is deprecated, use dngettext() instead', DeprecationWarning, 2)
    codeset = _localecodesets.get(domain)
    try:
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', '.*\\bparameter codeset\\b.*', DeprecationWarning)
            t = translation(domain, (_localedirs.get(domain, None)), codeset=codeset)
    except OSError:
        if n == 1:
            tmsg = msgid1
        else:
            tmsg = msgid2
        return tmsg.encode(codeset or locale.getpreferredencoding())
    else:
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', '.*\\blngettext\\b.*', DeprecationWarning)
            return t.lngettext(msgid1, msgid2, n)


def dpgettext(domain, context, message):
    try:
        t = translation(domain, _localedirs.get(domain, None))
    except OSError:
        return message
    else:
        return t.pgettext(context, message)


def dnpgettext(domain, context, msgid1, msgid2, n):
    try:
        t = translation(domain, _localedirs.get(domain, None))
    except OSError:
        if n == 1:
            return msgid1
        else:
            return msgid2
    else:
        return t.npgettext(context, msgid1, msgid2, n)


def gettext(message):
    return dgettext(_current_domain, message)


def lgettext(message):
    import warnings
    warnings.warn('lgettext() is deprecated, use gettext() instead', DeprecationWarning, 2)
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', '.*\\bldgettext\\b.*', DeprecationWarning)
        return ldgettext(_current_domain, message)


def ngettext(msgid1, msgid2, n):
    return dngettext(_current_domain, msgid1, msgid2, n)


def lngettext(msgid1, msgid2, n):
    import warnings
    warnings.warn('lngettext() is deprecated, use ngettext() instead', DeprecationWarning, 2)
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', '.*\\bldngettext\\b.*', DeprecationWarning)
        return ldngettext(_current_domain, msgid1, msgid2, n)


def pgettext(context, message):
    return dpgettext(_current_domain, context, message)


def npgettext(context, msgid1, msgid2, n):
    return dnpgettext(_current_domain, context, msgid1, msgid2, n)


Catalog = translation