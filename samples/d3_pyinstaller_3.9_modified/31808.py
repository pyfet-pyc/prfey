# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
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
VERSION_MANY = Combine((VERSION_ONE + ZeroOrMore(COMMA + VERSION_ONE)),
  joinString=',', adjacent=False)('_raw_spec')
_VERSION_SPEC = Optional(LPAREN + VERSION_MANY + RPAREN | VERSION_MANY)
_VERSION_SPEC.setParseAction(lambda s, l, t: t._raw_spec or '')
VERSION_SPEC = originalTextFor(_VERSION_SPEC)('specifier')
VERSION_SPEC.setParseAction(lambda s, l, t: t[1])
MARKER_EXPR = originalTextFor(MARKER_EXPR())('marker')
MARKER_EXPR.setParseAction(lambda s, l, t: Marker(s[t._original_start:t._original_end]))
MARKER_SEPARATOR = SEMICOLON
MARKER = MARKER_SEPARATOR + MARKER_EXPR
VERSION_AND_MARKER = VERSION_SPEC + Optional(MARKER)
URL_AND_MARKER = URL + Optional(MARKER)
NAMED_REQUIREMENT = NAME + Optional(EXTRAS) + (URL_AND_MARKER | VERSION_AND_MARKER)
REQUIREMENT = stringStart + NAMED_REQUIREMENT + stringEnd
REQUIREMENT.parseString('x[]')

class Requirement(object):
    __doc__ = 'Parse a requirement.\n\n    Parse a given requirement string into its parts, such as name, specifier,\n    URL, and extras. Raises InvalidRequirement on a badly-formed requirement\n    string.\n    '

    def __init__--- This code section failed: ---

 L.  92         0  SETUP_FINALLY        16  'to 16'

 L.  93         2  LOAD_GLOBAL              REQUIREMENT
                4  LOAD_METHOD              parseString
                6  LOAD_FAST                'requirement_string'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'req'
               12  POP_BLOCK        
               14  JUMP_FORWARD         86  'to 86'
             16_0  COME_FROM_FINALLY     0  '0'

 L.  94        16  DUP_TOP          
               18  LOAD_GLOBAL              ParseException
               20  <121>                84  ''
               22  POP_TOP          
               24  STORE_FAST               'e'
               26  POP_TOP          
               28  SETUP_FINALLY        76  'to 76'

 L.  95        30  LOAD_GLOBAL              InvalidRequirement

 L.  96        32  LOAD_STR                 'Parse error at "{0!r}": {1}'
               34  LOAD_METHOD              format

 L.  97        36  LOAD_FAST                'requirement_string'
               38  LOAD_FAST                'e'
               40  LOAD_ATTR                loc
               42  LOAD_FAST                'e'
               44  LOAD_ATTR                loc
               46  LOAD_CONST               8
               48  BINARY_ADD       
               50  BUILD_SLICE_2         2 
               52  BINARY_SUBSCR    
               54  LOAD_FAST                'e'
               56  LOAD_ATTR                msg

 L.  96        58  CALL_METHOD_2         2  ''

 L.  95        60  CALL_FUNCTION_1       1  ''
               62  RAISE_VARARGS_1       1  'exception instance'
               64  POP_BLOCK        
               66  POP_EXCEPT       
               68  LOAD_CONST               None
               70  STORE_FAST               'e'
               72  DELETE_FAST              'e'
               74  JUMP_FORWARD         86  'to 86'
             76_0  COME_FROM_FINALLY    28  '28'
               76  LOAD_CONST               None
               78  STORE_FAST               'e'
               80  DELETE_FAST              'e'
               82  <48>             
               84  <48>             
             86_0  COME_FROM            74  '74'
             86_1  COME_FROM            14  '14'

 L. 101        86  LOAD_FAST                'req'
               88  LOAD_ATTR                name
               90  LOAD_FAST                'self'
               92  STORE_ATTR               name

 L. 102        94  LOAD_FAST                'req'
               96  LOAD_ATTR                url
               98  POP_JUMP_IF_FALSE   198  'to 198'

 L. 103       100  LOAD_GLOBAL              urlparse
              102  LOAD_METHOD              urlparse
              104  LOAD_FAST                'req'
              106  LOAD_ATTR                url
              108  CALL_METHOD_1         1  ''
              110  STORE_FAST               'parsed_url'

 L. 104       112  LOAD_FAST                'parsed_url'
              114  LOAD_ATTR                scheme
              116  LOAD_STR                 'file'
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   148  'to 148'

 L. 105       122  LOAD_GLOBAL              urlparse
              124  LOAD_METHOD              urlunparse
              126  LOAD_FAST                'parsed_url'
              128  CALL_METHOD_1         1  ''
              130  LOAD_FAST                'req'
              132  LOAD_ATTR                url
              134  COMPARE_OP               !=
              136  POP_JUMP_IF_FALSE   188  'to 188'

 L. 106       138  LOAD_GLOBAL              InvalidRequirement
              140  LOAD_STR                 'Invalid URL given'
              142  CALL_FUNCTION_1       1  ''
              144  RAISE_VARARGS_1       1  'exception instance'
              146  JUMP_FORWARD        188  'to 188'
            148_0  COME_FROM           120  '120'

 L. 107       148  LOAD_FAST                'parsed_url'
              150  LOAD_ATTR                scheme
              152  POP_JUMP_IF_FALSE   172  'to 172'
              154  LOAD_FAST                'parsed_url'
              156  LOAD_ATTR                netloc
              158  POP_JUMP_IF_FALSE   172  'to 172'

 L. 108       160  LOAD_FAST                'parsed_url'
              162  LOAD_ATTR                scheme

 L. 107       164  POP_JUMP_IF_TRUE    188  'to 188'

 L. 108       166  LOAD_FAST                'parsed_url'
              168  LOAD_ATTR                netloc

 L. 107       170  POP_JUMP_IF_TRUE    188  'to 188'
            172_0  COME_FROM           158  '158'
            172_1  COME_FROM           152  '152'

 L. 110       172  LOAD_GLOBAL              InvalidRequirement
              174  LOAD_STR                 'Invalid URL: {0}'
              176  LOAD_METHOD              format
              178  LOAD_FAST                'req'
              180  LOAD_ATTR                url
              182  CALL_METHOD_1         1  ''
              184  CALL_FUNCTION_1       1  ''
              186  RAISE_VARARGS_1       1  'exception instance'
            188_0  COME_FROM           170  '170'
            188_1  COME_FROM           164  '164'
            188_2  COME_FROM           146  '146'
            188_3  COME_FROM           136  '136'

 L. 111       188  LOAD_FAST                'req'
              190  LOAD_ATTR                url
              192  LOAD_FAST                'self'
              194  STORE_ATTR               url
              196  JUMP_FORWARD        204  'to 204'
            198_0  COME_FROM            98  '98'

 L. 113       198  LOAD_CONST               None
              200  LOAD_FAST                'self'
              202  STORE_ATTR               url
            204_0  COME_FROM           196  '196'

 L. 114       204  LOAD_GLOBAL              set
              206  LOAD_FAST                'req'
              208  LOAD_ATTR                extras
              210  POP_JUMP_IF_FALSE   222  'to 222'
              212  LOAD_FAST                'req'
              214  LOAD_ATTR                extras
              216  LOAD_METHOD              asList
              218  CALL_METHOD_0         0  ''
              220  JUMP_FORWARD        224  'to 224'
            222_0  COME_FROM           210  '210'
              222  BUILD_LIST_0          0 
            224_0  COME_FROM           220  '220'
              224  CALL_FUNCTION_1       1  ''
              226  LOAD_FAST                'self'
              228  STORE_ATTR               extras

 L. 115       230  LOAD_GLOBAL              SpecifierSet
              232  LOAD_FAST                'req'
              234  LOAD_ATTR                specifier
              236  CALL_FUNCTION_1       1  ''
              238  LOAD_FAST                'self'
              240  STORE_ATTR               specifier

 L. 116       242  LOAD_FAST                'req'
              244  LOAD_ATTR                marker
              246  POP_JUMP_IF_FALSE   254  'to 254'
              248  LOAD_FAST                'req'
              250  LOAD_ATTR                marker
              252  JUMP_FORWARD        256  'to 256'
            254_0  COME_FROM           246  '246'
              254  LOAD_CONST               None
            256_0  COME_FROM           252  '252'
              256  LOAD_FAST                'self'
              258  STORE_ATTR               marker

Parse error at or near `<121>' instruction at offset 20

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
                parts.append(' ')
        if self.marker:
            parts.append('; {0}'.format(self.marker))
        return ''.join(parts)

    def __repr__(self):
        return '<Requirement({0!r})>'.format(str(self))