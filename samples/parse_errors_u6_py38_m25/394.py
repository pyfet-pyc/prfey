# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: email\_header_value_parser.py
"""Header value parser implementing various email-related RFC parsing rules.

The parsing methods defined in this module implement various email related
parsing rules.  Principal among them is RFC 5322, which is the followon
to RFC 2822 and primarily a clarification of the former.  It also implements
RFC 2047 encoded word decoding.

RFC 5322 goes to considerable trouble to maintain backward compatibility with
RFC 822 in the parse phase, while cleaning up the structure on the generation
phase.  This parser supports correct RFC 5322 generation by tagging white space
as folding white space only when folding is allowed in the non-obsolete rule
sets.  Actually, the parser is even more generous when accepting input than RFC
5322 mandates, following the spirit of Postel's Law, which RFC 5322 encourages.
Where possible deviations from the standard are annotated on the 'defects'
attribute of tokens that deviate.

The general structure of the parser follows RFC 5322, and uses its terminology
where there is a direct correspondence.  Where the implementation requires a
somewhat different structure than that used by the formal grammar, new terms
that mimic the closest existing terms are used.  Thus, it really helps to have
a copy of RFC 5322 handy when studying this code.

Input to the parser is a string that has already been unfolded according to
RFC 5322 rules.  According to the RFC this unfolding is the very first step, and
this parser leaves the unfolding step to a higher level message parser, which
will have already detected the line breaks that need unfolding while
determining the beginning and end of each header.

The output of the parser is a TokenList object, which is a list subclass.  A
TokenList is a recursive data structure.  The terminal nodes of the structure
are Terminal objects, which are subclasses of str.  These do not correspond
directly to terminal objects in the formal grammar, but are instead more
practical higher level combinations of true terminals.

All TokenList and Terminal objects have a 'value' attribute, which produces the
semantically meaningful value of that part of the parse subtree.  The value of
all whitespace tokens (no matter how many sub-tokens they may contain) is a
single space, as per the RFC rules.  This includes 'CFWS', which is herein
included in the general class of whitespace tokens.  There is one exception to
the rule that whitespace tokens are collapsed into single spaces in values: in
the value of a 'bare-quoted-string' (a quoted-string with no leading or
trailing whitespace), any whitespace that appeared between the quotation marks
is preserved in the returned value.  Note that in all Terminal strings quoted
pairs are turned into their unquoted values.

All TokenList and Terminal objects also have a string value, which attempts to
be a "canonical" representation of the RFC-compliant form of the substring that
produced the parsed subtree, including minimal use of quoted pair quoting.
Whitespace runs are not collapsed.

Comment tokens also have a 'content' attribute providing the string found
between the parens (including any nested comments) with whitespace preserved.

All TokenList and Terminal objects have a 'defects' attribute which is a
possibly empty list all of the defects found while creating the token.  Defects
may appear on any token in the tree, and a composite list of all defects in the
subtree is available through the 'all_defects' attribute of any node.  (For
Terminal notes x.defects == x.all_defects.)

Each object in a parse tree is called a 'token', and each has a 'token_type'
attribute that gives the name from the RFC 5322 grammar that it represents.
Not all RFC 5322 nodes are produced, and there is one non-RFC 5322 node that
may be produced: 'ptext'.  A 'ptext' is a string of printable ascii characters.
It is returned in place of lists of (ctext/quoted-pair) and
(qtext/quoted-pair).

XXX: provide complete list of token types.
"""
import re, sys, urllib
from string import hexdigits
from operator import itemgetter
from email import _encoded_words as _ew
from email import errors
from email import utils
WSP = set(' \t')
CFWS_LEADER = WSP | set('(')
SPECIALS = set('()<>@,:;.\\"[]')
ATOM_ENDS = SPECIALS | WSP
DOT_ATOM_ENDS = ATOM_ENDS - set('.')
PHRASE_ENDS = SPECIALS - set('."(')
TSPECIALS = (SPECIALS | set('/?=')) - set('.')
TOKEN_ENDS = TSPECIALS | WSP
ASPECIALS = TSPECIALS | set("*'%")
ATTRIBUTE_ENDS = ASPECIALS | WSP
EXTENDED_ATTRIBUTE_ENDS = ATTRIBUTE_ENDS - set('%')

def quote_string(value):
    return '"' + str(value).replace('\\', '\\\\').replace('"', '\\"') + '"'


rfc2047_matcher = re.compile("\n   =\\?            # literal =?\n   [^?]*          # charset\n   \\?             # literal ?\n   [qQbB]         # literal 'q' or 'b', case insensitive\n   \\?             # literal ?\n  .*?             # encoded word\n  \\?=             # literal ?=\n", re.VERBOSE | re.MULTILINE)

class TokenList(list):
    token_type = None
    syntactic_break = True
    ew_combine_allowed = True

    def __init__(self, *args, **kw):
        (super().__init__)(*args, **kw)
        self.defects = []

    def __str__(self):
        return ''.join((str(x) for x in self))

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, super().__repr__())

    @property
    def value(self):
        return ''.join((x.value for x in self if x.value))

    @property
    def all_defects(self):
        return sum((x.all_defects for x in self), self.defects)

    def startswith_fws(self):
        return self[0].startswith_fws()

    @property
    def as_ew_allowed(self):
        """True if all top level tokens of this part may be RFC2047 encoded."""
        return all((part.as_ew_allowed for part in self))

    @property
    def comments(self):
        comments = []
        for token in self:
            comments.extend(token.comments)
        else:
            return comments

    def fold(self, *, policy):
        return _refold_parse_tree(self, policy=policy)

    def pprint(self, indent=''):
        print(self.ppstr(indent=indent))

    def ppstr(self, indent=''):
        return '\n'.join(self._pp(indent=indent))

    def _pp(self, indent=''):
        (yield '{}{}/{}('.format(indent, self.__class__.__name__, self.token_type))
        for token in self:
            if not hasattr(token, '_pp'):
                (yield indent + '    !! invalid element in token list: {!r}'.format(token))
            else:
                (yield from token._pp(indent + '    '))
        else:
            if self.defects:
                extra = ' Defects: {}'.format(self.defects)
            else:
                extra = ''
            (yield '{}){}'.format(indent, extra))


class WhiteSpaceTokenList(TokenList):

    @property
    def value(self):
        return ' '

    @property
    def comments(self):
        return [x.content for x in self if x.token_type == 'comment']


class UnstructuredTokenList(TokenList):
    token_type = 'unstructured'


class Phrase(TokenList):
    token_type = 'phrase'


class Word(TokenList):
    token_type = 'word'


class CFWSList(WhiteSpaceTokenList):
    token_type = 'cfws'


class Atom(TokenList):
    token_type = 'atom'


class Token(TokenList):
    token_type = 'token'
    encode_as_ew = False


class EncodedWord(TokenList):
    token_type = 'encoded-word'
    cte = None
    charset = None
    lang = None


class QuotedString(TokenList):
    token_type = 'quoted-string'

    @property
    def content(self):
        for x in self:
            if x.token_type == 'bare-quoted-string':
                return x.value

    @property
    def quoted_value(self):
        res = []
        for x in self:
            if x.token_type == 'bare-quoted-string':
                res.append(str(x))
            else:
                res.append(x.value)
        else:
            return ''.join(res)

    @property
    def stripped_value(self):
        for token in self:
            if token.token_type == 'bare-quoted-string':
                return token.value


class BareQuotedString(QuotedString):
    token_type = 'bare-quoted-string'

    def __str__(self):
        return quote_string(''.join((str(x) for x in self)))

    @property
    def value(self):
        return ''.join((str(x) for x in self))


class Comment(WhiteSpaceTokenList):
    token_type = 'comment'

    def __str__(self):
        return ''.join(sum([
         [
          '('],
         [self.quote(x) for x in self],
         [
          ')']], []))

    def quote(self, value):
        if value.token_type == 'comment':
            return str(value)
        return str(value).replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')

    @property
    def content(self):
        return ''.join((str(x) for x in self))

    @property
    def comments(self):
        return [self.content]


class AddressList(TokenList):
    token_type = 'address-list'

    @property
    def addresses(self):
        return [x for x in self if x.token_type == 'address']

    @property
    def mailboxes(self):
        return sum((x.mailboxes for x in self if x.token_type == 'address'), [])

    @property
    def all_mailboxes(self):
        return sum((x.all_mailboxes for x in self if x.token_type == 'address'), [])


class Address(TokenList):
    token_type = 'address'

    @property
    def display_name(self):
        if self[0].token_type == 'group':
            return self[0].display_name

    @property
    def mailboxes(self):
        if self[0].token_type == 'mailbox':
            return [
             self[0]]
        if self[0].token_type == 'invalid-mailbox':
            return []
        return self[0].mailboxes

    @property
    def all_mailboxes(self):
        if self[0].token_type == 'mailbox':
            return [
             self[0]]
        if self[0].token_type == 'invalid-mailbox':
            return [
             self[0]]
        return self[0].all_mailboxes


class MailboxList(TokenList):
    token_type = 'mailbox-list'

    @property
    def mailboxes(self):
        return [x for x in self if x.token_type == 'mailbox']

    @property
    def all_mailboxes(self):
        return [x for x in self if x.token_type in ('mailbox', 'invalid-mailbox')]


class GroupList(TokenList):
    token_type = 'group-list'

    @property
    def mailboxes(self):
        if not self or self[0].token_type != 'mailbox-list':
            return []
        return self[0].mailboxes

    @property
    def all_mailboxes(self):
        if not self or self[0].token_type != 'mailbox-list':
            return []
        return self[0].all_mailboxes


class Group(TokenList):
    token_type = 'group'

    @property
    def mailboxes(self):
        if self[2].token_type != 'group-list':
            return []
        return self[2].mailboxes

    @property
    def all_mailboxes(self):
        if self[2].token_type != 'group-list':
            return []
        return self[2].all_mailboxes

    @property
    def display_name(self):
        return self[0].display_name


class NameAddr(TokenList):
    token_type = 'name-addr'

    @property
    def display_name(self):
        if len(self) == 1:
            return
        return self[0].display_name

    @property
    def local_part(self):
        return self[(-1)].local_part

    @property
    def domain(self):
        return self[(-1)].domain

    @property
    def route(self):
        return self[(-1)].route

    @property
    def addr_spec(self):
        return self[(-1)].addr_spec


class AngleAddr(TokenList):
    token_type = 'angle-addr'

    @property
    def local_part(self):
        for x in self:
            if x.token_type == 'addr-spec':
                return x.local_part

    @property
    def domain(self):
        for x in self:
            if x.token_type == 'addr-spec':
                return x.domain

    @property
    def route(self):
        for x in self:
            if x.token_type == 'obs-route':
                return x.domains

    @property
    def addr_spec(self):
        for x in self:
            if x.token_type == 'addr-spec':
                if x.local_part:
                    return x.addr_spec
                return quote_string(x.local_part) + x.addr_spec
            return '<>'


class ObsRoute(TokenList):
    token_type = 'obs-route'

    @property
    def domains(self):
        return [x.domain for x in self if x.token_type == 'domain']


class Mailbox(TokenList):
    token_type = 'mailbox'

    @property
    def display_name(self):
        if self[0].token_type == 'name-addr':
            return self[0].display_name

    @property
    def local_part(self):
        return self[0].local_part

    @property
    def domain(self):
        return self[0].domain

    @property
    def route(self):
        if self[0].token_type == 'name-addr':
            return self[0].route

    @property
    def addr_spec(self):
        return self[0].addr_spec


class InvalidMailbox(TokenList):
    token_type = 'invalid-mailbox'

    @property
    def display_name(self):
        pass

    local_part = domain = route = addr_spec = display_name


class Domain(TokenList):
    token_type = 'domain'
    as_ew_allowed = False

    @property
    def domain(self):
        return ''.join(super().value.split())


class DotAtom(TokenList):
    token_type = 'dot-atom'


class DotAtomText(TokenList):
    token_type = 'dot-atom-text'
    as_ew_allowed = True


class NoFoldLiteral(TokenList):
    token_type = 'no-fold-literal'
    as_ew_allowed = False


class AddrSpec(TokenList):
    token_type = 'addr-spec'
    as_ew_allowed = False

    @property
    def local_part(self):
        return self[0].local_part

    @property
    def domain(self):
        if len(self) < 3:
            return
        return self[(-1)].domain

    @property
    def value(self):
        if len(self) < 3:
            return self[0].value
        return self[0].value.rstrip() + self[1].value + self[2].value.lstrip()

    @property
    def addr_spec(self):
        nameset = set(self.local_part)
        if len(nameset) > len(nameset - DOT_ATOM_ENDS):
            lp = quote_string(self.local_part)
        else:
            lp = self.local_part
        if self.domain is not None:
            return lp + '@' + self.domain
        return lp


class ObsLocalPart(TokenList):
    token_type = 'obs-local-part'
    as_ew_allowed = False


class DisplayName(Phrase):
    token_type = 'display-name'
    ew_combine_allowed = False

    @property
    def display_name(self):
        res = TokenList(self)
        if len(res) == 0:
            return res.value
        if res[0].token_type == 'cfws':
            res.pop(0)
        else:
            if res[0][0].token_type == 'cfws':
                res[0] = TokenList(res[0][1:])
            elif res[(-1)].token_type == 'cfws':
                res.pop()
            else:
                if res[(-1)][(-1)].token_type == 'cfws':
                    res[-1] = TokenList(res[(-1)][:-1])
            return res.value

    @property
    def value(self):
        quote = False
        if self.defects:
            quote = True
        else:
            for x in self:
                if x.token_type == 'quoted-string':
                    quote = True
                else:
                    if len(self) != 0:
                        if quote:
                            pre = post = ''
                            if self[0].token_type == 'cfws' or self[0][0].token_type == 'cfws':
                                pre = ' '
                            if self[(-1)].token_type == 'cfws' or self[(-1)][(-1)].token_type == 'cfws':
                                post = ' '
                            return pre + quote_string(self.display_name) + post
                    return super().value


class LocalPart(TokenList):
    token_type = 'local-part'
    as_ew_allowed = False

    @property
    def value(self):
        if self[0].token_type == 'quoted-string':
            return self[0].quoted_value
        return self[0].value

    @property
    def local_part(self):
        res = [
         DOT]
        last = DOT
        last_is_tl = False
        for tok in self[0] + [DOT]:
            if tok.token_type == 'cfws':
                pass
            else:
                if last_is_tl:
                    if tok.token_type == 'dot':
                        if last[(-1)].token_type == 'cfws':
                            res[-1] = TokenList(last[:-1])
                is_tl = isinstance(tok, TokenList)
                if is_tl and last.token_type == 'dot' and tok[0].token_type == 'cfws':
                    res.append(TokenList(tok[1:]))
                else:
                    res.append(tok)
                last = res[(-1)]
                last_is_tl = is_tl
        else:
            res = TokenList(res[1:-1])
            return res.value


class DomainLiteral(TokenList):
    token_type = 'domain-literal'
    as_ew_allowed = False

    @property
    def domain(self):
        return ''.join(super().value.split())

    @property
    def ip(self):
        for x in self:
            if x.token_type == 'ptext':
                return x.value


class MIMEVersion(TokenList):
    token_type = 'mime-version'
    major = None
    minor = None


class Parameter(TokenList):
    token_type = 'parameter'
    sectioned = False
    extended = False
    charset = 'us-ascii'

    @property
    def section_number(self):
        if self.sectioned:
            return self[1].number
        return 0

    @property
    def param_value(self):
        for token in self:
            if token.token_type == 'value':
                return token.stripped_value
            if token.token_type == 'quoted-string':
                for token in token:
                    if token.token_type == 'bare-quoted-string':
                        for token in token:
                            if token.token_type == 'value':
                                return token.stripped_value

            return ''


class InvalidParameter(Parameter):
    token_type = 'invalid-parameter'


class Attribute(TokenList):
    token_type = 'attribute'

    @property
    def stripped_value(self):
        for token in self:
            if token.token_type.endswith('attrtext'):
                return token.value


class Section(TokenList):
    token_type = 'section'
    number = None


class Value(TokenList):
    token_type = 'value'

    @property
    def stripped_value(self):
        token = self[0]
        if token.token_type == 'cfws':
            token = self[1]
        if token.token_type.endswith(('quoted-string', 'attribute', 'extended-attribute')):
            return token.stripped_value
        return self.value


class MimeParameters(TokenList):
    token_type = 'mime-parameters'
    syntactic_break = False

    @property
    def params--- This code section failed: ---

 L. 733         0  BUILD_MAP_0           0 
                2  STORE_FAST               'params'

 L. 734         4  LOAD_FAST                'self'
                6  GET_ITER         
                8  FOR_ITER             94  'to 94'
               10  STORE_FAST               'token'

 L. 735        12  LOAD_FAST                'token'
               14  LOAD_ATTR                token_type
               16  LOAD_METHOD              endswith
               18  LOAD_STR                 'parameter'
               20  CALL_METHOD_1         1  ''
               22  POP_JUMP_IF_TRUE     26  'to 26'

 L. 736        24  JUMP_BACK             8  'to 8'
             26_0  COME_FROM            22  '22'

 L. 737        26  LOAD_FAST                'token'
               28  LOAD_CONST               0
               30  BINARY_SUBSCR    
               32  LOAD_ATTR                token_type
               34  LOAD_STR                 'attribute'
               36  COMPARE_OP               !=
               38  POP_JUMP_IF_FALSE    42  'to 42'

 L. 738        40  JUMP_BACK             8  'to 8'
             42_0  COME_FROM            38  '38'

 L. 739        42  LOAD_FAST                'token'
               44  LOAD_CONST               0
               46  BINARY_SUBSCR    
               48  LOAD_ATTR                value
               50  LOAD_METHOD              strip
               52  CALL_METHOD_0         0  ''
               54  STORE_FAST               'name'

 L. 740        56  LOAD_FAST                'name'
               58  LOAD_FAST                'params'
               60  COMPARE_OP               not-in
               62  POP_JUMP_IF_FALSE    72  'to 72'

 L. 741        64  BUILD_LIST_0          0 
               66  LOAD_FAST                'params'
               68  LOAD_FAST                'name'
               70  STORE_SUBSCR     
             72_0  COME_FROM            62  '62'

 L. 742        72  LOAD_FAST                'params'
               74  LOAD_FAST                'name'
               76  BINARY_SUBSCR    
               78  LOAD_METHOD              append
               80  LOAD_FAST                'token'
               82  LOAD_ATTR                section_number
               84  LOAD_FAST                'token'
               86  BUILD_TUPLE_2         2 
               88  CALL_METHOD_1         1  ''
               90  POP_TOP          
               92  JUMP_BACK             8  'to 8'

 L. 743        94  LOAD_FAST                'params'
               96  LOAD_METHOD              items
               98  CALL_METHOD_0         0  ''
              100  GET_ITER         
          102_104  FOR_ITER            488  'to 488'
              106  UNPACK_SEQUENCE_2     2 
              108  STORE_FAST               'name'
              110  STORE_FAST               'parts'

 L. 744       112  LOAD_GLOBAL              sorted
              114  LOAD_FAST                'parts'
              116  LOAD_GLOBAL              itemgetter
              118  LOAD_CONST               0
              120  CALL_FUNCTION_1       1  ''
              122  LOAD_CONST               ('key',)
              124  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              126  STORE_FAST               'parts'

 L. 745       128  LOAD_FAST                'parts'
              130  LOAD_CONST               0
              132  BINARY_SUBSCR    
              134  LOAD_CONST               1
              136  BINARY_SUBSCR    
              138  STORE_FAST               'first_param'

 L. 746       140  LOAD_FAST                'first_param'
              142  LOAD_ATTR                charset
              144  STORE_FAST               'charset'

 L. 750       146  LOAD_FAST                'first_param'
              148  LOAD_ATTR                extended
              150  POP_JUMP_IF_TRUE    218  'to 218'
              152  LOAD_GLOBAL              len
              154  LOAD_FAST                'parts'
              156  CALL_FUNCTION_1       1  ''
              158  LOAD_CONST               1
              160  COMPARE_OP               >
              162  POP_JUMP_IF_FALSE   218  'to 218'

 L. 751       164  LOAD_FAST                'parts'
              166  LOAD_CONST               1
              168  BINARY_SUBSCR    
              170  LOAD_CONST               0
              172  BINARY_SUBSCR    
              174  LOAD_CONST               0
              176  COMPARE_OP               ==
              178  POP_JUMP_IF_FALSE   218  'to 218'

 L. 752       180  LOAD_FAST                'parts'
              182  LOAD_CONST               1
              184  BINARY_SUBSCR    
              186  LOAD_CONST               1
              188  BINARY_SUBSCR    
              190  LOAD_ATTR                defects
              192  LOAD_METHOD              append
              194  LOAD_GLOBAL              errors
              196  LOAD_METHOD              InvalidHeaderDefect

 L. 753       198  LOAD_STR                 'duplicate parameter name; duplicate(s) ignored'

 L. 752       200  CALL_METHOD_1         1  ''
              202  CALL_METHOD_1         1  ''
              204  POP_TOP          

 L. 754       206  LOAD_FAST                'parts'
              208  LOAD_CONST               None
              210  LOAD_CONST               1
              212  BUILD_SLICE_2         2 
              214  BINARY_SUBSCR    
              216  STORE_FAST               'parts'
            218_0  COME_FROM           178  '178'
            218_1  COME_FROM           162  '162'
            218_2  COME_FROM           150  '150'

 L. 757       218  BUILD_LIST_0          0 
              220  STORE_FAST               'value_parts'

 L. 758       222  LOAD_CONST               0
              224  STORE_FAST               'i'

 L. 759       226  LOAD_FAST                'parts'
              228  GET_ITER         
              230  FOR_ITER            466  'to 466'
              232  UNPACK_SEQUENCE_2     2 
              234  STORE_FAST               'section_number'
              236  STORE_FAST               'param'

 L. 760       238  LOAD_FAST                'section_number'
              240  LOAD_FAST                'i'
              242  COMPARE_OP               !=
          244_246  POP_JUMP_IF_FALSE   296  'to 296'

 L. 764       248  LOAD_FAST                'param'
              250  LOAD_ATTR                extended
          252_254  POP_JUMP_IF_TRUE    278  'to 278'

 L. 765       256  LOAD_FAST                'param'
              258  LOAD_ATTR                defects
              260  LOAD_METHOD              append
              262  LOAD_GLOBAL              errors
              264  LOAD_METHOD              InvalidHeaderDefect

 L. 766       266  LOAD_STR                 'duplicate parameter name; duplicate ignored'

 L. 765       268  CALL_METHOD_1         1  ''
              270  CALL_METHOD_1         1  ''
              272  POP_TOP          

 L. 767       274  JUMP_BACK           230  'to 230'
              276  JUMP_FORWARD        296  'to 296'
            278_0  COME_FROM           252  '252'

 L. 769       278  LOAD_FAST                'param'
              280  LOAD_ATTR                defects
              282  LOAD_METHOD              append
              284  LOAD_GLOBAL              errors
              286  LOAD_METHOD              InvalidHeaderDefect

 L. 770       288  LOAD_STR                 'inconsistent RFC2231 parameter numbering'

 L. 769       290  CALL_METHOD_1         1  ''
              292  CALL_METHOD_1         1  ''
              294  POP_TOP          
            296_0  COME_FROM           276  '276'
            296_1  COME_FROM           244  '244'

 L. 771       296  LOAD_FAST                'i'
              298  LOAD_CONST               1
              300  INPLACE_ADD      
              302  STORE_FAST               'i'

 L. 772       304  LOAD_FAST                'param'
              306  LOAD_ATTR                param_value
              308  STORE_FAST               'value'

 L. 773       310  LOAD_FAST                'param'
              312  LOAD_ATTR                extended
          314_316  POP_JUMP_IF_FALSE   454  'to 454'

 L. 774       318  SETUP_FINALLY       336  'to 336'

 L. 775       320  LOAD_GLOBAL              urllib
              322  LOAD_ATTR                parse
              324  LOAD_METHOD              unquote_to_bytes
              326  LOAD_FAST                'value'
              328  CALL_METHOD_1         1  ''
              330  STORE_FAST               'value'
              332  POP_BLOCK        
              334  JUMP_FORWARD        374  'to 374'
            336_0  COME_FROM_FINALLY   318  '318'

 L. 776       336  DUP_TOP          
              338  LOAD_GLOBAL              UnicodeEncodeError
              340  COMPARE_OP               exception-match
          342_344  POP_JUMP_IF_FALSE   372  'to 372'
              346  POP_TOP          
              348  POP_TOP          
              350  POP_TOP          

 L. 780       352  LOAD_GLOBAL              urllib
              354  LOAD_ATTR                parse
              356  LOAD_ATTR                unquote
              358  LOAD_FAST                'value'
              360  LOAD_STR                 'latin-1'
              362  LOAD_CONST               ('encoding',)
              364  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              366  STORE_FAST               'value'
              368  POP_EXCEPT       
              370  JUMP_FORWARD        454  'to 454'
            372_0  COME_FROM           342  '342'
              372  END_FINALLY      
            374_0  COME_FROM           334  '334'

 L. 782       374  SETUP_FINALLY       392  'to 392'

 L. 783       376  LOAD_FAST                'value'
              378  LOAD_METHOD              decode
              380  LOAD_FAST                'charset'
              382  LOAD_STR                 'surrogateescape'
              384  CALL_METHOD_2         2  ''
              386  STORE_FAST               'value'
              388  POP_BLOCK        
              390  JUMP_FORWARD        426  'to 426'
            392_0  COME_FROM_FINALLY   374  '374'

 L. 784       392  DUP_TOP          
              394  LOAD_GLOBAL              LookupError
              396  COMPARE_OP               exception-match
          398_400  POP_JUMP_IF_FALSE   424  'to 424'
              402  POP_TOP          
              404  POP_TOP          
              406  POP_TOP          

 L. 789       408  LOAD_FAST                'value'
              410  LOAD_METHOD              decode
              412  LOAD_STR                 'us-ascii'
              414  LOAD_STR                 'surrogateescape'
              416  CALL_METHOD_2         2  ''
              418  STORE_FAST               'value'
              420  POP_EXCEPT       
              422  JUMP_FORWARD        426  'to 426'
            424_0  COME_FROM           398  '398'
              424  END_FINALLY      
            426_0  COME_FROM           422  '422'
            426_1  COME_FROM           390  '390'

 L. 790       426  LOAD_GLOBAL              utils
              428  LOAD_METHOD              _has_surrogates
              430  LOAD_FAST                'value'
              432  CALL_METHOD_1         1  ''
          434_436  POP_JUMP_IF_FALSE   454  'to 454'

 L. 791       438  LOAD_FAST                'param'
              440  LOAD_ATTR                defects
              442  LOAD_METHOD              append
              444  LOAD_GLOBAL              errors
              446  LOAD_METHOD              UndecodableBytesDefect
              448  CALL_METHOD_0         0  ''
              450  CALL_METHOD_1         1  ''
              452  POP_TOP          
            454_0  COME_FROM           434  '434'
            454_1  COME_FROM           370  '370'
            454_2  COME_FROM           314  '314'

 L. 792       454  LOAD_FAST                'value_parts'
              456  LOAD_METHOD              append
              458  LOAD_FAST                'value'
              460  CALL_METHOD_1         1  ''
              462  POP_TOP          
              464  JUMP_BACK           230  'to 230'

 L. 793       466  LOAD_STR                 ''
              468  LOAD_METHOD              join
              470  LOAD_FAST                'value_parts'
              472  CALL_METHOD_1         1  ''
              474  STORE_FAST               'value'

 L. 794       476  LOAD_FAST                'name'
              478  LOAD_FAST                'value'
              480  BUILD_TUPLE_2         2 
              482  YIELD_VALUE      
              484  POP_TOP          
              486  JUMP_BACK           102  'to 102'

Parse error at or near `JUMP_FORWARD' instruction at offset 276

    def __str__(self):
        params = []
        for name, value in self.params:
            if value:
                params.append('{}={}'.format(name, quote_string(value)))
            else:
                params.append(name)
        else:
            params = '; '.join(params)
            if params:
                return ' ' + params
            return ''


class ParameterizedHeaderValue(TokenList):
    syntactic_break = False

    @property
    def params(self):
        for token in reversed(self):
            if token.token_type == 'mime-parameters':
                return token.params
            return {}


class ContentType(ParameterizedHeaderValue):
    token_type = 'content-type'
    as_ew_allowed = False
    maintype = 'text'
    subtype = 'plain'


class ContentDisposition(ParameterizedHeaderValue):
    token_type = 'content-disposition'
    as_ew_allowed = False
    content_disposition = None


class ContentTransferEncoding(TokenList):
    token_type = 'content-transfer-encoding'
    as_ew_allowed = False
    cte = '7bit'


class HeaderLabel(TokenList):
    token_type = 'header-label'
    as_ew_allowed = False


class MsgID(TokenList):
    token_type = 'msg-id'
    as_ew_allowed = False

    def fold(self, policy):
        return str(self) + policy.linesep


class MessageID(MsgID):
    token_type = 'message-id'


class InvalidMessageID(MessageID):
    token_type = 'invalid-message-id'


class Header(TokenList):
    token_type = 'header'


class Terminal(str):
    as_ew_allowed = True
    ew_combine_allowed = True
    syntactic_break = True

    def __new__(cls, value, token_type):
        self = super().__new__(cls, value)
        self.token_type = token_type
        self.defects = []
        return self

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, super().__repr__())

    def pprint(self):
        print(self.__class__.__name__ + '/' + self.token_type)

    @property
    def all_defects(self):
        return list(self.defects)

    def _pp(self, indent=''):
        return [
         '{}{}/{}({}){}'.format(indent, self.__class__.__name__, self.token_type, super().__repr__(), '' if not self.defects else ' {}'.format(self.defects))]

    def pop_trailing_ws(self):
        pass

    @property
    def comments(self):
        return []

    def __getnewargs__(self):
        return (
         str(self), self.token_type)


class WhiteSpaceTerminal(Terminal):

    @property
    def value(self):
        return ' '

    def startswith_fws(self):
        return True


class ValueTerminal(Terminal):

    @property
    def value(self):
        return self

    def startswith_fws(self):
        return False


class EWWhiteSpaceTerminal(WhiteSpaceTerminal):

    @property
    def value(self):
        return ''

    def __str__(self):
        return ''


class _InvalidEwError(errors.HeaderParseError):
    __doc__ = 'Invalid encoded word found while parsing headers.'


DOT = ValueTerminal('.', 'dot')
ListSeparator = ValueTerminal(',', 'list-separator')
RouteComponentMarker = ValueTerminal('@', 'route-component-marker')
_wsp_splitter = re.compile('([{}]+)'.format(''.join(WSP))).split
_non_atom_end_matcher = re.compile('[^{}]+'.format(re.escape(''.join(ATOM_ENDS)))).match
_non_printable_finder = re.compile('[\\x00-\\x20\\x7F]').findall
_non_token_end_matcher = re.compile('[^{}]+'.format(re.escape(''.join(TOKEN_ENDS)))).match
_non_attribute_end_matcher = re.compile('[^{}]+'.format(re.escape(''.join(ATTRIBUTE_ENDS)))).match
_non_extended_attribute_end_matcher = re.compile('[^{}]+'.format(re.escape(''.join(EXTENDED_ATTRIBUTE_ENDS)))).match

def _validate_xtext(xtext):
    """If input token contains ASCII non-printables, register a defect."""
    non_printables = _non_printable_finder(xtext)
    if non_printables:
        xtext.defects.append(errors.NonPrintableDefect(non_printables))
    if utils._has_surrogates(xtext):
        xtext.defects.append(errors.UndecodableBytesDefect('Non-ASCII characters found in header token'))


def _get_ptext_to_endchars--- This code section failed: ---

 L.1005         0  LOAD_GLOBAL              _wsp_splitter
                2  LOAD_FAST                'value'
                4  LOAD_CONST               1
                6  CALL_FUNCTION_2       2  ''
                8  UNPACK_EX_1+0           
               10  STORE_FAST               'fragment'
               12  STORE_FAST               'remainder'

 L.1006        14  BUILD_LIST_0          0 
               16  STORE_FAST               'vchars'

 L.1007        18  LOAD_CONST               False
               20  STORE_FAST               'escape'

 L.1008        22  LOAD_CONST               False
               24  STORE_FAST               'had_qp'

 L.1009        26  LOAD_GLOBAL              range
               28  LOAD_GLOBAL              len
               30  LOAD_FAST                'fragment'
               32  CALL_FUNCTION_1       1  ''
               34  CALL_FUNCTION_1       1  ''
               36  GET_ITER         
               38  FOR_ITER            116  'to 116'
               40  STORE_FAST               'pos'

 L.1010        42  LOAD_FAST                'fragment'
               44  LOAD_FAST                'pos'
               46  BINARY_SUBSCR    
               48  LOAD_STR                 '\\'
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    74  'to 74'

 L.1011        54  LOAD_FAST                'escape'
               56  POP_JUMP_IF_FALSE    68  'to 68'

 L.1012        58  LOAD_CONST               False
               60  STORE_FAST               'escape'

 L.1013        62  LOAD_CONST               True
               64  STORE_FAST               'had_qp'
               66  JUMP_FORWARD         74  'to 74'
             68_0  COME_FROM            56  '56'

 L.1015        68  LOAD_CONST               True
               70  STORE_FAST               'escape'

 L.1016        72  JUMP_BACK            38  'to 38'
             74_0  COME_FROM            66  '66'
             74_1  COME_FROM            52  '52'

 L.1017        74  LOAD_FAST                'escape'
               76  POP_JUMP_IF_FALSE    84  'to 84'

 L.1018        78  LOAD_CONST               False
               80  STORE_FAST               'escape'
               82  JUMP_FORWARD        100  'to 100'
             84_0  COME_FROM            76  '76'

 L.1019        84  LOAD_FAST                'fragment'
               86  LOAD_FAST                'pos'
               88  BINARY_SUBSCR    
               90  LOAD_FAST                'endchars'
               92  COMPARE_OP               in
               94  POP_JUMP_IF_FALSE   100  'to 100'

 L.1020        96  POP_TOP          
               98  JUMP_ABSOLUTE       124  'to 124'
            100_0  COME_FROM            94  '94'
            100_1  COME_FROM            82  '82'

 L.1021       100  LOAD_FAST                'vchars'
              102  LOAD_METHOD              append
              104  LOAD_FAST                'fragment'
              106  LOAD_FAST                'pos'
              108  BINARY_SUBSCR    
              110  CALL_METHOD_1         1  ''
              112  POP_TOP          
              114  JUMP_BACK            38  'to 38'

 L.1023       116  LOAD_FAST                'pos'
              118  LOAD_CONST               1
              120  BINARY_ADD       
              122  STORE_FAST               'pos'

 L.1024       124  LOAD_STR                 ''
              126  LOAD_METHOD              join
              128  LOAD_FAST                'vchars'
              130  CALL_METHOD_1         1  ''
              132  LOAD_STR                 ''
              134  LOAD_METHOD              join
              136  LOAD_FAST                'fragment'
              138  LOAD_FAST                'pos'
              140  LOAD_CONST               None
              142  BUILD_SLICE_2         2 
              144  BINARY_SUBSCR    
              146  BUILD_LIST_1          1 
              148  LOAD_FAST                'remainder'
              150  BINARY_ADD       
              152  CALL_METHOD_1         1  ''
              154  LOAD_FAST                'had_qp'
              156  BUILD_TUPLE_3         3 
              158  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 98


def get_fws(value):
    """FWS = 1*WSP

    This isn't the RFC definition.  We're using fws to represent tokens where
    folding can be done, but when we are parsing the *un*folding has already
    been done so we don't need to watch out for CRLF.

    """
    newvalue = value.lstrip()
    fws = WhiteSpaceTerminal(value[:len(value) - len(newvalue)], 'fws')
    return (fws, newvalue)


def get_encoded_word(value):
    """ encoded-word = "=?" charset "?" encoding "?" encoded-text "?="

    """
    ew = EncodedWord()
    if not value.startswith('=?'):
        raise errors.HeaderParseError('expected encoded word but found {}'.format(value))
    tok, *remainder = value[2:].split('?=', 1)
    if tok == value[2:]:
        raise errors.HeaderParseError('expected encoded word but found {}'.format(value))
    remstr = ''.join(remainder)
    if len(remstr) > 1:
        if remstr[0] in hexdigits:
            if remstr[1] in hexdigits:
                if tok.count('?') < 2:
                    rest, *remainder = remstr.split('?=', 1)
                    tok = tok + '?=' + rest
    if len(tok.split()) > 1:
        ew.defects.append(errors.InvalidHeaderDefect('whitespace inside encoded word'))
    ew.cte = value
    value = ''.join(remainder)
    try:
        text, charset, lang, defects = _ew.decode('=?' + tok + '?=')
    except (ValueError, KeyError):
        raise _InvalidEwError("encoded word format invalid: '{}'".format(ew.cte))
    else:
        ew.charset = charset
        ew.lang = lang
        ew.defects.extend(defects)
        if text:
            if text[0] in WSP:
                token, text = get_fws(text)
                ew.append(token)
            else:
                chars, *remainder = _wsp_splitter(text, 1)
                vtext = ValueTerminal(chars, 'vtext')
                _validate_xtext(vtext)
                ew.append(vtext)
                text = ''.join(remainder)
        else:
            if value:
                if value[0] not in WSP:
                    ew.defects.append(errors.InvalidHeaderDefect('missing trailing whitespace after encoded-word'))
            return (
             ew, value)


def get_unstructured(value):
    """unstructured = (*([FWS] vchar) *WSP) / obs-unstruct
       obs-unstruct = *((*LF *CR *(obs-utext) *LF *CR)) / FWS)
       obs-utext = %d0 / obs-NO-WS-CTL / LF / CR

       obs-NO-WS-CTL is control characters except WSP/CR/LF.

    So, basically, we have printable runs, plus control characters or nulls in
    the obsolete syntax, separated by whitespace.  Since RFC 2047 uses the
    obsolete syntax in its specification, but requires whitespace on either
    side of the encoded words, I can see no reason to need to separate the
    non-printable-non-whitespace from the printable runs if they occur, so we
    parse this into xtext tokens separated by WSP tokens.

    Because an 'unstructured' value must by definition constitute the entire
    value, this 'get' routine does not return a remaining value, only the
    parsed TokenList.

    """
    unstructured = UnstructuredTokenList()
    while value:
        if value[0] in WSP:
            token, value = get_fws(value)
            unstructured.append(token)
        else:
            valid_ew = True
            if value.startswith('=?'):
                try:
                    token, value = get_encoded_word(value)
                except _InvalidEwError:
                    valid_ew = False
                except errors.HeaderParseError:
                    pass
                else:
                    have_ws = True
                    if len(unstructured) > 0:
                        if unstructured[(-1)].token_type != 'fws':
                            unstructured.defects.append(errors.InvalidHeaderDefect('missing whitespace before encoded word'))
                            have_ws = False
                    if have_ws:
                        if len(unstructured) > 1:
                            if unstructured[(-2)].token_type == 'encoded-word':
                                unstructured[-1] = EWWhiteSpaceTerminal(unstructured[(-1)], 'fws')
                    unstructured.append(token)
            else:
                tok, *remainder = _wsp_splitter(value, 1)
                if valid_ew:
                    if rfc2047_matcher.search(tok):
                        tok, *remainder = value.partition('=?')
                vtext = ValueTerminal(tok, 'vtext')
                _validate_xtext(vtext)
                unstructured.append(vtext)
                value = ''.join(remainder)

    return unstructured


def get_qp_ctext(value):
    r"""ctext = <printable ascii except \ ( )>

    This is not the RFC ctext, since we are handling nested comments in comment
    and unquoting quoted-pairs here.  We allow anything except the '()'
    characters, but if we find any ASCII other than the RFC defined printable
    ASCII, a NonPrintableDefect is added to the token's defects list.  Since
    quoted pairs are converted to their unquoted values, what is returned is
    a 'ptext' token.  In this case it is a WhiteSpaceTerminal, so it's value
    is ' '.

    """
    ptext, value, _ = _get_ptext_to_endchars(value, '()')
    ptext = WhiteSpaceTerminal(ptext, 'ptext')
    _validate_xtext(ptext)
    return (ptext, value)


def get_qcontent(value):
    """qcontent = qtext / quoted-pair

    We allow anything except the DQUOTE character, but if we find any ASCII
    other than the RFC defined printable ASCII, a NonPrintableDefect is
    added to the token's defects list.  Any quoted pairs are converted to their
    unquoted values, so what is returned is a 'ptext' token.  In this case it
    is a ValueTerminal.

    """
    ptext, value, _ = _get_ptext_to_endchars(value, '"')
    ptext = ValueTerminal(ptext, 'ptext')
    _validate_xtext(ptext)
    return (ptext, value)


def get_atext(value):
    """atext = <matches _atext_matcher>

    We allow any non-ATOM_ENDS in atext, but add an InvalidATextDefect to
    the token's defects list if we find non-atext characters.
    """
    m = _non_atom_end_matcher(value)
    if not m:
        raise errors.HeaderParseError("expected atext but found '{}'".format(value))
    atext = m.group()
    value = value[len(atext):]
    atext = ValueTerminal(atext, 'atext')
    _validate_xtext(atext)
    return (atext, value)


def get_bare_quoted_string(value):
    """bare-quoted-string = DQUOTE *([FWS] qcontent) [FWS] DQUOTE

    A quoted-string without the leading or trailing white space.  Its
    value is the text between the quote marks, with whitespace
    preserved and quoted pairs decoded.
    """
    if value[0] != '"':
        raise errors.HeaderParseError('expected \'"\' but found \'{}\''.format(value))
    else:
        bare_quoted_string = BareQuotedString()
        value = value[1:]
        if value and value[0] == '"':
            token, value = get_qcontent(value)
            bare_quoted_string.append(token)
        while value:
            if value[0] != '"':
                if value[0] in WSP:
                    token, value = get_fws(value)
                else:
                    if value[:2] == '=?':
                        try:
                            token, value = get_encoded_word(value)
                            bare_quoted_string.defects.append(errors.InvalidHeaderDefect('encoded word inside quoted string'))
                        except errors.HeaderParseError:
                            token, value = get_qcontent(value)

                    else:
                        token, value = get_qcontent(value)
                bare_quoted_string.append(token)

        value or bare_quoted_string.defects.append(errors.InvalidHeaderDefect('end of header inside quoted string'))
        return (bare_quoted_string, value)
    return (
     bare_quoted_string, value[1:])


def get_comment(value):
    """comment = "(" *([FWS] ccontent) [FWS] ")"
       ccontent = ctext / quoted-pair / comment

    We handle nested comments here, and quoted-pair in our qp-ctext routine.
    """
    if value:
        if value[0] != '(':
            raise errors.HeaderParseError("expected '(' but found '{}'".format(value))
    else:
        comment = Comment()
        value = value[1:]
        while value:
            if value[0] != ')':
                if value[0] in WSP:
                    token, value = get_fws(value)
                else:
                    if value[0] == '(':
                        token, value = get_comment(value)
                    else:
                        token, value = get_qp_ctext(value)
                comment.append(token)

        value or comment.defects.append(errors.InvalidHeaderDefect('end of header inside comment'))
        return (comment, value)
    return (
     comment, value[1:])


def get_cfws(value):
    """CFWS = (1*([FWS] comment) [FWS]) / FWS

    """
    cfws = CFWSList()
    while value:
        if value[0] in CFWS_LEADER:
            if value[0] in WSP:
                token, value = get_fws(value)
            else:
                token, value = get_comment(value)
            cfws.append(token)

    return (
     cfws, value)


def get_quoted_string(value):
    """quoted-string = [CFWS] <bare-quoted-string> [CFWS]

    'bare-quoted-string' is an intermediate class defined by this
    parser and not by the RFC grammar.  It is the quoted string
    without any attached CFWS.
    """
    quoted_string = QuotedString()
    if value:
        if value[0] in CFWS_LEADER:
            token, value = get_cfws(value)
            quoted_string.append(token)
    token, value = get_bare_quoted_string(value)
    quoted_string.append(token)
    if value:
        if value[0] in CFWS_LEADER:
            token, value = get_cfws(value)
            quoted_string.append(token)
    return (
     quoted_string, value)


def get_atom(value):
    """atom = [CFWS] 1*atext [CFWS]

    An atom could be an rfc2047 encoded word.
    """
    atom = Atom()
    if value:
        if value[0] in CFWS_LEADER:
            token, value = get_cfws(value)
            atom.append(token)
    if value:
        if value[0] in ATOM_ENDS:
            raise errors.HeaderParseError("expected atom but found '{}'".format(value))
    elif value.startswith('=?'):
        try:
            token, value = get_encoded_word(value)
        except errors.HeaderParseError:
            token, value = get_atext(value)

    else:
        token, value = get_atext(value)
    atom.append(token)
    if value:
        if value[0] in CFWS_LEADER:
            token, value = get_cfws(value)
            atom.append(token)
    return (
     atom, value)


def get_dot_atom_text(value):
    """ dot-text = 1*atext *("." 1*atext)

    """
    dot_atom_text = DotAtomText()
    if not value or value[0] in ATOM_ENDS:
        raise errors.HeaderParseError("expected atom at a start of dot-atom-text but found '{}'".format(value))
    else:
        while value:
            if value[0] not in ATOM_ENDS:
                token, value = get_atext(value)
                dot_atom_text.append(token)
                if value and value[0] == '.':
                    dot_atom_text.append(DOT)
                    value = value[1:]

    if dot_atom_text[(-1)] is DOT:
        raise errors.HeaderParseError("expected atom at end of dot-atom-text but found '{}'".format('.' + value))
    return (
     dot_atom_text, value)


def get_dot_atom(value):
    """ dot-atom = [CFWS] dot-atom-text [CFWS]

    Any place we can have a dot atom, we could instead have an rfc2047 encoded
    word.
    """
    dot_atom = DotAtom()
    if value[0] in CFWS_LEADER:
        token, value = get_cfws(value)
        dot_atom.append(token)
    elif value.startswith('=?'):
        try:
            token, value = get_encoded_word(value)
        except errors.HeaderParseError:
            token, value = get_dot_atom_text(value)

    else:
        token, value = get_dot_atom_text(value)
    dot_atom.append(token)
    if value:
        if value[0] in CFWS_LEADER:
            token, value = get_cfws(value)
            dot_atom.append(token)
    return (
     dot_atom, value)


def get_word(value):
    """word = atom / quoted-string

    Either atom or quoted-string may start with CFWS.  We have to peel off this
    CFWS first to determine which type of word to parse.  Afterward we splice
    the leading CFWS, if any, into the parsed sub-token.

    If neither an atom or a quoted-string is found before the next special, a
    HeaderParseError is raised.

    The token returned is either an Atom or a QuotedString, as appropriate.
    This means the 'word' level of the formal grammar is not represented in the
    parse tree; this is because having that extra layer when manipulating the
    parse tree is more confusing than it is helpful.

    """
    if value[0] in CFWS_LEADER:
        leader, value = get_cfws(value)
    else:
        leader = None
    if not value:
        raise errors.HeaderParseError("Expected 'atom' or 'quoted-string' but found nothing.")
    elif value[0] == '"':
        token, value = get_quoted_string(value)
    else:
        if value[0] in SPECIALS:
            raise errors.HeaderParseError("Expected 'atom' or 'quoted-string' but found '{}'".format(value))
        else:
            token, value = get_atom(value)
    if leader is not None:
        token[:0] = [
         leader]
    return (
     token, value)


def get_phrase(value):
    """ phrase = 1*word / obs-phrase
        obs-phrase = word *(word / "." / CFWS)

    This means a phrase can be a sequence of words, periods, and CFWS in any
    order as long as it starts with at least one word.  If anything other than
    words is detected, an ObsoleteHeaderDefect is added to the token's defect
    list.  We also accept a phrase that starts with CFWS followed by a dot;
    this is registered as an InvalidHeaderDefect, since it is not supported by
    even the obsolete grammar.

    """
    phrase = Phrase()
    try:
        token, value = get_word(value)
        phrase.append(token)
    except errors.HeaderParseError:
        phrase.defects.append(errors.InvalidHeaderDefect('phrase does not start with word'))
    else:
        while value:
            if value[0] not in PHRASE_ENDS:
                if value[0] == '.':
                    phrase.append(DOT)
                    phrase.defects.append(errors.ObsoleteHeaderDefect("period in 'phrase'"))
                    value = value[1:]
            else:
                try:
                    token, value = get_word(value)
                except errors.HeaderParseError:
                    if value[0] in CFWS_LEADER:
                        token, value = get_cfws(value)
                        phrase.defects.append(errors.ObsoleteHeaderDefect('comment found without atom'))
                    else:
                        raise
                else:
                    phrase.append(token)

        return (
         phrase, value)


def get_local_part(value):
    """ local-part = dot-atom / quoted-string / obs-local-part

    """
    local_part = LocalPart()
    leader = None
    if value[0] in CFWS_LEADER:
        leader, value = get_cfws(value)
    if not value:
        raise errors.HeaderParseError("expected local-part but found '{}'".format(value))
    try:
        token, value = get_dot_atom(value)
    except errors.HeaderParseError:
        try:
            token, value = get_word(value)
        except errors.HeaderParseError:
            if value[0] != '\\':
                if value[0] in PHRASE_ENDS:
                    raise
            token = TokenList()

    else:
        if leader is not None:
            token[:0] = [
             leader]
        local_part.append(token)
        if value:
            if not value[0] == '\\':
                if value[0] not in PHRASE_ENDS:
                    obs_local_part, value = get_obs_local_part(str(local_part) + value)
                    if obs_local_part.token_type == 'invalid-obs-local-part':
                        local_part.defects.append(errors.InvalidHeaderDefect('local-part is not dot-atom, quoted-string, or obs-local-part'))
                    else:
                        local_part.defects.append(errors.ObsoleteHeaderDefect('local-part is not a dot-atom (contains CFWS)'))
                    local_part[0] = obs_local_part
                try:
                    local_part.value.encode('ascii')
                except UnicodeEncodeError:
                    local_part.defects.append(errors.NonASCIILocalPartDefect('local-part contains non-ASCII characters)'))
                else:
                    return (
                     local_part, value)


def get_obs_local_part--- This code section failed: ---

 L.1477         0  LOAD_GLOBAL              ObsLocalPart
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'obs_local_part'

 L.1478         6  LOAD_CONST               False
                8  STORE_FAST               'last_non_ws_was_dot'

 L.1479        10  LOAD_FAST                'value'
            12_14  POP_JUMP_IF_FALSE   296  'to 296'
               16  LOAD_FAST                'value'
               18  LOAD_CONST               0
               20  BINARY_SUBSCR    
               22  LOAD_STR                 '\\'
               24  COMPARE_OP               ==
               26  POP_JUMP_IF_TRUE     42  'to 42'
               28  LOAD_FAST                'value'
               30  LOAD_CONST               0
               32  BINARY_SUBSCR    
               34  LOAD_GLOBAL              PHRASE_ENDS
               36  COMPARE_OP               not-in
            38_40  POP_JUMP_IF_FALSE   296  'to 296'
             42_0  COME_FROM            26  '26'

 L.1480        42  LOAD_FAST                'value'
               44  LOAD_CONST               0
               46  BINARY_SUBSCR    
               48  LOAD_STR                 '.'
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE   106  'to 106'

 L.1481        54  LOAD_FAST                'last_non_ws_was_dot'
               56  POP_JUMP_IF_FALSE    76  'to 76'

 L.1482        58  LOAD_FAST                'obs_local_part'
               60  LOAD_ATTR                defects
               62  LOAD_METHOD              append
               64  LOAD_GLOBAL              errors
               66  LOAD_METHOD              InvalidHeaderDefect

 L.1483        68  LOAD_STR                 "invalid repeated '.'"

 L.1482        70  CALL_METHOD_1         1  ''
               72  CALL_METHOD_1         1  ''
               74  POP_TOP          
             76_0  COME_FROM            56  '56'

 L.1484        76  LOAD_FAST                'obs_local_part'
               78  LOAD_METHOD              append
               80  LOAD_GLOBAL              DOT
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          

 L.1485        86  LOAD_CONST               True
               88  STORE_FAST               'last_non_ws_was_dot'

 L.1486        90  LOAD_FAST                'value'
               92  LOAD_CONST               1
               94  LOAD_CONST               None
               96  BUILD_SLICE_2         2 
               98  BINARY_SUBSCR    
              100  STORE_FAST               'value'

 L.1487       102  JUMP_BACK            10  'to 10'
              104  JUMP_FORWARD        174  'to 174'
            106_0  COME_FROM            52  '52'

 L.1488       106  LOAD_FAST                'value'
              108  LOAD_CONST               0
              110  BINARY_SUBSCR    
              112  LOAD_STR                 '\\'
              114  COMPARE_OP               ==
              116  POP_JUMP_IF_FALSE   174  'to 174'

 L.1489       118  LOAD_FAST                'obs_local_part'
              120  LOAD_METHOD              append
              122  LOAD_GLOBAL              ValueTerminal
              124  LOAD_FAST                'value'
              126  LOAD_CONST               0
              128  BINARY_SUBSCR    

 L.1490       130  LOAD_STR                 'misplaced-special'

 L.1489       132  CALL_FUNCTION_2       2  ''
              134  CALL_METHOD_1         1  ''
              136  POP_TOP          

 L.1491       138  LOAD_FAST                'value'
              140  LOAD_CONST               1
              142  LOAD_CONST               None
              144  BUILD_SLICE_2         2 
              146  BINARY_SUBSCR    
              148  STORE_FAST               'value'

 L.1492       150  LOAD_FAST                'obs_local_part'
              152  LOAD_ATTR                defects
              154  LOAD_METHOD              append
              156  LOAD_GLOBAL              errors
              158  LOAD_METHOD              InvalidHeaderDefect

 L.1493       160  LOAD_STR                 "'\\' character outside of quoted-string/ccontent"

 L.1492       162  CALL_METHOD_1         1  ''
              164  CALL_METHOD_1         1  ''
              166  POP_TOP          

 L.1494       168  LOAD_CONST               False
              170  STORE_FAST               'last_non_ws_was_dot'

 L.1495       172  JUMP_BACK            10  'to 10'
            174_0  COME_FROM           116  '116'
            174_1  COME_FROM           104  '104'

 L.1496       174  LOAD_FAST                'obs_local_part'
              176  POP_JUMP_IF_FALSE   210  'to 210'
              178  LOAD_FAST                'obs_local_part'
              180  LOAD_CONST               -1
              182  BINARY_SUBSCR    
              184  LOAD_ATTR                token_type
              186  LOAD_STR                 'dot'
              188  COMPARE_OP               !=
              190  POP_JUMP_IF_FALSE   210  'to 210'

 L.1497       192  LOAD_FAST                'obs_local_part'
              194  LOAD_ATTR                defects
              196  LOAD_METHOD              append
              198  LOAD_GLOBAL              errors
              200  LOAD_METHOD              InvalidHeaderDefect

 L.1498       202  LOAD_STR                 "missing '.' between words"

 L.1497       204  CALL_METHOD_1         1  ''
              206  CALL_METHOD_1         1  ''
              208  POP_TOP          
            210_0  COME_FROM           190  '190'
            210_1  COME_FROM           176  '176'

 L.1499       210  SETUP_FINALLY       232  'to 232'

 L.1500       212  LOAD_GLOBAL              get_word
              214  LOAD_FAST                'value'
              216  CALL_FUNCTION_1       1  ''
              218  UNPACK_SEQUENCE_2     2 
              220  STORE_FAST               'token'
              222  STORE_FAST               'value'

 L.1501       224  LOAD_CONST               False
              226  STORE_FAST               'last_non_ws_was_dot'
              228  POP_BLOCK        
              230  JUMP_FORWARD        284  'to 284'
            232_0  COME_FROM_FINALLY   210  '210'

 L.1502       232  DUP_TOP          
              234  LOAD_GLOBAL              errors
              236  LOAD_ATTR                HeaderParseError
              238  COMPARE_OP               exception-match
          240_242  POP_JUMP_IF_FALSE   282  'to 282'
              244  POP_TOP          
              246  POP_TOP          
              248  POP_TOP          

 L.1503       250  LOAD_FAST                'value'
              252  LOAD_CONST               0
              254  BINARY_SUBSCR    
              256  LOAD_GLOBAL              CFWS_LEADER
              258  COMPARE_OP               not-in
          260_262  POP_JUMP_IF_FALSE   266  'to 266'

 L.1504       264  RAISE_VARARGS_0       0  'reraise'
            266_0  COME_FROM           260  '260'

 L.1505       266  LOAD_GLOBAL              get_cfws
              268  LOAD_FAST                'value'
              270  CALL_FUNCTION_1       1  ''
              272  UNPACK_SEQUENCE_2     2 
              274  STORE_FAST               'token'
              276  STORE_FAST               'value'
              278  POP_EXCEPT       
              280  JUMP_FORWARD        284  'to 284'
            282_0  COME_FROM           240  '240'
              282  END_FINALLY      
            284_0  COME_FROM           280  '280'
            284_1  COME_FROM           230  '230'

 L.1506       284  LOAD_FAST                'obs_local_part'
              286  LOAD_METHOD              append
              288  LOAD_FAST                'token'
              290  CALL_METHOD_1         1  ''
              292  POP_TOP          
              294  JUMP_BACK            10  'to 10'
            296_0  COME_FROM            38  '38'
            296_1  COME_FROM            12  '12'

 L.1507       296  LOAD_FAST                'obs_local_part'
              298  LOAD_CONST               0
              300  BINARY_SUBSCR    
              302  LOAD_ATTR                token_type
              304  LOAD_STR                 'dot'
              306  COMPARE_OP               ==
          308_310  POP_JUMP_IF_TRUE    344  'to 344'

 L.1508       312  LOAD_FAST                'obs_local_part'
              314  LOAD_CONST               0
              316  BINARY_SUBSCR    
              318  LOAD_ATTR                token_type
              320  LOAD_STR                 'cfws'
              322  COMPARE_OP               ==

 L.1507   324_326  POP_JUMP_IF_FALSE   362  'to 362'

 L.1509       328  LOAD_FAST                'obs_local_part'
              330  LOAD_CONST               1
              332  BINARY_SUBSCR    
              334  LOAD_ATTR                token_type
              336  LOAD_STR                 'dot'
              338  COMPARE_OP               ==

 L.1507   340_342  POP_JUMP_IF_FALSE   362  'to 362'
            344_0  COME_FROM           308  '308'

 L.1510       344  LOAD_FAST                'obs_local_part'
              346  LOAD_ATTR                defects
              348  LOAD_METHOD              append
              350  LOAD_GLOBAL              errors
              352  LOAD_METHOD              InvalidHeaderDefect

 L.1511       354  LOAD_STR                 "Invalid leading '.' in local part"

 L.1510       356  CALL_METHOD_1         1  ''
              358  CALL_METHOD_1         1  ''
              360  POP_TOP          
            362_0  COME_FROM           340  '340'
            362_1  COME_FROM           324  '324'

 L.1512       362  LOAD_FAST                'obs_local_part'
              364  LOAD_CONST               -1
              366  BINARY_SUBSCR    
              368  LOAD_ATTR                token_type
              370  LOAD_STR                 'dot'
              372  COMPARE_OP               ==
          374_376  POP_JUMP_IF_TRUE    410  'to 410'

 L.1513       378  LOAD_FAST                'obs_local_part'
              380  LOAD_CONST               -1
              382  BINARY_SUBSCR    
              384  LOAD_ATTR                token_type
              386  LOAD_STR                 'cfws'
              388  COMPARE_OP               ==

 L.1512   390_392  POP_JUMP_IF_FALSE   428  'to 428'

 L.1514       394  LOAD_FAST                'obs_local_part'
              396  LOAD_CONST               -2
              398  BINARY_SUBSCR    
              400  LOAD_ATTR                token_type
              402  LOAD_STR                 'dot'
              404  COMPARE_OP               ==

 L.1512   406_408  POP_JUMP_IF_FALSE   428  'to 428'
            410_0  COME_FROM           374  '374'

 L.1515       410  LOAD_FAST                'obs_local_part'
              412  LOAD_ATTR                defects
              414  LOAD_METHOD              append
              416  LOAD_GLOBAL              errors
              418  LOAD_METHOD              InvalidHeaderDefect

 L.1516       420  LOAD_STR                 "Invalid trailing '.' in local part"

 L.1515       422  CALL_METHOD_1         1  ''
              424  CALL_METHOD_1         1  ''
              426  POP_TOP          
            428_0  COME_FROM           406  '406'
            428_1  COME_FROM           390  '390'

 L.1517       428  LOAD_FAST                'obs_local_part'
              430  LOAD_ATTR                defects
          432_434  POP_JUMP_IF_FALSE   442  'to 442'

 L.1518       436  LOAD_STR                 'invalid-obs-local-part'
              438  LOAD_FAST                'obs_local_part'
              440  STORE_ATTR               token_type
            442_0  COME_FROM           432  '432'

 L.1519       442  LOAD_FAST                'obs_local_part'
              444  LOAD_FAST                'value'
              446  BUILD_TUPLE_2         2 
              448  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 104


def get_dtext(value):
    r""" dtext = <printable ascii except \ [ ]> / obs-dtext
        obs-dtext = obs-NO-WS-CTL / quoted-pair

    We allow anything except the excluded characters, but if we find any
    ASCII other than the RFC defined printable ASCII, a NonPrintableDefect is
    added to the token's defects list.  Quoted pairs are converted to their
    unquoted values, so what is returned is a ptext token, in this case a
    ValueTerminal.  If there were quoted-printables, an ObsoleteHeaderDefect is
    added to the returned token's defect list.

    """
    ptext, value, had_qp = _get_ptext_to_endchars(value, '[]')
    ptext = ValueTerminal(ptext, 'ptext')
    if had_qp:
        ptext.defects.append(errors.ObsoleteHeaderDefect('quoted printable found in domain-literal'))
    _validate_xtext(ptext)
    return (ptext, value)


def _check_for_early_dl_end(value, domain_literal):
    if value:
        return False
    domain_literal.append(errors.InvalidHeaderDefect('end of input inside domain-literal'))
    domain_literal.append(ValueTerminal(']', 'domain-literal-end'))
    return True


def get_domain_literal(value):
    """ domain-literal = [CFWS] "[" *([FWS] dtext) [FWS] "]" [CFWS]

    """
    domain_literal = DomainLiteral()
    if value[0] in CFWS_LEADER:
        token, value = get_cfws(value)
        domain_literal.append(token)
    if not value:
        raise errors.HeaderParseError('expected domain-literal')
    if value[0] != '[':
        raise errors.HeaderParseError("expected '[' at start of domain-literal but found '{}'".format(value))
    value = value[1:]
    if _check_for_early_dl_end(value, domain_literal):
        return (
         domain_literal, value)
    domain_literal.append(ValueTerminal('[', 'domain-literal-start'))
    if value[0] in WSP:
        token, value = get_fws(value)
        domain_literal.append(token)
    token, value = get_dtext(value)
    domain_literal.append(token)
    if _check_for_early_dl_end(value, domain_literal):
        return (
         domain_literal, value)
    if value[0] in WSP:
        token, value = get_fws(value)
        domain_literal.append(token)
    if _check_for_early_dl_end(value, domain_literal):
        return (
         domain_literal, value)
    if value[0] != ']':
        raise errors.HeaderParseError("expected ']' at end of domain-literal but found '{}'".format(value))
    domain_literal.append(ValueTerminal(']', 'domain-literal-end'))
    value = value[1:]
    if value:
        if value[0] in CFWS_LEADER:
            token, value = get_cfws(value)
            domain_literal.append(token)
    return (
     domain_literal, value)


def get_domain(value):
    """ domain = dot-atom / domain-literal / obs-domain
        obs-domain = atom *("." atom))

    """
    domain = Domain()
    leader = None
    if value[0] in CFWS_LEADER:
        leader, value = get_cfws(value)
    if not value:
        raise errors.HeaderParseError("expected domain but found '{}'".format(value))
    if value[0] == '[':
        token, value = get_domain_literal(value)
        if leader is not None:
            token[:0] = [
             leader]
        domain.append(token)
        return (domain, value)
    try:
        token, value = get_dot_atom(value)
    except errors.HeaderParseError:
        token, value = get_atom(value)
    else:
        if value:
            if value[0] == '@':
                raise errors.HeaderParseError('Invalid Domain')
        if leader is not None:
            token[:0] = [
             leader]
        domain.append(token)
        if value and value[0] == '.':
            domain.defects.append(errors.ObsoleteHeaderDefect('domain is not a dot-atom (contains CFWS)'))
            if domain[0].token_type == 'dot-atom':
                domain[:] = domain[0]
            if value and value[0] == '.':
                domain.append(DOT)
                token, value = get_atom(value[1:])
                domain.append(token)
        else:
            return (
             domain, value)


def get_addr_spec(value):
    """ addr-spec = local-part "@" domain

    """
    addr_spec = AddrSpec()
    token, value = get_local_part(value)
    addr_spec.append(token)
    if not value or value[0] != '@':
        addr_spec.defects.append(errors.InvalidHeaderDefect('addr-spec local part with no domain'))
        return (addr_spec, value)
    addr_spec.append(ValueTerminal('@', 'address-at-symbol'))
    token, value = get_domain(value[1:])
    addr_spec.append(token)
    return (addr_spec, value)


def get_obs_route(value):
    """ obs-route = obs-domain-list ":"
        obs-domain-list = *(CFWS / ",") "@" domain *("," [CFWS] ["@" domain])

        Returns an obs-route token with the appropriate sub-tokens (that is,
        there is no obs-domain-list in the parse tree).
    """
    obs_route = ObsRoute()
    while value:
        if value[0] == ',' or value[0] in CFWS_LEADER:
            if value[0] in CFWS_LEADER:
                token, value = get_cfws(value)
                obs_route.append(token)
        elif value[0] == ',':
            obs_route.append(ListSeparator)
            value = value[1:]

    if value:
        if value[0] != '@':
            raise errors.HeaderParseError("expected obs-route domain but found '{}'".format(value))
        obs_route.append(RouteComponentMarker)
        token, value = get_domain(value[1:])
        obs_route.append(token)
    else:
        while value:
            if value[0] == ',':
                obs_route.append(ListSeparator)
                value = value[1:]
                if not value:
                    break
                if value[0] in CFWS_LEADER:
                    token, value = get_cfws(value)
                    obs_route.append(token)
                if value[0] == '@':
                    obs_route.append(RouteComponentMarker)
                    token, value = get_domain(value[1:])
                    obs_route.append(token)

    if not value:
        raise errors.HeaderParseError('end of header while parsing obs-route')
    if value[0] != ':':
        raise errors.HeaderParseError("expected ':' marking end of obs-route but found '{}'".format(value))
    obs_route.append(ValueTerminal(':', 'end-of-obs-route-marker'))
    return (obs_route, value[1:])


def get_angle_addr(value):
    """ angle-addr = [CFWS] "<" addr-spec ">" [CFWS] / obs-angle-addr
        obs-angle-addr = [CFWS] "<" obs-route addr-spec ">" [CFWS]

    """
    angle_addr = AngleAddr()
    if value[0] in CFWS_LEADER:
        token, value = get_cfws(value)
        angle_addr.append(token)
    if not value or value[0] != '<':
        raise errors.HeaderParseError("expected angle-addr but found '{}'".format(value))
    angle_addr.append(ValueTerminal('<', 'angle-addr-start'))
    value = value[1:]
    if value[0] == '>':
        angle_addr.append(ValueTerminal('>', 'angle-addr-end'))
        angle_addr.defects.append(errors.InvalidHeaderDefect('null addr-spec in angle-addr'))
        value = value[1:]
        return (angle_addr, value)
    try:
        token, value = get_addr_spec(value)
    except errors.HeaderParseError:
        try:
            token, value = get_obs_route(value)
            angle_addr.defects.append(errors.ObsoleteHeaderDefect('obsolete route specification in angle-addr'))
        except errors.HeaderParseError:
            raise errors.HeaderParseError("expected addr-spec or obs-route but found '{}'".format(value))
        else:
            angle_addr.append(token)
            token, value = get_addr_spec(value)
    else:
        angle_addr.append(token)
        if value and value[0] == '>':
            value = value[1:]
        else:
            angle_addr.defects.append(errors.InvalidHeaderDefect("missing trailing '>' on angle-addr"))
        angle_addr.append(ValueTerminal('>', 'angle-addr-end'))
        if value:
            if value[0] in CFWS_LEADER:
                token, value = get_cfws(value)
                angle_addr.append(token)
        return (
         angle_addr, value)


def get_display_name(value):
    """ display-name = phrase

    Because this is simply a name-rule, we don't return a display-name
    token containing a phrase, but rather a display-name token with
    the content of the phrase.

    """
    display_name = DisplayName()
    token, value = get_phrase(value)
    display_name.extend(token[:])
    display_name.defects = token.defects[:]
    return (display_name, value)


def get_name_addr(value):
    """ name-addr = [display-name] angle-addr

    """
    name_addr = NameAddr()
    leader = None
    if value[0] in CFWS_LEADER:
        leader, value = get_cfws(value)
        if not value:
            raise errors.HeaderParseError("expected name-addr but found '{}'".format(leader))
    if value[0] != '<':
        if value[0] in PHRASE_ENDS:
            raise errors.HeaderParseError("expected name-addr but found '{}'".format(value))
        token, value = get_display_name(value)
        if not value:
            raise errors.HeaderParseError("expected name-addr but found '{}'".format(token))
        if leader is not None:
            token[0][:0] = [
             leader]
            leader = None
        name_addr.append(token)
    token, value = get_angle_addr(value)
    if leader is not None:
        token[:0] = [
         leader]
    name_addr.append(token)
    return (name_addr, value)


def get_mailbox(value):
    """ mailbox = name-addr / addr-spec

    """
    mailbox = Mailbox()
    try:
        token, value = get_name_addr(value)
    except errors.HeaderParseError:
        try:
            token, value = get_addr_spec(value)
        except errors.HeaderParseError:
            raise errors.HeaderParseError("expected mailbox but found '{}'".format(value))

    else:
        if any((isinstance(x, errors.InvalidHeaderDefect) for x in token.all_defects)):
            mailbox.token_type = 'invalid-mailbox'
        mailbox.append(token)
        return (mailbox, value)


def get_invalid_mailbox(value, endchars):
    """ Read everything up to one of the chars in endchars.

    This is outside the formal grammar.  The InvalidMailbox TokenList that is
    returned acts like a Mailbox, but the data attributes are None.

    """
    invalid_mailbox = InvalidMailbox()
    while value:
        if value[0] not in endchars:
            if value[0] in PHRASE_ENDS:
                invalid_mailbox.append(ValueTerminal(value[0], 'misplaced-special'))
                value = value[1:]
        else:
            token, value = get_phrase(value)
            invalid_mailbox.append(token)

    return (
     invalid_mailbox, value)


def get_mailbox_list(value):
    """ mailbox-list = (mailbox *("," mailbox)) / obs-mbox-list
        obs-mbox-list = *([CFWS] ",") mailbox *("," [mailbox / CFWS])

    For this routine we go outside the formal grammar in order to improve error
    handling.  We recognize the end of the mailbox list only at the end of the
    value or at a ';' (the group terminator).  This is so that we can turn
    invalid mailboxes into InvalidMailbox tokens and continue parsing any
    remaining valid mailboxes.  We also allow all mailbox entries to be null,
    and this condition is handled appropriately at a higher level.

    """
    mailbox_list = MailboxList()
    while value and value[0] != ';':
        try:
            token, value = get_mailbox(value)
            mailbox_list.append(token)
        except errors.HeaderParseError:
            leader = None
            if value[0] in CFWS_LEADER:
                leader, value = get_cfws(value)
                if not value or value[0] in ',;':
                    mailbox_list.append(leader)
                    mailbox_list.defects.append(errors.ObsoleteHeaderDefect('empty element in mailbox-list'))
                else:
                    token, value = get_invalid_mailbox(value, ',;')
                    if leader is not None:
                        token[:0] = [
                         leader]
                    mailbox_list.append(token)
                    mailbox_list.defects.append(errors.InvalidHeaderDefect('invalid mailbox in mailbox-list'))
            else:
                if value[0] == ',':
                    mailbox_list.defects.append(errors.ObsoleteHeaderDefect('empty element in mailbox-list'))
                else:
                    token, value = get_invalid_mailbox(value, ',;')
                    if leader is not None:
                        token[:0] = [
                         leader]
                    mailbox_list.append(token)
                    mailbox_list.defects.append(errors.InvalidHeaderDefect('invalid mailbox in mailbox-list'))
        else:
            if value:
                if value[0] not in ',;':
                    mailbox = mailbox_list[(-1)]
                    mailbox.token_type = 'invalid-mailbox'
                    token, value = get_invalid_mailbox(value, ',;')
                    mailbox.extend(token)
                    mailbox_list.defects.append(errors.InvalidHeaderDefect('invalid mailbox in mailbox-list'))
            if value and value[0] == ',':
                mailbox_list.append(ListSeparator)
                value = value[1:]

    return (
     mailbox_list, value)


def get_group_list(value):
    """ group-list = mailbox-list / CFWS / obs-group-list
        obs-group-list = 1*([CFWS] ",") [CFWS]

    """
    group_list = GroupList()
    if not value:
        group_list.defects.append(errors.InvalidHeaderDefect('end of header before group-list'))
        return (group_list, value)
    else:
        leader = None
        if value:
            if value[0] in CFWS_LEADER:
                leader, value = get_cfws(value)
                if not value:
                    group_list.defects.append(errors.InvalidHeaderDefect('end of header in group-list'))
                    group_list.append(leader)
                    return (group_list, value)
                if value[0] == ';':
                    group_list.append(leader)
                    return (group_list, value)
    token, value = get_mailbox_list(value)
    if len(token.all_mailboxes) == 0:
        if leader is not None:
            group_list.append(leader)
        group_list.extend(token)
        group_list.defects.append(errors.ObsoleteHeaderDefect('group-list with empty entries'))
        return (group_list, value)
    if leader is not None:
        token[:0] = [
         leader]
    group_list.append(token)
    return (group_list, value)


def get_group(value):
    """ group = display-name ":" [group-list] ";" [CFWS]

    """
    group = Group()
    token, value = get_display_name(value)
    if value:
        if value[0] != ':':
            raise errors.HeaderParseError("expected ':' at end of group display name but found '{}'".format(value))
        group.append(token)
        group.append(ValueTerminal(':', 'group-display-name-terminator'))
        value = value[1:]
        if value:
            if value[0] == ';':
                group.append(ValueTerminal(';', 'group-terminator'))
                return (group, value[1:])
        token, value = get_group_list(value)
        group.append(token)
        value or group.defects.append(errors.InvalidHeaderDefect('end of header in group'))
    else:
        if value[0] != ';':
            raise errors.HeaderParseError("expected ';' at end of group but found {}".format(value))
        else:
            group.append(ValueTerminal(';', 'group-terminator'))
            value = value[1:]
            if value and value[0] in CFWS_LEADER:
                token, value = get_cfws(value)
                group.append(token)
        return (
         group, value)


def get_address(value):
    """ address = mailbox / group

    Note that counter-intuitively, an address can be either a single address or
    a list of addresses (a group).  This is why the returned Address object has
    a 'mailboxes' attribute which treats a single address as a list of length
    one.  When you need to differentiate between to two cases, extract the single
    element, which is either a mailbox or a group token.

    """
    address = Address()
    try:
        token, value = get_group(value)
    except errors.HeaderParseError:
        try:
            token, value = get_mailbox(value)
        except errors.HeaderParseError:
            raise errors.HeaderParseError("expected address but found '{}'".format(value))

    else:
        address.append(token)
        return (address, value)


def get_address_list(value):
    """ address_list = (address *("," address)) / obs-addr-list
        obs-addr-list = *([CFWS] ",") address *("," [address / CFWS])

    We depart from the formal grammar here by continuing to parse until the end
    of the input, assuming the input to be entirely composed of an
    address-list.  This is always true in email parsing, and allows us
    to skip invalid addresses to parse additional valid ones.

    """
    address_list = AddressList()
    while value:
        try:
            token, value = get_address(value)
            address_list.append(token)
        except errors.HeaderParseError as err:
            try:
                leader = None
                if value[0] in CFWS_LEADER:
                    leader, value = get_cfws(value)
                    if not value or value[0] == ',':
                        address_list.append(leader)
                        address_list.defects.append(errors.ObsoleteHeaderDefect('address-list entry with no content'))
                    else:
                        token, value = get_invalid_mailbox(value, ',')
                        if leader is not None:
                            token[:0] = [
                             leader]
                        address_list.append(Address([token]))
                        address_list.defects.append(errors.InvalidHeaderDefect('invalid address in address-list'))
                else:
                    if value[0] == ',':
                        address_list.defects.append(errors.ObsoleteHeaderDefect('empty element in address-list'))
                    else:
                        token, value = get_invalid_mailbox(value, ',')
                        if leader is not None:
                            token[:0] = [
                             leader]
                        address_list.append(Address([token]))
                        address_list.defects.append(errors.InvalidHeaderDefect('invalid address in address-list'))
            finally:
                err = None
                del err

        else:
            if value:
                if value[0] != ',':
                    mailbox = address_list[(-1)][0]
                    mailbox.token_type = 'invalid-mailbox'
                    token, value = get_invalid_mailbox(value, ',')
                    mailbox.extend(token)
                    address_list.defects.append(errors.InvalidHeaderDefect('invalid address in address-list'))
            if value:
                address_list.append(ValueTerminal(',', 'list-separator'))
                value = value[1:]

    return (
     address_list, value)


def get_no_fold_literal(value):
    """ no-fold-literal = "[" *dtext "]"
    """
    no_fold_literal = NoFoldLiteral()
    if not value:
        raise errors.HeaderParseError("expected no-fold-literal but found '{}'".format(value))
    if value[0] != '[':
        raise errors.HeaderParseError("expected '[' at the start of no-fold-literal but found '{}'".format(value))
    no_fold_literal.append(ValueTerminal('[', 'no-fold-literal-start'))
    value = value[1:]
    token, value = get_dtext(value)
    no_fold_literal.append(token)
    if not value or value[0] != ']':
        raise errors.HeaderParseError("expected ']' at the end of no-fold-literal but found '{}'".format(value))
    no_fold_literal.append(ValueTerminal(']', 'no-fold-literal-end'))
    return (no_fold_literal, value[1:])


def get_msg_id(value):
    """msg-id = [CFWS] "<" id-left '@' id-right  ">" [CFWS]
       id-left = dot-atom-text / obs-id-left
       id-right = dot-atom-text / no-fold-literal / obs-id-right
       no-fold-literal = "[" *dtext "]"
    """
    msg_id = MsgID()
    if value:
        if value[0] in CFWS_LEADER:
            token, value = get_cfws(value)
            msg_id.append(token)
    if not value or value[0] != '<':
        raise errors.HeaderParseError("expected msg-id but found '{}'".format(value))
    msg_id.append(ValueTerminal('<', 'msg-id-start'))
    value = value[1:]
    try:
        token, value = get_dot_atom_text(value)
    except errors.HeaderParseError:
        try:
            token, value = get_obs_local_part(value)
            msg_id.defects.append(errors.ObsoleteHeaderDefect('obsolete id-left in msg-id'))
        except errors.HeaderParseError:
            raise errors.HeaderParseError("expected dot-atom-text or obs-id-left but found '{}'".format(value))

    else:
        msg_id.append(token)
        if not value or value[0] != '@':
            msg_id.defects.append(errors.InvalidHeaderDefect('msg-id with no id-right'))
            if value:
                if value[0] == '>':
                    msg_id.append(ValueTerminal('>', 'msg-id-end'))
                    value = value[1:]
            return (
             msg_id, value)
        msg_id.append(ValueTerminal('@', 'address-at-symbol'))
        value = value[1:]
    try:
        token, value = get_dot_atom_text(value)
    except errors.HeaderParseError:
        try:
            token, value = get_no_fold_literal(value)
        except errors.HeaderParseError as e:
            try:
                try:
                    token, value = get_domain(value)
                    msg_id.defects.append(errors.ObsoleteHeaderDefect('obsolete id-right in msg-id'))
                except errors.HeaderParseError:
                    raise errors.HeaderParseError("expected dot-atom-text, no-fold-literal or obs-id-right but found '{}'".format(value))

            finally:
                e = None
                del e

    else:
        msg_id.append(token)
        if value and value[0] == '>':
            value = value[1:]
        else:
            msg_id.defects.append(errors.InvalidHeaderDefect("missing trailing '>' on msg-id"))
        msg_id.append(ValueTerminal('>', 'msg-id-end'))
        if value:
            if value[0] in CFWS_LEADER:
                token, value = get_cfws(value)
                msg_id.append(token)
        return (
         msg_id, value)


def parse_message_id(value):
    """message-id      =   "Message-ID:" msg-id CRLF
    """
    message_id = MessageID()
    try:
        token, value = get_msg_id(value)
        message_id.append(token)
    except errors.HeaderParseError as ex:
        try:
            token = get_unstructured(value)
            message_id = InvalidMessageID(token)
            message_id.defects.append(errors.InvalidHeaderDefect('Invalid msg-id: {!r}'.format(ex)))
        finally:
            ex = None
            del ex

    else:
        if value:
            message_id.defects.append(errors.InvalidHeaderDefect('Unexpected {!r}'.format(value)))


def parse_mime_version(value):
    """ mime-version = [CFWS] 1*digit [CFWS] "." [CFWS] 1*digit [CFWS]

    """
    mime_version = MIMEVersion()
    if not value:
        mime_version.defects.append(errors.HeaderMissingRequiredValue('Missing MIME version number (eg: 1.0)'))
        return mime_version
    if value[0] in CFWS_LEADER:
        token, value = get_cfws(value)
        mime_version.append(token)
        if not value:
            mime_version.defects.append(errors.HeaderMissingRequiredValue('Expected MIME version number but found only CFWS'))
    digits = ''
    if value:
        if value[0] != '.':
            if value[0] not in CFWS_LEADER:
                digits += value[0]
                value = value[1:]
    elif not digits.isdigit():
        mime_version.defects.append(errors.InvalidHeaderDefect('Expected MIME major version number but found {!r}'.format(digits)))
        mime_version.append(ValueTerminal(digits, 'xtext'))
    else:
        mime_version.major = int(digits)
        mime_version.append(ValueTerminal(digits, 'digits'))
    if value:
        if value[0] in CFWS_LEADER:
            token, value = get_cfws(value)
            mime_version.append(token)
        if not value or value[0] != '.':
            if mime_version.major is not None:
                mime_version.defects.append(errors.InvalidHeaderDefect('Incomplete MIME version; found only major number'))
    else:
        if value:
            mime_version.append(ValueTerminal(value, 'xtext'))
        return mime_version
    mime_version.append(ValueTerminal('.', 'version-separator'))
    value = value[1:]
    if value:
        if value[0] in CFWS_LEADER:
            token, value = get_cfws(value)
            mime_version.append(token)
    if not value:
        if mime_version.major is not None:
            mime_version.defects.append(errors.InvalidHeaderDefect('Incomplete MIME version; found only major number'))
        return mime_version
    digits = ''
    if value:
        if value[0] not in CFWS_LEADER:
            digits += value[0]
            value = value[1:]
    elif not digits.isdigit():
        mime_version.defects.append(errors.InvalidHeaderDefect('Expected MIME minor version number but found {!r}'.format(digits)))
        mime_version.append(ValueTerminal(digits, 'xtext'))
    else:
        mime_version.minor = int(digits)
        mime_version.append(ValueTerminal(digits, 'digits'))
    if value:
        if value[0] in CFWS_LEADER:
            token, value = get_cfws(value)
            mime_version.append(token)
    if value:
        mime_version.defects.append(errors.InvalidHeaderDefect('Excess non-CFWS text after MIME version'))
        mime_version.append(ValueTerminal(value, 'xtext'))
    return mime_version


def get_invalid_parameter(value):
    """ Read everything up to the next ';'.

    This is outside the formal grammar.  The InvalidParameter TokenList that is
    returned acts like a Parameter, but the data attributes are None.

    """
    invalid_parameter = InvalidParameter()
    while value:
        if value[0] != ';':
            if value[0] in PHRASE_ENDS:
                invalid_parameter.append(ValueTerminal(value[0], 'misplaced-special'))
                value = value[1:]
        else:
            token, value = get_phrase(value)
            invalid_parameter.append(token)

    return (
     invalid_parameter, value)


def get_ttext(value):
    """ttext = <matches _ttext_matcher>

    We allow any non-TOKEN_ENDS in ttext, but add defects to the token's
    defects list if we find non-ttext characters.  We also register defects for
    *any* non-printables even though the RFC doesn't exclude all of them,
    because we follow the spirit of RFC 5322.

    """
    m = _non_token_end_matcher(value)
    if not m:
        raise errors.HeaderParseError("expected ttext but found '{}'".format(value))
    ttext = m.group()
    value = value[len(ttext):]
    ttext = ValueTerminal(ttext, 'ttext')
    _validate_xtext(ttext)
    return (ttext, value)


def get_token(value):
    """token = [CFWS] 1*ttext [CFWS]

    The RFC equivalent of ttext is any US-ASCII chars except space, ctls, or
    tspecials.  We also exclude tabs even though the RFC doesn't.

    The RFC implies the CFWS but is not explicit about it in the BNF.

    """
    mtoken = Token()
    if value:
        if value[0] in CFWS_LEADER:
            token, value = get_cfws(value)
            mtoken.append(token)
    if value:
        if value[0] in TOKEN_ENDS:
            raise errors.HeaderParseError("expected token but found '{}'".format(value))
    token, value = get_ttext(value)
    mtoken.append(token)
    if value:
        if value[0] in CFWS_LEADER:
            token, value = get_cfws(value)
            mtoken.append(token)
    return (
     mtoken, value)


def get_attrtext(value):
    """attrtext = 1*(any non-ATTRIBUTE_ENDS character)

    We allow any non-ATTRIBUTE_ENDS in attrtext, but add defects to the
    token's defects list if we find non-attrtext characters.  We also register
    defects for *any* non-printables even though the RFC doesn't exclude all of
    them, because we follow the spirit of RFC 5322.

    """
    m = _non_attribute_end_matcher(value)
    if not m:
        raise errors.HeaderParseError('expected attrtext but found {!r}'.format(value))
    attrtext = m.group()
    value = value[len(attrtext):]
    attrtext = ValueTerminal(attrtext, 'attrtext')
    _validate_xtext(attrtext)
    return (attrtext, value)


def get_attribute(value):
    """ [CFWS] 1*attrtext [CFWS]

    This version of the BNF makes the CFWS explicit, and as usual we use a
    value terminal for the actual run of characters.  The RFC equivalent of
    attrtext is the token characters, with the subtraction of '*', "'", and '%'.
    We include tab in the excluded set just as we do for token.

    """
    attribute = Attribute()
    if value:
        if value[0] in CFWS_LEADER:
            token, value = get_cfws(value)
            attribute.append(token)
    if value:
        if value[0] in ATTRIBUTE_ENDS:
            raise errors.HeaderParseError("expected token but found '{}'".format(value))
    token, value = get_attrtext(value)
    attribute.append(token)
    if value:
        if value[0] in CFWS_LEADER:
            token, value = get_cfws(value)
            attribute.append(token)
    return (
     attribute, value)


def get_extended_attrtext(value):
    """attrtext = 1*(any non-ATTRIBUTE_ENDS character plus '%')

    This is a special parsing routine so that we get a value that
    includes % escapes as a single string (which we decode as a single
    string later).

    """
    m = _non_extended_attribute_end_matcher(value)
    if not m:
        raise errors.HeaderParseError('expected extended attrtext but found {!r}'.format(value))
    attrtext = m.group()
    value = value[len(attrtext):]
    attrtext = ValueTerminal(attrtext, 'extended-attrtext')
    _validate_xtext(attrtext)
    return (attrtext, value)


def get_extended_attribute(value):
    """ [CFWS] 1*extended_attrtext [CFWS]

    This is like the non-extended version except we allow % characters, so that
    we can pick up an encoded value as a single string.

    """
    attribute = Attribute()
    if value:
        if value[0] in CFWS_LEADER:
            token, value = get_cfws(value)
            attribute.append(token)
    if value:
        if value[0] in EXTENDED_ATTRIBUTE_ENDS:
            raise errors.HeaderParseError("expected token but found '{}'".format(value))
    token, value = get_extended_attrtext(value)
    attribute.append(token)
    if value:
        if value[0] in CFWS_LEADER:
            token, value = get_cfws(value)
            attribute.append(token)
    return (
     attribute, value)


def get_section(value):
    """ '*' digits

    The formal BNF is more complicated because leading 0s are not allowed.  We
    check for that and add a defect.  We also assume no CFWS is allowed between
    the '*' and the digits, though the RFC is not crystal clear on that.
    The caller should already have dealt with leading CFWS.

    """
    section = Section()
    if not value or value[0] != '*':
        raise errors.HeaderParseError('Expected section but found {}'.format(value))
    else:
        section.append(ValueTerminal('*', 'section-marker'))
        value = value[1:]
        if not (value and value[0].isdigit()):
            raise errors.HeaderParseError('Expected section number but found {}'.format(value))
        digits = ''
        while value:
            if value[0].isdigit():
                digits += value[0]
                value = value[1:]

    if digits[0] == '0':
        if digits != '0':
            section.defects.append(errors.InvalidHeaderError('section number has an invalid leading 0'))
    section.number = int(digits)
    section.append(ValueTerminal(digits, 'digits'))
    return (section, value)


def get_value(value):
    """ quoted-string / attribute

    """
    v = Value()
    if not value:
        raise errors.HeaderParseError('Expected value but found end of string')
    leader = None
    if value[0] in CFWS_LEADER:
        leader, value = get_cfws(value)
    else:
        if not value:
            raise errors.HeaderParseError('Expected value but found only {}'.format(leader))
        if value[0] == '"':
            token, value = get_quoted_string(value)
        else:
            token, value = get_extended_attribute(value)
    if leader is not None:
        token[:0] = [
         leader]
    v.append(token)
    return (v, value)


def get_parameter(value):
    """ attribute [section] ["*"] [CFWS] "=" value

    The CFWS is implied by the RFC but not made explicit in the BNF.  This
    simplified form of the BNF from the RFC is made to conform with the RFC BNF
    through some extra checks.  We do it this way because it makes both error
    recovery and working with the resulting parse tree easier.
    """
    param = Parameter()
    token, value = get_attribute(value)
    param.append(token)
    if not value or value[0] == ';':
        param.defects.append(errors.InvalidHeaderDefect('Parameter contains name ({}) but no value'.format(token)))
        return (param, value)
    if value[0] == '*':
        try:
            token, value = get_section(value)
            param.sectioned = True
            param.append(token)
        except errors.HeaderParseError:
            pass
        else:
            if not value:
                raise errors.HeaderParseError('Incomplete parameter')
            if value[0] == '*':
                param.append(ValueTerminal('*', 'extended-parameter-marker'))
                value = value[1:]
                param.extended = True
    if value[0] != '=':
        raise errors.HeaderParseError("Parameter not followed by '='")
    param.append(ValueTerminal('=', 'parameter-separator'))
    value = value[1:]
    leader = None
    if value:
        if value[0] in CFWS_LEADER:
            token, value = get_cfws(value)
            param.append(token)
        remainder = None
        appendto = param
        if param.extended and value and value[0] == '"':
            qstring, remainder = get_quoted_string(value)
            inner_value = qstring.stripped_value
            semi_valid = False
            if param.section_number == 0:
                if inner_value and inner_value[0] == "'":
                    semi_valid = True
        else:
            token, rest = get_attrtext(inner_value)
            if rest and rest[0] == "'":
                semi_valid = True
    else:
        try:
            token, rest = get_extended_attrtext(inner_value)
        except:
            pass
        else:
            if not rest:
                semi_valid = True
            if not param.extended or param.section_number > 0:
                if not value or value[0] != "'":
                    appendto.append(token)
                    if remainder is not None:
                        if value:
                            raise AssertionError(value)
                        value = remainder
                    return (
                     param, value)
                param.defects.append(errors.InvalidHeaderDefect('Apparent initial-extended-value but attribute was not marked as extended or was not initial section'))
            value or param.defects.append(errors.InvalidHeaderDefect('Missing required charset/lang delimiters'))
            appendto.append(token)
    if remainder is None:
        return (
         param, value)
    else:
        if token is not None:
            for t in token:
                if t.token_type == 'extended-attrtext':
                    break
                t.token_type == 'attrtext'
                appendto.append(t)
                param.charset = t.value

        if value[0] != "'":
            raise errors.HeaderParseError('Expected RFC2231 char/lang encoding delimiter, but found {!r}'.format(value))
        appendto.append(ValueTerminal("'", 'RFC2231-delimiter'))
        value = value[1:]
        if value and value[0] != "'":
            token, value = get_attrtext(value)
            appendto.append(token)
            param.lang = token.value
            if not value or value[0] != "'":
                raise errors.HeaderParseError('Expected RFC2231 char/lang encoding delimiter, but found {}'.format(value))
            appendto.append(ValueTerminal("'", 'RFC2231-delimiter'))
            value = value[1:]
        elif remainder is not None:
            v = Value()
            while value:
                if value[0] in WSP:
                    token, value = get_fws(value)
                else:
                    if value[0] == '"':
                        token = ValueTerminal('"', 'DQUOTE')
                        value = value[1:]
                    else:
                        token, value = get_qcontent(value)
                v.append(token)

            token = v
        else:
            token, value = get_value(value)
        appendto.append(token)
        if remainder is not None:
            if value:
                raise AssertionError(value)
            value = remainder
        return (
         param, value)


def parse_mime_parameters--- This code section failed: ---

 L.2557         0  LOAD_GLOBAL              MimeParameters
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'mime_parameters'
              6_0  COME_FROM           326  '326'

 L.2558         6  LOAD_FAST                'value'
             8_10  POP_JUMP_IF_FALSE   358  'to 358'

 L.2559        12  SETUP_FINALLY        40  'to 40'

 L.2560        14  LOAD_GLOBAL              get_parameter
               16  LOAD_FAST                'value'
               18  CALL_FUNCTION_1       1  ''
               20  UNPACK_SEQUENCE_2     2 
               22  STORE_FAST               'token'
               24  STORE_FAST               'value'

 L.2561        26  LOAD_FAST                'mime_parameters'
               28  LOAD_METHOD              append
               30  LOAD_FAST                'token'
               32  CALL_METHOD_1         1  ''
               34  POP_TOP          
               36  POP_BLOCK        
               38  JUMP_FORWARD        244  'to 244'
             40_0  COME_FROM_FINALLY    12  '12'

 L.2562        40  DUP_TOP          
               42  LOAD_GLOBAL              errors
               44  LOAD_ATTR                HeaderParseError
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE   242  'to 242'
               50  POP_TOP          
               52  STORE_FAST               'err'
               54  POP_TOP          
               56  SETUP_FINALLY       230  'to 230'

 L.2563        58  LOAD_CONST               None
               60  STORE_FAST               'leader'

 L.2564        62  LOAD_FAST                'value'
               64  LOAD_CONST               0
               66  BINARY_SUBSCR    
               68  LOAD_GLOBAL              CFWS_LEADER
               70  COMPARE_OP               in
               72  POP_JUMP_IF_FALSE    86  'to 86'

 L.2565        74  LOAD_GLOBAL              get_cfws
               76  LOAD_FAST                'value'
               78  CALL_FUNCTION_1       1  ''
               80  UNPACK_SEQUENCE_2     2 
               82  STORE_FAST               'leader'
               84  STORE_FAST               'value'
             86_0  COME_FROM            72  '72'

 L.2566        86  LOAD_FAST                'value'
               88  POP_JUMP_IF_TRUE    112  'to 112'

 L.2567        90  LOAD_FAST                'mime_parameters'
               92  LOAD_METHOD              append
               94  LOAD_FAST                'leader'
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          

 L.2568       100  LOAD_FAST                'mime_parameters'
              102  ROT_FOUR         
              104  POP_BLOCK        
              106  POP_EXCEPT       
              108  CALL_FINALLY        230  'to 230'
              110  RETURN_VALUE     
            112_0  COME_FROM            88  '88'

 L.2569       112  LOAD_FAST                'value'
              114  LOAD_CONST               0
              116  BINARY_SUBSCR    
              118  LOAD_STR                 ';'
              120  COMPARE_OP               ==
              122  POP_JUMP_IF_FALSE   162  'to 162'

 L.2570       124  LOAD_FAST                'leader'
              126  LOAD_CONST               None
              128  COMPARE_OP               is-not
              130  POP_JUMP_IF_FALSE   142  'to 142'

 L.2571       132  LOAD_FAST                'mime_parameters'
              134  LOAD_METHOD              append
              136  LOAD_FAST                'leader'
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          
            142_0  COME_FROM           130  '130'

 L.2572       142  LOAD_FAST                'mime_parameters'
              144  LOAD_ATTR                defects
              146  LOAD_METHOD              append
              148  LOAD_GLOBAL              errors
              150  LOAD_METHOD              InvalidHeaderDefect

 L.2573       152  LOAD_STR                 'parameter entry with no content'

 L.2572       154  CALL_METHOD_1         1  ''
              156  CALL_METHOD_1         1  ''
              158  POP_TOP          
              160  JUMP_FORWARD        226  'to 226'
            162_0  COME_FROM           122  '122'

 L.2575       162  LOAD_GLOBAL              get_invalid_parameter
              164  LOAD_FAST                'value'
              166  CALL_FUNCTION_1       1  ''
              168  UNPACK_SEQUENCE_2     2 
              170  STORE_FAST               'token'
              172  STORE_FAST               'value'

 L.2576       174  LOAD_FAST                'leader'
              176  POP_JUMP_IF_FALSE   192  'to 192'

 L.2577       178  LOAD_FAST                'leader'
              180  BUILD_LIST_1          1 
              182  LOAD_FAST                'token'
              184  LOAD_CONST               None
              186  LOAD_CONST               0
              188  BUILD_SLICE_2         2 
              190  STORE_SUBSCR     
            192_0  COME_FROM           176  '176'

 L.2578       192  LOAD_FAST                'mime_parameters'
              194  LOAD_METHOD              append
              196  LOAD_FAST                'token'
              198  CALL_METHOD_1         1  ''
              200  POP_TOP          

 L.2579       202  LOAD_FAST                'mime_parameters'
              204  LOAD_ATTR                defects
              206  LOAD_METHOD              append
              208  LOAD_GLOBAL              errors
              210  LOAD_METHOD              InvalidHeaderDefect

 L.2580       212  LOAD_STR                 'invalid parameter {!r}'
              214  LOAD_METHOD              format
              216  LOAD_FAST                'token'
              218  CALL_METHOD_1         1  ''

 L.2579       220  CALL_METHOD_1         1  ''
              222  CALL_METHOD_1         1  ''
              224  POP_TOP          
            226_0  COME_FROM           160  '160'
              226  POP_BLOCK        
              228  BEGIN_FINALLY    
            230_0  COME_FROM           108  '108'
            230_1  COME_FROM_FINALLY    56  '56'
              230  LOAD_CONST               None
              232  STORE_FAST               'err'
              234  DELETE_FAST              'err'
              236  END_FINALLY      
              238  POP_EXCEPT       
              240  JUMP_FORWARD        244  'to 244'
            242_0  COME_FROM            48  '48'
              242  END_FINALLY      
            244_0  COME_FROM           240  '240'
            244_1  COME_FROM            38  '38'

 L.2581       244  LOAD_FAST                'value'
          246_248  POP_JUMP_IF_FALSE   324  'to 324'
              250  LOAD_FAST                'value'
              252  LOAD_CONST               0
              254  BINARY_SUBSCR    
              256  LOAD_STR                 ';'
              258  COMPARE_OP               !=
          260_262  POP_JUMP_IF_FALSE   324  'to 324'

 L.2584       264  LOAD_FAST                'mime_parameters'
              266  LOAD_CONST               -1
              268  BINARY_SUBSCR    
              270  STORE_FAST               'param'

 L.2585       272  LOAD_STR                 'invalid-parameter'
              274  LOAD_FAST                'param'
              276  STORE_ATTR               token_type

 L.2586       278  LOAD_GLOBAL              get_invalid_parameter
              280  LOAD_FAST                'value'
              282  CALL_FUNCTION_1       1  ''
              284  UNPACK_SEQUENCE_2     2 
              286  STORE_FAST               'token'
              288  STORE_FAST               'value'

 L.2587       290  LOAD_FAST                'param'
              292  LOAD_METHOD              extend
              294  LOAD_FAST                'token'
              296  CALL_METHOD_1         1  ''
              298  POP_TOP          

 L.2588       300  LOAD_FAST                'mime_parameters'
              302  LOAD_ATTR                defects
              304  LOAD_METHOD              append
              306  LOAD_GLOBAL              errors
              308  LOAD_METHOD              InvalidHeaderDefect

 L.2589       310  LOAD_STR                 'parameter with invalid trailing text {!r}'
              312  LOAD_METHOD              format
              314  LOAD_FAST                'token'
              316  CALL_METHOD_1         1  ''

 L.2588       318  CALL_METHOD_1         1  ''
              320  CALL_METHOD_1         1  ''
              322  POP_TOP          
            324_0  COME_FROM           260  '260'
            324_1  COME_FROM           246  '246'

 L.2590       324  LOAD_FAST                'value'
              326  POP_JUMP_IF_FALSE     6  'to 6'

 L.2592       328  LOAD_FAST                'mime_parameters'
              330  LOAD_METHOD              append
              332  LOAD_GLOBAL              ValueTerminal
              334  LOAD_STR                 ';'
              336  LOAD_STR                 'parameter-separator'
              338  CALL_FUNCTION_2       2  ''
              340  CALL_METHOD_1         1  ''
              342  POP_TOP          

 L.2593       344  LOAD_FAST                'value'
              346  LOAD_CONST               1
              348  LOAD_CONST               None
              350  BUILD_SLICE_2         2 
              352  BINARY_SUBSCR    
              354  STORE_FAST               'value'
              356  JUMP_BACK             6  'to 6'
            358_0  COME_FROM             8  '8'

 L.2594       358  LOAD_FAST                'mime_parameters'
              360  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 104


def _find_mime_parameters(tokenlist, value):
    """Do our best to find the parameters in an invalid MIME header

    """
    if value:
        if value[0] != ';':
            if value[0] in PHRASE_ENDS:
                tokenlist.append(ValueTerminal(value[0], 'misplaced-special'))
                value = value[1:]
            else:
                token, value = get_phrase(value)
                tokenlist.append(token)
    else:
        return value or None
    tokenlist.append(ValueTerminal(';', 'parameter-separator'))
    tokenlist.append(parse_mime_parameters(value[1:]))


def parse_content_type_header(value):
    """ maintype "/" subtype *( ";" parameter )

    The maintype and substype are tokens.  Theoretically they could
    be checked against the official IANA list + x-token, but we
    don't do that.
    """
    ctype = ContentType()
    recover = False
    if not value:
        ctype.defects.append(errors.HeaderMissingRequiredValue('Missing content type specification'))
        return ctype
    try:
        token, value = get_token(value)
    except errors.HeaderParseError:
        ctype.defects.append(errors.InvalidHeaderDefect('Expected content maintype but found {!r}'.format(value)))
        _find_mime_parameters(ctype, value)
        return ctype
    else:
        ctype.append(token)
        if not value or value[0] != '/':
            ctype.defects.append(errors.InvalidHeaderDefect('Invalid content type'))
            if value:
                _find_mime_parameters(ctype, value)
            return ctype
        ctype.maintype = token.value.strip().lower()
        ctype.append(ValueTerminal('/', 'content-type-separator'))
        value = value[1:]
    try:
        token, value = get_token(value)
    except errors.HeaderParseError:
        ctype.defects.append(errors.InvalidHeaderDefect('Expected content subtype but found {!r}'.format(value)))
        _find_mime_parameters(ctype, value)
        return ctype
    else:
        ctype.append(token)
        ctype.subtype = token.value.strip().lower()
        if not value:
            return ctype
        if value[0] != ';':
            ctype.defects.append(errors.InvalidHeaderDefect('Only parameters are valid after content type, but found {!r}'.format(value)))
            del ctype.maintype
            del ctype.subtype
            _find_mime_parameters(ctype, value)
            return ctype
        ctype.append(ValueTerminal(';', 'parameter-separator'))
        ctype.append(parse_mime_parameters(value[1:]))
        return ctype


def parse_content_disposition_header(value):
    """ disposition-type *( ";" parameter )

    """
    disp_header = ContentDisposition()
    if not value:
        disp_header.defects.append(errors.HeaderMissingRequiredValue('Missing content disposition'))
        return disp_header
    try:
        token, value = get_token(value)
    except errors.HeaderParseError:
        disp_header.defects.append(errors.InvalidHeaderDefect('Expected content disposition but found {!r}'.format(value)))
        _find_mime_parameters(disp_header, value)
        return disp_header
    else:
        disp_header.append(token)
        disp_header.content_disposition = token.value.strip().lower()
        if not value:
            return disp_header
        if value[0] != ';':
            disp_header.defects.append(errors.InvalidHeaderDefect('Only parameters are valid after content disposition, but found {!r}'.format(value)))
            _find_mime_parameters(disp_header, value)
            return disp_header
        disp_header.append(ValueTerminal(';', 'parameter-separator'))
        disp_header.append(parse_mime_parameters(value[1:]))
        return disp_header


def parse_content_transfer_encoding_header(value):
    """ mechanism

    """
    cte_header = ContentTransferEncoding()
    if not value:
        cte_header.defects.append(errors.HeaderMissingRequiredValue('Missing content transfer encoding'))
        return cte_header
    try:
        token, value = get_token(value)
    except errors.HeaderParseError:
        cte_header.defects.append(errors.InvalidHeaderDefect('Expected content transfer encoding but found {!r}'.format(value)))
    else:
        cte_header.append(token)
        cte_header.cte = token.value.strip().lower()
    if not value:
        return cte_header
    else:
        while value:
            cte_header.defects.append(errors.InvalidHeaderDefect('Extra text after content transfer encoding'))
            if value[0] in PHRASE_ENDS:
                cte_header.append(ValueTerminal(value[0], 'misplaced-special'))
                value = value[1:]
            else:
                token, value = get_phrase(value)
                cte_header.append(token)

    return cte_header


def _steal_trailing_WSP_if_exists(lines):
    wsp = ''
    if lines:
        if lines[(-1)]:
            if lines[(-1)][(-1)] in WSP:
                wsp = lines[(-1)][(-1)]
                lines[-1] = lines[(-1)][:-1]
    return wsp


def _refold_parse_tree(parse_tree, *, policy):
    """Return string of contents of parse_tree folded according to RFC rules.

    """
    maxlen = policy.max_line_length or sys.maxsize
    encoding = 'utf-8' if policy.utf8 else 'us-ascii'
    lines = ['']
    last_ew = None
    wrap_as_ew_blocked = 0
    want_encoding = False
    end_ew_not_allowed = Terminal('', 'wrap_as_ew_blocked')
    parts = list(parse_tree)
    while parts:
        part = parts.pop(0)
        if part is end_ew_not_allowed:
            wrap_as_ew_blocked -= 1

    tstr = str(part)
    if part.token_type == 'ptext':
        if set(tstr) & SPECIALS:
            want_encoding = True
    try:
        tstr.encode(encoding)
        charset = encoding
    except UnicodeEncodeError:
        if any((isinstance(x, errors.UndecodableBytesDefect) for x in part.all_defects)):
            charset = 'unknown-8bit'
        else:
            charset = 'utf-8'
        want_encoding = True
    else:
        if part.token_type == 'mime-parameters':
            _fold_mime_parameters(part, lines, maxlen, encoding)
        elif want_encoding:
            if not (wrap_as_ew_blocked or part.as_ew_allowed):
                want_encoding = False
                last_ew = None
                if part.syntactic_break:
                    encoded_part = part.fold(policy=policy)[:-len(policy.linesep)]
                    if policy.linesep not in encoded_part:
                        if len(encoded_part) > maxlen - len(lines[(-1)]):
                            newline = _steal_trailing_WSP_if_exists(lines)
                            lines.append(newline)
                        lines[(-1)] += encoded_part
                if not hasattr(part, 'encode'):
                    parts = list(part) + parts
            else:
                last_ew = _fold_as_ew(tstr, lines, maxlen, last_ew, part.ew_combine_allowed, charset)
            want_encoding = False
        elif len(tstr) <= maxlen - len(lines[(-1)]):
            lines[(-1)] += tstr
        else:
            if part.syntactic_break:
                if len(tstr) + 1 <= maxlen:
                    newline = _steal_trailing_WSP_if_exists(lines)
                    if newline or part.startswith_fws():
                        lines.append(newline + tstr)
                        last_ew = None
            if not hasattr(part, 'encode'):
                newparts = list(part)
                if not part.as_ew_allowed:
                    wrap_as_ew_blocked += 1
                    newparts.append(end_ew_not_allowed)
                parts = newparts + parts
            elif part.as_ew_allowed:
                wrap_as_ew_blocked or parts.insert(0, part)
                want_encoding = True
            else:
                newline = _steal_trailing_WSP_if_exists(lines)
                if newline or part.startswith_fws():
                    lines.append(newline + tstr)
                else:
                    lines[(-1)] += tstr
                return policy.linesep.join(lines) + policy.linesep


def _fold_as_ew(to_encode, lines, maxlen, last_ew, ew_combine_allowed, charset):
    """Fold string to_encode into lines as encoded word, combining if allowed.
    Return the new value for last_ew, or None if ew_combine_allowed is False.

    If there is already an encoded word in the last line of lines (indicated by
    a non-None value for last_ew) and ew_combine_allowed is true, decode the
    existing ew, combine it with to_encode, and re-encode.  Otherwise, encode
    to_encode.  In either case, split to_encode as necessary so that the
    encoded segments fit within maxlen.

    """
    if last_ew is not None:
        if ew_combine_allowed:
            to_encode = str(get_unstructured(lines[(-1)][last_ew:] + to_encode))
            lines[-1] = lines[(-1)][:last_ew]
    else:
        if to_encode[0] in WSP:
            leading_wsp = to_encode[0]
            to_encode = to_encode[1:]
            if len(lines[(-1)]) == maxlen:
                lines.append(_steal_trailing_WSP_if_exists(lines))
            lines[(-1)] += leading_wsp
        trailing_wsp = ''
        if to_encode[(-1)] in WSP:
            trailing_wsp = to_encode[(-1)]
            to_encode = to_encode[:-1]
        new_last_ew = len(lines[(-1)]) if last_ew is None else last_ew
        encode_as = 'utf-8' if charset == 'us-ascii' else charset
        chrome_len = len(encode_as) + 7
        if chrome_len + 1 >= maxlen:
            raise errors.HeaderParseError('max_line_length is too small to fit an encoded word')
        while to_encode:
            remaining_space = maxlen - len(lines[(-1)])
            text_space = remaining_space - chrome_len
            if text_space <= 0:
                lines.append(' ')
            else:
                to_encode_word = to_encode[:text_space]
                encoded_word = _ew.encode(to_encode_word, charset=encode_as)
                excess = len(encoded_word) - remaining_space
                if excess > 0:
                    to_encode_word = to_encode_word[:-1]
                    encoded_word = _ew.encode(to_encode_word, charset=encode_as)
                    excess = len(encoded_word) - remaining_space
                else:
                    lines[(-1)] += encoded_word
                    to_encode = to_encode[len(to_encode_word):]
                    if to_encode:
                        lines.append(' ')
                        new_last_ew = len(lines[(-1)])

    lines[(-1)] += trailing_wsp
    if ew_combine_allowed:
        return new_last_ew


def _fold_mime_parameters--- This code section failed: ---

 L.2936         0  LOAD_FAST                'part'
                2  LOAD_ATTR                params
                4  GET_ITER         
              6_0  COME_FROM           280  '280'
              6_8  FOR_ITER            482  'to 482'
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'name'
               14  STORE_FAST               'value'

 L.2942        16  LOAD_FAST                'lines'
               18  LOAD_CONST               -1
               20  BINARY_SUBSCR    
               22  LOAD_METHOD              rstrip
               24  CALL_METHOD_0         0  ''
               26  LOAD_METHOD              endswith
               28  LOAD_STR                 ';'
               30  CALL_METHOD_1         1  ''
               32  POP_JUMP_IF_TRUE     50  'to 50'

 L.2943        34  LOAD_FAST                'lines'
               36  LOAD_CONST               -1
               38  DUP_TOP_TWO      
               40  BINARY_SUBSCR    
               42  LOAD_STR                 ';'
               44  INPLACE_ADD      
               46  ROT_THREE        
               48  STORE_SUBSCR     
             50_0  COME_FROM            32  '32'

 L.2944        50  LOAD_FAST                'encoding'
               52  STORE_FAST               'charset'

 L.2945        54  LOAD_STR                 'strict'
               56  STORE_FAST               'error_handler'

 L.2946        58  SETUP_FINALLY        78  'to 78'

 L.2947        60  LOAD_FAST                'value'
               62  LOAD_METHOD              encode
               64  LOAD_FAST                'encoding'
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          

 L.2948        70  LOAD_CONST               False
               72  STORE_FAST               'encoding_required'
               74  POP_BLOCK        
               76  JUMP_FORWARD        126  'to 126'
             78_0  COME_FROM_FINALLY    58  '58'

 L.2949        78  DUP_TOP          
               80  LOAD_GLOBAL              UnicodeEncodeError
               82  COMPARE_OP               exception-match
               84  POP_JUMP_IF_FALSE   124  'to 124'
               86  POP_TOP          
               88  POP_TOP          
               90  POP_TOP          

 L.2950        92  LOAD_CONST               True
               94  STORE_FAST               'encoding_required'

 L.2951        96  LOAD_GLOBAL              utils
               98  LOAD_METHOD              _has_surrogates
              100  LOAD_FAST                'value'
              102  CALL_METHOD_1         1  ''
              104  POP_JUMP_IF_FALSE   116  'to 116'

 L.2952       106  LOAD_STR                 'unknown-8bit'
              108  STORE_FAST               'charset'

 L.2953       110  LOAD_STR                 'surrogateescape'
              112  STORE_FAST               'error_handler'
              114  JUMP_FORWARD        120  'to 120'
            116_0  COME_FROM           104  '104'

 L.2955       116  LOAD_STR                 'utf-8'
              118  STORE_FAST               'charset'
            120_0  COME_FROM           114  '114'
              120  POP_EXCEPT       
              122  JUMP_FORWARD        126  'to 126'
            124_0  COME_FROM            84  '84'
              124  END_FINALLY      
            126_0  COME_FROM           122  '122'
            126_1  COME_FROM            76  '76'

 L.2956       126  LOAD_FAST                'encoding_required'
              128  POP_JUMP_IF_FALSE   164  'to 164'

 L.2957       130  LOAD_GLOBAL              urllib
              132  LOAD_ATTR                parse
              134  LOAD_ATTR                quote

 L.2958       136  LOAD_FAST                'value'

 L.2958       138  LOAD_STR                 ''

 L.2958       140  LOAD_FAST                'error_handler'

 L.2957       142  LOAD_CONST               ('safe', 'errors')
              144  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              146  STORE_FAST               'encoded_value'

 L.2959       148  LOAD_STR                 "{}*={}''{}"
              150  LOAD_METHOD              format
              152  LOAD_FAST                'name'
              154  LOAD_FAST                'charset'
              156  LOAD_FAST                'encoded_value'
              158  CALL_METHOD_3         3  ''
              160  STORE_FAST               'tstr'
              162  JUMP_FORWARD        180  'to 180'
            164_0  COME_FROM           128  '128'

 L.2961       164  LOAD_STR                 '{}={}'
              166  LOAD_METHOD              format
              168  LOAD_FAST                'name'
              170  LOAD_GLOBAL              quote_string
              172  LOAD_FAST                'value'
              174  CALL_FUNCTION_1       1  ''
              176  CALL_METHOD_2         2  ''
              178  STORE_FAST               'tstr'
            180_0  COME_FROM           162  '162'

 L.2962       180  LOAD_GLOBAL              len
              182  LOAD_FAST                'lines'
              184  LOAD_CONST               -1
              186  BINARY_SUBSCR    
              188  CALL_FUNCTION_1       1  ''
              190  LOAD_GLOBAL              len
              192  LOAD_FAST                'tstr'
              194  CALL_FUNCTION_1       1  ''
              196  BINARY_ADD       
              198  LOAD_CONST               1
              200  BINARY_ADD       
              202  LOAD_FAST                'maxlen'
              204  COMPARE_OP               <
              206  POP_JUMP_IF_FALSE   232  'to 232'

 L.2963       208  LOAD_FAST                'lines'
              210  LOAD_CONST               -1
              212  BINARY_SUBSCR    
              214  LOAD_STR                 ' '
              216  BINARY_ADD       
              218  LOAD_FAST                'tstr'
              220  BINARY_ADD       
              222  LOAD_FAST                'lines'
              224  LOAD_CONST               -1
              226  STORE_SUBSCR     

 L.2964       228  JUMP_BACK             6  'to 6'
              230  JUMP_FORWARD        266  'to 266'
            232_0  COME_FROM           206  '206'

 L.2965       232  LOAD_GLOBAL              len
              234  LOAD_FAST                'tstr'
              236  CALL_FUNCTION_1       1  ''
              238  LOAD_CONST               2
              240  BINARY_ADD       
              242  LOAD_FAST                'maxlen'
              244  COMPARE_OP               <=
          246_248  POP_JUMP_IF_FALSE   266  'to 266'

 L.2966       250  LOAD_FAST                'lines'
              252  LOAD_METHOD              append
              254  LOAD_STR                 ' '
              256  LOAD_FAST                'tstr'
              258  BINARY_ADD       
              260  CALL_METHOD_1         1  ''
              262  POP_TOP          

 L.2967       264  JUMP_BACK             6  'to 6'
            266_0  COME_FROM           246  '246'
            266_1  COME_FROM           230  '230'

 L.2970       266  LOAD_CONST               0
              268  STORE_FAST               'section'

 L.2971       270  LOAD_FAST                'charset'
              272  LOAD_STR                 "''"
              274  BINARY_ADD       
              276  STORE_FAST               'extra_chrome'
            278_0  COME_FROM           456  '456'

 L.2972       278  LOAD_FAST                'value'
              280  POP_JUMP_IF_FALSE     6  'to 6'

 L.2973       282  LOAD_GLOBAL              len
              284  LOAD_FAST                'name'
              286  CALL_FUNCTION_1       1  ''
              288  LOAD_GLOBAL              len
              290  LOAD_GLOBAL              str
              292  LOAD_FAST                'section'
              294  CALL_FUNCTION_1       1  ''
              296  CALL_FUNCTION_1       1  ''
              298  BINARY_ADD       
              300  LOAD_CONST               3
              302  BINARY_ADD       
              304  LOAD_GLOBAL              len
              306  LOAD_FAST                'extra_chrome'
              308  CALL_FUNCTION_1       1  ''
              310  BINARY_ADD       
              312  STORE_FAST               'chrome_len'

 L.2974       314  LOAD_FAST                'maxlen'
              316  LOAD_FAST                'chrome_len'
              318  LOAD_CONST               3
              320  BINARY_ADD       
              322  COMPARE_OP               <=
          324_326  POP_JUMP_IF_FALSE   332  'to 332'

 L.2979       328  LOAD_CONST               78
              330  STORE_FAST               'maxlen'
            332_0  COME_FROM           324  '324'

 L.2980       332  LOAD_FAST                'maxlen'
              334  LOAD_FAST                'chrome_len'
              336  BINARY_SUBTRACT  
              338  LOAD_CONST               2
              340  BINARY_SUBTRACT  
              342  DUP_TOP          
              344  STORE_FAST               'splitpoint'
              346  STORE_FAST               'maxchars'

 L.2982       348  LOAD_FAST                'value'
              350  LOAD_CONST               None
              352  LOAD_FAST                'splitpoint'
              354  BUILD_SLICE_2         2 
              356  BINARY_SUBSCR    
              358  STORE_FAST               'partial'

 L.2983       360  LOAD_GLOBAL              urllib
              362  LOAD_ATTR                parse
              364  LOAD_ATTR                quote

 L.2984       366  LOAD_FAST                'partial'

 L.2984       368  LOAD_STR                 ''

 L.2984       370  LOAD_FAST                'error_handler'

 L.2983       372  LOAD_CONST               ('safe', 'errors')
              374  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              376  STORE_FAST               'encoded_value'

 L.2985       378  LOAD_GLOBAL              len
              380  LOAD_FAST                'encoded_value'
              382  CALL_FUNCTION_1       1  ''
              384  LOAD_FAST                'maxchars'
              386  COMPARE_OP               <=
          388_390  POP_JUMP_IF_FALSE   396  'to 396'

 L.2986   392_394  BREAK_LOOP          408  'to 408'
            396_0  COME_FROM           388  '388'

 L.2987       396  LOAD_FAST                'splitpoint'
              398  LOAD_CONST               1
              400  INPLACE_SUBTRACT 
              402  STORE_FAST               'splitpoint'
          404_406  JUMP_BACK           348  'to 348'

 L.2988       408  LOAD_FAST                'lines'
              410  LOAD_METHOD              append
              412  LOAD_STR                 ' {}*{}*={}{}'
              414  LOAD_METHOD              format

 L.2989       416  LOAD_FAST                'name'

 L.2989       418  LOAD_FAST                'section'

 L.2989       420  LOAD_FAST                'extra_chrome'

 L.2989       422  LOAD_FAST                'encoded_value'

 L.2988       424  CALL_METHOD_4         4  ''
              426  CALL_METHOD_1         1  ''
              428  POP_TOP          

 L.2990       430  LOAD_STR                 ''
              432  STORE_FAST               'extra_chrome'

 L.2991       434  LOAD_FAST                'section'
              436  LOAD_CONST               1
              438  INPLACE_ADD      
              440  STORE_FAST               'section'

 L.2992       442  LOAD_FAST                'value'
              444  LOAD_FAST                'splitpoint'
              446  LOAD_CONST               None
              448  BUILD_SLICE_2         2 
              450  BINARY_SUBSCR    
              452  STORE_FAST               'value'

 L.2993       454  LOAD_FAST                'value'
          456_458  POP_JUMP_IF_FALSE   278  'to 278'

 L.2994       460  LOAD_FAST                'lines'
              462  LOAD_CONST               -1
              464  DUP_TOP_TWO      
              466  BINARY_SUBSCR    
              468  LOAD_STR                 ';'
              470  INPLACE_ADD      
              472  ROT_THREE        
              474  STORE_SUBSCR     
          476_478  JUMP_BACK           278  'to 278'
              480  JUMP_BACK             6  'to 6'

Parse error at or near `JUMP_FORWARD' instruction at offset 230