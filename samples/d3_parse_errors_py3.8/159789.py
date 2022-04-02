# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\mechanize\_equiv.py
from __future__ import absolute_import, division, print_function, unicode_literals
import re, string
from ._entities import html5_entities
from .polyglot import codepoint_to_chr
space_chars = frozenset(('\t', '\n', '\x0c', ' ', '\r'))
space_chars_bytes = frozenset((item.encode('ascii') for item in space_chars))
ascii_letters_bytes = frozenset((item.encode('ascii') for item in string.ascii_letters))
spaces_angle_brackets = space_chars_bytes | frozenset((b'>', b'<'))
skip1 = space_chars_bytes | frozenset((b'/', ))
head_elems = frozenset((b'html', b'head', b'title', b'base', b'script', b'style', b'meta',
                        b'link', b'object'))

def my_unichr--- This code section failed: ---

 L.  26         0  SETUP_FINALLY        12  'to 12'

 L.  27         2  LOAD_GLOBAL              codepoint_to_chr
                4  LOAD_FAST                'num'
                6  CALL_FUNCTION_1       1  ''
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L.  28        12  DUP_TOP          
               14  LOAD_GLOBAL              ValueError
               16  LOAD_GLOBAL              OverflowError
               18  BUILD_TUPLE_2         2 
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    36  'to 36'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.  29        30  POP_EXCEPT       
               32  LOAD_STR                 '?'
               34  RETURN_VALUE     
             36_0  COME_FROM            22  '22'
               36  END_FINALLY      

Parse error at or near `LOAD_STR' instruction at offset 32


def replace_entity--- This code section failed: ---

 L.  33         0  LOAD_FAST                'match'
                2  LOAD_METHOD              group
                4  LOAD_CONST               1
                6  CALL_METHOD_1         1  ''
                8  LOAD_METHOD              lower
               10  CALL_METHOD_0         0  ''
               12  STORE_FAST               'ent'

 L.  34        14  LOAD_FAST                'ent'
               16  LOAD_CONST               frozenset({'apos', 'squot'})
               18  COMPARE_OP               in
               20  POP_JUMP_IF_FALSE    26  'to 26'

 L.  36        22  LOAD_STR                 "'"
               24  RETURN_VALUE     
             26_0  COME_FROM            20  '20'

 L.  37        26  LOAD_FAST                'ent'
               28  LOAD_STR                 'hellips'
               30  COMPARE_OP               ==
               32  POP_JUMP_IF_FALSE    38  'to 38'

 L.  38        34  LOAD_STR                 'hellip'
               36  STORE_FAST               'ent'
             38_0  COME_FROM            32  '32'

 L.  39        38  LOAD_FAST                'ent'
               40  LOAD_METHOD              startswith
               42  LOAD_STR                 '#'
               44  CALL_METHOD_1         1  ''
               46  POP_JUMP_IF_FALSE   196  'to 196'

 L.  40        48  SETUP_FINALLY       102  'to 102'

 L.  41        50  LOAD_FAST                'ent'
               52  LOAD_CONST               1
               54  BINARY_SUBSCR    
               56  LOAD_CONST               ('x', 'X')
               58  COMPARE_OP               in
               60  POP_JUMP_IF_FALSE    82  'to 82'

 L.  42        62  LOAD_GLOBAL              int
               64  LOAD_FAST                'ent'
               66  LOAD_CONST               2
               68  LOAD_CONST               None
               70  BUILD_SLICE_2         2 
               72  BINARY_SUBSCR    
               74  LOAD_CONST               16
               76  CALL_FUNCTION_2       2  ''
               78  STORE_FAST               'num'
               80  JUMP_FORWARD         98  'to 98'
             82_0  COME_FROM            60  '60'

 L.  44        82  LOAD_GLOBAL              int
               84  LOAD_FAST                'ent'
               86  LOAD_CONST               1
               88  LOAD_CONST               None
               90  BUILD_SLICE_2         2 
               92  BINARY_SUBSCR    
               94  CALL_FUNCTION_1       1  ''
               96  STORE_FAST               'num'
             98_0  COME_FROM            80  '80'
               98  POP_BLOCK        
              100  JUMP_FORWARD        134  'to 134'
            102_0  COME_FROM_FINALLY    48  '48'

 L.  45       102  DUP_TOP          
              104  LOAD_GLOBAL              Exception
              106  COMPARE_OP               exception-match
              108  POP_JUMP_IF_FALSE   132  'to 132'
              110  POP_TOP          
              112  POP_TOP          
              114  POP_TOP          

 L.  46       116  LOAD_STR                 '&'
              118  LOAD_FAST                'ent'
              120  BINARY_ADD       
              122  LOAD_STR                 ';'
              124  BINARY_ADD       
              126  ROT_FOUR         
              128  POP_EXCEPT       
              130  RETURN_VALUE     
            132_0  COME_FROM           108  '108'
              132  END_FINALLY      
            134_0  COME_FROM           100  '100'

 L.  47       134  LOAD_FAST                'num'
              136  LOAD_CONST               255
              138  COMPARE_OP               >
              140  POP_JUMP_IF_FALSE   150  'to 150'

 L.  48       142  LOAD_GLOBAL              my_unichr
              144  LOAD_FAST                'num'
              146  CALL_FUNCTION_1       1  ''
              148  RETURN_VALUE     
            150_0  COME_FROM           140  '140'

 L.  49       150  SETUP_FINALLY       168  'to 168'

 L.  50       152  LOAD_GLOBAL              chr
              154  LOAD_FAST                'num'
              156  CALL_FUNCTION_1       1  ''
              158  LOAD_METHOD              decode
              160  LOAD_STR                 'cp1252'
              162  CALL_METHOD_1         1  ''
              164  POP_BLOCK        
              166  RETURN_VALUE     
            168_0  COME_FROM_FINALLY   150  '150'

 L.  51       168  DUP_TOP          
              170  LOAD_GLOBAL              UnicodeDecodeError
              172  COMPARE_OP               exception-match
              174  POP_JUMP_IF_FALSE   194  'to 194'
              176  POP_TOP          
              178  POP_TOP          
              180  POP_TOP          

 L.  52       182  LOAD_GLOBAL              my_unichr
              184  LOAD_FAST                'num'
              186  CALL_FUNCTION_1       1  ''
              188  ROT_FOUR         
              190  POP_EXCEPT       
              192  RETURN_VALUE     
            194_0  COME_FROM           174  '174'
              194  END_FINALLY      
            196_0  COME_FROM            46  '46'

 L.  53       196  SETUP_FINALLY       208  'to 208'

 L.  54       198  LOAD_GLOBAL              html5_entities
              200  LOAD_FAST                'ent'
              202  BINARY_SUBSCR    
              204  POP_BLOCK        
              206  RETURN_VALUE     
            208_0  COME_FROM_FINALLY   196  '196'

 L.  55       208  DUP_TOP          
              210  LOAD_GLOBAL              KeyError
              212  COMPARE_OP               exception-match
              214  POP_JUMP_IF_FALSE   226  'to 226'
              216  POP_TOP          
              218  POP_TOP          
              220  POP_TOP          

 L.  56       222  POP_EXCEPT       
              224  JUMP_FORWARD        228  'to 228'
            226_0  COME_FROM           214  '214'
              226  END_FINALLY      
            228_0  COME_FROM           224  '224'

 L.  57       228  LOAD_STR                 '&'
              230  LOAD_FAST                'ent'
              232  BINARY_ADD       
              234  LOAD_STR                 ';'
              236  BINARY_ADD       
              238  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 226_0


class Bytes(bytes):
    __doc__ = 'String-like object with an associated position and various extra methods\n    If the position is ever greater than the string length then an exception is\n    raised'

    def __init__(self, value):
        self._position = -1

    def __iter__(self):
        return self

    def __next__(self):
        p = self._position = self._position + 1
        if p >= len(self):
            raise StopIteration
        elif p < 0:
            raise TypeError
        return self[p:p + 1]

    def next(self):
        return self.__next__

    def previous(self):
        p = self._position
        if p >= len(self):
            raise StopIteration
        elif p < 0:
            raise TypeError
        self._position = p = p - 1
        return self[p:p + 1]

    @property
    def position(self):
        if self._position >= len(self):
            raise StopIteration
        if self._position >= 0:
            return self._position

    @position.setter
    def position(self, position):
        if self._position >= len(self):
            raise StopIteration
        self._position = position

    @property
    def current_byte(self):
        return self[self.position:self.position + 1]

    def skip(self, chars=space_chars_bytes):
        """Skip past a list of characters"""
        p = self.position
        while True:
            if p < len(self):
                c = self[p:p + 1]
                if c not in chars:
                    self._position = p
                    return c
                p += 1

        self._position = p

    def skip_until(self, chars):
        p = pos = self.position
        while True:
            if p < len(self):
                c = self[p:p + 1]
                if c in chars:
                    self._position = p
                    return (
                     self[pos:p], c)
                p += 1

        self._position = p
        return (b'', b'')

    def match_bytes(self, bytes):
        """Look for a sequence of bytes at the start of a string. If the bytes
        are found return True and advance the position to the byte after the
        match. Otherwise return False and leave the position alone"""
        p = self.position
        data = self[p:p + len(bytes)]
        rv = data.startswith(bytes)
        if rv:
            self.position += len(bytes)
        return rv

    def match_bytes_pat(self, pat):
        bytes = pat.pattern
        m = pat.match(self, self.position)
        if m is None:
            return False
        bytes = m.group
        self.position += len(bytes)
        return True

    def jump_to(self, bytes):
        """Look for the next sequence of bytes matching a given sequence. If
        a match is found advance the position to the last byte of the match"""
        new_pos = self.find(bytes, max0self.position)
        if new_pos > -1:
            new_pos -= self.position
            if self._position == -1:
                self._position = 0
            self._position += new_pos + len(bytes) - 1
            return True
        raise StopIteration


class HTTPEquivParser(object):
    __doc__ = 'Mini parser for detecting http-equiv headers from meta tags '

    def __init__(self, data):
        """string - the data to work on """
        self.data = Bytes(data)
        self.headers = []

    def __call__--- This code section failed: ---

 L. 175         0  LOAD_FAST                'self'
                2  LOAD_ATTR                data
                4  LOAD_ATTR                match_bytes
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                data
               10  LOAD_ATTR                match_bytes_pat
               12  ROT_TWO          
               14  STORE_FAST               'mb'
               16  STORE_FAST               'mbp'

 L. 177        18  LOAD_FAST                'mb'
               20  LOAD_CONST               b'<!--'
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                handle_comment
               26  BUILD_TUPLE_3         3 

 L. 178        28  LOAD_FAST                'mbp'
               30  LOAD_GLOBAL              re
               32  LOAD_ATTR                compile
               34  LOAD_CONST               b'<meta'
               36  LOAD_GLOBAL              re
               38  LOAD_ATTR                IGNORECASE
               40  LOAD_CONST               ('flags',)
               42  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 179        44  LOAD_FAST                'self'
               46  LOAD_ATTR                handle_meta

 L. 178        48  BUILD_TUPLE_3         3 

 L. 180        50  LOAD_FAST                'mbp'
               52  LOAD_GLOBAL              re
               54  LOAD_ATTR                compile
               56  LOAD_CONST               b'</head'
               58  LOAD_GLOBAL              re
               60  LOAD_ATTR                IGNORECASE
               62  LOAD_CONST               ('flags',)
               64  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 181        66  LOAD_LAMBDA              '<code_object <lambda>>'
               68  LOAD_STR                 'HTTPEquivParser.__call__.<locals>.<lambda>'
               70  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 180        72  BUILD_TUPLE_3         3 

 L. 182        74  LOAD_FAST                'mb'
               76  LOAD_CONST               b'</'
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                handle_possible_end_tag
               82  BUILD_TUPLE_3         3 

 L. 183        84  LOAD_FAST                'mb'
               86  LOAD_CONST               b'<!'
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                handle_other
               92  BUILD_TUPLE_3         3 

 L. 184        94  LOAD_FAST                'mb'
               96  LOAD_CONST               b'<?'
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                handle_other
              102  BUILD_TUPLE_3         3 

 L. 185       104  LOAD_FAST                'mb'
              106  LOAD_CONST               b'<'
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                handle_possible_start_tag
              112  BUILD_TUPLE_3         3 

 L. 176       114  BUILD_TUPLE_7         7 
              116  STORE_FAST               'dispatch'

 L. 187       118  LOAD_FAST                'self'
              120  LOAD_ATTR                data
              122  GET_ITER         
            124_0  COME_FROM           212  '212'
            124_1  COME_FROM           206  '206'
              124  FOR_ITER            214  'to 214'
              126  STORE_FAST               'byte'

 L. 188       128  LOAD_CONST               True
              130  STORE_FAST               'keep_parsing'

 L. 189       132  LOAD_FAST                'dispatch'
              134  GET_ITER         
            136_0  COME_FROM           202  '202'
            136_1  COME_FROM           198  '198'
            136_2  COME_FROM           170  '170'
            136_3  COME_FROM           152  '152'
              136  FOR_ITER            204  'to 204'
              138  UNPACK_SEQUENCE_3     3 
              140  STORE_FAST               'matcher'
              142  STORE_FAST               'key'
              144  STORE_FAST               'method'

 L. 190       146  LOAD_FAST                'matcher'
              148  LOAD_FAST                'key'
              150  CALL_FUNCTION_1       1  ''
              152  POP_JUMP_IF_FALSE_BACK   136  'to 136'

 L. 191       154  SETUP_FINALLY       172  'to 172'

 L. 192       156  LOAD_FAST                'method'
              158  CALL_FUNCTION_0       0  ''
              160  STORE_FAST               'keep_parsing'

 L. 193       162  POP_BLOCK        
              164  POP_TOP          
              166  JUMP_FORWARD        204  'to 204'
              168  POP_BLOCK        
              170  JUMP_BACK           136  'to 136'
            172_0  COME_FROM_FINALLY   154  '154'

 L. 194       172  DUP_TOP          
              174  LOAD_GLOBAL              StopIteration
              176  COMPARE_OP               exception-match
              178  POP_JUMP_IF_FALSE   200  'to 200'
              180  POP_TOP          
              182  POP_TOP          
              184  POP_TOP          

 L. 195       186  LOAD_CONST               False
              188  STORE_FAST               'keep_parsing'

 L. 196       190  POP_EXCEPT       
              192  POP_TOP          
              194  JUMP_FORWARD        204  'to 204'
              196  POP_EXCEPT       
              198  JUMP_BACK           136  'to 136'
            200_0  COME_FROM           178  '178'
              200  END_FINALLY      
              202  JUMP_BACK           136  'to 136'
            204_0  COME_FROM           194  '194'
            204_1  COME_FROM           166  '166'
            204_2  COME_FROM           136  '136'

 L. 197       204  LOAD_FAST                'keep_parsing'
              206  POP_JUMP_IF_TRUE_BACK   124  'to 124'

 L. 198       208  POP_TOP          
              210  BREAK_LOOP          214  'to 214'
              212  JUMP_BACK           124  'to 124'
            214_0  COME_FROM           210  '210'
            214_1  COME_FROM           124  '124'

 L. 200       214  BUILD_LIST_0          0 
              216  STORE_FAST               'ans'

 L. 201       218  LOAD_GLOBAL              re
              220  LOAD_METHOD              compile
              222  LOAD_STR                 '&(\\S+?);'
              224  CALL_METHOD_1         1  ''
              226  STORE_FAST               'entity_pat'

 L. 202       228  LOAD_FAST                'self'
              230  LOAD_ATTR                headers
              232  GET_ITER         
            234_0  COME_FROM           388  '388'
            234_1  COME_FROM           366  '366'
            234_2  COME_FROM           288  '288'
              234  FOR_ITER            390  'to 390'
              236  UNPACK_SEQUENCE_2     2 
              238  STORE_FAST               'name'
              240  STORE_FAST               'val'

 L. 203       242  SETUP_FINALLY       270  'to 270'

 L. 204       244  LOAD_FAST                'name'
              246  LOAD_METHOD              decode
              248  LOAD_STR                 'ascii'
              250  CALL_METHOD_1         1  ''
              252  LOAD_FAST                'val'
              254  LOAD_METHOD              decode
              256  LOAD_STR                 'ascii'
              258  CALL_METHOD_1         1  ''
              260  ROT_TWO          
              262  STORE_FAST               'name'
              264  STORE_FAST               'val'
              266  POP_BLOCK        
              268  JUMP_FORWARD        296  'to 296'
            270_0  COME_FROM_FINALLY   242  '242'

 L. 205       270  DUP_TOP          
              272  LOAD_GLOBAL              ValueError
              274  COMPARE_OP               exception-match
          276_278  POP_JUMP_IF_FALSE   294  'to 294'
              280  POP_TOP          
              282  POP_TOP          
              284  POP_TOP          

 L. 206       286  POP_EXCEPT       
              288  JUMP_BACK           234  'to 234'
              290  POP_EXCEPT       
              292  JUMP_FORWARD        296  'to 296'
            294_0  COME_FROM           276  '276'
              294  END_FINALLY      
            296_0  COME_FROM           292  '292'
            296_1  COME_FROM           268  '268'

 L. 207       296  LOAD_FAST                'entity_pat'
              298  LOAD_METHOD              sub
              300  LOAD_GLOBAL              replace_entity
              302  LOAD_FAST                'name'
              304  CALL_METHOD_2         2  ''
              306  STORE_FAST               'name'

 L. 208       308  LOAD_FAST                'entity_pat'
              310  LOAD_METHOD              sub
              312  LOAD_GLOBAL              replace_entity
              314  LOAD_FAST                'val'
              316  CALL_METHOD_2         2  ''
              318  STORE_FAST               'val'

 L. 209       320  SETUP_FINALLY       348  'to 348'

 L. 210       322  LOAD_FAST                'name'
              324  LOAD_METHOD              encode
              326  LOAD_STR                 'ascii'
              328  CALL_METHOD_1         1  ''
              330  LOAD_FAST                'val'
              332  LOAD_METHOD              encode
              334  LOAD_STR                 'ascii'
              336  CALL_METHOD_1         1  ''
              338  ROT_TWO          
              340  STORE_FAST               'name'
              342  STORE_FAST               'val'
              344  POP_BLOCK        
              346  JUMP_FORWARD        374  'to 374'
            348_0  COME_FROM_FINALLY   320  '320'

 L. 211       348  DUP_TOP          
              350  LOAD_GLOBAL              ValueError
              352  COMPARE_OP               exception-match
          354_356  POP_JUMP_IF_FALSE   372  'to 372'
              358  POP_TOP          
              360  POP_TOP          
              362  POP_TOP          

 L. 212       364  POP_EXCEPT       
              366  JUMP_BACK           234  'to 234'
              368  POP_EXCEPT       
              370  JUMP_FORWARD        374  'to 374'
            372_0  COME_FROM           354  '354'
              372  END_FINALLY      
            374_0  COME_FROM           370  '370'
            374_1  COME_FROM           346  '346'

 L. 213       374  LOAD_FAST                'ans'
              376  LOAD_METHOD              append
              378  LOAD_FAST                'name'
              380  LOAD_FAST                'val'
              382  BUILD_TUPLE_2         2 
              384  CALL_METHOD_1         1  ''
              386  POP_TOP          
              388  JUMP_BACK           234  'to 234'
            390_0  COME_FROM           234  '234'

 L. 214       390  LOAD_FAST                'ans'
              392  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 192

    def handle_comment(self):
        """Skip over comments"""
        return self.data.jump_to(b'-->')

    def handle_meta--- This code section failed: ---

 L. 221         0  LOAD_FAST                'self'
                2  LOAD_ATTR                data
                4  LOAD_ATTR                current_byte
                6  LOAD_GLOBAL              space_chars_bytes
                8  COMPARE_OP               not-in
               10  POP_JUMP_IF_FALSE    16  'to 16'

 L. 223        12  LOAD_CONST               True
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L. 225        16  LOAD_CONST               None
               18  DUP_TOP          
               20  STORE_FAST               'pending_header'
               22  STORE_FAST               'pending_content'
             24_0  COME_FROM           150  '150'
             24_1  COME_FROM           120  '120'
             24_2  COME_FROM           116  '116'
             24_3  COME_FROM           108  '108'

 L. 229        24  LOAD_FAST                'self'
               26  LOAD_METHOD              get_attribute
               28  CALL_METHOD_0         0  ''
               30  STORE_FAST               'attr'

 L. 230        32  LOAD_FAST                'attr'
               34  LOAD_CONST               None
               36  COMPARE_OP               is
               38  POP_JUMP_IF_FALSE    44  'to 44'

 L. 231        40  LOAD_CONST               True
               42  RETURN_VALUE     
             44_0  COME_FROM            38  '38'

 L. 232        44  LOAD_FAST                'attr'
               46  UNPACK_SEQUENCE_2     2 
               48  STORE_FAST               'name'
               50  STORE_FAST               'val'

 L. 233        52  LOAD_FAST                'name'
               54  LOAD_METHOD              lower
               56  CALL_METHOD_0         0  ''
               58  STORE_FAST               'name'

 L. 234        60  LOAD_FAST                'name'
               62  LOAD_CONST               b'http-equiv'
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE   110  'to 110'

 L. 235        68  LOAD_FAST                'val'
               70  POP_JUMP_IF_FALSE   150  'to 150'

 L. 236        72  LOAD_FAST                'val'
               74  LOAD_METHOD              lower
               76  CALL_METHOD_0         0  ''
               78  STORE_FAST               'val'

 L. 237        80  LOAD_FAST                'pending_content'
               82  POP_JUMP_IF_FALSE   104  'to 104'

 L. 238        84  LOAD_FAST                'self'
               86  LOAD_ATTR                headers
               88  LOAD_METHOD              append
               90  LOAD_FAST                'val'
               92  LOAD_FAST                'pending_content'
               94  BUILD_TUPLE_2         2 
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          

 L. 239       100  LOAD_CONST               True
              102  RETURN_VALUE     
            104_0  COME_FROM            82  '82'

 L. 240       104  LOAD_FAST                'val'
              106  STORE_FAST               'pending_header'
              108  JUMP_BACK            24  'to 24'
            110_0  COME_FROM            66  '66'

 L. 241       110  LOAD_FAST                'name'
              112  LOAD_CONST               b'content'
              114  COMPARE_OP               ==
              116  POP_JUMP_IF_FALSE_BACK    24  'to 24'

 L. 242       118  LOAD_FAST                'val'
              120  POP_JUMP_IF_FALSE_BACK    24  'to 24'

 L. 243       122  LOAD_FAST                'pending_header'
              124  POP_JUMP_IF_FALSE   146  'to 146'

 L. 244       126  LOAD_FAST                'self'
              128  LOAD_ATTR                headers
              130  LOAD_METHOD              append
              132  LOAD_FAST                'pending_header'
              134  LOAD_FAST                'val'
              136  BUILD_TUPLE_2         2 
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          

 L. 245       142  LOAD_CONST               True
              144  RETURN_VALUE     
            146_0  COME_FROM           124  '124'

 L. 246       146  LOAD_FAST                'val'
              148  STORE_FAST               'pending_content'
            150_0  COME_FROM            70  '70'
              150  JUMP_BACK            24  'to 24'

 L. 247       152  LOAD_CONST               True
              154  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 152

    def handle_possible_start_tag(self):
        return self.handle_possible_tag(False)

    def handle_possible_end_tag(self):
        next(self.data)
        return self.handle_possible_tag(True)

    def handle_possible_tag(self, end_tag):
        data = self.data
        if data.current_byte not in ascii_letters_bytes:
            if end_tag:
                data.previous
                self.handle_other
            return True
        tag_name, c = data.skip_until(spaces_angle_brackets)
        tag_name = tag_name.lower
        if not end_tag:
            if tag_name not in head_elems:
                return False
        if c == b'<':
            data.previous
        else:
            attr = self.get_attribute
            while True:
                if attr is not None:
                    attr = self.get_attribute

        return True

    def handle_other(self):
        return self.data.jump_to(b'>')

    def get_attribute--- This code section failed: ---

 L. 288         0  LOAD_FAST                'self'
                2  LOAD_ATTR                data
                4  STORE_FAST               'data'

 L. 290         6  LOAD_FAST                'data'
                8  LOAD_METHOD              skip
               10  LOAD_GLOBAL              skip1
               12  CALL_METHOD_1         1  ''
               14  STORE_FAST               'c'

 L. 291        16  LOAD_FAST                'c'
               18  LOAD_CONST               None
               20  COMPARE_OP               is
               22  POP_JUMP_IF_TRUE     40  'to 40'
               24  LOAD_GLOBAL              len
               26  LOAD_FAST                'c'
               28  CALL_FUNCTION_1       1  ''
               30  LOAD_CONST               1
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_TRUE     40  'to 40'
               36  LOAD_ASSERT              AssertionError
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            34  '34'
             40_1  COME_FROM            22  '22'

 L. 293        40  LOAD_FAST                'c'
               42  LOAD_CONST               (b'>', None)
               44  COMPARE_OP               in
               46  POP_JUMP_IF_FALSE    52  'to 52'

 L. 294        48  LOAD_CONST               None
               50  RETURN_VALUE     
             52_0  COME_FROM            46  '46'

 L. 296        52  BUILD_LIST_0          0 
               54  STORE_FAST               'attr_name'

 L. 297        56  BUILD_LIST_0          0 
               58  STORE_FAST               'attr_value'
             60_0  COME_FROM           148  '148'

 L. 300        60  LOAD_FAST                'c'
               62  LOAD_CONST               b'='
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE    76  'to 76'
               68  LOAD_FAST                'attr_name'
               70  POP_JUMP_IF_FALSE    76  'to 76'

 L. 301        72  JUMP_FORWARD        150  'to 150'
               74  BREAK_LOOP          140  'to 140'
             76_0  COME_FROM            70  '70'
             76_1  COME_FROM            66  '66'

 L. 302        76  LOAD_FAST                'c'
               78  LOAD_GLOBAL              space_chars_bytes
               80  COMPARE_OP               in
               82  POP_JUMP_IF_FALSE    96  'to 96'

 L. 304        84  LOAD_FAST                'data'
               86  LOAD_METHOD              skip
               88  CALL_METHOD_0         0  ''
               90  STORE_FAST               'c'

 L. 305        92  JUMP_FORWARD        150  'to 150'
               94  BREAK_LOOP          140  'to 140'
             96_0  COME_FROM            82  '82'

 L. 306        96  LOAD_FAST                'c'
               98  LOAD_CONST               (b'/', b'>')
              100  COMPARE_OP               in
              102  POP_JUMP_IF_FALSE   118  'to 118'

 L. 307       104  LOAD_CONST               b''
              106  LOAD_METHOD              join
              108  LOAD_FAST                'attr_name'
              110  CALL_METHOD_1         1  ''
              112  LOAD_CONST               b''
              114  BUILD_TUPLE_2         2 
              116  RETURN_VALUE     
            118_0  COME_FROM           102  '102'

 L. 308       118  LOAD_FAST                'c'
              120  LOAD_CONST               None
              122  COMPARE_OP               is
              124  POP_JUMP_IF_FALSE   130  'to 130'

 L. 309       126  LOAD_CONST               None
              128  RETURN_VALUE     
            130_0  COME_FROM           124  '124'

 L. 311       130  LOAD_FAST                'attr_name'
              132  LOAD_METHOD              append
              134  LOAD_FAST                'c'
              136  CALL_METHOD_1         1  ''
              138  POP_TOP          
            140_0  COME_FROM            94  '94'
            140_1  COME_FROM            74  '74'

 L. 313       140  LOAD_GLOBAL              next
              142  LOAD_FAST                'data'
              144  CALL_FUNCTION_1       1  ''
              146  STORE_FAST               'c'
              148  JUMP_BACK            60  'to 60'
            150_0  COME_FROM            92  '92'
            150_1  COME_FROM            72  '72'

 L. 315       150  LOAD_FAST                'c'
              152  LOAD_CONST               b'='
              154  COMPARE_OP               !=
              156  POP_JUMP_IF_FALSE   180  'to 180'

 L. 316       158  LOAD_FAST                'data'
              160  LOAD_METHOD              previous
              162  CALL_METHOD_0         0  ''
              164  POP_TOP          

 L. 317       166  LOAD_CONST               b''
              168  LOAD_METHOD              join
              170  LOAD_FAST                'attr_name'
              172  CALL_METHOD_1         1  ''
              174  LOAD_CONST               b''
              176  BUILD_TUPLE_2         2 
              178  RETURN_VALUE     
            180_0  COME_FROM           156  '156'

 L. 319       180  LOAD_GLOBAL              next
              182  LOAD_FAST                'data'
              184  CALL_FUNCTION_1       1  ''
              186  POP_TOP          

 L. 321       188  LOAD_FAST                'data'
              190  LOAD_METHOD              skip
              192  CALL_METHOD_0         0  ''
              194  STORE_FAST               'c'

 L. 323       196  LOAD_FAST                'c'
              198  LOAD_CONST               (b"'", b'"')
              200  COMPARE_OP               in
          202_204  POP_JUMP_IF_FALSE   270  'to 270'

 L. 325       206  LOAD_FAST                'c'
              208  STORE_FAST               'quote_char'
            210_0  COME_FROM           266  '266'

 L. 328       210  LOAD_GLOBAL              next
              212  LOAD_FAST                'data'
              214  CALL_FUNCTION_1       1  ''
              216  STORE_FAST               'c'

 L. 330       218  LOAD_FAST                'c'
              220  LOAD_FAST                'quote_char'
              222  COMPARE_OP               ==
          224_226  POP_JUMP_IF_FALSE   256  'to 256'

 L. 331       228  LOAD_GLOBAL              next
              230  LOAD_FAST                'data'
              232  CALL_FUNCTION_1       1  ''
              234  POP_TOP          

 L. 332       236  LOAD_CONST               b''
              238  LOAD_METHOD              join
              240  LOAD_FAST                'attr_name'
              242  CALL_METHOD_1         1  ''
              244  LOAD_CONST               b''
              246  LOAD_METHOD              join
              248  LOAD_FAST                'attr_value'
              250  CALL_METHOD_1         1  ''
              252  BUILD_TUPLE_2         2 
              254  RETURN_VALUE     
            256_0  COME_FROM           224  '224'

 L. 335       256  LOAD_FAST                'attr_value'
              258  LOAD_METHOD              append
              260  LOAD_FAST                'c'
              262  CALL_METHOD_1         1  ''
              264  POP_TOP          
              266  JUMP_BACK           210  'to 210'
              268  JUMP_FORWARD        318  'to 318'
            270_0  COME_FROM           202  '202'

 L. 336       270  LOAD_FAST                'c'
              272  LOAD_CONST               b'>'
              274  COMPARE_OP               ==
          276_278  POP_JUMP_IF_FALSE   294  'to 294'

 L. 337       280  LOAD_CONST               b''
              282  LOAD_METHOD              join
              284  LOAD_FAST                'attr_name'
              286  CALL_METHOD_1         1  ''
              288  LOAD_CONST               b''
              290  BUILD_TUPLE_2         2 
              292  RETURN_VALUE     
            294_0  COME_FROM           276  '276'

 L. 338       294  LOAD_FAST                'c'
              296  LOAD_CONST               None
              298  COMPARE_OP               is
          300_302  POP_JUMP_IF_FALSE   308  'to 308'

 L. 339       304  LOAD_CONST               None
              306  RETURN_VALUE     
            308_0  COME_FROM           300  '300'

 L. 341       308  LOAD_FAST                'attr_value'
              310  LOAD_METHOD              append
              312  LOAD_FAST                'c'
              314  CALL_METHOD_1         1  ''
              316  POP_TOP          
            318_0  COME_FROM           380  '380'
            318_1  COME_FROM           268  '268'

 L. 344       318  LOAD_GLOBAL              next
              320  LOAD_FAST                'data'
              322  CALL_FUNCTION_1       1  ''
              324  STORE_FAST               'c'

 L. 345       326  LOAD_FAST                'c'
              328  LOAD_GLOBAL              spaces_angle_brackets
              330  COMPARE_OP               in
          332_334  POP_JUMP_IF_FALSE   356  'to 356'

 L. 346       336  LOAD_CONST               b''
              338  LOAD_METHOD              join
              340  LOAD_FAST                'attr_name'
              342  CALL_METHOD_1         1  ''
              344  LOAD_CONST               b''
              346  LOAD_METHOD              join
              348  LOAD_FAST                'attr_value'
              350  CALL_METHOD_1         1  ''
              352  BUILD_TUPLE_2         2 
              354  RETURN_VALUE     
            356_0  COME_FROM           332  '332'

 L. 347       356  LOAD_FAST                'c'
              358  LOAD_CONST               None
              360  COMPARE_OP               is
          362_364  POP_JUMP_IF_FALSE   370  'to 370'

 L. 348       366  LOAD_CONST               None
              368  RETURN_VALUE     
            370_0  COME_FROM           362  '362'

 L. 350       370  LOAD_FAST                'attr_value'
              372  LOAD_METHOD              append
              374  LOAD_FAST                'c'
              376  CALL_METHOD_1         1  ''
              378  POP_TOP          
          380_382  JUMP_BACK           318  'to 318'

Parse error at or near `LOAD_FAST' instruction at offset 150