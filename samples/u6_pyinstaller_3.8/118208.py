# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
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

Parse error at or near `POP_TOP' instruction at offset 26


def replace_entity--- This code section failed: ---

 L.  33         0  LOAD_FAST                'match'
                2  LOAD_METHOD              group
                4  LOAD_CONST               1
                6  CALL_METHOD_1         1  ''
                8  LOAD_METHOD              lower
               10  CALL_METHOD_0         0  ''
               12  STORE_FAST               'ent'

 L.  34        14  LOAD_FAST                'ent'
               16  LOAD_CONST               {'squot', 'apos'}
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

Parse error at or near `POP_TOP' instruction at offset 178


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
        else:
            if p < 0:
                raise TypeError
        return self[p:p + 1]

    def next(self):
        return self.__next__

    def previous(self):
        p = self._position
        if p >= len(self):
            raise StopIteration
        else:
            if p < 0:
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
        while p < len(self):
            c = self[p:p + 1]
            if c not in chars:
                self._position = p
                return c
            p += 1

        self._position = p

    def skip_until(self, chars):
        p = pos = self.position
        while p < len(self):
            c = self[p:p + 1]
            if c in chars:
                self._position = p
                return (self[pos:p], c)
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
            124_0  COME_FROM           206  '206'
              124  FOR_ITER            214  'to 214'
              126  STORE_FAST               'byte'

 L. 188       128  LOAD_CONST               True
              130  STORE_FAST               'keep_parsing'

 L. 189       132  LOAD_FAST                'dispatch'
              134  GET_ITER         
            136_0  COME_FROM           152  '152'
              136  FOR_ITER            204  'to 204'
              138  UNPACK_SEQUENCE_3     3 
              140  STORE_FAST               'matcher'
              142  STORE_FAST               'key'
              144  STORE_FAST               'method'

 L. 190       146  LOAD_FAST                'matcher'
              148  LOAD_FAST                'key'
              150  CALL_FUNCTION_1       1  ''
              152  POP_JUMP_IF_FALSE   136  'to 136'

 L. 191       154  SETUP_FINALLY       172  'to 172'

 L. 192       156  LOAD_FAST                'method'
              158  CALL_FUNCTION_0       0  ''
              160  STORE_FAST               'keep_parsing'

 L. 193       162  POP_BLOCK        
              164  POP_TOP          
              166  BREAK_LOOP          204  'to 204'
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
              194  BREAK_LOOP          204  'to 204'
              196  POP_EXCEPT       
              198  JUMP_BACK           136  'to 136'
            200_0  COME_FROM           178  '178'
              200  END_FINALLY      
              202  JUMP_BACK           136  'to 136'

 L. 197       204  LOAD_FAST                'keep_parsing'
              206  POP_JUMP_IF_TRUE    124  'to 124'

 L. 198       208  POP_TOP          
              210  BREAK_LOOP          214  'to 214'
              212  JUMP_BACK           124  'to 124'

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

 L. 214       390  LOAD_FAST                'ans'
              392  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 192

    def handle_comment(self):
        """Skip over comments"""
        return self.data.jump_to(b'-->')

    def handle_meta(self):
        if self.data.current_byte not in space_chars_bytes:
            return True
        else:
            pending_header = pending_content = None
        while True:
            attr = self.get_attribute
            if attr is None:
                return True
                name, val = attr
                name = name.lower
                if name == b'http-equiv':
                    if val:
                        val = val.lower
                        if pending_content:
                            self.headers.append((val, pending_content))
                            return True
                        pending_header = val
            elif name == b'content':
                if val:
                    if pending_header:
                        self.headers.append((pending_header, val))
                        return True
                    pending_content = val

        return True

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
            while attr is not None:
                attr = self.get_attribute

            return True

    def handle_other(self):
        return self.data.jump_to(b'>')

    def get_attribute(self):
        """Return a name,value pair for the next attribute in the stream,
        if one is found, or None"""
        data = self.data
        c = data.skip(skip1)
        if not c is None:
            assert len(c) == 1
        if c in (b'>', None):
            return
        attr_name = []
        attr_value = []
        while c == b'=':
            if attr_name:
                break
            else:
                if c in space_chars_bytes:
                    c = data.skip
                    break
                else:
                    if c in (b'/', b'>'):
                        return (
                         (b'').join(attr_name), b'')
                    if c is None:
                        return
                    attr_name.append(c)
            c = next(data)

        if c != b'=':
            data.previous
            return ((b'').join(attr_name), b'')
        next(data)
        c = data.skip
        if c in (b"'", b'"'):
            quote_char = c
            while True:
                c = next(data)
                if c == quote_char:
                    next(data)
                    return ((b'').join(attr_name), (b'').join(attr_value))
                attr_value.append(c)

        else:
            if c == b'>':
                return (
                 (b'').join(attr_name), b'')
            if c is None:
                return
            attr_value.append(c)
            while True:
                c = next(data)
                if c in spaces_angle_brackets:
                    return (
                     (b'').join(attr_name), (b'').join(attr_value))
                if c is None:
                    return
                attr_value.append(c)