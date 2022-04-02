# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\future\backports\email\feedparser.py
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
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future.builtins import object, range, super
from future.utils import implements_iterator, PY3
__all__ = [
 b'FeedParser', b'BytesFeedParser']
import re
from future.backports.email import errors
from future.backports.email import message
from future.backports.email._policybase import compat32
NLCRE = re.compile(b'\r\n|\r|\n')
NLCRE_bol = re.compile(b'(\r\n|\r|\n)')
NLCRE_eol = re.compile(b'(\r\n|\r|\n)\\Z')
NLCRE_crack = re.compile(b'(\r\n|\r|\n)')
headerRE = re.compile(b'^(From |[\\041-\\071\\073-\\176]{1,}:|[\\t ])')
EMPTYSTRING = b''
NL = b'\n'
NeedMoreData = object()

class BufferedSubFile(object):
    """A file-ish object that can have new data loaded into it.

    You can also push and pop line-matching predicates onto a stack.  When the
    current predicate matches the current line, a false EOF response
    (i.e. empty string) is returned instead.  This lets the parser adhere to a
    simple abstraction -- it parses until EOF closes the current message.
    """

    def __init__(self):
        self._partial = b''
        self._lines = []
        self._eofstack = []
        self._closed = False

    def push_eof_matcher(self, pred):
        self._eofstack.append(pred)

    def pop_eof_matcher(self):
        return self._eofstack.pop()

    def close(self):
        self._lines.append(self._partial)
        self._partial = b''
        self._closed = True

    def readline(self):
        if not self._lines:
            if self._closed:
                return b''
            return NeedMoreData
        line = self._lines.pop()
        for ateof in self._eofstack[::-1]:
            if ateof(line):
                self._lines.append(line)
                return b''

        return line

    def unreadline(self, line):
        assert line is not NeedMoreData
        self._lines.append(line)

    def push(self, data):
        """Push some new data into this object."""
        data, self._partial = self._partial + data, b''
        parts = NLCRE_crack.split(data)
        self._partial = parts.pop()
        if not self._partial and parts and parts[(-1)].endswith(b'\r'):
            self._partial = parts.pop(-2) + parts.pop()
        lines = []
        for i in range(len(parts) // 2):
            lines.append(parts[(i * 2)] + parts[(i * 2 + 1)])

        self.pushlines(lines)

    def pushlines(self, lines):
        self._lines[:0] = lines[::-1]

    def __iter__(self):
        return self

    def __next__(self):
        line = self.readline()
        if line == b'':
            raise StopIteration
        return line


class FeedParser(object):
    """A feed-style parser of email."""

    def __init__(self, _factory=message.Message, **_3to2kwargs):
        if b'policy' in _3to2kwargs:
            policy = _3to2kwargs[b'policy']
            del _3to2kwargs[b'policy']
        else:
            policy = compat32
        self._factory = _factory
        self.policy = policy
        try:
            _factory(policy=self.policy)
            self._factory_kwds = lambda : {b'policy': self.policy}
        except TypeError:
            self._factory_kwds = lambda : {}

        self._input = BufferedSubFile()
        self._msgstack = []
        if PY3:
            self._parse = self._parsegen().__next__
        else:
            self._parse = self._parsegen().next
        self._cur = None
        self._last = None
        self._headersonly = False
        return

    def _set_headersonly(self):
        self._headersonly = True

    def feed(self, data):
        """Push more data into the parser."""
        self._input.push(data)
        self._call_parse()

    def _call_parse(self):
        try:
            self._parse()
        except StopIteration:
            pass

    def close(self):
        """Parse all remaining data and return the root message object."""
        self._input.close()
        self._call_parse()
        root = self._pop_message()
        assert not self._msgstack
        if root.get_content_maintype() == b'multipart' and not root.is_multipart():
            defect = errors.MultipartInvariantViolationDefect()
            self.policy.handle_defect(root, defect)
        return root

    def _new_message(self):
        msg = self._factory(**self._factory_kwds())
        if self._cur and self._cur.get_content_type() == b'multipart/digest':
            msg.set_default_type(b'message/rfc822')
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

    def _parsegen(self):
        self._new_message()
        headers = []
        for line in self._input:
            if line is NeedMoreData:
                yield NeedMoreData
                continue
            if not headerRE.match(line):
                if not NLCRE.match(line):
                    defect = errors.MissingHeaderBodySeparatorDefect()
                    self.policy.handle_defect(self._cur, defect)
                    self._input.unreadline(line)
                break
            headers.append(line)

        self._parse_headers(headers)
        if self._headersonly:
            lines = []
            while True:
                line = self._input.readline()
                if line is NeedMoreData:
                    yield NeedMoreData
                    continue
                if line == b'':
                    break
                lines.append(line)

            self._cur.set_payload(EMPTYSTRING.join(lines))
            return
        else:
            if self._cur.get_content_type() == b'message/delivery-status':
                while True:
                    self._input.push_eof_matcher(NLCRE.match)
                    for retval in self._parsegen():
                        if retval is NeedMoreData:
                            yield NeedMoreData
                            continue
                        break

                    msg = self._pop_message()
                    self._input.pop_eof_matcher()
                    while True:
                        line = self._input.readline()
                        if line is NeedMoreData:
                            yield NeedMoreData
                            continue
                        break

                    while True:
                        line = self._input.readline()
                        if line is NeedMoreData:
                            yield NeedMoreData
                            continue
                        break

                    if line == b'':
                        break
                    self._input.unreadline(line)

                return
            if self._cur.get_content_maintype() == b'message':
                for retval in self._parsegen():
                    if retval is NeedMoreData:
                        yield NeedMoreData
                        continue
                    break

                self._pop_message()
                return
            if self._cur.get_content_maintype() == b'multipart':
                boundary = self._cur.get_boundary()
                if boundary is None:
                    defect = errors.NoBoundaryInMultipartDefect()
                    self.policy.handle_defect(self._cur, defect)
                    lines = []
                    for line in self._input:
                        if line is NeedMoreData:
                            yield NeedMoreData
                            continue
                        lines.append(line)

                    self._cur.set_payload(EMPTYSTRING.join(lines))
                    return
                if self._cur.get(b'content-transfer-encoding', b'8bit').lower() not in ('7bit',
                                                                                        '8bit',
                                                                                        'binary'):
                    defect = errors.InvalidMultipartContentTransferEncodingDefect()
                    self.policy.handle_defect(self._cur, defect)
                separator = b'--' + boundary
                boundaryre = re.compile(b'(?P<sep>' + re.escape(separator) + b')(?P<end>--)?(?P<ws>[ \\t]*)(?P<linesep>\\r\\n|\\r|\\n)?$')
                capturing_preamble = True
                preamble = []
                linesep = False
                close_boundary_seen = False
                while True:
                    line = self._input.readline()
                    if line is NeedMoreData:
                        yield NeedMoreData
                        continue
                    if line == b'':
                        break
                    mo = boundaryre.match(line)
                    if mo:
                        if mo.group(b'end'):
                            close_boundary_seen = True
                            linesep = mo.group(b'linesep')
                            break
                        if capturing_preamble:
                            if preamble:
                                lastline = preamble[(-1)]
                                eolmo = NLCRE_eol.search(lastline)
                                if eolmo:
                                    preamble[-1] = lastline[:-len(eolmo.group(0))]
                                self._cur.preamble = EMPTYSTRING.join(preamble)
                            capturing_preamble = False
                            self._input.unreadline(line)
                            continue
                        while True:
                            line = self._input.readline()
                            if line is NeedMoreData:
                                yield NeedMoreData
                                continue
                            mo = boundaryre.match(line)
                            if not mo:
                                self._input.unreadline(line)
                                break

                        self._input.push_eof_matcher(boundaryre.match)
                        for retval in self._parsegen():
                            if retval is NeedMoreData:
                                yield NeedMoreData
                                continue
                            break

                        if self._last.get_content_maintype() == b'multipart':
                            epilogue = self._last.epilogue
                            if epilogue == b'':
                                self._last.epilogue = None
                            elif epilogue is not None:
                                mo = NLCRE_eol.search(epilogue)
                                if mo:
                                    end = len(mo.group(0))
                                    self._last.epilogue = epilogue[:-end]
                        else:
                            payload = self._last._payload
                            if isinstance(payload, str):
                                mo = NLCRE_eol.search(payload)
                                if mo:
                                    payload = payload[:-len(mo.group(0))]
                                    self._last._payload = payload
                        self._input.pop_eof_matcher()
                        self._pop_message()
                        self._last = self._cur
                    else:
                        assert capturing_preamble
                        preamble.append(line)

                if capturing_preamble:
                    defect = errors.StartBoundaryNotFoundDefect()
                    self.policy.handle_defect(self._cur, defect)
                    self._cur.set_payload(EMPTYSTRING.join(preamble))
                    epilogue = []
                    for line in self._input:
                        if line is NeedMoreData:
                            yield NeedMoreData
                            continue

                    self._cur.epilogue = EMPTYSTRING.join(epilogue)
                    return
                if not close_boundary_seen:
                    defect = errors.CloseBoundaryNotFoundDefect()
                    self.policy.handle_defect(self._cur, defect)
                    return
                if linesep:
                    epilogue = [
                     b'']
                else:
                    epilogue = []
                for line in self._input:
                    if line is NeedMoreData:
                        yield NeedMoreData
                        continue
                    epilogue.append(line)

                if epilogue:
                    firstline = epilogue[0]
                    bolmo = NLCRE_bol.match(firstline)
                    if bolmo:
                        epilogue[0] = firstline[len(bolmo.group(0)):]
                self._cur.epilogue = EMPTYSTRING.join(epilogue)
                return
            lines = []
            for line in self._input:
                if line is NeedMoreData:
                    yield NeedMoreData
                    continue
                lines.append(line)

            self._cur.set_payload(EMPTYSTRING.join(lines))
            return

    def _parse_headers--- This code section failed: ---

 L. 471         0  LOAD_CONST               ''
                3  STORE_FAST            2  'lastheader'

 L. 472         6  BUILD_LIST_0          0 
                9  STORE_FAST            3  'lastvalue'

 L. 473        12  SETUP_LOOP          396  'to 411'
               15  LOAD_GLOBAL           0  'enumerate'
               18  LOAD_FAST             1  'lines'
               21  CALL_FUNCTION_1       1  None
               24  GET_ITER         
               25  FOR_ITER            382  'to 410'
               28  UNPACK_SEQUENCE_2     2 
               31  STORE_FAST            4  'lineno'
               34  STORE_FAST            5  'line'

 L. 475        37  LOAD_FAST             5  'line'
               40  LOAD_CONST               0
               43  BINARY_SUBSCR    
               44  LOAD_CONST               ' \t'
               47  COMPARE_OP            6  in
               50  POP_JUMP_IF_FALSE   121  'to 121'

 L. 476        53  LOAD_FAST             2  'lastheader'
               56  POP_JUMP_IF_TRUE    102  'to 102'

 L. 480        59  LOAD_GLOBAL           1  'errors'
               62  LOAD_ATTR             2  'FirstHeaderLineIsContinuationDefect'
               65  LOAD_FAST             5  'line'
               68  CALL_FUNCTION_1       1  None
               71  STORE_FAST            6  'defect'

 L. 481        74  LOAD_FAST             0  'self'
               77  LOAD_ATTR             3  'policy'
               80  LOAD_ATTR             4  'handle_defect'
               83  LOAD_FAST             0  'self'
               86  LOAD_ATTR             5  '_cur'
               89  LOAD_FAST             6  'defect'
               92  CALL_FUNCTION_2       2  None
               95  POP_TOP          

 L. 482        96  CONTINUE             25  'to 25'
               99  JUMP_FORWARD          0  'to 102'
            102_0  COME_FROM            99  '99'

 L. 483       102  LOAD_FAST             3  'lastvalue'
              105  LOAD_ATTR             6  'append'
              108  LOAD_FAST             5  'line'
              111  CALL_FUNCTION_1       1  None
              114  POP_TOP          

 L. 484       115  CONTINUE             25  'to 25'
              118  JUMP_FORWARD          0  'to 121'
            121_0  COME_FROM           118  '118'

 L. 485       121  LOAD_FAST             2  'lastheader'
              124  POP_JUMP_IF_FALSE   171  'to 171'

 L. 486       127  LOAD_FAST             0  'self'
              130  LOAD_ATTR             5  '_cur'
              133  LOAD_ATTR             7  'set_raw'
              136  LOAD_FAST             0  'self'
              139  LOAD_ATTR             3  'policy'
              142  LOAD_ATTR             8  'header_source_parse'
              145  LOAD_FAST             3  'lastvalue'
              148  CALL_FUNCTION_1       1  None
              151  CALL_FUNCTION_VAR_0     0  None
              154  POP_TOP          

 L. 487       155  LOAD_CONST               ''
              158  BUILD_LIST_0          0 
              161  ROT_TWO          
              162  STORE_FAST            2  'lastheader'
              165  STORE_FAST            3  'lastvalue'
              168  JUMP_FORWARD          0  'to 171'
            171_0  COME_FROM           168  '168'

 L. 489       171  LOAD_FAST             5  'line'
              174  LOAD_ATTR             9  'startswith'
              177  LOAD_CONST               'From '
              180  CALL_FUNCTION_1       1  None
              183  POP_JUMP_IF_FALSE   352  'to 352'

 L. 490       186  LOAD_FAST             4  'lineno'
              189  LOAD_CONST               0
              192  COMPARE_OP            2  ==
              195  POP_JUMP_IF_FALSE   270  'to 270'

 L. 492       198  LOAD_GLOBAL          10  'NLCRE_eol'
              201  LOAD_ATTR            11  'search'
              204  LOAD_FAST             5  'line'
              207  CALL_FUNCTION_1       1  None
              210  STORE_FAST            7  'mo'

 L. 493       213  LOAD_FAST             7  'mo'
              216  POP_JUMP_IF_FALSE   248  'to 248'

 L. 494       219  LOAD_FAST             5  'line'
              222  LOAD_GLOBAL          12  'len'
              225  LOAD_FAST             7  'mo'
              228  LOAD_ATTR            13  'group'
              231  LOAD_CONST               0
              234  CALL_FUNCTION_1       1  None
              237  CALL_FUNCTION_1       1  None
              240  UNARY_NEGATIVE   
              241  SLICE+2          
              242  STORE_FAST            5  'line'
              245  JUMP_FORWARD          0  'to 248'
            248_0  COME_FROM           245  '245'

 L. 495       248  LOAD_FAST             0  'self'
              251  LOAD_ATTR             5  '_cur'
              254  LOAD_ATTR            14  'set_unixfrom'
              257  LOAD_FAST             5  'line'
              260  CALL_FUNCTION_1       1  None
              263  POP_TOP          

 L. 496       264  CONTINUE             25  'to 25'
              267  JUMP_ABSOLUTE       352  'to 352'

 L. 497       270  LOAD_FAST             4  'lineno'
              273  LOAD_GLOBAL          12  'len'
              276  LOAD_FAST             1  'lines'
              279  CALL_FUNCTION_1       1  None
              282  LOAD_CONST               1
              285  BINARY_SUBTRACT  
              286  COMPARE_OP            2  ==
              289  POP_JUMP_IF_FALSE   312  'to 312'

 L. 501       292  LOAD_FAST             0  'self'
              295  LOAD_ATTR            15  '_input'
              298  LOAD_ATTR            16  'unreadline'
              301  LOAD_FAST             5  'line'
              304  CALL_FUNCTION_1       1  None
              307  POP_TOP          

 L. 502       308  LOAD_CONST               None
              311  RETURN_END_IF    
            312_0  COME_FROM           289  '289'

 L. 506       312  LOAD_GLOBAL           1  'errors'
              315  LOAD_ATTR            17  'MisplacedEnvelopeHeaderDefect'
              318  LOAD_FAST             5  'line'
              321  CALL_FUNCTION_1       1  None
              324  STORE_FAST            6  'defect'

 L. 507       327  LOAD_FAST             0  'self'
              330  LOAD_ATTR             5  '_cur'
              333  LOAD_ATTR            18  'defects'
              336  LOAD_ATTR             6  'append'
              339  LOAD_FAST             6  'defect'
              342  CALL_FUNCTION_1       1  None
              345  POP_TOP          

 L. 508       346  CONTINUE             25  'to 25'
              349  JUMP_FORWARD          0  'to 352'
            352_0  COME_FROM           349  '349'

 L. 512       352  LOAD_FAST             5  'line'
              355  LOAD_ATTR            19  'find'
              358  LOAD_CONST               ':'
              361  CALL_FUNCTION_1       1  None
              364  STORE_FAST            8  'i'

 L. 513       367  LOAD_FAST             8  'i'
              370  LOAD_CONST               0
              373  COMPARE_OP            4  >
              376  POP_JUMP_IF_TRUE    388  'to 388'
              379  LOAD_ASSERT              AssertionError
              382  LOAD_CONST               '_parse_headers fed line with no : and no leading WS'
              385  RAISE_VARARGS_2       2  None

 L. 514       388  LOAD_FAST             5  'line'
              391  LOAD_FAST             8  'i'
              394  SLICE+2          
              395  STORE_FAST            2  'lastheader'

 L. 515       398  LOAD_FAST             5  'line'
              401  BUILD_LIST_1          1 
              404  STORE_FAST            3  'lastvalue'
              407  JUMP_BACK            25  'to 25'
              410  POP_BLOCK        
            411_0  COME_FROM            12  '12'

 L. 517       411  LOAD_FAST             2  'lastheader'
              414  POP_JUMP_IF_FALSE   448  'to 448'

 L. 518       417  LOAD_FAST             0  'self'
              420  LOAD_ATTR             5  '_cur'
              423  LOAD_ATTR             7  'set_raw'
              426  LOAD_FAST             0  'self'
              429  LOAD_ATTR             3  'policy'
              432  LOAD_ATTR             8  'header_source_parse'
              435  LOAD_FAST             3  'lastvalue'
              438  CALL_FUNCTION_1       1  None
              441  CALL_FUNCTION_VAR_0     0  None
              444  POP_TOP          
              445  JUMP_FORWARD          0  'to 448'
            448_0  COME_FROM           445  '445'

Parse error at or near `POP_BLOCK' instruction at offset 410


class BytesFeedParser(FeedParser):
    """Like FeedParser, but feed accepts bytes."""

    def feed(self, data):
        super().feed(data.decode(b'ascii', b'surrogateescape'))