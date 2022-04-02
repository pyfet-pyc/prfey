# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: soupsieve\css_parser.py
"""CSS selector parser."""
import re
from functools import lru_cache
from . import util
from . import css_match as cm
from . import css_types as ct
from .util import SelectorSyntaxError
UNICODE_REPLACEMENT_CHAR = 65533
PSEUDO_SIMPLE = {
 ':any-link',
 ':empty',
 ':first-child',
 ':first-of-type',
 ':in-range',
 ':out-of-range',
 ':last-child',
 ':last-of-type',
 ':link',
 ':only-child',
 ':only-of-type',
 ':root',
 ':checked',
 ':default',
 ':disabled',
 ':enabled',
 ':indeterminate',
 ':optional',
 ':placeholder-shown',
 ':read-only',
 ':read-write',
 ':required',
 ':scope',
 ':defined'}
PSEUDO_SIMPLE_NO_MATCH = {
 ':active',
 ':current',
 ':focus',
 ':focus-visible',
 ':focus-within',
 ':future',
 ':host',
 ':hover',
 ':local-link',
 ':past',
 ':paused',
 ':playing',
 ':target',
 ':target-within',
 ':user-invalid',
 ':visited'}
PSEUDO_COMPLEX = {
 ':contains',
 ':has',
 ':is',
 ':matches',
 ':not',
 ':where'}
PSEUDO_COMPLEX_NO_MATCH = {
 ':current',
 ':host',
 ':host-context'}
PSEUDO_SPECIAL = {
 ':dir',
 ':lang',
 ':nth-child',
 ':nth-last-child',
 ':nth-last-of-type',
 ':nth-of-type'}
PSEUDO_SUPPORTED = PSEUDO_SIMPLE | PSEUDO_SIMPLE_NO_MATCH | PSEUDO_COMPLEX | PSEUDO_COMPLEX_NO_MATCH | PSEUDO_SPECIAL
NEWLINE = '(?:\\r\\n|(?!\\r\\n)[\\n\\f\\r])'
WS = '(?:[ \\t]|{})'.format(NEWLINE)
COMMENTS = '(?:/\\*[^*]*\\*+(?:[^/*][^*]*\\*+)*/)'
WSC = '(?:{ws}|{comments})'.format(ws=WS, comments=COMMENTS)
CSS_ESCAPES = '(?:\\\\(?:[a-f0-9]{{1,6}}{ws}?|[^\\r\\n\\f]|$))'.format(ws=WS)
CSS_STRING_ESCAPES = '(?:\\\\(?:[a-f0-9]{{1,6}}{ws}?|[^\\r\\n\\f]|$|{nl}))'.format(ws=WS, nl=NEWLINE)
IDENTIFIER = '\n(?:(?:-?(?:[^\\x00-\\x2f\\x30-\\x40\\x5B-\\x5E\\x60\\x7B-\\x9f]|{esc})+|--)\n(?:[^\\x00-\\x2c\\x2e\\x2f\\x3A-\\x40\\x5B-\\x5E\\x60\\x7B-\\x9f]|{esc})*)\n'.format(esc=CSS_ESCAPES)
NTH = '(?:[-+])?(?:[0-9]+n?|n)(?:(?<=n){ws}*(?:[-+]){ws}*(?:[0-9]+))?'.format(ws=WSC)
VALUE = '\n(?:"(?:\\\\(?:.|{nl})|[^\\\\"\\r\\n\\f]+)*?"|\'(?:\\\\(?:.|{nl})|[^\\\\\'\\r\\n\\f]+)*?\'|{ident}+)\n'.format(nl=NEWLINE, ident=IDENTIFIER)
ATTR = '\n(?:{ws}*(?P<cmp>[!~^|*$]?=){ws}*(?P<value>{value})(?:{ws}+(?P<case>[is]))?)?{ws}*\\]\n'.format(ws=WSC, value=VALUE)
PAT_ID = '\\#{ident}'.format(ident=IDENTIFIER)
PAT_CLASS = '\\.{ident}'.format(ident=IDENTIFIER)
PAT_TAG = '(?P<tag_ns>(?:{ident}|\\*)?\\|)?(?P<tag_name>{ident}|\\*)'.format(ident=IDENTIFIER)
PAT_ATTR = '\n\\[{ws}*(?P<attr_ns>(?:{ident}|\\*)?\\|)?(?P<attr_name>{ident}){attr}\n'.format(ws=WSC, ident=IDENTIFIER, attr=ATTR)
PAT_PSEUDO_CLASS = '(?P<name>:{ident})(?P<open>\\({ws}*)?'.format(ws=WSC, ident=IDENTIFIER)
PAT_PSEUDO_CLASS_SPECIAL = '(?P<name>:{ident})(?P<open>\\({ws}*)'.format(ws=WSC, ident=IDENTIFIER)
PAT_PSEUDO_CLASS_CUSTOM = '(?P<name>:(?=--){ident})'.format(ident=IDENTIFIER)
PAT_PSEUDO_CLOSE = '{ws}*\\)'.format(ws=WSC)
PAT_PSEUDO_ELEMENT = ':{}'.format(PAT_PSEUDO_CLASS)
PAT_AT_RULE = '@P{ident}'.format(ident=IDENTIFIER)
PAT_PSEUDO_NTH_CHILD = '\n(?P<pseudo_nth_child>{name}\n(?P<nth_child>{nth}|even|odd))(?:{wsc}*\\)|(?P<of>{comments}*{ws}{wsc}*of{comments}*{ws}{wsc}*))\n'.format(name=PAT_PSEUDO_CLASS_SPECIAL, wsc=WSC, comments=COMMENTS, ws=WS, nth=NTH)
PAT_PSEUDO_NTH_TYPE = '\n(?P<pseudo_nth_type>{name}\n(?P<nth_type>{nth}|even|odd)){ws}*\\)\n'.format(name=PAT_PSEUDO_CLASS_SPECIAL, ws=WSC, nth=NTH)
PAT_PSEUDO_LANG = '{name}(?P<values>{value}(?:{ws}*,{ws}*{value})*){ws}*\\)'.format(name=PAT_PSEUDO_CLASS_SPECIAL,
  ws=WSC,
  value=VALUE)
PAT_PSEUDO_DIR = '{name}(?P<dir>ltr|rtl){ws}*\\)'.format(name=PAT_PSEUDO_CLASS_SPECIAL, ws=WSC)
PAT_COMBINE = '{wsc}*?(?P<relation>[,+>~]|{ws}(?![,+>~])){wsc}*'.format(ws=WS, wsc=WSC)
PAT_PSEUDO_CONTAINS = '{name}(?P<values>{value}(?:{ws}*,{ws}*{value})*){ws}*\\)'.format(name=PAT_PSEUDO_CLASS_SPECIAL,
  ws=WSC,
  value=VALUE)
RE_CSS_ESC = re.compile('(?:(\\\\[a-f0-9]{{1,6}}{ws}?)|(\\\\[^\\r\\n\\f])|(\\\\$))'.format(ws=WSC), re.I)
RE_CSS_STR_ESC = re.compile('(?:(\\\\[a-f0-9]{{1,6}}{ws}?)|(\\\\[^\\r\\n\\f])|(\\\\$)|(\\\\{nl}))'.format(ws=WS, nl=NEWLINE), re.I)
RE_NTH = re.compile('(?P<s1>[-+])?(?P<a>[0-9]+n?|n)(?:(?<=n){ws}*(?P<s2>[-+]){ws}*(?P<b>[0-9]+))?'.format(ws=WSC), re.I)
RE_VALUES = re.compile('(?:(?P<value>{value})|(?P<split>{ws}*,{ws}*))'.format(ws=WSC, value=VALUE), re.X)
RE_WS = re.compile(WS)
RE_WS_BEGIN = re.compile('^{}*'.format(WSC))
RE_WS_END = re.compile('{}*$'.format(WSC))
RE_CUSTOM = re.compile('^{}$'.format(PAT_PSEUDO_CLASS_CUSTOM), re.X)
COMMA_COMBINATOR = ','
WS_COMBINATOR = ' '
FLG_PSEUDO = 1
FLG_NOT = 2
FLG_RELATIVE = 4
FLG_DEFAULT = 8
FLG_HTML = 16
FLG_INDETERMINATE = 32
FLG_OPEN = 64
FLG_IN_RANGE = 128
FLG_OUT_OF_RANGE = 256
FLG_PLACEHOLDER_SHOWN = 512
_MAXCACHE = 500

@lru_cache(maxsize=_MAXCACHE)
def _cached_css_compile(pattern, namespaces, custom, flags):
    """Cached CSS compile."""
    custom_selectors = process_custom(custom)
    return cm.SoupSieve(pattern, CSSParser(pattern, custom=custom_selectors, flags=flags).process_selectors(), namespaces, custom, flags)


def _purge_cache():
    """Purge the cache."""
    _cached_css_compile.cache_clear()


def process_custom(custom):
    """Process custom."""
    custom_selectors = {}
    if custom is not None:
        for key, value in custom.items():
            name = util.lower(key)
            if RE_CUSTOM.match(name) is None:
                raise SelectorSyntaxError("The name '{}' is not a valid custom pseudo-class name".format(name))
            else:
                if name in custom_selectors:
                    raise KeyError("The custom selector '{}' has already been registered".format(name))
                custom_selectors[css_unescape(name)] = value

    return custom_selectors


def css_unescape(content, string=False):
    """
    Unescape CSS value.

    Strings allow for spanning the value on multiple strings by escaping a new line.
    """

    def replace(m):
        """Replace with the appropriate substitute."""
        if m.group(1):
            codepoint = int(m.group(1)[1:], 16)
            if codepoint == 0:
                codepoint = UNICODE_REPLACEMENT_CHAR
            value = chr(codepoint)
        elif m.group(2):
            value = m.group(2)[1:]
        elif m.group(3):
            value = '�'
        else:
            value = ''
        return value

    return RE_CSS_ESC if (not string) else RE_CSS_STR_ESC.sub(replace, content)


def escape--- This code section failed: ---

 L. 266         0  BUILD_LIST_0          0 
                2  STORE_FAST               'string'

 L. 267         4  LOAD_GLOBAL              len
                6  LOAD_FAST                'ident'
                8  CALL_FUNCTION_1       1  '1 positional argument'
               10  STORE_FAST               'length'

 L. 268        12  LOAD_FAST                'length'
               14  LOAD_CONST               0
               16  COMPARE_OP               >
               18  JUMP_IF_FALSE_OR_POP    30  'to 30'
               20  LOAD_FAST                'ident'
               22  LOAD_CONST               0
               24  BINARY_SUBSCR    
               26  LOAD_STR                 '-'
               28  COMPARE_OP               ==
             30_0  COME_FROM            18  '18'
               30  STORE_FAST               'start_dash'

 L. 269        32  LOAD_FAST                'length'
               34  LOAD_CONST               1
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE    64  'to 64'
               40  LOAD_FAST                'start_dash'
               42  POP_JUMP_IF_FALSE    64  'to 64'

 L. 271        44  LOAD_FAST                'string'
               46  LOAD_METHOD              append
               48  LOAD_STR                 '\\{}'
               50  LOAD_METHOD              format
               52  LOAD_FAST                'ident'
               54  CALL_METHOD_1         1  '1 positional argument'
               56  CALL_METHOD_1         1  '1 positional argument'
               58  POP_TOP          
            60_62  JUMP_FORWARD        382  'to 382'
             64_0  COME_FROM            42  '42'
             64_1  COME_FROM            38  '38'

 L. 273     64_66  SETUP_LOOP          382  'to 382'
               68  LOAD_GLOBAL              enumerate
               70  LOAD_FAST                'ident'
               72  CALL_FUNCTION_1       1  '1 positional argument'
               74  GET_ITER         
             76_0  COME_FROM           378  '378'
             76_1  COME_FROM           360  '360'
             76_2  COME_FROM           222  '222'
             76_3  COME_FROM           160  '160'
             76_4  COME_FROM           112  '112'
            76_78  FOR_ITER            380  'to 380'
               80  UNPACK_SEQUENCE_2     2 
               82  STORE_FAST               'index'
               84  STORE_FAST               'c'

 L. 274        86  LOAD_GLOBAL              ord
               88  LOAD_FAST                'c'
               90  CALL_FUNCTION_1       1  '1 positional argument'
               92  STORE_FAST               'codepoint'

 L. 275        94  LOAD_FAST                'codepoint'
               96  LOAD_CONST               0
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE   114  'to 114'

 L. 276       102  LOAD_FAST                'string'
              104  LOAD_METHOD              append
              106  LOAD_STR                 '�'
              108  CALL_METHOD_1         1  '1 positional argument'
              110  POP_TOP          
              112  JUMP_BACK            76  'to 76'
            114_0  COME_FROM           100  '100'

 L. 277       114  LOAD_CONST               1
              116  LOAD_FAST                'codepoint'
              118  DUP_TOP          
              120  ROT_THREE        
              122  COMPARE_OP               <=
              124  POP_JUMP_IF_FALSE   134  'to 134'
              126  LOAD_CONST               31
              128  COMPARE_OP               <=
              130  POP_JUMP_IF_TRUE    144  'to 144'
              132  JUMP_FORWARD        136  'to 136'
            134_0  COME_FROM           124  '124'
              134  POP_TOP          
            136_0  COME_FROM           132  '132'
              136  LOAD_FAST                'codepoint'
              138  LOAD_CONST               127
              140  COMPARE_OP               ==
              142  POP_JUMP_IF_FALSE   162  'to 162'
            144_0  COME_FROM           130  '130'

 L. 278       144  LOAD_FAST                'string'
              146  LOAD_METHOD              append
              148  LOAD_STR                 '\\{:x} '
              150  LOAD_METHOD              format
              152  LOAD_FAST                'codepoint'
              154  CALL_METHOD_1         1  '1 positional argument'
              156  CALL_METHOD_1         1  '1 positional argument'
              158  POP_TOP          
              160  JUMP_BACK            76  'to 76'
            162_0  COME_FROM           142  '142'

 L. 279       162  LOAD_FAST                'index'
              164  LOAD_CONST               0
              166  COMPARE_OP               ==
              168  POP_JUMP_IF_TRUE    182  'to 182'
              170  LOAD_FAST                'start_dash'
              172  POP_JUMP_IF_FALSE   224  'to 224'
              174  LOAD_FAST                'index'
              176  LOAD_CONST               1
              178  COMPARE_OP               ==
              180  POP_JUMP_IF_FALSE   224  'to 224'
            182_0  COME_FROM           168  '168'
              182  LOAD_CONST               48
              184  LOAD_FAST                'codepoint'
              186  DUP_TOP          
              188  ROT_THREE        
              190  COMPARE_OP               <=
              192  POP_JUMP_IF_FALSE   202  'to 202'
              194  LOAD_CONST               57
              196  COMPARE_OP               <=
              198  POP_JUMP_IF_FALSE   224  'to 224'
              200  JUMP_FORWARD        206  'to 206'
            202_0  COME_FROM           192  '192'
              202  POP_TOP          
              204  JUMP_FORWARD        224  'to 224'
            206_0  COME_FROM           200  '200'

 L. 280       206  LOAD_FAST                'string'
              208  LOAD_METHOD              append
              210  LOAD_STR                 '\\{:x} '
              212  LOAD_METHOD              format
              214  LOAD_FAST                'codepoint'
              216  CALL_METHOD_1         1  '1 positional argument'
              218  CALL_METHOD_1         1  '1 positional argument'
              220  POP_TOP          
              222  JUMP_BACK            76  'to 76'
            224_0  COME_FROM           204  '204'
            224_1  COME_FROM           198  '198'
            224_2  COME_FROM           180  '180'
            224_3  COME_FROM           172  '172'

 L. 282       224  LOAD_FAST                'codepoint'
              226  LOAD_CONST               (45, 95)
              228  COMPARE_OP               in
          230_232  POP_JUMP_IF_TRUE    350  'to 350'
              234  LOAD_FAST                'codepoint'
              236  LOAD_CONST               128
              238  COMPARE_OP               >=
          240_242  POP_JUMP_IF_TRUE    350  'to 350'
              244  LOAD_CONST               48
              246  LOAD_FAST                'codepoint'
              248  DUP_TOP          
              250  ROT_THREE        
              252  COMPARE_OP               <=
          254_256  POP_JUMP_IF_FALSE   268  'to 268'
              258  LOAD_CONST               57
              260  COMPARE_OP               <=
          262_264  POP_JUMP_IF_TRUE    350  'to 350'
              266  JUMP_FORWARD        270  'to 270'
            268_0  COME_FROM           254  '254'
              268  POP_TOP          
            270_0  COME_FROM           266  '266'

 L. 283       270  LOAD_CONST               48
              272  LOAD_FAST                'codepoint'
              274  DUP_TOP          
              276  ROT_THREE        
              278  COMPARE_OP               <=
          280_282  POP_JUMP_IF_FALSE   294  'to 294'
              284  LOAD_CONST               57
              286  COMPARE_OP               <=
          288_290  POP_JUMP_IF_TRUE    350  'to 350'
              292  JUMP_FORWARD        296  'to 296'
            294_0  COME_FROM           280  '280'
              294  POP_TOP          
            296_0  COME_FROM           292  '292'
              296  LOAD_CONST               65
              298  LOAD_FAST                'codepoint'
              300  DUP_TOP          
              302  ROT_THREE        
              304  COMPARE_OP               <=
          306_308  POP_JUMP_IF_FALSE   320  'to 320'
              310  LOAD_CONST               90
              312  COMPARE_OP               <=
          314_316  POP_JUMP_IF_TRUE    350  'to 350'
              318  JUMP_FORWARD        322  'to 322'
            320_0  COME_FROM           306  '306'
              320  POP_TOP          
            322_0  COME_FROM           318  '318'
              322  LOAD_CONST               97
              324  LOAD_FAST                'codepoint'
              326  DUP_TOP          
              328  ROT_THREE        
              330  COMPARE_OP               <=
          332_334  POP_JUMP_IF_FALSE   346  'to 346'
              336  LOAD_CONST               122
              338  COMPARE_OP               <=
          340_342  POP_JUMP_IF_FALSE   362  'to 362'
              344  JUMP_FORWARD        350  'to 350'
            346_0  COME_FROM           332  '332'
              346  POP_TOP          
              348  JUMP_FORWARD        362  'to 362'
            350_0  COME_FROM           344  '344'
            350_1  COME_FROM           314  '314'
            350_2  COME_FROM           288  '288'
            350_3  COME_FROM           262  '262'
            350_4  COME_FROM           240  '240'
            350_5  COME_FROM           230  '230'

 L. 285       350  LOAD_FAST                'string'
              352  LOAD_METHOD              append
              354  LOAD_FAST                'c'
              356  CALL_METHOD_1         1  '1 positional argument'
              358  POP_TOP          
              360  JUMP_BACK            76  'to 76'
            362_0  COME_FROM           348  '348'
            362_1  COME_FROM           340  '340'

 L. 287       362  LOAD_FAST                'string'
              364  LOAD_METHOD              append
              366  LOAD_STR                 '\\{}'
              368  LOAD_METHOD              format
              370  LOAD_FAST                'c'
              372  CALL_METHOD_1         1  '1 positional argument'
              374  CALL_METHOD_1         1  '1 positional argument'
              376  POP_TOP          
              378  JUMP_BACK            76  'to 76'
              380  POP_BLOCK        
            382_0  COME_FROM_LOOP       64  '64'
            382_1  COME_FROM            60  '60'

 L. 288       382  LOAD_STR                 ''
              384  LOAD_METHOD              join
              386  LOAD_FAST                'string'
              388  CALL_METHOD_1         1  '1 positional argument'
              390  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 382_0


class SelectorPattern(object):
    __doc__ = 'Selector pattern.'

    def __init__(self, name, pattern):
        """Initialize."""
        self.name = name
        self.re_pattern = re.compile(pattern, re.I | re.X | re.U)

    def get_name(self):
        """Get name."""
        return self.name

    def match(self, selector, index, flags):
        """Match the selector."""
        return self.re_pattern.match(selector, index)


class SpecialPseudoPattern(SelectorPattern):
    __doc__ = 'Selector pattern.'

    def __init__(self, patterns):
        """Initialize."""
        self.patterns = {}
        for p in patterns:
            name = p[0]
            pattern = p[3](name, p[2])
            for pseudo in p[1]:
                self.patterns[pseudo] = pattern

        self.matched_name = None
        self.re_pseudo_name = re.compile(PAT_PSEUDO_CLASS_SPECIAL, re.I | re.X | re.U)

    def get_name(self):
        """Get name."""
        return self.matched_name.get_name()

    def match(self, selector, index, flags):
        """Match the selector."""
        pseudo = None
        m = self.re_pseudo_name.match(selector, index)
        if m:
            name = util.lower(css_unescape(m.group('name')))
            pattern = self.patterns.get(name)
            if pattern:
                pseudo = pattern.match(selector, index, flags)
                if pseudo:
                    self.matched_name = pattern
        return pseudo


class _Selector(object):
    __doc__ = '\n    Intermediate selector class.\n\n    This stores selector data for a compound selector as we are acquiring them.\n    Once we are done collecting the data for a compound selector, we freeze\n    the data in an object that can be pickled and hashed.\n    '

    def __init__(self, **kwargs):
        """Initialize."""
        self.tag = kwargs.get('tag', None)
        self.ids = kwargs.get('ids', [])
        self.classes = kwargs.get('classes', [])
        self.attributes = kwargs.get('attributes', [])
        self.nth = kwargs.get('nth', [])
        self.selectors = kwargs.get('selectors', [])
        self.relations = kwargs.get('relations', [])
        self.rel_type = kwargs.get('rel_type', None)
        self.contains = kwargs.get('contains', [])
        self.lang = kwargs.get('lang', [])
        self.flags = kwargs.get('flags', 0)
        self.no_match = kwargs.get('no_match', False)

    def _freeze_relations(self, relations):
        """Freeze relation."""
        if relations:
            sel = relations[0]
            sel.relations.extend(relations[1:])
            return ct.SelectorList([sel.freeze()])
        return ct.SelectorList()

    def freeze(self):
        """Freeze self."""
        if self.no_match:
            return ct.SelectorNull()
        return ct.Selector(self.tag, tuple(self.ids), tuple(self.classes), tuple(self.attributes), tuple(self.nth), tuple(self.selectors), self._freeze_relations(self.relations), self.rel_type, tuple(self.contains), tuple(self.lang), self.flags)

    def __str__(self):
        """String representation."""
        return '_Selector(tag={!r}, ids={!r}, classes={!r}, attributes={!r}, nth={!r}, selectors={!r}, relations={!r}, rel_type={!r}, contains={!r}, lang={!r}, flags={!r}, no_match={!r})'.format(self.tag, self.ids, self.classes, self.attributes, self.nth, self.selectors, self.relations, self.rel_type, self.contains, self.lang, self.flags, self.no_match)

    __repr__ = __str__


class CSSParser(object):
    __doc__ = 'Parse CSS selectors.'
    css_tokens = (
     SelectorPattern('pseudo_close', PAT_PSEUDO_CLOSE),
     SpecialPseudoPattern((
      (
       'pseudo_contains', (':contains', ), PAT_PSEUDO_CONTAINS, SelectorPattern),
      (
       'pseudo_nth_child', (':nth-child', ':nth-last-child'), PAT_PSEUDO_NTH_CHILD, SelectorPattern),
      (
       'pseudo_nth_type', (':nth-of-type', ':nth-last-of-type'), PAT_PSEUDO_NTH_TYPE, SelectorPattern),
      (
       'pseudo_lang', (':lang', ), PAT_PSEUDO_LANG, SelectorPattern),
      (
       'pseudo_dir', (':dir', ), PAT_PSEUDO_DIR, SelectorPattern))),
     SelectorPattern('pseudo_class_custom', PAT_PSEUDO_CLASS_CUSTOM),
     SelectorPattern('pseudo_class', PAT_PSEUDO_CLASS),
     SelectorPattern('pseudo_element', PAT_PSEUDO_ELEMENT),
     SelectorPattern('at_rule', PAT_AT_RULE),
     SelectorPattern('id', PAT_ID),
     SelectorPattern('class', PAT_CLASS),
     SelectorPattern('tag', PAT_TAG),
     SelectorPattern('attribute', PAT_ATTR),
     SelectorPattern('combine', PAT_COMBINE))

    def __init__(self, selector, custom=None, flags=0):
        """Initialize."""
        self.pattern = selector.replace('\x00', '�')
        self.flags = flags
        self.debug = self.flags & util.DEBUG
        self.custom = {} if custom is None else custom

    def parse_attribute_selector--- This code section failed: ---

 L. 453         0  LOAD_CONST               False
                2  STORE_FAST               'inverse'

 L. 454         4  LOAD_FAST                'm'
                6  LOAD_METHOD              group
                8  LOAD_STR                 'cmp'
               10  CALL_METHOD_1         1  '1 positional argument'
               12  STORE_FAST               'op'

 L. 455        14  LOAD_FAST                'm'
               16  LOAD_METHOD              group
               18  LOAD_STR                 'case'
               20  CALL_METHOD_1         1  '1 positional argument'
               22  POP_JUMP_IF_FALSE    40  'to 40'
               24  LOAD_GLOBAL              util
               26  LOAD_METHOD              lower
               28  LOAD_FAST                'm'
               30  LOAD_METHOD              group
               32  LOAD_STR                 'case'
               34  CALL_METHOD_1         1  '1 positional argument'
               36  CALL_METHOD_1         1  '1 positional argument'
               38  JUMP_FORWARD         42  'to 42'
             40_0  COME_FROM            22  '22'
               40  LOAD_CONST               None
             42_0  COME_FROM            38  '38'
               42  STORE_FAST               'case'

 L. 456        44  LOAD_FAST                'm'
               46  LOAD_METHOD              group
               48  LOAD_STR                 'attr_ns'
               50  CALL_METHOD_1         1  '1 positional argument'
               52  POP_JUMP_IF_FALSE    76  'to 76'
               54  LOAD_GLOBAL              css_unescape
               56  LOAD_FAST                'm'
               58  LOAD_METHOD              group
               60  LOAD_STR                 'attr_ns'
               62  CALL_METHOD_1         1  '1 positional argument'
               64  LOAD_CONST               None
               66  LOAD_CONST               -1
               68  BUILD_SLICE_2         2 
               70  BINARY_SUBSCR    
               72  CALL_FUNCTION_1       1  '1 positional argument'
               74  JUMP_FORWARD         78  'to 78'
             76_0  COME_FROM            52  '52'
               76  LOAD_STR                 ''
             78_0  COME_FROM            74  '74'
               78  STORE_FAST               'ns'

 L. 457        80  LOAD_GLOBAL              css_unescape
               82  LOAD_FAST                'm'
               84  LOAD_METHOD              group
               86  LOAD_STR                 'attr_name'
               88  CALL_METHOD_1         1  '1 positional argument'
               90  CALL_FUNCTION_1       1  '1 positional argument'
               92  STORE_FAST               'attr'

 L. 458        94  LOAD_CONST               False
               96  STORE_FAST               'is_type'

 L. 459        98  LOAD_CONST               None
              100  STORE_FAST               'pattern2'

 L. 461       102  LOAD_FAST                'case'
              104  POP_JUMP_IF_FALSE   126  'to 126'

 L. 462       106  LOAD_FAST                'case'
              108  LOAD_STR                 'i'
              110  COMPARE_OP               ==
              112  POP_JUMP_IF_FALSE   120  'to 120'
              114  LOAD_GLOBAL              re
              116  LOAD_ATTR                I
              118  JUMP_FORWARD        122  'to 122'
            120_0  COME_FROM           112  '112'
              120  LOAD_CONST               0
            122_0  COME_FROM           118  '118'
              122  STORE_FAST               'flags'
              124  JUMP_FORWARD        156  'to 156'
            126_0  COME_FROM           104  '104'

 L. 463       126  LOAD_GLOBAL              util
              128  LOAD_METHOD              lower
              130  LOAD_FAST                'attr'
              132  CALL_METHOD_1         1  '1 positional argument'
              134  LOAD_STR                 'type'
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_FALSE   152  'to 152'

 L. 464       140  LOAD_GLOBAL              re
              142  LOAD_ATTR                I
              144  STORE_FAST               'flags'

 L. 465       146  LOAD_CONST               True
              148  STORE_FAST               'is_type'
              150  JUMP_FORWARD        156  'to 156'
            152_0  COME_FROM           138  '138'

 L. 467       152  LOAD_CONST               0
              154  STORE_FAST               'flags'
            156_0  COME_FROM           150  '150'
            156_1  COME_FROM           124  '124'

 L. 469       156  LOAD_FAST                'op'
              158  POP_JUMP_IF_FALSE   218  'to 218'

 L. 470       160  LOAD_FAST                'm'
              162  LOAD_METHOD              group
              164  LOAD_STR                 'value'
              166  CALL_METHOD_1         1  '1 positional argument'
              168  LOAD_METHOD              startswith
              170  LOAD_CONST               ('"', "'")
              172  CALL_METHOD_1         1  '1 positional argument'
              174  POP_JUMP_IF_FALSE   202  'to 202'

 L. 471       176  LOAD_GLOBAL              css_unescape
              178  LOAD_FAST                'm'
              180  LOAD_METHOD              group
              182  LOAD_STR                 'value'
              184  CALL_METHOD_1         1  '1 positional argument'
              186  LOAD_CONST               1
              188  LOAD_CONST               -1
              190  BUILD_SLICE_2         2 
              192  BINARY_SUBSCR    
              194  LOAD_CONST               True
              196  CALL_FUNCTION_2       2  '2 positional arguments'
              198  STORE_FAST               'value'
              200  JUMP_FORWARD        222  'to 222'
            202_0  COME_FROM           174  '174'

 L. 473       202  LOAD_GLOBAL              css_unescape
              204  LOAD_FAST                'm'
              206  LOAD_METHOD              group
              208  LOAD_STR                 'value'
              210  CALL_METHOD_1         1  '1 positional argument'
              212  CALL_FUNCTION_1       1  '1 positional argument'
              214  STORE_FAST               'value'
              216  JUMP_FORWARD        222  'to 222'
            218_0  COME_FROM           158  '158'

 L. 475       218  LOAD_CONST               None
              220  STORE_FAST               'value'
            222_0  COME_FROM           216  '216'
            222_1  COME_FROM           200  '200'

 L. 476       222  LOAD_FAST                'op'
              224  POP_JUMP_IF_TRUE    232  'to 232'

 L. 478       226  LOAD_CONST               None
              228  STORE_FAST               'pattern'
              230  JUMP_FORWARD        476  'to 476'
            232_0  COME_FROM           224  '224'

 L. 479       232  LOAD_FAST                'op'
              234  LOAD_METHOD              startswith
              236  LOAD_STR                 '^'
              238  CALL_METHOD_1         1  '1 positional argument'
          240_242  POP_JUMP_IF_FALSE   268  'to 268'

 L. 481       244  LOAD_GLOBAL              re
              246  LOAD_METHOD              compile
              248  LOAD_STR                 '^%s.*'
              250  LOAD_GLOBAL              re
              252  LOAD_METHOD              escape
              254  LOAD_FAST                'value'
              256  CALL_METHOD_1         1  '1 positional argument'
              258  BINARY_MODULO    
              260  LOAD_FAST                'flags'
              262  CALL_METHOD_2         2  '2 positional arguments'
              264  STORE_FAST               'pattern'
              266  JUMP_FORWARD        476  'to 476'
            268_0  COME_FROM           240  '240'

 L. 482       268  LOAD_FAST                'op'
              270  LOAD_METHOD              startswith
              272  LOAD_STR                 '$'
              274  CALL_METHOD_1         1  '1 positional argument'
          276_278  POP_JUMP_IF_FALSE   304  'to 304'

 L. 484       280  LOAD_GLOBAL              re
              282  LOAD_METHOD              compile
              284  LOAD_STR                 '.*?%s$'
              286  LOAD_GLOBAL              re
              288  LOAD_METHOD              escape
              290  LOAD_FAST                'value'
              292  CALL_METHOD_1         1  '1 positional argument'
              294  BINARY_MODULO    
              296  LOAD_FAST                'flags'
              298  CALL_METHOD_2         2  '2 positional arguments'
              300  STORE_FAST               'pattern'
              302  JUMP_FORWARD        476  'to 476'
            304_0  COME_FROM           276  '276'

 L. 485       304  LOAD_FAST                'op'
              306  LOAD_METHOD              startswith
              308  LOAD_STR                 '*'
              310  CALL_METHOD_1         1  '1 positional argument'
          312_314  POP_JUMP_IF_FALSE   340  'to 340'

 L. 487       316  LOAD_GLOBAL              re
              318  LOAD_METHOD              compile
              320  LOAD_STR                 '.*?%s.*'
              322  LOAD_GLOBAL              re
              324  LOAD_METHOD              escape
              326  LOAD_FAST                'value'
              328  CALL_METHOD_1         1  '1 positional argument'
              330  BINARY_MODULO    
              332  LOAD_FAST                'flags'
              334  CALL_METHOD_2         2  '2 positional arguments'
              336  STORE_FAST               'pattern'
              338  JUMP_FORWARD        476  'to 476'
            340_0  COME_FROM           312  '312'

 L. 488       340  LOAD_FAST                'op'
              342  LOAD_METHOD              startswith
              344  LOAD_STR                 '~'
              346  CALL_METHOD_1         1  '1 positional argument'
          348_350  POP_JUMP_IF_FALSE   402  'to 402'

 L. 492       352  LOAD_FAST                'value'
          354_356  POP_JUMP_IF_FALSE   370  'to 370'
              358  LOAD_GLOBAL              RE_WS
              360  LOAD_METHOD              search
              362  LOAD_FAST                'value'
              364  CALL_METHOD_1         1  '1 positional argument'
          366_368  POP_JUMP_IF_FALSE   374  'to 374'
            370_0  COME_FROM           354  '354'
              370  LOAD_STR                 '[^\\s\\S]'
              372  JUMP_FORWARD        382  'to 382'
            374_0  COME_FROM           366  '366'
              374  LOAD_GLOBAL              re
              376  LOAD_METHOD              escape
              378  LOAD_FAST                'value'
              380  CALL_METHOD_1         1  '1 positional argument'
            382_0  COME_FROM           372  '372'
              382  STORE_FAST               'value'

 L. 493       384  LOAD_GLOBAL              re
              386  LOAD_METHOD              compile
              388  LOAD_STR                 '.*?(?:(?<=^)|(?<=[ \\t\\r\\n\\f]))%s(?=(?:[ \\t\\r\\n\\f]|$)).*'
              390  LOAD_FAST                'value'
              392  BINARY_MODULO    
              394  LOAD_FAST                'flags'
              396  CALL_METHOD_2         2  '2 positional arguments'
              398  STORE_FAST               'pattern'
              400  JUMP_FORWARD        476  'to 476'
            402_0  COME_FROM           348  '348'

 L. 494       402  LOAD_FAST                'op'
              404  LOAD_METHOD              startswith
              406  LOAD_STR                 '|'
              408  CALL_METHOD_1         1  '1 positional argument'
          410_412  POP_JUMP_IF_FALSE   438  'to 438'

 L. 496       414  LOAD_GLOBAL              re
              416  LOAD_METHOD              compile
              418  LOAD_STR                 '^%s(?:-.*)?$'
              420  LOAD_GLOBAL              re
              422  LOAD_METHOD              escape
              424  LOAD_FAST                'value'
              426  CALL_METHOD_1         1  '1 positional argument'
              428  BINARY_MODULO    
              430  LOAD_FAST                'flags'
              432  CALL_METHOD_2         2  '2 positional arguments'
              434  STORE_FAST               'pattern'
              436  JUMP_FORWARD        476  'to 476'
            438_0  COME_FROM           410  '410'

 L. 499       438  LOAD_GLOBAL              re
              440  LOAD_METHOD              compile
              442  LOAD_STR                 '^%s$'
              444  LOAD_GLOBAL              re
              446  LOAD_METHOD              escape
              448  LOAD_FAST                'value'
              450  CALL_METHOD_1         1  '1 positional argument'
              452  BINARY_MODULO    
              454  LOAD_FAST                'flags'
              456  CALL_METHOD_2         2  '2 positional arguments'
              458  STORE_FAST               'pattern'

 L. 500       460  LOAD_FAST                'op'
              462  LOAD_METHOD              startswith
              464  LOAD_STR                 '!'
              466  CALL_METHOD_1         1  '1 positional argument'
          468_470  POP_JUMP_IF_FALSE   476  'to 476'

 L. 502       472  LOAD_CONST               True
              474  STORE_FAST               'inverse'
            476_0  COME_FROM           468  '468'
            476_1  COME_FROM           436  '436'
            476_2  COME_FROM           400  '400'
            476_3  COME_FROM           338  '338'
            476_4  COME_FROM           302  '302'
            476_5  COME_FROM           266  '266'
            476_6  COME_FROM           230  '230'

 L. 503       476  LOAD_FAST                'is_type'
          478_480  POP_JUMP_IF_FALSE   500  'to 500'
              482  LOAD_FAST                'pattern'
          484_486  POP_JUMP_IF_FALSE   500  'to 500'

 L. 504       488  LOAD_GLOBAL              re
              490  LOAD_METHOD              compile
              492  LOAD_FAST                'pattern'
              494  LOAD_ATTR                pattern
              496  CALL_METHOD_1         1  '1 positional argument'
              498  STORE_FAST               'pattern2'
            500_0  COME_FROM           484  '484'
            500_1  COME_FROM           478  '478'

 L. 507       500  LOAD_GLOBAL              ct
              502  LOAD_METHOD              SelectorAttribute
              504  LOAD_FAST                'attr'
              506  LOAD_FAST                'ns'
              508  LOAD_FAST                'pattern'
              510  LOAD_FAST                'pattern2'
              512  CALL_METHOD_4         4  '4 positional arguments'
              514  STORE_FAST               'sel_attr'

 L. 508       516  LOAD_FAST                'inverse'
          518_520  POP_JUMP_IF_FALSE   574  'to 574'

 L. 510       522  LOAD_GLOBAL              _Selector
              524  CALL_FUNCTION_0       0  '0 positional arguments'
              526  STORE_FAST               'sub_sel'

 L. 511       528  LOAD_FAST                'sub_sel'
              530  LOAD_ATTR                attributes
              532  LOAD_METHOD              append
              534  LOAD_FAST                'sel_attr'
              536  CALL_METHOD_1         1  '1 positional argument'
              538  POP_TOP          

 L. 512       540  LOAD_GLOBAL              ct
              542  LOAD_METHOD              SelectorList
              544  LOAD_FAST                'sub_sel'
              546  LOAD_METHOD              freeze
              548  CALL_METHOD_0         0  '0 positional arguments'
              550  BUILD_LIST_1          1 
              552  LOAD_CONST               True
              554  LOAD_CONST               False
              556  CALL_METHOD_3         3  '3 positional arguments'
              558  STORE_FAST               'not_list'

 L. 513       560  LOAD_FAST                'sel'
              562  LOAD_ATTR                selectors
              564  LOAD_METHOD              append
              566  LOAD_FAST                'not_list'
              568  CALL_METHOD_1         1  '1 positional argument'
              570  POP_TOP          
              572  JUMP_FORWARD        586  'to 586'
            574_0  COME_FROM           518  '518'

 L. 515       574  LOAD_FAST                'sel'
              576  LOAD_ATTR                attributes
              578  LOAD_METHOD              append
              580  LOAD_FAST                'sel_attr'
              582  CALL_METHOD_1         1  '1 positional argument'
              584  POP_TOP          
            586_0  COME_FROM           572  '572'

 L. 517       586  LOAD_CONST               True
              588  STORE_FAST               'has_selector'

 L. 518       590  LOAD_FAST                'has_selector'
              592  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 374_0

    def parse_tag_pattern(self, sel, m, has_selector):
        """Parse tag pattern from regex match."""
        prefix = css_unescape(m.group('tag_ns')[:-1]) if m.group('tag_ns') else None
        tag = css_unescape(m.group('tag_name'))
        sel.tag = ct.SelectorTag(tag, prefix)
        has_selector = True
        return has_selector

    def parse_pseudo_class_custom(self, sel, m, has_selector):
        """
        Parse custom pseudo class alias.

        Compile custom selectors as we need them. When compiling a custom selector,
        set it to `None` in the dictionary so we can avoid an infinite loop.
        """
        pseudo = util.lower(css_unescape(m.group('name')))
        selector = self.custom.get(pseudo)
        if selector is None:
            raise SelectorSyntaxError("Undefined custom selector '{}' found at postion {}".format(pseudo, m.end(0)), self.pattern, m.end(0))
        if not isinstance(selector, ct.SelectorList):
            self.custom[pseudo] = None
            selector = CSSParser(selector,
              custom=(self.custom), flags=(self.flags)).process_selectors(flags=FLG_PSEUDO)
            self.custom[pseudo] = selector
        sel.selectors.append(selector)
        has_selector = True
        return has_selector

    def parse_pseudo_class(self, sel, m, has_selector, iselector, is_html):
        """Parse pseudo class."""
        complex_pseudo = False
        pseudo = util.lower(css_unescape(m.group('name')))
        if m.group('open'):
            complex_pseudo = True
        if complex_pseudo and pseudo in PSEUDO_COMPLEX:
            has_selector = self.parse_pseudo_open(sel, pseudo, has_selector, iselector, m.end(0))
        elif not complex_pseudo or pseudo in PSEUDO_SIMPLE:
            if pseudo == ':root':
                sel.flags |= ct.SEL_ROOT
            elif pseudo == ':defined':
                sel.flags |= ct.SEL_DEFINED
                is_html = True
            elif pseudo == ':scope':
                sel.flags |= ct.SEL_SCOPE
            elif pseudo == ':empty':
                sel.flags |= ct.SEL_EMPTY
            elif pseudo in (':link', ':any-link'):
                sel.selectors.append(CSS_LINK)
            elif pseudo == ':checked':
                sel.selectors.append(CSS_CHECKED)
            elif pseudo == ':default':
                sel.selectors.append(CSS_DEFAULT)
            elif pseudo == ':indeterminate':
                sel.selectors.append(CSS_INDETERMINATE)
            elif pseudo == ':disabled':
                sel.selectors.append(CSS_DISABLED)
            elif pseudo == ':enabled':
                sel.selectors.append(CSS_ENABLED)
            elif pseudo == ':required':
                sel.selectors.append(CSS_REQUIRED)
            elif pseudo == ':optional':
                sel.selectors.append(CSS_OPTIONAL)
            elif pseudo == ':read-only':
                sel.selectors.append(CSS_READ_ONLY)
            elif pseudo == ':read-write':
                sel.selectors.append(CSS_READ_WRITE)
            elif pseudo == ':in-range':
                sel.selectors.append(CSS_IN_RANGE)
            elif pseudo == ':out-of-range':
                sel.selectors.append(CSS_OUT_OF_RANGE)
            elif pseudo == ':placeholder-shown':
                sel.selectors.append(CSS_PLACEHOLDER_SHOWN)
            elif pseudo == ':first-child':
                sel.nth.append(ct.SelectorNth(1, False, 0, False, False, ct.SelectorList()))
            elif pseudo == ':last-child':
                sel.nth.append(ct.SelectorNth(1, False, 0, False, True, ct.SelectorList()))
            elif pseudo == ':first-of-type':
                sel.nth.append(ct.SelectorNth(1, False, 0, True, False, ct.SelectorList()))
            elif pseudo == ':last-of-type':
                sel.nth.append(ct.SelectorNth(1, False, 0, True, True, ct.SelectorList()))
            elif pseudo == ':only-child':
                sel.nth.extend([
                 ct.SelectorNth(1, False, 0, False, False, ct.SelectorList()),
                 ct.SelectorNth(1, False, 0, False, True, ct.SelectorList())])
            elif pseudo == ':only-of-type':
                sel.nth.extend([
                 ct.SelectorNth(1, False, 0, True, False, ct.SelectorList()),
                 ct.SelectorNth(1, False, 0, True, True, ct.SelectorList())])
            has_selector = True
        elif complex_pseudo and pseudo in PSEUDO_COMPLEX_NO_MATCH:
            self.parse_selectors(iselector, m.end(0), FLG_PSEUDO | FLG_OPEN)
            sel.no_match = True
            has_selector = True
        elif not complex_pseudo or pseudo in PSEUDO_SIMPLE_NO_MATCH:
            sel.no_match = True
            has_selector = True
        elif pseudo in PSEUDO_SUPPORTED:
            raise SelectorSyntaxError("Invalid syntax for pseudo class '{}'".format(pseudo), self.pattern, m.start(0))
        else:
            raise NotImplementedError("'{}' pseudo-class is not implemented at this time".format(pseudo))
        return (
         has_selector, is_html)

    def parse_pseudo_nth(self, sel, m, has_selector, iselector):
        """Parse `nth` pseudo."""
        mdict = m.groupdict()
        if mdict.get('pseudo_nth_child'):
            postfix = '_child'
        else:
            postfix = '_type'
        mdict['name'] = util.lower(css_unescape(mdict['name']))
        content = util.lower(mdict.get('nth' + postfix))
        if content == 'even':
            s1 = 2
            s2 = 0
            var = True
        elif content == 'odd':
            s1 = 2
            s2 = 1
            var = True
        else:
            nth_parts = RE_NTH.match(content)
            s1 = '-' if (nth_parts.group('s1')) and (nth_parts.group('s1') == '-') else ''
            a = nth_parts.group('a')
            var = a.endswith('n')
            if a.startswith('n'):
                s1 += '1'
            elif var:
                s1 += a[:-1]
            else:
                s1 += a
            s2 = '-' if (nth_parts.group('s2')) and (nth_parts.group('s2') == '-') else ''
            if nth_parts.group('b'):
                s2 += nth_parts.group('b')
            else:
                s2 = '0'
            s1 = int(s1, 10)
            s2 = int(s2, 10)
        pseudo_sel = mdict['name']
        if postfix == '_child':
            if m.group('of'):
                nth_sel = self.parse_selectors(iselector, m.end(0), FLG_PSEUDO | FLG_OPEN)
            else:
                nth_sel = CSS_NTH_OF_S_DEFAULT
            if pseudo_sel == ':nth-child':
                sel.nth.append(ct.SelectorNth(s1, var, s2, False, False, nth_sel))
            elif pseudo_sel == ':nth-last-child':
                sel.nth.append(ct.SelectorNth(s1, var, s2, False, True, nth_sel))
        elif pseudo_sel == ':nth-of-type':
            sel.nth.append(ct.SelectorNth(s1, var, s2, True, False, ct.SelectorList()))
        elif pseudo_sel == ':nth-last-of-type':
            sel.nth.append(ct.SelectorNth(s1, var, s2, True, True, ct.SelectorList()))
        has_selector = True
        return has_selector

    def parse_pseudo_open(self, sel, name, has_selector, iselector, index):
        """Parse pseudo with opening bracket."""
        flags = FLG_PSEUDO | FLG_OPEN
        if name == ':not':
            flags |= FLG_NOT
        if name == ':has':
            flags |= FLG_RELATIVE
        sel.selectors.append(self.parse_selectors(iselector, index, flags))
        has_selector = True
        return has_selector

    def parse_has_combinator(self, sel, m, has_selector, selectors, rel_type, index):
        """Parse combinator tokens."""
        combinator = m.group('relation').strip()
        if not combinator:
            combinator = WS_COMBINATOR
        if combinator == COMMA_COMBINATOR:
            if not has_selector:
                raise SelectorSyntaxError("The combinator '{}' at postion {}, must have a selector before it".format(combinator, index), self.pattern, index)
            sel.rel_type = rel_type
            selectors[(-1)].relations.append(sel)
            rel_type = ':' + WS_COMBINATOR
            selectors.append(_Selector)
        else:
            if has_selector:
                sel.rel_type = rel_type
                selectors[(-1)].relations.append(sel)
            elif rel_type[1:] != WS_COMBINATOR:
                raise SelectorSyntaxError('The multiple combinators at position {}'.format(index), self.pattern, index)
            rel_type = ':' + combinator
        sel = _Selector
        has_selector = False
        return (
         has_selector, sel, rel_type)

    def parse_combinator(self, sel, m, has_selector, selectors, relations, is_pseudo, index):
        """Parse combinator tokens."""
        combinator = m.group('relation').strip()
        if not combinator:
            combinator = WS_COMBINATOR
        if not has_selector:
            raise SelectorSyntaxError("The combinator '{}' at postion {}, must have a selector before it".format(combinator, index), self.pattern, index)
        if combinator == COMMA_COMBINATOR:
            if not sel.tag:
                if not is_pseudo:
                    sel.tag = ct.SelectorTag('*', None)
            sel.relations.extend(relations)
            selectors.append(sel)
            del relations[:]
        else:
            sel.relations.extend(relations)
            sel.rel_type = combinator
            del relations[:]
            relations.append(sel)
        sel = _Selector
        has_selector = False
        return (
         has_selector, sel)

    def parse_class_id(self, sel, m, has_selector):
        """Parse HTML classes and ids."""
        selector = m.group(0)
        if selector.startswith('.'):
            sel.classes.append(css_unescape(selector[1:]))
        else:
            sel.ids.append(css_unescape(selector[1:]))
        has_selector = True
        return has_selector

    def parse_pseudo_contains(self, sel, m, has_selector):
        """Parse contains."""
        values = m.group('values')
        patterns = []
        for token in RE_VALUES.finditer(values):
            if token.group('split'):
                continue
            else:
                value = token.group('value')
                if value.startswith(("'", '"')):
                    value = css_unescape(value[1:-1], True)
                else:
                    value = css_unescape(value)
                patterns.append(value)

        sel.contains.append(ct.SelectorContains(tuple(patterns)))
        has_selector = True
        return has_selector

    def parse_pseudo_lang(self, sel, m, has_selector):
        """Parse pseudo language."""
        values = m.group('values')
        patterns = []
        for token in RE_VALUES.finditer(values):
            if token.group('split'):
                continue
            else:
                value = token.group('value')
                if value.startswith(('"', "'")):
                    value = css_unescape(value[1:-1], True)
                else:
                    value = css_unescape(value)
                patterns.append(value)

        sel.lang.append(ct.SelectorLang(patterns))
        has_selector = True
        return has_selector

    def parse_pseudo_dir(self, sel, m, has_selector):
        """Parse pseudo direction."""
        value = ct.SEL_DIR_LTR if util.lower(m.group('dir')) == 'ltr' else ct.SEL_DIR_RTL
        sel.flags |= value
        has_selector = True
        return has_selector

    def parse_selectors(self, iselector, index=0, flags=0):
        """Parse selectors."""
        sel = _Selector
        selectors = []
        has_selector = False
        closed = False
        relations = []
        rel_type = ':' + WS_COMBINATOR
        is_open = bool(flags & FLG_OPEN)
        is_pseudo = bool(flags & FLG_PSEUDO)
        is_relative = bool(flags & FLG_RELATIVE)
        is_not = bool(flags & FLG_NOT)
        is_html = bool(flags & FLG_HTML)
        is_default = bool(flags & FLG_DEFAULT)
        is_indeterminate = bool(flags & FLG_INDETERMINATE)
        is_in_range = bool(flags & FLG_IN_RANGE)
        is_out_of_range = bool(flags & FLG_OUT_OF_RANGE)
        is_placeholder_shown = bool(flags & FLG_PLACEHOLDER_SHOWN)
        if self.debug:
            if is_pseudo:
                print('    is_pseudo: True')
            if is_open:
                print('    is_open: True')
            if is_relative:
                print('    is_relative: True')
            if is_not:
                print('    is_not: True')
            if is_html:
                print('    is_html: True')
            if is_default:
                print('    is_default: True')
            if is_indeterminate:
                print('    is_indeterminate: True')
            if is_in_range:
                print('    is_in_range: True')
            if is_out_of_range:
                print('    is_out_of_range: True')
            if is_placeholder_shown:
                print('    is_placeholder_shown: True')
        if is_relative:
            selectors.append(_Selector)
        try:
            while True:
                key, m = next(iselector)
                if key == 'at_rule':
                    raise NotImplementedError('At-rules found at position {}'.format(m.start(0)))
                else:
                    if key == 'pseudo_class_custom':
                        has_selector = self.parse_pseudo_class_custom(sel, m, has_selector)
                    else:
                        if key == 'pseudo_class':
                            has_selector, is_html = self.parse_pseudo_class(sel, m, has_selector, iselector, is_html)
                        else:
                            if key == 'pseudo_element':
                                raise NotImplementedError('Psuedo-element found at position {}'.format(m.start(0)))
                            else:
                                if key == 'pseudo_contains':
                                    has_selector = self.parse_pseudo_contains(sel, m, has_selector)
                                else:
                                    if key in ('pseudo_nth_type', 'pseudo_nth_child'):
                                        has_selector = self.parse_pseudo_nthselmhas_selectoriselector
                                    else:
                                        if key == 'pseudo_lang':
                                            has_selector = self.parse_pseudo_lang(sel, m, has_selector)
                                        else:
                                            if key == 'pseudo_dir':
                                                has_selector = self.parse_pseudo_dir(sel, m, has_selector)
                                                is_html = True
                                            else:
                                                if key == 'pseudo_close':
                                                    if not has_selector:
                                                        raise SelectorSyntaxError('Expected a selector at postion {}'.format(m.start(0)), self.pattern, m.start(0))
                                                    if is_open:
                                                        closed = True
                                                        break
                                                    else:
                                                        raise SelectorSyntaxError('Unmatched pseudo-class close at postion {}'.format(m.start(0)), self.pattern, m.start(0))
                                                elif key == 'combine':
                                                    if is_relative:
                                                        has_selector, sel, rel_type = self.parse_has_combinator(sel, m, has_selector, selectors, rel_type, index)
                                                    else:
                                                        has_selector, sel = self.parse_combinator(sel, m, has_selector, selectors, relations, is_pseudo, index)
                                                elif key == 'attribute':
                                                    has_selector = self.parse_attribute_selector(sel, m, has_selector)
                                                elif key == 'tag':
                                                    if has_selector:
                                                        raise SelectorSyntaxError('Tag name found at position {} instead of at the start'.format(m.start(0)), self.pattern, m.start(0))
                                                    has_selector = self.parse_tag_pattern(sel, m, has_selector)
                                                elif key in ('class', 'id'):
                                                    has_selector = self.parse_class_id(sel, m, has_selector)
                index = m.end(0)

        except StopIteration:
            pass

        if is_open:
            if not closed:
                raise SelectorSyntaxError('Unclosed pseudo-class at position {}'.format(index), self.pattern, index)
            if has_selector:
                if not sel.tag:
                    if not is_pseudo:
                        sel.tag = ct.SelectorTag('*', None)
                if is_relative:
                    sel.rel_type = rel_type
                    selectors[(-1)].relations.append(sel)
                else:
                    sel.relations.extend(relations)
                    del relations[:]
                    selectors.append(sel)
            else:
                raise SelectorSyntaxError('Expected a selector at position {}'.format(index), self.pattern, index)
            if is_default:
                selectors[(-1)].flags = ct.SEL_DEFAULT
            if is_indeterminate:
                selectors[(-1)].flags = ct.SEL_INDETERMINATE
            if is_in_range:
                selectors[(-1)].flags = ct.SEL_IN_RANGE
            if is_out_of_range:
                selectors[(-1)].flags = ct.SEL_OUT_OF_RANGE
            if is_placeholder_shown:
                selectors[(-1)].flags = ct.SEL_PLACEHOLDER_SHOWN
            return ct.SelectorList([s.freeze() for s in selectors], is_not, is_html)

    def selector_iter(self, pattern):
        """Iterate selector tokens."""
        m = RE_WS_BEGIN.search(pattern)
        index = m.end(0) if m else 0
        m = RE_WS_END.search(pattern)
        end = m.start(0) - 1 if m else len(pattern) - 1
        if self.debug:
            print('## PARSING: {!r}'.format(pattern))
        while index <= end:
            m = None
            for v in self.css_tokens:
                m = v.match(pattern, index, self.flags)
                if m:
                    name = v.get_name()
                    if self.debug:
                        print("TOKEN: '{}' --> {!r} at position {}".format(name, m.group(0), m.start(0)))
                    else:
                        index = m.end(0)
                        yield (name, m)
                    break

            if m is None:
                c = pattern[index]
                if c == '[':
                    msg = 'Malformed attribute selector at position {}'.format(index)
                elif c == '.':
                    msg = 'Malformed class selector at position {}'.format(index)
                elif c == '#':
                    msg = 'Malformed id selector at position {}'.format(index)
                elif c == ':':
                    msg = 'Malformed pseudo-class selector at position {}'.format(index)
                else:
                    msg = 'Invalid character {!r} position {}'.format(c, index)
                raise SelectorSyntaxError(msg, self.pattern, index)

        if self.debug:
            print('## END PARSING')

    def process_selectors(self, index=0, flags=0):
        """Process selectors."""
        return self.parse_selectors(self.selector_iter(self.pattern), index, flags)


CSS_LINK = CSSParser('html|*:is(a, area, link)[href]').process_selectors(flags=(FLG_PSEUDO | FLG_HTML))
CSS_CHECKED = CSSParser('\n    html|*:is(input[type=checkbox], input[type=radio])[checked], html|option[selected]\n    ').process_selectors(flags=(FLG_PSEUDO | FLG_HTML))
CSS_DEFAULT = CSSParser('\n    :checked,\n\n    /*\n    This pattern must be at the end.\n    Special logic is applied to the last selector.\n    */\n    html|form html|*:is(button, input)[type="submit"]\n    ').process_selectors(flags=(FLG_PSEUDO | FLG_HTML | FLG_DEFAULT))
CSS_INDETERMINATE = CSSParser('\n    html|input[type="checkbox"][indeterminate],\n    html|input[type="radio"]:is(:not([name]), [name=""]):not([checked]),\n    html|progress:not([value]),\n\n    /*\n    This pattern must be at the end.\n    Special logic is applied to the last selector.\n    */\n    html|input[type="radio"][name][name!=\'\']:not([checked])\n    ').process_selectors(flags=(FLG_PSEUDO | FLG_HTML | FLG_INDETERMINATE))
CSS_DISABLED = CSSParser('\n    html|*:is(input[type!=hidden], button, select, textarea, fieldset, optgroup, option, fieldset)[disabled],\n    html|optgroup[disabled] > html|option,\n    html|fieldset[disabled] > html|*:is(input[type!=hidden], button, select, textarea, fieldset),\n    html|fieldset[disabled] >\n        html|*:not(legend:nth-of-type(1)) html|*:is(input[type!=hidden], button, select, textarea, fieldset)\n    ').process_selectors(flags=(FLG_PSEUDO | FLG_HTML))
CSS_ENABLED = CSSParser('\n    html|*:is(input[type!=hidden], button, select, textarea, fieldset, optgroup, option, fieldset):not(:disabled)\n    ').process_selectors(flags=(FLG_PSEUDO | FLG_HTML))
CSS_REQUIRED = CSSParser('html|*:is(input, textarea, select)[required]').process_selectors(flags=(FLG_PSEUDO | FLG_HTML))
CSS_OPTIONAL = CSSParser('html|*:is(input, textarea, select):not([required])').process_selectors(flags=(FLG_PSEUDO | FLG_HTML))
CSS_PLACEHOLDER_SHOWN = CSSParser('\n    html|input:is(\n        :not([type]),\n        [type=""],\n        [type=text],\n        [type=search],\n        [type=url],\n        [type=tel],\n        [type=email],\n        [type=password],\n        [type=number]\n    )[placeholder][placeholder!=\'\']:is(:not([value]), [value=""]),\n    html|textarea[placeholder][placeholder!=\'\']\n    ').process_selectors(flags=(FLG_PSEUDO | FLG_HTML | FLG_PLACEHOLDER_SHOWN))
CSS_NTH_OF_S_DEFAULT = CSSParser('*|*').process_selectors(flags=FLG_PSEUDO)
CSS_READ_WRITE = CSSParser('\n    html|*:is(\n        textarea,\n        input:is(\n            :not([type]),\n            [type=""],\n            [type=text],\n            [type=search],\n            [type=url],\n            [type=tel],\n            [type=email],\n            [type=number],\n            [type=password],\n            [type=date],\n            [type=datetime-local],\n            [type=month],\n            [type=time],\n            [type=week]\n        )\n    ):not([readonly], :disabled),\n    html|*:is([contenteditable=""], [contenteditable="true" i])\n    ').process_selectors(flags=(FLG_PSEUDO | FLG_HTML))
CSS_READ_ONLY = CSSParser('\n    html|*:not(:read-write)\n    ').process_selectors(flags=(FLG_PSEUDO | FLG_HTML))
CSS_IN_RANGE = CSSParser('\n    html|input:is(\n        [type="date"],\n        [type="month"],\n        [type="week"],\n        [type="time"],\n        [type="datetime-local"],\n        [type="number"],\n        [type="range"]\n    ):is(\n        [min],\n        [max]\n    )\n    ').process_selectors(flags=(FLG_PSEUDO | FLG_IN_RANGE | FLG_HTML))
CSS_OUT_OF_RANGE = CSSParser('\n    html|input:is(\n        [type="date"],\n        [type="month"],\n        [type="week"],\n        [type="time"],\n        [type="datetime-local"],\n        [type="number"],\n        [type="range"]\n    ):is(\n        [min],\n        [max]\n    )\n    ').process_selectors(flags=(FLG_PSEUDO | FLG_OUT_OF_RANGE | FLG_HTML))