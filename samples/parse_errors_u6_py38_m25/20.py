# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: http\server.py
"""HTTP server classes.

Note: BaseHTTPRequestHandler doesn't implement any HTTP request; see
SimpleHTTPRequestHandler for simple implementations of GET, HEAD and POST,
and CGIHTTPRequestHandler for CGI scripts.

It does, however, optionally implement HTTP/1.1 persistent connections,
as of version 0.3.

Notes on CGIHTTPRequestHandler
------------------------------

This class implements GET and POST requests to cgi-bin scripts.

If the os.fork() function is not present (e.g. on Windows),
subprocess.Popen() is used as a fallback, with slightly altered semantics.

In all cases, the implementation is intentionally naive -- all
requests are executed synchronously.

SECURITY WARNING: DON'T USE THIS CODE UNLESS YOU ARE INSIDE A FIREWALL
-- it may execute arbitrary Python code or external programs.

Note that status code 200 is sent prior to execution of a CGI script, so
scripts cannot send other status codes such as 302 (redirect).

XXX To do:

- log requests even later (to capture byte count)
- log user-agent header and other interesting goodies
- send error log to separate file
"""
__version__ = '0.6'
__all__ = [
 'HTTPServer', 'ThreadingHTTPServer', 'BaseHTTPRequestHandler',
 'SimpleHTTPRequestHandler', 'CGIHTTPRequestHandler']
import copy, datetime, email.utils, html, http.client, io, mimetypes, os, posixpath, select, shutil, socket, socketserver, sys, time, urllib.parse, contextlib
from functools import partial
from http import HTTPStatus
DEFAULT_ERROR_MESSAGE = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"\n        "http://www.w3.org/TR/html4/strict.dtd">\n<html>\n    <head>\n        <meta http-equiv="Content-Type" content="text/html;charset=utf-8">\n        <title>Error response</title>\n    </head>\n    <body>\n        <h1>Error response</h1>\n        <p>Error code: %(code)d</p>\n        <p>Message: %(message)s.</p>\n        <p>Error code explanation: %(code)s - %(explain)s.</p>\n    </body>\n</html>\n'
DEFAULT_ERROR_CONTENT_TYPE = 'text/html;charset=utf-8'

class HTTPServer(socketserver.TCPServer):
    allow_reuse_address = 1

    def server_bind(self):
        """Override server_bind to store the server name."""
        socketserver.TCPServer.server_bind(self)
        host, port = self.server_address[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port


class ThreadingHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    daemon_threads = True


class BaseHTTPRequestHandler(socketserver.StreamRequestHandler):
    __doc__ = 'HTTP request handler base class.\n\n    The following explanation of HTTP serves to guide you through the\n    code as well as to expose any misunderstandings I may have about\n    HTTP (so you don\'t need to read the code to figure out I\'m wrong\n    :-).\n\n    HTTP (HyperText Transfer Protocol) is an extensible protocol on\n    top of a reliable stream transport (e.g. TCP/IP).  The protocol\n    recognizes three parts to a request:\n\n    1. One line identifying the request type and path\n    2. An optional set of RFC-822-style headers\n    3. An optional data part\n\n    The headers and data are separated by a blank line.\n\n    The first line of the request has the form\n\n    <command> <path> <version>\n\n    where <command> is a (case-sensitive) keyword such as GET or POST,\n    <path> is a string containing path information for the request,\n    and <version> should be the string "HTTP/1.0" or "HTTP/1.1".\n    <path> is encoded using the URL encoding scheme (using %xx to signify\n    the ASCII character with hex code xx).\n\n    The specification specifies that lines are separated by CRLF but\n    for compatibility with the widest range of clients recommends\n    servers also handle LF.  Similarly, whitespace in the request line\n    is treated sensibly (allowing multiple spaces between components\n    and allowing trailing whitespace).\n\n    Similarly, for output, lines ought to be separated by CRLF pairs\n    but most clients grok LF characters just fine.\n\n    If the first line of the request has the form\n\n    <command> <path>\n\n    (i.e. <version> is left out) then this is assumed to be an HTTP\n    0.9 request; this form has no optional headers and data part and\n    the reply consists of just the data.\n\n    The reply form of the HTTP 1.x protocol again has three parts:\n\n    1. One line giving the response code\n    2. An optional set of RFC-822-style headers\n    3. The data\n\n    Again, the headers and data are separated by a blank line.\n\n    The response code line has the form\n\n    <version> <responsecode> <responsestring>\n\n    where <version> is the protocol version ("HTTP/1.0" or "HTTP/1.1"),\n    <responsecode> is a 3-digit response code indicating success or\n    failure of the request, and <responsestring> is an optional\n    human-readable string explaining what the response code means.\n\n    This server parses the request and the headers, and then calls a\n    function specific to the request type (<command>).  Specifically,\n    a request SPAM will be handled by a method do_SPAM().  If no\n    such method exists the server sends an error response to the\n    client.  If it exists, it is called with no arguments:\n\n    do_SPAM()\n\n    Note that the request name is case sensitive (i.e. SPAM and spam\n    are different requests).\n\n    The various request details are stored in instance variables:\n\n    - client_address is the client IP address in the form (host,\n    port);\n\n    - command, path and version are the broken-down request line;\n\n    - headers is an instance of email.message.Message (or a derived\n    class) containing the header information;\n\n    - rfile is a file object open for reading positioned at the\n    start of the optional input data part;\n\n    - wfile is a file object open for writing.\n\n    IT IS IMPORTANT TO ADHERE TO THE PROTOCOL FOR WRITING!\n\n    The first thing to be written must be the response line.  Then\n    follow 0 or more header lines, then a blank line, and then the\n    actual data (if any).  The meaning of the header lines depends on\n    the command executed by the server; in most cases, when data is\n    returned, there should be at least one header line of the form\n\n    Content-type: <type>/<subtype>\n\n    where <type> and <subtype> should be registered MIME types,\n    e.g. "text/html" or "text/plain".\n\n    '
    sys_version = 'Python/' + sys.version.split()[0]
    server_version = 'BaseHTTP/' + __version__
    error_message_format = DEFAULT_ERROR_MESSAGE
    error_content_type = DEFAULT_ERROR_CONTENT_TYPE
    default_request_version = 'HTTP/0.9'

    def parse_request--- This code section failed: ---

 L. 280         0  LOAD_CONST               None
                2  LOAD_FAST                'self'
                4  STORE_ATTR               command

 L. 281         6  LOAD_FAST                'self'
                8  LOAD_ATTR                default_request_version
               10  DUP_TOP          
               12  LOAD_FAST                'self'
               14  STORE_ATTR               request_version
               16  STORE_FAST               'version'

 L. 282        18  LOAD_CONST               True
               20  LOAD_FAST                'self'
               22  STORE_ATTR               close_connection

 L. 283        24  LOAD_GLOBAL              str
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                raw_requestline
               30  LOAD_STR                 'iso-8859-1'
               32  CALL_FUNCTION_2       2  ''
               34  STORE_FAST               'requestline'

 L. 284        36  LOAD_FAST                'requestline'
               38  LOAD_METHOD              rstrip
               40  LOAD_STR                 '\r\n'
               42  CALL_METHOD_1         1  ''
               44  STORE_FAST               'requestline'

 L. 285        46  LOAD_FAST                'requestline'
               48  LOAD_FAST                'self'
               50  STORE_ATTR               requestline

 L. 286        52  LOAD_FAST                'requestline'
               54  LOAD_METHOD              split
               56  CALL_METHOD_0         0  ''
               58  STORE_FAST               'words'

 L. 287        60  LOAD_GLOBAL              len
               62  LOAD_FAST                'words'
               64  CALL_FUNCTION_1       1  ''
               66  LOAD_CONST               0
               68  COMPARE_OP               ==
               70  POP_JUMP_IF_FALSE    76  'to 76'

 L. 288        72  LOAD_CONST               False
               74  RETURN_VALUE     
             76_0  COME_FROM            70  '70'

 L. 290        76  LOAD_GLOBAL              len
               78  LOAD_FAST                'words'
               80  CALL_FUNCTION_1       1  ''
               82  LOAD_CONST               3
               84  COMPARE_OP               >=
            86_88  POP_JUMP_IF_FALSE   294  'to 294'

 L. 291        90  LOAD_FAST                'words'
               92  LOAD_CONST               -1
               94  BINARY_SUBSCR    
               96  STORE_FAST               'version'

 L. 292        98  SETUP_FINALLY       184  'to 184'

 L. 293       100  LOAD_FAST                'version'
              102  LOAD_METHOD              startswith
              104  LOAD_STR                 'HTTP/'
              106  CALL_METHOD_1         1  ''
              108  POP_JUMP_IF_TRUE    114  'to 114'

 L. 294       110  LOAD_GLOBAL              ValueError
              112  RAISE_VARARGS_1       1  'exception instance'
            114_0  COME_FROM           108  '108'

 L. 295       114  LOAD_FAST                'version'
              116  LOAD_METHOD              split
              118  LOAD_STR                 '/'
              120  LOAD_CONST               1
              122  CALL_METHOD_2         2  ''
              124  LOAD_CONST               1
              126  BINARY_SUBSCR    
              128  STORE_FAST               'base_version_number'

 L. 296       130  LOAD_FAST                'base_version_number'
              132  LOAD_METHOD              split
              134  LOAD_STR                 '.'
              136  CALL_METHOD_1         1  ''
              138  STORE_FAST               'version_number'

 L. 303       140  LOAD_GLOBAL              len
              142  LOAD_FAST                'version_number'
              144  CALL_FUNCTION_1       1  ''
              146  LOAD_CONST               2
              148  COMPARE_OP               !=
              150  POP_JUMP_IF_FALSE   156  'to 156'

 L. 304       152  LOAD_GLOBAL              ValueError
              154  RAISE_VARARGS_1       1  'exception instance'
            156_0  COME_FROM           150  '150'

 L. 305       156  LOAD_GLOBAL              int
              158  LOAD_FAST                'version_number'
              160  LOAD_CONST               0
              162  BINARY_SUBSCR    
              164  CALL_FUNCTION_1       1  ''
              166  LOAD_GLOBAL              int
              168  LOAD_FAST                'version_number'
              170  LOAD_CONST               1
              172  BINARY_SUBSCR    
              174  CALL_FUNCTION_1       1  ''
              176  BUILD_TUPLE_2         2 
              178  STORE_FAST               'version_number'
              180  POP_BLOCK        
              182  JUMP_FORWARD        228  'to 228'
            184_0  COME_FROM_FINALLY    98  '98'

 L. 306       184  DUP_TOP          
              186  LOAD_GLOBAL              ValueError
              188  LOAD_GLOBAL              IndexError
              190  BUILD_TUPLE_2         2 
              192  COMPARE_OP               exception-match
              194  POP_JUMP_IF_FALSE   226  'to 226'
              196  POP_TOP          
              198  POP_TOP          
              200  POP_TOP          

 L. 307       202  LOAD_FAST                'self'
              204  LOAD_METHOD              send_error

 L. 308       206  LOAD_GLOBAL              HTTPStatus
              208  LOAD_ATTR                BAD_REQUEST

 L. 309       210  LOAD_STR                 'Bad request version (%r)'
              212  LOAD_FAST                'version'
              214  BINARY_MODULO    

 L. 307       216  CALL_METHOD_2         2  ''
              218  POP_TOP          

 L. 310       220  POP_EXCEPT       
              222  LOAD_CONST               False
              224  RETURN_VALUE     
            226_0  COME_FROM           194  '194'
              226  END_FINALLY      
            228_0  COME_FROM           182  '182'

 L. 311       228  LOAD_FAST                'version_number'
              230  LOAD_CONST               (1, 1)
              232  COMPARE_OP               >=
          234_236  POP_JUMP_IF_FALSE   256  'to 256'
              238  LOAD_FAST                'self'
              240  LOAD_ATTR                protocol_version
              242  LOAD_STR                 'HTTP/1.1'
              244  COMPARE_OP               >=
          246_248  POP_JUMP_IF_FALSE   256  'to 256'

 L. 312       250  LOAD_CONST               False
              252  LOAD_FAST                'self'
              254  STORE_ATTR               close_connection
            256_0  COME_FROM           246  '246'
            256_1  COME_FROM           234  '234'

 L. 313       256  LOAD_FAST                'version_number'
              258  LOAD_CONST               (2, 0)
              260  COMPARE_OP               >=
          262_264  POP_JUMP_IF_FALSE   288  'to 288'

 L. 314       266  LOAD_FAST                'self'
              268  LOAD_METHOD              send_error

 L. 315       270  LOAD_GLOBAL              HTTPStatus
              272  LOAD_ATTR                HTTP_VERSION_NOT_SUPPORTED

 L. 316       274  LOAD_STR                 'Invalid HTTP version (%s)'
              276  LOAD_FAST                'base_version_number'
              278  BINARY_MODULO    

 L. 314       280  CALL_METHOD_2         2  ''
              282  POP_TOP          

 L. 317       284  LOAD_CONST               False
              286  RETURN_VALUE     
            288_0  COME_FROM           262  '262'

 L. 318       288  LOAD_FAST                'version'
              290  LOAD_FAST                'self'
              292  STORE_ATTR               request_version
            294_0  COME_FROM            86  '86'

 L. 320       294  LOAD_CONST               2
              296  LOAD_GLOBAL              len
              298  LOAD_FAST                'words'
              300  CALL_FUNCTION_1       1  ''
              302  DUP_TOP          
              304  ROT_THREE        
              306  COMPARE_OP               <=
          308_310  POP_JUMP_IF_FALSE   322  'to 322'
              312  LOAD_CONST               3
              314  COMPARE_OP               <=
          316_318  POP_JUMP_IF_TRUE    346  'to 346'
              320  JUMP_FORWARD        324  'to 324'
            322_0  COME_FROM           308  '308'
              322  POP_TOP          
            324_0  COME_FROM           320  '320'

 L. 321       324  LOAD_FAST                'self'
              326  LOAD_METHOD              send_error

 L. 322       328  LOAD_GLOBAL              HTTPStatus
              330  LOAD_ATTR                BAD_REQUEST

 L. 323       332  LOAD_STR                 'Bad request syntax (%r)'
              334  LOAD_FAST                'requestline'
              336  BINARY_MODULO    

 L. 321       338  CALL_METHOD_2         2  ''
              340  POP_TOP          

 L. 324       342  LOAD_CONST               False
              344  RETURN_VALUE     
            346_0  COME_FROM           316  '316'

 L. 325       346  LOAD_FAST                'words'
              348  LOAD_CONST               None
              350  LOAD_CONST               2
              352  BUILD_SLICE_2         2 
              354  BINARY_SUBSCR    
              356  UNPACK_SEQUENCE_2     2 
              358  STORE_FAST               'command'
              360  STORE_FAST               'path'

 L. 326       362  LOAD_GLOBAL              len
              364  LOAD_FAST                'words'
              366  CALL_FUNCTION_1       1  ''
              368  LOAD_CONST               2
              370  COMPARE_OP               ==
          372_374  POP_JUMP_IF_FALSE   414  'to 414'

 L. 327       376  LOAD_CONST               True
              378  LOAD_FAST                'self'
              380  STORE_ATTR               close_connection

 L. 328       382  LOAD_FAST                'command'
              384  LOAD_STR                 'GET'
              386  COMPARE_OP               !=
          388_390  POP_JUMP_IF_FALSE   414  'to 414'

 L. 329       392  LOAD_FAST                'self'
              394  LOAD_METHOD              send_error

 L. 330       396  LOAD_GLOBAL              HTTPStatus
              398  LOAD_ATTR                BAD_REQUEST

 L. 331       400  LOAD_STR                 'Bad HTTP/0.9 request type (%r)'
              402  LOAD_FAST                'command'
              404  BINARY_MODULO    

 L. 329       406  CALL_METHOD_2         2  ''
              408  POP_TOP          

 L. 332       410  LOAD_CONST               False
              412  RETURN_VALUE     
            414_0  COME_FROM           388  '388'
            414_1  COME_FROM           372  '372'

 L. 333       414  LOAD_FAST                'command'
              416  LOAD_FAST                'path'
              418  ROT_TWO          
              420  LOAD_FAST                'self'
              422  STORE_ATTR               command
              424  LOAD_FAST                'self'
              426  STORE_ATTR               path

 L. 336       428  SETUP_FINALLY       456  'to 456'

 L. 337       430  LOAD_GLOBAL              http
              432  LOAD_ATTR                client
              434  LOAD_ATTR                parse_headers
              436  LOAD_FAST                'self'
              438  LOAD_ATTR                rfile

 L. 338       440  LOAD_FAST                'self'
              442  LOAD_ATTR                MessageClass

 L. 337       444  LOAD_CONST               ('_class',)
              446  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              448  LOAD_FAST                'self'
              450  STORE_ATTR               headers
              452  POP_BLOCK        
              454  JUMP_FORWARD        586  'to 586'
            456_0  COME_FROM_FINALLY   428  '428'

 L. 339       456  DUP_TOP          
              458  LOAD_GLOBAL              http
              460  LOAD_ATTR                client
              462  LOAD_ATTR                LineTooLong
              464  COMPARE_OP               exception-match
          466_468  POP_JUMP_IF_FALSE   520  'to 520'
              470  POP_TOP          
              472  STORE_FAST               'err'
              474  POP_TOP          
              476  SETUP_FINALLY       508  'to 508'

 L. 340       478  LOAD_FAST                'self'
              480  LOAD_METHOD              send_error

 L. 341       482  LOAD_GLOBAL              HTTPStatus
              484  LOAD_ATTR                REQUEST_HEADER_FIELDS_TOO_LARGE

 L. 342       486  LOAD_STR                 'Line too long'

 L. 343       488  LOAD_GLOBAL              str
              490  LOAD_FAST                'err'
              492  CALL_FUNCTION_1       1  ''

 L. 340       494  CALL_METHOD_3         3  ''
              496  POP_TOP          

 L. 344       498  POP_BLOCK        
              500  POP_EXCEPT       
              502  CALL_FINALLY        508  'to 508'
              504  LOAD_CONST               False
              506  RETURN_VALUE     
            508_0  COME_FROM           502  '502'
            508_1  COME_FROM_FINALLY   476  '476'
              508  LOAD_CONST               None
              510  STORE_FAST               'err'
              512  DELETE_FAST              'err'
              514  END_FINALLY      
              516  POP_EXCEPT       
              518  JUMP_FORWARD        586  'to 586'
            520_0  COME_FROM           466  '466'

 L. 345       520  DUP_TOP          
              522  LOAD_GLOBAL              http
              524  LOAD_ATTR                client
              526  LOAD_ATTR                HTTPException
              528  COMPARE_OP               exception-match
          530_532  POP_JUMP_IF_FALSE   584  'to 584'
              534  POP_TOP          
              536  STORE_FAST               'err'
              538  POP_TOP          
              540  SETUP_FINALLY       572  'to 572'

 L. 346       542  LOAD_FAST                'self'
              544  LOAD_METHOD              send_error

 L. 347       546  LOAD_GLOBAL              HTTPStatus
              548  LOAD_ATTR                REQUEST_HEADER_FIELDS_TOO_LARGE

 L. 348       550  LOAD_STR                 'Too many headers'

 L. 349       552  LOAD_GLOBAL              str
              554  LOAD_FAST                'err'
              556  CALL_FUNCTION_1       1  ''

 L. 346       558  CALL_METHOD_3         3  ''
              560  POP_TOP          

 L. 351       562  POP_BLOCK        
              564  POP_EXCEPT       
              566  CALL_FINALLY        572  'to 572'
              568  LOAD_CONST               False
              570  RETURN_VALUE     
            572_0  COME_FROM           566  '566'
            572_1  COME_FROM_FINALLY   540  '540'
              572  LOAD_CONST               None
              574  STORE_FAST               'err'
              576  DELETE_FAST              'err'
              578  END_FINALLY      
              580  POP_EXCEPT       
              582  JUMP_FORWARD        586  'to 586'
            584_0  COME_FROM           530  '530'
              584  END_FINALLY      
            586_0  COME_FROM           582  '582'
            586_1  COME_FROM           518  '518'
            586_2  COME_FROM           454  '454'

 L. 353       586  LOAD_FAST                'self'
              588  LOAD_ATTR                headers
              590  LOAD_METHOD              get
              592  LOAD_STR                 'Connection'
              594  LOAD_STR                 ''
              596  CALL_METHOD_2         2  ''
              598  STORE_FAST               'conntype'

 L. 354       600  LOAD_FAST                'conntype'
              602  LOAD_METHOD              lower
              604  CALL_METHOD_0         0  ''
              606  LOAD_STR                 'close'
              608  COMPARE_OP               ==
          610_612  POP_JUMP_IF_FALSE   622  'to 622'

 L. 355       614  LOAD_CONST               True
              616  LOAD_FAST                'self'
              618  STORE_ATTR               close_connection
              620  JUMP_FORWARD        654  'to 654'
            622_0  COME_FROM           610  '610'

 L. 356       622  LOAD_FAST                'conntype'
              624  LOAD_METHOD              lower
              626  CALL_METHOD_0         0  ''
              628  LOAD_STR                 'keep-alive'
              630  COMPARE_OP               ==
          632_634  POP_JUMP_IF_FALSE   654  'to 654'

 L. 357       636  LOAD_FAST                'self'
              638  LOAD_ATTR                protocol_version
              640  LOAD_STR                 'HTTP/1.1'
              642  COMPARE_OP               >=

 L. 356   644_646  POP_JUMP_IF_FALSE   654  'to 654'

 L. 358       648  LOAD_CONST               False
              650  LOAD_FAST                'self'
              652  STORE_ATTR               close_connection
            654_0  COME_FROM           644  '644'
            654_1  COME_FROM           632  '632'
            654_2  COME_FROM           620  '620'

 L. 360       654  LOAD_FAST                'self'
              656  LOAD_ATTR                headers
              658  LOAD_METHOD              get
              660  LOAD_STR                 'Expect'
              662  LOAD_STR                 ''
              664  CALL_METHOD_2         2  ''
              666  STORE_FAST               'expect'

 L. 361       668  LOAD_FAST                'expect'
              670  LOAD_METHOD              lower
              672  CALL_METHOD_0         0  ''
              674  LOAD_STR                 '100-continue'
              676  COMPARE_OP               ==
          678_680  POP_JUMP_IF_FALSE   720  'to 720'

 L. 362       682  LOAD_FAST                'self'
              684  LOAD_ATTR                protocol_version
              686  LOAD_STR                 'HTTP/1.1'
              688  COMPARE_OP               >=

 L. 361   690_692  POP_JUMP_IF_FALSE   720  'to 720'

 L. 363       694  LOAD_FAST                'self'
              696  LOAD_ATTR                request_version
              698  LOAD_STR                 'HTTP/1.1'
              700  COMPARE_OP               >=

 L. 361   702_704  POP_JUMP_IF_FALSE   720  'to 720'

 L. 364       706  LOAD_FAST                'self'
              708  LOAD_METHOD              handle_expect_100
              710  CALL_METHOD_0         0  ''
          712_714  POP_JUMP_IF_TRUE    720  'to 720'

 L. 365       716  LOAD_CONST               False
              718  RETURN_VALUE     
            720_0  COME_FROM           712  '712'
            720_1  COME_FROM           702  '702'
            720_2  COME_FROM           690  '690'
            720_3  COME_FROM           678  '678'

 L. 366       720  LOAD_CONST               True
              722  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 222

    def handle_expect_100(self):
        """Decide what to do with an "Expect: 100-continue" header.

        If the client is expecting a 100 Continue response, we must
        respond with either a 100 Continue or a final response before
        waiting for the request body. The default is to always respond
        with a 100 Continue. You can behave differently (for example,
        reject unauthorized requests) by overriding this method.

        This method should either return True (possibly after sending
        a 100 Continue response) or send an error response and return
        False.

        """
        self.send_response_only(HTTPStatus.CONTINUE)
        self.end_headers()
        return True

    def handle_one_request--- This code section failed: ---

 L. 394         0  SETUP_FINALLY       174  'to 174'

 L. 395         2  LOAD_FAST                'self'
                4  LOAD_ATTR                rfile
                6  LOAD_METHOD              readline
                8  LOAD_CONST               65537
               10  CALL_METHOD_1         1  ''
               12  LOAD_FAST                'self'
               14  STORE_ATTR               raw_requestline

 L. 396        16  LOAD_GLOBAL              len
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                raw_requestline
               22  CALL_FUNCTION_1       1  ''
               24  LOAD_CONST               65536
               26  COMPARE_OP               >
               28  POP_JUMP_IF_FALSE    66  'to 66'

 L. 397        30  LOAD_STR                 ''
               32  LOAD_FAST                'self'
               34  STORE_ATTR               requestline

 L. 398        36  LOAD_STR                 ''
               38  LOAD_FAST                'self'
               40  STORE_ATTR               request_version

 L. 399        42  LOAD_STR                 ''
               44  LOAD_FAST                'self'
               46  STORE_ATTR               command

 L. 400        48  LOAD_FAST                'self'
               50  LOAD_METHOD              send_error
               52  LOAD_GLOBAL              HTTPStatus
               54  LOAD_ATTR                REQUEST_URI_TOO_LONG
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          

 L. 401        60  POP_BLOCK        
               62  LOAD_CONST               None
               64  RETURN_VALUE     
             66_0  COME_FROM            28  '28'

 L. 402        66  LOAD_FAST                'self'
               68  LOAD_ATTR                raw_requestline
               70  POP_JUMP_IF_TRUE     84  'to 84'

 L. 403        72  LOAD_CONST               True
               74  LOAD_FAST                'self'
               76  STORE_ATTR               close_connection

 L. 404        78  POP_BLOCK        
               80  LOAD_CONST               None
               82  RETURN_VALUE     
             84_0  COME_FROM            70  '70'

 L. 405        84  LOAD_FAST                'self'
               86  LOAD_METHOD              parse_request
               88  CALL_METHOD_0         0  ''
               90  POP_JUMP_IF_TRUE     98  'to 98'

 L. 407        92  POP_BLOCK        
               94  LOAD_CONST               None
               96  RETURN_VALUE     
             98_0  COME_FROM            90  '90'

 L. 408        98  LOAD_STR                 'do_'
              100  LOAD_FAST                'self'
              102  LOAD_ATTR                command
              104  BINARY_ADD       
              106  STORE_FAST               'mname'

 L. 409       108  LOAD_GLOBAL              hasattr
              110  LOAD_FAST                'self'
              112  LOAD_FAST                'mname'
              114  CALL_FUNCTION_2       2  ''
              116  POP_JUMP_IF_TRUE    144  'to 144'

 L. 410       118  LOAD_FAST                'self'
              120  LOAD_METHOD              send_error

 L. 411       122  LOAD_GLOBAL              HTTPStatus
              124  LOAD_ATTR                NOT_IMPLEMENTED

 L. 412       126  LOAD_STR                 'Unsupported method (%r)'
              128  LOAD_FAST                'self'
              130  LOAD_ATTR                command
              132  BINARY_MODULO    

 L. 410       134  CALL_METHOD_2         2  ''
              136  POP_TOP          

 L. 413       138  POP_BLOCK        
              140  LOAD_CONST               None
              142  RETURN_VALUE     
            144_0  COME_FROM           116  '116'

 L. 414       144  LOAD_GLOBAL              getattr
              146  LOAD_FAST                'self'
              148  LOAD_FAST                'mname'
              150  CALL_FUNCTION_2       2  ''
              152  STORE_FAST               'method'

 L. 415       154  LOAD_FAST                'method'
              156  CALL_FUNCTION_0       0  ''
              158  POP_TOP          

 L. 416       160  LOAD_FAST                'self'
              162  LOAD_ATTR                wfile
              164  LOAD_METHOD              flush
              166  CALL_METHOD_0         0  ''
              168  POP_TOP          
              170  POP_BLOCK        
              172  JUMP_FORWARD        234  'to 234'
            174_0  COME_FROM_FINALLY     0  '0'

 L. 417       174  DUP_TOP          
              176  LOAD_GLOBAL              socket
              178  LOAD_ATTR                timeout
              180  COMPARE_OP               exception-match
              182  POP_JUMP_IF_FALSE   232  'to 232'
              184  POP_TOP          
              186  STORE_FAST               'e'
              188  POP_TOP          
              190  SETUP_FINALLY       220  'to 220'

 L. 419       192  LOAD_FAST                'self'
              194  LOAD_METHOD              log_error
              196  LOAD_STR                 'Request timed out: %r'
              198  LOAD_FAST                'e'
              200  CALL_METHOD_2         2  ''
              202  POP_TOP          

 L. 420       204  LOAD_CONST               True
              206  LOAD_FAST                'self'
              208  STORE_ATTR               close_connection

 L. 421       210  POP_BLOCK        
              212  POP_EXCEPT       
              214  CALL_FINALLY        220  'to 220'
              216  LOAD_CONST               None
              218  RETURN_VALUE     
            220_0  COME_FROM           214  '214'
            220_1  COME_FROM_FINALLY   190  '190'
              220  LOAD_CONST               None
              222  STORE_FAST               'e'
              224  DELETE_FAST              'e'
              226  END_FINALLY      
              228  POP_EXCEPT       
              230  JUMP_FORWARD        234  'to 234'
            232_0  COME_FROM           182  '182'
              232  END_FINALLY      
            234_0  COME_FROM           230  '230'
            234_1  COME_FROM           172  '172'

Parse error at or near `LOAD_CONST' instruction at offset 62

    def handle(self):
        """Handle multiple requests if necessary."""
        self.close_connection = True
        self.handle_one_request()
        while not self.close_connection:
            self.handle_one_request()

    def send_error(self, code, message=None, explain=None):
        """Send and log an error reply.

        Arguments are
        * code:    an HTTP error code
                   3 digits
        * message: a simple optional 1 line reason phrase.
                   *( HTAB / SP / VCHAR / %x80-FF )
                   defaults to short entry matching the response code
        * explain: a detailed message defaults to the long entry
                   matching the response code.

        This sends an error response (so it must be called before any
        output has been generated), logs the error, and finally sends
        a piece of HTML explaining the error to the user.

        """
        try:
            shortmsg, longmsg = self.responses[code]
        except KeyError:
            shortmsg, longmsg = ('???', '???')
        else:
            if message is None:
                message = shortmsg
            else:
                if explain is None:
                    explain = longmsg
                self.log_error'code %d, message %s'codemessage
                self.send_responsecodemessage
                self.send_header'Connection''close'
                body = None
                if code >= 200 and code not in (HTTPStatus.NO_CONTENT,
                 HTTPStatus.RESET_CONTENT,
                 HTTPStatus.NOT_MODIFIED):
                    content = self.error_message_format % {'code':code, 
                     'message':html.escape(message, quote=False), 
                     'explain':html.escape(explain, quote=False)}
                    body = content.encode'UTF-8''replace'
                    self.send_header'Content-Type'self.error_content_type
                    self.send_header'Content-Length'str(len(body))
            self.end_headers()
            if self.command != 'HEAD':
                if body:
                    self.wfile.write(body)

    def send_response(self, code, message=None):
        """Add the response header to the headers buffer and log the
        response code.

        Also send two standard headers with the server software
        version and the current date.

        """
        self.log_request(code)
        self.send_response_onlycodemessage
        self.send_header'Server'self.version_string()
        self.send_header'Date'self.date_time_string()

    def send_response_only(self, code, message=None):
        """Send the response header only."""
        if self.request_version != 'HTTP/0.9':
            if message is None:
                if code in self.responses:
                    message = self.responses[code][0]
                else:
                    message = ''
            if not hasattrself'_headers_buffer':
                self._headers_buffer = []
            self._headers_buffer.append(('%s %d %s\r\n' % (
             self.protocol_version, code, message)).encode'latin-1''strict')

    def send_header(self, keyword, value):
        """Send a MIME header to the headers buffer."""
        if self.request_version != 'HTTP/0.9':
            if not hasattrself'_headers_buffer':
                self._headers_buffer = []
            self._headers_buffer.append(('%s: %s\r\n' % (keyword, value)).encode'latin-1''strict')
        elif keyword.lower() == 'connection':
            if value.lower() == 'close':
                self.close_connection = True
            else:
                if value.lower() == 'keep-alive':
                    self.close_connection = False

    def end_headers(self):
        """Send the blank line ending the MIME headers."""
        if self.request_version != 'HTTP/0.9':
            self._headers_buffer.append(b'\r\n')
            self.flush_headers()

    def flush_headers(self):
        if hasattrself'_headers_buffer':
            self.wfile.write((b'').join(self._headers_buffer))
            self._headers_buffer = []

    def log_request(self, code='-', size='-'):
        """Log an accepted request.

        This is called by send_response().

        """
        if isinstancecodeHTTPStatus:
            code = code.value
        self.log_message('"%s" %s %s', self.requestline, str(code), str(size))

    def log_error(self, format, *args):
        """Log an error.

        This is called when a request cannot be fulfilled.  By
        default it passes the message on to log_message().

        Arguments are the same as for log_message().

        XXX This should go to the separate error log.

        """
        (self.log_message)(format, *args)

    def log_message(self, format, *args):
        """Log an arbitrary message.

        This is used by all other logging functions.  Override
        it if you have specific logging wishes.

        The first argument, FORMAT, is a format string for the
        message to be logged.  If the format string contains
        any % escapes requiring parameters, they should be
        specified as subsequent arguments (it's just like
        printf!).

        The client ip and current date/time are prefixed to
        every message.

        """
        sys.stderr.write('%s - - [%s] %s\n' % (
         self.address_string(),
         self.log_date_time_string(),
         format % args))

    def version_string(self):
        """Return the server software version string."""
        return self.server_version + ' ' + self.sys_version

    def date_time_string(self, timestamp=None):
        """Return the current date and time formatted for a message header."""
        if timestamp is None:
            timestamp = time.time()
        return email.utils.formatdate(timestamp, usegmt=True)

    def log_date_time_string(self):
        """Return the current time formatted for logging."""
        now = time.time()
        year, month, day, hh, mm, ss, x, y, z = time.localtime(now)
        s = '%02d/%3s/%04d %02d:%02d:%02d' % (
         day, self.monthname[month], year, hh, mm, ss)
        return s

    weekdayname = [
     'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    monthname = [
     None,
     'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    def address_string(self):
        """Return the client address."""
        return self.client_address[0]

    protocol_version = 'HTTP/1.0'
    MessageClass = http.client.HTTPMessage
    responses = {(
     v.phrase, v.description):v for v in HTTPStatus.__members__.values()}


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    __doc__ = 'Simple HTTP request handler with GET and HEAD commands.\n\n    This serves files from the current directory and any of its\n    subdirectories.  The MIME type for files is determined by\n    calling the .guess_type() method.\n\n    The GET and HEAD requests are identical except that the HEAD\n    request omits the actual contents of the file.\n\n    '
    server_version = 'SimpleHTTP/' + __version__

    def __init__(self, *args, directory=None, **kwargs):
        if directory is None:
            directory = os.getcwd()
        self.directory = directory
        (super.__init__)(*args, **kwargs)

    def do_GET(self):
        """Serve a GET request."""
        f = self.send_head()
        if f:
            try:
                self.copyfilefself.wfile
            finally:
                f.close()

    def do_HEAD(self):
        """Serve a HEAD request."""
        f = self.send_head()
        if f:
            f.close()

    def send_head--- This code section failed: ---

 L. 675         0  LOAD_FAST                'self'
                2  LOAD_METHOD              translate_path
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                path
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'path'

 L. 676        12  LOAD_CONST               None
               14  STORE_FAST               'f'

 L. 677        16  LOAD_GLOBAL              os
               18  LOAD_ATTR                path
               20  LOAD_METHOD              isdir
               22  LOAD_FAST                'path'
               24  CALL_METHOD_1         1  ''
               26  POP_JUMP_IF_FALSE   194  'to 194'

 L. 678        28  LOAD_GLOBAL              urllib
               30  LOAD_ATTR                parse
               32  LOAD_METHOD              urlsplit
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                path
               38  CALL_METHOD_1         1  ''
               40  STORE_FAST               'parts'

 L. 679        42  LOAD_FAST                'parts'
               44  LOAD_ATTR                path
               46  LOAD_METHOD              endswith
               48  LOAD_STR                 '/'
               50  CALL_METHOD_1         1  ''
               52  POP_JUMP_IF_TRUE    140  'to 140'

 L. 681        54  LOAD_FAST                'self'
               56  LOAD_METHOD              send_response
               58  LOAD_GLOBAL              HTTPStatus
               60  LOAD_ATTR                MOVED_PERMANENTLY
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          

 L. 682        66  LOAD_FAST                'parts'
               68  LOAD_CONST               0
               70  BINARY_SUBSCR    
               72  LOAD_FAST                'parts'
               74  LOAD_CONST               1
               76  BINARY_SUBSCR    
               78  LOAD_FAST                'parts'
               80  LOAD_CONST               2
               82  BINARY_SUBSCR    
               84  LOAD_STR                 '/'
               86  BINARY_ADD       

 L. 683        88  LOAD_FAST                'parts'
               90  LOAD_CONST               3
               92  BINARY_SUBSCR    

 L. 683        94  LOAD_FAST                'parts'
               96  LOAD_CONST               4
               98  BINARY_SUBSCR    

 L. 682       100  BUILD_TUPLE_5         5 
              102  STORE_FAST               'new_parts'

 L. 684       104  LOAD_GLOBAL              urllib
              106  LOAD_ATTR                parse
              108  LOAD_METHOD              urlunsplit
              110  LOAD_FAST                'new_parts'
              112  CALL_METHOD_1         1  ''
              114  STORE_FAST               'new_url'

 L. 685       116  LOAD_FAST                'self'
              118  LOAD_METHOD              send_header
              120  LOAD_STR                 'Location'
              122  LOAD_FAST                'new_url'
              124  CALL_METHOD_2         2  ''
              126  POP_TOP          

 L. 686       128  LOAD_FAST                'self'
              130  LOAD_METHOD              end_headers
              132  CALL_METHOD_0         0  ''
              134  POP_TOP          

 L. 687       136  LOAD_CONST               None
              138  RETURN_VALUE     
            140_0  COME_FROM            52  '52'

 L. 688       140  LOAD_CONST               ('index.html', 'index.htm')
              142  GET_ITER         
            144_0  COME_FROM           172  '172'
              144  FOR_ITER            184  'to 184'
              146  STORE_FAST               'index'

 L. 689       148  LOAD_GLOBAL              os
              150  LOAD_ATTR                path
              152  LOAD_METHOD              join
              154  LOAD_FAST                'path'
              156  LOAD_FAST                'index'
              158  CALL_METHOD_2         2  ''
              160  STORE_FAST               'index'

 L. 690       162  LOAD_GLOBAL              os
              164  LOAD_ATTR                path
              166  LOAD_METHOD              exists
              168  LOAD_FAST                'index'
              170  CALL_METHOD_1         1  ''
              172  POP_JUMP_IF_FALSE   144  'to 144'

 L. 691       174  LOAD_FAST                'index'
              176  STORE_FAST               'path'

 L. 692       178  POP_TOP          
              180  BREAK_LOOP          194  'to 194'
              182  JUMP_BACK           144  'to 144'

 L. 694       184  LOAD_FAST                'self'
              186  LOAD_METHOD              list_directory
              188  LOAD_FAST                'path'
              190  CALL_METHOD_1         1  ''
              192  RETURN_VALUE     
            194_0  COME_FROM            26  '26'

 L. 695       194  LOAD_FAST                'self'
              196  LOAD_METHOD              guess_type
              198  LOAD_FAST                'path'
              200  CALL_METHOD_1         1  ''
              202  STORE_FAST               'ctype'

 L. 701       204  LOAD_FAST                'path'
              206  LOAD_METHOD              endswith
              208  LOAD_STR                 '/'
              210  CALL_METHOD_1         1  ''
              212  POP_JUMP_IF_FALSE   232  'to 232'

 L. 702       214  LOAD_FAST                'self'
              216  LOAD_METHOD              send_error
              218  LOAD_GLOBAL              HTTPStatus
              220  LOAD_ATTR                NOT_FOUND
              222  LOAD_STR                 'File not found'
              224  CALL_METHOD_2         2  ''
              226  POP_TOP          

 L. 703       228  LOAD_CONST               None
              230  RETURN_VALUE     
            232_0  COME_FROM           212  '212'

 L. 704       232  SETUP_FINALLY       248  'to 248'

 L. 705       234  LOAD_GLOBAL              open
              236  LOAD_FAST                'path'
              238  LOAD_STR                 'rb'
              240  CALL_FUNCTION_2       2  ''
              242  STORE_FAST               'f'
              244  POP_BLOCK        
              246  JUMP_FORWARD        286  'to 286'
            248_0  COME_FROM_FINALLY   232  '232'

 L. 706       248  DUP_TOP          
              250  LOAD_GLOBAL              OSError
              252  COMPARE_OP               exception-match
          254_256  POP_JUMP_IF_FALSE   284  'to 284'
              258  POP_TOP          
              260  POP_TOP          
              262  POP_TOP          

 L. 707       264  LOAD_FAST                'self'
              266  LOAD_METHOD              send_error
              268  LOAD_GLOBAL              HTTPStatus
              270  LOAD_ATTR                NOT_FOUND
              272  LOAD_STR                 'File not found'
              274  CALL_METHOD_2         2  ''
              276  POP_TOP          

 L. 708       278  POP_EXCEPT       
              280  LOAD_CONST               None
              282  RETURN_VALUE     
            284_0  COME_FROM           254  '254'
              284  END_FINALLY      
            286_0  COME_FROM           246  '246'

 L. 710   286_288  SETUP_FINALLY       580  'to 580'

 L. 711       290  LOAD_GLOBAL              os
              292  LOAD_METHOD              fstat
              294  LOAD_FAST                'f'
              296  LOAD_METHOD              fileno
              298  CALL_METHOD_0         0  ''
              300  CALL_METHOD_1         1  ''
              302  STORE_FAST               'fs'

 L. 713       304  LOAD_STR                 'If-Modified-Since'
              306  LOAD_FAST                'self'
              308  LOAD_ATTR                headers
              310  COMPARE_OP               in
          312_314  POP_JUMP_IF_FALSE   502  'to 502'

 L. 714       316  LOAD_STR                 'If-None-Match'
              318  LOAD_FAST                'self'
              320  LOAD_ATTR                headers
              322  COMPARE_OP               not-in

 L. 713   324_326  POP_JUMP_IF_FALSE   502  'to 502'

 L. 716       328  SETUP_FINALLY       352  'to 352'

 L. 717       330  LOAD_GLOBAL              email
              332  LOAD_ATTR                utils
              334  LOAD_METHOD              parsedate_to_datetime

 L. 718       336  LOAD_FAST                'self'
              338  LOAD_ATTR                headers
              340  LOAD_STR                 'If-Modified-Since'
              342  BINARY_SUBSCR    

 L. 717       344  CALL_METHOD_1         1  ''
              346  STORE_FAST               'ims'
              348  POP_BLOCK        
              350  JUMP_FORWARD        382  'to 382'
            352_0  COME_FROM_FINALLY   328  '328'

 L. 719       352  DUP_TOP          
              354  LOAD_GLOBAL              TypeError
              356  LOAD_GLOBAL              IndexError
              358  LOAD_GLOBAL              OverflowError
              360  LOAD_GLOBAL              ValueError
              362  BUILD_TUPLE_4         4 
              364  COMPARE_OP               exception-match
          366_368  POP_JUMP_IF_FALSE   380  'to 380'
              370  POP_TOP          
              372  POP_TOP          
              374  POP_TOP          

 L. 721       376  POP_EXCEPT       
              378  JUMP_FORWARD        502  'to 502'
            380_0  COME_FROM           366  '366'
              380  END_FINALLY      
            382_0  COME_FROM           350  '350'

 L. 723       382  LOAD_FAST                'ims'
              384  LOAD_ATTR                tzinfo
              386  LOAD_CONST               None
              388  COMPARE_OP               is
          390_392  POP_JUMP_IF_FALSE   410  'to 410'

 L. 726       394  LOAD_FAST                'ims'
              396  LOAD_ATTR                replace
              398  LOAD_GLOBAL              datetime
              400  LOAD_ATTR                timezone
              402  LOAD_ATTR                utc
              404  LOAD_CONST               ('tzinfo',)
              406  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              408  STORE_FAST               'ims'
            410_0  COME_FROM           390  '390'

 L. 727       410  LOAD_FAST                'ims'
              412  LOAD_ATTR                tzinfo
              414  LOAD_GLOBAL              datetime
              416  LOAD_ATTR                timezone
              418  LOAD_ATTR                utc
              420  COMPARE_OP               is
          422_424  POP_JUMP_IF_FALSE   502  'to 502'

 L. 729       426  LOAD_GLOBAL              datetime
              428  LOAD_ATTR                datetime
              430  LOAD_METHOD              fromtimestamp

 L. 730       432  LOAD_FAST                'fs'
              434  LOAD_ATTR                st_mtime

 L. 730       436  LOAD_GLOBAL              datetime
              438  LOAD_ATTR                timezone
              440  LOAD_ATTR                utc

 L. 729       442  CALL_METHOD_2         2  ''
              444  STORE_FAST               'last_modif'

 L. 732       446  LOAD_FAST                'last_modif'
              448  LOAD_ATTR                replace
              450  LOAD_CONST               0
              452  LOAD_CONST               ('microsecond',)
              454  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              456  STORE_FAST               'last_modif'

 L. 734       458  LOAD_FAST                'last_modif'
              460  LOAD_FAST                'ims'
              462  COMPARE_OP               <=
          464_466  POP_JUMP_IF_FALSE   502  'to 502'

 L. 735       468  LOAD_FAST                'self'
              470  LOAD_METHOD              send_response
              472  LOAD_GLOBAL              HTTPStatus
              474  LOAD_ATTR                NOT_MODIFIED
              476  CALL_METHOD_1         1  ''
              478  POP_TOP          

 L. 736       480  LOAD_FAST                'self'
              482  LOAD_METHOD              end_headers
              484  CALL_METHOD_0         0  ''
              486  POP_TOP          

 L. 737       488  LOAD_FAST                'f'
              490  LOAD_METHOD              close
              492  CALL_METHOD_0         0  ''
              494  POP_TOP          

 L. 738       496  POP_BLOCK        
              498  LOAD_CONST               None
              500  RETURN_VALUE     
            502_0  COME_FROM           464  '464'
            502_1  COME_FROM           422  '422'
            502_2  COME_FROM           378  '378'
            502_3  COME_FROM           324  '324'
            502_4  COME_FROM           312  '312'

 L. 740       502  LOAD_FAST                'self'
              504  LOAD_METHOD              send_response
              506  LOAD_GLOBAL              HTTPStatus
              508  LOAD_ATTR                OK
              510  CALL_METHOD_1         1  ''
              512  POP_TOP          

 L. 741       514  LOAD_FAST                'self'
              516  LOAD_METHOD              send_header
              518  LOAD_STR                 'Content-type'
              520  LOAD_FAST                'ctype'
              522  CALL_METHOD_2         2  ''
              524  POP_TOP          

 L. 742       526  LOAD_FAST                'self'
              528  LOAD_METHOD              send_header
              530  LOAD_STR                 'Content-Length'
              532  LOAD_GLOBAL              str
              534  LOAD_FAST                'fs'
              536  LOAD_CONST               6
              538  BINARY_SUBSCR    
              540  CALL_FUNCTION_1       1  ''
              542  CALL_METHOD_2         2  ''
              544  POP_TOP          

 L. 743       546  LOAD_FAST                'self'
              548  LOAD_METHOD              send_header
              550  LOAD_STR                 'Last-Modified'

 L. 744       552  LOAD_FAST                'self'
              554  LOAD_METHOD              date_time_string
              556  LOAD_FAST                'fs'
              558  LOAD_ATTR                st_mtime
              560  CALL_METHOD_1         1  ''

 L. 743       562  CALL_METHOD_2         2  ''
              564  POP_TOP          

 L. 745       566  LOAD_FAST                'self'
              568  LOAD_METHOD              end_headers
              570  CALL_METHOD_0         0  ''
              572  POP_TOP          

 L. 746       574  LOAD_FAST                'f'
              576  POP_BLOCK        
              578  RETURN_VALUE     
            580_0  COME_FROM_FINALLY   286  '286'

 L. 747       580  POP_TOP          
              582  POP_TOP          
              584  POP_TOP          

 L. 748       586  LOAD_FAST                'f'
              588  LOAD_METHOD              close
              590  CALL_METHOD_0         0  ''
              592  POP_TOP          

 L. 749       594  RAISE_VARARGS_0       0  'reraise'
              596  POP_EXCEPT       
              598  JUMP_FORWARD        602  'to 602'
              600  END_FINALLY      
            602_0  COME_FROM           598  '598'

Parse error at or near `LOAD_CONST' instruction at offset 280

    def list_directory--- This code section failed: ---

 L. 759         0  SETUP_FINALLY        16  'to 16'

 L. 760         2  LOAD_GLOBAL              os
                4  LOAD_METHOD              listdir
                6  LOAD_FAST                'path'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'list'
               12  POP_BLOCK        
               14  JUMP_FORWARD         52  'to 52'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 761        16  DUP_TOP          
               18  LOAD_GLOBAL              OSError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    50  'to 50'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 762        30  LOAD_FAST                'self'
               32  LOAD_METHOD              send_error

 L. 763        34  LOAD_GLOBAL              HTTPStatus
               36  LOAD_ATTR                NOT_FOUND

 L. 764        38  LOAD_STR                 'No permission to list directory'

 L. 762        40  CALL_METHOD_2         2  ''
               42  POP_TOP          

 L. 765        44  POP_EXCEPT       
               46  LOAD_CONST               None
               48  RETURN_VALUE     
             50_0  COME_FROM            22  '22'
               50  END_FINALLY      
             52_0  COME_FROM            14  '14'

 L. 766        52  LOAD_FAST                'list'
               54  LOAD_ATTR                sort
               56  LOAD_LAMBDA              '<code_object <lambda>>'
               58  LOAD_STR                 'SimpleHTTPRequestHandler.list_directory.<locals>.<lambda>'
               60  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               62  LOAD_CONST               ('key',)
               64  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               66  POP_TOP          

 L. 767        68  BUILD_LIST_0          0 
               70  STORE_FAST               'r'

 L. 768        72  SETUP_FINALLY        96  'to 96'

 L. 769        74  LOAD_GLOBAL              urllib
               76  LOAD_ATTR                parse
               78  LOAD_ATTR                unquote
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                path

 L. 770        84  LOAD_STR                 'surrogatepass'

 L. 769        86  LOAD_CONST               ('errors',)
               88  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               90  STORE_FAST               'displaypath'
               92  POP_BLOCK        
               94  JUMP_FORWARD        128  'to 128'
             96_0  COME_FROM_FINALLY    72  '72'

 L. 771        96  DUP_TOP          
               98  LOAD_GLOBAL              UnicodeDecodeError
              100  COMPARE_OP               exception-match
              102  POP_JUMP_IF_FALSE   126  'to 126'
              104  POP_TOP          
              106  POP_TOP          
              108  POP_TOP          

 L. 772       110  LOAD_GLOBAL              urllib
              112  LOAD_ATTR                parse
              114  LOAD_METHOD              unquote
              116  LOAD_FAST                'path'
              118  CALL_METHOD_1         1  ''
              120  STORE_FAST               'displaypath'
              122  POP_EXCEPT       
              124  JUMP_FORWARD        128  'to 128'
            126_0  COME_FROM           102  '102'
              126  END_FINALLY      
            128_0  COME_FROM           124  '124'
            128_1  COME_FROM            94  '94'

 L. 773       128  LOAD_GLOBAL              html
              130  LOAD_ATTR                escape
              132  LOAD_FAST                'displaypath'
              134  LOAD_CONST               False
              136  LOAD_CONST               ('quote',)
              138  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              140  STORE_FAST               'displaypath'

 L. 774       142  LOAD_GLOBAL              sys
              144  LOAD_METHOD              getfilesystemencoding
              146  CALL_METHOD_0         0  ''
              148  STORE_FAST               'enc'

 L. 775       150  LOAD_STR                 'Directory listing for %s'
              152  LOAD_FAST                'displaypath'
              154  BINARY_MODULO    
              156  STORE_FAST               'title'

 L. 776       158  LOAD_FAST                'r'
              160  LOAD_METHOD              append
              162  LOAD_STR                 '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">'
              164  CALL_METHOD_1         1  ''
              166  POP_TOP          

 L. 778       168  LOAD_FAST                'r'
              170  LOAD_METHOD              append
              172  LOAD_STR                 '<html>\n<head>'
              174  CALL_METHOD_1         1  ''
              176  POP_TOP          

 L. 779       178  LOAD_FAST                'r'
              180  LOAD_METHOD              append
              182  LOAD_STR                 '<meta http-equiv="Content-Type" content="text/html; charset=%s">'

 L. 780       184  LOAD_FAST                'enc'

 L. 779       186  BINARY_MODULO    
              188  CALL_METHOD_1         1  ''
              190  POP_TOP          

 L. 781       192  LOAD_FAST                'r'
              194  LOAD_METHOD              append
              196  LOAD_STR                 '<title>%s</title>\n</head>'
              198  LOAD_FAST                'title'
              200  BINARY_MODULO    
              202  CALL_METHOD_1         1  ''
              204  POP_TOP          

 L. 782       206  LOAD_FAST                'r'
              208  LOAD_METHOD              append
              210  LOAD_STR                 '<body>\n<h1>%s</h1>'
              212  LOAD_FAST                'title'
              214  BINARY_MODULO    
              216  CALL_METHOD_1         1  ''
              218  POP_TOP          

 L. 783       220  LOAD_FAST                'r'
              222  LOAD_METHOD              append
              224  LOAD_STR                 '<hr>\n<ul>'
              226  CALL_METHOD_1         1  ''
              228  POP_TOP          

 L. 784       230  LOAD_FAST                'list'
              232  GET_ITER         
              234  FOR_ITER            354  'to 354'
              236  STORE_FAST               'name'

 L. 785       238  LOAD_GLOBAL              os
              240  LOAD_ATTR                path
              242  LOAD_METHOD              join
              244  LOAD_FAST                'path'
              246  LOAD_FAST                'name'
              248  CALL_METHOD_2         2  ''
              250  STORE_FAST               'fullname'

 L. 786       252  LOAD_FAST                'name'
              254  DUP_TOP          
              256  STORE_FAST               'displayname'
              258  STORE_FAST               'linkname'

 L. 788       260  LOAD_GLOBAL              os
              262  LOAD_ATTR                path
              264  LOAD_METHOD              isdir
              266  LOAD_FAST                'fullname'
              268  CALL_METHOD_1         1  ''
          270_272  POP_JUMP_IF_FALSE   290  'to 290'

 L. 789       274  LOAD_FAST                'name'
              276  LOAD_STR                 '/'
              278  BINARY_ADD       
              280  STORE_FAST               'displayname'

 L. 790       282  LOAD_FAST                'name'
              284  LOAD_STR                 '/'
              286  BINARY_ADD       
              288  STORE_FAST               'linkname'
            290_0  COME_FROM           270  '270'

 L. 791       290  LOAD_GLOBAL              os
              292  LOAD_ATTR                path
              294  LOAD_METHOD              islink
              296  LOAD_FAST                'fullname'
              298  CALL_METHOD_1         1  ''
          300_302  POP_JUMP_IF_FALSE   312  'to 312'

 L. 792       304  LOAD_FAST                'name'
              306  LOAD_STR                 '@'
              308  BINARY_ADD       
              310  STORE_FAST               'displayname'
            312_0  COME_FROM           300  '300'

 L. 794       312  LOAD_FAST                'r'
              314  LOAD_METHOD              append
              316  LOAD_STR                 '<li><a href="%s">%s</a></li>'

 L. 795       318  LOAD_GLOBAL              urllib
              320  LOAD_ATTR                parse
              322  LOAD_ATTR                quote
              324  LOAD_FAST                'linkname'

 L. 796       326  LOAD_STR                 'surrogatepass'

 L. 795       328  LOAD_CONST               ('errors',)
              330  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 797       332  LOAD_GLOBAL              html
              334  LOAD_ATTR                escape
              336  LOAD_FAST                'displayname'
              338  LOAD_CONST               False
              340  LOAD_CONST               ('quote',)
              342  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 795       344  BUILD_TUPLE_2         2 

 L. 794       346  BINARY_MODULO    
              348  CALL_METHOD_1         1  ''
              350  POP_TOP          
              352  JUMP_BACK           234  'to 234'

 L. 798       354  LOAD_FAST                'r'
              356  LOAD_METHOD              append
              358  LOAD_STR                 '</ul>\n<hr>\n</body>\n</html>\n'
              360  CALL_METHOD_1         1  ''
              362  POP_TOP          

 L. 799       364  LOAD_STR                 '\n'
              366  LOAD_METHOD              join
              368  LOAD_FAST                'r'
              370  CALL_METHOD_1         1  ''
              372  LOAD_METHOD              encode
              374  LOAD_FAST                'enc'
              376  LOAD_STR                 'surrogateescape'
              378  CALL_METHOD_2         2  ''
              380  STORE_FAST               'encoded'

 L. 800       382  LOAD_GLOBAL              io
              384  LOAD_METHOD              BytesIO
              386  CALL_METHOD_0         0  ''
              388  STORE_FAST               'f'

 L. 801       390  LOAD_FAST                'f'
              392  LOAD_METHOD              write
              394  LOAD_FAST                'encoded'
              396  CALL_METHOD_1         1  ''
              398  POP_TOP          

 L. 802       400  LOAD_FAST                'f'
              402  LOAD_METHOD              seek
              404  LOAD_CONST               0
              406  CALL_METHOD_1         1  ''
              408  POP_TOP          

 L. 803       410  LOAD_FAST                'self'
              412  LOAD_METHOD              send_response
              414  LOAD_GLOBAL              HTTPStatus
              416  LOAD_ATTR                OK
              418  CALL_METHOD_1         1  ''
              420  POP_TOP          

 L. 804       422  LOAD_FAST                'self'
              424  LOAD_METHOD              send_header
              426  LOAD_STR                 'Content-type'
              428  LOAD_STR                 'text/html; charset=%s'
              430  LOAD_FAST                'enc'
              432  BINARY_MODULO    
              434  CALL_METHOD_2         2  ''
              436  POP_TOP          

 L. 805       438  LOAD_FAST                'self'
              440  LOAD_METHOD              send_header
              442  LOAD_STR                 'Content-Length'
              444  LOAD_GLOBAL              str
              446  LOAD_GLOBAL              len
              448  LOAD_FAST                'encoded'
              450  CALL_FUNCTION_1       1  ''
              452  CALL_FUNCTION_1       1  ''
              454  CALL_METHOD_2         2  ''
              456  POP_TOP          

 L. 806       458  LOAD_FAST                'self'
              460  LOAD_METHOD              end_headers
              462  CALL_METHOD_0         0  ''
              464  POP_TOP          

 L. 807       466  LOAD_FAST                'f'
              468  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 46

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        path = path.split'?'1[0]
        path = path.split'#'1[0]
        trailing_slash = path.rstrip().endswith('/')
        try:
            path = urllib.parse.unquote(path, errors='surrogatepass')
        except UnicodeDecodeError:
            path = urllib.parse.unquote(path)
        else:
            path = posixpath.normpath(path)
            words = path.split('/')
            words = filterNonewords
            path = self.directory
            for word in words:
                if not os.path.dirname(word):
                    if word in (os.curdir, os.pardir):
                        pass
                    else:
                        path = os.path.joinpathword
                if trailing_slash:
                    path += '/'
                return path

    def copyfile(self, source, outputfile):
        """Copy all data between two file objects.

        The SOURCE argument is a file object open for reading
        (or anything with a read() method) and the DESTINATION
        argument is a file object open for writing (or
        anything with a write() method).

        The only reason for overriding this would be to change
        the block size or perhaps to replace newlines by CRLF
        -- note however that this the default server uses this
        to copy binary data as well.

        """
        shutil.copyfileobjsourceoutputfile

    def guess_type(self, path):
        """Guess the type of a file.

        Argument is a PATH (a filename).

        Return value is a string of the form type/subtype,
        usable for a MIME Content-type header.

        The default implementation looks the file's extension
        up in the table self.extensions_map, using application/octet-stream
        as a default; however it would be permissible (if
        slow) to look inside the data to make a better guess.

        """
        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        return self.extensions_map['']

    if not mimetypes.inited:
        mimetypes.init()
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({'':'application/octet-stream', 
     '.py':'text/plain', 
     '.c':'text/plain', 
     '.h':'text/plain'})


def _url_collapse_path(path):
    """
    Given a URL path, remove extra '/'s and '.' path elements and collapse
    any '..' references and returns a collapsed path.

    Implements something akin to RFC-2396 5.2 step 6 to parse relative paths.
    The utility of this function is limited to is_cgi method and helps
    preventing some security attacks.

    Returns: The reconstituted URL, which will always start with a '/'.

    Raises: IndexError if too many '..' occur within the path.

    """
    path, _, query = path.partition('?')
    path = urllib.parse.unquote(path)
    path_parts = path.split('/')
    head_parts = []
    for part in path_parts[:-1]:
        if part == '..':
            head_parts.pop()
        else:
            if part:
                if part != '.':
                    head_parts.append(part)
                if path_parts:
                    tail_part = path_parts.pop()
                    if tail_part:
                        if tail_part == '..':
                            head_parts.pop()
                            tail_part = ''
                        elif tail_part == '.':
                            tail_part = ''
                else:
                    tail_part = ''
                if query:
                    tail_part = '?'.join((tail_part, query))
            splitpath = (
             '/' + '/'.join(head_parts), tail_part)
            collapsed_path = '/'.join(splitpath)
            return collapsed_path


nobody = None

def nobody_uid():
    """Internal routine to get nobody's uid"""
    global nobody
    if nobody:
        return nobody
    try:
        import pwd
    except ImportError:
        return -1
    else:
        try:
            nobody = pwd.getpwnam('nobody')[2]
        except KeyError:
            nobody = 1 + max((x[2] for x in pwd.getpwall()))
        else:
            return nobody


def executable(path):
    """Test for executable file."""
    return os.accesspathos.X_OK


class CGIHTTPRequestHandler(SimpleHTTPRequestHandler):
    __doc__ = 'Complete HTTP server with GET, HEAD and POST commands.\n\n    GET and HEAD also support running CGI scripts.\n\n    The POST command is *only* implemented for CGI scripts.\n\n    '
    have_fork = hasattros'fork'
    rbufsize = 0

    def do_POST(self):
        """Serve a POST request.

        This is only implemented for CGI scripts.

        """
        if self.is_cgi():
            self.run_cgi()
        else:
            self.send_errorHTTPStatus.NOT_IMPLEMENTED'Can only POST to CGI scripts'

    def send_head(self):
        """Version of send_head that support CGI scripts"""
        if self.is_cgi():
            return self.run_cgi()
        return SimpleHTTPRequestHandler.send_head(self)

    def is_cgi(self):
        """Test whether self.path corresponds to a CGI script.

        Returns True and updates the cgi_info attribute to the tuple
        (dir, rest) if self.path requires running a CGI script.
        Returns False otherwise.

        If any exception is raised, the caller should assume that
        self.path was rejected as invalid and act accordingly.

        The default implementation tests whether the normalized url
        path begins with one of the strings in self.cgi_directories
        (and the next character is a '/' or the end of the string).

        """
        collapsed_path = _url_collapse_path(self.path)
        dir_sep = collapsed_path.find'/'1
        head, tail = collapsed_path[:dir_sep], collapsed_path[dir_sep + 1:]
        if head in self.cgi_directories:
            self.cgi_info = (
             head, tail)
            return True
        return False

    cgi_directories = [
     '/cgi-bin', '/htbin']

    def is_executable(self, path):
        """Test whether argument path is an executable file."""
        return executable(path)

    def is_python(self, path):
        """Test whether argument path is a Python script."""
        head, tail = os.path.splitext(path)
        return tail.lower() in ('.py', '.pyw')

    def run_cgi--- This code section failed: ---

 L.1038         0  LOAD_FAST                'self'
                2  LOAD_ATTR                cgi_info
                4  UNPACK_SEQUENCE_2     2 
                6  STORE_FAST               'dir'
                8  STORE_FAST               'rest'

 L.1039        10  LOAD_FAST                'dir'
               12  LOAD_STR                 '/'
               14  BINARY_ADD       
               16  LOAD_FAST                'rest'
               18  BINARY_ADD       
               20  STORE_FAST               'path'

 L.1040        22  LOAD_FAST                'path'
               24  LOAD_METHOD              find
               26  LOAD_STR                 '/'
               28  LOAD_GLOBAL              len
               30  LOAD_FAST                'dir'
               32  CALL_FUNCTION_1       1  ''
               34  LOAD_CONST               1
               36  BINARY_ADD       
               38  CALL_METHOD_2         2  ''
               40  STORE_FAST               'i'

 L.1041        42  LOAD_FAST                'i'
               44  LOAD_CONST               0
               46  COMPARE_OP               >=
               48  POP_JUMP_IF_FALSE   136  'to 136'

 L.1042        50  LOAD_FAST                'path'
               52  LOAD_CONST               None
               54  LOAD_FAST                'i'
               56  BUILD_SLICE_2         2 
               58  BINARY_SUBSCR    
               60  STORE_FAST               'nextdir'

 L.1043        62  LOAD_FAST                'path'
               64  LOAD_FAST                'i'
               66  LOAD_CONST               1
               68  BINARY_ADD       
               70  LOAD_CONST               None
               72  BUILD_SLICE_2         2 
               74  BINARY_SUBSCR    
               76  STORE_FAST               'nextrest'

 L.1045        78  LOAD_FAST                'self'
               80  LOAD_METHOD              translate_path
               82  LOAD_FAST                'nextdir'
               84  CALL_METHOD_1         1  ''
               86  STORE_FAST               'scriptdir'

 L.1046        88  LOAD_GLOBAL              os
               90  LOAD_ATTR                path
               92  LOAD_METHOD              isdir
               94  LOAD_FAST                'scriptdir'
               96  CALL_METHOD_1         1  ''
               98  POP_JUMP_IF_FALSE   136  'to 136'

 L.1047       100  LOAD_FAST                'nextdir'
              102  LOAD_FAST                'nextrest'
              104  ROT_TWO          
              106  STORE_FAST               'dir'
              108  STORE_FAST               'rest'

 L.1048       110  LOAD_FAST                'path'
              112  LOAD_METHOD              find
              114  LOAD_STR                 '/'
              116  LOAD_GLOBAL              len
              118  LOAD_FAST                'dir'
              120  CALL_FUNCTION_1       1  ''
              122  LOAD_CONST               1
              124  BINARY_ADD       
              126  CALL_METHOD_2         2  ''
              128  STORE_FAST               'i'
              130  JUMP_BACK            42  'to 42'

 L.1050       132  BREAK_LOOP          136  'to 136'
              134  JUMP_BACK            42  'to 42'
            136_0  COME_FROM            98  '98'
            136_1  COME_FROM            48  '48'

 L.1053       136  LOAD_FAST                'rest'
              138  LOAD_METHOD              partition
              140  LOAD_STR                 '?'
              142  CALL_METHOD_1         1  ''
              144  UNPACK_SEQUENCE_3     3 
              146  STORE_FAST               'rest'
              148  STORE_FAST               '_'
              150  STORE_FAST               'query'

 L.1057       152  LOAD_FAST                'rest'
              154  LOAD_METHOD              find
              156  LOAD_STR                 '/'
              158  CALL_METHOD_1         1  ''
              160  STORE_FAST               'i'

 L.1058       162  LOAD_FAST                'i'
              164  LOAD_CONST               0
              166  COMPARE_OP               >=
              168  POP_JUMP_IF_FALSE   198  'to 198'

 L.1059       170  LOAD_FAST                'rest'
              172  LOAD_CONST               None
              174  LOAD_FAST                'i'
              176  BUILD_SLICE_2         2 
              178  BINARY_SUBSCR    
              180  LOAD_FAST                'rest'
              182  LOAD_FAST                'i'
              184  LOAD_CONST               None
              186  BUILD_SLICE_2         2 
              188  BINARY_SUBSCR    
              190  ROT_TWO          
              192  STORE_FAST               'script'
              194  STORE_FAST               'rest'
              196  JUMP_FORWARD        208  'to 208'
            198_0  COME_FROM           168  '168'

 L.1061       198  LOAD_FAST                'rest'
              200  LOAD_STR                 ''
              202  ROT_TWO          
              204  STORE_FAST               'script'
              206  STORE_FAST               'rest'
            208_0  COME_FROM           196  '196'

 L.1063       208  LOAD_FAST                'dir'
              210  LOAD_STR                 '/'
              212  BINARY_ADD       
              214  LOAD_FAST                'script'
              216  BINARY_ADD       
              218  STORE_FAST               'scriptname'

 L.1064       220  LOAD_FAST                'self'
              222  LOAD_METHOD              translate_path
              224  LOAD_FAST                'scriptname'
              226  CALL_METHOD_1         1  ''
              228  STORE_FAST               'scriptfile'

 L.1065       230  LOAD_GLOBAL              os
              232  LOAD_ATTR                path
              234  LOAD_METHOD              exists
              236  LOAD_FAST                'scriptfile'
              238  CALL_METHOD_1         1  ''
          240_242  POP_JUMP_IF_TRUE    266  'to 266'

 L.1066       244  LOAD_FAST                'self'
              246  LOAD_METHOD              send_error

 L.1067       248  LOAD_GLOBAL              HTTPStatus
              250  LOAD_ATTR                NOT_FOUND

 L.1068       252  LOAD_STR                 'No such CGI script (%r)'
              254  LOAD_FAST                'scriptname'
              256  BINARY_MODULO    

 L.1066       258  CALL_METHOD_2         2  ''
              260  POP_TOP          

 L.1069       262  LOAD_CONST               None
              264  RETURN_VALUE     
            266_0  COME_FROM           240  '240'

 L.1070       266  LOAD_GLOBAL              os
              268  LOAD_ATTR                path
              270  LOAD_METHOD              isfile
              272  LOAD_FAST                'scriptfile'
              274  CALL_METHOD_1         1  ''
          276_278  POP_JUMP_IF_TRUE    302  'to 302'

 L.1071       280  LOAD_FAST                'self'
              282  LOAD_METHOD              send_error

 L.1072       284  LOAD_GLOBAL              HTTPStatus
              286  LOAD_ATTR                FORBIDDEN

 L.1073       288  LOAD_STR                 'CGI script is not a plain file (%r)'
              290  LOAD_FAST                'scriptname'
              292  BINARY_MODULO    

 L.1071       294  CALL_METHOD_2         2  ''
              296  POP_TOP          

 L.1074       298  LOAD_CONST               None
              300  RETURN_VALUE     
            302_0  COME_FROM           276  '276'

 L.1075       302  LOAD_FAST                'self'
              304  LOAD_METHOD              is_python
              306  LOAD_FAST                'scriptname'
              308  CALL_METHOD_1         1  ''
              310  STORE_FAST               'ispy'

 L.1076       312  LOAD_FAST                'self'
              314  LOAD_ATTR                have_fork
          316_318  POP_JUMP_IF_TRUE    326  'to 326'
              320  LOAD_FAST                'ispy'
          322_324  POP_JUMP_IF_TRUE    360  'to 360'
            326_0  COME_FROM           316  '316'

 L.1077       326  LOAD_FAST                'self'
              328  LOAD_METHOD              is_executable
              330  LOAD_FAST                'scriptfile'
              332  CALL_METHOD_1         1  ''
          334_336  POP_JUMP_IF_TRUE    360  'to 360'

 L.1078       338  LOAD_FAST                'self'
              340  LOAD_METHOD              send_error

 L.1079       342  LOAD_GLOBAL              HTTPStatus
              344  LOAD_ATTR                FORBIDDEN

 L.1080       346  LOAD_STR                 'CGI script is not executable (%r)'
              348  LOAD_FAST                'scriptname'
              350  BINARY_MODULO    

 L.1078       352  CALL_METHOD_2         2  ''
              354  POP_TOP          

 L.1081       356  LOAD_CONST               None
              358  RETURN_VALUE     
            360_0  COME_FROM           334  '334'
            360_1  COME_FROM           322  '322'

 L.1085       360  LOAD_GLOBAL              copy
              362  LOAD_METHOD              deepcopy
              364  LOAD_GLOBAL              os
              366  LOAD_ATTR                environ
              368  CALL_METHOD_1         1  ''
              370  STORE_FAST               'env'

 L.1086       372  LOAD_FAST                'self'
              374  LOAD_METHOD              version_string
              376  CALL_METHOD_0         0  ''
              378  LOAD_FAST                'env'
              380  LOAD_STR                 'SERVER_SOFTWARE'
              382  STORE_SUBSCR     

 L.1087       384  LOAD_FAST                'self'
              386  LOAD_ATTR                server
              388  LOAD_ATTR                server_name
              390  LOAD_FAST                'env'
              392  LOAD_STR                 'SERVER_NAME'
              394  STORE_SUBSCR     

 L.1088       396  LOAD_STR                 'CGI/1.1'
              398  LOAD_FAST                'env'
              400  LOAD_STR                 'GATEWAY_INTERFACE'
              402  STORE_SUBSCR     

 L.1089       404  LOAD_FAST                'self'
              406  LOAD_ATTR                protocol_version
              408  LOAD_FAST                'env'
              410  LOAD_STR                 'SERVER_PROTOCOL'
              412  STORE_SUBSCR     

 L.1090       414  LOAD_GLOBAL              str
              416  LOAD_FAST                'self'
              418  LOAD_ATTR                server
              420  LOAD_ATTR                server_port
              422  CALL_FUNCTION_1       1  ''
              424  LOAD_FAST                'env'
              426  LOAD_STR                 'SERVER_PORT'
              428  STORE_SUBSCR     

 L.1091       430  LOAD_FAST                'self'
              432  LOAD_ATTR                command
              434  LOAD_FAST                'env'
              436  LOAD_STR                 'REQUEST_METHOD'
              438  STORE_SUBSCR     

 L.1092       440  LOAD_GLOBAL              urllib
              442  LOAD_ATTR                parse
              444  LOAD_METHOD              unquote
              446  LOAD_FAST                'rest'
              448  CALL_METHOD_1         1  ''
              450  STORE_FAST               'uqrest'

 L.1093       452  LOAD_FAST                'uqrest'
              454  LOAD_FAST                'env'
              456  LOAD_STR                 'PATH_INFO'
              458  STORE_SUBSCR     

 L.1094       460  LOAD_FAST                'self'
              462  LOAD_METHOD              translate_path
              464  LOAD_FAST                'uqrest'
              466  CALL_METHOD_1         1  ''
              468  LOAD_FAST                'env'
              470  LOAD_STR                 'PATH_TRANSLATED'
              472  STORE_SUBSCR     

 L.1095       474  LOAD_FAST                'scriptname'
              476  LOAD_FAST                'env'
              478  LOAD_STR                 'SCRIPT_NAME'
              480  STORE_SUBSCR     

 L.1096       482  LOAD_FAST                'query'
          484_486  POP_JUMP_IF_FALSE   496  'to 496'

 L.1097       488  LOAD_FAST                'query'
              490  LOAD_FAST                'env'
              492  LOAD_STR                 'QUERY_STRING'
              494  STORE_SUBSCR     
            496_0  COME_FROM           484  '484'

 L.1098       496  LOAD_FAST                'self'
              498  LOAD_ATTR                client_address
              500  LOAD_CONST               0
              502  BINARY_SUBSCR    
              504  LOAD_FAST                'env'
              506  LOAD_STR                 'REMOTE_ADDR'
              508  STORE_SUBSCR     

 L.1099       510  LOAD_FAST                'self'
              512  LOAD_ATTR                headers
              514  LOAD_METHOD              get
              516  LOAD_STR                 'authorization'
              518  CALL_METHOD_1         1  ''
              520  STORE_FAST               'authorization'

 L.1100       522  LOAD_FAST                'authorization'
          524_526  POP_JUMP_IF_FALSE   696  'to 696'

 L.1101       528  LOAD_FAST                'authorization'
              530  LOAD_METHOD              split
              532  CALL_METHOD_0         0  ''
              534  STORE_FAST               'authorization'

 L.1102       536  LOAD_GLOBAL              len
              538  LOAD_FAST                'authorization'
              540  CALL_FUNCTION_1       1  ''
              542  LOAD_CONST               2
              544  COMPARE_OP               ==
          546_548  POP_JUMP_IF_FALSE   696  'to 696'

 L.1103       550  LOAD_CONST               0
              552  LOAD_CONST               None
              554  IMPORT_NAME              base64
              556  STORE_FAST               'base64'
              558  LOAD_CONST               0
              560  LOAD_CONST               None
              562  IMPORT_NAME              binascii
              564  STORE_FAST               'binascii'

 L.1104       566  LOAD_FAST                'authorization'
              568  LOAD_CONST               0
              570  BINARY_SUBSCR    
              572  LOAD_FAST                'env'
              574  LOAD_STR                 'AUTH_TYPE'
              576  STORE_SUBSCR     

 L.1105       578  LOAD_FAST                'authorization'
              580  LOAD_CONST               0
              582  BINARY_SUBSCR    
              584  LOAD_METHOD              lower
              586  CALL_METHOD_0         0  ''
              588  LOAD_STR                 'basic'
              590  COMPARE_OP               ==
          592_594  POP_JUMP_IF_FALSE   696  'to 696'

 L.1106       596  SETUP_FINALLY       632  'to 632'

 L.1107       598  LOAD_FAST                'authorization'
              600  LOAD_CONST               1
              602  BINARY_SUBSCR    
              604  LOAD_METHOD              encode
              606  LOAD_STR                 'ascii'
              608  CALL_METHOD_1         1  ''
              610  STORE_FAST               'authorization'

 L.1108       612  LOAD_FAST                'base64'
              614  LOAD_METHOD              decodebytes
              616  LOAD_FAST                'authorization'
              618  CALL_METHOD_1         1  ''
              620  LOAD_METHOD              decode

 L.1109       622  LOAD_STR                 'ascii'

 L.1108       624  CALL_METHOD_1         1  ''
              626  STORE_FAST               'authorization'
              628  POP_BLOCK        
              630  JUMP_FORWARD        660  'to 660'
            632_0  COME_FROM_FINALLY   596  '596'

 L.1110       632  DUP_TOP          
              634  LOAD_FAST                'binascii'
              636  LOAD_ATTR                Error
              638  LOAD_GLOBAL              UnicodeError
              640  BUILD_TUPLE_2         2 
              642  COMPARE_OP               exception-match
          644_646  POP_JUMP_IF_FALSE   658  'to 658'
              648  POP_TOP          
              650  POP_TOP          
              652  POP_TOP          

 L.1111       654  POP_EXCEPT       
              656  JUMP_FORWARD        696  'to 696'
            658_0  COME_FROM           644  '644'
              658  END_FINALLY      
            660_0  COME_FROM           630  '630'

 L.1113       660  LOAD_FAST                'authorization'
              662  LOAD_METHOD              split
              664  LOAD_STR                 ':'
              666  CALL_METHOD_1         1  ''
              668  STORE_FAST               'authorization'

 L.1114       670  LOAD_GLOBAL              len
              672  LOAD_FAST                'authorization'
              674  CALL_FUNCTION_1       1  ''
              676  LOAD_CONST               2
              678  COMPARE_OP               ==
          680_682  POP_JUMP_IF_FALSE   696  'to 696'

 L.1115       684  LOAD_FAST                'authorization'
              686  LOAD_CONST               0
              688  BINARY_SUBSCR    
              690  LOAD_FAST                'env'
              692  LOAD_STR                 'REMOTE_USER'
              694  STORE_SUBSCR     
            696_0  COME_FROM           680  '680'
            696_1  COME_FROM           656  '656'
            696_2  COME_FROM           592  '592'
            696_3  COME_FROM           546  '546'
            696_4  COME_FROM           524  '524'

 L.1117       696  LOAD_FAST                'self'
              698  LOAD_ATTR                headers
              700  LOAD_METHOD              get
              702  LOAD_STR                 'content-type'
              704  CALL_METHOD_1         1  ''
              706  LOAD_CONST               None
              708  COMPARE_OP               is
          710_712  POP_JUMP_IF_FALSE   730  'to 730'

 L.1118       714  LOAD_FAST                'self'
              716  LOAD_ATTR                headers
              718  LOAD_METHOD              get_content_type
              720  CALL_METHOD_0         0  ''
              722  LOAD_FAST                'env'
              724  LOAD_STR                 'CONTENT_TYPE'
              726  STORE_SUBSCR     
              728  JUMP_FORWARD        744  'to 744'
            730_0  COME_FROM           710  '710'

 L.1120       730  LOAD_FAST                'self'
              732  LOAD_ATTR                headers
              734  LOAD_STR                 'content-type'
              736  BINARY_SUBSCR    
              738  LOAD_FAST                'env'
              740  LOAD_STR                 'CONTENT_TYPE'
              742  STORE_SUBSCR     
            744_0  COME_FROM           728  '728'

 L.1121       744  LOAD_FAST                'self'
              746  LOAD_ATTR                headers
              748  LOAD_METHOD              get
              750  LOAD_STR                 'content-length'
              752  CALL_METHOD_1         1  ''
              754  STORE_FAST               'length'

 L.1122       756  LOAD_FAST                'length'
          758_760  POP_JUMP_IF_FALSE   770  'to 770'

 L.1123       762  LOAD_FAST                'length'
              764  LOAD_FAST                'env'
              766  LOAD_STR                 'CONTENT_LENGTH'
              768  STORE_SUBSCR     
            770_0  COME_FROM           758  '758'

 L.1124       770  LOAD_FAST                'self'
              772  LOAD_ATTR                headers
              774  LOAD_METHOD              get
              776  LOAD_STR                 'referer'
              778  CALL_METHOD_1         1  ''
              780  STORE_FAST               'referer'

 L.1125       782  LOAD_FAST                'referer'
          784_786  POP_JUMP_IF_FALSE   796  'to 796'

 L.1126       788  LOAD_FAST                'referer'
              790  LOAD_FAST                'env'
              792  LOAD_STR                 'HTTP_REFERER'
              794  STORE_SUBSCR     
            796_0  COME_FROM           784  '784'

 L.1127       796  BUILD_LIST_0          0 
              798  STORE_FAST               'accept'

 L.1128       800  LOAD_FAST                'self'
              802  LOAD_ATTR                headers
              804  LOAD_METHOD              getallmatchingheaders
              806  LOAD_STR                 'accept'
              808  CALL_METHOD_1         1  ''
              810  GET_ITER         
              812  FOR_ITER            876  'to 876'
              814  STORE_FAST               'line'

 L.1129       816  LOAD_FAST                'line'
              818  LOAD_CONST               None
              820  LOAD_CONST               1
              822  BUILD_SLICE_2         2 
              824  BINARY_SUBSCR    
              826  LOAD_STR                 '\t\n\r '
              828  COMPARE_OP               in
          830_832  POP_JUMP_IF_FALSE   850  'to 850'

 L.1130       834  LOAD_FAST                'accept'
              836  LOAD_METHOD              append
              838  LOAD_FAST                'line'
              840  LOAD_METHOD              strip
              842  CALL_METHOD_0         0  ''
              844  CALL_METHOD_1         1  ''
              846  POP_TOP          
              848  JUMP_BACK           812  'to 812'
            850_0  COME_FROM           830  '830'

 L.1132       850  LOAD_FAST                'accept'
              852  LOAD_FAST                'line'
              854  LOAD_CONST               7
              856  LOAD_CONST               None
              858  BUILD_SLICE_2         2 
              860  BINARY_SUBSCR    
              862  LOAD_METHOD              split
              864  LOAD_STR                 ','
              866  CALL_METHOD_1         1  ''
              868  BINARY_ADD       
              870  STORE_FAST               'accept'
          872_874  JUMP_BACK           812  'to 812'

 L.1133       876  LOAD_STR                 ','
              878  LOAD_METHOD              join
              880  LOAD_FAST                'accept'
              882  CALL_METHOD_1         1  ''
              884  LOAD_FAST                'env'
              886  LOAD_STR                 'HTTP_ACCEPT'
              888  STORE_SUBSCR     

 L.1134       890  LOAD_FAST                'self'
              892  LOAD_ATTR                headers
              894  LOAD_METHOD              get
              896  LOAD_STR                 'user-agent'
              898  CALL_METHOD_1         1  ''
              900  STORE_FAST               'ua'

 L.1135       902  LOAD_FAST                'ua'
          904_906  POP_JUMP_IF_FALSE   916  'to 916'

 L.1136       908  LOAD_FAST                'ua'
              910  LOAD_FAST                'env'
              912  LOAD_STR                 'HTTP_USER_AGENT'
              914  STORE_SUBSCR     
            916_0  COME_FROM           904  '904'

 L.1137       916  LOAD_GLOBAL              filter
              918  LOAD_CONST               None
              920  LOAD_FAST                'self'
              922  LOAD_ATTR                headers
              924  LOAD_METHOD              get_all
              926  LOAD_STR                 'cookie'
              928  BUILD_LIST_0          0 
              930  CALL_METHOD_2         2  ''
              932  CALL_FUNCTION_2       2  ''
              934  STORE_FAST               'co'

 L.1138       936  LOAD_STR                 ', '
              938  LOAD_METHOD              join
              940  LOAD_FAST                'co'
              942  CALL_METHOD_1         1  ''
              944  STORE_FAST               'cookie_str'

 L.1139       946  LOAD_FAST                'cookie_str'
          948_950  POP_JUMP_IF_FALSE   960  'to 960'

 L.1140       952  LOAD_FAST                'cookie_str'
              954  LOAD_FAST                'env'
              956  LOAD_STR                 'HTTP_COOKIE'
              958  STORE_SUBSCR     
            960_0  COME_FROM           948  '948'

 L.1144       960  LOAD_CONST               ('QUERY_STRING', 'REMOTE_HOST', 'CONTENT_LENGTH', 'HTTP_USER_AGENT', 'HTTP_COOKIE', 'HTTP_REFERER')
              962  GET_ITER         
              964  FOR_ITER            984  'to 984'
              966  STORE_FAST               'k'

 L.1146       968  LOAD_FAST                'env'
              970  LOAD_METHOD              setdefault
              972  LOAD_FAST                'k'
              974  LOAD_STR                 ''
              976  CALL_METHOD_2         2  ''
              978  POP_TOP          
          980_982  JUMP_BACK           964  'to 964'

 L.1148       984  LOAD_FAST                'self'
              986  LOAD_METHOD              send_response
              988  LOAD_GLOBAL              HTTPStatus
              990  LOAD_ATTR                OK
              992  LOAD_STR                 'Script output follows'
              994  CALL_METHOD_2         2  ''
              996  POP_TOP          

 L.1149       998  LOAD_FAST                'self'
             1000  LOAD_METHOD              flush_headers
             1002  CALL_METHOD_0         0  ''
             1004  POP_TOP          

 L.1151      1006  LOAD_FAST                'query'
             1008  LOAD_METHOD              replace
             1010  LOAD_STR                 '+'
             1012  LOAD_STR                 ' '
             1014  CALL_METHOD_2         2  ''
             1016  STORE_FAST               'decoded_query'

 L.1153      1018  LOAD_FAST                'self'
             1020  LOAD_ATTR                have_fork
         1022_1024  POP_JUMP_IF_FALSE  1310  'to 1310'

 L.1155      1026  LOAD_FAST                'script'
             1028  BUILD_LIST_1          1 
             1030  STORE_FAST               'args'

 L.1156      1032  LOAD_STR                 '='
             1034  LOAD_FAST                'decoded_query'
             1036  COMPARE_OP               not-in
         1038_1040  POP_JUMP_IF_FALSE  1052  'to 1052'

 L.1157      1042  LOAD_FAST                'args'
             1044  LOAD_METHOD              append
             1046  LOAD_FAST                'decoded_query'
             1048  CALL_METHOD_1         1  ''
             1050  POP_TOP          
           1052_0  COME_FROM          1038  '1038'

 L.1158      1052  LOAD_GLOBAL              nobody_uid
             1054  CALL_FUNCTION_0       0  ''
             1056  STORE_FAST               'nobody'

 L.1159      1058  LOAD_FAST                'self'
             1060  LOAD_ATTR                wfile
             1062  LOAD_METHOD              flush
             1064  CALL_METHOD_0         0  ''
             1066  POP_TOP          

 L.1160      1068  LOAD_GLOBAL              os
             1070  LOAD_METHOD              fork
             1072  CALL_METHOD_0         0  ''
             1074  STORE_FAST               'pid'

 L.1161      1076  LOAD_FAST                'pid'
             1078  LOAD_CONST               0
             1080  COMPARE_OP               !=
         1082_1084  POP_JUMP_IF_FALSE  1172  'to 1172'

 L.1163      1086  LOAD_GLOBAL              os
             1088  LOAD_METHOD              waitpid
             1090  LOAD_FAST                'pid'
             1092  LOAD_CONST               0
             1094  CALL_METHOD_2         2  ''
             1096  UNPACK_SEQUENCE_2     2 
             1098  STORE_FAST               'pid'
             1100  STORE_FAST               'sts'
           1102_0  COME_FROM          1138  '1138'

 L.1165      1102  LOAD_GLOBAL              select
             1104  LOAD_METHOD              select
             1106  LOAD_FAST                'self'
             1108  LOAD_ATTR                rfile
             1110  BUILD_LIST_1          1 
             1112  BUILD_LIST_0          0 
             1114  BUILD_LIST_0          0 
             1116  LOAD_CONST               0
             1118  CALL_METHOD_4         4  ''
             1120  LOAD_CONST               0
             1122  BINARY_SUBSCR    
         1124_1126  POP_JUMP_IF_FALSE  1150  'to 1150'

 L.1166      1128  LOAD_FAST                'self'
             1130  LOAD_ATTR                rfile
             1132  LOAD_METHOD              read
             1134  LOAD_CONST               1
             1136  CALL_METHOD_1         1  ''
         1138_1140  POP_JUMP_IF_TRUE   1102  'to 1102'

 L.1167  1142_1144  BREAK_LOOP         1150  'to 1150'
         1146_1148  JUMP_BACK          1102  'to 1102'
           1150_0  COME_FROM          1124  '1124'

 L.1168      1150  LOAD_FAST                'sts'
         1152_1154  POP_JUMP_IF_FALSE  1168  'to 1168'

 L.1169      1156  LOAD_FAST                'self'
             1158  LOAD_METHOD              log_error
             1160  LOAD_STR                 'CGI script exit status %#x'
             1162  LOAD_FAST                'sts'
             1164  CALL_METHOD_2         2  ''
             1166  POP_TOP          
           1168_0  COME_FROM          1152  '1152'

 L.1170      1168  LOAD_CONST               None
             1170  RETURN_VALUE     
           1172_0  COME_FROM          1082  '1082'

 L.1172      1172  SETUP_FINALLY      1266  'to 1266'

 L.1173      1174  SETUP_FINALLY      1190  'to 1190'

 L.1174      1176  LOAD_GLOBAL              os
             1178  LOAD_METHOD              setuid
             1180  LOAD_FAST                'nobody'
             1182  CALL_METHOD_1         1  ''
             1184  POP_TOP          
             1186  POP_BLOCK        
             1188  JUMP_FORWARD       1212  'to 1212'
           1190_0  COME_FROM_FINALLY  1174  '1174'

 L.1175      1190  DUP_TOP          
             1192  LOAD_GLOBAL              OSError
             1194  COMPARE_OP               exception-match
         1196_1198  POP_JUMP_IF_FALSE  1210  'to 1210'
             1200  POP_TOP          
             1202  POP_TOP          
             1204  POP_TOP          

 L.1176      1206  POP_EXCEPT       
             1208  JUMP_FORWARD       1212  'to 1212'
           1210_0  COME_FROM          1196  '1196'
             1210  END_FINALLY      
           1212_0  COME_FROM          1208  '1208'
           1212_1  COME_FROM          1188  '1188'

 L.1177      1212  LOAD_GLOBAL              os
             1214  LOAD_METHOD              dup2
             1216  LOAD_FAST                'self'
             1218  LOAD_ATTR                rfile
             1220  LOAD_METHOD              fileno
             1222  CALL_METHOD_0         0  ''
             1224  LOAD_CONST               0
             1226  CALL_METHOD_2         2  ''
             1228  POP_TOP          

 L.1178      1230  LOAD_GLOBAL              os
             1232  LOAD_METHOD              dup2
             1234  LOAD_FAST                'self'
             1236  LOAD_ATTR                wfile
             1238  LOAD_METHOD              fileno
             1240  CALL_METHOD_0         0  ''
             1242  LOAD_CONST               1
             1244  CALL_METHOD_2         2  ''
             1246  POP_TOP          

 L.1179      1248  LOAD_GLOBAL              os
             1250  LOAD_METHOD              execve
             1252  LOAD_FAST                'scriptfile'
             1254  LOAD_FAST                'args'
             1256  LOAD_FAST                'env'
             1258  CALL_METHOD_3         3  ''
             1260  POP_TOP          
             1262  POP_BLOCK        
             1264  JUMP_FORWARD       1698  'to 1698'
           1266_0  COME_FROM_FINALLY  1172  '1172'

 L.1180      1266  POP_TOP          
             1268  POP_TOP          
             1270  POP_TOP          

 L.1181      1272  LOAD_FAST                'self'
             1274  LOAD_ATTR                server
             1276  LOAD_METHOD              handle_error
             1278  LOAD_FAST                'self'
             1280  LOAD_ATTR                request
             1282  LOAD_FAST                'self'
             1284  LOAD_ATTR                client_address
             1286  CALL_METHOD_2         2  ''
             1288  POP_TOP          

 L.1182      1290  LOAD_GLOBAL              os
             1292  LOAD_METHOD              _exit
             1294  LOAD_CONST               127
             1296  CALL_METHOD_1         1  ''
             1298  POP_TOP          
             1300  POP_EXCEPT       
             1302  JUMP_FORWARD       1698  'to 1698'
             1304  END_FINALLY      
         1306_1308  JUMP_FORWARD       1698  'to 1698'
           1310_0  COME_FROM          1022  '1022'

 L.1186      1310  LOAD_CONST               0
             1312  LOAD_CONST               None
             1314  IMPORT_NAME              subprocess
             1316  STORE_FAST               'subprocess'

 L.1187      1318  LOAD_FAST                'scriptfile'
             1320  BUILD_LIST_1          1 
             1322  STORE_FAST               'cmdline'

 L.1188      1324  LOAD_FAST                'self'
             1326  LOAD_METHOD              is_python
             1328  LOAD_FAST                'scriptfile'
             1330  CALL_METHOD_1         1  ''
         1332_1334  POP_JUMP_IF_FALSE  1394  'to 1394'

 L.1189      1336  LOAD_GLOBAL              sys
             1338  LOAD_ATTR                executable
             1340  STORE_FAST               'interp'

 L.1190      1342  LOAD_FAST                'interp'
             1344  LOAD_METHOD              lower
             1346  CALL_METHOD_0         0  ''
             1348  LOAD_METHOD              endswith
             1350  LOAD_STR                 'w.exe'
             1352  CALL_METHOD_1         1  ''
         1354_1356  POP_JUMP_IF_FALSE  1382  'to 1382'

 L.1192      1358  LOAD_FAST                'interp'
             1360  LOAD_CONST               None
             1362  LOAD_CONST               -5
             1364  BUILD_SLICE_2         2 
             1366  BINARY_SUBSCR    
             1368  LOAD_FAST                'interp'
             1370  LOAD_CONST               -4
             1372  LOAD_CONST               None
             1374  BUILD_SLICE_2         2 
             1376  BINARY_SUBSCR    
             1378  BINARY_ADD       
             1380  STORE_FAST               'interp'
           1382_0  COME_FROM          1354  '1354'

 L.1193      1382  LOAD_FAST                'interp'
             1384  LOAD_STR                 '-u'
             1386  BUILD_LIST_2          2 
             1388  LOAD_FAST                'cmdline'
             1390  BINARY_ADD       
             1392  STORE_FAST               'cmdline'
           1394_0  COME_FROM          1332  '1332'

 L.1194      1394  LOAD_STR                 '='
             1396  LOAD_FAST                'query'
             1398  COMPARE_OP               not-in
         1400_1402  POP_JUMP_IF_FALSE  1414  'to 1414'

 L.1195      1404  LOAD_FAST                'cmdline'
             1406  LOAD_METHOD              append
             1408  LOAD_FAST                'query'
             1410  CALL_METHOD_1         1  ''
             1412  POP_TOP          
           1414_0  COME_FROM          1400  '1400'

 L.1196      1414  LOAD_FAST                'self'
             1416  LOAD_METHOD              log_message
             1418  LOAD_STR                 'command: %s'
             1420  LOAD_FAST                'subprocess'
             1422  LOAD_METHOD              list2cmdline
             1424  LOAD_FAST                'cmdline'
             1426  CALL_METHOD_1         1  ''
             1428  CALL_METHOD_2         2  ''
             1430  POP_TOP          

 L.1197      1432  SETUP_FINALLY      1446  'to 1446'

 L.1198      1434  LOAD_GLOBAL              int
             1436  LOAD_FAST                'length'
             1438  CALL_FUNCTION_1       1  ''
             1440  STORE_FAST               'nbytes'
             1442  POP_BLOCK        
             1444  JUMP_FORWARD       1476  'to 1476'
           1446_0  COME_FROM_FINALLY  1432  '1432'

 L.1199      1446  DUP_TOP          
             1448  LOAD_GLOBAL              TypeError
             1450  LOAD_GLOBAL              ValueError
             1452  BUILD_TUPLE_2         2 
             1454  COMPARE_OP               exception-match
         1456_1458  POP_JUMP_IF_FALSE  1474  'to 1474'
             1460  POP_TOP          
             1462  POP_TOP          
             1464  POP_TOP          

 L.1200      1466  LOAD_CONST               0
             1468  STORE_FAST               'nbytes'
             1470  POP_EXCEPT       
             1472  JUMP_FORWARD       1476  'to 1476'
           1474_0  COME_FROM          1456  '1456'
             1474  END_FINALLY      
           1476_0  COME_FROM          1472  '1472'
           1476_1  COME_FROM          1444  '1444'

 L.1201      1476  LOAD_FAST                'subprocess'
             1478  LOAD_ATTR                Popen
             1480  LOAD_FAST                'cmdline'

 L.1202      1482  LOAD_FAST                'subprocess'
             1484  LOAD_ATTR                PIPE

 L.1203      1486  LOAD_FAST                'subprocess'
             1488  LOAD_ATTR                PIPE

 L.1204      1490  LOAD_FAST                'subprocess'
             1492  LOAD_ATTR                PIPE

 L.1205      1494  LOAD_FAST                'env'

 L.1201      1496  LOAD_CONST               ('stdin', 'stdout', 'stderr', 'env')
             1498  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1500  STORE_FAST               'p'

 L.1207      1502  LOAD_FAST                'self'
             1504  LOAD_ATTR                command
             1506  LOAD_METHOD              lower
             1508  CALL_METHOD_0         0  ''
             1510  LOAD_STR                 'post'
             1512  COMPARE_OP               ==
         1514_1516  POP_JUMP_IF_FALSE  1542  'to 1542'
             1518  LOAD_FAST                'nbytes'
             1520  LOAD_CONST               0
             1522  COMPARE_OP               >
         1524_1526  POP_JUMP_IF_FALSE  1542  'to 1542'

 L.1208      1528  LOAD_FAST                'self'
             1530  LOAD_ATTR                rfile
             1532  LOAD_METHOD              read
             1534  LOAD_FAST                'nbytes'
             1536  CALL_METHOD_1         1  ''
             1538  STORE_FAST               'data'
             1540  JUMP_FORWARD       1546  'to 1546'
           1542_0  COME_FROM          1524  '1524'
           1542_1  COME_FROM          1514  '1514'

 L.1210      1542  LOAD_CONST               None
             1544  STORE_FAST               'data'
           1546_0  COME_FROM          1586  '1586'
           1546_1  COME_FROM          1540  '1540'

 L.1212      1546  LOAD_GLOBAL              select
             1548  LOAD_METHOD              select
             1550  LOAD_FAST                'self'
             1552  LOAD_ATTR                rfile
             1554  LOAD_ATTR                _sock
             1556  BUILD_LIST_1          1 
             1558  BUILD_LIST_0          0 
             1560  BUILD_LIST_0          0 
             1562  LOAD_CONST               0
             1564  CALL_METHOD_4         4  ''
             1566  LOAD_CONST               0
             1568  BINARY_SUBSCR    
         1570_1572  POP_JUMP_IF_FALSE  1598  'to 1598'

 L.1213      1574  LOAD_FAST                'self'
             1576  LOAD_ATTR                rfile
             1578  LOAD_ATTR                _sock
             1580  LOAD_METHOD              recv
             1582  LOAD_CONST               1
             1584  CALL_METHOD_1         1  ''
         1586_1588  POP_JUMP_IF_TRUE   1546  'to 1546'

 L.1214  1590_1592  BREAK_LOOP         1598  'to 1598'
         1594_1596  JUMP_BACK          1546  'to 1546'
           1598_0  COME_FROM          1570  '1570'

 L.1215      1598  LOAD_FAST                'p'
             1600  LOAD_METHOD              communicate
             1602  LOAD_FAST                'data'
             1604  CALL_METHOD_1         1  ''
             1606  UNPACK_SEQUENCE_2     2 
             1608  STORE_FAST               'stdout'
             1610  STORE_FAST               'stderr'

 L.1216      1612  LOAD_FAST                'self'
             1614  LOAD_ATTR                wfile
             1616  LOAD_METHOD              write
             1618  LOAD_FAST                'stdout'
             1620  CALL_METHOD_1         1  ''
             1622  POP_TOP          

 L.1217      1624  LOAD_FAST                'stderr'
         1626_1628  POP_JUMP_IF_FALSE  1642  'to 1642'

 L.1218      1630  LOAD_FAST                'self'
             1632  LOAD_METHOD              log_error
             1634  LOAD_STR                 '%s'
             1636  LOAD_FAST                'stderr'
             1638  CALL_METHOD_2         2  ''
             1640  POP_TOP          
           1642_0  COME_FROM          1626  '1626'

 L.1219      1642  LOAD_FAST                'p'
             1644  LOAD_ATTR                stderr
             1646  LOAD_METHOD              close
             1648  CALL_METHOD_0         0  ''
             1650  POP_TOP          

 L.1220      1652  LOAD_FAST                'p'
           1654_0  COME_FROM          1264  '1264'
             1654  LOAD_ATTR                stdout
             1656  LOAD_METHOD              close
             1658  CALL_METHOD_0         0  ''
             1660  POP_TOP          

 L.1221      1662  LOAD_FAST                'p'
             1664  LOAD_ATTR                returncode
             1666  STORE_FAST               'status'

 L.1222      1668  LOAD_FAST                'status'
         1670_1672  POP_JUMP_IF_FALSE  1688  'to 1688'

 L.1223      1674  LOAD_FAST                'self'
             1676  LOAD_METHOD              log_error
             1678  LOAD_STR                 'CGI script exit status %#x'
             1680  LOAD_FAST                'status'
             1682  CALL_METHOD_2         2  ''
             1684  POP_TOP          
             1686  JUMP_FORWARD       1698  'to 1698'
           1688_0  COME_FROM          1670  '1670'

 L.1225      1688  LOAD_FAST                'self'
             1690  LOAD_METHOD              log_message
           1692_0  COME_FROM          1302  '1302'
             1692  LOAD_STR                 'CGI script exited OK'
             1694  CALL_METHOD_1         1  ''
             1696  POP_TOP          
           1698_0  COME_FROM          1686  '1686'
           1698_1  COME_FROM          1306  '1306'

Parse error at or near `LOAD_ATTR' instruction at offset 1654


def _get_best_family(*address):
    infos = (socket.getaddrinfo)(*address, type=socket.SOCK_STREAM, 
     flags=socket.AI_PASSIVE)
    family, type, proto, canonname, sockaddr = next(iter(infos))
    return (family, sockaddr)


def test(HandlerClass=BaseHTTPRequestHandler, ServerClass=ThreadingHTTPServer, protocol='HTTP/1.0', port=8000, bind=None):
    """Test the HTTP request handler class.

    This runs an HTTP server on port 8000 (or the port argument).

    """
    ServerClass.address_family, addr = _get_best_familybindport
    HandlerClass.protocol_version = protocol
    with ServerClassaddrHandlerClass as (httpd):
        host, port = httpd.socket.getsockname()[:2]
        url_host = f"[{host}]" if ':' in host else host
        print(f"Serving HTTP on {host} port {port} (http://{url_host}:{port}/) ...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\nKeyboard interrupt received, exiting.')
            sys.exit(0)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--cgi', action='store_true', help='Run as CGI Server')
    parser.add_argument('--bind', '-b', metavar='ADDRESS', help='Specify alternate bind address [default: all interfaces]')
    parser.add_argument('--directory', '-d', default=(os.getcwd()), help='Specify alternative directory [default:current directory]')
    parser.add_argument('port', action='store', default=8000,
      type=int,
      nargs='?',
      help='Specify alternate port [default: 8000]')
    args = parser.parse_args()
    if args.cgi:
        handler_class = CGIHTTPRequestHandler
    else:
        handler_class = partial(SimpleHTTPRequestHandler, directory=(args.directory))

    class DualStackServer(ThreadingHTTPServer):

        def server_bind(self):
            with contextlib.suppress(Exception):
                self.socket.setsockoptsocket.IPPROTO_IPV6socket.IPV6_V6ONLY0
            return super.server_bind()


    test(HandlerClass=handler_class,
      ServerClass=DualStackServer,
      port=(args.port),
      bind=(args.bind))