# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\bs4\dammit.py
"""Beautiful Soup bonus library: Unicode, Dammit

This library converts a bytestream to Unicode through any means
necessary. It is heavily based on code from Mark Pilgrim's Universal
Feed Parser. It works best on XML and HTML, but it does not rewrite the
XML or HTML to reflect a new encoding; that's the tree builder's job.
"""
__license__ = 'MIT'
import codecs
from html.entities import codepoint2name
import re, logging, string
chardet_type = None
try:
    import cchardet

    def chardet_dammit(s):
        if isinstance(s, str):
            return
        return cchardet.detect(s)['encoding']


except ImportError:
    try:
        import chardet

        def chardet_dammit(s):
            if isinstance(s, str):
                return
            return chardet.detect(s)['encoding']


    except ImportError:

        def chardet_dammit(s):
            pass


try:
    import iconv_codec
except ImportError:
    pass

xml_encoding = '^\\s*<\\?.*encoding=[\'"](.*?)[\'"].*\\?>'
html_meta = '<\\s*meta[^>]+charset\\s*=\\s*["\']?([^>]*?)[ /;\'">]'
encoding_res = dict()
encoding_res[bytes] = {'html':re.compile(html_meta.encode('ascii'), re.I), 
 'xml':re.compile(xml_encoding.encode('ascii'), re.I)}
encoding_res[str] = {'html':re.compile(html_meta, re.I), 
 'xml':re.compile(xml_encoding, re.I)}

class EntitySubstitution(object):
    __doc__ = 'Substitute XML or HTML entities for the corresponding characters.'

    def _populate_class_variables():
        lookup = {}
        reverse_lookup = {}
        characters_for_re = []
        extra = [
         (39, 'apos')]
        for codepoint, name in list(codepoint2name.items()) + extra:
            character = chr(codepoint)
            if codepoint not in (34, 39):
                characters_for_re.append(character)
                lookup[character] = name
            reverse_lookup[name] = character

        re_definition = '[%s]' % ''.join(characters_for_re)
        return (lookup, reverse_lookup, re.compile(re_definition))

    CHARACTER_TO_HTML_ENTITY, HTML_ENTITY_TO_CHARACTER, CHARACTER_TO_HTML_ENTITY_RE = _populate_class_variables()
    CHARACTER_TO_XML_ENTITY = {"'":'apos', 
     '"':'quot', 
     '&':'amp', 
     '<':'lt', 
     '>':'gt'}
    BARE_AMPERSAND_OR_BRACKET = re.compile('([<>]|&(?!#\\d+;|#x[0-9a-fA-F]+;|\\w+;))')
    AMPERSAND_OR_BRACKET = re.compile('([<>&])')

    @classmethod
    def _substitute_html_entity(cls, matchobj):
        entity = cls.CHARACTER_TO_HTML_ENTITY.get(matchobj.group(0))
        return '&%s;' % entity

    @classmethod
    def _substitute_xml_entity(cls, matchobj):
        """Used with a regular expression to substitute the
        appropriate XML entity for an XML special character."""
        entity = cls.CHARACTER_TO_XML_ENTITY[matchobj.group(0)]
        return '&%s;' % entity

    @classmethod
    def quoted_attribute_value(self, value):
        """Make a value into a quoted XML attribute, possibly escaping it.

         Most strings will be quoted using double quotes.

          Bob's Bar -> "Bob's Bar"

         If a string contains double quotes, it will be quoted using
         single quotes.

          Welcome to "my bar" -> 'Welcome to "my bar"'

         If a string contains both single and double quotes, the
         double quotes will be escaped, and the string will be quoted
         using double quotes.

          Welcome to "Bob's Bar" -> "Welcome to &quot;Bob's bar&quot;
        """
        quote_with = '"'
        if '"' in value:
            if "'" in value:
                replace_with = '&quot;'
                value = value.replace('"', replace_with)
            else:
                quote_with = "'"
        return quote_with + value + quote_with

    @classmethod
    def substitute_xml(cls, value, make_quoted_attribute=False):
        """Substitute XML entities for special XML characters.

        :param value: A string to be substituted. The less-than sign
          will become &lt;, the greater-than sign will become &gt;,
          and any ampersands will become &amp;. If you want ampersands
          that appear to be part of an entity definition to be left
          alone, use substitute_xml_containing_entities() instead.

        :param make_quoted_attribute: If True, then the string will be
         quoted, as befits an attribute value.
        """
        value = cls.AMPERSAND_OR_BRACKET.sub(cls._substitute_xml_entity, value)
        if make_quoted_attribute:
            value = cls.quoted_attribute_value(value)
        return value

    @classmethod
    def substitute_xml_containing_entities(cls, value, make_quoted_attribute=False):
        """Substitute XML entities for special XML characters.

        :param value: A string to be substituted. The less-than sign will
          become &lt;, the greater-than sign will become &gt;, and any
          ampersands that are not part of an entity defition will
          become &amp;.

        :param make_quoted_attribute: If True, then the string will be
         quoted, as befits an attribute value.
        """
        value = cls.BARE_AMPERSAND_OR_BRACKET.sub(cls._substitute_xml_entity, value)
        if make_quoted_attribute:
            value = cls.quoted_attribute_value(value)
        return value

    @classmethod
    def substitute_html(cls, s):
        """Replace certain Unicode characters with named HTML entities.

        This differs from data.encode(encoding, 'xmlcharrefreplace')
        in that the goal is to make the result more readable (to those
        with ASCII displays) rather than to recover from
        errors. There's absolutely nothing wrong with a UTF-8 string
        containg a LATIN SMALL LETTER E WITH ACUTE, but replacing that
        character with "&eacute;" will make it more readable to some
        people.
        """
        return cls.CHARACTER_TO_HTML_ENTITY_RE.sub(cls._substitute_html_entity, s)


class EncodingDetector:
    __doc__ = 'Suggests a number of possible encodings for a bytestring.\n\n    Order of precedence:\n\n    1. Encodings you specifically tell EncodingDetector to try first\n    (the override_encodings argument to the constructor).\n\n    2. An encoding declared within the bytestring itself, either in an\n    XML declaration (if the bytestring is to be interpreted as an XML\n    document), or in a <meta> tag (if the bytestring is to be\n    interpreted as an HTML document.)\n\n    3. An encoding detected through textual analysis by chardet,\n    cchardet, or a similar external library.\n\n    4. UTF-8.\n\n    5. Windows-1252.\n    '

    def __init__(self, markup, override_encodings=None, is_html=False, exclude_encodings=None):
        self.override_encodings = override_encodings or []
        exclude_encodings = exclude_encodings or []
        self.exclude_encodings = set([x.lower() for x in exclude_encodings])
        self.chardet_encoding = None
        self.is_html = is_html
        self.declared_encoding = None
        self.markup, self.sniffed_encoding = self.strip_byte_order_mark(markup)

    def _usable(self, encoding, tried):
        if encoding is not None:
            encoding = encoding.lower()
            if encoding in self.exclude_encodings:
                return False
            if encoding not in tried:
                tried.add(encoding)
                return True
        return False

    @property
    def encodings(self):
        """Yield a number of encodings that might work for this markup."""
        tried = set()
        for e in self.override_encodings:
            if self._usable(e, tried):
                yield e

        if self._usable(self.sniffed_encoding, tried):
            yield self.sniffed_encoding
        if self.declared_encoding is None:
            self.declared_encoding = self.find_declared_encoding(self.markup, self.is_html)
        if self._usable(self.declared_encoding, tried):
            yield self.declared_encoding
        if self.chardet_encoding is None:
            self.chardet_encoding = chardet_dammit(self.markup)
        if self._usable(self.chardet_encoding, tried):
            yield self.chardet_encoding
        for e in ('utf-8', 'windows-1252'):
            if self._usable(e, tried):
                yield e

    @classmethod
    def strip_byte_order_mark(cls, data):
        """If a byte-order mark is present, strip it and return the encoding it implies."""
        encoding = None
        if isinstance(data, str):
            return (data, encoding)
        if len(data) >= 4 and data[:2] == b'\xfe\xff' and data[2:4] != '\x00\x00':
            encoding = 'utf-16be'
            data = data[2:]
        else:
            if len(data) >= 4 and data[:2] == b'\xff\xfe' and data[2:4] != '\x00\x00':
                encoding = 'utf-16le'
                data = data[2:]
            else:
                if data[:3] == b'\xef\xbb\xbf':
                    encoding = 'utf-8'
                    data = data[3:]
                else:
                    if data[:4] == b'\x00\x00\xfe\xff':
                        encoding = 'utf-32be'
                        data = data[4:]
                    else:
                        if data[:4] == b'\xff\xfe\x00\x00':
                            encoding = 'utf-32le'
                            data = data[4:]
        return (
         data, encoding)

    @classmethod
    def find_declared_encoding(cls, markup, is_html=False, search_entire_document=False):
        """Given a document, tries to find its declared encoding.

        An XML encoding is declared at the beginning of the document.

        An HTML encoding is declared in a <meta> tag, hopefully near the
        beginning of the document.
        """
        if search_entire_document:
            xml_endpos = html_endpos = len(markup)
        else:
            xml_endpos = 1024
            html_endpos = max(2048, int(len(markup) * 0.05))
        if isinstance(markup, bytes):
            res = encoding_res[bytes]
        else:
            res = encoding_res[str]
        xml_re = res['xml']
        html_re = res['html']
        declared_encoding = None
        declared_encoding_match = xml_re.search(markup, endpos=xml_endpos)
        if not declared_encoding_match:
            if is_html:
                declared_encoding_match = html_re.search(markup, endpos=html_endpos)
        if declared_encoding_match is not None:
            declared_encoding = declared_encoding_match.groups()[0]
        if declared_encoding:
            if isinstance(declared_encoding, bytes):
                declared_encoding = declared_encoding.decode('ascii', 'replace')
            return declared_encoding.lower()


class UnicodeDammit:
    __doc__ = 'A class for detecting the encoding of a *ML document and\n    converting it to a Unicode string. If the source encoding is\n    windows-1252, can replace MS smart quotes with their HTML or XML\n    equivalents.'
    CHARSET_ALIASES = {'macintosh':'mac-roman', 
     'x-sjis':'shift-jis'}
    ENCODINGS_WITH_SMART_QUOTES = [
     'windows-1252',
     'iso-8859-1',
     'iso-8859-2']

    def __init__(self, markup, override_encodings=[], smart_quotes_to=None, is_html=False, exclude_encodings=[]):
        self.smart_quotes_to = smart_quotes_to
        self.tried_encodings = []
        self.contains_replacement_characters = False
        self.is_html = is_html
        self.log = logging.getLogger(__name__)
        self.detector = EncodingDetector(markup, override_encodings, is_html, exclude_encodings)
        if isinstance(markup, str) or markup == '':
            self.markup = markup
            self.unicode_markup = str(markup)
            self.original_encoding = None
            return
        self.markup = self.detector.markup
        u = None
        for encoding in self.detector.encodings:
            markup = self.detector.markup
            u = self._convert_from(encoding)
            if u is not None:
                break

        if not u:
            for encoding in self.detector.encodings:
                if encoding != 'ascii':
                    u = self._convert_from(encoding, 'replace')
                if u is not None:
                    self.log.warning('Some characters could not be decoded, and were replaced with REPLACEMENT CHARACTER.')
                    self.contains_replacement_characters = True
                    break

        self.unicode_markup = u
        if not u:
            self.original_encoding = None

    def _sub_ms_char(self, match):
        """Changes a MS smart quote character to an XML or HTML
        entity, or an ASCII character."""
        orig = match.group(1)
        if self.smart_quotes_to == 'ascii':
            sub = self.MS_CHARS_TO_ASCII.get(orig).encode()
        else:
            sub = self.MS_CHARS.get(orig)
            if type(sub) == tuple:
                if self.smart_quotes_to == 'xml':
                    sub = '&#x'.encode() + sub[1].encode() + ';'.encode()
                else:
                    sub = '&'.encode() + sub[0].encode() + ';'.encode()
            else:
                sub = sub.encode()
        return sub

    def _convert_from(self, proposed, errors='strict'):
        proposed = self.find_codec(proposed)
        if not proposed or (proposed, errors) in self.tried_encodings:
            return
        self.tried_encodings.append((proposed, errors))
        markup = self.markup
        if self.smart_quotes_to is not None:
            if proposed in self.ENCODINGS_WITH_SMART_QUOTES:
                smart_quotes_re = b'([\x80-\x9f])'
                smart_quotes_compiled = re.compile(smart_quotes_re)
                markup = smart_quotes_compiled.sub(self._sub_ms_char, markup)
        try:
            u = self._to_unicode(markup, proposed, errors)
            self.markup = u
            self.original_encoding = proposed
        except Exception as e:
            try:
                return
            finally:
                e = None
                del e

        return self.markup

    def _to_unicode(self, data, encoding, errors='strict'):
        """Given a string and its encoding, decodes the string into Unicode.
        %encoding is a string recognized by encodings.aliases"""
        return str(data, encoding, errors)

    @property
    def declared_html_encoding(self):
        if not self.is_html:
            return
        return self.detector.declared_encoding

    def find_codec(self, charset):
        value = self._codec(self.CHARSET_ALIASES.get(charset, charset)) or charset and self._codec(charset.replace('-', '')) or charset and self._codec(charset.replace('-', '_')) or charset and charset.lower() or charset
        if value:
            return value.lower()

    def _codec(self, charset):
        if not charset:
            return charset
        codec = None
        try:
            codecs.lookup(charset)
            codec = charset
        except (LookupError, ValueError):
            pass

        return codec

    MS_CHARS = {b'\x80':('euro', '20AC'), 
     b'\x81':' ', 
     b'\x82':('sbquo', '201A'), 
     b'\x83':('fnof', '192'), 
     b'\x84':('bdquo', '201E'), 
     b'\x85':('hellip', '2026'), 
     b'\x86':('dagger', '2020'), 
     b'\x87':('Dagger', '2021'), 
     b'\x88':('circ', '2C6'), 
     b'\x89':('permil', '2030'), 
     b'\x8a':('Scaron', '160'), 
     b'\x8b':('lsaquo', '2039'), 
     b'\x8c':('OElig', '152'), 
     b'\x8d':'?', 
     b'\x8e':('#x17D', '17D'), 
     b'\x8f':'?', 
     b'\x90':'?', 
     b'\x91':('lsquo', '2018'), 
     b'\x92':('rsquo', '2019'), 
     b'\x93':('ldquo', '201C'), 
     b'\x94':('rdquo', '201D'), 
     b'\x95':('bull', '2022'), 
     b'\x96':('ndash', '2013'), 
     b'\x97':('mdash', '2014'), 
     b'\x98':('tilde', '2DC'), 
     b'\x99':('trade', '2122'), 
     b'\x9a':('scaron', '161'), 
     b'\x9b':('rsaquo', '203A'), 
     b'\x9c':('oelig', '153'), 
     b'\x9d':'?', 
     b'\x9e':('#x17E', '17E'), 
     b'\x9f':('Yuml', '')}
    MS_CHARS_TO_ASCII = {b'\x80':'EUR', 
     b'\x81':' ', 
     b'\x82':',', 
     b'\x83':'f', 
     b'\x84':',,', 
     b'\x85':'...', 
     b'\x86':'+', 
     b'\x87':'++', 
     b'\x88':'^', 
     b'\x89':'%', 
     b'\x8a':'S', 
     b'\x8b':'<', 
     b'\x8c':'OE', 
     b'\x8d':'?', 
     b'\x8e':'Z', 
     b'\x8f':'?', 
     b'\x90':'?', 
     b'\x91':"'", 
     b'\x92':"'", 
     b'\x93':'"', 
     b'\x94':'"', 
     b'\x95':'*', 
     b'\x96':'-', 
     b'\x97':'--', 
     b'\x98':'~', 
     b'\x99':'(TM)', 
     b'\x9a':'s', 
     b'\x9b':'>', 
     b'\x9c':'oe', 
     b'\x9d':'?', 
     b'\x9e':'z', 
     b'\x9f':'Y', 
     b'\xa0':' ', 
     b'\xa1':'!', 
     b'\xa2':'c', 
     b'\xa3':'GBP', 
     b'\xa4':'$', 
     b'\xa5':'YEN', 
     b'\xa6':'|', 
     b'\xa7':'S', 
     b'\xa8':'..', 
     b'\xa9':'', 
     b'\xaa':'(th)', 
     b'\xab':'<<', 
     b'\xac':'!', 
     b'\xad':' ', 
     b'\xae':'(R)', 
     b'\xaf':'-', 
     b'\xb0':'o', 
     b'\xb1':'+-', 
     b'\xb2':'2', 
     b'\xb3':'3', 
     b'\xb4':("'", 'acute'), 
     b'\xb5':'u', 
     b'\xb6':'P', 
     b'\xb7':'*', 
     b'\xb8':',', 
     b'\xb9':'1', 
     b'\xba':'(th)', 
     b'\xbb':'>>', 
     b'\xbc':'1/4', 
     b'\xbd':'1/2', 
     b'\xbe':'3/4', 
     b'\xbf':'?', 
     b'\xc0':'A', 
     b'\xc1':'A', 
     b'\xc2':'A', 
     b'\xc3':'A', 
     b'\xc4':'A', 
     b'\xc5':'A', 
     b'\xc6':'AE', 
     b'\xc7':'C', 
     b'\xc8':'E', 
     b'\xc9':'E', 
     b'\xca':'E', 
     b'\xcb':'E', 
     b'\xcc':'I', 
     b'\xcd':'I', 
     b'\xce':'I', 
     b'\xcf':'I', 
     b'\xd0':'D', 
     b'\xd1':'N', 
     b'\xd2':'O', 
     b'\xd3':'O', 
     b'\xd4':'O', 
     b'\xd5':'O', 
     b'\xd6':'O', 
     b'\xd7':'*', 
     b'\xd8':'O', 
     b'\xd9':'U', 
     b'\xda':'U', 
     b'\xdb':'U', 
     b'\xdc':'U', 
     b'\xdd':'Y', 
     b'\xde':'b', 
     b'\xdf':'B', 
     b'\xe0':'a', 
     b'\xe1':'a', 
     b'\xe2':'a', 
     b'\xe3':'a', 
     b'\xe4':'a', 
     b'\xe5':'a', 
     b'\xe6':'ae', 
     b'\xe7':'c', 
     b'\xe8':'e', 
     b'\xe9':'e', 
     b'\xea':'e', 
     b'\xeb':'e', 
     b'\xec':'i', 
     b'\xed':'i', 
     b'\xee':'i', 
     b'\xef':'i', 
     b'\xf0':'o', 
     b'\xf1':'n', 
     b'\xf2':'o', 
     b'\xf3':'o', 
     b'\xf4':'o', 
     b'\xf5':'o', 
     b'\xf6':'o', 
     b'\xf7':'/', 
     b'\xf8':'o', 
     b'\xf9':'u', 
     b'\xfa':'u', 
     b'\xfb':'u', 
     b'\xfc':'u', 
     b'\xfd':'y', 
     b'\xfe':'b', 
     b'\xff':'y'}
    WINDOWS_1252_TO_UTF8 = {128:b'\xe2\x82\xac', 
     130:b'\xe2\x80\x9a', 
     131:b'\xc6\x92', 
     132:b'\xe2\x80\x9e', 
     133:b'\xe2\x80\xa6', 
     134:b'\xe2\x80\xa0', 
     135:b'\xe2\x80\xa1', 
     136:b'\xcb\x86', 
     137:b'\xe2\x80\xb0', 
     138:b'\xc5\xa0', 
     139:b'\xe2\x80\xb9', 
     140:b'\xc5\x92', 
     142:b'\xc5\xbd', 
     145:b'\xe2\x80\x98', 
     146:b'\xe2\x80\x99', 
     147:b'\xe2\x80\x9c', 
     148:b'\xe2\x80\x9d', 
     149:b'\xe2\x80\xa2', 
     150:b'\xe2\x80\x93', 
     151:b'\xe2\x80\x94', 
     152:b'\xcb\x9c', 
     153:b'\xe2\x84\xa2', 
     154:b'\xc5\xa1', 
     155:b'\xe2\x80\xba', 
     156:b'\xc5\x93', 
     158:b'\xc5\xbe', 
     159:b'\xc5\xb8', 
     160:b'\xc2\xa0', 
     161:b'\xc2\xa1', 
     162:b'\xc2\xa2', 
     163:b'\xc2\xa3', 
     164:b'\xc2\xa4', 
     165:b'\xc2\xa5', 
     166:b'\xc2\xa6', 
     167:b'\xc2\xa7', 
     168:b'\xc2\xa8', 
     169:b'\xc2\xa9', 
     170:b'\xc2\xaa', 
     171:b'\xc2\xab', 
     172:b'\xc2\xac', 
     173:b'\xc2\xad', 
     174:b'\xc2\xae', 
     175:b'\xc2\xaf', 
     176:b'\xc2\xb0', 
     177:b'\xc2\xb1', 
     178:b'\xc2\xb2', 
     179:b'\xc2\xb3', 
     180:b'\xc2\xb4', 
     181:b'\xc2\xb5', 
     182:b'\xc2\xb6', 
     183:b'\xc2\xb7', 
     184:b'\xc2\xb8', 
     185:b'\xc2\xb9', 
     186:b'\xc2\xba', 
     187:b'\xc2\xbb', 
     188:b'\xc2\xbc', 
     189:b'\xc2\xbd', 
     190:b'\xc2\xbe', 
     191:b'\xc2\xbf', 
     192:b'\xc3\x80', 
     193:b'\xc3\x81', 
     194:b'\xc3\x82', 
     195:b'\xc3\x83', 
     196:b'\xc3\x84', 
     197:b'\xc3\x85', 
     198:b'\xc3\x86', 
     199:b'\xc3\x87', 
     200:b'\xc3\x88', 
     201:b'\xc3\x89', 
     202:b'\xc3\x8a', 
     203:b'\xc3\x8b', 
     204:b'\xc3\x8c', 
     205:b'\xc3\x8d', 
     206:b'\xc3\x8e', 
     207:b'\xc3\x8f', 
     208:b'\xc3\x90', 
     209:b'\xc3\x91', 
     210:b'\xc3\x92', 
     211:b'\xc3\x93', 
     212:b'\xc3\x94', 
     213:b'\xc3\x95', 
     214:b'\xc3\x96', 
     215:b'\xc3\x97', 
     216:b'\xc3\x98', 
     217:b'\xc3\x99', 
     218:b'\xc3\x9a', 
     219:b'\xc3\x9b', 
     220:b'\xc3\x9c', 
     221:b'\xc3\x9d', 
     222:b'\xc3\x9e', 
     223:b'\xc3\x9f', 
     224:b'\xc3\xa0', 
     225:b'\xa1', 
     226:b'\xc3\xa2', 
     227:b'\xc3\xa3', 
     228:b'\xc3\xa4', 
     229:b'\xc3\xa5', 
     230:b'\xc3\xa6', 
     231:b'\xc3\xa7', 
     232:b'\xc3\xa8', 
     233:b'\xc3\xa9', 
     234:b'\xc3\xaa', 
     235:b'\xc3\xab', 
     236:b'\xc3\xac', 
     237:b'\xc3\xad', 
     238:b'\xc3\xae', 
     239:b'\xc3\xaf', 
     240:b'\xc3\xb0', 
     241:b'\xc3\xb1', 
     242:b'\xc3\xb2', 
     243:b'\xc3\xb3', 
     244:b'\xc3\xb4', 
     245:b'\xc3\xb5', 
     246:b'\xc3\xb6', 
     247:b'\xc3\xb7', 
     248:b'\xc3\xb8', 
     249:b'\xc3\xb9', 
     250:b'\xc3\xba', 
     251:b'\xc3\xbb', 
     252:b'\xc3\xbc', 
     253:b'\xc3\xbd', 
     254:b'\xc3\xbe'}
    MULTIBYTE_MARKERS_AND_SIZES = [
     (194, 223, 2),
     (224, 239, 3),
     (240, 244, 4)]
    FIRST_MULTIBYTE_MARKER = MULTIBYTE_MARKERS_AND_SIZES[0][0]
    LAST_MULTIBYTE_MARKER = MULTIBYTE_MARKERS_AND_SIZES[(-1)][1]

    @classmethod
    def detwingle--- This code section failed: ---

 L. 824         0  LOAD_FAST                'embedded_encoding'
                2  LOAD_METHOD              replace
                4  LOAD_STR                 '_'
                6  LOAD_STR                 '-'
                8  CALL_METHOD_2         2  '2 positional arguments'
               10  LOAD_METHOD              lower
               12  CALL_METHOD_0         0  '0 positional arguments'

 L. 825        14  LOAD_CONST               ('windows-1252', 'windows_1252')
               16  COMPARE_OP               not-in
               18  POP_JUMP_IF_FALSE    28  'to 28'

 L. 826        20  LOAD_GLOBAL              NotImplementedError

 L. 827        22  LOAD_STR                 'Windows-1252 and ISO-8859-1 are the only currently supported embedded encodings.'
               24  CALL_FUNCTION_1       1  '1 positional argument'
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            18  '18'

 L. 830        28  LOAD_FAST                'main_encoding'
               30  LOAD_METHOD              lower
               32  CALL_METHOD_0         0  '0 positional arguments'
               34  LOAD_CONST               ('utf8', 'utf-8')
               36  COMPARE_OP               not-in
               38  POP_JUMP_IF_FALSE    48  'to 48'

 L. 831        40  LOAD_GLOBAL              NotImplementedError

 L. 832        42  LOAD_STR                 'UTF-8 is the only currently supported main encoding.'
               44  CALL_FUNCTION_1       1  '1 positional argument'
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            38  '38'

 L. 834        48  BUILD_LIST_0          0 
               50  STORE_FAST               'byte_chunks'

 L. 836        52  LOAD_CONST               0
               54  STORE_FAST               'chunk_start'

 L. 837        56  LOAD_CONST               0
               58  STORE_FAST               'pos'

 L. 838        60  SETUP_LOOP          248  'to 248'
               62  LOAD_FAST                'pos'
               64  LOAD_GLOBAL              len
               66  LOAD_FAST                'in_bytes'
               68  CALL_FUNCTION_1       1  '1 positional argument'
               70  COMPARE_OP               <
               72  POP_JUMP_IF_FALSE   246  'to 246'

 L. 839        74  LOAD_FAST                'in_bytes'
               76  LOAD_FAST                'pos'
               78  BINARY_SUBSCR    
               80  STORE_FAST               'byte'

 L. 840        82  LOAD_GLOBAL              isinstance
               84  LOAD_FAST                'byte'
               86  LOAD_GLOBAL              int
               88  CALL_FUNCTION_2       2  '2 positional arguments'
               90  POP_JUMP_IF_TRUE    100  'to 100'

 L. 842        92  LOAD_GLOBAL              ord
               94  LOAD_FAST                'byte'
               96  CALL_FUNCTION_1       1  '1 positional argument'
               98  STORE_FAST               'byte'
            100_0  COME_FROM            90  '90'

 L. 843       100  LOAD_FAST                'byte'
              102  LOAD_FAST                'cls'
              104  LOAD_ATTR                FIRST_MULTIBYTE_MARKER
              106  COMPARE_OP               >=
              108  POP_JUMP_IF_FALSE   170  'to 170'

 L. 844       110  LOAD_FAST                'byte'
              112  LOAD_FAST                'cls'
              114  LOAD_ATTR                LAST_MULTIBYTE_MARKER
              116  COMPARE_OP               <=
              118  POP_JUMP_IF_FALSE   170  'to 170'

 L. 847       120  SETUP_LOOP          244  'to 244'
              122  LOAD_FAST                'cls'
              124  LOAD_ATTR                MULTIBYTE_MARKERS_AND_SIZES
              126  GET_ITER         
            128_0  COME_FROM           152  '152'
            128_1  COME_FROM           144  '144'
              128  FOR_ITER            166  'to 166'
              130  UNPACK_SEQUENCE_3     3 
              132  STORE_FAST               'start'
              134  STORE_FAST               'end'
              136  STORE_FAST               'size'

 L. 848       138  LOAD_FAST                'byte'
              140  LOAD_FAST                'start'
              142  COMPARE_OP               >=
              144  POP_JUMP_IF_FALSE   128  'to 128'
              146  LOAD_FAST                'byte'
              148  LOAD_FAST                'end'
              150  COMPARE_OP               <=
              152  POP_JUMP_IF_FALSE   128  'to 128'

 L. 849       154  LOAD_FAST                'pos'
              156  LOAD_FAST                'size'
              158  INPLACE_ADD      
              160  STORE_FAST               'pos'

 L. 850       162  BREAK_LOOP       
              164  JUMP_BACK           128  'to 128'
              166  POP_BLOCK        
              168  JUMP_BACK            62  'to 62'
            170_0  COME_FROM           118  '118'
            170_1  COME_FROM           108  '108'

 L. 851       170  LOAD_FAST                'byte'
              172  LOAD_CONST               128
              174  COMPARE_OP               >=
              176  POP_JUMP_IF_FALSE   236  'to 236'
              178  LOAD_FAST                'byte'
              180  LOAD_FAST                'cls'
              182  LOAD_ATTR                WINDOWS_1252_TO_UTF8
              184  COMPARE_OP               in
              186  POP_JUMP_IF_FALSE   236  'to 236'

 L. 854       188  LOAD_FAST                'byte_chunks'
              190  LOAD_METHOD              append
              192  LOAD_FAST                'in_bytes'
              194  LOAD_FAST                'chunk_start'
              196  LOAD_FAST                'pos'
              198  BUILD_SLICE_2         2 
              200  BINARY_SUBSCR    
              202  CALL_METHOD_1         1  '1 positional argument'
              204  POP_TOP          

 L. 858       206  LOAD_FAST                'byte_chunks'
              208  LOAD_METHOD              append
              210  LOAD_FAST                'cls'
              212  LOAD_ATTR                WINDOWS_1252_TO_UTF8
              214  LOAD_FAST                'byte'
              216  BINARY_SUBSCR    
              218  CALL_METHOD_1         1  '1 positional argument'
              220  POP_TOP          

 L. 859       222  LOAD_FAST                'pos'
              224  LOAD_CONST               1
              226  INPLACE_ADD      
              228  STORE_FAST               'pos'

 L. 860       230  LOAD_FAST                'pos'
              232  STORE_FAST               'chunk_start'
              234  JUMP_BACK            62  'to 62'
            236_0  COME_FROM           186  '186'
            236_1  COME_FROM           176  '176'

 L. 863       236  LOAD_FAST                'pos'
              238  LOAD_CONST               1
              240  INPLACE_ADD      
              242  STORE_FAST               'pos'
            244_0  COME_FROM_LOOP      120  '120'
              244  JUMP_BACK            62  'to 62'
            246_0  COME_FROM            72  '72'
              246  POP_BLOCK        
            248_0  COME_FROM_LOOP       60  '60'

 L. 864       248  LOAD_FAST                'chunk_start'
              250  LOAD_CONST               0
              252  COMPARE_OP               ==
          254_256  POP_JUMP_IF_FALSE   262  'to 262'

 L. 866       258  LOAD_FAST                'in_bytes'
              260  RETURN_VALUE     
            262_0  COME_FROM           254  '254'

 L. 869       262  LOAD_FAST                'byte_chunks'
              264  LOAD_METHOD              append
              266  LOAD_FAST                'in_bytes'
              268  LOAD_FAST                'chunk_start'
              270  LOAD_CONST               None
              272  BUILD_SLICE_2         2 
              274  BINARY_SUBSCR    
              276  CALL_METHOD_1         1  '1 positional argument'
              278  POP_TOP          

 L. 870       280  LOAD_CONST               b''
              282  LOAD_METHOD              join
              284  LOAD_FAST                'byte_chunks'
              286  CALL_METHOD_1         1  '1 positional argument'
              288  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 246_0