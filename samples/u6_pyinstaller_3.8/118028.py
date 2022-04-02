# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\dns\ipv6.py
"""IPv6 helper functions."""
import re, binascii, dns.exception, dns.ipv4
from ._compat import xrange, binary_type, maybe_decode
_leading_zero = re.compile('0+([0-9a-f]+)')

def inet_ntoa(address):
    """Convert an IPv6 address in binary form to text form.

    *address*, a ``binary``, the IPv6 address in binary form.

    Raises ``ValueError`` if the address isn't 16 bytes long.
    Returns a ``text``.
    """
    if len(address) != 16:
        raise ValueError('IPv6 addresses are 16 bytes long')
    else:
        hex = binascii.hexlify(address)
        chunks = []
        i = 0
        l = len(hex)
        while True:
            if i < l:
                chunk = maybe_decode(hex[i:i + 4])
                m = _leading_zero.match(chunk)
                if m is not None:
                    chunk = m.group(1)
                chunks.append(chunk)
                i += 4

    best_start = 0
    best_len = 0
    start = -1
    last_was_zero = False
    for i in xrange(8):
        if chunks[i] != '0':
            if last_was_zero:
                end = i
                current_len = end - start
                if current_len > best_len:
                    best_start = start
                    best_len = current_len
                last_was_zero = False
        elif not last_was_zero:
            start = i
            last_was_zero = True
        else:
            if last_was_zero:
                end = 8
                current_len = end - start
                if current_len > best_len:
                    best_start = start
                    best_len = current_len
            elif best_len > 1:
                if best_start == 0 and not best_len == 6:
                    if not best_len == 5 or chunks[5] == 'ffff':
                        if best_len == 6:
                            prefix = '::'
                        else:
                            prefix = '::ffff:'
                        hex = prefix + dns.ipv4.inet_ntoa(address[12:])
                    else:
                        hex = ':'.join(chunks[:best_start]) + '::' + ':'.join(chunks[best_start + best_len:])
            else:
                hex = ':'.join(chunks)
            return hex


_v4_ending = re.compile(b'(.*):(\\d+\\.\\d+\\.\\d+\\.\\d+)$')
_colon_colon_start = re.compile(b'::.*')
_colon_colon_end = re.compile(b'.*::$')

def inet_aton--- This code section failed: ---

 L. 111         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'text'
                4  LOAD_GLOBAL              binary_type
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     18  'to 18'

 L. 112        10  LOAD_FAST                'text'
               12  LOAD_METHOD              encode
               14  CALL_METHOD_0         0  ''
               16  STORE_FAST               'text'
             18_0  COME_FROM             8  '8'

 L. 114        18  LOAD_FAST                'text'
               20  LOAD_CONST               b'::'
               22  COMPARE_OP               ==
               24  POP_JUMP_IF_FALSE    30  'to 30'

 L. 115        26  LOAD_CONST               b'0::'
               28  STORE_FAST               'text'
             30_0  COME_FROM            24  '24'

 L. 119        30  LOAD_GLOBAL              _v4_ending
               32  LOAD_METHOD              match
               34  LOAD_FAST                'text'
               36  CALL_METHOD_1         1  ''
               38  STORE_FAST               'm'

 L. 120        40  LOAD_FAST                'm'
               42  LOAD_CONST               None
               44  COMPARE_OP               is-not
               46  POP_JUMP_IF_FALSE   118  'to 118'

 L. 121        48  LOAD_GLOBAL              bytearray
               50  LOAD_GLOBAL              dns
               52  LOAD_ATTR                ipv4
               54  LOAD_METHOD              inet_aton
               56  LOAD_FAST                'm'
               58  LOAD_METHOD              group
               60  LOAD_CONST               2
               62  CALL_METHOD_1         1  ''
               64  CALL_METHOD_1         1  ''
               66  CALL_FUNCTION_1       1  ''
               68  STORE_FAST               'b'

 L. 122        70  LOAD_STR                 '{}:{:02x}{:02x}:{:02x}{:02x}'
               72  LOAD_METHOD              format
               74  LOAD_FAST                'm'
               76  LOAD_METHOD              group
               78  LOAD_CONST               1
               80  CALL_METHOD_1         1  ''
               82  LOAD_METHOD              decode
               84  CALL_METHOD_0         0  ''

 L. 123        86  LOAD_FAST                'b'
               88  LOAD_CONST               0
               90  BINARY_SUBSCR    

 L. 123        92  LOAD_FAST                'b'
               94  LOAD_CONST               1
               96  BINARY_SUBSCR    

 L. 123        98  LOAD_FAST                'b'
              100  LOAD_CONST               2
              102  BINARY_SUBSCR    

 L. 124       104  LOAD_FAST                'b'
              106  LOAD_CONST               3
              108  BINARY_SUBSCR    

 L. 122       110  CALL_METHOD_5         5  ''
              112  LOAD_METHOD              encode
              114  CALL_METHOD_0         0  ''
              116  STORE_FAST               'text'
            118_0  COME_FROM            46  '46'

 L. 129       118  LOAD_GLOBAL              _colon_colon_start
              120  LOAD_METHOD              match
              122  LOAD_FAST                'text'
              124  CALL_METHOD_1         1  ''
              126  STORE_FAST               'm'

 L. 130       128  LOAD_FAST                'm'
              130  LOAD_CONST               None
              132  COMPARE_OP               is-not
              134  POP_JUMP_IF_FALSE   150  'to 150'

 L. 131       136  LOAD_FAST                'text'
              138  LOAD_CONST               1
              140  LOAD_CONST               None
              142  BUILD_SLICE_2         2 
              144  BINARY_SUBSCR    
              146  STORE_FAST               'text'
              148  JUMP_FORWARD        180  'to 180'
            150_0  COME_FROM           134  '134'

 L. 133       150  LOAD_GLOBAL              _colon_colon_end
              152  LOAD_METHOD              match
              154  LOAD_FAST                'text'
              156  CALL_METHOD_1         1  ''
              158  STORE_FAST               'm'

 L. 134       160  LOAD_FAST                'm'
              162  LOAD_CONST               None
              164  COMPARE_OP               is-not
              166  POP_JUMP_IF_FALSE   180  'to 180'

 L. 135       168  LOAD_FAST                'text'
              170  LOAD_CONST               None
              172  LOAD_CONST               -1
              174  BUILD_SLICE_2         2 
              176  BINARY_SUBSCR    
              178  STORE_FAST               'text'
            180_0  COME_FROM           166  '166'
            180_1  COME_FROM           148  '148'

 L. 139       180  LOAD_FAST                'text'
              182  LOAD_METHOD              split
              184  LOAD_CONST               b':'
              186  CALL_METHOD_1         1  ''
              188  STORE_FAST               'chunks'

 L. 140       190  LOAD_GLOBAL              len
              192  LOAD_FAST                'chunks'
              194  CALL_FUNCTION_1       1  ''
              196  STORE_FAST               'l'

 L. 141       198  LOAD_FAST                'l'
              200  LOAD_CONST               8
              202  COMPARE_OP               >
              204  POP_JUMP_IF_FALSE   214  'to 214'

 L. 142       206  LOAD_GLOBAL              dns
              208  LOAD_ATTR                exception
              210  LOAD_ATTR                SyntaxError
              212  RAISE_VARARGS_1       1  'exception instance'
            214_0  COME_FROM           204  '204'

 L. 143       214  LOAD_CONST               False
              216  STORE_FAST               'seen_empty'

 L. 144       218  BUILD_LIST_0          0 
              220  STORE_FAST               'canonical'

 L. 145       222  LOAD_FAST                'chunks'
              224  GET_ITER         
              226  FOR_ITER            358  'to 358'
              228  STORE_FAST               'c'

 L. 146       230  LOAD_FAST                'c'
              232  LOAD_CONST               b''
              234  COMPARE_OP               ==
          236_238  POP_JUMP_IF_FALSE   294  'to 294'

 L. 147       240  LOAD_FAST                'seen_empty'
              242  POP_JUMP_IF_FALSE   252  'to 252'

 L. 148       244  LOAD_GLOBAL              dns
              246  LOAD_ATTR                exception
              248  LOAD_ATTR                SyntaxError
              250  RAISE_VARARGS_1       1  'exception instance'
            252_0  COME_FROM           242  '242'

 L. 149       252  LOAD_CONST               True
              254  STORE_FAST               'seen_empty'

 L. 150       256  LOAD_GLOBAL              xrange
              258  LOAD_CONST               0
              260  LOAD_CONST               8
              262  LOAD_FAST                'l'
              264  BINARY_SUBTRACT  
              266  LOAD_CONST               1
              268  BINARY_ADD       
              270  CALL_FUNCTION_2       2  ''
              272  GET_ITER         
              274  FOR_ITER            292  'to 292'
              276  STORE_FAST               'i'

 L. 151       278  LOAD_FAST                'canonical'
              280  LOAD_METHOD              append
              282  LOAD_CONST               b'0000'
              284  CALL_METHOD_1         1  ''
              286  POP_TOP          
          288_290  JUMP_BACK           274  'to 274'
              292  JUMP_BACK           226  'to 226'
            294_0  COME_FROM           236  '236'

 L. 153       294  LOAD_GLOBAL              len
              296  LOAD_FAST                'c'
              298  CALL_FUNCTION_1       1  ''
              300  STORE_FAST               'lc'

 L. 154       302  LOAD_FAST                'lc'
              304  LOAD_CONST               4
              306  COMPARE_OP               >
          308_310  POP_JUMP_IF_FALSE   320  'to 320'

 L. 155       312  LOAD_GLOBAL              dns
              314  LOAD_ATTR                exception
              316  LOAD_ATTR                SyntaxError
              318  RAISE_VARARGS_1       1  'exception instance'
            320_0  COME_FROM           308  '308'

 L. 156       320  LOAD_FAST                'lc'
              322  LOAD_CONST               4
              324  COMPARE_OP               !=
          326_328  POP_JUMP_IF_FALSE   346  'to 346'

 L. 157       330  LOAD_CONST               b'0'
              332  LOAD_CONST               4
              334  LOAD_FAST                'lc'
              336  BINARY_SUBTRACT  
              338  BINARY_MULTIPLY  
              340  LOAD_FAST                'c'
              342  BINARY_ADD       
              344  STORE_FAST               'c'
            346_0  COME_FROM           326  '326'

 L. 158       346  LOAD_FAST                'canonical'
              348  LOAD_METHOD              append
              350  LOAD_FAST                'c'
              352  CALL_METHOD_1         1  ''
              354  POP_TOP          
              356  JUMP_BACK           226  'to 226'

 L. 159       358  LOAD_FAST                'l'
              360  LOAD_CONST               8
              362  COMPARE_OP               <
          364_366  POP_JUMP_IF_FALSE   382  'to 382'
              368  LOAD_FAST                'seen_empty'
          370_372  POP_JUMP_IF_TRUE    382  'to 382'

 L. 160       374  LOAD_GLOBAL              dns
              376  LOAD_ATTR                exception
              378  LOAD_ATTR                SyntaxError
              380  RAISE_VARARGS_1       1  'exception instance'
            382_0  COME_FROM           370  '370'
            382_1  COME_FROM           364  '364'

 L. 161       382  LOAD_CONST               b''
              384  LOAD_METHOD              join
              386  LOAD_FAST                'canonical'
              388  CALL_METHOD_1         1  ''
              390  STORE_FAST               'text'

 L. 166       392  SETUP_FINALLY       406  'to 406'

 L. 167       394  LOAD_GLOBAL              binascii
              396  LOAD_METHOD              unhexlify
              398  LOAD_FAST                'text'
              400  CALL_METHOD_1         1  ''
              402  POP_BLOCK        
              404  RETURN_VALUE     
            406_0  COME_FROM_FINALLY   392  '392'

 L. 168       406  DUP_TOP          
              408  LOAD_GLOBAL              binascii
              410  LOAD_ATTR                Error
              412  LOAD_GLOBAL              TypeError
              414  BUILD_TUPLE_2         2 
              416  COMPARE_OP               exception-match
          418_420  POP_JUMP_IF_FALSE   440  'to 440'
              422  POP_TOP          
              424  POP_TOP          
              426  POP_TOP          

 L. 169       428  LOAD_GLOBAL              dns
              430  LOAD_ATTR                exception
              432  LOAD_ATTR                SyntaxError
              434  RAISE_VARARGS_1       1  'exception instance'
              436  POP_EXCEPT       
              438  JUMP_FORWARD        442  'to 442'
            440_0  COME_FROM           418  '418'
              440  END_FINALLY      
            442_0  COME_FROM           438  '438'

Parse error at or near `POP_TOP' instruction at offset 424


_mapped_prefix = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff'

def is_mapped(address):
    """Is the specified address a mapped IPv4 address?

    *address*, a ``binary`` is an IPv6 address in binary form.

    Returns a ``bool``.
    """
    return address.startswith(_mapped_prefix)