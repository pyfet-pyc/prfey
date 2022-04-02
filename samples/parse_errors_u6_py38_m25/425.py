# uncompyle6 version 3.7.4
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
    while nexttok == '!':
        result += 'not '
        nexttok = next(tokens)

    if nexttok == '(':
        sub, nexttok = _parse(tokens)
        result = '%s(%s)' % (result, sub)
        if nexttok != ')':
            raise ValueError('unbalanced parenthesis in plural form')
    elif nexttok == 'n':
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
                    break
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


def c2py--- This code section failed: ---

 L. 181         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'plural'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_CONST               1000
                8  COMPARE_OP               >
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 182        12  LOAD_GLOBAL              ValueError
               14  LOAD_STR                 'plural form expression is too long'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 183        20  SETUP_FINALLY       146  'to 146'

 L. 184        22  LOAD_GLOBAL              _parse
               24  LOAD_GLOBAL              _tokenize
               26  LOAD_FAST                'plural'
               28  CALL_FUNCTION_1       1  ''
               30  CALL_FUNCTION_1       1  ''
               32  UNPACK_SEQUENCE_2     2 
               34  STORE_FAST               'result'
               36  STORE_FAST               'nexttok'

 L. 185        38  LOAD_FAST                'nexttok'
               40  POP_JUMP_IF_FALSE    50  'to 50'

 L. 186        42  LOAD_GLOBAL              _error
               44  LOAD_FAST                'nexttok'
               46  CALL_FUNCTION_1       1  ''
               48  RAISE_VARARGS_1       1  'exception instance'
             50_0  COME_FROM            40  '40'

 L. 188        50  LOAD_CONST               0
               52  STORE_FAST               'depth'

 L. 189        54  LOAD_FAST                'result'
               56  GET_ITER         
             58_0  COME_FROM           102  '102'
               58  FOR_ITER            114  'to 114'
               60  STORE_FAST               'c'

 L. 190        62  LOAD_FAST                'c'
               64  LOAD_STR                 '('
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE    96  'to 96'

 L. 191        70  LOAD_FAST                'depth'
               72  LOAD_CONST               1
               74  INPLACE_ADD      
               76  STORE_FAST               'depth'

 L. 192        78  LOAD_FAST                'depth'
               80  LOAD_CONST               20
               82  COMPARE_OP               >
               84  POP_JUMP_IF_FALSE   112  'to 112'

 L. 195        86  LOAD_GLOBAL              ValueError
               88  LOAD_STR                 'plural form expression is too complex'
               90  CALL_FUNCTION_1       1  ''
               92  RAISE_VARARGS_1       1  'exception instance'
               94  JUMP_BACK            58  'to 58'
             96_0  COME_FROM            68  '68'

 L. 196        96  LOAD_FAST                'c'
               98  LOAD_STR                 ')'
              100  COMPARE_OP               ==
              102  POP_JUMP_IF_FALSE    58  'to 58'

 L. 197       104  LOAD_FAST                'depth'
              106  LOAD_CONST               1
              108  INPLACE_SUBTRACT 
              110  STORE_FAST               'depth'
            112_0  COME_FROM            84  '84'
              112  JUMP_BACK            58  'to 58'

 L. 199       114  LOAD_STR                 '_as_int'
              116  LOAD_GLOBAL              _as_int
              118  BUILD_MAP_1           1 
              120  STORE_FAST               'ns'

 L. 200       122  LOAD_GLOBAL              exec
              124  LOAD_STR                 'if True:\n            def func(n):\n                if not isinstance(n, int):\n                    n = _as_int(n)\n                return int(%s)\n            '

 L. 205       126  LOAD_FAST                'result'

 L. 200       128  BINARY_MODULO    

 L. 205       130  LOAD_FAST                'ns'

 L. 200       132  CALL_FUNCTION_2       2  ''
              134  POP_TOP          

 L. 206       136  LOAD_FAST                'ns'
              138  LOAD_STR                 'func'
              140  BINARY_SUBSCR    
              142  POP_BLOCK        
              144  RETURN_VALUE     
            146_0  COME_FROM_FINALLY    20  '20'

 L. 207       146  DUP_TOP          
              148  LOAD_GLOBAL              RecursionError
              150  COMPARE_OP               exception-match
              152  POP_JUMP_IF_FALSE   172  'to 172'
              154  POP_TOP          
              156  POP_TOP          
              158  POP_TOP          

 L. 209       160  LOAD_GLOBAL              ValueError
              162  LOAD_STR                 'plural form expression is too complex'
              164  CALL_FUNCTION_1       1  ''
              166  RAISE_VARARGS_1       1  'exception instance'
              168  POP_EXCEPT       
              170  JUMP_FORWARD        174  'to 174'
            172_0  COME_FROM           152  '152'
              172  END_FINALLY      
            174_0  COME_FROM           170  '170'

Parse error at or near `POP_TOP' instruction at offset 156


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
            if i & COMPONENT_CODESET:
                val += codeset
            if i & COMPONENT_MODIFIER:
                val += modifier
            ret.append(val)
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

    def lgettext--- This code section failed: ---

 L. 278         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              warnings
                6  STORE_FAST               'warnings'

 L. 279         8  LOAD_FAST                'warnings'
               10  LOAD_METHOD              warn
               12  LOAD_STR                 'lgettext() is deprecated, use gettext() instead'

 L. 280        14  LOAD_GLOBAL              DeprecationWarning

 L. 280        16  LOAD_CONST               2

 L. 279        18  CALL_METHOD_3         3  ''
               20  POP_TOP          

 L. 281        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _fallback
               26  POP_JUMP_IF_FALSE    82  'to 82'

 L. 282        28  LOAD_FAST                'warnings'
               30  LOAD_METHOD              catch_warnings
               32  CALL_METHOD_0         0  ''
               34  SETUP_WITH           76  'to 76'
               36  POP_TOP          

 L. 283        38  LOAD_FAST                'warnings'
               40  LOAD_METHOD              filterwarnings
               42  LOAD_STR                 'ignore'
               44  LOAD_STR                 '.*\\blgettext\\b.*'

 L. 284        46  LOAD_GLOBAL              DeprecationWarning

 L. 283        48  CALL_METHOD_3         3  ''
               50  POP_TOP          

 L. 285        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _fallback
               56  LOAD_METHOD              lgettext
               58  LOAD_FAST                'message'
               60  CALL_METHOD_1         1  ''
               62  POP_BLOCK        
               64  ROT_TWO          
               66  BEGIN_FINALLY    
               68  WITH_CLEANUP_START
               70  WITH_CLEANUP_FINISH
               72  POP_FINALLY           0  ''
               74  RETURN_VALUE     
             76_0  COME_FROM_WITH       34  '34'
               76  WITH_CLEANUP_START
               78  WITH_CLEANUP_FINISH
               80  END_FINALLY      
             82_0  COME_FROM            26  '26'

 L. 286        82  LOAD_FAST                'self'
               84  LOAD_ATTR                _output_charset
               86  POP_JUMP_IF_FALSE   100  'to 100'

 L. 287        88  LOAD_FAST                'message'
               90  LOAD_METHOD              encode
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                _output_charset
               96  CALL_METHOD_1         1  ''
               98  RETURN_VALUE     
            100_0  COME_FROM            86  '86'

 L. 288       100  LOAD_FAST                'message'
              102  LOAD_METHOD              encode
              104  LOAD_GLOBAL              locale
              106  LOAD_METHOD              getpreferredencoding
              108  CALL_METHOD_0         0  ''
              110  CALL_METHOD_1         1  ''
              112  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_TWO' instruction at offset 64

    def ngettext(self, msgid1, msgid2, n):
        if self._fallback:
            return self._fallback.ngettext(msgid1, msgid2, n)
        if n == 1:
            return msgid1
        return msgid2

    def lngettext--- This code section failed: ---

 L. 299         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              warnings
                6  STORE_FAST               'warnings'

 L. 300         8  LOAD_FAST                'warnings'
               10  LOAD_METHOD              warn
               12  LOAD_STR                 'lngettext() is deprecated, use ngettext() instead'

 L. 301        14  LOAD_GLOBAL              DeprecationWarning

 L. 301        16  LOAD_CONST               2

 L. 300        18  CALL_METHOD_3         3  ''
               20  POP_TOP          

 L. 302        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _fallback
               26  POP_JUMP_IF_FALSE    86  'to 86'

 L. 303        28  LOAD_FAST                'warnings'
               30  LOAD_METHOD              catch_warnings
               32  CALL_METHOD_0         0  ''
               34  SETUP_WITH           80  'to 80'
               36  POP_TOP          

 L. 304        38  LOAD_FAST                'warnings'
               40  LOAD_METHOD              filterwarnings
               42  LOAD_STR                 'ignore'
               44  LOAD_STR                 '.*\\blngettext\\b.*'

 L. 305        46  LOAD_GLOBAL              DeprecationWarning

 L. 304        48  CALL_METHOD_3         3  ''
               50  POP_TOP          

 L. 306        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _fallback
               56  LOAD_METHOD              lngettext
               58  LOAD_FAST                'msgid1'
               60  LOAD_FAST                'msgid2'
               62  LOAD_FAST                'n'
               64  CALL_METHOD_3         3  ''
               66  POP_BLOCK        
               68  ROT_TWO          
               70  BEGIN_FINALLY    
               72  WITH_CLEANUP_START
               74  WITH_CLEANUP_FINISH
               76  POP_FINALLY           0  ''
               78  RETURN_VALUE     
             80_0  COME_FROM_WITH       34  '34'
               80  WITH_CLEANUP_START
               82  WITH_CLEANUP_FINISH
               84  END_FINALLY      
             86_0  COME_FROM            26  '26'

 L. 307        86  LOAD_FAST                'n'
               88  LOAD_CONST               1
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_FALSE   100  'to 100'

 L. 308        94  LOAD_FAST                'msgid1'
               96  STORE_FAST               'tmsg'
               98  JUMP_FORWARD        104  'to 104'
            100_0  COME_FROM            92  '92'

 L. 310       100  LOAD_FAST                'msgid2'
              102  STORE_FAST               'tmsg'
            104_0  COME_FROM            98  '98'

 L. 311       104  LOAD_FAST                'self'
              106  LOAD_ATTR                _output_charset
              108  POP_JUMP_IF_FALSE   122  'to 122'

 L. 312       110  LOAD_FAST                'tmsg'
              112  LOAD_METHOD              encode
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                _output_charset
              118  CALL_METHOD_1         1  ''
              120  RETURN_VALUE     
            122_0  COME_FROM           108  '108'

 L. 313       122  LOAD_FAST                'tmsg'
              124  LOAD_METHOD              encode
              126  LOAD_GLOBAL              locale
              128  LOAD_METHOD              getpreferredencoding
              130  CALL_METHOD_0         0  ''
              132  CALL_METHOD_1         1  ''
              134  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_TWO' instruction at offset 68

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

    def _parse(self, fp):
        """Override this method to support alternative .mo formats."""
        from struct import unpack
        filename = getattr(fp, 'name', '')
        self._catalog = catalog = {}
        self.plural = lambda n: int(n != 1)
        buf = fp.read()
        buflen = len(buf)
        magic = unpack('<I', buf[:4])[0]
        if magic == self.LE_MAGIC:
            version, msgcount, masteridx, transidx = unpack('<4I', buf[4:20])
            ii = '<II'
        else:
            if magic == self.BE_MAGIC:
                version, msgcount, masteridx, transidx = unpack('>4I', buf[4:20])
                ii = '>II'
            else:
                raise OSError(0, 'Bad magic number', filename)
        major_version, minor_version = self._get_versions(version)
        if major_version not in self.VERSIONS:
            raise OSError(0, 'Bad version number ' + str(major_version), filename)
        for i in range(0, msgcount):
            mlen, moff = unpack(ii, buf[masteridx:masteridx + 8])
            mend = moff + mlen
            tlen, toff = unpack(ii, buf[transidx:transidx + 8])
            tend = toff + tlen
            if mend < buflen and tend < buflen:
                msg = buf[moff:mend]
                tmsg = buf[toff:tend]
            else:
                raise OSError(0, 'File is corrupt', filename)
            if mlen == 0:
                lastk = None
                for b_item in tmsg.split(b'\n'):
                    item = b_item.decode().strip()
                    if not item:
                        pass
                    elif item.startswith('#-#-#-#-#') and item.endswith('#-#-#-#-#'):
                        pass
                    else:
                        k = v = None
                        if ':' in item:
                            k, v = item.split(':', 1)
                            k = k.strip().lower()
                            v = v.strip()
                            self._info[k] = v
                            lastk = k

            else:
                if lastk:
                    self._info[lastk] += '\n' + item
            if k == 'content-type':
                self._charset = v.split('charset=')[1]
            elif k == 'plural-forms':
                v = v.split(';')
                plural = v[1].split('plural=')[1]
                self.plural = c2py(plural)
            else:
                charset = self._charset or 'ascii'
                if b'\x00' in msg:
                    msgid1, msgid2 = msg.split(b'\x00')
                    tmsg = tmsg.split(b'\x00')
                    msgid1 = str(msgid1, charset)
                    for i, x in enumerate(tmsg):
                        catalog[(msgid1, i)] = str(x, charset)

                else:
                    catalog[str(msg, charset)] = str(tmsg, charset)
                masteridx += 8
                transidx += 8

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
                mofile = os.path.join(localedir, lang, 'LC_MESSAGES', '%s.mo' % domain)
                if os.path.exists(mofile):
                    if all:
                        result.append(mofile)
                    else:
                        return mofile
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
            with open(mofile, 'rb') as (fp):
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


def ldgettext--- This code section failed: ---

 L. 668         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              warnings
                6  STORE_FAST               'warnings'

 L. 669         8  LOAD_FAST                'warnings'
               10  LOAD_METHOD              warn
               12  LOAD_STR                 'ldgettext() is deprecated, use dgettext() instead'

 L. 670        14  LOAD_GLOBAL              DeprecationWarning

 L. 670        16  LOAD_CONST               2

 L. 669        18  CALL_METHOD_3         3  ''
               20  POP_TOP          

 L. 671        22  LOAD_GLOBAL              _localecodesets
               24  LOAD_METHOD              get
               26  LOAD_FAST                'domain'
               28  CALL_METHOD_1         1  ''
               30  STORE_FAST               'codeset'

 L. 672        32  SETUP_FINALLY        94  'to 94'

 L. 673        34  LOAD_FAST                'warnings'
               36  LOAD_METHOD              catch_warnings
               38  CALL_METHOD_0         0  ''
               40  SETUP_WITH           84  'to 84'
               42  POP_TOP          

 L. 674        44  LOAD_FAST                'warnings'
               46  LOAD_METHOD              filterwarnings
               48  LOAD_STR                 'ignore'
               50  LOAD_STR                 '.*\\bparameter codeset\\b.*'

 L. 675        52  LOAD_GLOBAL              DeprecationWarning

 L. 674        54  CALL_METHOD_3         3  ''
               56  POP_TOP          

 L. 676        58  LOAD_GLOBAL              translation
               60  LOAD_FAST                'domain'
               62  LOAD_GLOBAL              _localedirs
               64  LOAD_METHOD              get
               66  LOAD_FAST                'domain'
               68  LOAD_CONST               None
               70  CALL_METHOD_2         2  ''
               72  LOAD_FAST                'codeset'
               74  LOAD_CONST               ('codeset',)
               76  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               78  STORE_FAST               't'
               80  POP_BLOCK        
               82  BEGIN_FINALLY    
             84_0  COME_FROM_WITH       40  '40'
               84  WITH_CLEANUP_START
               86  WITH_CLEANUP_FINISH
               88  END_FINALLY      
               90  POP_BLOCK        
               92  JUMP_FORWARD        132  'to 132'
             94_0  COME_FROM_FINALLY    32  '32'

 L. 677        94  DUP_TOP          
               96  LOAD_GLOBAL              OSError
               98  COMPARE_OP               exception-match
              100  POP_JUMP_IF_FALSE   130  'to 130'
              102  POP_TOP          
              104  POP_TOP          
              106  POP_TOP          

 L. 678       108  LOAD_FAST                'message'
              110  LOAD_METHOD              encode
              112  LOAD_FAST                'codeset'
              114  JUMP_IF_TRUE_OR_POP   122  'to 122'
              116  LOAD_GLOBAL              locale
              118  LOAD_METHOD              getpreferredencoding
              120  CALL_METHOD_0         0  ''
            122_0  COME_FROM           114  '114'
              122  CALL_METHOD_1         1  ''
              124  ROT_FOUR         
              126  POP_EXCEPT       
              128  RETURN_VALUE     
            130_0  COME_FROM           100  '100'
              130  END_FINALLY      
            132_0  COME_FROM            92  '92'

 L. 679       132  LOAD_FAST                'warnings'
              134  LOAD_METHOD              catch_warnings
              136  CALL_METHOD_0         0  ''
              138  SETUP_WITH          178  'to 178'
              140  POP_TOP          

 L. 680       142  LOAD_FAST                'warnings'
              144  LOAD_METHOD              filterwarnings
              146  LOAD_STR                 'ignore'
              148  LOAD_STR                 '.*\\blgettext\\b.*'

 L. 681       150  LOAD_GLOBAL              DeprecationWarning

 L. 680       152  CALL_METHOD_3         3  ''
              154  POP_TOP          

 L. 682       156  LOAD_FAST                't'
              158  LOAD_METHOD              lgettext
              160  LOAD_FAST                'message'
              162  CALL_METHOD_1         1  ''
              164  POP_BLOCK        
              166  ROT_TWO          
              168  BEGIN_FINALLY    
              170  WITH_CLEANUP_START
              172  WITH_CLEANUP_FINISH
              174  POP_FINALLY           0  ''
              176  RETURN_VALUE     
            178_0  COME_FROM_WITH      138  '138'
              178  WITH_CLEANUP_START
              180  WITH_CLEANUP_FINISH
              182  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 166


def dngettext(domain, msgid1, msgid2, n):
    try:
        t = translation(domain, _localedirs.get(domain, None))
    except OSError:
        if n == 1:
            return msgid1
        return msgid2
    else:
        return t.ngettext(msgid1, msgid2, n)


def ldngettext--- This code section failed: ---

 L. 695         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              warnings
                6  STORE_FAST               'warnings'

 L. 696         8  LOAD_FAST                'warnings'
               10  LOAD_METHOD              warn
               12  LOAD_STR                 'ldngettext() is deprecated, use dngettext() instead'

 L. 697        14  LOAD_GLOBAL              DeprecationWarning

 L. 697        16  LOAD_CONST               2

 L. 696        18  CALL_METHOD_3         3  ''
               20  POP_TOP          

 L. 698        22  LOAD_GLOBAL              _localecodesets
               24  LOAD_METHOD              get
               26  LOAD_FAST                'domain'
               28  CALL_METHOD_1         1  ''
               30  STORE_FAST               'codeset'

 L. 699        32  SETUP_FINALLY        94  'to 94'

 L. 700        34  LOAD_FAST                'warnings'
               36  LOAD_METHOD              catch_warnings
               38  CALL_METHOD_0         0  ''
               40  SETUP_WITH           84  'to 84'
               42  POP_TOP          

 L. 701        44  LOAD_FAST                'warnings'
               46  LOAD_METHOD              filterwarnings
               48  LOAD_STR                 'ignore'
               50  LOAD_STR                 '.*\\bparameter codeset\\b.*'

 L. 702        52  LOAD_GLOBAL              DeprecationWarning

 L. 701        54  CALL_METHOD_3         3  ''
               56  POP_TOP          

 L. 703        58  LOAD_GLOBAL              translation
               60  LOAD_FAST                'domain'
               62  LOAD_GLOBAL              _localedirs
               64  LOAD_METHOD              get
               66  LOAD_FAST                'domain'
               68  LOAD_CONST               None
               70  CALL_METHOD_2         2  ''
               72  LOAD_FAST                'codeset'
               74  LOAD_CONST               ('codeset',)
               76  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               78  STORE_FAST               't'
               80  POP_BLOCK        
               82  BEGIN_FINALLY    
             84_0  COME_FROM_WITH       40  '40'
               84  WITH_CLEANUP_START
               86  WITH_CLEANUP_FINISH
               88  END_FINALLY      
               90  POP_BLOCK        
               92  JUMP_FORWARD        150  'to 150'
             94_0  COME_FROM_FINALLY    32  '32'

 L. 704        94  DUP_TOP          
               96  LOAD_GLOBAL              OSError
               98  COMPARE_OP               exception-match
              100  POP_JUMP_IF_FALSE   148  'to 148'
              102  POP_TOP          
              104  POP_TOP          
              106  POP_TOP          

 L. 705       108  LOAD_FAST                'n'
              110  LOAD_CONST               1
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   122  'to 122'

 L. 706       116  LOAD_FAST                'msgid1'
              118  STORE_FAST               'tmsg'
              120  JUMP_FORWARD        126  'to 126'
            122_0  COME_FROM           114  '114'

 L. 708       122  LOAD_FAST                'msgid2'
              124  STORE_FAST               'tmsg'
            126_0  COME_FROM           120  '120'

 L. 709       126  LOAD_FAST                'tmsg'
              128  LOAD_METHOD              encode
              130  LOAD_FAST                'codeset'
              132  JUMP_IF_TRUE_OR_POP   140  'to 140'
              134  LOAD_GLOBAL              locale
              136  LOAD_METHOD              getpreferredencoding
              138  CALL_METHOD_0         0  ''
            140_0  COME_FROM           132  '132'
              140  CALL_METHOD_1         1  ''
              142  ROT_FOUR         
              144  POP_EXCEPT       
              146  RETURN_VALUE     
            148_0  COME_FROM           100  '100'
              148  END_FINALLY      
            150_0  COME_FROM            92  '92'

 L. 710       150  LOAD_FAST                'warnings'
              152  LOAD_METHOD              catch_warnings
              154  CALL_METHOD_0         0  ''
              156  SETUP_WITH          200  'to 200'
              158  POP_TOP          

 L. 711       160  LOAD_FAST                'warnings'
              162  LOAD_METHOD              filterwarnings
              164  LOAD_STR                 'ignore'
              166  LOAD_STR                 '.*\\blngettext\\b.*'

 L. 712       168  LOAD_GLOBAL              DeprecationWarning

 L. 711       170  CALL_METHOD_3         3  ''
              172  POP_TOP          

 L. 713       174  LOAD_FAST                't'
              176  LOAD_METHOD              lngettext
              178  LOAD_FAST                'msgid1'
              180  LOAD_FAST                'msgid2'
              182  LOAD_FAST                'n'
              184  CALL_METHOD_3         3  ''
              186  POP_BLOCK        
              188  ROT_TWO          
              190  BEGIN_FINALLY    
              192  WITH_CLEANUP_START
              194  WITH_CLEANUP_FINISH
              196  POP_FINALLY           0  ''
              198  RETURN_VALUE     
            200_0  COME_FROM_WITH      156  '156'
              200  WITH_CLEANUP_START
              202  WITH_CLEANUP_FINISH
              204  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 188


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
        return msgid2
    else:
        return t.npgettext(context, msgid1, msgid2, n)


def gettext(message):
    return dgettext(_current_domain, message)


def lgettext--- This code section failed: ---

 L. 739         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              warnings
                6  STORE_FAST               'warnings'

 L. 740         8  LOAD_FAST                'warnings'
               10  LOAD_METHOD              warn
               12  LOAD_STR                 'lgettext() is deprecated, use gettext() instead'

 L. 741        14  LOAD_GLOBAL              DeprecationWarning

 L. 741        16  LOAD_CONST               2

 L. 740        18  CALL_METHOD_3         3  ''
               20  POP_TOP          

 L. 742        22  LOAD_FAST                'warnings'
               24  LOAD_METHOD              catch_warnings
               26  CALL_METHOD_0         0  ''
               28  SETUP_WITH           68  'to 68'
               30  POP_TOP          

 L. 743        32  LOAD_FAST                'warnings'
               34  LOAD_METHOD              filterwarnings
               36  LOAD_STR                 'ignore'
               38  LOAD_STR                 '.*\\bldgettext\\b.*'

 L. 744        40  LOAD_GLOBAL              DeprecationWarning

 L. 743        42  CALL_METHOD_3         3  ''
               44  POP_TOP          

 L. 745        46  LOAD_GLOBAL              ldgettext
               48  LOAD_GLOBAL              _current_domain
               50  LOAD_FAST                'message'
               52  CALL_FUNCTION_2       2  ''
               54  POP_BLOCK        
               56  ROT_TWO          
               58  BEGIN_FINALLY    
               60  WITH_CLEANUP_START
               62  WITH_CLEANUP_FINISH
               64  POP_FINALLY           0  ''
               66  RETURN_VALUE     
             68_0  COME_FROM_WITH       28  '28'
               68  WITH_CLEANUP_START
               70  WITH_CLEANUP_FINISH
               72  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 56


def ngettext(msgid1, msgid2, n):
    return dngettext(_current_domain, msgid1, msgid2, n)


def lngettext--- This code section failed: ---

 L. 751         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              warnings
                6  STORE_FAST               'warnings'

 L. 752         8  LOAD_FAST                'warnings'
               10  LOAD_METHOD              warn
               12  LOAD_STR                 'lngettext() is deprecated, use ngettext() instead'

 L. 753        14  LOAD_GLOBAL              DeprecationWarning

 L. 753        16  LOAD_CONST               2

 L. 752        18  CALL_METHOD_3         3  ''
               20  POP_TOP          

 L. 754        22  LOAD_FAST                'warnings'
               24  LOAD_METHOD              catch_warnings
               26  CALL_METHOD_0         0  ''
               28  SETUP_WITH           72  'to 72'
               30  POP_TOP          

 L. 755        32  LOAD_FAST                'warnings'
               34  LOAD_METHOD              filterwarnings
               36  LOAD_STR                 'ignore'
               38  LOAD_STR                 '.*\\bldngettext\\b.*'

 L. 756        40  LOAD_GLOBAL              DeprecationWarning

 L. 755        42  CALL_METHOD_3         3  ''
               44  POP_TOP          

 L. 757        46  LOAD_GLOBAL              ldngettext
               48  LOAD_GLOBAL              _current_domain
               50  LOAD_FAST                'msgid1'
               52  LOAD_FAST                'msgid2'
               54  LOAD_FAST                'n'
               56  CALL_FUNCTION_4       4  ''
               58  POP_BLOCK        
               60  ROT_TWO          
               62  BEGIN_FINALLY    
               64  WITH_CLEANUP_START
               66  WITH_CLEANUP_FINISH
               68  POP_FINALLY           0  ''
               70  RETURN_VALUE     
             72_0  COME_FROM_WITH       28  '28'
               72  WITH_CLEANUP_START
               74  WITH_CLEANUP_FINISH
               76  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 60


def pgettext(context, message):
    return dpgettext(_current_domain, context, message)


def npgettext(context, msgid1, msgid2, n):
    return dnpgettext(_current_domain, context, msgid1, msgid2, n)


Catalog = translation