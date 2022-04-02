# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: quopri.py
"""Conversions to/from quoted-printable transport encoding as per RFC 1521."""
__all__ = [
 'encode', 'decode', 'encodestring', 'decodestring']
ESCAPE = b'='
MAXLINESIZE = 76
HEX = b'0123456789ABCDEF'
EMPTYSTRING = b''
try:
    from binascii import a2b_qp, b2a_qp
except ImportError:
    a2b_qp = None
    b2a_qp = None
else:

    def needsquoting(c, quotetabs, header):
        """Decide whether a particular byte ordinal needs to be quoted.

    The 'quotetabs' flag indicates whether embedded tabs and spaces should be
    quoted.  Note that line-ending tabs and spaces are always encoded, as per
    RFC 1521.
    """
        assert isinstance(c, bytes)
        if c in b' \t':
            return quotetabs
        if c == b'_':
            return header
        return c == ESCAPE or not b' ' <= c <= b'~'


    def quote(c):
        """Quote a single character."""
        if not (isinstance(c, bytes) and len(c) == 1):
            raise AssertionError
        c = ord(c)
        return ESCAPE + bytes((HEX[(c // 16)], HEX[(c % 16)]))


    def encode(input, output, quotetabs, header=False):
        """Read 'input', apply quoted-printable encoding, and write to 'output'.

    'input' and 'output' are binary file objects. The 'quotetabs' flag
    indicates whether embedded tabs and spaces should be quoted. Note that
    line-ending tabs and spaces are always encoded, as per RFC 1521.
    The 'header' flag indicates whether we are encoding spaces as _ as per RFC
    1522."""
        if b2a_qp is not None:
            data = input.read()
            odata = b2a_qp(data, quotetabs=quotetabs, header=header)
            output.write(odata)
            return

        def write(s, output=output, lineEnd=b'\n'):
            if s and s[-1:] in b' \t':
                output.write(s[:-1] + quote(s[-1:]) + lineEnd)
            elif s == b'.':
                output.write(quote(s) + lineEnd)
            else:
                output.write(s + lineEnd)

        prevline = None
        while True:
            line = input.readline()
            if not line:
                pass
            else:
                outline = []
                stripped = b''
            if line[-1:] == b'\n':
                line = line[:-1]
                stripped = b'\n'
            else:
                for c in line:
                    c = bytes((c,))
                    if needsquoting(c, quotetabs, header):
                        c = quote(c)
                    if header and c == b' ':
                        outline.append(b'_')
                    else:
                        outline.append(c)
                else:
                    if prevline is not None:
                        write(prevline)
                    thisline = EMPTYSTRING.join(outline)
                    while True:
                        if len(thisline) > MAXLINESIZE:
                            write((thisline[:MAXLINESIZE - 1]), lineEnd=b'=\n')
                            thisline = thisline[MAXLINESIZE - 1:]

                    prevline = thisline

        if prevline is not None:
            write(prevline, lineEnd=stripped)


    def encodestring(s, quotetabs=False, header=False):
        if b2a_qp is not None:
            return b2a_qp(s, quotetabs=quotetabs, header=header)
        from io import BytesIO
        infp = BytesIO(s)
        outfp = BytesIO()
        encode(infp, outfp, quotetabs, header)
        return outfp.getvalue()


    def decode(input, output, header=False):
        """Read 'input', apply quoted-printable decoding, and write to 'output'.
    'input' and 'output' are binary file objects.
    If 'header' is true, decode underscore as space (per RFC 1522)."""
        if a2b_qp is not None:
            data = input.read()
            odata = a2b_qp(data, header=header)
            output.write(odata)
            return
        new = b''
        while True:
            line = input.readline()
            if not line:
                pass
            else:
                i, n = 0, len(line)
                if n > 0 and line[n - 1:n] == b'\n':
                    partial = 0
                    n = n - 1
                    while not n > 0 or line[n - 1:n] in b' \t\r':
                        n = n - 1

                else:
                    partial = 1
                while i < n:
                    c = line[i:i + 1]
                    if c == b'_':
                        if header:
                            new = new + b' '
                            i = i + 1

            if c != ESCAPE:
                new = new + c
                i = i + 1
            else:
                if i + 1 == n:
                    if not partial:
                        partial = 1
                if i + 1 < n and line[i + 1:i + 2] == ESCAPE:
                    new = new + ESCAPE
                    i = i + 2
                else:
                    if i + 2 < n:
                        if ishex(line[i + 1:i + 2]) and ishex(line[i + 2:i + 3]):
                            new = new + bytes((unhex(line[i + 1:i + 3]),))
                            i = i + 3
                        else:
                            new = new + c
                            i = i + 1
                if not partial:
                    output.write(new + b'\n')
                    new = b''

        if new:
            output.write(new)


    def decodestring(s, header=False):
        if a2b_qp is not None:
            return a2b_qp(s, header=header)
        from io import BytesIO
        infp = BytesIO(s)
        outfp = BytesIO()
        decode(infp, outfp, header=header)
        return outfp.getvalue()


    def ishex(c):
        """Return true if the byte ordinal 'c' is a hexadecimal digit in ASCII."""
        assert isinstance(c, bytes)
        return b'0' <= c <= b'9' or b'a' <= c <= b'f' or b'A' <= c <= b'F'


    def unhex(s):
        """Get the integer value of a hexadecimal number."""
        bits = 0
        for c in s:
            c = bytes((c,))
            if b'0' <= c <= b'9':
                i = ord('0')
            else:
                if b'a' <= c <= b'f':
                    i = ord('a') - 10
                elif b'A' <= c <= b'F':
                    i = ord(b'A') - 10
                elif not False:
                    raise AssertionError('non-hex digit ' + repr(c))
                bits = bits * 16 + (ord(c) - i)
        else:
            return bits


    def main--- This code section failed: ---

 L. 196         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              sys
                6  STORE_FAST               'sys'

 L. 197         8  LOAD_CONST               0
               10  LOAD_CONST               None
               12  IMPORT_NAME              getopt
               14  STORE_FAST               'getopt'

 L. 198        16  SETUP_FINALLY        48  'to 48'

 L. 199        18  LOAD_FAST                'getopt'
               20  LOAD_METHOD              getopt
               22  LOAD_FAST                'sys'
               24  LOAD_ATTR                argv
               26  LOAD_CONST               1
               28  LOAD_CONST               None
               30  BUILD_SLICE_2         2 
               32  BINARY_SUBSCR    
               34  LOAD_STR                 'td'
               36  CALL_METHOD_2         2  ''
               38  UNPACK_SEQUENCE_2     2 
               40  STORE_FAST               'opts'
               42  STORE_FAST               'args'
               44  POP_BLOCK        
               46  JUMP_FORWARD        134  'to 134'
             48_0  COME_FROM_FINALLY    16  '16'

 L. 200        48  DUP_TOP          
               50  LOAD_FAST                'getopt'
               52  LOAD_ATTR                error
               54  COMPARE_OP               exception-match
               56  POP_JUMP_IF_FALSE   132  'to 132'
               58  POP_TOP          
               60  STORE_FAST               'msg'
               62  POP_TOP          
               64  SETUP_FINALLY       120  'to 120'

 L. 201        66  LOAD_FAST                'sys'
               68  LOAD_ATTR                stderr
               70  LOAD_FAST                'sys'
               72  STORE_ATTR               stdout

 L. 202        74  LOAD_GLOBAL              print
               76  LOAD_FAST                'msg'
               78  CALL_FUNCTION_1       1  ''
               80  POP_TOP          

 L. 203        82  LOAD_GLOBAL              print
               84  LOAD_STR                 'usage: quopri [-t | -d] [file] ...'
               86  CALL_FUNCTION_1       1  ''
               88  POP_TOP          

 L. 204        90  LOAD_GLOBAL              print
               92  LOAD_STR                 '-t: quote tabs'
               94  CALL_FUNCTION_1       1  ''
               96  POP_TOP          

 L. 205        98  LOAD_GLOBAL              print
              100  LOAD_STR                 '-d: decode; default encode'
              102  CALL_FUNCTION_1       1  ''
              104  POP_TOP          

 L. 206       106  LOAD_FAST                'sys'
              108  LOAD_METHOD              exit
              110  LOAD_CONST               2
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          
              116  POP_BLOCK        
              118  BEGIN_FINALLY    
            120_0  COME_FROM_FINALLY    64  '64'
              120  LOAD_CONST               None
              122  STORE_FAST               'msg'
              124  DELETE_FAST              'msg'
              126  END_FINALLY      
              128  POP_EXCEPT       
              130  JUMP_FORWARD        134  'to 134'
            132_0  COME_FROM            56  '56'
              132  END_FINALLY      
            134_0  COME_FROM           130  '130'
            134_1  COME_FROM            46  '46'

 L. 207       134  LOAD_CONST               0
              136  STORE_FAST               'deco'

 L. 208       138  LOAD_CONST               0
              140  STORE_FAST               'tabs'

 L. 209       142  LOAD_FAST                'opts'
              144  GET_ITER         
            146_0  COME_FROM           178  '178'
            146_1  COME_FROM           172  '172'
              146  FOR_ITER            180  'to 180'
              148  UNPACK_SEQUENCE_2     2 
              150  STORE_FAST               'o'
              152  STORE_FAST               'a'

 L. 210       154  LOAD_FAST                'o'
              156  LOAD_STR                 '-t'
              158  COMPARE_OP               ==
              160  POP_JUMP_IF_FALSE   166  'to 166'

 L. 210       162  LOAD_CONST               1
              164  STORE_FAST               'tabs'
            166_0  COME_FROM           160  '160'

 L. 211       166  LOAD_FAST                'o'
              168  LOAD_STR                 '-d'
              170  COMPARE_OP               ==
              172  POP_JUMP_IF_FALSE_BACK   146  'to 146'

 L. 211       174  LOAD_CONST               1
              176  STORE_FAST               'deco'
              178  JUMP_BACK           146  'to 146'
            180_0  COME_FROM           146  '146'

 L. 212       180  LOAD_FAST                'tabs'
              182  POP_JUMP_IF_FALSE   214  'to 214'
              184  LOAD_FAST                'deco'
              186  POP_JUMP_IF_FALSE   214  'to 214'

 L. 213       188  LOAD_FAST                'sys'
              190  LOAD_ATTR                stderr
              192  LOAD_FAST                'sys'
              194  STORE_ATTR               stdout

 L. 214       196  LOAD_GLOBAL              print
              198  LOAD_STR                 '-t and -d are mutually exclusive'
              200  CALL_FUNCTION_1       1  ''
              202  POP_TOP          

 L. 215       204  LOAD_FAST                'sys'
              206  LOAD_METHOD              exit
              208  LOAD_CONST               2
              210  CALL_METHOD_1         1  ''
              212  POP_TOP          
            214_0  COME_FROM           186  '186'
            214_1  COME_FROM           182  '182'

 L. 216       214  LOAD_FAST                'args'
              216  POP_JUMP_IF_TRUE    224  'to 224'

 L. 216       218  LOAD_STR                 '-'
              220  BUILD_LIST_1          1 
              222  STORE_FAST               'args'
            224_0  COME_FROM           216  '216'

 L. 217       224  LOAD_CONST               0
              226  STORE_FAST               'sts'

 L. 218       228  LOAD_FAST                'args'
              230  GET_ITER         
            232_0  COME_FROM           402  '402'
            232_1  COME_FROM           318  '318'
              232  FOR_ITER            404  'to 404'
              234  STORE_FAST               'file'

 L. 219       236  LOAD_FAST                'file'
              238  LOAD_STR                 '-'
              240  COMPARE_OP               ==
              242  POP_JUMP_IF_FALSE   254  'to 254'

 L. 220       244  LOAD_FAST                'sys'
              246  LOAD_ATTR                stdin
              248  LOAD_ATTR                buffer
              250  STORE_FAST               'fp'
              252  JUMP_FORWARD        338  'to 338'
            254_0  COME_FROM           242  '242'

 L. 222       254  SETUP_FINALLY       270  'to 270'

 L. 223       256  LOAD_GLOBAL              open
              258  LOAD_FAST                'file'
              260  LOAD_STR                 'rb'
              262  CALL_FUNCTION_2       2  ''
              264  STORE_FAST               'fp'
              266  POP_BLOCK        
              268  JUMP_FORWARD        338  'to 338'
            270_0  COME_FROM_FINALLY   254  '254'

 L. 224       270  DUP_TOP          
              272  LOAD_GLOBAL              OSError
              274  COMPARE_OP               exception-match
          276_278  POP_JUMP_IF_FALSE   336  'to 336'
              280  POP_TOP          
              282  STORE_FAST               'msg'
              284  POP_TOP          
              286  SETUP_FINALLY       324  'to 324'

 L. 225       288  LOAD_FAST                'sys'
              290  LOAD_ATTR                stderr
              292  LOAD_METHOD              write
              294  LOAD_STR                 "%s: can't open (%s)\n"
              296  LOAD_FAST                'file'
              298  LOAD_FAST                'msg'
              300  BUILD_TUPLE_2         2 
              302  BINARY_MODULO    
              304  CALL_METHOD_1         1  ''
              306  POP_TOP          

 L. 226       308  LOAD_CONST               1
              310  STORE_FAST               'sts'

 L. 227       312  POP_BLOCK        
              314  POP_EXCEPT       
              316  CALL_FINALLY        324  'to 324'
              318  JUMP_BACK           232  'to 232'
              320  POP_BLOCK        
              322  BEGIN_FINALLY    
            324_0  COME_FROM           316  '316'
            324_1  COME_FROM_FINALLY   286  '286'
              324  LOAD_CONST               None
              326  STORE_FAST               'msg'
              328  DELETE_FAST              'msg'
              330  END_FINALLY      
              332  POP_EXCEPT       
              334  JUMP_FORWARD        338  'to 338'
            336_0  COME_FROM           276  '276'
              336  END_FINALLY      
            338_0  COME_FROM           334  '334'
            338_1  COME_FROM           268  '268'
            338_2  COME_FROM           252  '252'

 L. 228       338  SETUP_FINALLY       382  'to 382'

 L. 229       340  LOAD_FAST                'deco'
          342_344  POP_JUMP_IF_FALSE   362  'to 362'

 L. 230       346  LOAD_GLOBAL              decode
              348  LOAD_FAST                'fp'
              350  LOAD_FAST                'sys'
              352  LOAD_ATTR                stdout
              354  LOAD_ATTR                buffer
              356  CALL_FUNCTION_2       2  ''
              358  POP_TOP          
              360  JUMP_FORWARD        378  'to 378'
            362_0  COME_FROM           342  '342'

 L. 232       362  LOAD_GLOBAL              encode
              364  LOAD_FAST                'fp'
              366  LOAD_FAST                'sys'
              368  LOAD_ATTR                stdout
              370  LOAD_ATTR                buffer
              372  LOAD_FAST                'tabs'
              374  CALL_FUNCTION_3       3  ''
              376  POP_TOP          
            378_0  COME_FROM           360  '360'
              378  POP_BLOCK        
              380  BEGIN_FINALLY    
            382_0  COME_FROM_FINALLY   338  '338'

 L. 234       382  LOAD_FAST                'file'
              384  LOAD_STR                 '-'
              386  COMPARE_OP               !=
          388_390  POP_JUMP_IF_FALSE   400  'to 400'

 L. 235       392  LOAD_FAST                'fp'
              394  LOAD_METHOD              close
              396  CALL_METHOD_0         0  ''
              398  POP_TOP          
            400_0  COME_FROM           388  '388'
              400  END_FINALLY      
              402  JUMP_BACK           232  'to 232'
            404_0  COME_FROM           232  '232'

 L. 236       404  LOAD_FAST                'sts'
          406_408  POP_JUMP_IF_FALSE   420  'to 420'

 L. 237       410  LOAD_FAST                'sys'
              412  LOAD_METHOD              exit
              414  LOAD_FAST                'sts'
              416  CALL_METHOD_1         1  ''
              418  POP_TOP          
            420_0  COME_FROM           406  '406'

Parse error at or near `CALL_FINALLY' instruction at offset 316


    if __name__ == '__main__':
        main()