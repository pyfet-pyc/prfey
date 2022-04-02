# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: urllib3\util\ssltransport.py
import io, socket, ssl
from urllib3.exceptions import ProxySchemeUnsupported
from urllib3.packages import six
SSL_BLOCKSIZE = 16384

class SSLTransport:
    __doc__ = "\n    The SSLTransport wraps an existing socket and establishes an SSL connection.\n\n    Contrary to Python's implementation of SSLSocket, it allows you to chain\n    multiple TLS connections together. It's particularly useful if you need to\n    implement TLS within TLS.\n\n    The class supports most of the socket API operations.\n    "

    @staticmethod
    def _validate_ssl_context_for_tls_in_tls(ssl_context):
        """
        Raises a ProxySchemeUnsupported if the provided ssl_context can't be used
        for TLS in TLS.

        The only requirement is that the ssl_context provides the 'wrap_bio'
        methods.
        """
        if not hasattr(ssl_context, 'wrap_bio'):
            if six.PY2:
                raise ProxySchemeUnsupported("TLS in TLS requires SSLContext.wrap_bio() which isn't supported on Python 2")
            else:
                raise ProxySchemeUnsupported("TLS in TLS requires SSLContext.wrap_bio() which isn't available on non-native SSLContext")

    def __init__(self, socket, ssl_context, server_hostname=None, suppress_ragged_eofs=True):
        """
        Create an SSLTransport around socket using the provided ssl_context.
        """
        self.incoming = ssl.MemoryBIO()
        self.outgoing = ssl.MemoryBIO()
        self.suppress_ragged_eofs = suppress_ragged_eofs
        self.socket = socket
        self.sslobj = ssl_context.wrap_bio((self.incoming),
          (self.outgoing), server_hostname=server_hostname)
        self._ssl_io_loop(self.sslobj.do_handshake)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def fileno(self):
        return self.socket.fileno()

    def read(self, len=1024, buffer=None):
        return self._wrap_ssl_read(len, buffer)

    def recv(self, len=1024, flags=0):
        if flags != 0:
            raise ValueError('non-zero flags not allowed in calls to recv')
        return self._wrap_ssl_read(len)

    def recv_into--- This code section failed: ---

 L.  81         0  LOAD_FAST                'flags'
                2  LOAD_CONST               0
                4  COMPARE_OP               !=
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.  82         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'non-zero flags not allowed in calls to recv_into'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L.  83        16  LOAD_FAST                'buffer'
               18  POP_JUMP_IF_FALSE    38  'to 38'
               20  LOAD_FAST                'nbytes'
               22  LOAD_CONST               None
               24  <117>                 0  ''
               26  POP_JUMP_IF_FALSE    38  'to 38'

 L.  84        28  LOAD_GLOBAL              len
               30  LOAD_FAST                'buffer'
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'nbytes'
               36  JUMP_FORWARD         50  'to 50'
             38_0  COME_FROM            26  '26'
             38_1  COME_FROM            18  '18'

 L.  85        38  LOAD_FAST                'nbytes'
               40  LOAD_CONST               None
               42  <117>                 0  ''
               44  POP_JUMP_IF_FALSE    50  'to 50'

 L.  86        46  LOAD_CONST               1024
               48  STORE_FAST               'nbytes'
             50_0  COME_FROM            44  '44'
             50_1  COME_FROM            36  '36'

 L.  87        50  LOAD_FAST                'self'
               52  LOAD_METHOD              read
               54  LOAD_FAST                'nbytes'
               56  LOAD_FAST                'buffer'
               58  CALL_METHOD_2         2  ''
               60  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 24

    def sendall--- This code section failed: ---

 L.  90         0  LOAD_FAST                'flags'
                2  LOAD_CONST               0
                4  COMPARE_OP               !=
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.  91         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'non-zero flags not allowed in calls to sendall'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L.  92        16  LOAD_CONST               0
               18  STORE_FAST               'count'

 L.  93        20  LOAD_GLOBAL              memoryview
               22  LOAD_FAST                'data'
               24  CALL_FUNCTION_1       1  ''
               26  SETUP_WITH          130  'to 130'
               28  STORE_FAST               'view'
               30  LOAD_FAST                'view'
               32  LOAD_METHOD              cast
               34  LOAD_STR                 'B'
               36  CALL_METHOD_1         1  ''
               38  SETUP_WITH          100  'to 100'
               40  STORE_FAST               'byte_view'

 L.  94        42  LOAD_GLOBAL              len
               44  LOAD_FAST                'byte_view'
               46  CALL_FUNCTION_1       1  ''
               48  STORE_FAST               'amount'
             50_0  COME_FROM            84  '84'

 L.  95        50  LOAD_FAST                'count'
               52  LOAD_FAST                'amount'
               54  COMPARE_OP               <
               56  POP_JUMP_IF_FALSE    86  'to 86'

 L.  96        58  LOAD_FAST                'self'
               60  LOAD_METHOD              send
               62  LOAD_FAST                'byte_view'
               64  LOAD_FAST                'count'
               66  LOAD_CONST               None
               68  BUILD_SLICE_2         2 
               70  BINARY_SUBSCR    
               72  CALL_METHOD_1         1  ''
               74  STORE_FAST               'v'

 L.  97        76  LOAD_FAST                'count'
               78  LOAD_FAST                'v'
               80  INPLACE_ADD      
               82  STORE_FAST               'count'
               84  JUMP_BACK            50  'to 50'
             86_0  COME_FROM            56  '56'
               86  POP_BLOCK        
               88  LOAD_CONST               None
               90  DUP_TOP          
               92  DUP_TOP          
               94  CALL_FUNCTION_3       3  ''
               96  POP_TOP          
               98  JUMP_FORWARD        116  'to 116'
            100_0  COME_FROM_WITH       38  '38'
              100  <49>             
              102  POP_JUMP_IF_TRUE    106  'to 106'
              104  <48>             
            106_0  COME_FROM           102  '102'
              106  POP_TOP          
              108  POP_TOP          
              110  POP_TOP          
              112  POP_EXCEPT       
              114  POP_TOP          
            116_0  COME_FROM            98  '98'
              116  POP_BLOCK        
              118  LOAD_CONST               None
              120  DUP_TOP          
              122  DUP_TOP          
              124  CALL_FUNCTION_3       3  ''
              126  POP_TOP          
              128  JUMP_FORWARD        146  'to 146'
            130_0  COME_FROM_WITH       26  '26'
              130  <49>             
              132  POP_JUMP_IF_TRUE    136  'to 136'
              134  <48>             
            136_0  COME_FROM           132  '132'
              136  POP_TOP          
              138  POP_TOP          
              140  POP_TOP          
              142  POP_EXCEPT       
              144  POP_TOP          
            146_0  COME_FROM           128  '128'

Parse error at or near `DUP_TOP' instruction at offset 92

    def send(self, data, flags=0):
        if flags != 0:
            raise ValueError('non-zero flags not allowed in calls to send')
        response = self._ssl_io_loop(self.sslobj.write, data)
        return response

    def makefile--- This code section failed: ---

 L. 115         0  LOAD_GLOBAL              set
                2  LOAD_FAST                'mode'
                4  CALL_FUNCTION_1       1  ''
                6  BUILD_SET_0           0 
                8  LOAD_CONST               frozenset({'b', 'w', 'r'})
               10  POP_FINALLY           1  ''
               12  COMPARE_OP               <=
               14  POP_JUMP_IF_TRUE     30  'to 30'

 L. 116        16  LOAD_GLOBAL              ValueError
               18  LOAD_STR                 'invalid mode %r (only r, w, b allowed)'
               20  LOAD_FAST                'mode'
               22  BUILD_TUPLE_1         1 
               24  BINARY_MODULO    
               26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            14  '14'

 L. 118        30  LOAD_STR                 'w'
               32  LOAD_FAST                'mode'
               34  <118>                 0  ''
               36  STORE_FAST               'writing'

 L. 119        38  LOAD_STR                 'r'
               40  LOAD_FAST                'mode'
               42  <118>                 0  ''
               44  JUMP_IF_TRUE_OR_POP    50  'to 50'
               46  LOAD_FAST                'writing'
               48  UNARY_NOT        
             50_0  COME_FROM            44  '44'
               50  STORE_FAST               'reading'

 L. 120        52  LOAD_FAST                'reading'
               54  POP_JUMP_IF_TRUE     64  'to 64'
               56  LOAD_FAST                'writing'
               58  POP_JUMP_IF_TRUE     64  'to 64'
               60  <74>             
               62  RAISE_VARARGS_1       1  'exception instance'
             64_0  COME_FROM            58  '58'
             64_1  COME_FROM            54  '54'

 L. 121        64  LOAD_STR                 'b'
               66  LOAD_FAST                'mode'
               68  <118>                 0  ''
               70  STORE_FAST               'binary'

 L. 122        72  LOAD_STR                 ''
               74  STORE_FAST               'rawmode'

 L. 123        76  LOAD_FAST                'reading'
               78  POP_JUMP_IF_FALSE    88  'to 88'

 L. 124        80  LOAD_FAST                'rawmode'
               82  LOAD_STR                 'r'
               84  INPLACE_ADD      
               86  STORE_FAST               'rawmode'
             88_0  COME_FROM            78  '78'

 L. 125        88  LOAD_FAST                'writing'
               90  POP_JUMP_IF_FALSE   100  'to 100'

 L. 126        92  LOAD_FAST                'rawmode'
               94  LOAD_STR                 'w'
               96  INPLACE_ADD      
               98  STORE_FAST               'rawmode'
            100_0  COME_FROM            90  '90'

 L. 127       100  LOAD_GLOBAL              socket
              102  LOAD_METHOD              SocketIO
              104  LOAD_FAST                'self'
              106  LOAD_FAST                'rawmode'
              108  CALL_METHOD_2         2  ''
              110  STORE_FAST               'raw'

 L. 128       112  LOAD_FAST                'self'
              114  LOAD_ATTR                socket
              116  DUP_TOP          
              118  LOAD_ATTR                _io_refs
              120  LOAD_CONST               1
              122  INPLACE_ADD      
              124  ROT_TWO          
              126  STORE_ATTR               _io_refs

 L. 129       128  LOAD_FAST                'buffering'
              130  LOAD_CONST               None
              132  <117>                 0  ''
              134  POP_JUMP_IF_FALSE   140  'to 140'

 L. 130       136  LOAD_CONST               -1
              138  STORE_FAST               'buffering'
            140_0  COME_FROM           134  '134'

 L. 131       140  LOAD_FAST                'buffering'
              142  LOAD_CONST               0
              144  COMPARE_OP               <
              146  POP_JUMP_IF_FALSE   154  'to 154'

 L. 132       148  LOAD_GLOBAL              io
              150  LOAD_ATTR                DEFAULT_BUFFER_SIZE
              152  STORE_FAST               'buffering'
            154_0  COME_FROM           146  '146'

 L. 133       154  LOAD_FAST                'buffering'
              156  LOAD_CONST               0
              158  COMPARE_OP               ==
              160  POP_JUMP_IF_FALSE   178  'to 178'

 L. 134       162  LOAD_FAST                'binary'
              164  POP_JUMP_IF_TRUE    174  'to 174'

 L. 135       166  LOAD_GLOBAL              ValueError
              168  LOAD_STR                 'unbuffered streams must be binary'
              170  CALL_FUNCTION_1       1  ''
              172  RAISE_VARARGS_1       1  'exception instance'
            174_0  COME_FROM           164  '164'

 L. 136       174  LOAD_FAST                'raw'
              176  RETURN_VALUE     
            178_0  COME_FROM           160  '160'

 L. 137       178  LOAD_FAST                'reading'
              180  POP_JUMP_IF_FALSE   202  'to 202'
              182  LOAD_FAST                'writing'
              184  POP_JUMP_IF_FALSE   202  'to 202'

 L. 138       186  LOAD_GLOBAL              io
              188  LOAD_METHOD              BufferedRWPair
              190  LOAD_FAST                'raw'
              192  LOAD_FAST                'raw'
              194  LOAD_FAST                'buffering'
              196  CALL_METHOD_3         3  ''
              198  STORE_FAST               'buffer'
              200  JUMP_FORWARD        240  'to 240'
            202_0  COME_FROM           184  '184'
            202_1  COME_FROM           180  '180'

 L. 139       202  LOAD_FAST                'reading'
              204  POP_JUMP_IF_FALSE   220  'to 220'

 L. 140       206  LOAD_GLOBAL              io
              208  LOAD_METHOD              BufferedReader
              210  LOAD_FAST                'raw'
              212  LOAD_FAST                'buffering'
              214  CALL_METHOD_2         2  ''
              216  STORE_FAST               'buffer'
              218  JUMP_FORWARD        240  'to 240'
            220_0  COME_FROM           204  '204'

 L. 142       220  LOAD_FAST                'writing'
              222  POP_JUMP_IF_TRUE    228  'to 228'
              224  <74>             
              226  RAISE_VARARGS_1       1  'exception instance'
            228_0  COME_FROM           222  '222'

 L. 143       228  LOAD_GLOBAL              io
              230  LOAD_METHOD              BufferedWriter
              232  LOAD_FAST                'raw'
              234  LOAD_FAST                'buffering'
              236  CALL_METHOD_2         2  ''
              238  STORE_FAST               'buffer'
            240_0  COME_FROM           218  '218'
            240_1  COME_FROM           200  '200'

 L. 144       240  LOAD_FAST                'binary'
              242  POP_JUMP_IF_FALSE   248  'to 248'

 L. 145       244  LOAD_FAST                'buffer'
              246  RETURN_VALUE     
            248_0  COME_FROM           242  '242'

 L. 146       248  LOAD_GLOBAL              io
              250  LOAD_METHOD              TextIOWrapper
              252  LOAD_FAST                'buffer'
              254  LOAD_FAST                'encoding'
              256  LOAD_FAST                'errors'
              258  LOAD_FAST                'newline'
              260  CALL_METHOD_4         4  ''
              262  STORE_FAST               'text'

 L. 147       264  LOAD_FAST                'mode'
              266  LOAD_FAST                'text'
              268  STORE_ATTR               mode

 L. 148       270  LOAD_FAST                'text'
              272  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def unwrap(self):
        self._ssl_io_loop(self.sslobj.unwrap)

    def close(self):
        self.socket.close()

    def getpeercert(self, binary_form=False):
        return self.sslobj.getpeercert(binary_form)

    def version(self):
        return self.sslobj.version()

    def cipher(self):
        return self.sslobj.cipher()

    def selected_alpn_protocol(self):
        return self.sslobj.selected_alpn_protocol()

    def selected_npn_protocol(self):
        return self.sslobj.selected_npn_protocol()

    def shared_ciphers(self):
        return self.sslobj.shared_ciphers()

    def compression(self):
        return self.sslobj.compression()

    def settimeout(self, value):
        self.socket.settimeout(value)

    def gettimeout(self):
        return self.socket.gettimeout()

    def _decref_socketios(self):
        self.socket._decref_socketios()

    def _wrap_ssl_read--- This code section failed: ---

 L. 187         0  SETUP_FINALLY        22  'to 22'

 L. 188         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _ssl_io_loop
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                sslobj
               10  LOAD_ATTR                read
               12  LOAD_FAST                'len'
               14  LOAD_FAST                'buffer'
               16  CALL_METHOD_3         3  ''
               18  POP_BLOCK        
               20  RETURN_VALUE     
             22_0  COME_FROM_FINALLY     0  '0'

 L. 189        22  DUP_TOP          
               24  LOAD_GLOBAL              ssl
               26  LOAD_ATTR                SSLError
               28  <121>                92  ''
               30  POP_TOP          
               32  STORE_FAST               'e'
               34  POP_TOP          
               36  SETUP_FINALLY        84  'to 84'

 L. 190        38  LOAD_FAST                'e'
               40  LOAD_ATTR                errno
               42  LOAD_GLOBAL              ssl
               44  LOAD_ATTR                SSL_ERROR_EOF
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE    70  'to 70'
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                suppress_ragged_eofs
               54  POP_JUMP_IF_FALSE    70  'to 70'

 L. 191        56  POP_BLOCK        
               58  POP_EXCEPT       
               60  LOAD_CONST               None
               62  STORE_FAST               'e'
               64  DELETE_FAST              'e'
               66  LOAD_CONST               0
               68  RETURN_VALUE     
             70_0  COME_FROM            54  '54'
             70_1  COME_FROM            48  '48'

 L. 193        70  RAISE_VARARGS_0       0  'reraise'
               72  POP_BLOCK        
               74  POP_EXCEPT       
               76  LOAD_CONST               None
               78  STORE_FAST               'e'
               80  DELETE_FAST              'e'
               82  JUMP_FORWARD         94  'to 94'
             84_0  COME_FROM_FINALLY    36  '36'
               84  LOAD_CONST               None
               86  STORE_FAST               'e'
               88  DELETE_FAST              'e'
               90  <48>             
               92  <48>             
             94_0  COME_FROM            82  '82'

Parse error at or near `<121>' instruction at offset 28

    def _ssl_io_loop--- This code section failed: ---

 L. 197         0  LOAD_CONST               True
                2  STORE_FAST               'should_loop'

 L. 198         4  LOAD_CONST               None
                6  STORE_FAST               'ret'
              8_0  COME_FROM           182  '182'
              8_1  COME_FROM           170  '170'
              8_2  COME_FROM           140  '140'
              8_3  COME_FROM           130  '130'

 L. 200         8  LOAD_FAST                'should_loop'
               10  POP_JUMP_IF_FALSE   184  'to 184'

 L. 201        12  LOAD_CONST               None
               14  STORE_FAST               'errno'

 L. 202        16  SETUP_FINALLY        30  'to 30'

 L. 203        18  LOAD_FAST                'func'
               20  LOAD_FAST                'args'
               22  CALL_FUNCTION_EX      0  'positional arguments only'
               24  STORE_FAST               'ret'
               26  POP_BLOCK        
               28  JUMP_FORWARD         96  'to 96'
             30_0  COME_FROM_FINALLY    16  '16'

 L. 204        30  DUP_TOP          
               32  LOAD_GLOBAL              ssl
               34  LOAD_ATTR                SSLError
               36  <121>                94  ''
               38  POP_TOP          
               40  STORE_FAST               'e'
               42  POP_TOP          
               44  SETUP_FINALLY        86  'to 86'

 L. 205        46  LOAD_FAST                'e'
               48  LOAD_ATTR                errno
               50  LOAD_GLOBAL              ssl
               52  LOAD_ATTR                SSL_ERROR_WANT_READ
               54  LOAD_GLOBAL              ssl
               56  LOAD_ATTR                SSL_ERROR_WANT_WRITE
               58  BUILD_TUPLE_2         2 
               60  <118>                 1  ''
               62  POP_JUMP_IF_FALSE    68  'to 68'

 L. 207        64  LOAD_FAST                'e'
               66  RAISE_VARARGS_1       1  'exception instance'
             68_0  COME_FROM            62  '62'

 L. 208        68  LOAD_FAST                'e'
               70  LOAD_ATTR                errno
               72  STORE_FAST               'errno'
               74  POP_BLOCK        
               76  POP_EXCEPT       
               78  LOAD_CONST               None
               80  STORE_FAST               'e'
               82  DELETE_FAST              'e'
               84  JUMP_FORWARD         96  'to 96'
             86_0  COME_FROM_FINALLY    44  '44'
               86  LOAD_CONST               None
               88  STORE_FAST               'e'
               90  DELETE_FAST              'e'
               92  <48>             
               94  <48>             
             96_0  COME_FROM            84  '84'
             96_1  COME_FROM            28  '28'

 L. 210        96  LOAD_FAST                'self'
               98  LOAD_ATTR                outgoing
              100  LOAD_METHOD              read
              102  CALL_METHOD_0         0  ''
              104  STORE_FAST               'buf'

 L. 211       106  LOAD_FAST                'self'
              108  LOAD_ATTR                socket
              110  LOAD_METHOD              sendall
              112  LOAD_FAST                'buf'
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          

 L. 213       118  LOAD_FAST                'errno'
              120  LOAD_CONST               None
              122  <117>                 0  ''
              124  POP_JUMP_IF_FALSE   132  'to 132'

 L. 214       126  LOAD_CONST               False
              128  STORE_FAST               'should_loop'
              130  JUMP_BACK             8  'to 8'
            132_0  COME_FROM           124  '124'

 L. 215       132  LOAD_FAST                'errno'
              134  LOAD_GLOBAL              ssl
              136  LOAD_ATTR                SSL_ERROR_WANT_READ
              138  COMPARE_OP               ==
              140  POP_JUMP_IF_FALSE_BACK     8  'to 8'

 L. 216       142  LOAD_FAST                'self'
              144  LOAD_ATTR                socket
              146  LOAD_METHOD              recv
              148  LOAD_GLOBAL              SSL_BLOCKSIZE
              150  CALL_METHOD_1         1  ''
              152  STORE_FAST               'buf'

 L. 217       154  LOAD_FAST                'buf'
              156  POP_JUMP_IF_FALSE   172  'to 172'

 L. 218       158  LOAD_FAST                'self'
              160  LOAD_ATTR                incoming
              162  LOAD_METHOD              write
              164  LOAD_FAST                'buf'
              166  CALL_METHOD_1         1  ''
              168  POP_TOP          
              170  JUMP_BACK             8  'to 8'
            172_0  COME_FROM           156  '156'

 L. 220       172  LOAD_FAST                'self'
              174  LOAD_ATTR                incoming
              176  LOAD_METHOD              write_eof
              178  CALL_METHOD_0         0  ''
              180  POP_TOP          
              182  JUMP_BACK             8  'to 8'
            184_0  COME_FROM            10  '10'

 L. 221       184  LOAD_FAST                'ret'
              186  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 36