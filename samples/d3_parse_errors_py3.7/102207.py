# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: quopri.py
"""Conversions to/from quoted-printable transport encoding as per RFC 1521."""
__all__ = [
 'encode', 'decode', 'encodestring', 'decodestring']
ESCAPE = '='
MAXLINESIZE = 76
HEX = '0123456789ABCDEF'
EMPTYSTRING = ''
try:
    from binascii import a2b_qp, b2a_qp
except ImportError:
    a2b_qp = None
    b2a_qp = None

def needsquoting(c, quotetabs, header):
    """Decide whether a particular byte ordinal needs to be quoted.

    The 'quotetabs' flag indicates whether embedded tabs and spaces should be
    quoted.  Note that line-ending tabs and spaces are always encoded, as per
    RFC 1521.
    """
    assert isinstance(c, bytes)
    if c in ' \t':
        return quotetabs
    if c == '_':
        return header
    return c == ESCAPE or not ' ' <= c <= '~'


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

    def write(s, output=output, lineEnd='\n'):
        if s and s[-1:] in ' \t':
            output.write(s[:-1] + quote(s[-1:]) + lineEnd)
        elif s == '.':
            output.write(quote(s) + lineEnd)
        else:
            output.write(s + lineEnd)

    prevline = None
    while True:
        line = input.readline()
        if not line:
            break
        else:
            outline = []
            stripped = ''
            if line[-1:] == '\n':
                line = line[:-1]
                stripped = '\n'
            for c in line:
                c = bytes((c,))
                if needsquoting(c, quotetabs, header):
                    c = quote(c)
                if header and c == ' ':
                    outline.append('_')
                else:
                    outline.append(c)

            if prevline is not None:
                write(prevline)
            thisline = EMPTYSTRING.join(outline)
            while len(thisline) > MAXLINESIZE:
                write((thisline[:MAXLINESIZE - 1]), lineEnd='=\n')
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


def decode--- This code section failed: ---

 L. 122         0  LOAD_GLOBAL              a2b_qp
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    42  'to 42'

 L. 123         8  LOAD_FAST                'input'
               10  LOAD_METHOD              read
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  STORE_FAST               'data'

 L. 124        16  LOAD_GLOBAL              a2b_qp
               18  LOAD_FAST                'data'
               20  LOAD_FAST                'header'
               22  LOAD_CONST               ('header',)
               24  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               26  STORE_FAST               'odata'

 L. 125        28  LOAD_FAST                'output'
               30  LOAD_METHOD              write
               32  LOAD_FAST                'odata'
               34  CALL_METHOD_1         1  '1 positional argument'
               36  POP_TOP          

 L. 126        38  LOAD_CONST               None
               40  RETURN_VALUE     
             42_0  COME_FROM             6  '6'

 L. 128        42  LOAD_STR                 ''
               44  STORE_FAST               'new'

 L. 129     46_48  SETUP_LOOP          494  'to 494'
             50_0  COME_FROM           490  '490'
             50_1  COME_FROM           470  '470'

 L. 130        50  LOAD_FAST                'input'
               52  LOAD_METHOD              readline
               54  CALL_METHOD_0         0  '0 positional arguments'
               56  STORE_FAST               'line'

 L. 131        58  LOAD_FAST                'line'
               60  POP_JUMP_IF_TRUE     64  'to 64'

 L. 131        62  BREAK_LOOP       
             64_0  COME_FROM            60  '60'

 L. 132        64  LOAD_CONST               0
               66  LOAD_GLOBAL              len
               68  LOAD_FAST                'line'
               70  CALL_FUNCTION_1       1  '1 positional argument'
               72  ROT_TWO          
               74  STORE_FAST               'i'
               76  STORE_FAST               'n'

 L. 133        78  LOAD_FAST                'n'
               80  LOAD_CONST               0
               82  COMPARE_OP               >
               84  POP_JUMP_IF_FALSE   162  'to 162'
               86  LOAD_FAST                'line'
               88  LOAD_FAST                'n'
               90  LOAD_CONST               1
               92  BINARY_SUBTRACT  
               94  LOAD_FAST                'n'
               96  BUILD_SLICE_2         2 
               98  BINARY_SUBSCR    
              100  LOAD_STR                 '\n'
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   162  'to 162'

 L. 134       106  LOAD_CONST               0
              108  STORE_FAST               'partial'

 L. 134       110  LOAD_FAST                'n'
              112  LOAD_CONST               1
              114  BINARY_SUBTRACT  
              116  STORE_FAST               'n'

 L. 136       118  SETUP_LOOP          166  'to 166'
            120_0  COME_FROM           156  '156'
              120  LOAD_FAST                'n'
              122  LOAD_CONST               0
              124  COMPARE_OP               >
              126  POP_JUMP_IF_FALSE   158  'to 158'
              128  LOAD_FAST                'line'
              130  LOAD_FAST                'n'
              132  LOAD_CONST               1
              134  BINARY_SUBTRACT  
              136  LOAD_FAST                'n'
              138  BUILD_SLICE_2         2 
              140  BINARY_SUBSCR    
              142  LOAD_STR                 ' \t\r'
              144  COMPARE_OP               in
              146  POP_JUMP_IF_FALSE   158  'to 158'

 L. 137       148  LOAD_FAST                'n'
              150  LOAD_CONST               1
              152  BINARY_SUBTRACT  
              154  STORE_FAST               'n'
              156  JUMP_BACK           120  'to 120'
            158_0  COME_FROM           146  '146'
            158_1  COME_FROM           126  '126'
              158  POP_BLOCK        
              160  JUMP_FORWARD        166  'to 166'
            162_0  COME_FROM           104  '104'
            162_1  COME_FROM            84  '84'

 L. 139       162  LOAD_CONST               1
              164  STORE_FAST               'partial'
            166_0  COME_FROM           160  '160'
            166_1  COME_FROM_LOOP      118  '118'

 L. 140   166_168  SETUP_LOOP          468  'to 468'
            170_0  COME_FROM           464  '464'
            170_1  COME_FROM           446  '446'
            170_2  COME_FROM           336  '336'
            170_3  COME_FROM           278  '278'
            170_4  COME_FROM           250  '250'
            170_5  COME_FROM           224  '224'
              170  LOAD_FAST                'i'
              172  LOAD_FAST                'n'
              174  COMPARE_OP               <
          176_178  POP_JUMP_IF_FALSE   466  'to 466'

 L. 141       180  LOAD_FAST                'line'
              182  LOAD_FAST                'i'
              184  LOAD_FAST                'i'
              186  LOAD_CONST               1
              188  BINARY_ADD       
              190  BUILD_SLICE_2         2 
              192  BINARY_SUBSCR    
              194  STORE_FAST               'c'

 L. 142       196  LOAD_FAST                'c'
              198  LOAD_STR                 '_'
              200  COMPARE_OP               ==
              202  POP_JUMP_IF_FALSE   226  'to 226'
              204  LOAD_FAST                'header'
              206  POP_JUMP_IF_FALSE   226  'to 226'

 L. 143       208  LOAD_FAST                'new'
              210  LOAD_STR                 ' '
              212  BINARY_ADD       
              214  STORE_FAST               'new'

 L. 143       216  LOAD_FAST                'i'
              218  LOAD_CONST               1
              220  BINARY_ADD       
              222  STORE_FAST               'i'
              224  JUMP_BACK           170  'to 170'
            226_0  COME_FROM           206  '206'
            226_1  COME_FROM           202  '202'

 L. 144       226  LOAD_FAST                'c'
              228  LOAD_GLOBAL              ESCAPE
              230  COMPARE_OP               !=
              232  POP_JUMP_IF_FALSE   252  'to 252'

 L. 145       234  LOAD_FAST                'new'
              236  LOAD_FAST                'c'
              238  BINARY_ADD       
              240  STORE_FAST               'new'

 L. 145       242  LOAD_FAST                'i'
              244  LOAD_CONST               1
              246  BINARY_ADD       
              248  STORE_FAST               'i'
              250  JUMP_BACK           170  'to 170'
            252_0  COME_FROM           232  '232'

 L. 146       252  LOAD_FAST                'i'
              254  LOAD_CONST               1
              256  BINARY_ADD       
              258  LOAD_FAST                'n'
              260  COMPARE_OP               ==
          262_264  POP_JUMP_IF_FALSE   280  'to 280'
              266  LOAD_FAST                'partial'
          268_270  POP_JUMP_IF_TRUE    280  'to 280'

 L. 147       272  LOAD_CONST               1
              274  STORE_FAST               'partial'

 L. 147       276  BREAK_LOOP       
              278  JUMP_BACK           170  'to 170'
            280_0  COME_FROM           268  '268'
            280_1  COME_FROM           262  '262'

 L. 148       280  LOAD_FAST                'i'
              282  LOAD_CONST               1
              284  BINARY_ADD       
              286  LOAD_FAST                'n'
              288  COMPARE_OP               <
          290_292  POP_JUMP_IF_FALSE   338  'to 338'
              294  LOAD_FAST                'line'
              296  LOAD_FAST                'i'
              298  LOAD_CONST               1
              300  BINARY_ADD       
              302  LOAD_FAST                'i'
              304  LOAD_CONST               2
              306  BINARY_ADD       
              308  BUILD_SLICE_2         2 
              310  BINARY_SUBSCR    
              312  LOAD_GLOBAL              ESCAPE
              314  COMPARE_OP               ==
          316_318  POP_JUMP_IF_FALSE   338  'to 338'

 L. 149       320  LOAD_FAST                'new'
              322  LOAD_GLOBAL              ESCAPE
              324  BINARY_ADD       
              326  STORE_FAST               'new'

 L. 149       328  LOAD_FAST                'i'
              330  LOAD_CONST               2
              332  BINARY_ADD       
              334  STORE_FAST               'i'
              336  JUMP_BACK           170  'to 170'
            338_0  COME_FROM           316  '316'
            338_1  COME_FROM           290  '290'

 L. 150       338  LOAD_FAST                'i'
              340  LOAD_CONST               2
              342  BINARY_ADD       
              344  LOAD_FAST                'n'
              346  COMPARE_OP               <
          348_350  POP_JUMP_IF_FALSE   448  'to 448'
              352  LOAD_GLOBAL              ishex
              354  LOAD_FAST                'line'
              356  LOAD_FAST                'i'
              358  LOAD_CONST               1
              360  BINARY_ADD       
              362  LOAD_FAST                'i'
              364  LOAD_CONST               2
              366  BINARY_ADD       
              368  BUILD_SLICE_2         2 
              370  BINARY_SUBSCR    
              372  CALL_FUNCTION_1       1  '1 positional argument'
          374_376  POP_JUMP_IF_FALSE   448  'to 448'
              378  LOAD_GLOBAL              ishex
              380  LOAD_FAST                'line'
              382  LOAD_FAST                'i'
              384  LOAD_CONST               2
              386  BINARY_ADD       
              388  LOAD_FAST                'i'
              390  LOAD_CONST               3
              392  BINARY_ADD       
              394  BUILD_SLICE_2         2 
              396  BINARY_SUBSCR    
              398  CALL_FUNCTION_1       1  '1 positional argument'
          400_402  POP_JUMP_IF_FALSE   448  'to 448'

 L. 151       404  LOAD_FAST                'new'
              406  LOAD_GLOBAL              bytes
              408  LOAD_GLOBAL              unhex
              410  LOAD_FAST                'line'
              412  LOAD_FAST                'i'
              414  LOAD_CONST               1
              416  BINARY_ADD       
              418  LOAD_FAST                'i'
              420  LOAD_CONST               3
              422  BINARY_ADD       
              424  BUILD_SLICE_2         2 
              426  BINARY_SUBSCR    
              428  CALL_FUNCTION_1       1  '1 positional argument'
              430  BUILD_TUPLE_1         1 
              432  CALL_FUNCTION_1       1  '1 positional argument'
              434  BINARY_ADD       
              436  STORE_FAST               'new'

 L. 151       438  LOAD_FAST                'i'
              440  LOAD_CONST               3
              442  BINARY_ADD       
              444  STORE_FAST               'i'
              446  JUMP_BACK           170  'to 170'
            448_0  COME_FROM           400  '400'
            448_1  COME_FROM           374  '374'
            448_2  COME_FROM           348  '348'

 L. 153       448  LOAD_FAST                'new'
              450  LOAD_FAST                'c'
              452  BINARY_ADD       
              454  STORE_FAST               'new'

 L. 153       456  LOAD_FAST                'i'
              458  LOAD_CONST               1
              460  BINARY_ADD       
              462  STORE_FAST               'i'
              464  JUMP_BACK           170  'to 170'
            466_0  COME_FROM           176  '176'
              466  POP_BLOCK        
            468_0  COME_FROM_LOOP      166  '166'

 L. 154       468  LOAD_FAST                'partial'
              470  POP_JUMP_IF_TRUE_BACK    50  'to 50'

 L. 155       472  LOAD_FAST                'output'
              474  LOAD_METHOD              write
              476  LOAD_FAST                'new'
              478  LOAD_STR                 '\n'
              480  BINARY_ADD       
              482  CALL_METHOD_1         1  '1 positional argument'
              484  POP_TOP          

 L. 156       486  LOAD_STR                 ''
              488  STORE_FAST               'new'
              490  JUMP_BACK            50  'to 50'
              492  POP_BLOCK        
            494_0  COME_FROM_LOOP       46  '46'

 L. 157       494  LOAD_FAST                'new'
          496_498  POP_JUMP_IF_FALSE   510  'to 510'

 L. 158       500  LOAD_FAST                'output'
              502  LOAD_METHOD              write
              504  LOAD_FAST                'new'
              506  CALL_METHOD_1         1  '1 positional argument'
              508  POP_TOP          
            510_0  COME_FROM           496  '496'

Parse error at or near `JUMP_FORWARD' instruction at offset 160


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
    return '0' <= c <= '9' or 'a' <= c <= 'f' or 'A' <= c <= 'F'


def unhex(s):
    """Get the integer value of a hexadecimal number."""
    bits = 0
    for c in s:
        c = bytes((c,))
        if '0' <= c <= '9':
            i = ord('0')
        else:
            if 'a' <= c <= 'f':
                i = ord('a') - 10
            elif 'A' <= c <= 'F':
                i = ord('A') - 10
            elif not False:
                raise AssertionError('non-hex digit ' + repr(c))
            bits = bits * 16 + (ord(c) - i)

    return bits


def main():
    import sys, getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'td')
    except getopt.error as msg:
        try:
            sys.stdout = sys.stderr
            print(msg)
            print('usage: quopri [-t | -d] [file] ...')
            print('-t: quote tabs')
            print('-d: decode; default encode')
            sys.exit(2)
        finally:
            msg = None
            del msg

    deco = 0
    tabs = 0
    for o, a in opts:
        if o == '-t':
            tabs = 1
        if o == '-d':
            deco = 1

    if tabs:
        if deco:
            sys.stdout = sys.stderr
            print('-t and -d are mutually exclusive')
            sys.exit(2)
    if not args:
        args = [
         '-']
    sts = 0
    for file in args:
        if file == '-':
            fp = sys.stdin.buffer
        else:
            try:
                fp = open(file, 'rb')
            except OSError as msg:
                try:
                    sys.stderr.write("%s: can't open (%s)\n" % (file, msg))
                    sts = 1
                    continue
                finally:
                    msg = None
                    del msg

            try:
                if deco:
                    decode(fp, sys.stdout.buffer)
                else:
                    encode(fp, sys.stdout.buffer, tabs)
            finally:
                if file != '-':
                    fp.close()

    if sts:
        sys.exit(sts)


if __name__ == '__main__':
    main()