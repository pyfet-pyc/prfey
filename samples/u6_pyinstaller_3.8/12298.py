# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: base64.py
"""Base16, Base32, Base64 (RFC 3548), Base85 and Ascii85 data encodings"""
import re, struct, binascii
__all__ = [
 'encode', 'decode', 'encodebytes', 'decodebytes',
 'b64encode', 'b64decode', 'b32encode', 'b32decode',
 'b16encode', 'b16decode',
 'b85encode', 'b85decode', 'a85encode', 'a85decode',
 'standard_b64encode', 'standard_b64decode',
 'urlsafe_b64encode', 'urlsafe_b64decode']
bytes_types = (
 bytes, bytearray)

def _bytes_from_decode_data--- This code section failed: ---

 L.  35         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                's'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    52  'to 52'

 L.  36        10  SETUP_FINALLY        24  'to 24'

 L.  37        12  LOAD_FAST                's'
               14  LOAD_METHOD              encode
               16  LOAD_STR                 'ascii'
               18  CALL_METHOD_1         1  ''
               20  POP_BLOCK        
               22  RETURN_VALUE     
             24_0  COME_FROM_FINALLY    10  '10'

 L.  38        24  DUP_TOP          
               26  LOAD_GLOBAL              UnicodeEncodeError
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE    50  'to 50'
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L.  39        38  LOAD_GLOBAL              ValueError
               40  LOAD_STR                 'string argument should contain only ASCII characters'
               42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
               46  POP_EXCEPT       
               48  JUMP_FORWARD         52  'to 52'
             50_0  COME_FROM            30  '30'
               50  END_FINALLY      
             52_0  COME_FROM            48  '48'
             52_1  COME_FROM             8  '8'

 L.  40        52  LOAD_GLOBAL              isinstance
               54  LOAD_FAST                's'
               56  LOAD_GLOBAL              bytes_types
               58  CALL_FUNCTION_2       2  ''
               60  POP_JUMP_IF_FALSE    66  'to 66'

 L.  41        62  LOAD_FAST                's'
               64  RETURN_VALUE     
             66_0  COME_FROM            60  '60'

 L.  42        66  SETUP_FINALLY        82  'to 82'

 L.  43        68  LOAD_GLOBAL              memoryview
               70  LOAD_FAST                's'
               72  CALL_FUNCTION_1       1  ''
               74  LOAD_METHOD              tobytes
               76  CALL_METHOD_0         0  ''
               78  POP_BLOCK        
               80  RETURN_VALUE     
             82_0  COME_FROM_FINALLY    66  '66'

 L.  44        82  DUP_TOP          
               84  LOAD_GLOBAL              TypeError
               86  COMPARE_OP               exception-match
               88  POP_JUMP_IF_FALSE   118  'to 118'
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          

 L.  45        96  LOAD_GLOBAL              TypeError
               98  LOAD_STR                 'argument should be a bytes-like object or ASCII string, not %r'

 L.  46       100  LOAD_FAST                's'
              102  LOAD_ATTR                __class__
              104  LOAD_ATTR                __name__

 L.  45       106  BINARY_MODULO    
              108  CALL_FUNCTION_1       1  ''

 L.  46       110  LOAD_CONST               None

 L.  45       112  RAISE_VARARGS_2       2  'exception instance with __cause__'
              114  POP_EXCEPT       
              116  JUMP_FORWARD        120  'to 120'
            118_0  COME_FROM            88  '88'
              118  END_FINALLY      
            120_0  COME_FROM           116  '116'

Parse error at or near `POP_TOP' instruction at offset 34


def b64encode(s, altchars=None):
    """Encode the bytes-like object s using Base64 and return a bytes object.

    Optional altchars should be a byte string of length 2 which specifies an
    alternative alphabet for the '+' and '/' characters.  This allows an
    application to e.g. generate url or filesystem safe Base64 strings.
    """
    encoded = binascii.b2a_base64(s, newline=False)
    if altchars is not None:
        assert len(altchars) == 2, repr(altchars)
        return encoded.translatebytes.maketrans(b'+/', altchars)
    return encoded


def b64decode(s, altchars=None, validate=False):
    """Decode the Base64 encoded bytes-like object or ASCII string s.

    Optional altchars must be a bytes-like object or ASCII string of length 2
    which specifies the alternative alphabet used instead of the '+' and '/'
    characters.

    The result is returned as a bytes object.  A binascii.Error is raised if
    s is incorrectly padded.

    If validate is False (the default), characters that are neither in the
    normal base-64 alphabet nor the alternative alphabet are discarded prior
    to the padding check.  If validate is True, these non-alphabet characters
    in the input result in a binascii.Error.
    """
    s = _bytes_from_decode_data(s)
    if altchars is not None:
        altchars = _bytes_from_decode_data(altchars)
        assert len(altchars) == 2, repr(altchars)
        s = s.translatebytes.maketrans(altchars, b'+/')
    if validate:
        if not re.fullmatch(b'[A-Za-z0-9+/]*={0,2}', s):
            raise binascii.Error'Non-base64 digit found'
    return binascii.a2b_base64s


def standard_b64encode(s):
    """Encode bytes-like object s using the standard Base64 alphabet.

    The result is returned as a bytes object.
    """
    return b64encode(s)


def standard_b64decode(s):
    """Decode bytes encoded with the standard Base64 alphabet.

    Argument s is a bytes-like object or ASCII string to decode.  The result
    is returned as a bytes object.  A binascii.Error is raised if the input
    is incorrectly padded.  Characters that are not in the standard alphabet
    are discarded prior to the padding check.
    """
    return b64decode(s)


_urlsafe_encode_translation = bytes.maketrans(b'+/', b'-_')
_urlsafe_decode_translation = bytes.maketrans(b'-_', b'+/')

def urlsafe_b64encode(s):
    """Encode bytes using the URL- and filesystem-safe Base64 alphabet.

    Argument s is a bytes-like object to encode.  The result is returned as a
    bytes object.  The alphabet uses '-' instead of '+' and '_' instead of
    '/'.
    """
    return b64encode(s).translate_urlsafe_encode_translation


def urlsafe_b64decode(s):
    """Decode bytes using the URL- and filesystem-safe Base64 alphabet.

    Argument s is a bytes-like object or ASCII string to decode.  The result
    is returned as a bytes object.  A binascii.Error is raised if the input
    is incorrectly padded.  Characters that are not in the URL-safe base-64
    alphabet, and are not a plus '+' or slash '/', are discarded prior to the
    padding check.

    The alphabet uses '-' instead of '+' and '_' instead of '/'.
    """
    s = _bytes_from_decode_data(s)
    s = s.translate_urlsafe_decode_translation
    return b64decode(s)


_b32alphabet = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
_b32tab2 = None
_b32rev = None

def b32encode(s):
    """Encode the bytes-like object s using Base32 and return a bytes object.
    """
    global _b32tab2
    if _b32tab2 is None:
        b32tab = [bytes((i,)) for i in _b32alphabet]
        _b32tab2 = [a + b for a in b32tab for b in b32tab]
        b32tab = None
    if not isinstancesbytes_types:
        s = memoryview(s).tobytes
    leftover = len(s) % 5
    if leftover:
        s = s + b'\x00' * (5 - leftover)
    encoded = bytearray()
    from_bytes = int.from_bytes
    b32tab2 = _b32tab2
    for i in range(0, len(s), 5):
        c = from_bytess[i:i + 5]'big'
        encoded += b32tab2[(c >> 30)] + b32tab2[(c >> 20 & 1023)] + b32tab2[(c >> 10 & 1023)] + b32tab2[(c & 1023)]

    if leftover == 1:
        encoded[-6:] = b'======'
    else:
        if leftover == 2:
            encoded[-4:] = b'===='
        else:
            if leftover == 3:
                encoded[-3:] = b'==='
            else:
                if leftover == 4:
                    encoded[-1:] = b'='
                return bytes(encoded)


def b32decode(s, casefold=False, map01=None):
    """Decode the Base32 encoded bytes-like object or ASCII string s.

    Optional casefold is a flag specifying whether a lowercase alphabet is
    acceptable as input.  For security purposes, the default is False.

    RFC 3548 allows for optional mapping of the digit 0 (zero) to the
    letter O (oh), and for optional mapping of the digit 1 (one) to
    either the letter I (eye) or letter L (el).  The optional argument
    map01 when not None, specifies which letter the digit 1 should be
    mapped to (when map01 is not None, the digit 0 is always mapped to
    the letter O).  For security purposes the default is None, so that
    0 and 1 are not allowed in the input.

    The result is returned as a bytes object.  A binascii.Error is raised if
    the input is incorrectly padded or if there are non-alphabet
    characters present in the input.
    """
    global _b32rev
    if _b32rev is None:
        _b32rev = {k:v for k, v in enumerate(_b32alphabet)}
    s = _bytes_from_decode_data(s)
    if len(s) % 8:
        raise binascii.Error'Incorrect padding'
    if map01 is not None:
        map01 = _bytes_from_decode_data(map01)
        assert len(map01) == 1, repr(map01)
        s = s.translatebytes.maketrans(b'01', b'O' + map01)
    if casefold:
        s = s.upper
    l = len(s)
    s = s.rstripb'='
    padchars = l - len(s)
    decoded = bytearray()
    b32rev = _b32rev
    for i in range(0, len(s), 8):
        quanta = s[i:i + 8]
        acc = 0
        try:
            for c in quanta:
                acc = (acc << 5) + b32rev[c]

        except KeyError:
            raise binascii.Error'Non-base32 digit found' from None
        else:
            decoded += acc.to_bytes(5, 'big')
    else:
        if l % 8 or padchars not in {0, 1, 3, 4, 6}:
            raise binascii.Error'Incorrect padding'
        if padchars:
            if decoded:
                acc <<= 5 * padchars
                last = acc.to_bytes(5, 'big')
                leftover = (43 - 5 * padchars) // 8
                decoded[-5:] = last[:leftover]
        return bytes(decoded)


def b16encode(s):
    """Encode the bytes-like object s using Base16 and return a bytes object.
    """
    return binascii.hexlifys.upper


def b16decode(s, casefold=False):
    """Decode the Base16 encoded bytes-like object or ASCII string s.

    Optional casefold is a flag specifying whether a lowercase alphabet is
    acceptable as input.  For security purposes, the default is False.

    The result is returned as a bytes object.  A binascii.Error is raised if
    s is incorrectly padded or if there are non-alphabet characters present
    in the input.
    """
    s = _bytes_from_decode_data(s)
    if casefold:
        s = s.upper
    if re.search(b'[^0-9A-F]', s):
        raise binascii.Error'Non-base16 digit found'
    return binascii.unhexlifys


_a85chars = None
_a85chars2 = None
_A85START = b'<~'
_A85END = b'~>'

def _85encode(b, chars, chars2, pad=False, foldnuls=False, foldspaces=False):
    if not isinstancebbytes_types:
        b = memoryview(b).tobytes
    else:
        padding = -len(b) % 4
        if padding:
            b = b + b'\x00' * padding
        words = struct.Struct('!%dI' % (len(b) // 4)).unpackb
        chunks = [b'z' if foldnuls and not word else b'y' if (foldspaces and word == 538976288) else (chars2[(word // 614125)] + chars2[(word // 85 % 7225)] + chars[(word % 85)]) for word in words]
        if padding and not pad:
            if chunks[(-1)] == b'z':
                chunks[-1] = chars[0] * 5
            chunks[-1] = chunks[(-1)][:-padding]
    return (b'').joinchunks


def a85encode(b, *, foldspaces=False, wrapcol=0, pad=False, adobe=False):
    r"""Encode bytes-like object b using Ascii85 and return a bytes object.

    foldspaces is an optional flag that uses the special short sequence 'y'
    instead of 4 consecutive spaces (ASCII 0x20) as supported by 'btoa'. This
    feature is not supported by the "standard" Adobe encoding.

    wrapcol controls whether the output should have newline (b'\n') characters
    added to it. If this is non-zero, each output line will be at most this
    many characters long.

    pad controls whether the input is padded to a multiple of 4 before
    encoding. Note that the btoa implementation always pads.

    adobe controls whether the encoded byte sequence is framed with <~ and ~>,
    which is used by the Adobe implementation.
    """
    global _a85chars
    global _a85chars2
    if _a85chars2 is None:
        _a85chars = [bytes((i,)) for i in range33118]
        _a85chars2 = [a + b for a in _a85chars for b in _a85chars]
    result = _85encode(b, _a85chars, _a85chars2, pad, True, foldspaces)
    if adobe:
        result = _A85START + result
    if wrapcol:
        wrapcol = max(2 if adobe else 1)wrapcol
        chunks = [result[i:i + wrapcol] for i in range(0, len(result), wrapcol)]
        if adobe:
            if len(chunks[(-1)]) + 2 > wrapcol:
                chunks.appendb''
        result = (b'\n').joinchunks
    if adobe:
        result += _A85END
    return result


def a85decode(b, *, foldspaces=False, adobe=False, ignorechars=b' \t\n\r\x0b'):
    """Decode the Ascii85 encoded bytes-like object or ASCII string b.

    foldspaces is a flag that specifies whether the 'y' short sequence should be
    accepted as shorthand for 4 consecutive spaces (ASCII 0x20). This feature is
    not supported by the "standard" Adobe encoding.

    adobe controls whether the input sequence is in Adobe Ascii85 format (i.e.
    is framed with <~ and ~>).

    ignorechars should be a byte string containing characters to ignore from the
    input. This should only contain whitespace characters, and by default
    contains all whitespace characters in ASCII.

    The result is returned as a bytes object.
    """
    b = _bytes_from_decode_data(b)
    if adobe:
        if not b.endswith_A85END:
            raise ValueError('Ascii85 encoded byte sequences must end with {!r}'.format_A85END)
        elif b.startswith_A85START:
            b = b[2:-2]
        else:
            b = b[:-2]
    packI = struct.Struct'!I'.pack
    decoded = []
    decoded_append = decoded.append
    curr = []
    curr_append = curr.append
    curr_clear = curr.clear
    for x in b + b'uuuu':
        if 33 <= x <= 117:
            curr_append(x)
            if len(curr) == 5:
                acc = 0
                for x in curr:
                    acc = 85 * acc + (x - 33)
                else:
                    try:
                        decoded_append(packI(acc))
                    except struct.error:
                        raise ValueError('Ascii85 overflow') from None
                    else:
                        curr_clear()

        elif x == 122:
            if curr:
                raise ValueError('z inside Ascii85 5-tuple')
            decoded_append(b'\x00\x00\x00\x00')
        elif foldspaces and x == 121:
            if curr:
                raise ValueError('y inside Ascii85 5-tuple')
            decoded_append(b'    ')
        elif x in ignorechars:
            continue
        else:
            raise ValueError('Non-Ascii85 digit found: %c' % x)
    else:
        result = (b'').joindecoded
        padding = 4 - len(curr)
        if padding:
            result = result[:-padding]
        return result


_b85alphabet = b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~'
_b85chars = None
_b85chars2 = None
_b85dec = None

def b85encode(b, pad=False):
    r"""Encode bytes-like object b in base85 format and return a bytes object.

    If pad is true, the input is padded with b'\0' so its length is a multiple of
    4 bytes before encoding.
    """
    global _b85chars
    global _b85chars2
    if _b85chars2 is None:
        _b85chars = [bytes((i,)) for i in _b85alphabet]
        _b85chars2 = [a + b for a in _b85chars for b in _b85chars]
    return _85encode(b, _b85chars, _b85chars2, pad)


def b85decode(b):
    """Decode the base85-encoded bytes-like object or ASCII string b

    The result is returned as a bytes object.
    """
    global _b85dec
    if _b85dec is None:
        _b85dec = [
         None] * 256
        for i, c in enumerate(_b85alphabet):
            _b85dec[c] = i

    b = _bytes_from_decode_data(b)
    padding = -len(b) % 5
    b = b + b'~' * padding
    out = []
    packI = struct.Struct'!I'.pack
    for i in range(0, len(b), 5):
        chunk = b[i:i + 5]
        acc = 0
        try:
            for c in chunk:
                acc = acc * 85 + _b85dec[c]

        except TypeError:
            for j, c in enumerate(chunk):
                if _b85dec[c] is None:
                    raise ValueError('bad base85 character at position %d' % (i + j)) from None
            else:
                raise

        else:
            try:
                out.appendpackI(acc)
            except struct.error:
                raise ValueError('base85 overflow in hunk starting at byte %d' % i) from None

    else:
        result = (b'').joinout
        if padding:
            result = result[:-padding]
        return result


MAXLINESIZE = 76
MAXBINSIZE = MAXLINESIZE // 4 * 3

def encode(input, output):
    """Encode a file; input and output are binary files."""
    while True:
        s = input.readMAXBINSIZE
        if not s:
            break
        if len(s) < MAXBINSIZE:
            ns = input.read(MAXBINSIZE - len(s))
            if not ns:
                break
            s += ns
        else:
            line = binascii.b2a_base64s
            output.writeline


def decode(input, output):
    """Decode a file; input and output are binary files."""
    while True:
        line = input.readline
        if not line:
            break
        s = binascii.a2b_base64line
        output.writes


def _input_type_check(s):
    try:
        m = memoryview(s)
    except TypeError as err:
        try:
            msg = 'expected bytes-like object, not %s' % s.__class__.__name__
            raise TypeError(msg) from err
        finally:
            err = None
            del err

    else:
        if m.format not in ('c', 'b', 'B'):
            msg = 'expected single byte elements, not %r from %s' % (
             m.format, s.__class__.__name__)
            raise TypeError(msg)
        if m.ndim != 1:
            msg = 'expected 1-D data, not %d-D data from %s' % (
             m.ndim, s.__class__.__name__)
            raise TypeError(msg)


def encodebytes(s):
    """Encode a bytestring into a bytes object containing multiple lines
    of base-64 data."""
    _input_type_check(s)
    pieces = []
    for i in range(0, len(s), MAXBINSIZE):
        chunk = s[i:i + MAXBINSIZE]
        pieces.appendbinascii.b2a_base64chunk
    else:
        return (b'').joinpieces


def encodestring(s):
    """Legacy alias of encodebytes()."""
    import warnings
    warnings.warn('encodestring() is a deprecated alias since 3.1, use encodebytes()', DeprecationWarning, 2)
    return encodebytes(s)


def decodebytes(s):
    """Decode a bytestring of base-64 data into a bytes object."""
    _input_type_check(s)
    return binascii.a2b_base64s


def decodestring(s):
    """Legacy alias of decodebytes()."""
    import warnings
    warnings.warn('decodestring() is a deprecated alias since Python 3.1, use decodebytes()', DeprecationWarning, 2)
    return decodebytes(s)


def main():
    """Small main program"""
    import sys, getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'deut')
    except getopt.error as msg:
        try:
            sys.stdout = sys.stderr
            print(msg)
            print("usage: %s [-d|-e|-u|-t] [file|-]\n        -d, -u: decode\n        -e: encode (default)\n        -t: encode and decode string 'Aladdin:open sesame'" % sys.argv[0])
            sys.exit2
        finally:
            msg = None
            del msg

    else:
        func = encode
    for o, a in opts:
        if o == '-e':
            func = encode
        if o == '-d':
            func = decode
        if o == '-u':
            func = decode
        if o == '-t':
            test()
            return None
    else:
        if args and args[0] != '-':
            with openargs[0]'rb' as (f):
                funcfsys.stdout.buffer
        else:
            funcsys.stdin.buffersys.stdout.buffer


def test():
    s0 = b'Aladdin:open sesame'
    print(repr(s0))
    s1 = encodebytes(s0)
    print(repr(s1))
    s2 = decodebytes(s1)
    print(repr(s2))
    assert s0 == s2


if __name__ == '__main__':
    main()