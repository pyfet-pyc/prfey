# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\soupsieve\css_parser.py
"""CSS selector parser."""
from __future__ import unicode_literals
import re
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
PAT_TAG = '(?:(?:{ident}|\\*)?\\|)?(?:{ident}|\\*)'.format(ident=IDENTIFIER)
PAT_ATTR = '\\[{ws}*(?P<ns_attr>(?:(?:{ident}|\\*)?\\|)?{ident}){attr}'.format(ws=WSC, ident=IDENTIFIER, attr=ATTR)
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

@util.lru_cache(maxsize=_MAXCACHE)
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
            value = util.uchr(codepoint)
        elif m.group(2):
            value = m.group(2)[1:]
        elif m.group(3):
            value = '�'
        else:
            value = ''
        return value

    return RE_CSS_ESC if (not string) else RE_CSS_STR_ESC.sub(replace, content)


def escape--- This code section failed: ---

 L. 264         0  BUILD_LIST_0          0 
                2  STORE_FAST               'string'

 L. 265         4  LOAD_GLOBAL              len
                6  LOAD_FAST                'ident'
                8  CALL_FUNCTION_1       1  '1 positional argument'
               10  STORE_FAST               'length'

 L. 266        12  LOAD_FAST                'length'
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

 L. 267        32  LOAD_FAST                'length'
               34  LOAD_CONST               1
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE    64  'to 64'
               40  LOAD_FAST                'start_dash'
               42  POP_JUMP_IF_FALSE    64  'to 64'

 L. 269        44  LOAD_FAST                'string'
               46  LOAD_METHOD              append
               48  LOAD_STR                 '\\{}'
               50  LOAD_METHOD              format
               52  LOAD_FAST                'ident'
               54  CALL_METHOD_1         1  '1 positional argument'
               56  CALL_METHOD_1         1  '1 positional argument'
               58  POP_TOP          
            60_62  JUMP_FORWARD        384  'to 384'
             64_0  COME_FROM            42  '42'
             64_1  COME_FROM            38  '38'

 L. 271     64_66  SETUP_LOOP          384  'to 384'
               68  LOAD_GLOBAL              enumerate
               70  LOAD_FAST                'ident'
               72  CALL_FUNCTION_1       1  '1 positional argument'
               74  GET_ITER         
             76_0  COME_FROM           380  '380'
             76_1  COME_FROM           362  '362'
             76_2  COME_FROM           224  '224'
             76_3  COME_FROM           162  '162'
             76_4  COME_FROM           114  '114'
            76_78  FOR_ITER            382  'to 382'
               80  UNPACK_SEQUENCE_2     2 
               82  STORE_FAST               'index'
               84  STORE_FAST               'c'

 L. 272        86  LOAD_GLOBAL              util
               88  LOAD_METHOD              uord
               90  LOAD_FAST                'c'
               92  CALL_METHOD_1         1  '1 positional argument'
               94  STORE_FAST               'codepoint'

 L. 273        96  LOAD_FAST                'codepoint'
               98  LOAD_CONST               0
              100  COMPARE_OP               ==
              102  POP_JUMP_IF_FALSE   116  'to 116'

 L. 274       104  LOAD_FAST                'string'
              106  LOAD_METHOD              append
              108  LOAD_STR                 '�'
              110  CALL_METHOD_1         1  '1 positional argument'
              112  POP_TOP          
              114  JUMP_BACK            76  'to 76'
            116_0  COME_FROM           102  '102'

 L. 275       116  LOAD_CONST               1
              118  LOAD_FAST                'codepoint'
              120  DUP_TOP          
              122  ROT_THREE        
              124  COMPARE_OP               <=
              126  POP_JUMP_IF_FALSE   136  'to 136'
              128  LOAD_CONST               31
              130  COMPARE_OP               <=
              132  POP_JUMP_IF_TRUE    146  'to 146'
              134  JUMP_FORWARD        138  'to 138'
            136_0  COME_FROM           126  '126'
              136  POP_TOP          
            138_0  COME_FROM           134  '134'
              138  LOAD_FAST                'codepoint'
              140  LOAD_CONST               127
              142  COMPARE_OP               ==
              144  POP_JUMP_IF_FALSE   164  'to 164'
            146_0  COME_FROM           132  '132'

 L. 276       146  LOAD_FAST                'string'
              148  LOAD_METHOD              append
              150  LOAD_STR                 '\\{:x} '
              152  LOAD_METHOD              format
              154  LOAD_FAST                'codepoint'
              156  CALL_METHOD_1         1  '1 positional argument'
              158  CALL_METHOD_1         1  '1 positional argument'
              160  POP_TOP          
              162  JUMP_BACK            76  'to 76'
            164_0  COME_FROM           144  '144'

 L. 277       164  LOAD_FAST                'index'
              166  LOAD_CONST               0
              168  COMPARE_OP               ==
              170  POP_JUMP_IF_TRUE    184  'to 184'
              172  LOAD_FAST                'start_dash'
              174  POP_JUMP_IF_FALSE   226  'to 226'
              176  LOAD_FAST                'index'
              178  LOAD_CONST               1
              180  COMPARE_OP               ==
              182  POP_JUMP_IF_FALSE   226  'to 226'
            184_0  COME_FROM           170  '170'
              184  LOAD_CONST               48
              186  LOAD_FAST                'codepoint'
              188  DUP_TOP          
              190  ROT_THREE        
              192  COMPARE_OP               <=
              194  POP_JUMP_IF_FALSE   204  'to 204'
              196  LOAD_CONST               57
              198  COMPARE_OP               <=
              200  POP_JUMP_IF_FALSE   226  'to 226'
              202  JUMP_FORWARD        208  'to 208'
            204_0  COME_FROM           194  '194'
              204  POP_TOP          
              206  JUMP_FORWARD        226  'to 226'
            208_0  COME_FROM           202  '202'

 L. 278       208  LOAD_FAST                'string'
              210  LOAD_METHOD              append
              212  LOAD_STR                 '\\{:x} '
              214  LOAD_METHOD              format
              216  LOAD_FAST                'codepoint'
              218  CALL_METHOD_1         1  '1 positional argument'
              220  CALL_METHOD_1         1  '1 positional argument'
              222  POP_TOP          
              224  JUMP_BACK            76  'to 76'
            226_0  COME_FROM           206  '206'
            226_1  COME_FROM           200  '200'
            226_2  COME_FROM           182  '182'
            226_3  COME_FROM           174  '174'

 L. 280       226  LOAD_FAST                'codepoint'
              228  LOAD_CONST               (45, 95)
              230  COMPARE_OP               in
          232_234  POP_JUMP_IF_TRUE    352  'to 352'
              236  LOAD_FAST                'codepoint'
              238  LOAD_CONST               128
              240  COMPARE_OP               >=
          242_244  POP_JUMP_IF_TRUE    352  'to 352'
              246  LOAD_CONST               48
              248  LOAD_FAST                'codepoint'
              250  DUP_TOP          
              252  ROT_THREE        
              254  COMPARE_OP               <=
          256_258  POP_JUMP_IF_FALSE   270  'to 270'
              260  LOAD_CONST               57
              262  COMPARE_OP               <=
          264_266  POP_JUMP_IF_TRUE    352  'to 352'
              268  JUMP_FORWARD        272  'to 272'
            270_0  COME_FROM           256  '256'
              270  POP_TOP          
            272_0  COME_FROM           268  '268'

 L. 281       272  LOAD_CONST               48
              274  LOAD_FAST                'codepoint'
              276  DUP_TOP          
              278  ROT_THREE        
              280  COMPARE_OP               <=
          282_284  POP_JUMP_IF_FALSE   296  'to 296'
              286  LOAD_CONST               57
              288  COMPARE_OP               <=
          290_292  POP_JUMP_IF_TRUE    352  'to 352'
              294  JUMP_FORWARD        298  'to 298'
            296_0  COME_FROM           282  '282'
              296  POP_TOP          
            298_0  COME_FROM           294  '294'
              298  LOAD_CONST               65
              300  LOAD_FAST                'codepoint'
              302  DUP_TOP          
              304  ROT_THREE        
              306  COMPARE_OP               <=
          308_310  POP_JUMP_IF_FALSE   322  'to 322'
              312  LOAD_CONST               90
              314  COMPARE_OP               <=
          316_318  POP_JUMP_IF_TRUE    352  'to 352'
              320  JUMP_FORWARD        324  'to 324'
            322_0  COME_FROM           308  '308'
              322  POP_TOP          
            324_0  COME_FROM           320  '320'
              324  LOAD_CONST               97
              326  LOAD_FAST                'codepoint'
              328  DUP_TOP          
              330  ROT_THREE        
              332  COMPARE_OP               <=
          334_336  POP_JUMP_IF_FALSE   348  'to 348'
              338  LOAD_CONST               122
              340  COMPARE_OP               <=
          342_344  POP_JUMP_IF_FALSE   364  'to 364'
              346  JUMP_FORWARD        352  'to 352'
            348_0  COME_FROM           334  '334'
              348  POP_TOP          
              350  JUMP_FORWARD        364  'to 364'
            352_0  COME_FROM           346  '346'
            352_1  COME_FROM           316  '316'
            352_2  COME_FROM           290  '290'
            352_3  COME_FROM           264  '264'
            352_4  COME_FROM           242  '242'
            352_5  COME_FROM           232  '232'

 L. 283       352  LOAD_FAST                'string'
              354  LOAD_METHOD              append
              356  LOAD_FAST                'c'
              358  CALL_METHOD_1         1  '1 positional argument'
              360  POP_TOP          
              362  JUMP_BACK            76  'to 76'
            364_0  COME_FROM           350  '350'
            364_1  COME_FROM           342  '342'

 L. 285       364  LOAD_FAST                'string'
              366  LOAD_METHOD              append
              368  LOAD_STR                 '\\{}'
              370  LOAD_METHOD              format
              372  LOAD_FAST                'c'
              374  CALL_METHOD_1         1  '1 positional argument'
              376  CALL_METHOD_1         1  '1 positional argument'
              378  POP_TOP          
              380  JUMP_BACK            76  'to 76'
              382  POP_BLOCK        
            384_0  COME_FROM_LOOP       64  '64'
            384_1  COME_FROM            60  '60'

 L. 286       384  LOAD_STR                 ''
              386  LOAD_METHOD              join
              388  LOAD_FAST                'string'
              390  CALL_METHOD_1         1  '1 positional argument'
              392  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 384_0


class SelectorPattern(object):
    __doc__ = 'Selector pattern.'

    def __init__(self, name, pattern):
        """Initialize."""
        self.name = name
        self.re_pattern = re.compile(pattern, re.I | re.X | re.U)

    def get_name(self):
        """Get name."""
        return self.name

    def enabled(self, flags):
        """Enabled."""
        return True

    def match(self, selector, index):
        """Match the selector."""
        return self.re_pattern.match(selector, index)


class SpecialPseudoPattern(SelectorPattern):
    __doc__ = 'Selector pattern.'

    def __init__(self, patterns):
        """Initialize."""
        self.patterns = {}
        for p in patterns:
            name = p[0]
            pattern = SelectorPattern(name, p[2])
            for pseudo in p[1]:
                self.patterns[pseudo] = pattern

        self.matched_name = None
        self.re_pseudo_name = re.compile(PAT_PSEUDO_CLASS_SPECIAL, re.I | re.X | re.U)

    def get_name(self):
        """Get name."""
        return self.matched_name.get_name()

    def enabled(self, flags):
        """Enabled."""
        return True

    def match(self, selector, index):
        """Match the selector."""
        pseudo = None
        m = self.re_pseudo_name.match(selector, index)
        if m:
            name = util.lower(css_unescape(m.group('name')))
            pattern = self.patterns.get(name)
            if pattern:
                pseudo = pattern.match(selector, index)
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
       'pseudo_contains', (':contains', ), PAT_PSEUDO_CONTAINS),
      (
       'pseudo_nth_child', (':nth-child', ':nth-last-child'), PAT_PSEUDO_NTH_CHILD),
      (
       'pseudo_nth_type', (':nth-of-type', ':nth-last-of-type'), PAT_PSEUDO_NTH_TYPE),
      (
       'pseudo_lang', (':lang', ), PAT_PSEUDO_LANG),
      (
       'pseudo_dir', (':dir', ), PAT_PSEUDO_DIR))),
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

 L. 461         0  LOAD_CONST               False
                2  STORE_FAST               'inverse'

 L. 462         4  LOAD_FAST                'm'
                6  LOAD_METHOD              group
                8  LOAD_STR                 'cmp'
               10  CALL_METHOD_1         1  '1 positional argument'
               12  STORE_FAST               'op'

 L. 463        14  LOAD_FAST                'm'
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

 L. 464        44  LOAD_LISTCOMP            '<code_object <listcomp>>'
               46  LOAD_STR                 'CSSParser.parse_attribute_selector.<locals>.<listcomp>'
               48  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               50  LOAD_FAST                'm'
               52  LOAD_METHOD              group
               54  LOAD_STR                 'ns_attr'
               56  CALL_METHOD_1         1  '1 positional argument'
               58  LOAD_METHOD              split
               60  LOAD_STR                 '|'
               62  CALL_METHOD_1         1  '1 positional argument'
               64  GET_ITER         
               66  CALL_FUNCTION_1       1  '1 positional argument'
               68  STORE_FAST               'parts'

 L. 465        70  LOAD_STR                 ''
               72  STORE_FAST               'ns'

 L. 466        74  LOAD_CONST               False
               76  STORE_FAST               'is_type'

 L. 467        78  LOAD_CONST               None
               80  STORE_FAST               'pattern2'

 L. 468        82  LOAD_GLOBAL              len
               84  LOAD_FAST                'parts'
               86  CALL_FUNCTION_1       1  '1 positional argument'
               88  LOAD_CONST               1
               90  COMPARE_OP               >
               92  POP_JUMP_IF_FALSE   112  'to 112'

 L. 469        94  LOAD_FAST                'parts'
               96  LOAD_CONST               0
               98  BINARY_SUBSCR    
              100  STORE_FAST               'ns'

 L. 470       102  LOAD_FAST                'parts'
              104  LOAD_CONST               1
              106  BINARY_SUBSCR    
              108  STORE_FAST               'attr'
              110  JUMP_FORWARD        120  'to 120'
            112_0  COME_FROM            92  '92'

 L. 472       112  LOAD_FAST                'parts'
              114  LOAD_CONST               0
              116  BINARY_SUBSCR    
              118  STORE_FAST               'attr'
            120_0  COME_FROM           110  '110'

 L. 473       120  LOAD_FAST                'case'
              122  POP_JUMP_IF_FALSE   144  'to 144'

 L. 474       124  LOAD_FAST                'case'
              126  LOAD_STR                 'i'
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE   138  'to 138'
              132  LOAD_GLOBAL              re
              134  LOAD_ATTR                I
              136  JUMP_FORWARD        140  'to 140'
            138_0  COME_FROM           130  '130'
              138  LOAD_CONST               0
            140_0  COME_FROM           136  '136'
              140  STORE_FAST               'flags'
              142  JUMP_FORWARD        174  'to 174'
            144_0  COME_FROM           122  '122'

 L. 475       144  LOAD_GLOBAL              util
              146  LOAD_METHOD              lower
              148  LOAD_FAST                'attr'
              150  CALL_METHOD_1         1  '1 positional argument'
              152  LOAD_STR                 'type'
              154  COMPARE_OP               ==
              156  POP_JUMP_IF_FALSE   170  'to 170'

 L. 476       158  LOAD_GLOBAL              re
              160  LOAD_ATTR                I
              162  STORE_FAST               'flags'

 L. 477       164  LOAD_CONST               True
              166  STORE_FAST               'is_type'
              168  JUMP_FORWARD        174  'to 174'
            170_0  COME_FROM           156  '156'

 L. 479       170  LOAD_CONST               0
              172  STORE_FAST               'flags'
            174_0  COME_FROM           168  '168'
            174_1  COME_FROM           142  '142'

 L. 481       174  LOAD_FAST                'op'
              176  POP_JUMP_IF_FALSE   236  'to 236'

 L. 482       178  LOAD_FAST                'm'
              180  LOAD_METHOD              group
              182  LOAD_STR                 'value'
              184  CALL_METHOD_1         1  '1 positional argument'
              186  LOAD_METHOD              startswith
              188  LOAD_CONST               ('"', "'")
              190  CALL_METHOD_1         1  '1 positional argument'
              192  POP_JUMP_IF_FALSE   220  'to 220'

 L. 483       194  LOAD_GLOBAL              css_unescape
              196  LOAD_FAST                'm'
              198  LOAD_METHOD              group
              200  LOAD_STR                 'value'
              202  CALL_METHOD_1         1  '1 positional argument'
              204  LOAD_CONST               1
              206  LOAD_CONST               -1
              208  BUILD_SLICE_2         2 
              210  BINARY_SUBSCR    
              212  LOAD_CONST               True
              214  CALL_FUNCTION_2       2  '2 positional arguments'
              216  STORE_FAST               'value'
              218  JUMP_FORWARD        240  'to 240'
            220_0  COME_FROM           192  '192'

 L. 485       220  LOAD_GLOBAL              css_unescape
              222  LOAD_FAST                'm'
              224  LOAD_METHOD              group
              226  LOAD_STR                 'value'
              228  CALL_METHOD_1         1  '1 positional argument'
              230  CALL_FUNCTION_1       1  '1 positional argument'
              232  STORE_FAST               'value'
              234  JUMP_FORWARD        240  'to 240'
            236_0  COME_FROM           176  '176'

 L. 487       236  LOAD_CONST               None
              238  STORE_FAST               'value'
            240_0  COME_FROM           234  '234'
            240_1  COME_FROM           218  '218'

 L. 488       240  LOAD_FAST                'op'
              242  POP_JUMP_IF_TRUE    250  'to 250'

 L. 490       244  LOAD_CONST               None
              246  STORE_FAST               'pattern'
              248  JUMP_FORWARD        494  'to 494'
            250_0  COME_FROM           242  '242'

 L. 491       250  LOAD_FAST                'op'
              252  LOAD_METHOD              startswith
              254  LOAD_STR                 '^'
              256  CALL_METHOD_1         1  '1 positional argument'
          258_260  POP_JUMP_IF_FALSE   286  'to 286'

 L. 493       262  LOAD_GLOBAL              re
              264  LOAD_METHOD              compile
              266  LOAD_STR                 '^%s.*'
              268  LOAD_GLOBAL              re
              270  LOAD_METHOD              escape
              272  LOAD_FAST                'value'
              274  CALL_METHOD_1         1  '1 positional argument'
              276  BINARY_MODULO    
              278  LOAD_FAST                'flags'
              280  CALL_METHOD_2         2  '2 positional arguments'
              282  STORE_FAST               'pattern'
              284  JUMP_FORWARD        494  'to 494'
            286_0  COME_FROM           258  '258'

 L. 494       286  LOAD_FAST                'op'
              288  LOAD_METHOD              startswith
              290  LOAD_STR                 '$'
              292  CALL_METHOD_1         1  '1 positional argument'
          294_296  POP_JUMP_IF_FALSE   322  'to 322'

 L. 496       298  LOAD_GLOBAL              re
              300  LOAD_METHOD              compile
              302  LOAD_STR                 '.*?%s$'
              304  LOAD_GLOBAL              re
              306  LOAD_METHOD              escape
              308  LOAD_FAST                'value'
              310  CALL_METHOD_1         1  '1 positional argument'
              312  BINARY_MODULO    
              314  LOAD_FAST                'flags'
              316  CALL_METHOD_2         2  '2 positional arguments'
              318  STORE_FAST               'pattern'
              320  JUMP_FORWARD        494  'to 494'
            322_0  COME_FROM           294  '294'

 L. 497       322  LOAD_FAST                'op'
              324  LOAD_METHOD              startswith
              326  LOAD_STR                 '*'
              328  CALL_METHOD_1         1  '1 positional argument'
          330_332  POP_JUMP_IF_FALSE   358  'to 358'

 L. 499       334  LOAD_GLOBAL              re
              336  LOAD_METHOD              compile
              338  LOAD_STR                 '.*?%s.*'
              340  LOAD_GLOBAL              re
              342  LOAD_METHOD              escape
              344  LOAD_FAST                'value'
              346  CALL_METHOD_1         1  '1 positional argument'
              348  BINARY_MODULO    
              350  LOAD_FAST                'flags'
              352  CALL_METHOD_2         2  '2 positional arguments'
              354  STORE_FAST               'pattern'
              356  JUMP_FORWARD        494  'to 494'
            358_0  COME_FROM           330  '330'

 L. 500       358  LOAD_FAST                'op'
              360  LOAD_METHOD              startswith
              362  LOAD_STR                 '~'
              364  CALL_METHOD_1         1  '1 positional argument'
          366_368  POP_JUMP_IF_FALSE   420  'to 420'

 L. 504       370  LOAD_FAST                'value'
          372_374  POP_JUMP_IF_FALSE   388  'to 388'
              376  LOAD_GLOBAL              RE_WS
              378  LOAD_METHOD              search
              380  LOAD_FAST                'value'
              382  CALL_METHOD_1         1  '1 positional argument'
          384_386  POP_JUMP_IF_FALSE   392  'to 392'
            388_0  COME_FROM           372  '372'
              388  LOAD_STR                 '[^\\s\\S]'
              390  JUMP_FORWARD        400  'to 400'
            392_0  COME_FROM           384  '384'
              392  LOAD_GLOBAL              re
              394  LOAD_METHOD              escape
              396  LOAD_FAST                'value'
              398  CALL_METHOD_1         1  '1 positional argument'
            400_0  COME_FROM           390  '390'
              400  STORE_FAST               'value'

 L. 505       402  LOAD_GLOBAL              re
              404  LOAD_METHOD              compile
              406  LOAD_STR                 '.*?(?:(?<=^)|(?<=[ \\t\\r\\n\\f]))%s(?=(?:[ \\t\\r\\n\\f]|$)).*'
              408  LOAD_FAST                'value'
              410  BINARY_MODULO    
              412  LOAD_FAST                'flags'
              414  CALL_METHOD_2         2  '2 positional arguments'
              416  STORE_FAST               'pattern'
              418  JUMP_FORWARD        494  'to 494'
            420_0  COME_FROM           366  '366'

 L. 506       420  LOAD_FAST                'op'
              422  LOAD_METHOD              startswith
              424  LOAD_STR                 '|'
              426  CALL_METHOD_1         1  '1 positional argument'
          428_430  POP_JUMP_IF_FALSE   456  'to 456'

 L. 508       432  LOAD_GLOBAL              re
              434  LOAD_METHOD              compile
              436  LOAD_STR                 '^%s(?:-.*)?$'
              438  LOAD_GLOBAL              re
              440  LOAD_METHOD              escape
              442  LOAD_FAST                'value'
              444  CALL_METHOD_1         1  '1 positional argument'
              446  BINARY_MODULO    
              448  LOAD_FAST                'flags'
              450  CALL_METHOD_2         2  '2 positional arguments'
              452  STORE_FAST               'pattern'
              454  JUMP_FORWARD        494  'to 494'
            456_0  COME_FROM           428  '428'

 L. 511       456  LOAD_GLOBAL              re
              458  LOAD_METHOD              compile
              460  LOAD_STR                 '^%s$'
              462  LOAD_GLOBAL              re
              464  LOAD_METHOD              escape
              466  LOAD_FAST                'value'
              468  CALL_METHOD_1         1  '1 positional argument'
              470  BINARY_MODULO    
              472  LOAD_FAST                'flags'
              474  CALL_METHOD_2         2  '2 positional arguments'
              476  STORE_FAST               'pattern'

 L. 512       478  LOAD_FAST                'op'
              480  LOAD_METHOD              startswith
              482  LOAD_STR                 '!'
              484  CALL_METHOD_1         1  '1 positional argument'
          486_488  POP_JUMP_IF_FALSE   494  'to 494'

 L. 514       490  LOAD_CONST               True
              492  STORE_FAST               'inverse'
            494_0  COME_FROM           486  '486'
            494_1  COME_FROM           454  '454'
            494_2  COME_FROM           418  '418'
            494_3  COME_FROM           356  '356'
            494_4  COME_FROM           320  '320'
            494_5  COME_FROM           284  '284'
            494_6  COME_FROM           248  '248'

 L. 515       494  LOAD_FAST                'is_type'
          496_498  POP_JUMP_IF_FALSE   518  'to 518'
              500  LOAD_FAST                'pattern'
          502_504  POP_JUMP_IF_FALSE   518  'to 518'

 L. 516       506  LOAD_GLOBAL              re
              508  LOAD_METHOD              compile
              510  LOAD_FAST                'pattern'
              512  LOAD_ATTR                pattern
              514  CALL_METHOD_1         1  '1 positional argument'
              516  STORE_FAST               'pattern2'
            518_0  COME_FROM           502  '502'
            518_1  COME_FROM           496  '496'

 L. 519       518  LOAD_GLOBAL              ct
              520  LOAD_METHOD              SelectorAttribute
              522  LOAD_FAST                'attr'
              524  LOAD_FAST                'ns'
              526  LOAD_FAST                'pattern'
              528  LOAD_FAST                'pattern2'
              530  CALL_METHOD_4         4  '4 positional arguments'
              532  STORE_FAST               'sel_attr'

 L. 520       534  LOAD_FAST                'inverse'
          536_538  POP_JUMP_IF_FALSE   592  'to 592'

 L. 522       540  LOAD_GLOBAL              _Selector
              542  CALL_FUNCTION_0       0  '0 positional arguments'
              544  STORE_FAST               'sub_sel'

 L. 523       546  LOAD_FAST                'sub_sel'
              548  LOAD_ATTR                attributes
              550  LOAD_METHOD              append
              552  LOAD_FAST                'sel_attr'
              554  CALL_METHOD_1         1  '1 positional argument'
              556  POP_TOP          

 L. 524       558  LOAD_GLOBAL              ct
              560  LOAD_METHOD              SelectorList
              562  LOAD_FAST                'sub_sel'
              564  LOAD_METHOD              freeze
              566  CALL_METHOD_0         0  '0 positional arguments'
              568  BUILD_LIST_1          1 
              570  LOAD_CONST               True
              572  LOAD_CONST               False
              574  CALL_METHOD_3         3  '3 positional arguments'
              576  STORE_FAST               'not_list'

 L. 525       578  LOAD_FAST                'sel'
              580  LOAD_ATTR                selectors
              582  LOAD_METHOD              append
              584  LOAD_FAST                'not_list'
              586  CALL_METHOD_1         1  '1 positional argument'
              588  POP_TOP          
              590  JUMP_FORWARD        604  'to 604'
            592_0  COME_FROM           536  '536'

 L. 527       592  LOAD_FAST                'sel'
              594  LOAD_ATTR                attributes
              596  LOAD_METHOD              append
              598  LOAD_FAST                'sel_attr'
              600  CALL_METHOD_1         1  '1 positional argument'
              602  POP_TOP          
            604_0  COME_FROM           590  '590'

 L. 529       604  LOAD_CONST               True
              606  STORE_FAST               'has_selector'

 L. 530       608  LOAD_FAST                'has_selector'
              610  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 392_0

    def parse_tag_pattern(self, sel, m, has_selector):
        """Parse tag pattern from regex match."""
        parts = [css_unescape(x) for x in m.group(0).split('|')]
        if len(parts) > 1:
            prefix = parts[0]
            tag = parts[1]
        else:
            tag = parts[0]
            prefix = None
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
            self.parse_selectorsiselectorm.end(0)(FLG_PSEUDO | FLG_OPEN)
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
                nth_sel = self.parse_selectorsiselectorm.end(0)(FLG_PSEUDO | FLG_OPEN)
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
        sel.selectors.append(self.parse_selectorsiselectorindexflags)
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
                        has_selector = self.parse_pseudo_class_customselmhas_selector
                    else:
                        if key == 'pseudo_class':
                            has_selector, is_html = self.parse_pseudo_class(sel, m, has_selector, iselector, is_html)
                        else:
                            if key == 'pseudo_element':
                                raise NotImplementedError('Psuedo-element found at position {}'.format(m.start(0)))
                            else:
                                if key == 'pseudo_contains':
                                    has_selector = self.parse_pseudo_containsselmhas_selector
                                else:
                                    if key in ('pseudo_nth_type', 'pseudo_nth_child'):
                                        has_selector = self.parse_pseudo_nthselmhas_selectoriselector
                                    else:
                                        if key == 'pseudo_lang':
                                            has_selector = self.parse_pseudo_langselmhas_selector
                                        else:
                                            if key == 'pseudo_dir':
                                                has_selector = self.parse_pseudo_dirselmhas_selector
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
                                                    has_selector = self.parse_attribute_selectorselmhas_selector
                                                elif key == 'tag':
                                                    if has_selector:
                                                        raise SelectorSyntaxError('Tag name found at position {} instead of at the start'.format(m.start(0)), self.pattern, m.start(0))
                                                    has_selector = self.parse_tag_patternselmhas_selector
                                                elif key in ('class', 'id'):
                                                    has_selector = self.parse_class_idselmhas_selector
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
            return ct.SelectorList[s.freeze() for s in selectors]is_notis_html

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
                if not v.enabled(self.flags):
                    continue
                else:
                    m = v.match(pattern, index)
                if m:
                    name = v.get_name()
                    if self.debug:
                        print("TOKEN: '{}' --> {!r} at position {}".formatnamem.group(0)m.start(0))
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
        return self.parse_selectorsself.selector_iter(self.pattern)indexflags


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