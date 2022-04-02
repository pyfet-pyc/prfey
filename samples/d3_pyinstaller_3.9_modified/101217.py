# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: email\feedparser.py
"""FeedParser - An email feed parser.

The feed parser implements an interface for incrementally parsing an email
message, line by line.  This has advantages for certain applications, such as
those reading email messages off a socket.

FeedParser.feed() is the primary interface for pushing new data into the
parser.  It returns when there's nothing more it can do with the available
data.  When you have no more data to push into the parser, call .close().
This completes the parsing and returns the root message object.

The other advantage of this parser is that it will never raise a parsing
exception.  Instead, when it finds something unexpected, it adds a 'defect' to
the current message.  Defects are just instances that live on the message
object's .defects attribute.
"""
__all__ = [
 'FeedParser', 'BytesFeedParser']
import re
from email import errors
from email._policybase import compat32
from collections import deque
from io import StringIO
NLCRE = re.compile('\\r\\n|\\r|\\n')
NLCRE_bol = re.compile('(\\r\\n|\\r|\\n)')
NLCRE_eol = re.compile('(\\r\\n|\\r|\\n)\\Z')
NLCRE_crack = re.compile('(\\r\\n|\\r|\\n)')
headerRE = re.compile('^(From |[\\041-\\071\\073-\\176]*:|[\\t ])')
EMPTYSTRING = ''
NL = '\n'
NeedMoreData = object()

class BufferedSubFile(object):
    __doc__ = 'A file-ish object that can have new data loaded into it.\n\n    You can also push and pop line-matching predicates onto a stack.  When the\n    current predicate matches the current line, a false EOF response\n    (i.e. empty string) is returned instead.  This lets the parser adhere to a\n    simple abstraction -- it parses until EOF closes the current message.\n    '

    def __init__(self):
        self._partial = StringIO(newline='')
        self._lines = deque()
        self._eofstack = []
        self._closed = False

    def push_eof_matcher(self, pred):
        self._eofstack.append(pred)

    def pop_eof_matcher(self):
        return self._eofstack.pop()

    def close(self):
        self._partial.seek(0)
        self.pushlines(self._partial.readlines())
        self._partial.seek(0)
        self._partial.truncate()
        self._closed = True

    def readline(self):
        if not self._lines:
            if self._closed:
                return ''
            return NeedMoreData
        line = self._lines.popleft()
        for ateof in reversed(self._eofstack):
            if ateof(line):
                self._lines.appendleft(line)
                return ''
        else:
            return line

    def unreadline--- This code section failed: ---

 L.  98         0  LOAD_FAST                'line'
                2  LOAD_GLOBAL              NeedMoreData
                4  <117>                 1  ''
                6  POP_JUMP_IF_TRUE     12  'to 12'
                8  <74>             
               10  RAISE_VARARGS_1       1  'exception instance'
             12_0  COME_FROM             6  '6'

 L.  99        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _lines
               16  LOAD_METHOD              appendleft
               18  LOAD_FAST                'line'
               20  CALL_METHOD_1         1  ''
               22  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def push--- This code section failed: ---

 L. 103         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _partial
                4  LOAD_METHOD              write
                6  LOAD_FAST                'data'
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          

 L. 104        12  LOAD_STR                 '\n'
               14  LOAD_FAST                'data'
               16  <118>                 1  ''
               18  POP_JUMP_IF_FALSE    32  'to 32'
               20  LOAD_STR                 '\r'
               22  LOAD_FAST                'data'
               24  <118>                 1  ''
               26  POP_JUMP_IF_FALSE    32  'to 32'

 L. 106        28  LOAD_CONST               None
               30  RETURN_VALUE     
             32_0  COME_FROM            26  '26'
             32_1  COME_FROM            18  '18'

 L. 109        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _partial
               36  LOAD_METHOD              seek
               38  LOAD_CONST               0
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          

 L. 110        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _partial
               48  LOAD_METHOD              readlines
               50  CALL_METHOD_0         0  ''
               52  STORE_FAST               'parts'

 L. 111        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _partial
               58  LOAD_METHOD              seek
               60  LOAD_CONST               0
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          

 L. 112        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _partial
               70  LOAD_METHOD              truncate
               72  CALL_METHOD_0         0  ''
               74  POP_TOP          

 L. 118        76  LOAD_FAST                'parts'
               78  LOAD_CONST               -1
               80  BINARY_SUBSCR    
               82  LOAD_METHOD              endswith
               84  LOAD_STR                 '\n'
               86  CALL_METHOD_1         1  ''
               88  POP_JUMP_IF_TRUE    106  'to 106'

 L. 119        90  LOAD_FAST                'self'
               92  LOAD_ATTR                _partial
               94  LOAD_METHOD              write
               96  LOAD_FAST                'parts'
               98  LOAD_METHOD              pop
              100  CALL_METHOD_0         0  ''
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          
            106_0  COME_FROM            88  '88'

 L. 120       106  LOAD_FAST                'self'
              108  LOAD_METHOD              pushlines
              110  LOAD_FAST                'parts'
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          

Parse error at or near `<118>' instruction at offset 16

    def pushlines(self, lines):
        self._lines.extend(lines)

    def __iter__(self):
        return self

    def __next__(self):
        line = self.readline()
        if line == '':
            raise StopIteration
        return line


class FeedParser:
    __doc__ = 'A feed-style parser of email.'

    def __init__--- This code section failed: ---

 L. 147         0  LOAD_FAST                'policy'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               policy

 L. 148         6  LOAD_CONST               False
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _old_style_factory

 L. 149        12  LOAD_FAST                '_factory'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    60  'to 60'

 L. 150        20  LOAD_FAST                'policy'
               22  LOAD_ATTR                message_factory
               24  LOAD_CONST               None
               26  <117>                 0  ''
               28  POP_JUMP_IF_FALSE    50  'to 50'

 L. 151        30  LOAD_CONST               0
               32  LOAD_CONST               ('Message',)
               34  IMPORT_NAME_ATTR         email.message
               36  IMPORT_FROM              Message
               38  STORE_FAST               'Message'
               40  POP_TOP          

 L. 152        42  LOAD_FAST                'Message'
               44  LOAD_FAST                'self'
               46  STORE_ATTR               _factory
               48  JUMP_FORWARD        108  'to 108'
             50_0  COME_FROM            28  '28'

 L. 154        50  LOAD_FAST                'policy'
               52  LOAD_ATTR                message_factory
               54  LOAD_FAST                'self'
               56  STORE_ATTR               _factory
               58  JUMP_FORWARD        108  'to 108'
             60_0  COME_FROM            18  '18'

 L. 156        60  LOAD_FAST                '_factory'
               62  LOAD_FAST                'self'
               64  STORE_ATTR               _factory

 L. 157        66  SETUP_FINALLY        84  'to 84'

 L. 158        68  LOAD_FAST                '_factory'
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                policy
               74  LOAD_CONST               ('policy',)
               76  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               78  POP_TOP          
               80  POP_BLOCK        
               82  JUMP_FORWARD        108  'to 108'
             84_0  COME_FROM_FINALLY    66  '66'

 L. 159        84  DUP_TOP          
               86  LOAD_GLOBAL              TypeError
               88  <121>               106  ''
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          

 L. 161        96  LOAD_CONST               True
               98  LOAD_FAST                'self'
              100  STORE_ATTR               _old_style_factory
              102  POP_EXCEPT       
              104  JUMP_FORWARD        108  'to 108'
              106  <48>             
            108_0  COME_FROM           104  '104'
            108_1  COME_FROM            82  '82'
            108_2  COME_FROM            58  '58'
            108_3  COME_FROM            48  '48'

 L. 162       108  LOAD_GLOBAL              BufferedSubFile
              110  CALL_FUNCTION_0       0  ''
              112  LOAD_FAST                'self'
              114  STORE_ATTR               _input

 L. 163       116  BUILD_LIST_0          0 
              118  LOAD_FAST                'self'
              120  STORE_ATTR               _msgstack

 L. 164       122  LOAD_FAST                'self'
              124  LOAD_METHOD              _parsegen
              126  CALL_METHOD_0         0  ''
              128  LOAD_ATTR                __next__
              130  LOAD_FAST                'self'
              132  STORE_ATTR               _parse

 L. 165       134  LOAD_CONST               None
              136  LOAD_FAST                'self'
              138  STORE_ATTR               _cur

 L. 166       140  LOAD_CONST               None
              142  LOAD_FAST                'self'
              144  STORE_ATTR               _last

 L. 167       146  LOAD_CONST               False
              148  LOAD_FAST                'self'
              150  STORE_ATTR               _headersonly

Parse error at or near `<117>' instruction at offset 16

    def _set_headersonly(self):
        self._headersonly = True

    def feed(self, data):
        """Push more data into the parser."""
        self._input.push(data)
        self._call_parse()

    def _call_parse--- This code section failed: ---

 L. 179         0  SETUP_FINALLY        14  'to 14'

 L. 180         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _parse
                6  CALL_METHOD_0         0  ''
                8  POP_TOP          
               10  POP_BLOCK        
               12  JUMP_FORWARD         32  'to 32'
             14_0  COME_FROM_FINALLY     0  '0'

 L. 181        14  DUP_TOP          
               16  LOAD_GLOBAL              StopIteration
               18  <121>                30  ''
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 182        26  POP_EXCEPT       
               28  JUMP_FORWARD         32  'to 32'
               30  <48>             
             32_0  COME_FROM            28  '28'
             32_1  COME_FROM            12  '12'

Parse error at or near `<121>' instruction at offset 18

    def close--- This code section failed: ---

 L. 186         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _input
                4  LOAD_METHOD              close
                6  CALL_METHOD_0         0  ''
                8  POP_TOP          

 L. 187        10  LOAD_FAST                'self'
               12  LOAD_METHOD              _call_parse
               14  CALL_METHOD_0         0  ''
               16  POP_TOP          

 L. 188        18  LOAD_FAST                'self'
               20  LOAD_METHOD              _pop_message
               22  CALL_METHOD_0         0  ''
               24  STORE_FAST               'root'

 L. 189        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _msgstack
               30  POP_JUMP_IF_FALSE    36  'to 36'
               32  <74>             
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            30  '30'

 L. 191        36  LOAD_FAST                'root'
               38  LOAD_METHOD              get_content_maintype
               40  CALL_METHOD_0         0  ''
               42  LOAD_STR                 'multipart'
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_FALSE    78  'to 78'

 L. 192        48  LOAD_FAST                'root'
               50  LOAD_METHOD              is_multipart
               52  CALL_METHOD_0         0  ''

 L. 191        54  POP_JUMP_IF_TRUE     78  'to 78'

 L. 193        56  LOAD_GLOBAL              errors
               58  LOAD_METHOD              MultipartInvariantViolationDefect
               60  CALL_METHOD_0         0  ''
               62  STORE_FAST               'defect'

 L. 194        64  LOAD_FAST                'self'
               66  LOAD_ATTR                policy
               68  LOAD_METHOD              handle_defect
               70  LOAD_FAST                'root'
               72  LOAD_FAST                'defect'
               74  CALL_METHOD_2         2  ''
               76  POP_TOP          
             78_0  COME_FROM            54  '54'
             78_1  COME_FROM            46  '46'

 L. 195        78  LOAD_FAST                'root'
               80  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 32

    def _new_message(self):
        if self._old_style_factory:
            msg = self._factory()
        else:
            msg = self._factory(policy=(self.policy))
        if self._cur:
            if self._cur.get_content_type() == 'multipart/digest':
                msg.set_default_type('message/rfc822')
        if self._msgstack:
            self._msgstack[(-1)].attach(msg)
        self._msgstack.append(msg)
        self._cur = msg
        self._last = msg

    def _pop_message(self):
        retval = self._msgstack.pop()
        if self._msgstack:
            self._cur = self._msgstack[(-1)]
        else:
            self._cur = None
        return retval

    def _parsegen--- This code section failed: ---

 L. 220         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _new_message
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 221         8  BUILD_LIST_0          0 
               10  STORE_FAST               'headers'

 L. 224        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _input
               16  GET_ITER         
             18_0  COME_FROM           108  '108'
             18_1  COME_FROM            36  '36'
               18  FOR_ITER            110  'to 110'
               20  STORE_FAST               'line'

 L. 225        22  LOAD_FAST                'line'
               24  LOAD_GLOBAL              NeedMoreData
               26  <117>                 0  ''
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L. 226        30  LOAD_GLOBAL              NeedMoreData
               32  YIELD_VALUE      
               34  POP_TOP          

 L. 227        36  JUMP_BACK            18  'to 18'
             38_0  COME_FROM            28  '28'

 L. 228        38  LOAD_GLOBAL              headerRE
               40  LOAD_METHOD              match
               42  LOAD_FAST                'line'
               44  CALL_METHOD_1         1  ''
               46  POP_JUMP_IF_TRUE     98  'to 98'

 L. 232        48  LOAD_GLOBAL              NLCRE
               50  LOAD_METHOD              match
               52  LOAD_FAST                'line'
               54  CALL_METHOD_1         1  ''
               56  POP_JUMP_IF_TRUE     94  'to 94'

 L. 233        58  LOAD_GLOBAL              errors
               60  LOAD_METHOD              MissingHeaderBodySeparatorDefect
               62  CALL_METHOD_0         0  ''
               64  STORE_FAST               'defect'

 L. 234        66  LOAD_FAST                'self'
               68  LOAD_ATTR                policy
               70  LOAD_METHOD              handle_defect
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                _cur
               76  LOAD_FAST                'defect'
               78  CALL_METHOD_2         2  ''
               80  POP_TOP          

 L. 235        82  LOAD_FAST                'self'
               84  LOAD_ATTR                _input
               86  LOAD_METHOD              unreadline
               88  LOAD_FAST                'line'
               90  CALL_METHOD_1         1  ''
               92  POP_TOP          
             94_0  COME_FROM            56  '56'

 L. 236        94  POP_TOP          
               96  BREAK_LOOP          110  'to 110'
             98_0  COME_FROM            46  '46'

 L. 237        98  LOAD_FAST                'headers'
              100  LOAD_METHOD              append
              102  LOAD_FAST                'line'
              104  CALL_METHOD_1         1  ''
              106  POP_TOP          
              108  JUMP_BACK            18  'to 18'
            110_0  COME_FROM            96  '96'
            110_1  COME_FROM            18  '18'

 L. 240       110  LOAD_FAST                'self'
              112  LOAD_METHOD              _parse_headers
              114  LOAD_FAST                'headers'
              116  CALL_METHOD_1         1  ''
              118  POP_TOP          

 L. 244       120  LOAD_FAST                'self'
              122  LOAD_ATTR                _headersonly
              124  POP_JUMP_IF_FALSE   200  'to 200'

 L. 245       126  BUILD_LIST_0          0 
              128  STORE_FAST               'lines'
            130_0  COME_FROM           176  '176'
            130_1  COME_FROM           154  '154'

 L. 247       130  LOAD_FAST                'self'
              132  LOAD_ATTR                _input
              134  LOAD_METHOD              readline
              136  CALL_METHOD_0         0  ''
              138  STORE_FAST               'line'

 L. 248       140  LOAD_FAST                'line'
              142  LOAD_GLOBAL              NeedMoreData
              144  <117>                 0  ''
              146  POP_JUMP_IF_FALSE   156  'to 156'

 L. 249       148  LOAD_GLOBAL              NeedMoreData
              150  YIELD_VALUE      
              152  POP_TOP          

 L. 250       154  JUMP_BACK           130  'to 130'
            156_0  COME_FROM           146  '146'

 L. 251       156  LOAD_FAST                'line'
              158  LOAD_STR                 ''
              160  COMPARE_OP               ==
              162  POP_JUMP_IF_FALSE   166  'to 166'

 L. 252       164  JUMP_FORWARD        178  'to 178'
            166_0  COME_FROM           162  '162'

 L. 253       166  LOAD_FAST                'lines'
              168  LOAD_METHOD              append
              170  LOAD_FAST                'line'
              172  CALL_METHOD_1         1  ''
              174  POP_TOP          
              176  JUMP_BACK           130  'to 130'
            178_0  COME_FROM           164  '164'

 L. 254       178  LOAD_FAST                'self'
              180  LOAD_ATTR                _cur
              182  LOAD_METHOD              set_payload
              184  LOAD_GLOBAL              EMPTYSTRING
              186  LOAD_METHOD              join
              188  LOAD_FAST                'lines'
              190  CALL_METHOD_1         1  ''
              192  CALL_METHOD_1         1  ''
              194  POP_TOP          

 L. 255       196  LOAD_CONST               None
              198  RETURN_VALUE     
            200_0  COME_FROM           124  '124'

 L. 256       200  LOAD_FAST                'self'
              202  LOAD_ATTR                _cur
              204  LOAD_METHOD              get_content_type
              206  CALL_METHOD_0         0  ''
              208  LOAD_STR                 'message/delivery-status'
              210  COMPARE_OP               ==
          212_214  POP_JUMP_IF_FALSE   394  'to 394'
            216_0  COME_FROM           388  '388'

 L. 263       216  LOAD_FAST                'self'
              218  LOAD_ATTR                _input
              220  LOAD_METHOD              push_eof_matcher
              222  LOAD_GLOBAL              NLCRE
              224  LOAD_ATTR                match
              226  CALL_METHOD_1         1  ''
              228  POP_TOP          

 L. 264       230  LOAD_FAST                'self'
              232  LOAD_METHOD              _parsegen
              234  CALL_METHOD_0         0  ''
              236  GET_ITER         
            238_0  COME_FROM           266  '266'
            238_1  COME_FROM           258  '258'
              238  FOR_ITER            268  'to 268'
              240  STORE_FAST               'retval'

 L. 265       242  LOAD_FAST                'retval'
              244  LOAD_GLOBAL              NeedMoreData
              246  <117>                 0  ''
          248_250  POP_JUMP_IF_FALSE   260  'to 260'

 L. 266       252  LOAD_GLOBAL              NeedMoreData
              254  YIELD_VALUE      
              256  POP_TOP          

 L. 267       258  JUMP_BACK           238  'to 238'
            260_0  COME_FROM           248  '248'

 L. 268       260  POP_TOP          
          262_264  BREAK_LOOP          268  'to 268'
              266  JUMP_BACK           238  'to 238'
            268_0  COME_FROM           262  '262'
            268_1  COME_FROM           238  '238'

 L. 269       268  LOAD_FAST                'self'
              270  LOAD_METHOD              _pop_message
              272  CALL_METHOD_0         0  ''
              274  STORE_FAST               'msg'

 L. 273       276  LOAD_FAST                'self'
              278  LOAD_ATTR                _input
              280  LOAD_METHOD              pop_eof_matcher
              282  CALL_METHOD_0         0  ''
              284  POP_TOP          
            286_0  COME_FROM           320  '320'
            286_1  COME_FROM           312  '312'

 L. 279       286  LOAD_FAST                'self'
              288  LOAD_ATTR                _input
              290  LOAD_METHOD              readline
              292  CALL_METHOD_0         0  ''
              294  STORE_FAST               'line'

 L. 280       296  LOAD_FAST                'line'
              298  LOAD_GLOBAL              NeedMoreData
              300  <117>                 0  ''
          302_304  POP_JUMP_IF_FALSE   324  'to 324'

 L. 281       306  LOAD_GLOBAL              NeedMoreData
              308  YIELD_VALUE      
              310  POP_TOP          

 L. 282   312_314  JUMP_BACK           286  'to 286'

 L. 283   316_318  BREAK_LOOP          324  'to 324'
          320_322  JUMP_BACK           286  'to 286'
            324_0  COME_FROM           358  '358'
            324_1  COME_FROM           350  '350'
            324_2  COME_FROM           316  '316'
            324_3  COME_FROM           302  '302'

 L. 285       324  LOAD_FAST                'self'
              326  LOAD_ATTR                _input
              328  LOAD_METHOD              readline
              330  CALL_METHOD_0         0  ''
              332  STORE_FAST               'line'

 L. 286       334  LOAD_FAST                'line'
              336  LOAD_GLOBAL              NeedMoreData
              338  <117>                 0  ''
          340_342  POP_JUMP_IF_FALSE   362  'to 362'

 L. 287       344  LOAD_GLOBAL              NeedMoreData
              346  YIELD_VALUE      
              348  POP_TOP          

 L. 288   350_352  JUMP_BACK           324  'to 324'

 L. 289   354_356  BREAK_LOOP          362  'to 362'
          358_360  JUMP_BACK           324  'to 324'
            362_0  COME_FROM           354  '354'
            362_1  COME_FROM           340  '340'

 L. 290       362  LOAD_FAST                'line'
              364  LOAD_STR                 ''
              366  COMPARE_OP               ==
          368_370  POP_JUMP_IF_FALSE   376  'to 376'

 L. 291   372_374  JUMP_FORWARD        390  'to 390'
            376_0  COME_FROM           368  '368'

 L. 293       376  LOAD_FAST                'self'
              378  LOAD_ATTR                _input
              380  LOAD_METHOD              unreadline
              382  LOAD_FAST                'line'
              384  CALL_METHOD_1         1  ''
              386  POP_TOP          
              388  JUMP_BACK           216  'to 216'
            390_0  COME_FROM           372  '372'

 L. 294       390  LOAD_CONST               None
              392  RETURN_VALUE     
            394_0  COME_FROM           212  '212'

 L. 295       394  LOAD_FAST                'self'
              396  LOAD_ATTR                _cur
              398  LOAD_METHOD              get_content_maintype
              400  CALL_METHOD_0         0  ''
              402  LOAD_STR                 'message'
              404  COMPARE_OP               ==
          406_408  POP_JUMP_IF_FALSE   464  'to 464'

 L. 298       410  LOAD_FAST                'self'
              412  LOAD_METHOD              _parsegen
              414  CALL_METHOD_0         0  ''
              416  GET_ITER         
            418_0  COME_FROM           448  '448'
            418_1  COME_FROM           438  '438'
              418  FOR_ITER            452  'to 452'
              420  STORE_FAST               'retval'

 L. 299       422  LOAD_FAST                'retval'
              424  LOAD_GLOBAL              NeedMoreData
              426  <117>                 0  ''
          428_430  POP_JUMP_IF_FALSE   442  'to 442'

 L. 300       432  LOAD_GLOBAL              NeedMoreData
              434  YIELD_VALUE      
              436  POP_TOP          

 L. 301   438_440  JUMP_BACK           418  'to 418'
            442_0  COME_FROM           428  '428'

 L. 302       442  POP_TOP          
          444_446  BREAK_LOOP          452  'to 452'
          448_450  JUMP_BACK           418  'to 418'
            452_0  COME_FROM           444  '444'
            452_1  COME_FROM           418  '418'

 L. 303       452  LOAD_FAST                'self'
              454  LOAD_METHOD              _pop_message
              456  CALL_METHOD_0         0  ''
              458  POP_TOP          

 L. 304       460  LOAD_CONST               None
              462  RETURN_VALUE     
            464_0  COME_FROM           406  '406'

 L. 305       464  LOAD_FAST                'self'
              466  LOAD_ATTR                _cur
              468  LOAD_METHOD              get_content_maintype
              470  CALL_METHOD_0         0  ''
              472  LOAD_STR                 'multipart'
              474  COMPARE_OP               ==
          476_478  POP_JUMP_IF_FALSE  1502  'to 1502'

 L. 306       480  LOAD_FAST                'self'
              482  LOAD_ATTR                _cur
              484  LOAD_METHOD              get_boundary
              486  CALL_METHOD_0         0  ''
              488  STORE_FAST               'boundary'

 L. 307       490  LOAD_FAST                'boundary'
              492  LOAD_CONST               None
              494  <117>                 0  ''
          496_498  POP_JUMP_IF_FALSE   594  'to 594'

 L. 312       500  LOAD_GLOBAL              errors
              502  LOAD_METHOD              NoBoundaryInMultipartDefect
              504  CALL_METHOD_0         0  ''
              506  STORE_FAST               'defect'

 L. 313       508  LOAD_FAST                'self'
              510  LOAD_ATTR                policy
              512  LOAD_METHOD              handle_defect
              514  LOAD_FAST                'self'
              516  LOAD_ATTR                _cur
              518  LOAD_FAST                'defect'
              520  CALL_METHOD_2         2  ''
              522  POP_TOP          

 L. 314       524  BUILD_LIST_0          0 
              526  STORE_FAST               'lines'

 L. 315       528  LOAD_FAST                'self'
              530  LOAD_ATTR                _input
              532  GET_ITER         
            534_0  COME_FROM           568  '568'
            534_1  COME_FROM           554  '554'
              534  FOR_ITER            572  'to 572'
              536  STORE_FAST               'line'

 L. 316       538  LOAD_FAST                'line'
              540  LOAD_GLOBAL              NeedMoreData
              542  <117>                 0  ''
          544_546  POP_JUMP_IF_FALSE   558  'to 558'

 L. 317       548  LOAD_GLOBAL              NeedMoreData
              550  YIELD_VALUE      
              552  POP_TOP          

 L. 318   554_556  JUMP_BACK           534  'to 534'
            558_0  COME_FROM           544  '544'

 L. 319       558  LOAD_FAST                'lines'
              560  LOAD_METHOD              append
              562  LOAD_FAST                'line'
              564  CALL_METHOD_1         1  ''
              566  POP_TOP          
          568_570  JUMP_BACK           534  'to 534'
            572_0  COME_FROM           534  '534'

 L. 320       572  LOAD_FAST                'self'
              574  LOAD_ATTR                _cur
              576  LOAD_METHOD              set_payload
              578  LOAD_GLOBAL              EMPTYSTRING
              580  LOAD_METHOD              join
              582  LOAD_FAST                'lines'
              584  CALL_METHOD_1         1  ''
              586  CALL_METHOD_1         1  ''
              588  POP_TOP          

 L. 321       590  LOAD_CONST               None
              592  RETURN_VALUE     
            594_0  COME_FROM           496  '496'

 L. 323       594  LOAD_GLOBAL              str
              596  LOAD_FAST                'self'
              598  LOAD_ATTR                _cur
              600  LOAD_METHOD              get
              602  LOAD_STR                 'content-transfer-encoding'
              604  LOAD_STR                 '8bit'
              606  CALL_METHOD_2         2  ''
              608  CALL_FUNCTION_1       1  ''
              610  LOAD_METHOD              lower
              612  CALL_METHOD_0         0  ''

 L. 324       614  LOAD_CONST               ('7bit', '8bit', 'binary')

 L. 323       616  <118>                 1  ''
          618_620  POP_JUMP_IF_FALSE   646  'to 646'

 L. 325       622  LOAD_GLOBAL              errors
              624  LOAD_METHOD              InvalidMultipartContentTransferEncodingDefect
              626  CALL_METHOD_0         0  ''
              628  STORE_FAST               'defect'

 L. 326       630  LOAD_FAST                'self'
              632  LOAD_ATTR                policy
              634  LOAD_METHOD              handle_defect
              636  LOAD_FAST                'self'
              638  LOAD_ATTR                _cur
              640  LOAD_FAST                'defect'
              642  CALL_METHOD_2         2  ''
              644  POP_TOP          
            646_0  COME_FROM           618  '618'

 L. 331       646  LOAD_STR                 '--'
              648  LOAD_FAST                'boundary'
              650  BINARY_ADD       
              652  STORE_FAST               'separator'

 L. 332       654  LOAD_GLOBAL              re
              656  LOAD_METHOD              compile

 L. 333       658  LOAD_STR                 '(?P<sep>'
              660  LOAD_GLOBAL              re
              662  LOAD_METHOD              escape
              664  LOAD_FAST                'separator'
              666  CALL_METHOD_1         1  ''
              668  BINARY_ADD       

 L. 334       670  LOAD_STR                 ')(?P<end>--)?(?P<ws>[ \\t]*)(?P<linesep>\\r\\n|\\r|\\n)?$'

 L. 333       672  BINARY_ADD       

 L. 332       674  CALL_METHOD_1         1  ''
              676  STORE_FAST               'boundaryre'

 L. 335       678  LOAD_CONST               True
              680  STORE_FAST               'capturing_preamble'

 L. 336       682  BUILD_LIST_0          0 
              684  STORE_FAST               'preamble'

 L. 337       686  LOAD_CONST               False
              688  STORE_FAST               'linesep'

 L. 338       690  LOAD_CONST               False
              692  STORE_FAST               'close_boundary_seen'
            694_0  COME_FROM          1224  '1224'
            694_1  COME_FROM          1202  '1202'
            694_2  COME_FROM           878  '878'
            694_3  COME_FROM           720  '720'

 L. 340       694  LOAD_FAST                'self'
              696  LOAD_ATTR                _input
              698  LOAD_METHOD              readline
              700  CALL_METHOD_0         0  ''
              702  STORE_FAST               'line'

 L. 341       704  LOAD_FAST                'line'
              706  LOAD_GLOBAL              NeedMoreData
              708  <117>                 0  ''
          710_712  POP_JUMP_IF_FALSE   724  'to 724'

 L. 342       714  LOAD_GLOBAL              NeedMoreData
              716  YIELD_VALUE      
              718  POP_TOP          

 L. 343   720_722  JUMP_BACK           694  'to 694'
            724_0  COME_FROM           710  '710'

 L. 344       724  LOAD_FAST                'line'
              726  LOAD_STR                 ''
              728  COMPARE_OP               ==
          730_732  POP_JUMP_IF_FALSE   738  'to 738'

 L. 345   734_736  JUMP_FORWARD       1228  'to 1228'
            738_0  COME_FROM           730  '730'

 L. 346       738  LOAD_FAST                'boundaryre'
              740  LOAD_METHOD              match
              742  LOAD_FAST                'line'
              744  CALL_METHOD_1         1  ''
              746  STORE_FAST               'mo'

 L. 347       748  LOAD_FAST                'mo'
          750_752  POP_JUMP_IF_FALSE  1204  'to 1204'

 L. 352       754  LOAD_FAST                'mo'
              756  LOAD_METHOD              group
              758  LOAD_STR                 'end'
              760  CALL_METHOD_1         1  ''
          762_764  POP_JUMP_IF_FALSE   784  'to 784'

 L. 353       766  LOAD_CONST               True
              768  STORE_FAST               'close_boundary_seen'

 L. 354       770  LOAD_FAST                'mo'
              772  LOAD_METHOD              group
              774  LOAD_STR                 'linesep'
              776  CALL_METHOD_1         1  ''
              778  STORE_FAST               'linesep'

 L. 355   780_782  JUMP_FORWARD       1228  'to 1228'
            784_0  COME_FROM           762  '762'

 L. 357       784  LOAD_FAST                'capturing_preamble'
          786_788  POP_JUMP_IF_FALSE   882  'to 882'

 L. 358       790  LOAD_FAST                'preamble'
          792_794  POP_JUMP_IF_FALSE   862  'to 862'

 L. 361       796  LOAD_FAST                'preamble'
              798  LOAD_CONST               -1
              800  BINARY_SUBSCR    
              802  STORE_FAST               'lastline'

 L. 362       804  LOAD_GLOBAL              NLCRE_eol
              806  LOAD_METHOD              search
              808  LOAD_FAST                'lastline'
              810  CALL_METHOD_1         1  ''
              812  STORE_FAST               'eolmo'

 L. 363       814  LOAD_FAST                'eolmo'
          816_818  POP_JUMP_IF_FALSE   848  'to 848'

 L. 364       820  LOAD_FAST                'lastline'
              822  LOAD_CONST               None
              824  LOAD_GLOBAL              len
              826  LOAD_FAST                'eolmo'
              828  LOAD_METHOD              group
              830  LOAD_CONST               0
              832  CALL_METHOD_1         1  ''
              834  CALL_FUNCTION_1       1  ''
              836  UNARY_NEGATIVE   
              838  BUILD_SLICE_2         2 
              840  BINARY_SUBSCR    
              842  LOAD_FAST                'preamble'
              844  LOAD_CONST               -1
              846  STORE_SUBSCR     
            848_0  COME_FROM           816  '816'

 L. 365       848  LOAD_GLOBAL              EMPTYSTRING
              850  LOAD_METHOD              join
              852  LOAD_FAST                'preamble'
              854  CALL_METHOD_1         1  ''
              856  LOAD_FAST                'self'
              858  LOAD_ATTR                _cur
              860  STORE_ATTR               preamble
            862_0  COME_FROM           792  '792'

 L. 366       862  LOAD_CONST               False
              864  STORE_FAST               'capturing_preamble'

 L. 367       866  LOAD_FAST                'self'
              868  LOAD_ATTR                _input
              870  LOAD_METHOD              unreadline
              872  LOAD_FAST                'line'
              874  CALL_METHOD_1         1  ''
              876  POP_TOP          

 L. 368   878_880  JUMP_BACK           694  'to 694'
            882_0  COME_FROM           944  '944'
            882_1  COME_FROM           924  '924'
            882_2  COME_FROM           908  '908'
            882_3  COME_FROM           786  '786'

 L. 374       882  LOAD_FAST                'self'
              884  LOAD_ATTR                _input
              886  LOAD_METHOD              readline
              888  CALL_METHOD_0         0  ''
              890  STORE_FAST               'line'

 L. 375       892  LOAD_FAST                'line'
              894  LOAD_GLOBAL              NeedMoreData
              896  <117>                 0  ''
          898_900  POP_JUMP_IF_FALSE   912  'to 912'

 L. 376       902  LOAD_GLOBAL              NeedMoreData
              904  YIELD_VALUE      
              906  POP_TOP          

 L. 377   908_910  JUMP_BACK           882  'to 882'
            912_0  COME_FROM           898  '898'

 L. 378       912  LOAD_FAST                'boundaryre'
              914  LOAD_METHOD              match
              916  LOAD_FAST                'line'
              918  CALL_METHOD_1         1  ''
              920  STORE_FAST               'mo'

 L. 379       922  LOAD_FAST                'mo'
          924_926  POP_JUMP_IF_TRUE_BACK   882  'to 882'

 L. 380       928  LOAD_FAST                'self'
              930  LOAD_ATTR                _input
              932  LOAD_METHOD              unreadline
              934  LOAD_FAST                'line'
              936  CALL_METHOD_1         1  ''
              938  POP_TOP          

 L. 381   940_942  JUMP_FORWARD        948  'to 948'
          944_946  JUMP_BACK           882  'to 882'
            948_0  COME_FROM           940  '940'

 L. 384       948  LOAD_FAST                'self'
              950  LOAD_ATTR                _input
              952  LOAD_METHOD              push_eof_matcher
              954  LOAD_FAST                'boundaryre'
              956  LOAD_ATTR                match
              958  CALL_METHOD_1         1  ''
              960  POP_TOP          

 L. 385       962  LOAD_FAST                'self'
              964  LOAD_METHOD              _parsegen
              966  CALL_METHOD_0         0  ''
              968  GET_ITER         
            970_0  COME_FROM          1000  '1000'
            970_1  COME_FROM           990  '990'
              970  FOR_ITER           1004  'to 1004'
              972  STORE_FAST               'retval'

 L. 386       974  LOAD_FAST                'retval'
              976  LOAD_GLOBAL              NeedMoreData
              978  <117>                 0  ''
          980_982  POP_JUMP_IF_FALSE   994  'to 994'

 L. 387       984  LOAD_GLOBAL              NeedMoreData
              986  YIELD_VALUE      
              988  POP_TOP          

 L. 388   990_992  JUMP_BACK           970  'to 970'
            994_0  COME_FROM           980  '980'

 L. 389       994  POP_TOP          
          996_998  BREAK_LOOP         1004  'to 1004'
         1000_1002  JUMP_BACK           970  'to 970'
           1004_0  COME_FROM           996  '996'
           1004_1  COME_FROM           970  '970'

 L. 394      1004  LOAD_FAST                'self'
             1006  LOAD_ATTR                _last
             1008  LOAD_METHOD              get_content_maintype
             1010  CALL_METHOD_0         0  ''
             1012  LOAD_STR                 'multipart'
             1014  COMPARE_OP               ==
         1016_1018  POP_JUMP_IF_FALSE  1108  'to 1108'

 L. 395      1020  LOAD_FAST                'self'
             1022  LOAD_ATTR                _last
             1024  LOAD_ATTR                epilogue
             1026  STORE_FAST               'epilogue'

 L. 396      1028  LOAD_FAST                'epilogue'
             1030  LOAD_STR                 ''
             1032  COMPARE_OP               ==
         1034_1036  POP_JUMP_IF_FALSE  1048  'to 1048'

 L. 397      1038  LOAD_CONST               None
             1040  LOAD_FAST                'self'
             1042  LOAD_ATTR                _last
             1044  STORE_ATTR               epilogue
             1046  JUMP_FORWARD       1106  'to 1106'
           1048_0  COME_FROM          1034  '1034'

 L. 398      1048  LOAD_FAST                'epilogue'
             1050  LOAD_CONST               None
             1052  <117>                 1  ''
         1054_1056  POP_JUMP_IF_FALSE  1176  'to 1176'

 L. 399      1058  LOAD_GLOBAL              NLCRE_eol
             1060  LOAD_METHOD              search
             1062  LOAD_FAST                'epilogue'
             1064  CALL_METHOD_1         1  ''
             1066  STORE_FAST               'mo'

 L. 400      1068  LOAD_FAST                'mo'
         1070_1072  POP_JUMP_IF_FALSE  1176  'to 1176'

 L. 401      1074  LOAD_GLOBAL              len
             1076  LOAD_FAST                'mo'
             1078  LOAD_METHOD              group
             1080  LOAD_CONST               0
             1082  CALL_METHOD_1         1  ''
             1084  CALL_FUNCTION_1       1  ''
             1086  STORE_FAST               'end'

 L. 402      1088  LOAD_FAST                'epilogue'
             1090  LOAD_CONST               None
             1092  LOAD_FAST                'end'
             1094  UNARY_NEGATIVE   
             1096  BUILD_SLICE_2         2 
             1098  BINARY_SUBSCR    
             1100  LOAD_FAST                'self'
             1102  LOAD_ATTR                _last
             1104  STORE_ATTR               epilogue
           1106_0  COME_FROM          1046  '1046'
             1106  JUMP_FORWARD       1176  'to 1176'
           1108_0  COME_FROM          1016  '1016'

 L. 404      1108  LOAD_FAST                'self'
             1110  LOAD_ATTR                _last
             1112  LOAD_ATTR                _payload
             1114  STORE_FAST               'payload'

 L. 405      1116  LOAD_GLOBAL              isinstance
             1118  LOAD_FAST                'payload'
             1120  LOAD_GLOBAL              str
             1122  CALL_FUNCTION_2       2  ''
         1124_1126  POP_JUMP_IF_FALSE  1176  'to 1176'

 L. 406      1128  LOAD_GLOBAL              NLCRE_eol
             1130  LOAD_METHOD              search
             1132  LOAD_FAST                'payload'
             1134  CALL_METHOD_1         1  ''
             1136  STORE_FAST               'mo'

 L. 407      1138  LOAD_FAST                'mo'
         1140_1142  POP_JUMP_IF_FALSE  1176  'to 1176'

 L. 408      1144  LOAD_FAST                'payload'
             1146  LOAD_CONST               None
             1148  LOAD_GLOBAL              len
             1150  LOAD_FAST                'mo'
             1152  LOAD_METHOD              group
             1154  LOAD_CONST               0
             1156  CALL_METHOD_1         1  ''
             1158  CALL_FUNCTION_1       1  ''
             1160  UNARY_NEGATIVE   
             1162  BUILD_SLICE_2         2 
             1164  BINARY_SUBSCR    
             1166  STORE_FAST               'payload'

 L. 409      1168  LOAD_FAST                'payload'
             1170  LOAD_FAST                'self'
             1172  LOAD_ATTR                _last
             1174  STORE_ATTR               _payload
           1176_0  COME_FROM          1140  '1140'
           1176_1  COME_FROM          1124  '1124'
           1176_2  COME_FROM          1106  '1106'
           1176_3  COME_FROM          1070  '1070'
           1176_4  COME_FROM          1054  '1054'

 L. 410      1176  LOAD_FAST                'self'
             1178  LOAD_ATTR                _input
             1180  LOAD_METHOD              pop_eof_matcher
             1182  CALL_METHOD_0         0  ''
             1184  POP_TOP          

 L. 411      1186  LOAD_FAST                'self'
             1188  LOAD_METHOD              _pop_message
             1190  CALL_METHOD_0         0  ''
             1192  POP_TOP          

 L. 414      1194  LOAD_FAST                'self'
             1196  LOAD_ATTR                _cur
             1198  LOAD_FAST                'self'
             1200  STORE_ATTR               _last
             1202  JUMP_BACK           694  'to 694'
           1204_0  COME_FROM           750  '750'

 L. 417      1204  LOAD_FAST                'capturing_preamble'
         1206_1208  POP_JUMP_IF_TRUE   1214  'to 1214'
             1210  <74>             
             1212  RAISE_VARARGS_1       1  'exception instance'
           1214_0  COME_FROM          1206  '1206'

 L. 418      1214  LOAD_FAST                'preamble'
             1216  LOAD_METHOD              append
             1218  LOAD_FAST                'line'
             1220  CALL_METHOD_1         1  ''
             1222  POP_TOP          
         1224_1226  JUMP_BACK           694  'to 694'
           1228_0  COME_FROM           780  '780'
           1228_1  COME_FROM           734  '734'

 L. 422      1228  LOAD_FAST                'capturing_preamble'
         1230_1232  POP_JUMP_IF_FALSE  1332  'to 1332'

 L. 423      1234  LOAD_GLOBAL              errors
             1236  LOAD_METHOD              StartBoundaryNotFoundDefect
             1238  CALL_METHOD_0         0  ''
             1240  STORE_FAST               'defect'

 L. 424      1242  LOAD_FAST                'self'
             1244  LOAD_ATTR                policy
             1246  LOAD_METHOD              handle_defect
             1248  LOAD_FAST                'self'
             1250  LOAD_ATTR                _cur
             1252  LOAD_FAST                'defect'
             1254  CALL_METHOD_2         2  ''
             1256  POP_TOP          

 L. 425      1258  LOAD_FAST                'self'
             1260  LOAD_ATTR                _cur
             1262  LOAD_METHOD              set_payload
             1264  LOAD_GLOBAL              EMPTYSTRING
             1266  LOAD_METHOD              join
             1268  LOAD_FAST                'preamble'
             1270  CALL_METHOD_1         1  ''
             1272  CALL_METHOD_1         1  ''
             1274  POP_TOP          

 L. 426      1276  BUILD_LIST_0          0 
             1278  STORE_FAST               'epilogue'

 L. 427      1280  LOAD_FAST                'self'
             1282  LOAD_ATTR                _input
             1284  GET_ITER         
           1286_0  COME_FROM          1310  '1310'
           1286_1  COME_FROM          1306  '1306'
           1286_2  COME_FROM          1296  '1296'
             1286  FOR_ITER           1314  'to 1314'
             1288  STORE_FAST               'line'

 L. 428      1290  LOAD_FAST                'line'
             1292  LOAD_GLOBAL              NeedMoreData
             1294  <117>                 0  ''
         1296_1298  POP_JUMP_IF_FALSE_BACK  1286  'to 1286'

 L. 429      1300  LOAD_GLOBAL              NeedMoreData
             1302  YIELD_VALUE      
             1304  POP_TOP          

 L. 430  1306_1308  BREAK_LOOP         1286  'to 1286'
         1310_1312  JUMP_BACK          1286  'to 1286'
           1314_0  COME_FROM          1286  '1286'

 L. 431      1314  LOAD_GLOBAL              EMPTYSTRING
             1316  LOAD_METHOD              join
             1318  LOAD_FAST                'epilogue'
             1320  CALL_METHOD_1         1  ''
             1322  LOAD_FAST                'self'
             1324  LOAD_ATTR                _cur
             1326  STORE_ATTR               epilogue

 L. 432      1328  LOAD_CONST               None
             1330  RETURN_VALUE     
           1332_0  COME_FROM          1230  '1230'

 L. 435      1332  LOAD_FAST                'close_boundary_seen'
         1334_1336  POP_JUMP_IF_TRUE   1366  'to 1366'

 L. 436      1338  LOAD_GLOBAL              errors
             1340  LOAD_METHOD              CloseBoundaryNotFoundDefect
             1342  CALL_METHOD_0         0  ''
             1344  STORE_FAST               'defect'

 L. 437      1346  LOAD_FAST                'self'
             1348  LOAD_ATTR                policy
             1350  LOAD_METHOD              handle_defect
             1352  LOAD_FAST                'self'
             1354  LOAD_ATTR                _cur
             1356  LOAD_FAST                'defect'
             1358  CALL_METHOD_2         2  ''
             1360  POP_TOP          

 L. 438      1362  LOAD_CONST               None
             1364  RETURN_VALUE     
           1366_0  COME_FROM          1334  '1334'

 L. 442      1366  LOAD_FAST                'linesep'
         1368_1370  POP_JUMP_IF_FALSE  1380  'to 1380'

 L. 443      1372  LOAD_STR                 ''
             1374  BUILD_LIST_1          1 
             1376  STORE_FAST               'epilogue'
             1378  JUMP_FORWARD       1384  'to 1384'
           1380_0  COME_FROM          1368  '1368'

 L. 445      1380  BUILD_LIST_0          0 
             1382  STORE_FAST               'epilogue'
           1384_0  COME_FROM          1378  '1378'

 L. 446      1384  LOAD_FAST                'self'
             1386  LOAD_ATTR                _input
             1388  GET_ITER         
           1390_0  COME_FROM          1424  '1424'
           1390_1  COME_FROM          1410  '1410'
             1390  FOR_ITER           1428  'to 1428'
             1392  STORE_FAST               'line'

 L. 447      1394  LOAD_FAST                'line'
             1396  LOAD_GLOBAL              NeedMoreData
             1398  <117>                 0  ''
         1400_1402  POP_JUMP_IF_FALSE  1414  'to 1414'

 L. 448      1404  LOAD_GLOBAL              NeedMoreData
             1406  YIELD_VALUE      
             1408  POP_TOP          

 L. 449  1410_1412  JUMP_BACK          1390  'to 1390'
           1414_0  COME_FROM          1400  '1400'

 L. 450      1414  LOAD_FAST                'epilogue'
             1416  LOAD_METHOD              append
             1418  LOAD_FAST                'line'
             1420  CALL_METHOD_1         1  ''
             1422  POP_TOP          
         1424_1426  JUMP_BACK          1390  'to 1390'
           1428_0  COME_FROM          1390  '1390'

 L. 454      1428  LOAD_FAST                'epilogue'
         1430_1432  POP_JUMP_IF_FALSE  1484  'to 1484'

 L. 455      1434  LOAD_FAST                'epilogue'
             1436  LOAD_CONST               0
             1438  BINARY_SUBSCR    
             1440  STORE_FAST               'firstline'

 L. 456      1442  LOAD_GLOBAL              NLCRE_bol
             1444  LOAD_METHOD              match
             1446  LOAD_FAST                'firstline'
             1448  CALL_METHOD_1         1  ''
             1450  STORE_FAST               'bolmo'

 L. 457      1452  LOAD_FAST                'bolmo'
         1454_1456  POP_JUMP_IF_FALSE  1484  'to 1484'

 L. 458      1458  LOAD_FAST                'firstline'
             1460  LOAD_GLOBAL              len
             1462  LOAD_FAST                'bolmo'
             1464  LOAD_METHOD              group
             1466  LOAD_CONST               0
             1468  CALL_METHOD_1         1  ''
             1470  CALL_FUNCTION_1       1  ''
             1472  LOAD_CONST               None
             1474  BUILD_SLICE_2         2 
             1476  BINARY_SUBSCR    
             1478  LOAD_FAST                'epilogue'
             1480  LOAD_CONST               0
             1482  STORE_SUBSCR     
           1484_0  COME_FROM          1454  '1454'
           1484_1  COME_FROM          1430  '1430'

 L. 459      1484  LOAD_GLOBAL              EMPTYSTRING
             1486  LOAD_METHOD              join
             1488  LOAD_FAST                'epilogue'
             1490  CALL_METHOD_1         1  ''
             1492  LOAD_FAST                'self'
             1494  LOAD_ATTR                _cur
             1496  STORE_ATTR               epilogue

 L. 460      1498  LOAD_CONST               None
             1500  RETURN_VALUE     
           1502_0  COME_FROM           476  '476'

 L. 463      1502  BUILD_LIST_0          0 
             1504  STORE_FAST               'lines'

 L. 464      1506  LOAD_FAST                'self'
             1508  LOAD_ATTR                _input
             1510  GET_ITER         
           1512_0  COME_FROM          1546  '1546'
           1512_1  COME_FROM          1532  '1532'
             1512  FOR_ITER           1550  'to 1550'
             1514  STORE_FAST               'line'

 L. 465      1516  LOAD_FAST                'line'
             1518  LOAD_GLOBAL              NeedMoreData
             1520  <117>                 0  ''
         1522_1524  POP_JUMP_IF_FALSE  1536  'to 1536'

 L. 466      1526  LOAD_GLOBAL              NeedMoreData
             1528  YIELD_VALUE      
             1530  POP_TOP          

 L. 467  1532_1534  JUMP_BACK          1512  'to 1512'
           1536_0  COME_FROM          1522  '1522'

 L. 468      1536  LOAD_FAST                'lines'
             1538  LOAD_METHOD              append
             1540  LOAD_FAST                'line'
             1542  CALL_METHOD_1         1  ''
             1544  POP_TOP          
         1546_1548  JUMP_BACK          1512  'to 1512'
           1550_0  COME_FROM          1512  '1512'

 L. 469      1550  LOAD_FAST                'self'
             1552  LOAD_ATTR                _cur
             1554  LOAD_METHOD              set_payload
             1556  LOAD_GLOBAL              EMPTYSTRING
             1558  LOAD_METHOD              join
             1560  LOAD_FAST                'lines'
             1562  CALL_METHOD_1         1  ''
             1564  CALL_METHOD_1         1  ''
             1566  POP_TOP          

Parse error at or near `<117>' instruction at offset 26

    def _parse_headers--- This code section failed: ---

 L. 473         0  LOAD_STR                 ''
                2  STORE_FAST               'lastheader'

 L. 474         4  BUILD_LIST_0          0 
                6  STORE_FAST               'lastvalue'

 L. 475         8  LOAD_GLOBAL              enumerate
               10  LOAD_FAST                'lines'
               12  CALL_FUNCTION_1       1  ''
               14  GET_ITER         
             16_0  COME_FROM           330  '330'
             16_1  COME_FROM           292  '292'
             16_2  COME_FROM           246  '246'
             16_3  COME_FROM           184  '184'
             16_4  COME_FROM            80  '80'
             16_5  COME_FROM            68  '68'
            16_18  FOR_ITER            332  'to 332'
               20  UNPACK_SEQUENCE_2     2 
               22  STORE_FAST               'lineno'
               24  STORE_FAST               'line'

 L. 477        26  LOAD_FAST                'line'
               28  LOAD_CONST               0
               30  BINARY_SUBSCR    
               32  LOAD_STR                 ' \t'
               34  <118>                 0  ''
               36  POP_JUMP_IF_FALSE    82  'to 82'

 L. 478        38  LOAD_FAST                'lastheader'
               40  POP_JUMP_IF_TRUE     70  'to 70'

 L. 482        42  LOAD_GLOBAL              errors
               44  LOAD_METHOD              FirstHeaderLineIsContinuationDefect
               46  LOAD_FAST                'line'
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'defect'

 L. 483        52  LOAD_FAST                'self'
               54  LOAD_ATTR                policy
               56  LOAD_METHOD              handle_defect
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                _cur
               62  LOAD_FAST                'defect'
               64  CALL_METHOD_2         2  ''
               66  POP_TOP          

 L. 484        68  JUMP_BACK            16  'to 16'
             70_0  COME_FROM            40  '40'

 L. 485        70  LOAD_FAST                'lastvalue'
               72  LOAD_METHOD              append
               74  LOAD_FAST                'line'
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          

 L. 486        80  JUMP_BACK            16  'to 16'
             82_0  COME_FROM            36  '36'

 L. 487        82  LOAD_FAST                'lastheader'
               84  POP_JUMP_IF_FALSE   116  'to 116'

 L. 488        86  LOAD_FAST                'self'
               88  LOAD_ATTR                _cur
               90  LOAD_ATTR                set_raw
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                policy
               96  LOAD_METHOD              header_source_parse
               98  LOAD_FAST                'lastvalue'
              100  CALL_METHOD_1         1  ''
              102  CALL_FUNCTION_EX      0  'positional arguments only'
              104  POP_TOP          

 L. 489       106  LOAD_STR                 ''
              108  BUILD_LIST_0          0 
              110  ROT_TWO          
              112  STORE_FAST               'lastheader'
              114  STORE_FAST               'lastvalue'
            116_0  COME_FROM            84  '84'

 L. 491       116  LOAD_FAST                'line'
              118  LOAD_METHOD              startswith
              120  LOAD_STR                 'From '
              122  CALL_METHOD_1         1  ''
              124  POP_JUMP_IF_FALSE   248  'to 248'

 L. 492       126  LOAD_FAST                'lineno'
              128  LOAD_CONST               0
              130  COMPARE_OP               ==
              132  POP_JUMP_IF_FALSE   188  'to 188'

 L. 494       134  LOAD_GLOBAL              NLCRE_eol
              136  LOAD_METHOD              search
              138  LOAD_FAST                'line'
              140  CALL_METHOD_1         1  ''
              142  STORE_FAST               'mo'

 L. 495       144  LOAD_FAST                'mo'
              146  POP_JUMP_IF_FALSE   172  'to 172'

 L. 496       148  LOAD_FAST                'line'
              150  LOAD_CONST               None
              152  LOAD_GLOBAL              len
              154  LOAD_FAST                'mo'
              156  LOAD_METHOD              group
              158  LOAD_CONST               0
              160  CALL_METHOD_1         1  ''
              162  CALL_FUNCTION_1       1  ''
              164  UNARY_NEGATIVE   
              166  BUILD_SLICE_2         2 
              168  BINARY_SUBSCR    
              170  STORE_FAST               'line'
            172_0  COME_FROM           146  '146'

 L. 497       172  LOAD_FAST                'self'
              174  LOAD_ATTR                _cur
              176  LOAD_METHOD              set_unixfrom
              178  LOAD_FAST                'line'
              180  CALL_METHOD_1         1  ''
              182  POP_TOP          

 L. 498       184  JUMP_BACK            16  'to 16'
              186  JUMP_FORWARD        248  'to 248'
            188_0  COME_FROM           132  '132'

 L. 499       188  LOAD_FAST                'lineno'
              190  LOAD_GLOBAL              len
              192  LOAD_FAST                'lines'
              194  CALL_FUNCTION_1       1  ''
              196  LOAD_CONST               1
              198  BINARY_SUBTRACT  
              200  COMPARE_OP               ==
              202  POP_JUMP_IF_FALSE   222  'to 222'

 L. 503       204  LOAD_FAST                'self'
              206  LOAD_ATTR                _input
              208  LOAD_METHOD              unreadline
              210  LOAD_FAST                'line'
              212  CALL_METHOD_1         1  ''
              214  POP_TOP          

 L. 504       216  POP_TOP          
              218  LOAD_CONST               None
              220  RETURN_VALUE     
            222_0  COME_FROM           202  '202'

 L. 508       222  LOAD_GLOBAL              errors
              224  LOAD_METHOD              MisplacedEnvelopeHeaderDefect
              226  LOAD_FAST                'line'
              228  CALL_METHOD_1         1  ''
              230  STORE_FAST               'defect'

 L. 509       232  LOAD_FAST                'self'
              234  LOAD_ATTR                _cur
              236  LOAD_ATTR                defects
              238  LOAD_METHOD              append
              240  LOAD_FAST                'defect'
              242  CALL_METHOD_1         1  ''
              244  POP_TOP          

 L. 510       246  JUMP_BACK            16  'to 16'
            248_0  COME_FROM           186  '186'
            248_1  COME_FROM           124  '124'

 L. 514       248  LOAD_FAST                'line'
              250  LOAD_METHOD              find
              252  LOAD_STR                 ':'
              254  CALL_METHOD_1         1  ''
              256  STORE_FAST               'i'

 L. 519       258  LOAD_FAST                'i'
              260  LOAD_CONST               0
              262  COMPARE_OP               ==
          264_266  POP_JUMP_IF_FALSE   294  'to 294'

 L. 520       268  LOAD_GLOBAL              errors
              270  LOAD_METHOD              InvalidHeaderDefect
              272  LOAD_STR                 'Missing header name.'
              274  CALL_METHOD_1         1  ''
              276  STORE_FAST               'defect'

 L. 521       278  LOAD_FAST                'self'
              280  LOAD_ATTR                _cur
              282  LOAD_ATTR                defects
              284  LOAD_METHOD              append
              286  LOAD_FAST                'defect'
              288  CALL_METHOD_1         1  ''
              290  POP_TOP          

 L. 522       292  JUMP_BACK            16  'to 16'
            294_0  COME_FROM           264  '264'

 L. 524       294  LOAD_FAST                'i'
              296  LOAD_CONST               0
              298  COMPARE_OP               >
          300_302  POP_JUMP_IF_TRUE    312  'to 312'
              304  <74>             
              306  LOAD_STR                 '_parse_headers fed line with no : and no leading WS'
              308  CALL_FUNCTION_1       1  ''
              310  RAISE_VARARGS_1       1  'exception instance'
            312_0  COME_FROM           300  '300'

 L. 525       312  LOAD_FAST                'line'
              314  LOAD_CONST               None
              316  LOAD_FAST                'i'
              318  BUILD_SLICE_2         2 
              320  BINARY_SUBSCR    
              322  STORE_FAST               'lastheader'

 L. 526       324  LOAD_FAST                'line'
              326  BUILD_LIST_1          1 
              328  STORE_FAST               'lastvalue'
              330  JUMP_BACK            16  'to 16'
            332_0  COME_FROM            16  '16'

 L. 528       332  LOAD_FAST                'lastheader'
          334_336  POP_JUMP_IF_FALSE   358  'to 358'

 L. 529       338  LOAD_FAST                'self'
              340  LOAD_ATTR                _cur
              342  LOAD_ATTR                set_raw
              344  LOAD_FAST                'self'
              346  LOAD_ATTR                policy
              348  LOAD_METHOD              header_source_parse
              350  LOAD_FAST                'lastvalue'
              352  CALL_METHOD_1         1  ''
              354  CALL_FUNCTION_EX      0  'positional arguments only'
              356  POP_TOP          
            358_0  COME_FROM           334  '334'

Parse error at or near `<118>' instruction at offset 34


class BytesFeedParser(FeedParser):
    __doc__ = 'Like FeedParser, but feed accepts bytes.'

    def feed(self, data):
        super().feed(data.decode'ascii''surrogateescape')