# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\paramiko\ber.py
from paramiko.common import max_byte, zero_byte
from paramiko.py3compat import b, byte_ord, byte_chr, long
import paramiko.util as util

class BERException(Exception):
    pass


class BER(object):
    __doc__ = "\n    Robey's tiny little attempt at a BER decoder.\n    "

    def __init__(self, content=bytes()):
        self.content = b(content)
        self.idx = 0

    def asbytes(self):
        return self.content

    def __str__(self):
        return self.asbytes()

    def __repr__(self):
        return "BER('" + repr(self.content) + "')"

    def decode(self):
        return self.decode_next()

    def decode_next--- This code section failed: ---

 L.  50         0  LOAD_FAST                'self'
                2  LOAD_ATTR                idx
                4  LOAD_GLOBAL              len
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                content
               10  CALL_FUNCTION_1       1  '1 positional argument'
               12  COMPARE_OP               >=
               14  POP_JUMP_IF_FALSE    20  'to 20'

 L.  51        16  LOAD_CONST               None
               18  RETURN_VALUE     
             20_0  COME_FROM            14  '14'

 L.  52        20  LOAD_GLOBAL              byte_ord
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                content
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                idx
               30  BINARY_SUBSCR    
               32  CALL_FUNCTION_1       1  '1 positional argument'
               34  STORE_FAST               'ident'

 L.  53        36  LOAD_FAST                'self'
               38  DUP_TOP          
               40  LOAD_ATTR                idx
               42  LOAD_CONST               1
               44  INPLACE_ADD      
               46  ROT_TWO          
               48  STORE_ATTR               idx

 L.  54        50  LOAD_FAST                'ident'
               52  LOAD_CONST               31
               54  BINARY_AND       
               56  LOAD_CONST               31
               58  COMPARE_OP               ==
               60  POP_JUMP_IF_FALSE   144  'to 144'

 L.  56        62  LOAD_CONST               0
               64  STORE_FAST               'ident'

 L.  57        66  SETUP_LOOP          144  'to 144'
             68_0  COME_FROM           136  '136'
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                idx
               72  LOAD_GLOBAL              len
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                content
               78  CALL_FUNCTION_1       1  '1 positional argument'
               80  COMPARE_OP               <
               82  POP_JUMP_IF_FALSE   142  'to 142'

 L.  58        84  LOAD_GLOBAL              byte_ord
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                content
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                idx
               94  BINARY_SUBSCR    
               96  CALL_FUNCTION_1       1  '1 positional argument'
               98  STORE_FAST               't'

 L.  59       100  LOAD_FAST                'self'
              102  DUP_TOP          
              104  LOAD_ATTR                idx
              106  LOAD_CONST               1
              108  INPLACE_ADD      
              110  ROT_TWO          
              112  STORE_ATTR               idx

 L.  60       114  LOAD_FAST                'ident'
              116  LOAD_CONST               7
              118  BINARY_LSHIFT    
              120  LOAD_FAST                't'
              122  LOAD_CONST               127
              124  BINARY_AND       
              126  BINARY_OR        
              128  STORE_FAST               'ident'

 L.  61       130  LOAD_FAST                't'
              132  LOAD_CONST               128
              134  BINARY_AND       
              136  POP_JUMP_IF_TRUE     68  'to 68'

 L.  62       138  BREAK_LOOP       
              140  JUMP_BACK            68  'to 68'
            142_0  COME_FROM            82  '82'
              142  POP_BLOCK        
            144_0  COME_FROM_LOOP       66  '66'
            144_1  COME_FROM            60  '60'

 L.  63       144  LOAD_FAST                'self'
              146  LOAD_ATTR                idx
              148  LOAD_GLOBAL              len
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                content
              154  CALL_FUNCTION_1       1  '1 positional argument'
              156  COMPARE_OP               >=
              158  POP_JUMP_IF_FALSE   164  'to 164'

 L.  64       160  LOAD_CONST               None
              162  RETURN_VALUE     
            164_0  COME_FROM           158  '158'

 L.  66       164  LOAD_GLOBAL              byte_ord
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                content
              170  LOAD_FAST                'self'
              172  LOAD_ATTR                idx
              174  BINARY_SUBSCR    
              176  CALL_FUNCTION_1       1  '1 positional argument'
              178  STORE_FAST               'size'

 L.  67       180  LOAD_FAST                'self'
              182  DUP_TOP          
              184  LOAD_ATTR                idx
              186  LOAD_CONST               1
              188  INPLACE_ADD      
              190  ROT_TWO          
              192  STORE_ATTR               idx

 L.  68       194  LOAD_FAST                'size'
              196  LOAD_CONST               128
              198  BINARY_AND       
          200_202  POP_JUMP_IF_FALSE   280  'to 280'

 L.  71       204  LOAD_FAST                'size'
              206  LOAD_CONST               127
              208  BINARY_AND       
              210  STORE_FAST               't'

 L.  72       212  LOAD_FAST                'self'
              214  LOAD_ATTR                idx
              216  LOAD_FAST                't'
              218  BINARY_ADD       
              220  LOAD_GLOBAL              len
              222  LOAD_FAST                'self'
              224  LOAD_ATTR                content
              226  CALL_FUNCTION_1       1  '1 positional argument'
              228  COMPARE_OP               >
              230  POP_JUMP_IF_FALSE   236  'to 236'

 L.  73       232  LOAD_CONST               None
              234  RETURN_VALUE     
            236_0  COME_FROM           230  '230'

 L.  74       236  LOAD_GLOBAL              util
              238  LOAD_METHOD              inflate_long

 L.  75       240  LOAD_FAST                'self'
              242  LOAD_ATTR                content
              244  LOAD_FAST                'self'
              246  LOAD_ATTR                idx
              248  LOAD_FAST                'self'
              250  LOAD_ATTR                idx
              252  LOAD_FAST                't'
              254  BINARY_ADD       
              256  BUILD_SLICE_2         2 
              258  BINARY_SUBSCR    
              260  LOAD_CONST               True
              262  CALL_METHOD_2         2  '2 positional arguments'
              264  STORE_FAST               'size'

 L.  77       266  LOAD_FAST                'self'
              268  DUP_TOP          
              270  LOAD_ATTR                idx
              272  LOAD_FAST                't'
              274  INPLACE_ADD      
              276  ROT_TWO          
              278  STORE_ATTR               idx
            280_0  COME_FROM           200  '200'

 L.  78       280  LOAD_FAST                'self'
              282  LOAD_ATTR                idx
              284  LOAD_FAST                'size'
              286  BINARY_ADD       
              288  LOAD_GLOBAL              len
              290  LOAD_FAST                'self'
              292  LOAD_ATTR                content
              294  CALL_FUNCTION_1       1  '1 positional argument'
              296  COMPARE_OP               >
          298_300  POP_JUMP_IF_FALSE   306  'to 306'

 L.  80       302  LOAD_CONST               None
              304  RETURN_VALUE     
            306_0  COME_FROM           298  '298'

 L.  81       306  LOAD_FAST                'self'
              308  LOAD_ATTR                content
              310  LOAD_FAST                'self'
              312  LOAD_ATTR                idx
              314  LOAD_FAST                'self'
              316  LOAD_ATTR                idx
              318  LOAD_FAST                'size'
              320  BINARY_ADD       
              322  BUILD_SLICE_2         2 
              324  BINARY_SUBSCR    
              326  STORE_FAST               'data'

 L.  82       328  LOAD_FAST                'self'
              330  DUP_TOP          
              332  LOAD_ATTR                idx
              334  LOAD_FAST                'size'
              336  INPLACE_ADD      
              338  ROT_TWO          
              340  STORE_ATTR               idx

 L.  84       342  LOAD_FAST                'ident'
              344  LOAD_CONST               48
              346  COMPARE_OP               ==
          348_350  POP_JUMP_IF_FALSE   362  'to 362'

 L.  86       352  LOAD_FAST                'self'
              354  LOAD_METHOD              decode_sequence
              356  LOAD_FAST                'data'
              358  CALL_METHOD_1         1  '1 positional argument'
              360  RETURN_VALUE     
            362_0  COME_FROM           348  '348'

 L.  87       362  LOAD_FAST                'ident'
              364  LOAD_CONST               2
              366  COMPARE_OP               ==
          368_370  POP_JUMP_IF_FALSE   382  'to 382'

 L.  89       372  LOAD_GLOBAL              util
              374  LOAD_METHOD              inflate_long
              376  LOAD_FAST                'data'
              378  CALL_METHOD_1         1  '1 positional argument'
              380  RETURN_VALUE     
            382_0  COME_FROM           368  '368'

 L.  92       382  LOAD_STR                 'Unknown ber encoding type {:d} (robey is lazy)'
              384  STORE_FAST               'msg'

 L.  93       386  LOAD_GLOBAL              BERException
              388  LOAD_FAST                'msg'
              390  LOAD_METHOD              format
              392  LOAD_FAST                'ident'
              394  CALL_METHOD_1         1  '1 positional argument'
              396  CALL_FUNCTION_1       1  '1 positional argument'
              398  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `POP_BLOCK' instruction at offset 142

    @staticmethod
    def decode_sequence(data):
        out = []
        ber = BER(data)
        while True:
            x = ber.decode_next()
            if x is None:
                break
            out.appendx

        return out

    def encode_tlv(self, ident, val):
        self.content += byte_chr(ident)
        if len(val) > 127:
            lenstr = util.deflate_longlen(val)
            self.content += byte_chr(128 + len(lenstr)) + lenstr
        else:
            self.content += byte_chr(len(val))
        self.content += val

    def encode(self, x):
        if type(x) is bool:
            if x:
                self.encode_tlv1max_byte
            else:
                self.encode_tlv1zero_byte
        elif type(x) is int or type(x) is long:
            self.encode_tlv2util.deflate_longx
        else:
            if type(x) is str:
                self.encode_tlv4x
            else:
                if type(x) is list or type(x) is tuple:
                    self.encode_tlv48self.encode_sequencex
                else:
                    raise BERException('Unknown type for encoding: {!r}'.formattype(x))

    @staticmethod
    def encode_sequence(data):
        ber = BER()
        for item in data:
            ber.encodeitem

        return ber.asbytes()