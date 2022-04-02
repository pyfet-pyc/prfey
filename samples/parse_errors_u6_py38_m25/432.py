# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: email\quoprimime.py
"""Quoted-printable content transfer encoding per RFCs 2045-2047.

This module handles the content transfer encoding method defined in RFC 2045
to encode US ASCII-like 8-bit data called `quoted-printable'.  It is used to
safely encode text that is in a character set similar to the 7-bit US ASCII
character set, but that includes some 8-bit characters that are normally not
allowed in email bodies or headers.

Quoted-printable is very space-inefficient for encoding binary files; use the
email.base64mime module for that instead.

This module provides an interface to encode and decode both headers and bodies
with quoted-printable encoding.

RFC 2045 defines a method for including character set information in an
`encoded-word' in a header.  This method is commonly used for 8-bit real names
in To:/From:/Cc: etc. fields, as well as Subject: lines.

This module does not do the line wrapping or end-of-line character
conversion necessary for proper internationalized headers; it only
does dumb encoding and decoding.  To deal with the various line
wrapping issues, use the email.header module.
"""
__all__ = [
 'body_decode',
 'body_encode',
 'body_length',
 'decode',
 'decodestring',
 'header_decode',
 'header_encode',
 'header_length',
 'quote',
 'unquote']
import re
from string import ascii_letters, digits, hexdigits
CRLF = '\r\n'
NL = '\n'
EMPTYSTRING = ''
_QUOPRI_MAP = ['=%02X' % c for c in range(256)]
_QUOPRI_HEADER_MAP = _QUOPRI_MAP[:]
_QUOPRI_BODY_MAP = _QUOPRI_MAP[:]
for c in b'-!*+/' + ascii_letters.encode('ascii') + digits.encode('ascii'):
    _QUOPRI_HEADER_MAP[c] = chr(c)
else:
    _QUOPRI_HEADER_MAP[ord(' ')] = '_'
    for c in b' !"#$%&\'()*+,-./0123456789:;<>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\t':
        _QUOPRI_BODY_MAP[c] = chr(c)
    else:

        def header_check(octet):
            """Return True if the octet should be escaped with header quopri."""
            return chr(octet) != _QUOPRI_HEADER_MAP[octet]


        def body_check(octet):
            """Return True if the octet should be escaped with body quopri."""
            return chr(octet) != _QUOPRI_BODY_MAP[octet]


        def header_length(bytearray):
            """Return a header quoted-printable encoding length.

    Note that this does not include any RFC 2047 chrome added by
    `header_encode()`.

    :param bytearray: An array of bytes (a.k.a. octets).
    :return: The length in bytes of the byte array when it is encoded with
        quoted-printable for headers.
    """
            return sum((len(_QUOPRI_HEADER_MAP[octet]) for octet in bytearray))


        def body_length(bytearray):
            """Return a body quoted-printable encoding length.

    :param bytearray: An array of bytes (a.k.a. octets).
    :return: The length in bytes of the byte array when it is encoded with
        quoted-printable for bodies.
    """
            return sum((len(_QUOPRI_BODY_MAP[octet]) for octet in bytearray))


        def _max_append(L, s, maxlen, extra=''):
            if not isinstance(s, str):
                s = chr(s)
            elif not L:
                L.append(s.lstrip())
            else:
                if len(L[(-1)]) + len(s) <= maxlen:
                    L[(-1)] += extra + s
                else:
                    L.append(s.lstrip())


        def unquote(s):
            """Turn a string in the form =AB to the ASCII character with value 0xab"""
            return chr(int(s[1:3], 16))


        def quote(c):
            return _QUOPRI_MAP[ord(c)]


        def header_encode(header_bytes, charset='iso-8859-1'):
            """Encode a single header line with quoted-printable (like) encoding.

    Defined in RFC 2045, this `Q' encoding is similar to quoted-printable, but
    used specifically for email header fields to allow charsets with mostly 7
    bit characters (and some 8 bit) to remain more or less readable in non-RFC
    2045 aware mail clients.

    charset names the character set to use in the RFC 2046 header.  It
    defaults to iso-8859-1.
    """
            if not header_bytes:
                return ''
            encoded = header_bytes.decode('latin1').translate(_QUOPRI_HEADER_MAP)
            return '=?%s?q?%s?=' % (charset, encoded)


        _QUOPRI_BODY_ENCODE_MAP = _QUOPRI_BODY_MAP[:]
        for c in b'\r\n':
            _QUOPRI_BODY_ENCODE_MAP[c] = chr(c)
        else:

            def body_encode(body, maxlinelen=76, eol=NL):
                r"""Encode with quoted-printable, wrapping at maxlinelen characters.

    Each line of encoded text will end with eol, which defaults to "\n".  Set
    this to "\r\n" if you will be using the result of this function directly
    in an email.

    Each line will be wrapped at, at most, maxlinelen characters before the
    eol string (maxlinelen defaults to 76 characters, the maximum value
    permitted by RFC 2045).  Long lines will have the 'soft line break'
    quoted-printable character "=" appended to them, so the decoded text will
    be identical to the original text.

    The minimum maxlinelen is 4 to have room for a quoted character ("=XX")
    followed by a soft line break.  Smaller values will generate a
    ValueError.

    """
                if maxlinelen < 4:
                    raise ValueError('maxlinelen must be at least 4')
                else:
                    return body or body
                body = body.translate(_QUOPRI_BODY_ENCODE_MAP)
                soft_break = '=' + eol
                maxlinelen1 = maxlinelen - 1
                encoded_body = []
                append = encoded_body.append
                for line in body.splitlines():
                    start = 0
                    laststart = len(line) - 1 - maxlinelen
                    if start <= laststart:
                        stop = start + maxlinelen1
                        if line[(stop - 2)] == '=':
                            append(line[start:stop - 1])
                            start = stop - 2
                    elif line[(stop - 1)] == '=':
                        append(line[start:stop])
                        start = stop - 1
                    else:
                        append(line[start:stop] + '=')
                        start = stop
                    if line:
                        if line[(-1)] in ' \t':
                            room = start - laststart
                            if room >= 3:
                                q = quote(line[(-1)])
                            else:
                                if room == 2:
                                    q = line[(-1)] + soft_break
                                else:
                                    q = soft_break + quote(line[(-1)])
                            append(line[start:-1] + q)
                    append(line[start:])
                else:
                    if body[(-1)] in CRLF:
                        append('')
                    return eol.join(encoded_body)


            def decode--- This code section failed: ---

 L. 236         0  LOAD_FAST                'encoded'
                2  POP_JUMP_IF_TRUE      8  'to 8'

 L. 237         4  LOAD_FAST                'encoded'
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L. 241         8  LOAD_STR                 ''
               10  STORE_FAST               'decoded'

 L. 243        12  LOAD_FAST                'encoded'
               14  LOAD_METHOD              splitlines
               16  CALL_METHOD_0         0  ''
               18  GET_ITER         
             20_0  COME_FROM            64  '64'
               20  FOR_ITER            238  'to 238'
               22  STORE_FAST               'line'

 L. 244        24  LOAD_FAST                'line'
               26  LOAD_METHOD              rstrip
               28  CALL_METHOD_0         0  ''
               30  STORE_FAST               'line'

 L. 245        32  LOAD_FAST                'line'
               34  POP_JUMP_IF_TRUE     46  'to 46'

 L. 246        36  LOAD_FAST                'decoded'
               38  LOAD_FAST                'eol'
               40  INPLACE_ADD      
               42  STORE_FAST               'decoded'

 L. 247        44  JUMP_BACK            20  'to 20'
             46_0  COME_FROM            34  '34'

 L. 249        46  LOAD_CONST               0
               48  STORE_FAST               'i'

 L. 250        50  LOAD_GLOBAL              len
               52  LOAD_FAST                'line'
               54  CALL_FUNCTION_1       1  ''
               56  STORE_FAST               'n'
             58_0  COME_FROM           224  '224'

 L. 251        58  LOAD_FAST                'i'
               60  LOAD_FAST                'n'
               62  COMPARE_OP               <
               64  POP_JUMP_IF_FALSE    20  'to 20'

 L. 252        66  LOAD_FAST                'line'
               68  LOAD_FAST                'i'
               70  BINARY_SUBSCR    
               72  STORE_FAST               'c'

 L. 253        74  LOAD_FAST                'c'
               76  LOAD_STR                 '='
               78  COMPARE_OP               !=
               80  POP_JUMP_IF_FALSE   100  'to 100'

 L. 254        82  LOAD_FAST                'decoded'
               84  LOAD_FAST                'c'
               86  INPLACE_ADD      
               88  STORE_FAST               'decoded'

 L. 255        90  LOAD_FAST                'i'
               92  LOAD_CONST               1
               94  INPLACE_ADD      
               96  STORE_FAST               'i'
               98  JUMP_FORWARD        218  'to 218'
            100_0  COME_FROM            80  '80'

 L. 258       100  LOAD_FAST                'i'
              102  LOAD_CONST               1
              104  BINARY_ADD       
              106  LOAD_FAST                'n'
              108  COMPARE_OP               ==
              110  POP_JUMP_IF_FALSE   124  'to 124'

 L. 259       112  LOAD_FAST                'i'
              114  LOAD_CONST               1
              116  INPLACE_ADD      
              118  STORE_FAST               'i'

 L. 260       120  JUMP_BACK            58  'to 58'
              122  JUMP_FORWARD        218  'to 218'
            124_0  COME_FROM           110  '110'

 L. 262       124  LOAD_FAST                'i'
              126  LOAD_CONST               2
              128  BINARY_ADD       
              130  LOAD_FAST                'n'
              132  COMPARE_OP               <
              134  POP_JUMP_IF_FALSE   202  'to 202'
              136  LOAD_FAST                'line'
              138  LOAD_FAST                'i'
              140  LOAD_CONST               1
              142  BINARY_ADD       
              144  BINARY_SUBSCR    
              146  LOAD_GLOBAL              hexdigits
              148  COMPARE_OP               in
              150  POP_JUMP_IF_FALSE   202  'to 202'
              152  LOAD_FAST                'line'
              154  LOAD_FAST                'i'
              156  LOAD_CONST               2
              158  BINARY_ADD       
              160  BINARY_SUBSCR    
              162  LOAD_GLOBAL              hexdigits
              164  COMPARE_OP               in
              166  POP_JUMP_IF_FALSE   202  'to 202'

 L. 263       168  LOAD_FAST                'decoded'
              170  LOAD_GLOBAL              unquote
              172  LOAD_FAST                'line'
              174  LOAD_FAST                'i'
              176  LOAD_FAST                'i'
              178  LOAD_CONST               3
              180  BINARY_ADD       
              182  BUILD_SLICE_2         2 
              184  BINARY_SUBSCR    
              186  CALL_FUNCTION_1       1  ''
              188  INPLACE_ADD      
              190  STORE_FAST               'decoded'

 L. 264       192  LOAD_FAST                'i'
              194  LOAD_CONST               3
              196  INPLACE_ADD      
              198  STORE_FAST               'i'
              200  JUMP_FORWARD        218  'to 218'
            202_0  COME_FROM           166  '166'
            202_1  COME_FROM           150  '150'
            202_2  COME_FROM           134  '134'

 L. 267       202  LOAD_FAST                'decoded'
              204  LOAD_FAST                'c'
              206  INPLACE_ADD      
              208  STORE_FAST               'decoded'

 L. 268       210  LOAD_FAST                'i'
              212  LOAD_CONST               1
              214  INPLACE_ADD      
              216  STORE_FAST               'i'
            218_0  COME_FROM           200  '200'
            218_1  COME_FROM           122  '122'
            218_2  COME_FROM            98  '98'

 L. 270       218  LOAD_FAST                'i'
              220  LOAD_FAST                'n'
              222  COMPARE_OP               ==
              224  POP_JUMP_IF_FALSE    58  'to 58'

 L. 271       226  LOAD_FAST                'decoded'
              228  LOAD_FAST                'eol'
              230  INPLACE_ADD      
              232  STORE_FAST               'decoded'
              234  JUMP_BACK            58  'to 58'
              236  JUMP_BACK            20  'to 20'

 L. 273       238  LOAD_FAST                'encoded'
              240  LOAD_CONST               -1
              242  BINARY_SUBSCR    
              244  LOAD_STR                 '\r\n'
              246  COMPARE_OP               not-in
          248_250  POP_JUMP_IF_FALSE   276  'to 276'
              252  LOAD_FAST                'decoded'
              254  LOAD_METHOD              endswith
              256  LOAD_FAST                'eol'
              258  CALL_METHOD_1         1  ''
          260_262  POP_JUMP_IF_FALSE   276  'to 276'

 L. 274       264  LOAD_FAST                'decoded'
              266  LOAD_CONST               None
              268  LOAD_CONST               -1
              270  BUILD_SLICE_2         2 
              272  BINARY_SUBSCR    
              274  STORE_FAST               'decoded'
            276_0  COME_FROM           260  '260'
            276_1  COME_FROM           248  '248'

 L. 275       276  LOAD_FAST                'decoded'
              278  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 238


            body_decode = decode
            decodestring = decode

            def _unquote_match(match):
                """Turn a match in the form =AB to the ASCII character with value 0xab"""
                s = match.group(0)
                return unquote(s)


            def header_decode(s):
                """Decode a string encoded with RFC 2045 MIME header `Q' encoding.

    This function does not parse a full MIME header value encoded with
    quoted-printable (like =?iso-8859-1?q?Hello_World?=) -- please use
    the high level email.header class for that functionality.
    """
                s = s.replace('_', ' ')
                return re.sub('=[a-fA-F0-9]{2}', _unquote_match, s, flags=(re.ASCII))