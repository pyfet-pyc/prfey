# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: setuptools\_vendor\packaging\requirements.py
from __future__ import absolute_import, division, print_function
import string, re
from setuptools.extern.pyparsing import stringStart, stringEnd, originalTextFor, ParseException
from setuptools.extern.pyparsing import ZeroOrMore, Word, Optional, Regex, Combine
import setuptools.extern.pyparsing as L
import setuptools.extern.six.moves.urllib as urlparse
from .markers import MARKER_EXPR, Marker
from .specifiers import LegacySpecifier, Specifier, SpecifierSet

class InvalidRequirement(ValueError):
    __doc__ = '\n    An invalid requirement was found, users should refer to PEP 508.\n    '


ALPHANUM = Word(string.ascii_letters + string.digits)
LBRACKET = L('[').suppress()
RBRACKET = L(']').suppress()
LPAREN = L('(').suppress()
RPAREN = L(')').suppress()
COMMA = L(',').suppress()
SEMICOLON = L(';').suppress()
AT = L('@').suppress()
PUNCTUATION = Word('-_.')
IDENTIFIER_END = ALPHANUM | ZeroOrMore(PUNCTUATION) + ALPHANUM
IDENTIFIER = Combine(ALPHANUM + ZeroOrMore(IDENTIFIER_END))
NAME = IDENTIFIER('name')
EXTRA = IDENTIFIER
URI = Regex('[^ ]+')('url')
URL = AT + URI
EXTRAS_LIST = EXTRA + ZeroOrMore(COMMA + EXTRA)
EXTRAS = LBRACKET + Optional(EXTRAS_LIST) + RBRACKET('extras')
VERSION_PEP440 = Regex(Specifier._regex_str, re.VERBOSE | re.IGNORECASE)
VERSION_LEGACY = Regex(LegacySpecifier._regex_str, re.VERBOSE | re.IGNORECASE)
VERSION_ONE = VERSION_PEP440 ^ VERSION_LEGACY
VERSION_MANY = Combine((VERSION_ONE + ZeroOrMore(COMMA + VERSION_ONE)), joinString=',',
  adjacent=False)('_raw_spec')
_VERSION_SPEC = Optional(LPAREN + VERSION_MANY + RPAREN | VERSION_MANY)
_VERSION_SPEC.setParseAction(lambda s, l, t: t._raw_spec or '')
VERSION_SPEC = originalTextFor(_VERSION_SPEC)('specifier')
VERSION_SPEC.setParseAction(lambda s, l, t: t[1])
MARKER_EXPR = originalTextFor(MARKER_EXPR())('marker')
MARKER_EXPR.setParseAction(lambda s, l, t: Marker(s[t._original_start:t._original_end]))
MARKER_SEPERATOR = SEMICOLON
MARKER = MARKER_SEPERATOR + MARKER_EXPR
VERSION_AND_MARKER = VERSION_SPEC + Optional(MARKER)
URL_AND_MARKER = URL + Optional(MARKER)
NAMED_REQUIREMENT = NAME + Optional(EXTRAS) + (URL_AND_MARKER | VERSION_AND_MARKER)
REQUIREMENT = stringStart + NAMED_REQUIREMENT + stringEnd

class Requirement(object):
    __doc__ = 'Parse a requirement.\n\n    Parse a given requirement string into its parts, such as name, specifier,\n    URL, and extras. Raises InvalidRequirement on a badly-formed requirement\n    string.\n    '

    def __init__--- This code section failed: ---

 L.  89         0  SETUP_EXCEPT         16  'to 16'

 L.  90         2  LOAD_GLOBAL              REQUIREMENT
                4  LOAD_METHOD              parseString
                6  LOAD_FAST                'requirement_string'
                8  CALL_METHOD_1         1  '1 positional argument'
               10  STORE_FAST               'req'
               12  POP_BLOCK        
               14  JUMP_FORWARD         80  'to 80'
             16_0  COME_FROM_EXCEPT      0  '0'

 L.  91        16  DUP_TOP          
               18  LOAD_GLOBAL              ParseException
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    78  'to 78'
               24  POP_TOP          
               26  STORE_FAST               'e'
               28  POP_TOP          
               30  SETUP_FINALLY        66  'to 66'

 L.  92        32  LOAD_GLOBAL              InvalidRequirement

 L.  93        34  LOAD_STR                 'Invalid requirement, parse error at "{0!r}"'
               36  LOAD_METHOD              format

 L.  94        38  LOAD_FAST                'requirement_string'
               40  LOAD_FAST                'e'
               42  LOAD_ATTR                loc
               44  LOAD_FAST                'e'
               46  LOAD_ATTR                loc
               48  LOAD_CONST               8
               50  BINARY_ADD       
               52  BUILD_SLICE_2         2 
               54  BINARY_SUBSCR    
               56  CALL_METHOD_1         1  '1 positional argument'
               58  CALL_FUNCTION_1       1  '1 positional argument'
               60  RAISE_VARARGS_1       1  'exception instance'
               62  POP_BLOCK        
               64  LOAD_CONST               None
             66_0  COME_FROM_FINALLY    30  '30'
               66  LOAD_CONST               None
               68  STORE_FAST               'e'
               70  DELETE_FAST              'e'
               72  END_FINALLY      
               74  POP_EXCEPT       
               76  JUMP_FORWARD         80  'to 80'
             78_0  COME_FROM            22  '22'
               78  END_FINALLY      
             80_0  COME_FROM            76  '76'
             80_1  COME_FROM            14  '14'

 L.  96        80  LOAD_FAST                'req'
               82  LOAD_ATTR                name
               84  LOAD_FAST                'self'
               86  STORE_ATTR               name

 L.  97        88  LOAD_FAST                'req'
               90  LOAD_ATTR                url
               92  POP_JUMP_IF_FALSE   148  'to 148'

 L.  98        94  LOAD_GLOBAL              urlparse
               96  LOAD_METHOD              urlparse
               98  LOAD_FAST                'req'
              100  LOAD_ATTR                url
              102  CALL_METHOD_1         1  '1 positional argument'
              104  STORE_FAST               'parsed_url'

 L.  99       106  LOAD_FAST                'parsed_url'
              108  LOAD_ATTR                scheme
              110  POP_JUMP_IF_FALSE   130  'to 130'
              112  LOAD_FAST                'parsed_url'
              114  LOAD_ATTR                netloc
              116  POP_JUMP_IF_FALSE   130  'to 130'

 L. 100       118  LOAD_FAST                'parsed_url'
              120  LOAD_ATTR                scheme
              122  POP_JUMP_IF_TRUE    138  'to 138'
              124  LOAD_FAST                'parsed_url'
              126  LOAD_ATTR                netloc
              128  POP_JUMP_IF_TRUE    138  'to 138'
            130_0  COME_FROM           116  '116'
            130_1  COME_FROM           110  '110'

 L. 101       130  LOAD_GLOBAL              InvalidRequirement
              132  LOAD_STR                 'Invalid URL given'
              134  CALL_FUNCTION_1       1  '1 positional argument'
              136  RAISE_VARARGS_1       1  'exception instance'
            138_0  COME_FROM           128  '128'
            138_1  COME_FROM           122  '122'

 L. 102       138  LOAD_FAST                'req'
              140  LOAD_ATTR                url
              142  LOAD_FAST                'self'
              144  STORE_ATTR               url
              146  JUMP_FORWARD        154  'to 154'
            148_0  COME_FROM            92  '92'

 L. 104       148  LOAD_CONST               None
              150  LOAD_FAST                'self'
              152  STORE_ATTR               url
            154_0  COME_FROM           146  '146'

 L. 105       154  LOAD_GLOBAL              set
              156  LOAD_FAST                'req'
              158  LOAD_ATTR                extras
              160  POP_JUMP_IF_FALSE   172  'to 172'
              162  LOAD_FAST                'req'
              164  LOAD_ATTR                extras
              166  LOAD_METHOD              asList
              168  CALL_METHOD_0         0  '0 positional arguments'
              170  JUMP_FORWARD        174  'to 174'
            172_0  COME_FROM           160  '160'
              172  BUILD_LIST_0          0 
            174_0  COME_FROM           170  '170'
              174  CALL_FUNCTION_1       1  '1 positional argument'
              176  LOAD_FAST                'self'
              178  STORE_ATTR               extras

 L. 106       180  LOAD_GLOBAL              SpecifierSet
              182  LOAD_FAST                'req'
              184  LOAD_ATTR                specifier
              186  CALL_FUNCTION_1       1  '1 positional argument'
              188  LOAD_FAST                'self'
              190  STORE_ATTR               specifier

 L. 107       192  LOAD_FAST                'req'
              194  LOAD_ATTR                marker
              196  POP_JUMP_IF_FALSE   204  'to 204'
              198  LOAD_FAST                'req'
              200  LOAD_ATTR                marker
              202  JUMP_FORWARD        206  'to 206'
            204_0  COME_FROM           196  '196'
              204  LOAD_CONST               None
            206_0  COME_FROM           202  '202'
              206  LOAD_FAST                'self'
              208  STORE_ATTR               marker

Parse error at or near `JUMP_FORWARD' instruction at offset 146

    def __str__(self):
        parts = [
         self.name]
        if self.extras:
            parts.append('[{0}]'.format(','.join(sorted(self.extras))))
        if self.specifier:
            parts.append(str(self.specifier))
        if self.url:
            parts.append('@ {0}'.format(self.url))
        if self.marker:
            parts.append('; {0}'.format(self.marker))
        return ''.join(parts)

    def __repr__(self):
        return '<Requirement({0!r})>'.format(str(self))