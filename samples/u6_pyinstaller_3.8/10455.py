# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: email\_encoded_words.py
""" Routines for manipulating RFC2047 encoded words.

This is currently a package-private API, but will be considered for promotion
to a public API if there is demand.

"""
import re, base64, binascii, functools
from string import ascii_letters, digits
from email import errors
__all__ = [
 'decode_q',
 'encode_q',
 'decode_b',
 'encode_b',
 'len_q',
 'len_b',
 'decode',
 'encode']
_q_byte_subber = functools.partial(re.compile(b'=([a-fA-F0-9]{2})').sub, lambda m: bytes.fromhex(m.group(1).decode()))

def decode_q(encoded):
    encoded = encoded.replace(b'_', b' ')
    return (_q_byte_subber(encoded), [])


class _QByteMap(dict):
    safe = b'-!*+/' + ascii_letters.encode('ascii') + digits.encode('ascii')

    def __missing__(self, key):
        if key in self.safe:
            self[key] = chr(key)
        else:
            self[key] = '={:02X}'.format(key)
        return self[key]


_q_byte_map = _QByteMap()
_q_byte_map[ord(' ')] = '_'

def encode_q(bstring):
    return ''.join((_q_byte_map[x] for x in bstring))


def len_q(bstring):
    return sum((len(_q_byte_map[x]) for x in bstring))


def decode_b--- This code section failed: ---

 L. 103         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'encoded'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_CONST               4
                8  BINARY_MODULO    
               10  STORE_FAST               'pad_err'

 L. 104        12  LOAD_FAST                'pad_err'
               14  POP_JUMP_IF_FALSE    32  'to 32'
               16  LOAD_CONST               b'==='
               18  LOAD_CONST               None
               20  LOAD_CONST               4
               22  LOAD_FAST                'pad_err'
               24  BINARY_SUBTRACT  
               26  BUILD_SLICE_2         2 
               28  BINARY_SUBSCR    
               30  JUMP_FORWARD         34  'to 34'
             32_0  COME_FROM            14  '14'
               32  LOAD_CONST               b''
             34_0  COME_FROM            30  '30'
               34  STORE_FAST               'missing_padding'

 L. 105        36  SETUP_FINALLY        76  'to 76'

 L. 107        38  LOAD_GLOBAL              base64
               40  LOAD_ATTR                b64decode
               42  LOAD_FAST                'encoded'
               44  LOAD_FAST                'missing_padding'
               46  BINARY_ADD       
               48  LOAD_CONST               True
               50  LOAD_CONST               ('validate',)
               52  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 108        54  LOAD_FAST                'pad_err'
               56  POP_JUMP_IF_FALSE    68  'to 68'
               58  LOAD_GLOBAL              errors
               60  LOAD_METHOD              InvalidBase64PaddingDefect
               62  CALL_METHOD_0         0  ''
               64  BUILD_LIST_1          1 
               66  JUMP_FORWARD         70  'to 70'
             68_0  COME_FROM            56  '56'
               68  BUILD_LIST_0          0 
             70_0  COME_FROM            66  '66'

 L. 106        70  BUILD_TUPLE_2         2 
               72  POP_BLOCK        
               74  RETURN_VALUE     
             76_0  COME_FROM_FINALLY    36  '36'

 L. 110        76  DUP_TOP          
               78  LOAD_GLOBAL              binascii
               80  LOAD_ATTR                Error
               82  COMPARE_OP               exception-match
            84_86  POP_JUMP_IF_FALSE   242  'to 242'
               88  POP_TOP          
               90  POP_TOP          
               92  POP_TOP          

 L. 116        94  SETUP_FINALLY       126  'to 126'

 L. 118        96  LOAD_GLOBAL              base64
               98  LOAD_ATTR                b64decode
              100  LOAD_FAST                'encoded'
              102  LOAD_CONST               False
              104  LOAD_CONST               ('validate',)
              106  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 119       108  LOAD_GLOBAL              errors
              110  LOAD_METHOD              InvalidBase64CharactersDefect
              112  CALL_METHOD_0         0  ''
              114  BUILD_LIST_1          1 

 L. 117       116  BUILD_TUPLE_2         2 
              118  POP_BLOCK        
              120  ROT_FOUR         
              122  POP_EXCEPT       
              124  RETURN_VALUE     
            126_0  COME_FROM_FINALLY    94  '94'

 L. 121       126  DUP_TOP          
              128  LOAD_GLOBAL              binascii
              130  LOAD_ATTR                Error
              132  COMPARE_OP               exception-match
              134  POP_JUMP_IF_FALSE   236  'to 236'
              136  POP_TOP          
              138  POP_TOP          
              140  POP_TOP          

 L. 124       142  SETUP_FINALLY       188  'to 188'

 L. 126       144  LOAD_GLOBAL              base64
              146  LOAD_ATTR                b64decode
              148  LOAD_FAST                'encoded'
              150  LOAD_CONST               b'=='
              152  BINARY_ADD       
              154  LOAD_CONST               False
              156  LOAD_CONST               ('validate',)
              158  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 127       160  LOAD_GLOBAL              errors
              162  LOAD_METHOD              InvalidBase64CharactersDefect
              164  CALL_METHOD_0         0  ''

 L. 128       166  LOAD_GLOBAL              errors
              168  LOAD_METHOD              InvalidBase64PaddingDefect
              170  CALL_METHOD_0         0  ''

 L. 127       172  BUILD_LIST_2          2 

 L. 125       174  BUILD_TUPLE_2         2 
              176  POP_BLOCK        
              178  ROT_FOUR         
              180  POP_EXCEPT       
              182  ROT_FOUR         
              184  POP_EXCEPT       
              186  RETURN_VALUE     
            188_0  COME_FROM_FINALLY   142  '142'

 L. 130       188  DUP_TOP          
              190  LOAD_GLOBAL              binascii
              192  LOAD_ATTR                Error
              194  COMPARE_OP               exception-match
              196  POP_JUMP_IF_FALSE   230  'to 230'
              198  POP_TOP          
              200  POP_TOP          
              202  POP_TOP          

 L. 136       204  LOAD_FAST                'encoded'
              206  LOAD_GLOBAL              errors
              208  LOAD_METHOD              InvalidBase64LengthDefect
              210  CALL_METHOD_0         0  ''
              212  BUILD_LIST_1          1 
              214  BUILD_TUPLE_2         2 
              216  ROT_FOUR         
              218  POP_EXCEPT       
              220  ROT_FOUR         
              222  POP_EXCEPT       
              224  ROT_FOUR         
              226  POP_EXCEPT       
              228  RETURN_VALUE     
            230_0  COME_FROM           196  '196'
              230  END_FINALLY      
              232  POP_EXCEPT       
              234  JUMP_FORWARD        238  'to 238'
            236_0  COME_FROM           134  '134'
              236  END_FINALLY      
            238_0  COME_FROM           234  '234'
              238  POP_EXCEPT       
              240  JUMP_FORWARD        244  'to 244'
            242_0  COME_FROM            84  '84'
              242  END_FINALLY      
            244_0  COME_FROM           240  '240'

Parse error at or near `POP_TOP' instruction at offset 90


def encode_b(bstring):
    return base64.b64encode(bstring).decode('ascii')


def len_b(bstring):
    groups_of_3, leftover = divmod(len(bstring), 3)
    return groups_of_3 * 4 + (4 if leftover else 0)


_cte_decoders = {'q':decode_q, 
 'b':decode_b}

def decode(ew):
    r"""Decode encoded word and return (string, charset, lang, defects) tuple.

    An RFC 2047/2243 encoded word has the form:

        =?charset*lang?cte?encoded_string?=

    where '*lang' may be omitted but the other parts may not be.

    This function expects exactly such a string (that is, it does not check the
    syntax and may raise errors if the string is not well formed), and returns
    the encoded_string decoded first from its Content Transfer Encoding and
    then from the resulting bytes into unicode using the specified charset.  If
    the cte-decoded string does not successfully decode using the specified
    character set, a defect is added to the defects list and the unknown octets
    are replaced by the unicode 'unknown' character \uFDFF.

    The specified charset and language are returned.  The default for language,
    which is rarely if ever encountered, is the empty string.

    """
    _, charset, cte, cte_string, _ = ew.split('?')
    charset, _, lang = charset.partition('*')
    cte = cte.lower()
    bstring = cte_string.encode('ascii', 'surrogateescape')
    bstring, defects = _cte_decoders[cte](bstring)
    try:
        string = bstring.decode(charset)
    except UnicodeError:
        defects.append(errors.UndecodableBytesDefect('Encoded word contains bytes not decodable using {} charset'.format(charset)))
        string = bstring.decode(charset, 'surrogateescape')
    except LookupError:
        string = bstring.decode('ascii', 'surrogateescape')
        if charset.lower() != 'unknown-8bit':
            defects.append(errors.CharsetError('Unknown charset {} in encoded word; decoded as unknown bytes'.format(charset)))
    else:
        return (
         string, charset, lang, defects)


_cte_encoders = {'q':encode_q, 
 'b':encode_b}
_cte_encode_length = {'q':len_q, 
 'b':len_b}

def encode(string, charset='utf-8', encoding=None, lang=''):
    """Encode string using the CTE encoding that produces the shorter result.

    Produces an RFC 2047/2243 encoded word of the form:

        =?charset*lang?cte?encoded_string?=

    where '*lang' is omitted unless the 'lang' parameter is given a value.
    Optional argument charset (defaults to utf-8) specifies the charset to use
    to encode the string to binary before CTE encoding it.  Optional argument
    'encoding' is the cte specifier for the encoding that should be used ('q'
    or 'b'); if it is None (the default) the encoding which produces the
    shortest encoded sequence is used, except that 'q' is preferred if it is up
    to five characters longer.  Optional argument 'lang' (default '') gives the
    RFC 2243 language string to specify in the encoded word.

    """
    if charset == 'unknown-8bit':
        bstring = string.encode('ascii', 'surrogateescape')
    else:
        bstring = string.encode(charset)
    if encoding is None:
        qlen = _cte_encode_length['q'](bstring)
        blen = _cte_encode_length['b'](bstring)
        encoding = 'q' if qlen - blen < 5 else 'b'
    encoded = _cte_encoders[encoding](bstring)
    if lang:
        lang = '*' + lang
    return '=?{}{}?{}?{}?='.format(charset, lang, encoding, encoded)