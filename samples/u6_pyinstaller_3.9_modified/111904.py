# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: email\headerregistry.py
"""Representing and manipulating email headers via custom objects.

This module provides an implementation of the HeaderRegistry API.
The implementation is designed to flexibly follow RFC5322 rules.

Eventually HeaderRegistry will be a public API, but it isn't yet,
and will probably change some before that happens.

"""
from types import MappingProxyType
from email import utils
from email import errors
from email import _header_value_parser as parser

class Address:

    def __init__--- This code section failed: ---

 L.  35         0  LOAD_STR                 ''
                2  LOAD_METHOD              join
                4  LOAD_GLOBAL              filter
                6  LOAD_CONST               None
                8  LOAD_FAST                'display_name'
               10  LOAD_FAST                'username'
               12  LOAD_FAST                'domain'
               14  LOAD_FAST                'addr_spec'
               16  BUILD_TUPLE_4         4 
               18  CALL_FUNCTION_2       2  ''
               20  CALL_METHOD_1         1  ''
               22  STORE_FAST               'inputs'

 L.  36        24  LOAD_STR                 '\r'
               26  LOAD_FAST                'inputs'
               28  <118>                 0  ''
               30  POP_JUMP_IF_TRUE     40  'to 40'
               32  LOAD_STR                 '\n'
               34  LOAD_FAST                'inputs'
               36  <118>                 0  ''
               38  POP_JUMP_IF_FALSE    48  'to 48'
             40_0  COME_FROM            30  '30'

 L.  37        40  LOAD_GLOBAL              ValueError
               42  LOAD_STR                 'invalid arguments; address parts cannot contain CR or LF'
               44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            38  '38'

 L.  43        48  LOAD_FAST                'addr_spec'
               50  LOAD_CONST               None
               52  <117>                 1  ''
               54  POP_JUMP_IF_FALSE   134  'to 134'

 L.  44        56  LOAD_FAST                'username'
               58  POP_JUMP_IF_TRUE     64  'to 64'
               60  LOAD_FAST                'domain'
               62  POP_JUMP_IF_FALSE    72  'to 72'
             64_0  COME_FROM            58  '58'

 L.  45        64  LOAD_GLOBAL              TypeError
               66  LOAD_STR                 'addrspec specified when username and/or domain also specified'
               68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            62  '62'

 L.  47        72  LOAD_GLOBAL              parser
               74  LOAD_METHOD              get_addr_spec
               76  LOAD_FAST                'addr_spec'
               78  CALL_METHOD_1         1  ''
               80  UNPACK_SEQUENCE_2     2 
               82  STORE_FAST               'a_s'
               84  STORE_FAST               'rest'

 L.  48        86  LOAD_FAST                'rest'
               88  POP_JUMP_IF_FALSE   106  'to 106'

 L.  49        90  LOAD_GLOBAL              ValueError
               92  LOAD_STR                 "Invalid addr_spec; only '{}' could be parsed from '{}'"
               94  LOAD_METHOD              format

 L.  51        96  LOAD_FAST                'a_s'
               98  LOAD_FAST                'addr_spec'

 L.  49       100  CALL_METHOD_2         2  ''
              102  CALL_FUNCTION_1       1  ''
              104  RAISE_VARARGS_1       1  'exception instance'
            106_0  COME_FROM            88  '88'

 L.  52       106  LOAD_FAST                'a_s'
              108  LOAD_ATTR                all_defects
              110  POP_JUMP_IF_FALSE   122  'to 122'

 L.  53       112  LOAD_FAST                'a_s'
              114  LOAD_ATTR                all_defects
              116  LOAD_CONST               0
              118  BINARY_SUBSCR    
              120  RAISE_VARARGS_1       1  'exception instance'
            122_0  COME_FROM           110  '110'

 L.  54       122  LOAD_FAST                'a_s'
              124  LOAD_ATTR                local_part
              126  STORE_FAST               'username'

 L.  55       128  LOAD_FAST                'a_s'
              130  LOAD_ATTR                domain
              132  STORE_FAST               'domain'
            134_0  COME_FROM            54  '54'

 L.  56       134  LOAD_FAST                'display_name'
              136  LOAD_FAST                'self'
              138  STORE_ATTR               _display_name

 L.  57       140  LOAD_FAST                'username'
              142  LOAD_FAST                'self'
              144  STORE_ATTR               _username

 L.  58       146  LOAD_FAST                'domain'
              148  LOAD_FAST                'self'
              150  STORE_ATTR               _domain

Parse error at or near `<118>' instruction at offset 28

    @property
    def display_name(self):
        return self._display_name

    @property
    def username(self):
        return self._username

    @property
    def domain(self):
        return self._domain

    @property
    def addr_spec(self):
        """The addr_spec (username@domain) portion of the address, quoted
        according to RFC 5322 rules, but with no Content Transfer Encoding.
        """
        lp = self.username
        if not parser.DOT_ATOM_ENDS.isdisjointlp:
            lp = parser.quote_stringlp
        else:
            if self.domain:
                return lp + '@' + self.domain
            return lp or '<>'
        return lp

    def __repr__(self):
        return '{}(display_name={!r}, username={!r}, domain={!r})'.format(self.__class__.__name__, self.display_name, self.username, self.domain)

    def __str__(self):
        disp = self.display_name
        if not parser.SPECIALS.isdisjointdisp:
            disp = parser.quote_stringdisp
        if disp:
            addr_spec = '' if self.addr_spec == '<>' else self.addr_spec
            return '{} <{}>'.formatdispaddr_spec
        return self.addr_spec

    def __eq__(self, other):
        if not isinstance(other, Address):
            return NotImplemented
        return self.display_name == other.display_name and self.username == other.username and self.domain == other.domain


class Group:

    def __init__(self, display_name=None, addresses=None):
        """Create an object representing an address group.

        An address group consists of a display_name followed by colon and a
        list of addresses (see Address) terminated by a semi-colon.  The Group
        is created by specifying a display_name and a possibly empty list of
        Address objects.  A Group can also be used to represent a single
        address that is not in a group, which is convenient when manipulating
        lists that are a combination of Groups and individual Addresses.  In
        this case the display_name should be set to None.  In particular, the
        string representation of a Group whose display_name is None is the same
        as the Address object, if there is one and only one Address object in
        the addresses list.

        """
        self._display_name = display_name
        self._addresses = tuple(addresses) if addresses else tuple()

    @property
    def display_name(self):
        return self._display_name

    @property
    def addresses(self):
        return self._addresses

    def __repr__(self):
        return '{}(display_name={!r}, addresses={!r}'.format(self.__class__.__name__, self.display_name, self.addresses)

    def __str__--- This code section failed: ---

 L. 142         0  LOAD_FAST                'self'
                2  LOAD_ATTR                display_name
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    38  'to 38'
               10  LOAD_GLOBAL              len
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                addresses
               16  CALL_FUNCTION_1       1  ''
               18  LOAD_CONST               1
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_FALSE    38  'to 38'

 L. 143        24  LOAD_GLOBAL              str
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                addresses
               30  LOAD_CONST               0
               32  BINARY_SUBSCR    
               34  CALL_FUNCTION_1       1  ''
               36  RETURN_VALUE     
             38_0  COME_FROM            22  '22'
             38_1  COME_FROM             8  '8'

 L. 144        38  LOAD_FAST                'self'
               40  LOAD_ATTR                display_name
               42  STORE_FAST               'disp'

 L. 145        44  LOAD_FAST                'disp'
               46  LOAD_CONST               None
               48  <117>                 1  ''
               50  POP_JUMP_IF_FALSE    74  'to 74'
               52  LOAD_GLOBAL              parser
               54  LOAD_ATTR                SPECIALS
               56  LOAD_METHOD              isdisjoint
               58  LOAD_FAST                'disp'
               60  CALL_METHOD_1         1  ''
               62  POP_JUMP_IF_TRUE     74  'to 74'

 L. 146        64  LOAD_GLOBAL              parser
               66  LOAD_METHOD              quote_string
               68  LOAD_FAST                'disp'
               70  CALL_METHOD_1         1  ''
               72  STORE_FAST               'disp'
             74_0  COME_FROM            62  '62'
             74_1  COME_FROM            50  '50'

 L. 147        74  LOAD_STR                 ', '
               76  LOAD_METHOD              join
               78  LOAD_GENEXPR             '<code_object <genexpr>>'
               80  LOAD_STR                 'Group.__str__.<locals>.<genexpr>'
               82  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                addresses
               88  GET_ITER         
               90  CALL_FUNCTION_1       1  ''
               92  CALL_METHOD_1         1  ''
               94  STORE_FAST               'adrstr'

 L. 148        96  LOAD_FAST                'adrstr'
               98  POP_JUMP_IF_FALSE   108  'to 108'
              100  LOAD_STR                 ' '
              102  LOAD_FAST                'adrstr'
              104  BINARY_ADD       
              106  JUMP_FORWARD        110  'to 110'
            108_0  COME_FROM            98  '98'
              108  LOAD_FAST                'adrstr'
            110_0  COME_FROM           106  '106'
              110  STORE_FAST               'adrstr'

 L. 149       112  LOAD_STR                 '{}:{};'
              114  LOAD_METHOD              format
              116  LOAD_FAST                'disp'
              118  LOAD_FAST                'adrstr'
              120  CALL_METHOD_2         2  ''
              122  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __eq__(self, other):
        if not isinstance(other, Group):
            return NotImplemented
        return self.display_name == other.display_name and self.addresses == other.addresses


class BaseHeader(str):
    __doc__ = "Base class for message headers.\n\n    Implements generic behavior and provides tools for subclasses.\n\n    A subclass must define a classmethod named 'parse' that takes an unfolded\n    value string and a dictionary as its arguments.  The dictionary will\n    contain one key, 'defects', initialized to an empty list.  After the call\n    the dictionary must contain two additional keys: parse_tree, set to the\n    parse tree obtained from parsing the header, and 'decoded', set to the\n    string value of the idealized representation of the data from the value.\n    (That is, encoded words are decoded, and values that have canonical\n    representations are so represented.)\n\n    The defects key is intended to collect parsing defects, which the message\n    parser will subsequently dispose of as appropriate.  The parser should not,\n    insofar as practical, raise any errors.  Defects should be added to the\n    list instead.  The standard header parsers register defects for RFC\n    compliance issues, for obsolete RFC syntax, and for unrecoverable parsing\n    errors.\n\n    The parse method may add additional keys to the dictionary.  In this case\n    the subclass must define an 'init' method, which will be passed the\n    dictionary as its keyword arguments.  The method should use (usually by\n    setting them as the value of similarly named attributes) and remove all the\n    extra keys added by its parse method, and then use super to call its parent\n    class with the remaining arguments and keywords.\n\n    The subclass should also make sure that a 'max_count' attribute is defined\n    that is either None or 1. XXX: need to better define this API.\n\n    "

    def __new__--- This code section failed: ---

 L. 195         0  LOAD_STR                 'defects'
                2  BUILD_LIST_0          0 
                4  BUILD_MAP_1           1 
                6  STORE_FAST               'kwds'

 L. 196         8  LOAD_FAST                'cls'
               10  LOAD_METHOD              parse
               12  LOAD_FAST                'value'
               14  LOAD_FAST                'kwds'
               16  CALL_METHOD_2         2  ''
               18  POP_TOP          

 L. 197        20  LOAD_GLOBAL              utils
               22  LOAD_METHOD              _has_surrogates
               24  LOAD_FAST                'kwds'
               26  LOAD_STR                 'decoded'
               28  BINARY_SUBSCR    
               30  CALL_METHOD_1         1  ''
               32  POP_JUMP_IF_FALSE    52  'to 52'

 L. 198        34  LOAD_GLOBAL              utils
               36  LOAD_METHOD              _sanitize
               38  LOAD_FAST                'kwds'
               40  LOAD_STR                 'decoded'
               42  BINARY_SUBSCR    
               44  CALL_METHOD_1         1  ''
               46  LOAD_FAST                'kwds'
               48  LOAD_STR                 'decoded'
               50  STORE_SUBSCR     
             52_0  COME_FROM            32  '32'

 L. 199        52  LOAD_GLOBAL              str
               54  LOAD_METHOD              __new__
               56  LOAD_FAST                'cls'
               58  LOAD_FAST                'kwds'
               60  LOAD_STR                 'decoded'
               62  BINARY_SUBSCR    
               64  CALL_METHOD_2         2  ''
               66  STORE_FAST               'self'

 L. 200        68  LOAD_FAST                'kwds'
               70  LOAD_STR                 'decoded'
               72  DELETE_SUBSCR    

 L. 201        74  LOAD_FAST                'self'
               76  LOAD_ATTR                init
               78  LOAD_FAST                'name'
               80  BUILD_TUPLE_1         1 
               82  BUILD_MAP_0           0 
               84  LOAD_FAST                'kwds'
               86  <164>                 1  ''
               88  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               90  POP_TOP          

 L. 202        92  LOAD_FAST                'self'
               94  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 86

    def init(self, name, *, parse_tree, defects):
        self._name = name
        self._parse_tree = parse_tree
        self._defects = defects

    @property
    def name(self):
        return self._name

    @property
    def defects(self):
        return tuple(self._defects)

    def __reduce__(self):
        return (
         _reconstruct_header,
         (
          self.__class__.__name__,
          self.__class__.__bases__,
          str(self)),
         self.__dict__)

    @classmethod
    def _reconstruct(cls, value):
        return str.__new__clsvalue

    def fold(self, *, policy):
        """Fold header according to policy.

        The parsed representation of the header is folded according to
        RFC5322 rules, as modified by the policy.  If the parse tree
        contains surrogateescaped bytes, the bytes are CTE encoded using
        the charset 'unknown-8bit".

        Any non-ASCII characters in the parse tree are CTE encoded using
        charset utf-8. XXX: make this a policy setting.

        The returned value is an ASCII-only string possibly containing linesep
        characters, and ending with a linesep character.  The string includes
        the header name and the ': ' separator.

        """
        header = parser.Header[
         parser.HeaderLabel[
          parser.ValueTerminalself.name'header-name',
          parser.ValueTerminal':''header-sep']]
        if self._parse_tree:
            header.appendparser.CFWSList[parser.WhiteSpaceTerminal' ''fws']
        header.appendself._parse_tree
        return header.fold(policy=policy)


def _reconstruct_header(cls_name, bases, value):
    return type(cls_name, bases, {})._reconstructvalue


class UnstructuredHeader:
    max_count = None
    value_parser = staticmethod(parser.get_unstructured)

    @classmethod
    def parse(cls, value, kwds):
        kwds['parse_tree'] = cls.value_parservalue
        kwds['decoded'] = str(kwds['parse_tree'])


class UniqueUnstructuredHeader(UnstructuredHeader):
    max_count = 1


class DateHeader:
    __doc__ = "Header whose value consists of a single timestamp.\n\n    Provides an additional attribute, datetime, which is either an aware\n    datetime using a timezone, or a naive datetime if the timezone\n    in the input string is -0000.  Also accepts a datetime as input.\n    The 'value' attribute is the normalized form of the timestamp,\n    which means it is the output of format_datetime on the datetime.\n    "
    max_count = None
    value_parser = staticmethod(parser.get_unstructured)

    @classmethod
    def parse(cls, value, kwds):
        if not value:
            kwds['defects'].appenderrors.HeaderMissingRequiredValue()
            kwds['datetime'] = None
            kwds['decoded'] = ''
            kwds['parse_tree'] = parser.TokenList()
            return
        if isinstance(value, str):
            value = utils.parsedate_to_datetimevalue
        kwds['datetime'] = value
        kwds['decoded'] = utils.format_datetimekwds['datetime']
        kwds['parse_tree'] = cls.value_parserkwds['decoded']

    def init--- This code section failed: ---

 L. 311         0  LOAD_FAST                'kw'
                2  LOAD_METHOD              pop
                4  LOAD_STR                 'datetime'
                6  CALL_METHOD_1         1  ''
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _datetime

 L. 312        12  LOAD_GLOBAL              super
               14  CALL_FUNCTION_0       0  ''
               16  LOAD_ATTR                init
               18  LOAD_FAST                'args'
               20  BUILD_MAP_0           0 
               22  LOAD_FAST                'kw'
               24  <164>                 1  ''
               26  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               28  POP_TOP          

Parse error at or near `<164>' instruction at offset 24

    @property
    def datetime(self):
        return self._datetime


class UniqueDateHeader(DateHeader):
    max_count = 1


class AddressHeader:
    max_count = None

    @staticmethod
    def value_parser--- This code section failed: ---

 L. 330         0  LOAD_GLOBAL              parser
                2  LOAD_METHOD              get_address_list
                4  LOAD_FAST                'value'
                6  CALL_METHOD_1         1  ''
                8  UNPACK_SEQUENCE_2     2 
               10  STORE_FAST               'address_list'
               12  STORE_FAST               'value'

 L. 331        14  LOAD_FAST                'value'
               16  POP_JUMP_IF_FALSE    26  'to 26'
               18  <74>             
               20  LOAD_STR                 'this should not happen'
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            16  '16'

 L. 332        26  LOAD_FAST                'address_list'
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 18

    @classmethod
    def parse--- This code section failed: ---

 L. 336         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'value'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    86  'to 86'

 L. 339        10  LOAD_FAST                'cls'
               12  LOAD_METHOD              value_parser
               14  LOAD_FAST                'value'
               16  CALL_METHOD_1         1  ''
               18  DUP_TOP          
               20  LOAD_FAST                'kwds'
               22  LOAD_STR                 'parse_tree'
               24  STORE_SUBSCR     
               26  STORE_FAST               'address_list'

 L. 340        28  BUILD_LIST_0          0 
               30  STORE_FAST               'groups'

 L. 341        32  LOAD_FAST                'address_list'
               34  LOAD_ATTR                addresses
               36  GET_ITER         
               38  FOR_ITER             74  'to 74'
               40  STORE_FAST               'addr'

 L. 342        42  LOAD_FAST                'groups'
               44  LOAD_METHOD              append
               46  LOAD_GLOBAL              Group
               48  LOAD_FAST                'addr'
               50  LOAD_ATTR                display_name

 L. 343        52  LOAD_LISTCOMP            '<code_object <listcomp>>'
               54  LOAD_STR                 'AddressHeader.parse.<locals>.<listcomp>'
               56  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 346        58  LOAD_FAST                'addr'
               60  LOAD_ATTR                all_mailboxes

 L. 343        62  GET_ITER         
               64  CALL_FUNCTION_1       1  ''

 L. 342        66  CALL_FUNCTION_2       2  ''
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          
               72  JUMP_BACK            38  'to 38'

 L. 347        74  LOAD_GLOBAL              list
               76  LOAD_FAST                'address_list'
               78  LOAD_ATTR                all_defects
               80  CALL_FUNCTION_1       1  ''
               82  STORE_FAST               'defects'
               84  JUMP_FORWARD        120  'to 120'
             86_0  COME_FROM             8  '8'

 L. 350        86  LOAD_GLOBAL              hasattr
               88  LOAD_FAST                'value'
               90  LOAD_STR                 '__iter__'
               92  CALL_FUNCTION_2       2  ''
               94  POP_JUMP_IF_TRUE    102  'to 102'

 L. 351        96  LOAD_FAST                'value'
               98  BUILD_LIST_1          1 
              100  STORE_FAST               'value'
            102_0  COME_FROM            94  '94'

 L. 352       102  LOAD_LISTCOMP            '<code_object <listcomp>>'
              104  LOAD_STR                 'AddressHeader.parse.<locals>.<listcomp>'
              106  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 354       108  LOAD_FAST                'value'

 L. 352       110  GET_ITER         
              112  CALL_FUNCTION_1       1  ''
              114  STORE_FAST               'groups'

 L. 355       116  BUILD_LIST_0          0 
              118  STORE_FAST               'defects'
            120_0  COME_FROM            84  '84'

 L. 356       120  LOAD_FAST                'groups'
              122  LOAD_FAST                'kwds'
              124  LOAD_STR                 'groups'
              126  STORE_SUBSCR     

 L. 357       128  LOAD_FAST                'defects'
              130  LOAD_FAST                'kwds'
              132  LOAD_STR                 'defects'
              134  STORE_SUBSCR     

 L. 358       136  LOAD_STR                 ', '
              138  LOAD_METHOD              join
              140  LOAD_LISTCOMP            '<code_object <listcomp>>'
              142  LOAD_STR                 'AddressHeader.parse.<locals>.<listcomp>'
              144  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              146  LOAD_FAST                'groups'
              148  GET_ITER         
              150  CALL_FUNCTION_1       1  ''
              152  CALL_METHOD_1         1  ''
              154  LOAD_FAST                'kwds'
              156  LOAD_STR                 'decoded'
              158  STORE_SUBSCR     

 L. 359       160  LOAD_STR                 'parse_tree'
              162  LOAD_FAST                'kwds'
              164  <118>                 1  ''
              166  POP_JUMP_IF_FALSE   186  'to 186'

 L. 360       168  LOAD_FAST                'cls'
              170  LOAD_METHOD              value_parser
              172  LOAD_FAST                'kwds'
              174  LOAD_STR                 'decoded'
              176  BINARY_SUBSCR    
              178  CALL_METHOD_1         1  ''
              180  LOAD_FAST                'kwds'
              182  LOAD_STR                 'parse_tree'
              184  STORE_SUBSCR     
            186_0  COME_FROM           166  '166'

Parse error at or near `<118>' instruction at offset 164

    def init--- This code section failed: ---

 L. 363         0  LOAD_GLOBAL              tuple
                2  LOAD_FAST                'kw'
                4  LOAD_METHOD              pop
                6  LOAD_STR                 'groups'
                8  CALL_METHOD_1         1  ''
               10  CALL_FUNCTION_1       1  ''
               12  LOAD_FAST                'self'
               14  STORE_ATTR               _groups

 L. 364        16  LOAD_CONST               None
               18  LOAD_FAST                'self'
               20  STORE_ATTR               _addresses

 L. 365        22  LOAD_GLOBAL              super
               24  CALL_FUNCTION_0       0  ''
               26  LOAD_ATTR                init
               28  LOAD_FAST                'args'
               30  BUILD_MAP_0           0 
               32  LOAD_FAST                'kw'
               34  <164>                 1  ''
               36  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               38  POP_TOP          

Parse error at or near `<164>' instruction at offset 34

    @property
    def groups(self):
        return self._groups

    @property
    def addresses--- This code section failed: ---

 L. 373         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _addresses
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    32  'to 32'

 L. 374        10  LOAD_GLOBAL              tuple
               12  LOAD_GENEXPR             '<code_object <genexpr>>'
               14  LOAD_STR                 'AddressHeader.addresses.<locals>.<genexpr>'
               16  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _groups
               22  GET_ITER         
               24  CALL_FUNCTION_1       1  ''
               26  CALL_FUNCTION_1       1  ''
               28  LOAD_FAST                'self'
               30  STORE_ATTR               _addresses
             32_0  COME_FROM             8  '8'

 L. 376        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _addresses
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class UniqueAddressHeader(AddressHeader):
    max_count = 1


class SingleAddressHeader(AddressHeader):

    @property
    def address(self):
        if len(self.addresses) != 1:
            raise ValueError('value of single address header {} is not a single address'.formatself.name)
        return self.addresses[0]


class UniqueSingleAddressHeader(SingleAddressHeader):
    max_count = 1


class MIMEVersionHeader:
    max_count = 1
    value_parser = staticmethod(parser.parse_mime_version)

    @classmethod
    def parse--- This code section failed: ---

 L. 407         0  LOAD_FAST                'cls'
                2  LOAD_METHOD              value_parser
                4  LOAD_FAST                'value'
                6  CALL_METHOD_1         1  ''
                8  DUP_TOP          
               10  LOAD_FAST                'kwds'
               12  LOAD_STR                 'parse_tree'
               14  STORE_SUBSCR     
               16  STORE_FAST               'parse_tree'

 L. 408        18  LOAD_GLOBAL              str
               20  LOAD_FAST                'parse_tree'
               22  CALL_FUNCTION_1       1  ''
               24  LOAD_FAST                'kwds'
               26  LOAD_STR                 'decoded'
               28  STORE_SUBSCR     

 L. 409        30  LOAD_FAST                'kwds'
               32  LOAD_STR                 'defects'
               34  BINARY_SUBSCR    
               36  LOAD_METHOD              extend
               38  LOAD_FAST                'parse_tree'
               40  LOAD_ATTR                all_defects
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          

 L. 410        46  LOAD_FAST                'parse_tree'
               48  LOAD_ATTR                minor
               50  LOAD_CONST               None
               52  <117>                 0  ''
               54  POP_JUMP_IF_FALSE    60  'to 60'
               56  LOAD_CONST               None
               58  JUMP_FORWARD         64  'to 64'
             60_0  COME_FROM            54  '54'
               60  LOAD_FAST                'parse_tree'
               62  LOAD_ATTR                major
             64_0  COME_FROM            58  '58'
               64  LOAD_FAST                'kwds'
               66  LOAD_STR                 'major'
               68  STORE_SUBSCR     

 L. 411        70  LOAD_FAST                'parse_tree'
               72  LOAD_ATTR                minor
               74  LOAD_FAST                'kwds'
               76  LOAD_STR                 'minor'
               78  STORE_SUBSCR     

 L. 412        80  LOAD_FAST                'parse_tree'
               82  LOAD_ATTR                minor
               84  LOAD_CONST               None
               86  <117>                 1  ''
               88  POP_JUMP_IF_FALSE   116  'to 116'

 L. 413        90  LOAD_STR                 '{}.{}'
               92  LOAD_METHOD              format
               94  LOAD_FAST                'kwds'
               96  LOAD_STR                 'major'
               98  BINARY_SUBSCR    
              100  LOAD_FAST                'kwds'
              102  LOAD_STR                 'minor'
              104  BINARY_SUBSCR    
              106  CALL_METHOD_2         2  ''
              108  LOAD_FAST                'kwds'
              110  LOAD_STR                 'version'
              112  STORE_SUBSCR     
              114  JUMP_FORWARD        124  'to 124'
            116_0  COME_FROM            88  '88'

 L. 415       116  LOAD_CONST               None
              118  LOAD_FAST                'kwds'
              120  LOAD_STR                 'version'
              122  STORE_SUBSCR     
            124_0  COME_FROM           114  '114'

Parse error at or near `<117>' instruction at offset 52

    def init--- This code section failed: ---

 L. 418         0  LOAD_FAST                'kw'
                2  LOAD_METHOD              pop
                4  LOAD_STR                 'version'
                6  CALL_METHOD_1         1  ''
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _version

 L. 419        12  LOAD_FAST                'kw'
               14  LOAD_METHOD              pop
               16  LOAD_STR                 'major'
               18  CALL_METHOD_1         1  ''
               20  LOAD_FAST                'self'
               22  STORE_ATTR               _major

 L. 420        24  LOAD_FAST                'kw'
               26  LOAD_METHOD              pop
               28  LOAD_STR                 'minor'
               30  CALL_METHOD_1         1  ''
               32  LOAD_FAST                'self'
               34  STORE_ATTR               _minor

 L. 421        36  LOAD_GLOBAL              super
               38  CALL_FUNCTION_0       0  ''
               40  LOAD_ATTR                init
               42  LOAD_FAST                'args'
               44  BUILD_MAP_0           0 
               46  LOAD_FAST                'kw'
               48  <164>                 1  ''
               50  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               52  POP_TOP          

Parse error at or near `<164>' instruction at offset 48

    @property
    def major(self):
        return self._major

    @property
    def minor(self):
        return self._minor

    @property
    def version(self):
        return self._version


class ParameterizedMIMEHeader:
    max_count = 1

    @classmethod
    def parse--- This code section failed: ---

 L. 445         0  LOAD_FAST                'cls'
                2  LOAD_METHOD              value_parser
                4  LOAD_FAST                'value'
                6  CALL_METHOD_1         1  ''
                8  DUP_TOP          
               10  LOAD_FAST                'kwds'
               12  LOAD_STR                 'parse_tree'
               14  STORE_SUBSCR     
               16  STORE_FAST               'parse_tree'

 L. 446        18  LOAD_GLOBAL              str
               20  LOAD_FAST                'parse_tree'
               22  CALL_FUNCTION_1       1  ''
               24  LOAD_FAST                'kwds'
               26  LOAD_STR                 'decoded'
               28  STORE_SUBSCR     

 L. 447        30  LOAD_FAST                'kwds'
               32  LOAD_STR                 'defects'
               34  BINARY_SUBSCR    
               36  LOAD_METHOD              extend
               38  LOAD_FAST                'parse_tree'
               40  LOAD_ATTR                all_defects
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          

 L. 448        46  LOAD_FAST                'parse_tree'
               48  LOAD_ATTR                params
               50  LOAD_CONST               None
               52  <117>                 0  ''
               54  POP_JUMP_IF_FALSE    66  'to 66'

 L. 449        56  BUILD_MAP_0           0 
               58  LOAD_FAST                'kwds'
               60  LOAD_STR                 'params'
               62  STORE_SUBSCR     
               64  JUMP_FORWARD         86  'to 86'
             66_0  COME_FROM            54  '54'

 L. 452        66  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               68  LOAD_STR                 'ParameterizedMIMEHeader.parse.<locals>.<dictcomp>'
               70  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 454        72  LOAD_FAST                'parse_tree'
               74  LOAD_ATTR                params

 L. 452        76  GET_ITER         
               78  CALL_FUNCTION_1       1  ''
               80  LOAD_FAST                'kwds'
               82  LOAD_STR                 'params'
               84  STORE_SUBSCR     
             86_0  COME_FROM            64  '64'

Parse error at or near `<117>' instruction at offset 52

    def init--- This code section failed: ---

 L. 457         0  LOAD_FAST                'kw'
                2  LOAD_METHOD              pop
                4  LOAD_STR                 'params'
                6  CALL_METHOD_1         1  ''
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _params

 L. 458        12  LOAD_GLOBAL              super
               14  CALL_FUNCTION_0       0  ''
               16  LOAD_ATTR                init
               18  LOAD_FAST                'args'
               20  BUILD_MAP_0           0 
               22  LOAD_FAST                'kw'
               24  <164>                 1  ''
               26  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               28  POP_TOP          

Parse error at or near `<164>' instruction at offset 24

    @property
    def params(self):
        return MappingProxyType(self._params)


class ContentTypeHeader(ParameterizedMIMEHeader):
    value_parser = staticmethod(parser.parse_content_type_header)

    def init--- This code section failed: ---

 L. 470         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_ATTR                init
                6  LOAD_FAST                'args'
                8  BUILD_MAP_0           0 
               10  LOAD_FAST                'kw'
               12  <164>                 1  ''
               14  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               16  POP_TOP          

 L. 471        18  LOAD_GLOBAL              utils
               20  LOAD_METHOD              _sanitize
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                _parse_tree
               26  LOAD_ATTR                maintype
               28  CALL_METHOD_1         1  ''
               30  LOAD_FAST                'self'
               32  STORE_ATTR               _maintype

 L. 472        34  LOAD_GLOBAL              utils
               36  LOAD_METHOD              _sanitize
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                _parse_tree
               42  LOAD_ATTR                subtype
               44  CALL_METHOD_1         1  ''
               46  LOAD_FAST                'self'
               48  STORE_ATTR               _subtype

Parse error at or near `None' instruction at offset -1

    @property
    def maintype(self):
        return self._maintype

    @property
    def subtype(self):
        return self._subtype

    @property
    def content_type(self):
        return self.maintype + '/' + self.subtype


class ContentDispositionHeader(ParameterizedMIMEHeader):
    value_parser = staticmethod(parser.parse_content_disposition_header)

    def init--- This code section failed: ---

 L. 492         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_ATTR                init
                6  LOAD_FAST                'args'
                8  BUILD_MAP_0           0 
               10  LOAD_FAST                'kw'
               12  <164>                 1  ''
               14  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               16  POP_TOP          

 L. 493        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _parse_tree
               22  LOAD_ATTR                content_disposition
               24  STORE_FAST               'cd'

 L. 494        26  LOAD_FAST                'cd'
               28  LOAD_CONST               None
               30  <117>                 0  ''
               32  POP_JUMP_IF_FALSE    38  'to 38'
               34  LOAD_FAST                'cd'
               36  JUMP_FORWARD         46  'to 46'
             38_0  COME_FROM            32  '32'
               38  LOAD_GLOBAL              utils
               40  LOAD_METHOD              _sanitize
               42  LOAD_FAST                'cd'
               44  CALL_METHOD_1         1  ''
             46_0  COME_FROM            36  '36'
               46  LOAD_FAST                'self'
               48  STORE_ATTR               _content_disposition

Parse error at or near `None' instruction at offset -1

    @property
    def content_disposition(self):
        return self._content_disposition


class ContentTransferEncodingHeader:
    max_count = 1
    value_parser = staticmethod(parser.parse_content_transfer_encoding_header)

    @classmethod
    def parse(cls, value, kwds):
        kwds['parse_tree'] = parse_tree = cls.value_parservalue
        kwds['decoded'] = str(parse_tree)
        kwds['defects'].extendparse_tree.all_defects

    def init--- This code section failed: ---

 L. 514         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_ATTR                init
                6  LOAD_FAST                'args'
                8  BUILD_MAP_0           0 
               10  LOAD_FAST                'kw'
               12  <164>                 1  ''
               14  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               16  POP_TOP          

 L. 515        18  LOAD_GLOBAL              utils
               20  LOAD_METHOD              _sanitize
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                _parse_tree
               26  LOAD_ATTR                cte
               28  CALL_METHOD_1         1  ''
               30  LOAD_FAST                'self'
               32  STORE_ATTR               _cte

Parse error at or near `None' instruction at offset -1

    @property
    def cte(self):
        return self._cte


class MessageIDHeader:
    max_count = 1
    value_parser = staticmethod(parser.parse_message_id)

    @classmethod
    def parse(cls, value, kwds):
        kwds['parse_tree'] = parse_tree = cls.value_parservalue
        kwds['decoded'] = str(parse_tree)
        kwds['defects'].extendparse_tree.all_defects


_default_header_map = {'subject':UniqueUnstructuredHeader, 
 'date':UniqueDateHeader, 
 'resent-date':DateHeader, 
 'orig-date':UniqueDateHeader, 
 'sender':UniqueSingleAddressHeader, 
 'resent-sender':SingleAddressHeader, 
 'to':UniqueAddressHeader, 
 'resent-to':AddressHeader, 
 'cc':UniqueAddressHeader, 
 'resent-cc':AddressHeader, 
 'bcc':UniqueAddressHeader, 
 'resent-bcc':AddressHeader, 
 'from':UniqueAddressHeader, 
 'resent-from':AddressHeader, 
 'reply-to':UniqueAddressHeader, 
 'mime-version':MIMEVersionHeader, 
 'content-type':ContentTypeHeader, 
 'content-disposition':ContentDispositionHeader, 
 'content-transfer-encoding':ContentTransferEncodingHeader, 
 'message-id':MessageIDHeader}

class HeaderRegistry:
    __doc__ = 'A header_factory and header registry.'

    def __init__(self, base_class=BaseHeader, default_class=UnstructuredHeader, use_default_map=True):
        """Create a header_factory that works with the Policy API.

        base_class is the class that will be the last class in the created
        header class's __bases__ list.  default_class is the class that will be
        used if "name" (see __call__) does not appear in the registry.
        use_default_map controls whether or not the default mapping of names to
        specialized classes is copied in to the registry when the factory is
        created.  The default is True.

        """
        self.registry = {}
        self.base_class = base_class
        self.default_class = default_class
        if use_default_map:
            self.registry.update_default_header_map

    def map_to_type(self, name, cls):
        """Register cls as the specialized class for handling "name" headers.

        """
        self.registry[name.lower()] = cls

    def __getitem__(self, name):
        cls = self.registry.getname.lower()self.default_class
        return type('_' + cls.__name__, (cls, self.base_class), {})

    def __call__(self, name, value):
        """Create a header instance for header 'name' from 'value'.

        Creates a header instance by creating a specialized class for parsing
        and representing the specified header by combining the factory
        base_class with a specialized class from the registry or the
        default_class, and passing the name and value to the constructed
        class's constructor.

        """
        return self[name](name, value)