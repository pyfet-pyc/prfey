# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.11 (default, Sep  3 2021, 20:46:09) 
# [GCC 10.2.1 20210110]
# Embedded file name: email\charset.py
__all__ = [
 'Charset',
 'add_alias',
 'add_charset',
 'add_codec']
from functools import partial
import email.base64mime, email.quoprimime
from email import errors
from email.encoders import encode_7or8bit
QP = 1
BASE64 = 2
SHORTEST = 3
RFC2047_CHROME_LEN = 7
DEFAULT_CHARSET = 'us-ascii'
UNKNOWN8BIT = 'unknown-8bit'
EMPTYSTRING = ''
CHARSETS = {'iso-8859-1':(
  QP, QP, None), 
 'iso-8859-2':(
  QP, QP, None), 
 'iso-8859-3':(
  QP, QP, None), 
 'iso-8859-4':(
  QP, QP, None), 
 'iso-8859-9':(
  QP, QP, None), 
 'iso-8859-10':(
  QP, QP, None), 
 'iso-8859-13':(
  QP, QP, None), 
 'iso-8859-14':(
  QP, QP, None), 
 'iso-8859-15':(
  QP, QP, None), 
 'iso-8859-16':(
  QP, QP, None), 
 'windows-1252':(
  QP, QP, None), 
 'viscii':(
  QP, QP, None), 
 'us-ascii':(None, None, None), 
 'big5':(
  BASE64, BASE64, None), 
 'gb2312':(
  BASE64, BASE64, None), 
 'euc-jp':(
  BASE64, None, 'iso-2022-jp'), 
 'shift_jis':(
  BASE64, None, 'iso-2022-jp'), 
 'iso-2022-jp':(
  BASE64, None, None), 
 'koi8-r':(
  BASE64, BASE64, None), 
 'utf-8':(
  SHORTEST, BASE64, 'utf-8')}
ALIASES = {'latin_1':'iso-8859-1', 
 'latin-1':'iso-8859-1', 
 'latin_2':'iso-8859-2', 
 'latin-2':'iso-8859-2', 
 'latin_3':'iso-8859-3', 
 'latin-3':'iso-8859-3', 
 'latin_4':'iso-8859-4', 
 'latin-4':'iso-8859-4', 
 'latin_5':'iso-8859-9', 
 'latin-5':'iso-8859-9', 
 'latin_6':'iso-8859-10', 
 'latin-6':'iso-8859-10', 
 'latin_7':'iso-8859-13', 
 'latin-7':'iso-8859-13', 
 'latin_8':'iso-8859-14', 
 'latin-8':'iso-8859-14', 
 'latin_9':'iso-8859-15', 
 'latin-9':'iso-8859-15', 
 'latin_10':'iso-8859-16', 
 'latin-10':'iso-8859-16', 
 'cp949':'ks_c_5601-1987', 
 'euc_jp':'euc-jp', 
 'euc_kr':'euc-kr', 
 'ascii':'us-ascii'}
CODEC_MAP = {'gb2312':'eucgb2312_cn', 
 'big5':'big5_tw', 
 'us-ascii':None}

def add_charset(charset, header_enc=None, body_enc=None, output_charset=None):
    """Add character set properties to the global registry.

    charset is the input character set, and must be the canonical name of a
    character set.

    Optional header_enc and body_enc is either Charset.QP for
    quoted-printable, Charset.BASE64 for base64 encoding, Charset.SHORTEST for
    the shortest of qp or base64 encoding, or None for no encoding.  SHORTEST
    is only valid for header_enc.  It describes how message headers and
    message bodies in the input charset are to be encoded.  Default is no
    encoding.

    Optional output_charset is the character set that the output should be
    in.  Conversions will proceed from input charset, to Unicode, to the
    output charset when the method Charset.convert() is called.  The default
    is to output in the same character set as the input.

    Both input_charset and output_charset must have Unicode codec entries in
    the module's charset-to-codec mapping; use add_codec(charset, codecname)
    to add codecs the module does not know about.  See the codecs module's
    documentation for more information.
    """
    if body_enc == SHORTEST:
        raise ValueError('SHORTEST not allowed for body_enc')
    CHARSETS[charset] = (
     header_enc, body_enc, output_charset)


def add_alias(alias, canonical):
    """Add a character set alias.

    alias is the alias name, e.g. latin-1
    canonical is the character set's canonical name, e.g. iso-8859-1
    """
    ALIASES[alias] = canonical


def add_codec(charset, codecname):
    """Add a codec that map characters in the given charset to/from Unicode.

    charset is the canonical name of a character set.  codecname is the name
    of a Python codec, as appropriate for the second argument to the unicode()
    built-in, or to the encode() method of a Unicode string.
    """
    CODEC_MAP[charset] = codecname


def _encode(string, codec):
    if codec == UNKNOWN8BIT:
        return string.encode('ascii', 'surrogateescape')
    return string.encode(codec)


class Charset:
    __doc__ = "Map character sets to their email properties.\n\n    This class provides information about the requirements imposed on email\n    for a specific character set.  It also provides convenience routines for\n    converting between character sets, given the availability of the\n    applicable codecs.  Given a character set, it will do its best to provide\n    information on how to use that character set in an email in an\n    RFC-compliant way.\n\n    Certain character sets must be encoded with quoted-printable or base64\n    when used in email headers or bodies.  Certain character sets must be\n    converted outright, and are not allowed in email.  Instances of this\n    module expose the following information about a character set:\n\n    input_charset: The initial character set specified.  Common aliases\n                   are converted to their `official' email names (e.g. latin_1\n                   is converted to iso-8859-1).  Defaults to 7-bit us-ascii.\n\n    header_encoding: If the character set must be encoded before it can be\n                     used in an email header, this attribute will be set to\n                     Charset.QP (for quoted-printable), Charset.BASE64 (for\n                     base64 encoding), or Charset.SHORTEST for the shortest of\n                     QP or BASE64 encoding.  Otherwise, it will be None.\n\n    body_encoding: Same as header_encoding, but describes the encoding for the\n                   mail message's body, which indeed may be different than the\n                   header encoding.  Charset.SHORTEST is not allowed for\n                   body_encoding.\n\n    output_charset: Some character sets must be converted before they can be\n                    used in email headers or bodies.  If the input_charset is\n                    one of them, this attribute will contain the name of the\n                    charset output will be converted to.  Otherwise, it will\n                    be None.\n\n    input_codec: The name of the Python codec used to convert the\n                 input_charset to Unicode.  If no conversion codec is\n                 necessary, this attribute will be None.\n\n    output_codec: The name of the Python codec used to convert Unicode\n                  to the output_charset.  If no conversion codec is necessary,\n                  this attribute will have the same value as the input_codec.\n    "

    def __init__(self, input_charset=DEFAULT_CHARSET):
        try:
            if isinstance(input_charset, str):
                input_charset.encode('ascii')
            else:
                input_charset = str(input_charset, 'ascii')
        except UnicodeError:
            raise errors.CharsetError(input_charset)

        input_charset = input_charset.lower()
        self.input_charset = ALIASES.get(input_charset, input_charset)
        henc, benc, conv = CHARSETS.get(self.input_charset, (
         SHORTEST, BASE64, None))
        if not conv:
            conv = self.input_charset
        self.header_encoding = henc
        self.body_encoding = benc
        self.output_charset = ALIASES.get(conv, conv)
        self.input_codec = CODEC_MAP.get(self.input_charset, self.input_charset)
        self.output_codec = CODEC_MAP.get(self.output_charset, self.output_charset)

    def __str__(self):
        return self.input_charset.lower()

    __repr__ = __str__

    def __eq__(self, other):
        return str(self) == str(other).lower()

    def get_body_encoding(self):
        """Return the content-transfer-encoding used for body encoding.

        This is either the string `quoted-printable' or `base64' depending on
        the encoding used, or it is a function in which case you should call
        the function with a single argument, the Message object being
        encoded.  The function should then set the Content-Transfer-Encoding
        header itself to whatever is appropriate.

        Returns "quoted-printable" if self.body_encoding is QP.
        Returns "base64" if self.body_encoding is BASE64.
        Returns conversion function otherwise.
        """
        assert self.body_encoding != SHORTEST
        if self.body_encoding == QP:
            return 'quoted-printable'
        if self.body_encoding == BASE64:
            return 'base64'
        return encode_7or8bit

    def get_output_charset(self):
        """Return the output character set.

        This is self.output_charset if that is not None, otherwise it is
        self.input_charset.
        """
        return self.output_charset or self.input_charset

    def header_encode(self, string):
        """Header-encode a string by converting it first to bytes.

        The type of encoding (base64 or quoted-printable) will be based on
        this charset's `header_encoding`.

        :param string: A unicode string for the header.  It must be possible
            to encode this string to bytes using the character set's
            output codec.
        :return: The encoded string, with RFC 2047 chrome.
        """
        codec = self.output_codec or 'us-ascii'
        header_bytes = _encode(string, codec)
        encoder_module = self._get_encoder(header_bytes)
        if encoder_module is None:
            return string
        return encoder_module.header_encode(header_bytes, codec)

    def header_encode_lines--- This code section failed: ---

 L. 318         0  LOAD_FAST                'self'
                2  LOAD_ATTR                output_codec
                4  JUMP_IF_TRUE_OR_POP     8  'to 8'
                6  LOAD_STR                 'us-ascii'
              8_0  COME_FROM             4  '4'
                8  STORE_FAST               'codec'

 L. 319        10  LOAD_GLOBAL              _encode
               12  LOAD_FAST                'string'
               14  LOAD_FAST                'codec'
               16  CALL_FUNCTION_2       2  '2 positional arguments'
               18  STORE_FAST               'header_bytes'

 L. 320        20  LOAD_FAST                'self'
               22  LOAD_METHOD              _get_encoder
               24  LOAD_FAST                'header_bytes'
               26  CALL_METHOD_1         1  '1 positional argument'
               28  STORE_FAST               'encoder_module'

 L. 321        30  LOAD_GLOBAL              partial
               32  LOAD_FAST                'encoder_module'
               34  LOAD_ATTR                header_encode
               36  LOAD_FAST                'codec'
               38  LOAD_CONST               ('charset',)
               40  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               42  STORE_FAST               'encoder'

 L. 324        44  LOAD_FAST                'self'
               46  LOAD_METHOD              get_output_charset
               48  CALL_METHOD_0         0  '0 positional arguments'
               50  STORE_FAST               'charset'

 L. 325        52  LOAD_GLOBAL              len
               54  LOAD_FAST                'charset'
               56  CALL_FUNCTION_1       1  '1 positional argument'
               58  LOAD_GLOBAL              RFC2047_CHROME_LEN
               60  BINARY_ADD       
               62  STORE_FAST               'extra'

 L. 337        64  BUILD_LIST_0          0 
               66  STORE_FAST               'lines'

 L. 338        68  BUILD_LIST_0          0 
               70  STORE_FAST               'current_line'

 L. 339        72  LOAD_GLOBAL              next
               74  LOAD_FAST                'maxlengths'
               76  CALL_FUNCTION_1       1  '1 positional argument'
               78  LOAD_FAST                'extra'
               80  BINARY_SUBTRACT  
               82  STORE_FAST               'maxlen'

 L. 340        84  SETUP_LOOP          234  'to 234'
               86  LOAD_FAST                'string'
               88  GET_ITER         
             90_0  COME_FROM           230  '230'
             90_1  COME_FROM           136  '136'
               90  FOR_ITER            232  'to 232'
               92  STORE_FAST               'character'

 L. 341        94  LOAD_FAST                'current_line'
               96  LOAD_METHOD              append
               98  LOAD_FAST                'character'
              100  CALL_METHOD_1         1  '1 positional argument'
              102  POP_TOP          

 L. 342       104  LOAD_GLOBAL              EMPTYSTRING
              106  LOAD_METHOD              join
              108  LOAD_FAST                'current_line'
              110  CALL_METHOD_1         1  '1 positional argument'
              112  STORE_FAST               'this_line'

 L. 343       114  LOAD_FAST                'encoder_module'
              116  LOAD_METHOD              header_length
              118  LOAD_GLOBAL              _encode
              120  LOAD_FAST                'this_line'
              122  LOAD_FAST                'charset'
              124  CALL_FUNCTION_2       2  '2 positional arguments'
              126  CALL_METHOD_1         1  '1 positional argument'
              128  STORE_FAST               'length'

 L. 344       130  LOAD_FAST                'length'
              132  LOAD_FAST                'maxlen'
              134  COMPARE_OP               >
              136  POP_JUMP_IF_FALSE_BACK    90  'to 90'

 L. 346       138  LOAD_FAST                'current_line'
              140  LOAD_METHOD              pop
              142  CALL_METHOD_0         0  '0 positional arguments'
              144  POP_TOP          

 L. 348       146  LOAD_FAST                'lines'
              148  POP_JUMP_IF_TRUE    166  'to 166'
              150  LOAD_FAST                'current_line'
              152  POP_JUMP_IF_TRUE    166  'to 166'

 L. 349       154  LOAD_FAST                'lines'
              156  LOAD_METHOD              append
              158  LOAD_CONST               None
              160  CALL_METHOD_1         1  '1 positional argument'
              162  POP_TOP          
              164  JUMP_FORWARD        212  'to 212'
            166_0  COME_FROM           152  '152'
            166_1  COME_FROM           148  '148'

 L. 351       166  LOAD_FAST                'lines'
              168  POP_JUMP_IF_FALSE   174  'to 174'
              170  LOAD_STR                 ' '
              172  JUMP_FORWARD        176  'to 176'
            174_0  COME_FROM           168  '168'
              174  LOAD_STR                 ''
            176_0  COME_FROM           172  '172'
              176  STORE_FAST               'separator'

 L. 352       178  LOAD_GLOBAL              EMPTYSTRING
              180  LOAD_METHOD              join
              182  LOAD_FAST                'current_line'
              184  CALL_METHOD_1         1  '1 positional argument'
              186  STORE_FAST               'joined_line'

 L. 353       188  LOAD_GLOBAL              _encode
              190  LOAD_FAST                'joined_line'
              192  LOAD_FAST                'codec'
              194  CALL_FUNCTION_2       2  '2 positional arguments'
              196  STORE_FAST               'header_bytes'

 L. 354       198  LOAD_FAST                'lines'
              200  LOAD_METHOD              append
              202  LOAD_FAST                'encoder'
              204  LOAD_FAST                'header_bytes'
              206  CALL_FUNCTION_1       1  '1 positional argument'
              208  CALL_METHOD_1         1  '1 positional argument'
              210  POP_TOP          
            212_0  COME_FROM           164  '164'

 L. 355       212  LOAD_FAST                'character'
              214  BUILD_LIST_1          1 
              216  STORE_FAST               'current_line'

 L. 356       218  LOAD_GLOBAL              next
              220  LOAD_FAST                'maxlengths'
              222  CALL_FUNCTION_1       1  '1 positional argument'
              224  LOAD_FAST                'extra'
              226  BINARY_SUBTRACT  
              228  STORE_FAST               'maxlen'
              230  JUMP_BACK            90  'to 90'
              232  POP_BLOCK        
            234_0  COME_FROM_LOOP       84  '84'

 L. 357       234  LOAD_GLOBAL              EMPTYSTRING
              236  LOAD_METHOD              join
              238  LOAD_FAST                'current_line'
              240  CALL_METHOD_1         1  '1 positional argument'
              242  STORE_FAST               'joined_line'

 L. 358       244  LOAD_GLOBAL              _encode
              246  LOAD_FAST                'joined_line'
              248  LOAD_FAST                'codec'
              250  CALL_FUNCTION_2       2  '2 positional arguments'
              252  STORE_FAST               'header_bytes'

 L. 359       254  LOAD_FAST                'lines'
              256  LOAD_METHOD              append
              258  LOAD_FAST                'encoder'
              260  LOAD_FAST                'header_bytes'
              262  CALL_FUNCTION_1       1  '1 positional argument'
              264  CALL_METHOD_1         1  '1 positional argument'
              266  POP_TOP          

 L. 360       268  LOAD_FAST                'lines'
              270  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 212

    def _get_encoder(self, header_bytes):
        if self.header_encoding == BASE64:
            return email.base64mime
        if self.header_encoding == QP:
            return email.quoprimime
        if self.header_encoding == SHORTEST:
            len64 = email.base64mime.header_length(header_bytes)
            lenqp = email.quoprimime.header_length(header_bytes)
            if len64 < lenqp:
                return email.base64mime
            return email.quoprimime
        else:
            return

    def body_encode(self, string):
        """Body-encode a string by converting it first to bytes.

        The type of encoding (base64 or quoted-printable) will be based on
        self.body_encoding.  If body_encoding is None, we assume the
        output charset is a 7bit encoding, so re-encoding the decoded
        string using the ascii codec produces the correct string version
        of the content.
        """
        if not string:
            return string
        if self.body_encoding is BASE64:
            if isinstance(string, str):
                string = string.encode(self.output_charset)
            return email.base64mime.body_encode(string)
        if self.body_encoding is QP:
            if isinstance(string, str):
                string = string.encode(self.output_charset)
            string = string.decode('latin1')
            return email.quoprimime.body_encode(string)
        if isinstance(string, str):
            string = string.encode(self.output_charset).decode('ascii')
        return string