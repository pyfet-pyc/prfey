# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: lazagne\softwares\memory\libkeepass\pureSalsa20.py
"""
    pureSalsa20.py -- a pure Python implementation of the Salsa20 cipher
    ====================================================================
    There are comments here by two authors about three pieces of software:
        comments by Larry Bugbee about
            Salsa20, the stream cipher by Daniel J. Bernstein 
                 (including comments about the speed of the C version) and
            pySalsa20, Bugbee's own Python wrapper for salsa20.c
                 (including some references), and
        comments by Steve Witham about
            pureSalsa20, Witham's pure Python 2.5 implementation of Salsa20,
                which follows pySalsa20's API, and is in this file.

    Salsa20: a Fast Streaming Cipher (comments by Larry Bugbee)
    -----------------------------------------------------------

    Salsa20 is a fast stream cipher written by Daniel Bernstein 
    that basically uses a hash function and XOR making for fast 
    encryption.  (Decryption uses the same function.)  Salsa20 
    is simple and quick.  
    
    Some Salsa20 parameter values...
        design strength    128 bits
        key length         128 or 256 bits, exactly
        IV, aka nonce      64 bits, always
        chunk size         must be in multiples of 64 bytes
    
    Salsa20 has two reduced versions, 8 and 12 rounds each.
    
    One benchmark (10 MB):
        1.5GHz PPC G4     102/97/89 MB/sec for 8/12/20 rounds
        AMD Athlon 2500+   77/67/53 MB/sec for 8/12/20 rounds
          (no I/O and before Python GC kicks in)
    
    Salsa20 is a Phase 3 finalist in the EU eSTREAM competition 
    and appears to be one of the fastest ciphers.  It is well 
    documented so I will not attempt any injustice here.  Please 
    see "References" below.
    
    ...and Salsa20 is "free for any use".  
    
    
    pySalsa20: a Python wrapper for Salsa20 (Comments by Larry Bugbee)
    ------------------------------------------------------------------

    pySalsa20.py is a simple ctypes Python wrapper.  Salsa20 is 
    as it's name implies, 20 rounds, but there are two reduced 
    versions, 8 and 12 rounds each.  Because the APIs are 
    identical, pySalsa20 is capable of wrapping all three 
    versions (number of rounds hardcoded), including a special 
    version that allows you to set the number of rounds with a 
    set_rounds() function.  Compile the version of your choice 
    as a shared library (not as a Python extension), name and 
    install it as libsalsa20.so.
    
    Sample usage:
        from pySalsa20 import Salsa20
        s20 = Salsa20(key, IV)
        dataout = s20.encryptBytes(datain)   # same for decrypt
    
    This is EXPERIMENTAL software and intended for educational 
    purposes only.  To make experimentation less cumbersome, 
    pySalsa20 is also free for any use.      
    
    THIS PROGRAM IS PROVIDED WITHOUT WARRANTY OR GUARANTEE OF
    ANY KIND.  USE AT YOUR OWN RISK.  
    
    Enjoy,
      
    Larry Bugbee
    bugbee@seanet.com
    April 2007

    
    References:
    -----------
      http://en.wikipedia.org/wiki/Salsa20
      http://en.wikipedia.org/wiki/Daniel_Bernstein
      http://cr.yp.to/djb.html
      http://www.ecrypt.eu.org/stream/salsa20p3.html
      http://www.ecrypt.eu.org/stream/p3ciphers/salsa20/salsa20_p3source.zip

     
    Prerequisites for pySalsa20:
    ----------------------------
      - Python 2.5 (haven't tested in 2.4)

    pureSalsa20: Salsa20 in pure Python 2.5 (comments by Steve Witham)
    ------------------------------------------------------------------

    pureSalsa20 is the stand-alone Python code in this file.
    It implements the underlying Salsa20 core algorithm
    and emulates pySalsa20's Salsa20 class API (minus a bug(*)).

    pureSalsa20 is MUCH slower than libsalsa20.so wrapped with pySalsa20--
    about 1/1000 the speed for Salsa20/20 and 1/500 the speed for Salsa20/8,
    when encrypting 64k-byte blocks on my computer.

    pureSalsa20 is for cases where portability is much more important than
    speed.  I wrote it for use in a "structured" random number generator.

    There are comments about the reasons for this slowness in
          http://www.tiac.net/~sw/2010/02/PureSalsa20

    Sample usage:
        from pureSalsa20 import Salsa20
        s20 = Salsa20(key, IV)
        dataout = s20.encryptBytes(datain)   # same for decrypt

    I took the test code from pySalsa20, added a bunch of tests including
    rough speed tests, and moved them into the file testSalsa20.py.  
    To test both pySalsa20 and pureSalsa20, type
        python testSalsa20.py

    (*)The bug (?) in pySalsa20 is this.  The rounds variable is global to the
    libsalsa20.so library and not switched when switching between instances
    of the Salsa20 class.
        s1 = Salsa20( key, IV, 20 )
        s2 = Salsa20( key, IV, 8 )
    In this example,
        with pySalsa20, both s1 and s2 will do 8 rounds of encryption.
        with pureSalsa20, s1 will do 20 rounds and s2 will do 8 rounds.
    Perhaps giving each instance its own nRounds variable, which
    is passed to the salsa20wordtobyte() function, is insecure.  I'm not a 
    cryptographer.

    pureSalsa20.py and testSalsa20.py are EXPERIMENTAL software and 
    intended for educational purposes only.  To make experimentation less 
    cumbersome, pureSalsa20.py and testSalsa20.py are free for any use.

    Revisions:
    ----------
      p3.2   Fixed bug that initialized the output buffer with plaintext!
             Saner ramping of nreps in speed test.
             Minor changes and print statements.
      p3.1   Took timing variability out of add32() and rot32().
             Made the internals more like pySalsa20/libsalsa .
             Put the semicolons back in the main loop!
             In encryptBytes(), modify a byte array instead of appending.
             Fixed speed calculation bug.
             Used subclasses instead of patches in testSalsa20.py .
             Added 64k-byte messages to speed test to be fair to pySalsa20.
      p3     First version, intended to parallel pySalsa20 version 3.

    More references:
    ----------------
      http://www.seanet.com/~bugbee/crypto/salsa20/          [pySalsa20]
      http://cr.yp.to/snuffle.html        [The original name of Salsa20]
      http://cr.yp.to/snuffle/salsafamily-20071225.pdf [ Salsa20 design]
      http://www.tiac.net/~sw/2010/02/PureSalsa20
    
    THIS PROGRAM IS PROVIDED WITHOUT WARRANTY OR GUARANTEE OF
    ANY KIND.  USE AT YOUR OWN RISK.  

    Cheers,

    Steve Witham sw at remove-this tiac dot net
    February, 2010
"""
from array import array
from struct import Struct
little_u64 = Struct('<Q')
little16_i32 = Struct('<16i')
little4_i32 = Struct('<4i')
little2_i32 = Struct('<2i')
_version = 'p3.2'

class Salsa20(object):

    def __init__(self, key=None, IV=None, rounds=20):
        self._lastChunk64 = True
        self._IVbitlen = 64
        self.ctx = [0] * 16
        if key:
            self.setKey(key)
        if IV:
            self.setIV(IV)
        self.setRounds(rounds)

    def setKey(self, key):
        assert type(key) == str
        ctx = self.ctx
        if len(key) == 32:
            constants = 'expand 32-byte k'
            ctx[1], ctx[2], ctx[3], ctx[4] = little4_i32.unpack(key[0:16])
            ctx[11], ctx[12], ctx[13], ctx[14] = little4_i32.unpack(key[16:32])
        elif len(key) == 16:
            constants = 'expand 16-byte k'
            ctx[1], ctx[2], ctx[3], ctx[4] = little4_i32.unpack(key[0:16])
            ctx[11], ctx[12], ctx[13], ctx[14] = little4_i32.unpack(key[0:16])
        else:
            raise Exception("key length isn't 32 or 16 bytes.")
        ctx[0], ctx[5], ctx[10], ctx[15] = little4_i32.unpack(constants)

    def setIV--- This code section failed: ---

 L. 208         0  LOAD_GLOBAL           0  'type'
                3  LOAD_FAST             1  'IV'
                6  CALL_FUNCTION_1       1  None
                9  LOAD_GLOBAL           1  'str'
               12  COMPARE_OP            2  ==
               15  POP_JUMP_IF_TRUE     24  'to 24'
               18  LOAD_ASSERT              AssertionError
               21  RAISE_VARARGS_1       1  None

 L. 209        24  LOAD_GLOBAL           3  'len'
               27  LOAD_FAST             1  'IV'
               30  CALL_FUNCTION_1       1  None
               33  LOAD_CONST               8
               36  BINARY_MULTIPLY  
               37  LOAD_CONST               64
               40  COMPARE_OP            2  ==
               43  POP_JUMP_IF_TRUE     55  'to 55'
               46  LOAD_ASSERT              AssertionError
               49  LOAD_CONST               'nonce (IV) not 64 bits'
               52  RAISE_VARARGS_2       2  None

 L. 210        55  LOAD_FAST             1  'IV'
               58  LOAD_FAST             0  'self'
               61  STORE_ATTR            4  'IV'

 L. 211        64  LOAD_FAST             0  'self'
               67  LOAD_ATTR             5  'ctx'
               70  STORE_FAST            2  'ctx'

 L. 212        73  LOAD_GLOBAL           6  'little2_i32'
               76  LOAD_ATTR             7  'unpack'
               79  LOAD_FAST             1  'IV'
               82  CALL_FUNCTION_1       1  None
               85  UNPACK_SEQUENCE_2     2 
               88  LOAD_FAST             2  'ctx'
               91  LOAD_CONST               6
               94  STORE_SUBSCR     
               95  LOAD_FAST             2  'ctx'
               98  LOAD_CONST               7
              101  STORE_SUBSCR     

 L. 213       102  LOAD_CONST               (0, 0)
              105  UNPACK_SEQUENCE_2     2 
              108  LOAD_FAST             2  'ctx'
              111  LOAD_CONST               8
              114  STORE_SUBSCR     
              115  LOAD_FAST             2  'ctx'
              118  LOAD_CONST               9
              121  STORE_SUBSCR     

Parse error at or near `LOAD_CONST' instruction at offset 118

    setNonce = setIV

    def setCounter--- This code section failed: ---

 L. 219         0  LOAD_GLOBAL           0  'type'
                3  LOAD_FAST             1  'counter'
                6  CALL_FUNCTION_1       1  None
                9  LOAD_GLOBAL           1  'int'
               12  LOAD_GLOBAL           2  'long'
               15  BUILD_TUPLE_2         2 
               18  COMPARE_OP            6  in
               21  POP_JUMP_IF_TRUE     30  'to 30'
               24  LOAD_ASSERT              AssertionError
               27  RAISE_VARARGS_1       1  None

 L. 220        30  LOAD_CONST               0
               33  LOAD_FAST             1  'counter'
               36  DUP_TOP          
               37  ROT_THREE        
               38  COMPARE_OP            1  <=
               41  JUMP_IF_FALSE_OR_POP    53  'to 53'
               44  LOAD_CONST               18446744073709551616
               47  COMPARE_OP            0  <
               50  JUMP_FORWARD          2  'to 55'
             53_0  COME_FROM            41  '41'
               53  ROT_TWO          
               54  POP_TOP          
             55_0  COME_FROM            50  '50'
               55  POP_JUMP_IF_TRUE     67  'to 67'
               58  LOAD_ASSERT              AssertionError
               61  LOAD_CONST               'counter < 0 or >= 2**64'
               64  RAISE_VARARGS_2       2  None

 L. 221        67  LOAD_FAST             0  'self'
               70  LOAD_ATTR             4  'ctx'
               73  STORE_FAST            2  'ctx'

 L. 222        76  LOAD_GLOBAL           5  'little2_i32'
               79  LOAD_ATTR             6  'unpack'
               82  LOAD_GLOBAL           7  'little_u64'
               85  LOAD_ATTR             8  'pack'
               88  LOAD_FAST             1  'counter'
               91  CALL_FUNCTION_1       1  None
               94  CALL_FUNCTION_1       1  None
               97  UNPACK_SEQUENCE_2     2 
              100  LOAD_FAST             2  'ctx'
              103  LOAD_CONST               8
              106  STORE_SUBSCR     
              107  LOAD_FAST             2  'ctx'
              110  LOAD_CONST               9
              113  STORE_SUBSCR     

Parse error at or near `LOAD_CONST' instruction at offset 110

    def getCounter(self):
        return little_u64.unpack(little2_i32.pack(*self.ctx[8:10]))[0]

    def setRounds--- This code section failed: ---

 L. 229         0  LOAD_FAST             2  'testing'
                3  POP_JUMP_IF_TRUE     27  'to 27'
                6  LOAD_FAST             1  'rounds'
                9  LOAD_CONST               (8, 12, 20)
               12  COMPARE_OP            6  in
               15  POP_JUMP_IF_TRUE     27  'to 27'
               18  LOAD_ASSERT              AssertionError
               21  LOAD_CONST               'rounds must be 8, 12, 20'
               24  RAISE_VARARGS_2       2  None

 L. 230        27  LOAD_FAST             1  'rounds'
               30  LOAD_FAST             0  'self'
               33  STORE_ATTR            1  'rounds'

Parse error at or near `LOAD_FAST' instruction at offset 30

    def encryptBytes--- This code section failed: ---

 L. 234         0  LOAD_GLOBAL           0  'type'
                3  LOAD_FAST             1  'data'
                6  CALL_FUNCTION_1       1  None
                9  LOAD_GLOBAL           1  'str'
               12  COMPARE_OP            2  ==
               15  POP_JUMP_IF_TRUE     27  'to 27'
               18  LOAD_ASSERT              AssertionError
               21  LOAD_CONST               'data must be byte string'
               24  RAISE_VARARGS_2       2  None

 L. 235        27  LOAD_FAST             0  'self'
               30  LOAD_ATTR             3  '_lastChunk64'
               33  POP_JUMP_IF_TRUE     45  'to 45'
               36  LOAD_ASSERT              AssertionError
               39  LOAD_CONST               'previous chunk not multiple of 64 bytes'
               42  RAISE_VARARGS_2       2  None

 L. 236        45  LOAD_GLOBAL           4  'len'
               48  LOAD_FAST             1  'data'
               51  CALL_FUNCTION_1       1  None
               54  STORE_FAST            2  'lendata'

 L. 237        57  LOAD_GLOBAL           5  'array'
               60  LOAD_CONST               'c'
               63  LOAD_CONST               '\x00'
               66  LOAD_FAST             2  'lendata'
               69  BINARY_MULTIPLY  
               70  CALL_FUNCTION_2       2  None
               73  STORE_FAST            3  'munged'

 L. 238        76  SETUP_LOOP          164  'to 243'
               79  LOAD_GLOBAL           6  'xrange'
               82  LOAD_CONST               0
               85  LOAD_FAST             2  'lendata'
               88  LOAD_CONST               64
               91  CALL_FUNCTION_3       3  None
               94  GET_ITER         
               95  FOR_ITER            144  'to 242'
               98  STORE_FAST            4  'i'

 L. 239       101  LOAD_GLOBAL           7  'salsa20_wordtobyte'
              104  LOAD_FAST             0  'self'
              107  LOAD_ATTR             8  'ctx'
              110  LOAD_FAST             0  'self'
              113  LOAD_ATTR             9  'rounds'
              116  LOAD_CONST               'checkRounds'
              119  LOAD_GLOBAL          10  'False'
              122  CALL_FUNCTION_258   258  None
              125  STORE_FAST            5  'h'

 L. 240       128  LOAD_FAST             0  'self'
              131  LOAD_ATTR            11  'setCounter'
              134  LOAD_FAST             0  'self'
              137  LOAD_ATTR            12  'getCounter'
              140  CALL_FUNCTION_0       0  None
              143  LOAD_CONST               1
              146  BINARY_ADD       
              147  LOAD_CONST               18446744073709551616
              150  BINARY_MODULO    
              151  CALL_FUNCTION_1       1  None
              154  POP_TOP          

 L. 242       155  SETUP_LOOP           81  'to 239'
              158  LOAD_GLOBAL           6  'xrange'
              161  LOAD_GLOBAL          13  'min'
              164  LOAD_CONST               64
              167  LOAD_FAST             2  'lendata'
              170  LOAD_FAST             4  'i'
              173  BINARY_SUBTRACT  
              174  CALL_FUNCTION_2       2  None
              177  CALL_FUNCTION_1       1  None
              180  GET_ITER         
              181  FOR_ITER             54  'to 238'
              184  STORE_FAST            6  'j'

 L. 243       187  LOAD_GLOBAL          14  'chr'
              190  LOAD_GLOBAL          15  'ord'
              193  LOAD_FAST             1  'data'
              196  LOAD_FAST             4  'i'
              199  LOAD_FAST             6  'j'
              202  BINARY_ADD       
              203  BINARY_SUBSCR    
              204  CALL_FUNCTION_1       1  None
              207  LOAD_GLOBAL          15  'ord'
              210  LOAD_FAST             5  'h'
              213  LOAD_FAST             6  'j'
              216  BINARY_SUBSCR    
              217  CALL_FUNCTION_1       1  None
              220  BINARY_XOR       
              221  CALL_FUNCTION_1       1  None
              224  LOAD_FAST             3  'munged'
              227  LOAD_FAST             4  'i'
              230  LOAD_FAST             6  'j'
              233  BINARY_ADD       
              234  STORE_SUBSCR     
              235  JUMP_BACK           181  'to 181'
              238  POP_BLOCK        
            239_0  COME_FROM           155  '155'
              239  JUMP_BACK            95  'to 95'
              242  POP_BLOCK        
            243_0  COME_FROM            76  '76'

 L. 245       243  LOAD_FAST             2  'lendata'
              246  LOAD_CONST               64
              249  BINARY_MODULO    
              250  UNARY_NOT        
              251  LOAD_FAST             0  'self'
              254  STORE_ATTR            3  '_lastChunk64'

 L. 246       257  LOAD_FAST             3  'munged'
              260  LOAD_ATTR            16  'tostring'
              263  CALL_FUNCTION_0       0  None
              266  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 266

    decryptBytes = encryptBytes


def salsa20_wordtobyte(input, nRounds=20, checkRounds=True):
    """ Do nRounds Salsa20 rounds on a copy of 
            input: list or tuple of 16 ints treated as little-endian unsigneds.
        Returns a 64-byte string.
        """
    assert type(input) in (list, tuple) and len(input) == 16
    assert not checkRounds or nRounds in (8, 12, 20)
    x = list(input)

    def XOR(a, b):
        return a ^ b

    ROTATE = rot32
    PLUS = add32
    for i in range(nRounds / 2):
        x[4] = XOR(x[4], ROTATE(PLUS(x[0], x[12]), 7))
        x[8] = XOR(x[8], ROTATE(PLUS(x[4], x[0]), 9))
        x[12] = XOR(x[12], ROTATE(PLUS(x[8], x[4]), 13))
        x[0] = XOR(x[0], ROTATE(PLUS(x[12], x[8]), 18))
        x[9] = XOR(x[9], ROTATE(PLUS(x[5], x[1]), 7))
        x[13] = XOR(x[13], ROTATE(PLUS(x[9], x[5]), 9))
        x[1] = XOR(x[1], ROTATE(PLUS(x[13], x[9]), 13))
        x[5] = XOR(x[5], ROTATE(PLUS(x[1], x[13]), 18))
        x[14] = XOR(x[14], ROTATE(PLUS(x[10], x[6]), 7))
        x[2] = XOR(x[2], ROTATE(PLUS(x[14], x[10]), 9))
        x[6] = XOR(x[6], ROTATE(PLUS(x[2], x[14]), 13))
        x[10] = XOR(x[10], ROTATE(PLUS(x[6], x[2]), 18))
        x[3] = XOR(x[3], ROTATE(PLUS(x[15], x[11]), 7))
        x[7] = XOR(x[7], ROTATE(PLUS(x[3], x[15]), 9))
        x[11] = XOR(x[11], ROTATE(PLUS(x[7], x[3]), 13))
        x[15] = XOR(x[15], ROTATE(PLUS(x[11], x[7]), 18))
        x[1] = XOR(x[1], ROTATE(PLUS(x[0], x[3]), 7))
        x[2] = XOR(x[2], ROTATE(PLUS(x[1], x[0]), 9))
        x[3] = XOR(x[3], ROTATE(PLUS(x[2], x[1]), 13))
        x[0] = XOR(x[0], ROTATE(PLUS(x[3], x[2]), 18))
        x[6] = XOR(x[6], ROTATE(PLUS(x[5], x[4]), 7))
        x[7] = XOR(x[7], ROTATE(PLUS(x[6], x[5]), 9))
        x[4] = XOR(x[4], ROTATE(PLUS(x[7], x[6]), 13))
        x[5] = XOR(x[5], ROTATE(PLUS(x[4], x[7]), 18))
        x[11] = XOR(x[11], ROTATE(PLUS(x[10], x[9]), 7))
        x[8] = XOR(x[8], ROTATE(PLUS(x[11], x[10]), 9))
        x[9] = XOR(x[9], ROTATE(PLUS(x[8], x[11]), 13))
        x[10] = XOR(x[10], ROTATE(PLUS(x[9], x[8]), 18))
        x[12] = XOR(x[12], ROTATE(PLUS(x[15], x[14]), 7))
        x[13] = XOR(x[13], ROTATE(PLUS(x[12], x[15]), 9))
        x[14] = XOR(x[14], ROTATE(PLUS(x[13], x[12]), 13))
        x[15] = XOR(x[15], ROTATE(PLUS(x[14], x[13]), 18))

    for i in range(len(input)):
        x[i] = PLUS(x[i], input[i])

    return little16_i32.pack(*x)


def trunc32(w):
    """ Return the bottom 32 bits of w as a Python int.
        This creates longs temporarily, but returns an int. """
    w = int(w & 2147483647 | -(w & 2147483648))
    assert type(w) == int
    return w


def add32(a, b):
    """ Add two 32-bit words discarding carry above 32nd bit,
        and without creating a Python long.
        Timing shouldn't vary.
    """
    lo = (a & 65535) + (b & 65535)
    hi = (a >> 16) + (b >> 16) + (lo >> 16)
    return (-(hi & 32768) | hi & 32767) << 16 | lo & 65535


def rot32(w, nLeft):
    """ Rotate 32-bit word left by nLeft or right by -nLeft
        without creating a Python long.
        Timing depends on nLeft but not on w.
    """
    nLeft &= 31
    if nLeft == 0:
        return w
    RRR = (w >> 1 & 2147483647) >> 31 - nLeft
    sLLLLLL = -(1 << 31 - nLeft & w) | 2147483647 >> nLeft & w
    return RRR | sLLLLLL << nLeft