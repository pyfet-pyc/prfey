# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: http\client.py
r"""HTTP/1.1 client library

<intro stuff goes here>
<other stuff, too>

HTTPConnection goes through a number of "states", which define when a client
may legally make another request or fetch the response for a particular
request. This diagram details these state transitions:

    (null)
      |
      | HTTPConnection()
      v
    Idle
      |
      | putrequest()
      v
    Request-started
      |
      | ( putheader() )*  endheaders()
      v
    Request-sent
      |\_____________________________
      |                              | getresponse() raises
      | response = getresponse()     | ConnectionError
      v                              v
    Unread-response                Idle
    [Response-headers-read]
      |\____________________
      |                     |
      | response.read()     | putrequest()
      v                     v
    Idle                  Req-started-unread-response
                     ______/|
                   /        |
   response.read() |        | ( putheader() )*  endheaders()
                   v        v
       Request-started    Req-sent-unread-response
                            |
                            | response.read()
                            v
                          Request-sent

This diagram presents the following rules:
  -- a second request may not be started until {response-headers-read}
  -- a response [object] cannot be retrieved until {request-sent}
  -- there is no differentiation between an unread response body and a
     partially read response body

Note: this enforcement is applied by the HTTPConnection class. The
      HTTPResponse class does not enforce this state machine, which
      implies sophisticated clients may accelerate the request/response
      pipeline. Caution should be taken, though: accelerating the states
      beyond the above pattern may imply knowledge of the server's
      connection-close behavior for certain requests. For example, it
      is impossible to tell whether the server will close the connection
      UNTIL the response headers have been read; this means that further
      requests cannot be placed into the pipeline until it is known that
      the server will NOT be closing the connection.

Logical State                  __state            __response
-------------                  -------            ----------
Idle                           _CS_IDLE           None
Request-started                _CS_REQ_STARTED    None
Request-sent                   _CS_REQ_SENT       None
Unread-response                _CS_IDLE           <response_class>
Req-started-unread-response    _CS_REQ_STARTED    <response_class>
Req-sent-unread-response       _CS_REQ_SENT       <response_class>
"""
import email.parser, email.message, http, io, re, socket, collections.abc
from urllib.parse import urlsplit
__all__ = [
 'HTTPResponse', 'HTTPConnection',
 'HTTPException', 'NotConnected', 'UnknownProtocol',
 'UnknownTransferEncoding', 'UnimplementedFileMode',
 'IncompleteRead', 'InvalidURL', 'ImproperConnectionState',
 'CannotSendRequest', 'CannotSendHeader', 'ResponseNotReady',
 'BadStatusLine', 'LineTooLong', 'RemoteDisconnected', 'error',
 'responses']
HTTP_PORT = 80
HTTPS_PORT = 443
_UNKNOWN = 'UNKNOWN'
_CS_IDLE = 'Idle'
_CS_REQ_STARTED = 'Request-started'
_CS_REQ_SENT = 'Request-sent'
globals().update(http.HTTPStatus.__members__)
responses = {v.phrase:v for v in http.HTTPStatus.__members__.values()}
_MAXLINE = 65536
_MAXHEADERS = 100
_is_legal_header_name = re.compile(b'[^:\\s][^:\\r\\n]*').fullmatch
_is_illegal_header_value = re.compile(b'\\n(?![ \\t])|\\r(?![ \\t\\n])').search
_contains_disallowed_url_pchar_re = re.compile('[\x00- \x7f]')
_contains_disallowed_method_pchar_re = re.compile('[\x00-\x1f]')
_METHODS_EXPECTING_BODY = {
 'PATCH', 'POST', 'PUT'}

def _encode(data, name='data'):
    """Call data.encode("latin-1") but show a better error message."""
    try:
        return data.encode('latin-1')
    except UnicodeEncodeError as err:
        try:
            raise UnicodeEncodeError(err.encoding, err.object, err.start, err.end, "%s (%.20r) is not valid Latin-1. Use %s.encode('utf-8') if you want to send it encoded in UTF-8." % (
             name.title(), data[err.start:err.end], name)) from None
        finally:
            err = None
            del err


class HTTPMessage(email.message.Message):

    def getallmatchingheaders(self, name):
        """Find all header lines matching a given header name.

        Look through the list of headers and find all lines matching a given
        header name (and their continuation lines).  A list of the lines is
        returned, without interpretation.  If the header does not occur, an
        empty list is returned.  If the header occurs multiple times, all
        occurrences are returned.  Case is not important in the header name.

        """
        name = name.lower() + ':'
        n = len(name)
        lst = []
        hit = 0
        for line in self.keys():
            if line[:n].lower() == name:
                hit = 1
            else:
                if not line[:1].isspace():
                    hit = 0
                if hit:
                    lst.append(line)
        else:
            return lst


def parse_headers--- This code section failed: ---

 L. 214         0  BUILD_LIST_0          0 
                2  STORE_FAST               'headers'
              4_0  COME_FROM            82  '82'
              4_1  COME_FROM            78  '78'

 L. 216         4  LOAD_FAST                'fp'
                6  LOAD_METHOD              readline
                8  LOAD_GLOBAL              _MAXLINE
               10  LOAD_CONST               1
               12  BINARY_ADD       
               14  CALL_METHOD_1         1  ''
               16  STORE_FAST               'line'

 L. 217        18  LOAD_GLOBAL              len
               20  LOAD_FAST                'line'
               22  CALL_FUNCTION_1       1  ''
               24  LOAD_GLOBAL              _MAXLINE
               26  COMPARE_OP               >
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L. 218        30  LOAD_GLOBAL              LineTooLong
               32  LOAD_STR                 'header line'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'

 L. 219        38  LOAD_FAST                'headers'
               40  LOAD_METHOD              append
               42  LOAD_FAST                'line'
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          

 L. 220        48  LOAD_GLOBAL              len
               50  LOAD_FAST                'headers'
               52  CALL_FUNCTION_1       1  ''
               54  LOAD_GLOBAL              _MAXHEADERS
               56  COMPARE_OP               >
               58  POP_JUMP_IF_FALSE    72  'to 72'

 L. 221        60  LOAD_GLOBAL              HTTPException
               62  LOAD_STR                 'got more than %d headers'
               64  LOAD_GLOBAL              _MAXHEADERS
               66  BINARY_MODULO    
               68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            58  '58'

 L. 222        72  LOAD_FAST                'line'
               74  LOAD_CONST               (b'\r\n', b'\n', b'')
               76  COMPARE_OP               in
               78  POP_JUMP_IF_FALSE_BACK     4  'to 4'

 L. 223        80  JUMP_FORWARD         84  'to 84'
               82  JUMP_BACK             4  'to 4'
             84_0  COME_FROM            80  '80'

 L. 224        84  LOAD_CONST               b''
               86  LOAD_METHOD              join
               88  LOAD_FAST                'headers'
               90  CALL_METHOD_1         1  ''
               92  LOAD_METHOD              decode
               94  LOAD_STR                 'iso-8859-1'
               96  CALL_METHOD_1         1  ''
               98  STORE_FAST               'hstring'

 L. 225       100  LOAD_GLOBAL              email
              102  LOAD_ATTR                parser
              104  LOAD_ATTR                Parser
              106  LOAD_FAST                '_class'
              108  LOAD_CONST               ('_class',)
              110  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              112  LOAD_METHOD              parsestr
              114  LOAD_FAST                'hstring'
              116  CALL_METHOD_1         1  ''
              118  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 82


class HTTPResponse(io.BufferedIOBase):

    def __init__(self, sock, debuglevel=0, method=None, url=None):
        self.fp = sock.makefile('rb')
        self.debuglevel = debuglevel
        self._method = method
        self.headers = self.msg = None
        self.version = _UNKNOWN
        self.status = _UNKNOWN
        self.reason = _UNKNOWN
        self.chunked = _UNKNOWN
        self.chunk_left = _UNKNOWN
        self.length = _UNKNOWN
        self.will_close = _UNKNOWN

    def _read_status(self):
        line = str(self.fp.readline(_MAXLINE + 1), 'iso-8859-1')
        if len(line) > _MAXLINE:
            raise LineTooLong('status line')
        if self.debuglevel > 0:
            print('reply:', repr(line))
        if not line:
            raise RemoteDisconnected('Remote end closed connection without response')
        try:
            version, status, reason = line.split(None, 2)
        except ValueError:
            try:
                version, status = line.split(None, 1)
                reason = ''
            except ValueError:
                version = ''

        else:
            if not version.startswith('HTTP/'):
                self._close_conn()
                raise BadStatusLine(line)
            try:
                status = int(status)
                if status < 100 or (status > 999):
                    raise BadStatusLine(line)
            except ValueError:
                raise BadStatusLine(line)
            else:
                return (
                 version, status, reason)

    def begin--- This code section failed: ---

 L. 301         0  LOAD_FAST                'self'
                2  LOAD_ATTR                headers
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 303        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM           110  '110'
             14_1  COME_FROM            86  '86'
             14_2  COME_FROM             8  '8'

 L. 307        14  LOAD_FAST                'self'
               16  LOAD_METHOD              _read_status
               18  CALL_METHOD_0         0  ''
               20  UNPACK_SEQUENCE_3     3 
               22  STORE_FAST               'version'
               24  STORE_FAST               'status'
               26  STORE_FAST               'reason'

 L. 308        28  LOAD_FAST                'status'
               30  LOAD_GLOBAL              CONTINUE
               32  COMPARE_OP               !=
               34  POP_JUMP_IF_FALSE    38  'to 38'

 L. 309        36  JUMP_FORWARD        112  'to 112'
             38_0  COME_FROM           108  '108'
             38_1  COME_FROM            96  '96'
             38_2  COME_FROM            34  '34'

 L. 312        38  LOAD_FAST                'self'
               40  LOAD_ATTR                fp
               42  LOAD_METHOD              readline
               44  LOAD_GLOBAL              _MAXLINE
               46  LOAD_CONST               1
               48  BINARY_ADD       
               50  CALL_METHOD_1         1  ''
               52  STORE_FAST               'skip'

 L. 313        54  LOAD_GLOBAL              len
               56  LOAD_FAST                'skip'
               58  CALL_FUNCTION_1       1  ''
               60  LOAD_GLOBAL              _MAXLINE
               62  COMPARE_OP               >
               64  POP_JUMP_IF_FALSE    74  'to 74'

 L. 314        66  LOAD_GLOBAL              LineTooLong
               68  LOAD_STR                 'header line'
               70  CALL_FUNCTION_1       1  ''
               72  RAISE_VARARGS_1       1  'exception instance'
             74_0  COME_FROM            64  '64'

 L. 315        74  LOAD_FAST                'skip'
               76  LOAD_METHOD              strip
               78  CALL_METHOD_0         0  ''
               80  STORE_FAST               'skip'

 L. 316        82  LOAD_FAST                'skip'
               84  POP_JUMP_IF_TRUE     88  'to 88'

 L. 317        86  JUMP_BACK            14  'to 14'
             88_0  COME_FROM            84  '84'

 L. 318        88  LOAD_FAST                'self'
               90  LOAD_ATTR                debuglevel
               92  LOAD_CONST               0
               94  COMPARE_OP               >
               96  POP_JUMP_IF_FALSE_BACK    38  'to 38'

 L. 319        98  LOAD_GLOBAL              print
              100  LOAD_STR                 'header:'
              102  LOAD_FAST                'skip'
              104  CALL_FUNCTION_2       2  ''
              106  POP_TOP          
              108  JUMP_BACK            38  'to 38'
              110  JUMP_BACK            14  'to 14'
            112_0  COME_FROM            36  '36'

 L. 321       112  LOAD_FAST                'status'
              114  DUP_TOP          
              116  LOAD_FAST                'self'
              118  STORE_ATTR               code
              120  LOAD_FAST                'self'
              122  STORE_ATTR               status

 L. 322       124  LOAD_FAST                'reason'
              126  LOAD_METHOD              strip
              128  CALL_METHOD_0         0  ''
              130  LOAD_FAST                'self'
              132  STORE_ATTR               reason

 L. 323       134  LOAD_FAST                'version'
              136  LOAD_CONST               ('HTTP/1.0', 'HTTP/0.9')
              138  COMPARE_OP               in
              140  POP_JUMP_IF_FALSE   150  'to 150'

 L. 325       142  LOAD_CONST               10
              144  LOAD_FAST                'self'
              146  STORE_ATTR               version
              148  JUMP_FORWARD        176  'to 176'
            150_0  COME_FROM           140  '140'

 L. 326       150  LOAD_FAST                'version'
              152  LOAD_METHOD              startswith
              154  LOAD_STR                 'HTTP/1.'
              156  CALL_METHOD_1         1  ''
              158  POP_JUMP_IF_FALSE   168  'to 168'

 L. 327       160  LOAD_CONST               11
              162  LOAD_FAST                'self'
              164  STORE_ATTR               version
              166  JUMP_FORWARD        176  'to 176'
            168_0  COME_FROM           158  '158'

 L. 329       168  LOAD_GLOBAL              UnknownProtocol
              170  LOAD_FAST                'version'
              172  CALL_FUNCTION_1       1  ''
              174  RAISE_VARARGS_1       1  'exception instance'
            176_0  COME_FROM           166  '166'
            176_1  COME_FROM           148  '148'

 L. 331       176  LOAD_GLOBAL              parse_headers
              178  LOAD_FAST                'self'
              180  LOAD_ATTR                fp
              182  CALL_FUNCTION_1       1  ''
              184  DUP_TOP          
              186  LOAD_FAST                'self'
              188  STORE_ATTR               headers
              190  LOAD_FAST                'self'
              192  STORE_ATTR               msg

 L. 333       194  LOAD_FAST                'self'
              196  LOAD_ATTR                debuglevel
              198  LOAD_CONST               0
              200  COMPARE_OP               >
              202  POP_JUMP_IF_FALSE   240  'to 240'

 L. 334       204  LOAD_FAST                'self'
              206  LOAD_ATTR                headers
              208  LOAD_METHOD              items
              210  CALL_METHOD_0         0  ''
              212  GET_ITER         
            214_0  COME_FROM           238  '238'
              214  FOR_ITER            240  'to 240'
              216  UNPACK_SEQUENCE_2     2 
              218  STORE_FAST               'hdr'
              220  STORE_FAST               'val'

 L. 335       222  LOAD_GLOBAL              print
              224  LOAD_STR                 'header:'
              226  LOAD_FAST                'hdr'
              228  LOAD_STR                 ':'
              230  BINARY_ADD       
              232  LOAD_FAST                'val'
              234  CALL_FUNCTION_3       3  ''
              236  POP_TOP          
              238  JUMP_BACK           214  'to 214'
            240_0  COME_FROM           214  '214'
            240_1  COME_FROM           202  '202'

 L. 338       240  LOAD_FAST                'self'
              242  LOAD_ATTR                headers
              244  LOAD_METHOD              get
              246  LOAD_STR                 'transfer-encoding'
              248  CALL_METHOD_1         1  ''
              250  STORE_FAST               'tr_enc'

 L. 339       252  LOAD_FAST                'tr_enc'
          254_256  POP_JUMP_IF_FALSE   286  'to 286'
              258  LOAD_FAST                'tr_enc'
              260  LOAD_METHOD              lower
              262  CALL_METHOD_0         0  ''
              264  LOAD_STR                 'chunked'
              266  COMPARE_OP               ==
          268_270  POP_JUMP_IF_FALSE   286  'to 286'

 L. 340       272  LOAD_CONST               True
              274  LOAD_FAST                'self'
              276  STORE_ATTR               chunked

 L. 341       278  LOAD_CONST               None
              280  LOAD_FAST                'self'
              282  STORE_ATTR               chunk_left
              284  JUMP_FORWARD        292  'to 292'
            286_0  COME_FROM           268  '268'
            286_1  COME_FROM           254  '254'

 L. 343       286  LOAD_CONST               False
              288  LOAD_FAST                'self'
              290  STORE_ATTR               chunked
            292_0  COME_FROM           284  '284'

 L. 346       292  LOAD_FAST                'self'
              294  LOAD_METHOD              _check_close
              296  CALL_METHOD_0         0  ''
              298  LOAD_FAST                'self'
              300  STORE_ATTR               will_close

 L. 350       302  LOAD_CONST               None
              304  LOAD_FAST                'self'
              306  STORE_ATTR               length

 L. 351       308  LOAD_FAST                'self'
              310  LOAD_ATTR                headers
              312  LOAD_METHOD              get
              314  LOAD_STR                 'content-length'
              316  CALL_METHOD_1         1  ''
              318  STORE_FAST               'length'

 L. 352       320  LOAD_FAST                'length'
          322_324  POP_JUMP_IF_FALSE   398  'to 398'
              326  LOAD_FAST                'self'
              328  LOAD_ATTR                chunked
          330_332  POP_JUMP_IF_TRUE    398  'to 398'

 L. 353       334  SETUP_FINALLY       350  'to 350'

 L. 354       336  LOAD_GLOBAL              int
              338  LOAD_FAST                'length'
              340  CALL_FUNCTION_1       1  ''
              342  LOAD_FAST                'self'
              344  STORE_ATTR               length
              346  POP_BLOCK        
              348  JUMP_FORWARD        378  'to 378'
            350_0  COME_FROM_FINALLY   334  '334'

 L. 355       350  DUP_TOP          
              352  LOAD_GLOBAL              ValueError
              354  COMPARE_OP               exception-match
          356_358  POP_JUMP_IF_FALSE   376  'to 376'
              360  POP_TOP          
              362  POP_TOP          
              364  POP_TOP          

 L. 356       366  LOAD_CONST               None
              368  LOAD_FAST                'self'
              370  STORE_ATTR               length
              372  POP_EXCEPT       
              374  JUMP_FORWARD        396  'to 396'
            376_0  COME_FROM           356  '356'
              376  END_FINALLY      
            378_0  COME_FROM           348  '348'

 L. 358       378  LOAD_FAST                'self'
              380  LOAD_ATTR                length
              382  LOAD_CONST               0
              384  COMPARE_OP               <
          386_388  POP_JUMP_IF_FALSE   404  'to 404'

 L. 359       390  LOAD_CONST               None
              392  LOAD_FAST                'self'
              394  STORE_ATTR               length
            396_0  COME_FROM           374  '374'
              396  JUMP_FORWARD        404  'to 404'
            398_0  COME_FROM           330  '330'
            398_1  COME_FROM           322  '322'

 L. 361       398  LOAD_CONST               None
              400  LOAD_FAST                'self'
              402  STORE_ATTR               length
            404_0  COME_FROM           396  '396'
            404_1  COME_FROM           386  '386'

 L. 364       404  LOAD_FAST                'status'
              406  LOAD_GLOBAL              NO_CONTENT
              408  COMPARE_OP               ==
          410_412  POP_JUMP_IF_TRUE    462  'to 462'
              414  LOAD_FAST                'status'
              416  LOAD_GLOBAL              NOT_MODIFIED
              418  COMPARE_OP               ==
          420_422  POP_JUMP_IF_TRUE    462  'to 462'

 L. 365       424  LOAD_CONST               100

 L. 365       426  LOAD_FAST                'status'

 L. 364       428  DUP_TOP          
              430  ROT_THREE        
              432  COMPARE_OP               <=
          434_436  POP_JUMP_IF_FALSE   448  'to 448'

 L. 365       438  LOAD_CONST               200

 L. 364       440  COMPARE_OP               <
          442_444  POP_JUMP_IF_TRUE    462  'to 462'
              446  JUMP_FORWARD        450  'to 450'
            448_0  COME_FROM           434  '434'
              448  POP_TOP          
            450_0  COME_FROM           446  '446'

 L. 366       450  LOAD_FAST                'self'
              452  LOAD_ATTR                _method
              454  LOAD_STR                 'HEAD'
              456  COMPARE_OP               ==

 L. 364   458_460  POP_JUMP_IF_FALSE   468  'to 468'
            462_0  COME_FROM           442  '442'
            462_1  COME_FROM           420  '420'
            462_2  COME_FROM           410  '410'

 L. 367       462  LOAD_CONST               0
              464  LOAD_FAST                'self'
              466  STORE_ATTR               length
            468_0  COME_FROM           458  '458'

 L. 372       468  LOAD_FAST                'self'
              470  LOAD_ATTR                will_close
          472_474  POP_JUMP_IF_TRUE    502  'to 502'

 L. 373       476  LOAD_FAST                'self'
              478  LOAD_ATTR                chunked

 L. 372   480_482  POP_JUMP_IF_TRUE    502  'to 502'

 L. 374       484  LOAD_FAST                'self'
              486  LOAD_ATTR                length
              488  LOAD_CONST               None
              490  COMPARE_OP               is

 L. 372   492_494  POP_JUMP_IF_FALSE   502  'to 502'

 L. 375       496  LOAD_CONST               True
              498  LOAD_FAST                'self'
              500  STORE_ATTR               will_close
            502_0  COME_FROM           492  '492'
            502_1  COME_FROM           480  '480'
            502_2  COME_FROM           472  '472'

Parse error at or near `COME_FROM' instruction at offset 502_1

    def _check_close(self):
        conn = self.headers.get('connection')
        if self.version == 11:
            if conn:
                if 'close' in conn.lower():
                    return True
            return False
        if self.headers.get('keep-alive'):
            return False
        if conn:
            if 'keep-alive' in conn.lower():
                return False
        pconn = self.headers.get('proxy-connection')
        if pconn:
            if 'keep-alive' in pconn.lower():
                return False
        return True

    def _close_conn(self):
        fp = self.fp
        self.fp = None
        fp.close()

    def close(self):
        try:
            super().close()
        finally:
            if self.fp:
                self._close_conn()

    def flush(self):
        super().flush()
        if self.fp:
            self.fp.flush()

    def readable(self):
        """Always returns True"""
        return True

    def isclosed(self):
        """True if the connection is closed."""
        return self.fp is None

    def read(self, amt=None):
        if self.fp is None:
            return b''
        if self._method == 'HEAD':
            self._close_conn()
            return b''
        if amt is not None:
            b = bytearray(amt)
            n = self.readinto(b)
            return memoryview(b)[:n].tobytes()
        if self.chunked:
            return self._readall_chunked()
        if self.length is None:
            s = self.fp.read()
        else:
            try:
                s = self._safe_read(self.length)
            except IncompleteRead:
                self._close_conn()
                raise
            else:
                self.length = 0
        self._close_conn()
        return s

    def readinto(self, b):
        """Read up to len(b) bytes into bytearray b and return the number
        of bytes read.
        """
        if self.fp is None:
            return 0
        if self._method == 'HEAD':
            self._close_conn()
            return 0
        if self.chunked:
            return self._readinto_chunked(b)
        if self.length is not None:
            if len(b) > self.length:
                b = memoryview(b)[0:self.length]
        n = self.fp.readinto(b)
        if not n or b:
            self._close_conn()
        else:
            pass
        if self.length is not None:
            self.length -= n
            if not self.length:
                self._close_conn()
            return n

    def _read_next_chunk_size(self):
        line = self.fp.readline(_MAXLINE + 1)
        if len(line) > _MAXLINE:
            raise LineTooLong('chunk size')
        i = line.find(b';')
        if i >= 0:
            line = line[:i]
        try:
            return int(line, 16)
        except ValueError:
            self._close_conn()
            raise

    def _read_and_discard_trailer--- This code section failed: ---
              0_0  COME_FROM            52  '52'
              0_1  COME_FROM            48  '48'

 L. 530         0  LOAD_FAST                'self'
                2  LOAD_ATTR                fp
                4  LOAD_METHOD              readline
                6  LOAD_GLOBAL              _MAXLINE
                8  LOAD_CONST               1
               10  BINARY_ADD       
               12  CALL_METHOD_1         1  ''
               14  STORE_FAST               'line'

 L. 531        16  LOAD_GLOBAL              len
               18  LOAD_FAST                'line'
               20  CALL_FUNCTION_1       1  ''
               22  LOAD_GLOBAL              _MAXLINE
               24  COMPARE_OP               >
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 532        28  LOAD_GLOBAL              LineTooLong
               30  LOAD_STR                 'trailer line'
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            26  '26'

 L. 533        36  LOAD_FAST                'line'
               38  POP_JUMP_IF_TRUE     42  'to 42'

 L. 536        40  JUMP_FORWARD         54  'to 54'
             42_0  COME_FROM            38  '38'

 L. 537        42  LOAD_FAST                'line'
               44  LOAD_CONST               (b'\r\n', b'\n', b'')
               46  COMPARE_OP               in
               48  POP_JUMP_IF_FALSE_BACK     0  'to 0'

 L. 538        50  JUMP_FORWARD         54  'to 54'
               52  JUMP_BACK             0  'to 0'
             54_0  COME_FROM            50  '50'
             54_1  COME_FROM            40  '40'

Parse error at or near `JUMP_BACK' instruction at offset 52

    def _get_chunk_left(self):
        chunk_left = self.chunk_left
        if not chunk_left:
            if chunk_left is not None:
                self._safe_read(2)
            try:
                chunk_left = self._read_next_chunk_size()
            except ValueError:
                raise IncompleteRead(b'')
            else:
                if chunk_left == 0:
                    self._read_and_discard_trailer()
                    self._close_conn()
                    chunk_left = None
                self.chunk_left = chunk_left
            return chunk_left

    def _readall_chunked(self):
        assert self.chunked != _UNKNOWN
        value = []
        try:
            while True:
                chunk_left = self._get_chunk_left()
                if chunk_left is None:
                    pass
                else:
                    value.append(self._safe_read(chunk_left))
                    self.chunk_left = 0

            return (b'').join(value)
        except IncompleteRead:
            raise IncompleteRead((b'').join(value))

    def _readinto_chunked(self, b):
        assert self.chunked != _UNKNOWN
        total_bytes = 0
        mvb = memoryview(b)
        try:
            while True:
                chunk_left = self._get_chunk_left()
                if chunk_left is None:
                    return total_bytes
                else:
                    if len(mvb) <= chunk_left:
                        n = self._safe_readinto(mvb)
                        self.chunk_left = chunk_left - n
                        return total_bytes + n
                    temp_mvb = mvb[:chunk_left]
                    n = self._safe_readinto(temp_mvb)
                    mvb = mvb[n:]
                    total_bytes += n
                    self.chunk_left = 0

        except IncompleteRead:
            raise IncompleteRead(bytes(b[0:total_bytes]))

    def _safe_read(self, amt):
        """Read the number of bytes requested.

        This function should be used when <amt> bytes "should" be present for
        reading. If the bytes are truly not available (due to EOF), then the
        IncompleteRead exception can be used to detect the problem.
        """
        data = self.fp.read(amt)
        if len(data) < amt:
            raise IncompleteRead(data, amt - len(data))
        return data

    def _safe_readinto(self, b):
        """Same as _safe_read, but for reading into a buffer."""
        amt = len(b)
        n = self.fp.readinto(b)
        if n < amt:
            raise IncompleteRead(bytes(b[:n]), amt - n)
        return n

    def read1(self, n=-1):
        """Read with at most one underlying system call.  If at least one
        byte is buffered, return that instead.
        """
        if self.fp is None or (self._method == 'HEAD'):
            return b''
        if self.chunked:
            return self._read1_chunked(n)
        if self.length is not None:
            if n < 0 or (n > self.length):
                n = self.length
            result = self.fp.read1(n)
            if not result or n:
                self._close_conn()
            elif self.length is not None:
                self.length -= len(result)
            return result

    def peek(self, n=-1):
        if self.fp is None or (self._method == 'HEAD'):
            return b''
        if self.chunked:
            return self._peek_chunked(n)
        return self.fp.peek(n)

    def readline(self, limit=-1):
        if self.fp is None or (self._method == 'HEAD'):
            return b''
        if self.chunked:
            return super().readline(limit)
        if self.length is not None:
            if limit < 0 or (limit > self.length):
                limit = self.length
            result = self.fp.readline(limit)
            if not result or limit:
                self._close_conn()
            elif self.length is not None:
                self.length -= len(result)
            return result

    def _read1_chunked(self, n):
        chunk_left = self._get_chunk_left()
        if chunk_left is None or (n == 0):
            return b''
        if not 0 <= n <= chunk_left:
            n = chunk_left
        read = self.fp.read1(n)
        self.chunk_left -= len(read)
        if not read:
            raise IncompleteRead(b'')
        return read

    def _peek_chunked(self, n):
        try:
            chunk_left = self._get_chunk_left()
        except IncompleteRead:
            return b''
        else:
            if chunk_left is None:
                return b''
            else:
                return self.fp.peek(chunk_left)[:chunk_left]

    def fileno(self):
        return self.fp.fileno()

    def getheader(self, name, default=None):
        """Returns the value of the header matching *name*.

        If there are multiple matching headers, the values are
        combined into a single string separated by commas and spaces.

        If no matching header is found, returns *default* or None if
        the *default* is not specified.

        If the headers are unknown, raises http.client.ResponseNotReady.

        """
        if self.headers is None:
            raise ResponseNotReady()
        headers = self.headers.get_all(name) or default
        if not (isinstance(headers, str) or hasattr(headers, '__iter__')):
            return headers
        return ', '.join(headers)

    def getheaders(self):
        """Return list of (header, value) tuples."""
        if self.headers is None:
            raise ResponseNotReady()
        return list(self.headers.items())

    def __iter__(self):
        return self

    def info(self):
        """Returns an instance of the class mimetools.Message containing
        meta-information associated with the URL.

        When the method is HTTP, these headers are those returned by
        the server at the head of the retrieved HTML page (including
        Content-Length and Content-Type).

        When the method is FTP, a Content-Length header will be
        present if (as is now usual) the server passed back a file
        length in response to the FTP retrieval request. A
        Content-Type header will be present if the MIME type can be
        guessed.

        When the method is local-file, returned headers will include
        a Date representing the file's last-modified time, a
        Content-Length giving file size, and a Content-Type
        containing a guess at the file's type. See also the
        description of the mimetools module.

        """
        return self.headers

    def geturl(self):
        """Return the real URL of the page.

        In some cases, the HTTP server redirects a client to another
        URL. The urlopen() function handles this transparently, but in
        some cases the caller needs to know which URL the client was
        redirected to. The geturl() method can be used to get at this
        redirected URL.

        """
        return self.url

    def getcode(self):
        """Return the HTTP status code that was sent with the response,
        or None if the URL is not an HTTP URL.

        """
        return self.status


class HTTPConnection:
    _http_vsn = 11
    _http_vsn_str = 'HTTP/1.1'
    response_class = HTTPResponse
    default_port = HTTP_PORT
    auto_open = 1
    debuglevel = 0

    @staticmethod
    def _is_textIO(stream):
        """Test whether a file-like object is a text or a binary stream.
        """
        return isinstance(stream, io.TextIOBase)

    @staticmethod
    def _get_content_length--- This code section failed: ---

 L. 792         0  LOAD_FAST                'body'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    28  'to 28'

 L. 795         8  LOAD_FAST                'method'
               10  LOAD_METHOD              upper
               12  CALL_METHOD_0         0  ''
               14  LOAD_GLOBAL              _METHODS_EXPECTING_BODY
               16  COMPARE_OP               in
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L. 796        20  LOAD_CONST               0
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L. 798        24  LOAD_CONST               None
               26  RETURN_VALUE     
             28_0  COME_FROM             6  '6'

 L. 800        28  LOAD_GLOBAL              hasattr
               30  LOAD_FAST                'body'
               32  LOAD_STR                 'read'
               34  CALL_FUNCTION_2       2  ''
               36  POP_JUMP_IF_FALSE    42  'to 42'

 L. 802        38  LOAD_CONST               None
               40  RETURN_VALUE     
             42_0  COME_FROM            36  '36'

 L. 804        42  SETUP_FINALLY        60  'to 60'

 L. 806        44  LOAD_GLOBAL              memoryview
               46  LOAD_FAST                'body'
               48  CALL_FUNCTION_1       1  ''
               50  STORE_FAST               'mv'

 L. 807        52  LOAD_FAST                'mv'
               54  LOAD_ATTR                nbytes
               56  POP_BLOCK        
               58  RETURN_VALUE     
             60_0  COME_FROM_FINALLY    42  '42'

 L. 808        60  DUP_TOP          
               62  LOAD_GLOBAL              TypeError
               64  COMPARE_OP               exception-match
               66  POP_JUMP_IF_FALSE    78  'to 78'
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L. 809        74  POP_EXCEPT       
               76  JUMP_FORWARD         80  'to 80'
             78_0  COME_FROM            66  '66'
               78  END_FINALLY      
             80_0  COME_FROM            76  '76'

 L. 811        80  LOAD_GLOBAL              isinstance
               82  LOAD_FAST                'body'
               84  LOAD_GLOBAL              str
               86  CALL_FUNCTION_2       2  ''
               88  POP_JUMP_IF_FALSE    98  'to 98'

 L. 812        90  LOAD_GLOBAL              len
               92  LOAD_FAST                'body'
               94  CALL_FUNCTION_1       1  ''
               96  RETURN_VALUE     
             98_0  COME_FROM            88  '88'

Parse error at or near `COME_FROM' instruction at offset 78_0

    def __init__(self, host, port=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, source_address=None, blocksize=8192):
        self.timeout = timeout
        self.source_address = source_address
        self.blocksize = blocksize
        self.sock = None
        self._buffer = []
        self._HTTPConnection__response = None
        self._HTTPConnection__state = _CS_IDLE
        self._method = None
        self._tunnel_host = None
        self._tunnel_port = None
        self._tunnel_headers = {}
        self.host, self.port = self._get_hostport(host, port)
        self._validate_host(self.host)
        self._create_connection = socket.create_connection

    def set_tunnel(self, host, port=None, headers=None):
        """Set up host and port for HTTP CONNECT tunnelling.

        In a connection that uses HTTP CONNECT tunneling, the host passed to the
        constructor is used as a proxy server that relays all communication to
        the endpoint passed to `set_tunnel`. This done by sending an HTTP
        CONNECT request to the proxy server when the connection is established.

        This method must be called before the HTTP connection has been
        established.

        The headers argument should be a mapping of extra HTTP headers to send
        with the CONNECT request.
        """
        if self.sock:
            raise RuntimeError("Can't set up tunnel for established connection")
        self._tunnel_host, self._tunnel_port = self._get_hostport(host, port)
        if headers:
            self._tunnel_headers = headers
        else:
            self._tunnel_headers.clear()

    def _get_hostport(self, host, port):
        if port is None:
            i = host.rfind(':')
            j = host.rfind(']')
            if i > j:
                try:
                    port = int(host[i + 1:])
                except ValueError:
                    if host[i + 1:] == '':
                        port = self.default_port
                    else:
                        raise InvalidURL("nonnumeric port: '%s'" % host[i + 1:])
                else:
                    host = host[:i]
            else:
                port = self.default_port
            if host:
                if host[0] == '[':
                    if host[(-1)] == ']':
                        host = host[1:-1]
        return (
         host, port)

    def set_debuglevel(self, level):
        self.debuglevel = level

    def _tunnel(self):
        connect_str = 'CONNECT %s:%d HTTP/1.0\r\n' % (self._tunnel_host,
         self._tunnel_port)
        connect_bytes = connect_str.encode('ascii')
        self.send(connect_bytes)
        for header, value in self._tunnel_headers.items():
            header_str = '%s: %s\r\n' % (header, value)
            header_bytes = header_str.encode('latin-1')
            self.send(header_bytes)
        else:
            self.send(b'\r\n')
            response = self.response_class((self.sock), method=(self._method))
            version, code, message = response._read_status()
            if code != http.HTTPStatus.OK:
                self.close()
                raise OSError('Tunnel connection failed: %d %s' % (code,
                 message.strip()))
                while True:
                    line = response.fp.readline(_MAXLINE + 1)
                    if len(line) > _MAXLINE:
                        raise LineTooLong('header line')
                    if not line:
                        pass
                    else:
                        if line in (b'\r\n', b'\n', b''):
                            pass
                        else:
                            if self.debuglevel > 0:
                                print('header:', line.decode())

    def connect(self):
        """Connect to the host and port specified in __init__."""
        self.sock = self._create_connection((
         self.host, self.port), self.timeout, self.source_address)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        if self._tunnel_host:
            self._tunnel()

    def close(self):
        """Close the connection to the HTTP server."""
        self._HTTPConnection__state = _CS_IDLE
        try:
            sock = self.sock
            if sock:
                self.sock = None
                sock.close()
        finally:
            response = self._HTTPConnection__response
            if response:
                self._HTTPConnection__response = None
                response.close()

    def send(self, data):
        """Send `data' to the server.
        ``data`` can be a string object, a bytes object, an array object, a
        file-like object that supports a .read() method, or an iterable object.
        """
        if self.sock is None:
            if self.auto_open:
                self.connect()
            else:
                raise NotConnected()
        if self.debuglevel > 0:
            print('send:', repr(data))
        if hasattr(data, 'read'):
            if self.debuglevel > 0:
                print('sendIng a read()able')
            encode = self._is_textIO(data)
            if encode:
                if self.debuglevel > 0:
                    print('encoding file using iso-8859-1')
                    while True:
                        datablock = data.read(self.blocksize)
                        if not datablock:
                            pass
                        else:
                            pass
                        if encode:
                            datablock = datablock.encode('iso-8859-1')
                        else:
                            self.sock.sendall(datablock)

                return
        try:
            self.sock.sendall(data)
        except TypeError:
            if isinstance(data, collections.abc.Iterable):
                for d in data:
                    self.sock.sendall(d)

            else:
                raise TypeError('data should be a bytes-like object or an iterable, got %r' % type(data))

    def _output(self, s):
        r"""Add a line of output to the current request buffer.

        Assumes that the line does *not* end with \r\n.
        """
        self._buffer.append(s)

    def _read_readable(self, readable):
        if self.debuglevel > 0:
            print('sendIng a read()able')
        encode = self._is_textIO(readable)
        if encode:
            if self.debuglevel > 0:
                print('encoding file using iso-8859-1')
            while True:
                datablock = readable.read(self.blocksize)
                if not datablock:
                    pass
                else:
                    pass
                if encode:
                    datablock = datablock.encode('iso-8859-1')
                else:
                    yield datablock

    def _send_output(self, message_body=None, encode_chunked=False):
        r"""Send the currently buffered request and clear the buffer.

        Appends an extra \r\n to the buffer.
        A message_body may be specified, to be appended to the request.
        """
        self._buffer.extend((b'', b''))
        msg = (b'\r\n').join(self._buffer)
        del self._buffer[:]
        self.send(msg)
        if message_body is not None:
            if hasattr(message_body, 'read'):
                chunks = self._read_readable(message_body)
        else:
            pass
        try:
            memoryview(message_body)
        except TypeError:
            try:
                chunks = iter(message_body)
            except TypeError:
                raise TypeError('message_body should be a bytes-like object or an iterable, got %r' % type(message_body))

        else:
            chunks = (
             message_body,)
        for chunk in chunks:
            if not chunk:
                if self.debuglevel > 0:
                    print('Zero length chunk ignored')
            else:
                if encode_chunked:
                    if self._http_vsn == 11:
                        chunk = f"{len(chunk):X}\r\n".encode('ascii') + chunk + b'\r\n'
                self.send(chunk)
        else:
            if encode_chunked:
                if self._http_vsn == 11:
                    self.send(b'0\r\n\r\n')

    def putrequest(self, method, url, skip_host=False, skip_accept_encoding=False):
        """Send a request to the server.

        `method' specifies an HTTP request method, e.g. 'GET'.
        `url' specifies the object being requested, e.g. '/index.html'.
        `skip_host' if True does not add automatically a 'Host:' header
        `skip_accept_encoding' if True does not add automatically an
           'Accept-Encoding:' header
        """
        if self._HTTPConnection__response:
            if self._HTTPConnection__response.isclosed():
                self._HTTPConnection__response = None
        if self._HTTPConnection__state == _CS_IDLE:
            self._HTTPConnection__state = _CS_REQ_STARTED
        else:
            raise CannotSendRequest(self._HTTPConnection__state)
        self._validate_method(method)
        self._method = method
        url = url or '/'
        self._validate_path(url)
        request = '%s %s %s' % (method, url, self._http_vsn_str)
        self._output(self._encode_request(request))
        if self._http_vsn == 11:
            if not skip_host:
                netloc = ''
                if url.startswith('http'):
                    nil, netloc, nil, nil, nil = urlsplit(url)
                if netloc:
                    try:
                        netloc_enc = netloc.encode('ascii')
                    except UnicodeEncodeError:
                        netloc_enc = netloc.encode('idna')
                    else:
                        self.putheader('Host', netloc_enc)
        else:
            pass
        if self._tunnel_host:
            host = self._tunnel_host
            port = self._tunnel_port
        else:
            host = self.host
            port = self.port
        try:
            host_enc = host.encode('ascii')
        except UnicodeEncodeError:
            host_enc = host.encode('idna')
        else:
            if host.find(':') >= 0:
                host_enc = b'[' + host_enc + b']'
            if port == self.default_port:
                self.putheader('Host', host_enc)
            else:
                host_enc = host_enc.decode('ascii')
                self.putheader('Host', '%s:%s' % (host_enc, port))
        if not skip_accept_encoding:
            self.putheader('Accept-Encoding', 'identity')
        else:
            pass

    def _encode_request(self, request):
        return request.encode('ascii')

    def _validate_method(self, method):
        """Validate a method name for putrequest."""
        match = _contains_disallowed_method_pchar_re.search(method)
        if match:
            raise ValueError(f"method can't contain control characters. {method!r} (found at least {match.group()!r})")

    def _validate_path(self, url):
        """Validate a url for putrequest."""
        match = _contains_disallowed_url_pchar_re.search(url)
        if match:
            raise InvalidURL(f"URL can't contain control characters. {url!r} (found at least {match.group()!r})")

    def _validate_host(self, host):
        """Validate a host so it doesn't contain control characters."""
        match = _contains_disallowed_url_pchar_re.search(host)
        if match:
            raise InvalidURL(f"URL can't contain control characters. {host!r} (found at least {match.group()!r})")

    def putheader(self, header, *values):
        """Send a request header line to the server.

        For example: h.putheader('Accept', 'text/html')
        """
        if self._HTTPConnection__state != _CS_REQ_STARTED:
            raise CannotSendHeader()
        if hasattr(header, 'encode'):
            header = header.encode('ascii')
        if not _is_legal_header_name(header):
            raise ValueError('Invalid header name %r' % (header,))
        values = list(values)
        for i, one_value in enumerate(values):
            if hasattr(one_value, 'encode'):
                values[i] = one_value.encode('latin-1')
            elif isinstance(one_value, int):
                values[i] = str(one_value).encode('ascii')
            if _is_illegal_header_value(values[i]):
                raise ValueError('Invalid header value %r' % (values[i],))
        else:
            value = (b'\r\n\t').join(values)
            header = header + b': ' + value
            self._output(header)

    def endheaders(self, message_body=None, *, encode_chunked=False):
        """Indicate that the last header line has been sent to the server.

        This method sends the request to the server.  The optional message_body
        argument can be used to pass a message body associated with the
        request.
        """
        if self._HTTPConnection__state == _CS_REQ_STARTED:
            self._HTTPConnection__state = _CS_REQ_SENT
        else:
            raise CannotSendHeader()
        self._send_output(message_body, encode_chunked=encode_chunked)

    def request(self, method, url, body=None, headers={}, *, encode_chunked=False):
        """Send a complete request to the server."""
        self._send_request(method, url, body, headers, encode_chunked)

    def _send_request(self, method, url, body, headers, encode_chunked):
        header_names = frozenset((k.lower() for k in headers))
        skips = {}
        if 'host' in header_names:
            skips['skip_host'] = 1
        if 'accept-encoding' in header_names:
            skips['skip_accept_encoding'] = 1
        (self.putrequest)(method, url, **skips)
        if 'content-length' not in header_names:
            if 'transfer-encoding' not in header_names:
                encode_chunked = False
                content_length = self._get_content_length(body, method)
                if content_length is None:
                    if body is not None:
                        if self.debuglevel > 0:
                            print('Unable to determine size of %r' % body)
                        encode_chunked = True
                        self.putheader('Transfer-Encoding', 'chunked')
                else:
                    self.putheader('Content-Length', str(content_length))
        else:
            encode_chunked = False
        for hdr, value in headers.items():
            self.putheader(hdr, value)
        else:
            if isinstance(body, str):
                body = _encode(body, 'body')
            self.endheaders(body, encode_chunked=encode_chunked)

    def getresponse--- This code section failed: ---

 L.1315         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _HTTPConnection__response
                4  POP_JUMP_IF_FALSE    22  'to 22'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _HTTPConnection__response
               10  LOAD_METHOD              isclosed
               12  CALL_METHOD_0         0  ''
               14  POP_JUMP_IF_FALSE    22  'to 22'

 L.1316        16  LOAD_CONST               None
               18  LOAD_FAST                'self'
               20  STORE_ATTR               _HTTPConnection__response
             22_0  COME_FROM            14  '14'
             22_1  COME_FROM             4  '4'

 L.1333        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _HTTPConnection__state
               26  LOAD_GLOBAL              _CS_REQ_SENT
               28  COMPARE_OP               !=
               30  POP_JUMP_IF_TRUE     38  'to 38'
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                _HTTPConnection__response
               36  POP_JUMP_IF_FALSE    48  'to 48'
             38_0  COME_FROM            30  '30'

 L.1334        38  LOAD_GLOBAL              ResponseNotReady
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                _HTTPConnection__state
               44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            36  '36'

 L.1336        48  LOAD_FAST                'self'
               50  LOAD_ATTR                debuglevel
               52  LOAD_CONST               0
               54  COMPARE_OP               >
               56  POP_JUMP_IF_FALSE    82  'to 82'

 L.1337        58  LOAD_FAST                'self'
               60  LOAD_ATTR                response_class
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                sock
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                debuglevel

 L.1338        70  LOAD_FAST                'self'
               72  LOAD_ATTR                _method

 L.1337        74  LOAD_CONST               ('method',)
               76  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               78  STORE_FAST               'response'
               80  JUMP_FORWARD        100  'to 100'
             82_0  COME_FROM            56  '56'

 L.1340        82  LOAD_FAST                'self'
               84  LOAD_ATTR                response_class
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                sock
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                _method
               94  LOAD_CONST               ('method',)
               96  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               98  STORE_FAST               'response'
            100_0  COME_FROM            80  '80'

 L.1342       100  SETUP_FINALLY       194  'to 194'

 L.1343       102  SETUP_FINALLY       116  'to 116'

 L.1344       104  LOAD_FAST                'response'
              106  LOAD_METHOD              begin
              108  CALL_METHOD_0         0  ''
              110  POP_TOP          
              112  POP_BLOCK        
              114  JUMP_FORWARD        146  'to 146'
            116_0  COME_FROM_FINALLY   102  '102'

 L.1345       116  DUP_TOP          
              118  LOAD_GLOBAL              ConnectionError
              120  COMPARE_OP               exception-match
              122  POP_JUMP_IF_FALSE   144  'to 144'
              124  POP_TOP          
              126  POP_TOP          
              128  POP_TOP          

 L.1346       130  LOAD_FAST                'self'
              132  LOAD_METHOD              close
              134  CALL_METHOD_0         0  ''
              136  POP_TOP          

 L.1347       138  RAISE_VARARGS_0       0  'reraise'
              140  POP_EXCEPT       
              142  JUMP_FORWARD        146  'to 146'
            144_0  COME_FROM           122  '122'
              144  END_FINALLY      
            146_0  COME_FROM           142  '142'
            146_1  COME_FROM           114  '114'

 L.1348       146  LOAD_FAST                'response'
              148  LOAD_ATTR                will_close
              150  LOAD_GLOBAL              _UNKNOWN
              152  COMPARE_OP               !=
              154  POP_JUMP_IF_TRUE    160  'to 160'
              156  LOAD_ASSERT              AssertionError
              158  RAISE_VARARGS_1       1  'exception instance'
            160_0  COME_FROM           154  '154'

 L.1349       160  LOAD_GLOBAL              _CS_IDLE
              162  LOAD_FAST                'self'
              164  STORE_ATTR               _HTTPConnection__state

 L.1351       166  LOAD_FAST                'response'
              168  LOAD_ATTR                will_close
              170  POP_JUMP_IF_FALSE   182  'to 182'

 L.1353       172  LOAD_FAST                'self'
              174  LOAD_METHOD              close
              176  CALL_METHOD_0         0  ''
              178  POP_TOP          
              180  JUMP_FORWARD        188  'to 188'
            182_0  COME_FROM           170  '170'

 L.1356       182  LOAD_FAST                'response'
              184  LOAD_FAST                'self'
              186  STORE_ATTR               _HTTPConnection__response
            188_0  COME_FROM           180  '180'

 L.1358       188  LOAD_FAST                'response'
              190  POP_BLOCK        
              192  RETURN_VALUE     
            194_0  COME_FROM_FINALLY   100  '100'

 L.1359       194  POP_TOP          
              196  POP_TOP          
              198  POP_TOP          

 L.1360       200  LOAD_FAST                'response'
              202  LOAD_METHOD              close
              204  CALL_METHOD_0         0  ''
              206  POP_TOP          

 L.1361       208  RAISE_VARARGS_0       0  'reraise'
              210  POP_EXCEPT       
              212  JUMP_FORWARD        216  'to 216'
              214  END_FINALLY      
            216_0  COME_FROM           212  '212'

Parse error at or near `POP_TOP' instruction at offset 206


try:
    import ssl
except ImportError:
    pass
else:

    class HTTPSConnection(HTTPConnection):
        __doc__ = 'This class allows communication via SSL.'
        default_port = HTTPS_PORT

        def __init__(self, host, port=None, key_file=None, cert_file=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, source_address=None, *, context=None, check_hostname=None, blocksize=8192):
            super(HTTPSConnection, self).__init__(host, port, timeout, source_address,
              blocksize=blocksize)
            if key_file is not None or (cert_file is not None or check_hostname is not None):
                import warnings
                warnings.warn('key_file, cert_file and check_hostname are deprecated, use a custom context instead.', DeprecationWarning, 2)
            self.key_file = key_file
            self.cert_file = cert_file
            if context is None:
                context = ssl._create_default_https_context()
                if context.post_handshake_auth is not None:
                    context.post_handshake_auth = True
            will_verify = context.verify_mode != ssl.CERT_NONE
            if check_hostname is None:
                check_hostname = context.check_hostname
            if check_hostname:
                if not will_verify:
                    raise ValueError('check_hostname needs a SSL context with either CERT_OPTIONAL or CERT_REQUIRED')
                if key_file or (cert_file):
                    context.load_cert_chain(cert_file, key_file)
                    if context.post_handshake_auth is not None:
                        context.post_handshake_auth = True
                self._context = context
                if check_hostname is not None:
                    self._context.check_hostname = check_hostname

        def connect(self):
            super().connect()
            if self._tunnel_host:
                server_hostname = self._tunnel_host
            else:
                server_hostname = self.host
            self.sock = self._context.wrap_socket((self.sock), server_hostname=server_hostname)


    __all__.append('HTTPSConnection')

class HTTPException(Exception):
    pass


class NotConnected(HTTPException):
    pass


class InvalidURL(HTTPException):
    pass


class UnknownProtocol(HTTPException):

    def __init__(self, version):
        self.args = (
         version,)
        self.version = version


class UnknownTransferEncoding(HTTPException):
    pass


class UnimplementedFileMode(HTTPException):
    pass


class IncompleteRead(HTTPException):

    def __init__(self, partial, expected=None):
        self.args = (
         partial,)
        self.partial = partial
        self.expected = expected

    def __repr__(self):
        if self.expected is not None:
            e = ', %i more expected' % self.expected
        else:
            e = ''
        return '%s(%i bytes read%s)' % (self.__class__.__name__,
         len(self.partial), e)

    __str__ = object.__str__


class ImproperConnectionState(HTTPException):
    pass


class CannotSendRequest(ImproperConnectionState):
    pass


class CannotSendHeader(ImproperConnectionState):
    pass


class ResponseNotReady(ImproperConnectionState):
    pass


class BadStatusLine(HTTPException):

    def __init__(self, line):
        if not line:
            line = repr(line)
        self.args = (
         line,)
        self.line = line


class LineTooLong(HTTPException):

    def __init__(self, line_type):
        HTTPException.__init__(self, 'got more than %d bytes when reading %s' % (
         _MAXLINE, line_type))


class RemoteDisconnected(ConnectionResetError, BadStatusLine):

    def __init__(self, *pos, **kw):
        BadStatusLine.__init__(self, '')
        (ConnectionResetError.__init__)(self, *pos, **kw)


error = HTTPException