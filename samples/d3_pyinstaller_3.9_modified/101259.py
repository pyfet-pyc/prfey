# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: multiprocessing\resource_sharer.py
import os, signal, socket, sys, threading
from . import process
from .context import reduction
from . import util
__all__ = [
 'stop']
if sys.platform == 'win32':
    __all__ += ['DupSocket']

    class DupSocket(object):
        __doc__ = 'Picklable wrapper for a socket.'

        def __init__(self, sock):
            new_sock = sock.dup()

            def send(conn, pid):
                share = new_sock.share(pid)
                conn.send_bytes(share)

            self._id = _resource_sharer.register(send, new_sock.close)

        def detach--- This code section failed: ---

 L.  38         0  LOAD_GLOBAL              _resource_sharer
                2  LOAD_METHOD              get_connection
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _id
                8  CALL_METHOD_1         1  ''
               10  SETUP_WITH           46  'to 46'
               12  STORE_FAST               'conn'

 L.  39        14  LOAD_FAST                'conn'
               16  LOAD_METHOD              recv_bytes
               18  CALL_METHOD_0         0  ''
               20  STORE_FAST               'share'

 L.  40        22  LOAD_GLOBAL              socket
               24  LOAD_METHOD              fromshare
               26  LOAD_FAST                'share'
               28  CALL_METHOD_1         1  ''
               30  POP_BLOCK        
               32  ROT_TWO          
               34  LOAD_CONST               None
               36  DUP_TOP          
               38  DUP_TOP          
               40  CALL_FUNCTION_3       3  ''
               42  POP_TOP          
               44  RETURN_VALUE     
             46_0  COME_FROM_WITH       10  '10'
               46  <49>             
               48  POP_JUMP_IF_TRUE     52  'to 52'
               50  <48>             
             52_0  COME_FROM            48  '48'
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          
               58  POP_EXCEPT       
               60  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 34


else:
    __all__ += ['DupFd']

    class DupFd(object):
        __doc__ = 'Wrapper for fd which can be used at any time.'

        def __init__(self, fd):
            new_fd = os.dup(fd)

            def send(conn, pid):
                reduction.send_handle(conn, new_fd, pid)

            def close():
                os.close(new_fd)

            self._id = _resource_sharer.register(send, close)

        def detach--- This code section failed: ---

 L.  57         0  LOAD_GLOBAL              _resource_sharer
                2  LOAD_METHOD              get_connection
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _id
                8  CALL_METHOD_1         1  ''
               10  SETUP_WITH           38  'to 38'
               12  STORE_FAST               'conn'

 L.  58        14  LOAD_GLOBAL              reduction
               16  LOAD_METHOD              recv_handle
               18  LOAD_FAST                'conn'
               20  CALL_METHOD_1         1  ''
               22  POP_BLOCK        
               24  ROT_TWO          
               26  LOAD_CONST               None
               28  DUP_TOP          
               30  DUP_TOP          
               32  CALL_FUNCTION_3       3  ''
               34  POP_TOP          
               36  RETURN_VALUE     
             38_0  COME_FROM_WITH       10  '10'
               38  <49>             
               40  POP_JUMP_IF_TRUE     44  'to 44'
               42  <48>             
             44_0  COME_FROM            40  '40'
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          
               50  POP_EXCEPT       
               52  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 26


class _ResourceSharer(object):
    __doc__ = 'Manager for resources using background thread.'

    def __init__(self):
        self._key = 0
        self._cache = {}
        self._lock = threading.Lock()
        self._listener = None
        self._address = None
        self._thread = None
        util.register_after_fork(self, _ResourceSharer._afterfork)

    def register--- This code section failed: ---

 L.  74         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _lock
                4  SETUP_WITH           82  'to 82'
                6  POP_TOP          

 L.  75         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _address
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    26  'to 26'

 L.  76        18  LOAD_FAST                'self'
               20  LOAD_METHOD              _start
               22  CALL_METHOD_0         0  ''
               24  POP_TOP          
             26_0  COME_FROM            16  '16'

 L.  77        26  LOAD_FAST                'self'
               28  DUP_TOP          
               30  LOAD_ATTR                _key
               32  LOAD_CONST               1
               34  INPLACE_ADD      
               36  ROT_TWO          
               38  STORE_ATTR               _key

 L.  78        40  LOAD_FAST                'send'
               42  LOAD_FAST                'close'
               44  BUILD_TUPLE_2         2 
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _cache
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                _key
               54  STORE_SUBSCR     

 L.  79        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _address
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                _key
               64  BUILD_TUPLE_2         2 
               66  POP_BLOCK        
               68  ROT_TWO          
               70  LOAD_CONST               None
               72  DUP_TOP          
               74  DUP_TOP          
               76  CALL_FUNCTION_3       3  ''
               78  POP_TOP          
               80  RETURN_VALUE     
             82_0  COME_FROM_WITH        4  '4'
               82  <49>             
               84  POP_JUMP_IF_TRUE     88  'to 88'
               86  <48>             
             88_0  COME_FROM            84  '84'
               88  POP_TOP          
               90  POP_TOP          
               92  POP_TOP          
               94  POP_EXCEPT       
               96  POP_TOP          

Parse error at or near `<117>' instruction at offset 14

    @staticmethod
    def get_connection(ident):
        """Return connection from which to receive identified resource."""
        from .connection import Client
        address, key = ident
        c = Client(address, authkey=(process.current_process().authkey))
        c.send((key, os.getpid()))
        return c

    def stop--- This code section failed: ---

 L.  92         0  LOAD_CONST               1
                2  LOAD_CONST               ('Client',)
                4  IMPORT_NAME              connection
                6  IMPORT_FROM              Client
                8  STORE_FAST               'Client'
               10  POP_TOP          

 L.  93        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _lock
               16  SETUP_WITH          182  'to 182'
               18  POP_TOP          

 L.  94        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _address
               24  LOAD_CONST               None
               26  <117>                 1  ''
               28  POP_JUMP_IF_FALSE   168  'to 168'

 L.  95        30  LOAD_FAST                'Client'
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                _address

 L.  96        36  LOAD_GLOBAL              process
               38  LOAD_METHOD              current_process
               40  CALL_METHOD_0         0  ''
               42  LOAD_ATTR                authkey

 L.  95        44  LOAD_CONST               ('authkey',)
               46  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               48  STORE_FAST               'c'

 L.  97        50  LOAD_FAST                'c'
               52  LOAD_METHOD              send
               54  LOAD_CONST               None
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          

 L.  98        60  LOAD_FAST                'c'
               62  LOAD_METHOD              close
               64  CALL_METHOD_0         0  ''
               66  POP_TOP          

 L.  99        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _thread
               72  LOAD_METHOD              join
               74  LOAD_FAST                'timeout'
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          

 L. 100        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _thread
               84  LOAD_METHOD              is_alive
               86  CALL_METHOD_0         0  ''
               88  POP_JUMP_IF_FALSE   100  'to 100'

 L. 101        90  LOAD_GLOBAL              util
               92  LOAD_METHOD              sub_warning
               94  LOAD_STR                 '_ResourceSharer thread did not stop when asked'
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          
            100_0  COME_FROM            88  '88'

 L. 103       100  LOAD_FAST                'self'
              102  LOAD_ATTR                _listener
              104  LOAD_METHOD              close
              106  CALL_METHOD_0         0  ''
              108  POP_TOP          

 L. 104       110  LOAD_CONST               None
              112  LOAD_FAST                'self'
              114  STORE_ATTR               _thread

 L. 105       116  LOAD_CONST               None
              118  LOAD_FAST                'self'
              120  STORE_ATTR               _address

 L. 106       122  LOAD_CONST               None
              124  LOAD_FAST                'self'
              126  STORE_ATTR               _listener

 L. 107       128  LOAD_FAST                'self'
              130  LOAD_ATTR                _cache
              132  LOAD_METHOD              items
              134  CALL_METHOD_0         0  ''
              136  GET_ITER         
            138_0  COME_FROM           156  '156'
              138  FOR_ITER            158  'to 158'
              140  UNPACK_SEQUENCE_2     2 
              142  STORE_FAST               'key'
              144  UNPACK_SEQUENCE_2     2 
              146  STORE_FAST               'send'
              148  STORE_FAST               'close'

 L. 108       150  LOAD_FAST                'close'
              152  CALL_FUNCTION_0       0  ''
              154  POP_TOP          
              156  JUMP_BACK           138  'to 138'
            158_0  COME_FROM           138  '138'

 L. 109       158  LOAD_FAST                'self'
              160  LOAD_ATTR                _cache
              162  LOAD_METHOD              clear
              164  CALL_METHOD_0         0  ''
              166  POP_TOP          
            168_0  COME_FROM            28  '28'
              168  POP_BLOCK        
              170  LOAD_CONST               None
              172  DUP_TOP          
              174  DUP_TOP          
              176  CALL_FUNCTION_3       3  ''
              178  POP_TOP          
              180  JUMP_FORWARD        198  'to 198'
            182_0  COME_FROM_WITH       16  '16'
              182  <49>             
              184  POP_JUMP_IF_TRUE    188  'to 188'
              186  <48>             
            188_0  COME_FROM           184  '184'
              188  POP_TOP          
              190  POP_TOP          
              192  POP_TOP          
              194  POP_EXCEPT       
              196  POP_TOP          
            198_0  COME_FROM           180  '180'

Parse error at or near `<117>' instruction at offset 26

    def _afterfork--- This code section failed: ---

 L. 112         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _cache
                4  LOAD_METHOD              items
                6  CALL_METHOD_0         0  ''
                8  GET_ITER         
             10_0  COME_FROM            28  '28'
               10  FOR_ITER             30  'to 30'
               12  UNPACK_SEQUENCE_2     2 
               14  STORE_FAST               'key'
               16  UNPACK_SEQUENCE_2     2 
               18  STORE_FAST               'send'
               20  STORE_FAST               'close'

 L. 113        22  LOAD_FAST                'close'
               24  CALL_FUNCTION_0       0  ''
               26  POP_TOP          
               28  JUMP_BACK            10  'to 10'
             30_0  COME_FROM            10  '10'

 L. 114        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _cache
               34  LOAD_METHOD              clear
               36  CALL_METHOD_0         0  ''
               38  POP_TOP          

 L. 115        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _lock
               44  LOAD_METHOD              _at_fork_reinit
               46  CALL_METHOD_0         0  ''
               48  POP_TOP          

 L. 116        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _listener
               54  LOAD_CONST               None
               56  <117>                 1  ''
               58  POP_JUMP_IF_FALSE    70  'to 70'

 L. 117        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _listener
               64  LOAD_METHOD              close
               66  CALL_METHOD_0         0  ''
               68  POP_TOP          
             70_0  COME_FROM            58  '58'

 L. 118        70  LOAD_CONST               None
               72  LOAD_FAST                'self'
               74  STORE_ATTR               _listener

 L. 119        76  LOAD_CONST               None
               78  LOAD_FAST                'self'
               80  STORE_ATTR               _address

 L. 120        82  LOAD_CONST               None
               84  LOAD_FAST                'self'
               86  STORE_ATTR               _thread

Parse error at or near `<117>' instruction at offset 56

    def _start--- This code section failed: ---

 L. 123         0  LOAD_CONST               1
                2  LOAD_CONST               ('Listener',)
                4  IMPORT_NAME              connection
                6  IMPORT_FROM              Listener
                8  STORE_FAST               'Listener'
               10  POP_TOP          

 L. 124        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _listener
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_TRUE     30  'to 30'
               22  <74>             
               24  LOAD_STR                 'Already have Listener'
               26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            20  '20'

 L. 125        30  LOAD_GLOBAL              util
               32  LOAD_METHOD              debug
               34  LOAD_STR                 'starting listener and thread for sending handles'
               36  CALL_METHOD_1         1  ''
               38  POP_TOP          

 L. 126        40  LOAD_FAST                'Listener'
               42  LOAD_GLOBAL              process
               44  LOAD_METHOD              current_process
               46  CALL_METHOD_0         0  ''
               48  LOAD_ATTR                authkey
               50  LOAD_CONST               ('authkey',)
               52  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               54  LOAD_FAST                'self'
               56  STORE_ATTR               _listener

 L. 127        58  LOAD_FAST                'self'
               60  LOAD_ATTR                _listener
               62  LOAD_ATTR                address
               64  LOAD_FAST                'self'
               66  STORE_ATTR               _address

 L. 128        68  LOAD_GLOBAL              threading
               70  LOAD_ATTR                Thread
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                _serve
               76  LOAD_CONST               ('target',)
               78  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               80  STORE_FAST               't'

 L. 129        82  LOAD_CONST               True
               84  LOAD_FAST                't'
               86  STORE_ATTR               daemon

 L. 130        88  LOAD_FAST                't'
               90  LOAD_METHOD              start
               92  CALL_METHOD_0         0  ''
               94  POP_TOP          

 L. 131        96  LOAD_FAST                't'
               98  LOAD_FAST                'self'
              100  STORE_ATTR               _thread

Parse error at or near `<117>' instruction at offset 18

    def _serve--- This code section failed: ---

 L. 134         0  LOAD_GLOBAL              hasattr
                2  LOAD_GLOBAL              signal
                4  LOAD_STR                 'pthread_sigmask'
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    28  'to 28'

 L. 135        10  LOAD_GLOBAL              signal
               12  LOAD_METHOD              pthread_sigmask
               14  LOAD_GLOBAL              signal
               16  LOAD_ATTR                SIG_BLOCK
               18  LOAD_GLOBAL              signal
               20  LOAD_METHOD              valid_signals
               22  CALL_METHOD_0         0  ''
               24  CALL_METHOD_2         2  ''
               26  POP_TOP          
             28_0  COME_FROM           196  '196'
             28_1  COME_FROM           192  '192'
             28_2  COME_FROM           160  '160'
             28_3  COME_FROM             8  '8'

 L. 137        28  SETUP_FINALLY       162  'to 162'

 L. 138        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _listener
               34  LOAD_METHOD              accept
               36  CALL_METHOD_0         0  ''
               38  SETUP_WITH          142  'to 142'
               40  STORE_FAST               'conn'

 L. 139        42  LOAD_FAST                'conn'
               44  LOAD_METHOD              recv
               46  CALL_METHOD_0         0  ''
               48  STORE_FAST               'msg'

 L. 140        50  LOAD_FAST                'msg'
               52  LOAD_CONST               None
               54  <117>                 0  ''
               56  POP_JUMP_IF_FALSE    74  'to 74'

 L. 141        58  POP_BLOCK        
               60  LOAD_CONST               None
               62  DUP_TOP          
               64  DUP_TOP          
               66  CALL_FUNCTION_3       3  ''
               68  POP_TOP          
               70  POP_BLOCK        
               72  JUMP_FORWARD        198  'to 198'
             74_0  COME_FROM            56  '56'

 L. 142        74  LOAD_FAST                'msg'
               76  UNPACK_SEQUENCE_2     2 
               78  STORE_FAST               'key'
               80  STORE_FAST               'destination_pid'

 L. 143        82  LOAD_FAST                'self'
               84  LOAD_ATTR                _cache
               86  LOAD_METHOD              pop
               88  LOAD_FAST                'key'
               90  CALL_METHOD_1         1  ''
               92  UNPACK_SEQUENCE_2     2 
               94  STORE_FAST               'send'
               96  STORE_FAST               'close'

 L. 144        98  SETUP_FINALLY       120  'to 120'

 L. 145       100  LOAD_FAST                'send'
              102  LOAD_FAST                'conn'
              104  LOAD_FAST                'destination_pid'
              106  CALL_FUNCTION_2       2  ''
              108  POP_TOP          
              110  POP_BLOCK        

 L. 147       112  LOAD_FAST                'close'
              114  CALL_FUNCTION_0       0  ''
              116  POP_TOP          
              118  JUMP_FORWARD        128  'to 128'
            120_0  COME_FROM_FINALLY    98  '98'
              120  LOAD_FAST                'close'
              122  CALL_FUNCTION_0       0  ''
              124  POP_TOP          
              126  <48>             
            128_0  COME_FROM           118  '118'
              128  POP_BLOCK        
              130  LOAD_CONST               None
              132  DUP_TOP          
              134  DUP_TOP          
              136  CALL_FUNCTION_3       3  ''
              138  POP_TOP          
              140  JUMP_FORWARD        158  'to 158'
            142_0  COME_FROM_WITH       38  '38'
              142  <49>             
              144  POP_JUMP_IF_TRUE    148  'to 148'
              146  <48>             
            148_0  COME_FROM           144  '144'
              148  POP_TOP          
              150  POP_TOP          
              152  POP_TOP          
              154  POP_EXCEPT       
              156  POP_TOP          
            158_0  COME_FROM           140  '140'
              158  POP_BLOCK        
              160  JUMP_BACK            28  'to 28'
            162_0  COME_FROM_FINALLY    28  '28'

 L. 148       162  POP_TOP          
              164  POP_TOP          
              166  POP_TOP          

 L. 149       168  LOAD_GLOBAL              util
              170  LOAD_METHOD              is_exiting
              172  CALL_METHOD_0         0  ''
              174  POP_JUMP_IF_TRUE    190  'to 190'

 L. 150       176  LOAD_GLOBAL              sys
              178  LOAD_ATTR                excepthook
              180  LOAD_GLOBAL              sys
              182  LOAD_METHOD              exc_info
              184  CALL_METHOD_0         0  ''
              186  CALL_FUNCTION_EX      0  'positional arguments only'
              188  POP_TOP          
            190_0  COME_FROM           174  '174'
              190  POP_EXCEPT       
              192  JUMP_BACK            28  'to 28'
              194  <48>             
              196  JUMP_BACK            28  'to 28'
            198_0  COME_FROM            72  '72'

Parse error at or near `<117>' instruction at offset 54


_resource_sharer = _ResourceSharer()
stop = _resource_sharer.stop